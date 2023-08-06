import dataclasses
import logging
import pathlib
import platform
import re
import secrets
import subprocess
import tarfile
import tempfile
from enum import Enum
from typing import Dict, Iterable, List, Optional

import click
from memfault_cli.authenticator import BasicAuthenticator, OrgTokenAuthenticator
from memfault_cli.context import MemfaultCliClickContext
from memfault_cli.upload import ElfSymbolDirectoryUploader

from .elf import ELFFileInfo, find_elf_files

# See https://docs.yoctoproject.org/overview-manual/concepts.html#package-splitting
# for the directory structure of the Yocto build output.

LOG = logging.getLogger(__name__)


def tmp_path_from_image(image: pathlib.Path) -> pathlib.Path:
    """
    This function returns the resolved tmp/ given a .manifest file's path.
    The .manifest file is created by Yocto in tmp/deploy/images/<arch>/.
    """
    return image.resolve().parent.parent.parent.parent


def should_ignore_elf(elf_info: ELFFileInfo) -> bool:
    if elf_info.path.suffix in {".a", ".o"}:
        LOG.debug("Ignoring %s (static lib / object file)", elf_info.path)
        return True
    # Ignore ptests -- See https://wiki.yoctoproject.org/wiki/Ptest
    if any((parent.name == "ptest" for parent in elf_info.path.parents)):
        LOG.debug("Ignoring %s (ptest)", elf_info.path)
        return True
    if elf_info.gnu_build_id is None:
        LOG.debug("Ignoring %s (GNU Build ID missing)", elf_info.path)
        return True
    if not elf_info.has_text:
        LOG.debug("Ignoring %s (.text missing)", elf_info.path)
        return True
    return False


@dataclasses.dataclass
class FindSymbolFilesResult:
    found: Iterable[ELFFileInfo]
    missing: Iterable[ELFFileInfo]


def find_symbol_files_to_upload(image_elfs: Iterable[ELFFileInfo]) -> FindSymbolFilesResult:
    symbols_by_build_id: Dict[str, ELFFileInfo] = {}
    missing_debug_info_by_build_id: Dict[str, ELFFileInfo] = {}

    # First, analyze all the .elfs in the image:
    for elf_info in image_elfs:
        if should_ignore_elf(elf_info):
            continue
        gnu_build_id = elf_info.gnu_build_id
        assert gnu_build_id  # Should already be filtered out by should_ignore_elf
        if elf_info.has_debug_info:
            symbols_by_build_id[gnu_build_id] = elf_info
        else:
            missing_debug_info_by_build_id[gnu_build_id] = elf_info

    missing_build_ids = set(missing_debug_info_by_build_id.keys())

    return FindSymbolFilesResult(
        found=symbols_by_build_id.values(),
        missing=(missing_debug_info_by_build_id[build_id] for build_id in missing_build_ids),
    )


def find_elf_files_from_image(image_tar: pathlib.Path) -> Iterable[ELFFileInfo]:
    with tarfile.open(
        image_tar, "r:*"
    ) as tar, tempfile.TemporaryDirectory() as extraction_path_str:
        tar.extractall(extraction_path_str)
        extraction_path = pathlib.Path(extraction_path_str)
        yield from find_elf_files(extraction_path, relative_to=extraction_path)


# https://docs.yoctoproject.org/ref-manual/variables.html?highlight=package_debug_split_style#term-PACKAGE_DEBUG_SPLIT_STYLE
class PackageDebugSplitStyle(Enum):
    DEBUG = ".debug"
    DEBUG_WITH_SRCPKG = "debug-with-srcpkg"
    DEBUG_WITHOUT_SRC = "debug-without-src"
    DEBUG_FILE_DIRECTORY = "debug-file-directory"


# https://docs.yoctoproject.org/ref-manual/variables.html?highlight=package_debug_split_style#term-PACKAGE_DEBUG_SPLIT_STYLE
def guess_debug_file_path(bin_path: pathlib.Path, style: PackageDebugSplitStyle) -> pathlib.Path:
    if style == PackageDebugSplitStyle.DEBUG_FILE_DIRECTORY:
        debug_file_directory = pathlib.Path("/usr/lib/debug")
        return debug_file_directory / bin_path.relative_to(debug_file_directory)

    return bin_path.parent / ".debug" / bin_path.name


def eu_unstrip_path_from_components_dir(components_dir: pathlib.Path) -> pathlib.Path:
    eu_unstrip_sysroot_path = pathlib.Path("usr", "bin", "eu-unstrip")
    eu_unstrip_path = (
        components_dir / platform.machine() / "elfutils-native" / eu_unstrip_sysroot_path
    )
    return eu_unstrip_path


def eu_unstrip_run(
    *,
    stripped_elf: pathlib.Path,
    debug_elf: pathlib.Path,
    output_dir: pathlib.Path,
    eu_unstrip_path: pathlib.Path,
) -> Optional[pathlib.Path]:
    random = secrets.token_urlsafe(4)
    output_dir.mkdir(exist_ok=True, parents=True)
    output_path = output_dir / f"{stripped_elf.name}-{random}"

    pipe = subprocess.run(
        (eu_unstrip_path, "--output", output_path, stripped_elf, debug_elf),
        stderr=subprocess.PIPE,
        check=False,
    )

    if pipe.stderr:
        LOG.debug("Unexpected stderr from eu-unstrip: %s", pipe.stderr)
        return None

    return output_path


class OeInitBuildEnvNotSourcedError(Exception):
    pass


def get_from_bitbake_build_env(variables: List[str]) -> List[Optional[str]]:
    grep_pattern = "|".join(map(lambda variable: f"^{variable}", variables))

    try:
        bitbake_environment_process = subprocess.Popen(
            ("bitbake", "--environment"), stdout=subprocess.PIPE
        )
        output = subprocess.check_output(
            ("grep", "-E", grep_pattern), stdin=bitbake_environment_process.stdout
        )
        bitbake_environment_process.wait()
        output_str = output.decode()
    except subprocess.CalledProcessError as err:
        raise OeInitBuildEnvNotSourcedError(
            "Failed to run 'bitbake -e | grep'. Have you run 'source oe-init-build-env'?"
        ) from err

    values: List[Optional[str]] = []

    for variable in variables:
        matcher = r"(^|\n)" + re.escape(variable) + '="(?P<value>.*)"($|\n)'
        matches = re.search(matcher, output_str)
        if matches:
            value = matches.group("value")
            values.append(value or None)
        else:
            values.append(None)

    return values


@dataclasses.dataclass(frozen=True)
class BitbakeBuildEnvResult:
    eu_unstrip_path: pathlib.Path
    package_debug_split_style: PackageDebugSplitStyle


def get_necessary_from_bitbake_build_env() -> BitbakeBuildEnvResult:
    components_dir: Optional[str] = None
    package_debug_split_style: Optional[str] = None

    click.echo("Fetching configuration from bitbake build environment...")
    components_dir, package_debug_split_style = get_from_bitbake_build_env(
        ["COMPONENTS_DIR", "PACKAGE_DEBUG_SPLIT_STYLE"]
    )

    components_dir_path = pathlib.Path(components_dir) if components_dir else None
    if not components_dir_path or not components_dir_path.exists():
        raise click.exceptions.FileError(
            f"Failed to get a valid COMPONENTS_DIR path from bitbake --environment ({components_dir=})"
        )

    eu_unstrip_path = eu_unstrip_path_from_components_dir(components_dir_path)
    if not eu_unstrip_path.exists():
        raise click.exceptions.FileError(
            f"Failed to find executable eu-unstrip in expected location {eu_unstrip_path}"
        )

    try:
        style = PackageDebugSplitStyle(package_debug_split_style)
    except ValueError as err:
        raise click.exceptions.UsageError(
            f"Unsupported or missing PACKAGE_DEBUG_SPLIT_STYLE from bitbake --environment ({package_debug_split_style=})"
        ) from err

    return BitbakeBuildEnvResult(eu_unstrip_path=eu_unstrip_path, package_debug_split_style=style)


def process_and_upload_yocto_symbols(
    ctx: MemfaultCliClickContext, image: pathlib.Path, *, build_env: BitbakeBuildEnvResult
) -> None:
    def _image_elfs(image_tar: pathlib.Path) -> Iterable[ELFFileInfo]:
        with click.progressbar(
            find_elf_files_from_image(image_tar),
            label="Processing binaries in image...",
        ) as bar:
            yield from bar

    debug_image_suffixes = "".join(image.suffixes)
    debug_image_name = image.name.replace(debug_image_suffixes, f"-dbg{debug_image_suffixes}")
    debug_image = image.parent / debug_image_name
    debug_image_mb = "{:.2f}".format(debug_image.stat().st_size / 10e5)

    with tempfile.TemporaryDirectory() as workbench_dir_str, tarfile.open(
        debug_image, "r:*"
    ) as debug_image_tar:
        workbench_dir = pathlib.Path(workbench_dir_str)
        upload_paths: List[pathlib.Path] = []
        missing_infos: List[ELFFileInfo] = []

        debug_symbols_dir = workbench_dir / "debug"
        debug_symbols_dir.mkdir()

        click.echo(f"Extracting debug symbols ({debug_image_mb} MB) to a temporary directory...")
        debug_image_tar.extractall(debug_symbols_dir)

        for elf_info in _image_elfs(image):
            if "/lib/modules" in str(elf_info.path):
                # Not interested in kernel modules and we don't have debug
                # symbols for those anyway.
                continue

            debug_elf_path = guess_debug_file_path(
                elf_info.relpath, style=build_env.package_debug_split_style
            )
            upload_path = eu_unstrip_run(
                stripped_elf=elf_info.path,
                debug_elf=debug_symbols_dir / debug_elf_path,
                output_dir=workbench_dir / "unstripped",
                eu_unstrip_path=build_env.eu_unstrip_path,
            )
            if upload_path:
                upload_paths.append(upload_path)
            else:
                missing_infos.append(elf_info)

        ElfSymbolDirectoryUploader(
            ctx=ctx,
            file_path=image,  # Not used. TODO: refactor!
            authenticator=ctx.create_authenticator(OrgTokenAuthenticator, BasicAuthenticator),
            file_paths=upload_paths,
        ).upload()

        for info in missing_infos:
            LOG.warning(
                "Could not find debug info for %s (GNU build ID %s)",
                info.relpath,
                info.gnu_build_id,
            )

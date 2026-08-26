#!/usr/bin/env python3
"""Build deterministic current-subtitle ZIP files for every work."""

from __future__ import annotations

import hashlib
import re
import sys
import tempfile
import zipfile
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
WORKS_ROOT = REPOSITORY_ROOT / "works"
PACKAGES_ROOT = REPOSITORY_ROOT / "packages"
SEMVER = re.compile(
    r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
)
LANGUAGE_SUFFIX = re.compile(r".+\.zh-Hans\.(?:ja|en)\.ass\Z")
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


class PackageError(RuntimeError):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    return info


def add_bytes(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    archive.writestr(zip_info(name), data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def validate_release_dir(release_dir: Path) -> tuple[str, list[Path]]:
    version_file = release_dir / "VERSION"
    if not version_file.is_file():
        raise PackageError(f"{release_dir}: missing VERSION")
    version = version_file.read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise PackageError(f"{version_file}: expected SemVer without a leading v")

    subtitles = sorted(release_dir.glob("*.ass"), key=lambda path: path.name)
    if not subtitles:
        raise PackageError(f"{release_dir}: contains no ASS files")

    expected_marker = f"; Subtitle-Hub-Version: {version}".encode("ascii")
    marker_prefix = b"; Subtitle-Hub-Version:"
    for subtitle in subtitles:
        if not LANGUAGE_SUFFIX.fullmatch(subtitle.name):
            raise PackageError(f"{subtitle}: invalid language suffix")
        data = subtitle.read_bytes()
        markers = [line for line in data.splitlines() if line.startswith(marker_prefix)]
        if markers != [expected_marker]:
            raise PackageError(
                f"{subtitle}: expected exactly one version marker {expected_marker.decode()}"
            )
    unexpected = sorted(
        path.name for path in release_dir.iterdir() if path.is_file() and path.name != "VERSION" and path.suffix != ".ass"
    )
    if unexpected:
        raise PackageError(f"{release_dir}: unexpected file(s): {', '.join(unexpected)}")
    return version, subtitles


def validate_project(version_file: Path) -> tuple[Path, str, list[Path]]:
    current_dir = version_file.parent
    project_root = current_dir.parent.parent
    version, subtitles = validate_release_dir(current_dir)

    previous_dir = current_dir.parent / "previous"
    if previous_dir.exists():
        if not previous_dir.is_dir():
            raise PackageError(f"{previous_dir}: previous release must be a directory")
        previous_version, _ = validate_release_dir(previous_dir)
        if previous_version == version:
            raise PackageError(f"{previous_dir}: previous and current versions must differ")
    elif version != "1.0.0":
        raise PackageError(f"{previous_dir}: required for every release after the 1.0.0 baseline")
    return project_root, version, subtitles


def build_package(version_file: Path) -> Path:
    project_root, version, subtitles = validate_project(version_file)
    package_root = project_root.name
    output = PACKAGES_ROOT / f"{project_root.name}.zip"

    checksum_lines: list[str] = []
    subtitle_data: list[tuple[str, bytes]] = []
    for subtitle in subtitles:
        data = subtitle.read_bytes()
        relative_name = f"subtitles/{subtitle.name}"
        subtitle_data.append((relative_name, data))
        checksum_lines.append(f"{sha256(data)}  {relative_name}\n")

    version_data = f"{version}\n".encode("utf-8")
    checksum_lines.insert(0, f"{sha256(version_data)}  VERSION\n")
    checksums = "".join(checksum_lines).encode("utf-8")

    PACKAGES_ROOT.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=f".{output.name}.", suffix=".tmp", dir=PACKAGES_ROOT, delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)
    try:
        with zipfile.ZipFile(temporary_path, "w") as archive:
            add_bytes(archive, f"{package_root}/VERSION", version_data)
            add_bytes(archive, f"{package_root}/CHECKSUMS.sha256", checksums)
            for relative_name, data in subtitle_data:
                add_bytes(archive, f"{package_root}/{relative_name}", data)
        temporary_path.replace(output)
    finally:
        temporary_path.unlink(missing_ok=True)

    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise PackageError(f"{output}: ZIP CRC verification failed")
    print(f"built {output.relative_to(REPOSITORY_ROOT)} ({len(subtitles)} subtitles)")
    return output


def main() -> int:
    version_files = sorted(WORKS_ROOT.glob("**/subtitles/current/VERSION"))
    if not version_files:
        raise PackageError("no works/**/subtitles/current/VERSION files found")
    expected = {build_package(path).resolve() for path in version_files}
    stale = sorted(path for path in PACKAGES_ROOT.glob("*.zip") if path.resolve() not in expected)
    if stale:
        names = ", ".join(str(path.relative_to(REPOSITORY_ROOT)) for path in stale)
        raise PackageError(f"unexpected stale package(s): {names}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PackageError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)

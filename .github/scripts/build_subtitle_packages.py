#!/usr/bin/env python3
"""Build deterministic current-subtitle ZIP files for every work."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tempfile
import unicodedata
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
LEGACY_LANGUAGE_SUFFIX = re.compile(r".+\.zh-Hans\.(?:ja|en)\.ass\Z")
EPISODE_ID = re.compile(r"S\d{2}E\d{2}")
STYLE_RESET = re.compile(r"\\r([^\\}]*)")
INLINE_FONT = re.compile(r"\\fn([^\\}]*)")
STYLE_DEFINITION = re.compile(r"^Style:\s*(.*)$")
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
BANGUMI_ID = re.compile(r"[1-9]\d*\Z")
INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*]+')
MAX_PACKAGE_NAME_BYTES = 240
STANDARD_FONTS = {"Noto Sans CJK SC", "Noto Sans CJK JP"}


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


def yaml_scalar(text: str, field: str, indent: int) -> str:
    match = re.search(
        rf"^{' ' * indent}{re.escape(field)}:\s*(.+?)\s*$", text, re.MULTILINE
    )
    if not match:
        raise PackageError(f"project.yaml: missing {field} at indentation {indent}")
    value = match.group(1)
    if value.startswith('"'):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as error:
            raise PackageError(f"project.yaml: invalid quoted value for {field}") from error
    elif len(value) >= 2 and value[0] == value[-1] == "'":
        value = value[1:-1].replace("''", "'")
    return value


def yaml_block(text: str, field: str, indent: int) -> str:
    header = re.search(rf"^{' ' * indent}{re.escape(field)}:\s*$", text, re.MULTILINE)
    if not header:
        raise PackageError(f"project.yaml: missing {field} block")
    lines: list[str] = []
    for line in text[header.end() :].splitlines(keepends=True):
        if line.strip() and len(line) - len(line.lstrip(" ")) <= indent:
            break
        lines.append(line)
    return "".join(lines)


def bangumi_identity(project_root: Path) -> tuple[str, str, str, str]:
    metadata_path = project_root / "project.yaml"
    metadata = metadata_path.read_text(encoding="utf-8")
    if yaml_scalar(metadata, "schema_version", 0) != "3":
        raise PackageError(f"{metadata_path}: identity packaging requires schema_version 3")
    identity = yaml_block(metadata, "identity", 0)
    titles = yaml_block(identity, "titles", 2)
    provider = yaml_scalar(identity, "provider", 2)
    subject_id = yaml_scalar(identity, "id", 2)
    subject_url = yaml_scalar(identity, "url", 2)
    api_url = yaml_scalar(identity, "api_url", 2)
    title_ja = yaml_scalar(titles, "ja", 4)
    title_zh_hans = yaml_scalar(titles, "zh-Hans", 4)
    verification = yaml_scalar(identity, "verification", 2)
    if provider != "bangumi":
        raise PackageError(f"{metadata_path}: identity.provider must be bangumi")
    if not BANGUMI_ID.fullmatch(subject_id):
        raise PackageError(f"{metadata_path}: invalid Bangumi subject ID {subject_id!r}")
    if subject_url != f"https://bgm.tv/subject/{subject_id}":
        raise PackageError(f"{metadata_path}: Bangumi subject URL does not match its ID")
    if api_url != f"https://api.bgm.tv/v0/subjects/{subject_id}":
        raise PackageError(f"{metadata_path}: Bangumi API URL does not match its ID")
    if verification != "api-verified":
        raise PackageError(f"{metadata_path}: Bangumi identity must be api-verified")
    if not title_ja.strip() or not title_zh_hans.strip():
        raise PackageError(f"{metadata_path}: Bangumi name and name_cn must both be present")
    return subject_id, title_ja, title_zh_hans, api_url


def project_languages(project_root: Path) -> tuple[str, str]:
    metadata = (project_root / "project.yaml").read_text(encoding="utf-8")
    languages = yaml_block(metadata, "languages", 0)
    release = yaml_block(languages, "release", 2)
    return yaml_scalar(release, "primary", 4), yaml_scalar(release, "secondary", 4)


def validate_standard_ass(
    subtitle: Path, data: bytes, version: str, project_root: Path
) -> None:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as error:
        raise PackageError(f"{subtitle}: release ASS must be UTF-8") from error
    if "\r" in text:
        raise PackageError(f"{subtitle}: release ASS must use LF line endings")
    if "[Aegisub Project Garbage]" in text:
        raise PackageError(f"{subtitle}: contains Aegisub Project Garbage")
    if re.search(r"(?m)^\[Fonts\]$", text):
        raise PackageError(f"{subtitle}: embedded ASS Fonts section is not allowed")

    subject_id, _, title_zh_hans, _ = bangumi_identity(project_root)
    primary, secondary = project_languages(project_root)
    if not subtitle.name.endswith(f".{primary}.ass"):
        raise PackageError(f"{subtitle}: filename must end in .{primary}.ass")
    metadata = (project_root / "project.yaml").read_text(encoding="utf-8")
    project_type = yaml_scalar(metadata, "type", 0)
    episode_match = EPISODE_ID.search(subtitle.name)
    if episode_match:
        episode_id = episode_match.group(0)
    elif project_type == "movie":
        episode_id = "MOVIE"
    else:
        raise PackageError(f"{subtitle}: cannot determine episode ID for Title")

    lines = text.splitlines()
    try:
        styles_index = lines.index("[V4+ Styles]")
        events_index = lines.index("[Events]")
    except ValueError as error:
        raise PackageError(f"{subtitle}: missing Styles or Events section") from error
    if not 0 < styles_index < events_index:
        raise PackageError(f"{subtitle}: invalid ASS section order")

    header = lines[:styles_index]
    required_prefix = [
        "[Script Info]",
        f"; Subtitle-Hub-Version: {version}",
        f"; Subtitle-Hub-Languages: {primary}, {secondary}",
        f"; Subtitle-Hub-Primary-Language: {primary}",
        f"; Subtitle-Hub-Secondary-Language: {secondary}",
    ]
    if header[: len(required_prefix)] != required_prefix:
        raise PackageError(f"{subtitle}: noncanonical Subtitle Hub header prefix")
    cursor = len(required_prefix)
    for optional_prefix in (
        "; Subtitle-Hub-Timing-Note: ",
        "; Subtitle-Hub-Source-Credit: ",
    ):
        if cursor < len(header) and header[cursor].startswith(optional_prefix):
            if not header[cursor][len(optional_prefix) :].strip():
                raise PackageError(f"{subtitle}: empty optional header comment")
            cursor += 1
    expected_title = f"Title: bgm{subject_id} - {title_zh_hans} - {episode_id}"
    expected_labels = (
        "ScriptType",
        "WrapStyle",
        "ScaledBorderAndShadow",
        "PlayResX",
        "PlayResY",
        "YCbCr Matrix",
    )
    if cursor >= len(header) or header[cursor] != expected_title:
        raise PackageError(f"{subtitle}: noncanonical Title")
    cursor += 1
    for label in expected_labels:
        if cursor >= len(header) or not header[cursor].startswith(f"{label}: "):
            raise PackageError(f"{subtitle}: expected {label} in canonical order")
        if not header[cursor].split(":", 1)[1].strip():
            raise PackageError(f"{subtitle}: empty {label}")
        cursor += 1
    if header[cursor:] != [""]:
        raise PackageError(f"{subtitle}: unexpected or unordered Script Info fields")

    defined: set[str] = set()
    style_fonts: set[str] = set()
    for line in lines[styles_index + 1 : events_index]:
        style_match = STYLE_DEFINITION.match(line)
        if not style_match:
            continue
        style_parts = style_match.group(1).split(",")
        if len(style_parts) < 2:
            raise PackageError(f"{subtitle}: malformed style line")
        defined.add(style_parts[0])
        style_fonts.add(style_parts[1].strip())
    references: set[str] = set()
    inline_fonts: set[str] = set()
    for line in lines[events_index + 1 :]:
        if line.startswith("[") and line.endswith("]"):
            break
        if not line.startswith(("Dialogue:", "Comment:")):
            continue
        parts = line.split(",", 9)
        if len(parts) != 10:
            raise PackageError(f"{subtitle}: malformed event line")
        references.add(parts[3].strip() or "Default")
        for reset in STYLE_RESET.findall(parts[9]):
            if reset.strip():
                references.add(reset.strip())
        for font in INLINE_FONT.findall(parts[9]):
            if font.strip():
                inline_fonts.add(font.strip())
    missing = sorted(references - defined)
    unused = sorted(defined - references)
    if missing:
        raise PackageError(f"{subtitle}: undefined style references: {', '.join(missing)}")
    if unused:
        raise PackageError(f"{subtitle}: unused style definitions: {', '.join(unused)}")
    unsupported_fonts = sorted((style_fonts | inline_fonts) - STANDARD_FONTS)
    if unsupported_fonts:
        raise PackageError(
            f"{subtitle}: unsupported release fonts: {', '.join(unsupported_fonts)}"
        )


def package_name(project_root: Path, version: str | None = None) -> str:
    subject_id, _, title_zh_hans, _ = bangumi_identity(project_root)
    safe_title = unicodedata.normalize("NFC", title_zh_hans)
    safe_title = INVALID_FILENAME_CHARS.sub(" - ", safe_title)
    safe_title = " ".join(safe_title.split()).rstrip(" .")
    if not safe_title:
        raise PackageError(f"{project_root / 'project.yaml'}: name_cn is empty after normalization")
    if version is None:
        version_path = project_root / "subtitles/current/VERSION"
        if not version_path.is_file():
            raise PackageError(f"{version_path}: missing VERSION for package name")
        version = version_path.read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise PackageError(f"{project_root}: invalid release version {version!r}")
    name = f"bgm{subject_id} - {safe_title} [v{version}].zip"
    if len(name.encode("utf-8")) > MAX_PACKAGE_NAME_BYTES:
        raise PackageError(
            f"{project_root}: package filename exceeds {MAX_PACKAGE_NAME_BYTES} UTF-8 bytes"
        )
    return name


def validate_release_dir(
    release_dir: Path, project_root: Path | None = None
) -> tuple[str, list[Path]]:
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
    major_version = int(version.split(".", 1)[0])
    for subtitle in subtitles:
        if major_version < 2 and not LEGACY_LANGUAGE_SUFFIX.fullmatch(subtitle.name):
            raise PackageError(
                f"{subtitle}: expected legacy filename ending in .zh-Hans.<secondary>.ass"
            )
        data = subtitle.read_bytes()
        markers = [line for line in data.splitlines() if line.startswith(marker_prefix)]
        if markers != [expected_marker]:
            raise PackageError(
                f"{subtitle}: expected exactly one version marker {expected_marker.decode()}"
            )
        if major_version >= 2:
            if project_root is None:
                raise PackageError(f"{release_dir}: project root required for version 2+")
            validate_standard_ass(subtitle, data, version, project_root)
    unexpected = sorted(
        path.name
        for path in release_dir.iterdir()
        if path.is_file() and path.name != "VERSION" and path.suffix != ".ass"
    )
    if unexpected:
        raise PackageError(f"{release_dir}: unexpected file(s): {', '.join(unexpected)}")
    return version, subtitles


def validate_project(version_file: Path) -> tuple[Path, str, list[Path]]:
    current_dir = version_file.parent
    project_root = current_dir.parent.parent
    version, subtitles = validate_release_dir(current_dir, project_root)

    previous_dir = current_dir.parent / "previous"
    if previous_dir.exists():
        if not previous_dir.is_dir():
            raise PackageError(f"{previous_dir}: previous release must be a directory")
        previous_version, _ = validate_release_dir(previous_dir, project_root)
        if previous_version == version:
            raise PackageError(f"{previous_dir}: previous and current versions must differ")
    elif version != "1.0.0":
        raise PackageError(f"{previous_dir}: required for every release after the 1.0.0 baseline")
    return project_root, version, subtitles


def build_package(version_file: Path) -> Path:
    project_root, version, subtitles = validate_project(version_file)
    output = PACKAGES_ROOT / package_name(project_root, version)
    package_root = output.stem

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
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="validate releases and print planned names only"
    )
    args = parser.parse_args()
    version_files = sorted(WORKS_ROOT.glob("**/subtitles/current/VERSION"))
    if not version_files:
        raise PackageError("no works/**/subtitles/current/VERSION files found")
    planned: dict[Path, Path] = {}
    for version_file in version_files:
        project_root = version_file.parent.parent.parent
        version = version_file.read_text(encoding="utf-8").strip()
        output = (PACKAGES_ROOT / package_name(project_root, version)).resolve()
        if output in planned:
            raise PackageError(
                f"duplicate package identity: {project_root} and {planned[output]}"
            )
        planned[output] = project_root
    if args.check:
        for version_file in version_files:
            project_root, version, subtitles = validate_project(version_file)
            output = PACKAGES_ROOT / package_name(project_root, version)
            print(
                f"valid {project_root.relative_to(REPOSITORY_ROOT)} -> "
                f"{output.relative_to(REPOSITORY_ROOT)} ({len(subtitles)} subtitles)"
            )
        stale = sorted(
            path for path in PACKAGES_ROOT.glob("*.zip") if path.resolve() not in planned
        )
        for path in stale:
            print(f"stale {path.relative_to(REPOSITORY_ROOT)}")
        return 0
    expected = {build_package(path).resolve() for path in version_files}
    stale = sorted(path for path in PACKAGES_ROOT.glob("*.zip") if path.resolve() not in expected)
    for path in stale:
        path.resolve().relative_to(PACKAGES_ROOT.resolve())
        path.unlink()
        print(f"removed stale {path.relative_to(REPOSITORY_ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PackageError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)

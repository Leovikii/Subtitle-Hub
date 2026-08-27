#!/usr/bin/env python3
"""Validate Subtitle Hub project/control-plane invariants with no external packages."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

ALLOWED_ROLES = {
    "candidate-baseline",
    "source-text-reference",
    "timing-reference",
    "translation-reference",
    "forced-signs-reference",
    "style-layout-reference",
    "secondary-language-release-source",
}
ISSUE_STATUSES = {"candidate", "confirmed", "in-progress", "blocked", "fixed", "verified", "waived", "wont-fix"}
CHANGE_STATUSES = {"applied", "verified", "reverted", "released"}
ISSUE_HEADER = "issue_id\tdate\tepisode\tstart\tend\tcategory\tseverity\tdescription\tevidence\tproposed_action\tstatus\towner\tresolution"
CHANGE_HEADER = "change_id\tbatch_id\tdate\tepisode\tstart\tend\tcategory\tseverity\tbefore\tafter\tsource_ref\trationale\tstatus\tagent\treviewer"


def scalar(text: str, name: str, indent: int = 0) -> str | None:
    pattern = rf"(?m)^{' ' * indent}{re.escape(name)}:\s*(.*?)\s*$"
    match = re.search(pattern, text)
    if not match:
        return None
    value = match.group(1).split(" #", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1]
    return value


def section(text: str, name: str, indent: int = 0) -> str:
    lines = text.splitlines()
    prefix = " " * indent + name + ":"
    start = next((index for index, line in enumerate(lines) if line.startswith(prefix)), None)
    if start is None:
        return ""
    result = []
    for line in lines[start + 1 :]:
        if line.strip() and len(line) - len(line.lstrip(" ")) <= indent:
            break
        result.append(line)
    return "\n".join(result)


def subtitle_entries(text: str) -> list[dict[str, object]]:
    block = section(text, "subtitle_sources")
    starts = list(re.finditer(r"(?m)^  - id:\s*(.*?)\s*$", block))
    entries = []
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(block)
        chunk = block[match.start() : end]
        roles_block = section(chunk, "roles", 4)
        roles = re.findall(r"(?m)^      -\s*([a-z0-9-]+)\s*$", roles_block)
        language = scalar(chunk, "language", 4)
        if language is None and re.search(r"(?m)^    language:\s*$", chunk):
            language_block = section(chunk, "language", 4)
            languages = re.findall(r"(?m)^      -\s*([^\s]+)\s*$", language_block)
        else:
            languages = [language] if language else []
        classification = section(chunk, "classification", 4)
        entries.append(
            {
                "id": match.group(1).strip('"\''),
                "languages": languages,
                "path": scalar(chunk, "path", 4),
                "file_count": scalar(chunk, "file_count", 4),
                "scope": scalar(chunk, "scope", 4),
                "roles": roles,
                "classification": scalar(classification, "status", 6),
                "confirmed_by": scalar(classification, "confirmed_by", 6),
                "confirmed_at": scalar(classification, "confirmed_at", 6),
                "evidence": scalar(classification, "evidence", 6),
            }
        )
    return entries


def validate_tsv(path: Path, expected_header: str, status_index: int, allowed: set[str], errors: list[str]) -> None:
    try:
        lines = path.read_text(encoding="utf-8-sig").splitlines()
    except OSError as error:
        errors.append(f"{path}: {error}")
        return
    if not lines or lines[0] != expected_header:
        errors.append(f"{path}: unexpected TSV header")
        return
    for row_number, row in enumerate(csv.reader(lines[1:], delimiter="\t"), start=2):
        if not row:
            continue
        if len(row) != len(expected_header.split("\t")):
            errors.append(f"{path}:{row_number}: expected {len(expected_header.split(chr(9)))} fields, got {len(row)}")
        elif row[status_index] not in allowed:
            errors.append(f"{path}:{row_number}: invalid active status {row[status_index]!r}")


def validate_release(project_root: Path, metadata: str, errors: list[str], warnings: list[str]) -> None:
    release_language = scalar(section(section(metadata, "languages"), "release", 2), "primary", 4) or "zh-Hans"
    secondary = scalar(section(section(metadata, "languages"), "release", 2), "secondary", 4)
    if secondary == "null":
        secondary = None
    for directory_name in ("current", "previous"):
        directory = project_root / "subtitles" / directory_name
        if not directory.exists():
            if directory_name == "current":
                warnings.append(f"{directory}: no release exists yet")
            continue
        version_file = directory / "VERSION"
        if not version_file.is_file():
            errors.append(f"{directory}: VERSION is missing")
            continue
        version = version_file.read_text(encoding="utf-8-sig").strip()
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            errors.append(f"{version_file}: invalid SemVer {version!r}")
        ass_files = sorted(directory.glob("*.ass"))
        if not ass_files:
            errors.append(f"{directory}: no ASS files")
        for ass in ass_files:
            if not ass.name.endswith(f".{release_language}.ass"):
                errors.append(f"{ass}: filename does not declare only primary language {release_language}")
            text = ass.read_text(encoding="utf-8-sig")
            expected = {
                "Subtitle-Hub-Version": version,
                "Subtitle-Hub-Languages": release_language if secondary is None else f"{release_language}, {secondary}",
                "Subtitle-Hub-Primary-Language": release_language,
                "Subtitle-Hub-Secondary-Language": secondary,
            }
            for field, value in expected.items():
                if value and len(re.findall(rf"(?m)^; {re.escape(field)}: {re.escape(value)}$", text)) != 1:
                    errors.append(f"{ass}: expected exactly one {field}: {value}")
            if secondary is None and re.search(r"(?m)^; Subtitle-Hub-Secondary-Language:", text):
                errors.append(f"{ass}: monolingual release must omit Subtitle-Hub-Secondary-Language")
            if "[Fonts]" in text:
                errors.append(f"{ass}: ASS [Fonts] is prohibited")
            if directory_name == "current" and "Source-Metadata" in text:
                errors.append(f"{ass}: Source-Metadata must not appear in released ASS")
            if not re.search(r"(?m)^Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text$", text):
                errors.append(f"{ass}: required Events Format line is missing")
    current = project_root / "subtitles" / "current" / "VERSION"
    previous = project_root / "subtitles" / "previous" / "VERSION"
    if current.is_file():
        version = current.read_text(encoding="utf-8-sig").strip()
        if version != "1.0.0" and not previous.is_file():
            errors.append(f"{project_root}: a post-baseline current release requires subtitles/previous")
        if previous.is_file() and previous.read_text(encoding="utf-8-sig").strip() == version:
            errors.append(f"{project_root}: current and previous versions are identical")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Work root containing project.yaml")
    parser.add_argument("--release", action="store_true", help="Also require and inspect release artifacts")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable output")
    args = parser.parse_args()
    root = args.project.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    metadata_path = root / "project.yaml"
    try:
        metadata = metadata_path.read_text(encoding="utf-8-sig")
    except OSError as error:
        parser.error(str(error))

    if scalar(metadata, "schema_version") != "4":
        errors.append(f"{metadata_path}: schema_version must be 4")
    work_id = scalar(metadata, "id")
    if not work_id or not re.fullmatch(r"SH\d{4,}", work_id):
        errors.append(f"{metadata_path}: invalid work id")
    identity = section(metadata, "identity")
    if scalar(identity, "provider", 2) != "bangumi":
        errors.append(f"{metadata_path}: identity.provider must be bangumi")
    for name, indent in (("id", 2), ("verification", 2)):
        if not scalar(identity, name, indent):
            errors.append(f"{metadata_path}: identity.{name} is missing")
    titles = section(identity, "titles", 2)
    if not scalar(titles, "ja", 4) or not scalar(titles, "zh-Hans", 4):
        errors.append(f"{metadata_path}: Bangumi ja/name_cn identity titles are required")
    task = section(metadata, "task")
    if scalar(task, "mode", 2) != "proofreading":
        errors.append(f"{metadata_path}: task.mode must be proofreading")
    if not scalar(task, "source_language", 2):
        errors.append(f"{metadata_path}: task.source_language is required")

    entries = subtitle_entries(metadata)
    if not entries:
        errors.append(f"{metadata_path}: subtitle_sources is empty")
    all_roles: set[str] = set()
    for entry in entries:
        roles = set(entry["roles"])
        all_roles.update(roles)
        languages = entry["languages"]
        if not languages or "und" in languages:
            errors.append(f"{metadata_path}: source {entry['id']} has unresolved language")
        if not roles or roles - ALLOWED_ROLES:
            errors.append(f"{metadata_path}: source {entry['id']} has invalid roles {sorted(roles)}")
        if entry["classification"] not in {"declared", "verified", "user-confirmed"}:
            errors.append(f"{metadata_path}: source {entry['id']} lacks a valid classification status")
        if not entry["scope"]:
            errors.append(f"{metadata_path}: source {entry['id']} lacks an episode scope")
        if not entry["confirmed_by"] or not entry["confirmed_at"] or not entry["evidence"]:
            errors.append(f"{metadata_path}: source {entry['id']} classification lacks confirmer/date/evidence")
        source_path = str(entry["path"] or "")
        if not source_path.startswith("project/sources/") or re.match(r"^[A-Za-z]:[\\/]", source_path) or source_path.startswith("/"):
            errors.append(f"{metadata_path}: source {entry['id']} path must be repository-relative under project/sources")
        else:
            directory = root / Path(source_path)
            if not directory.exists():
                errors.append(f"{directory}: declared source path does not exist")
            elif entry["file_count"] and entry["file_count"].isdigit():
                actual = sum(1 for file in directory.rglob("*") if file.is_file() and file.name != ".gitignore")
                if actual != int(entry["file_count"]):
                    errors.append(f"{directory}: file_count is {entry['file_count']}, actual {actual}")
    if "candidate-baseline" not in all_roles:
        errors.append(f"{metadata_path}: proofreading requires a candidate-baseline source")

    video_block = section(metadata, "video_sources")
    video_names = re.findall(r'(?m)^      [^:]+:\s*["\']?(.*?)["\']?\s*$', video_block)
    if not video_names:
        errors.append(f"{metadata_path}: target-video episode map is empty")
    for name in video_names:
        if re.match(r"^[A-Za-z]:[\\/]", name) or name.startswith("/") or "/" in name or "\\" in name:
            errors.append(f"{metadata_path}: video map must store basename only, got {name!r}")

    docs = root / "docs"
    required = [docs / "project-guide.md", docs / "progress.yaml", docs / "issues.tsv", docs / "change-log.tsv"]
    for path in required:
        if not path.is_file():
            errors.append(f"{path}: required control file is missing")
    if (docs / "README.md").exists():
        errors.append(f"{docs / 'README.md'}: redundant project control README must be removed")
    documentation = section(metadata, "documentation")
    if scalar(documentation, "entry", 2):
        errors.append(f"{metadata_path}: documentation.entry is obsolete")
    if (docs / "project-guide.md").is_file() and re.search(r"docs/(?:timing|quality|source|chinese|release|project|series|workspace|references)[^\s`|;]*\.md", (docs / "project-guide.md").read_text(encoding="utf-8")):
        errors.append(f"{docs / 'project-guide.md'}: active rules must cite stable Skill IDs, not deleted docs paths")
    progress_path = docs / "progress.yaml"
    if progress_path.is_file():
        progress = progress_path.read_text(encoding="utf-8-sig")
        if scalar(progress, "schema_version") != "3":
            errors.append(f"{progress_path}: schema_version must be 3")
        if work_id and scalar(progress, "work_id") != work_id:
            errors.append(f"{progress_path}: work_id does not match project.yaml")
    if (docs / "issues.tsv").is_file():
        validate_tsv(docs / "issues.tsv", ISSUE_HEADER, 10, ISSUE_STATUSES, errors)
    if (docs / "change-log.tsv").is_file():
        validate_tsv(docs / "change-log.tsv", CHANGE_HEADER, 12, CHANGE_STATUSES, errors)

    if args.release:
        validate_release(root, metadata, errors, warnings)
    result = {"project": str(root), "errors": errors, "warnings": warnings, "valid": not errors}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for message in errors:
            print(f"ERROR: {message}")
        for message in warnings:
            print(f"WARNING: {message}")
        print(f"{'PASS' if not errors else 'FAIL'}: {root}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

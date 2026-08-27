#!/usr/bin/env python3
"""Validate Subtitle Hub project and release invariants with no external packages."""

from __future__ import annotations

import argparse
import json
import re
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
PROJECT_NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
EPISODE_PATTERNS = {
    "tv": re.compile(r"S\d{2}E\d{2,3}"),
    "ona": re.compile(r"S\d{2}E\d{2,3}"),
    "ova": re.compile(r"OVA\d{2,3}"),
    "special": re.compile(r"SP\d{2,3}"),
    "movie": re.compile(r"MOVIE"),
}
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
                "kind": scalar(chunk, "kind", 4),
                "container": scalar(chunk, "container", 4),
                "stream_index": scalar(chunk, "stream_index", 4),
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


def video_file_map(metadata: str) -> dict[str, str]:
    video_sources = section(metadata, "video_sources")
    target_video = section(video_sources, "target-video", 2)
    files = section(target_video, "files", 4)
    return {
        match.group(1): match.group(2).strip().strip('"\'')
        for match in re.finditer(r"(?m)^      ([A-Za-z0-9]+):\s*(.*?)\s*$", files)
    }


def validate_working_masters(project_root: Path, videos: dict[str, str], errors: list[str], warnings: list[str]) -> None:
    for episode in sorted(videos):
        master = project_root / "project" / "workspace" / "episodes" / episode / "master.ass"
        if not master.is_file():
            errors.append(f"{master}: proofreading-ready project requires a working master")
            continue
        try:
            text = master.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as error:
            errors.append(f"{master}: unreadable UTF-8 text: {error}")
            continue
        if "[Events]" not in text or not re.search(r"(?m)^Format:.*Start.*End.*Text\s*$", text):
            errors.append(f"{master}: missing a parseable ASS/SSA Events section")
        if not re.search(r"(?m)^Dialogue:", text):
            warnings.append(f"{master}: contains no Dialogue events")
    local_paths = project_root / "project" / "local.paths.yaml"
    if not local_paths.is_file():
        errors.append(f"{local_paths}: local video mapping is required for proofreading readiness")
    else:
        mapping = local_paths.read_text(encoding="utf-8-sig")
        for episode, expected_basename in videos.items():
            match = re.search(rf"(?m)^  {re.escape(episode)}:\s*(.+?)\s*$", mapping)
            if not match:
                errors.append(f"{local_paths}: missing local target-video path for {episode}")
                continue
            raw_path = match.group(1)
            try:
                local_value = json.loads(raw_path) if raw_path.startswith('"') else raw_path.strip("'")
            except json.JSONDecodeError:
                errors.append(f"{local_paths}: invalid quoted local path for {episode}")
                continue
            local_video = Path(local_value)
            if not local_video.is_file():
                errors.append(f"{local_paths}: target video for {episode} is not readable: {local_video}")
            elif local_video.name != expected_basename:
                errors.append(f"{local_paths}: target video basename for {episode} does not match project.yaml")


def validate_release(project_root: Path, metadata: str, errors: list[str], warnings: list[str]) -> None:
    release_language = scalar(section(section(metadata, "languages"), "release", 2), "primary", 4) or "zh-Hans"
    secondary = scalar(section(section(metadata, "languages"), "release", 2), "secondary", 4)
    if secondary == "null":
        secondary = None
    for directory_name in ("current", "previous"):
        directory = project_root / "subtitles" / directory_name
        if not directory.exists():
            if directory_name == "current":
                errors.append(f"{directory}: --release requires a current release")
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
        if directory_name == "current":
            expected_names = {f"{Path(name).stem}.{release_language}.ass" for name in video_file_map(metadata).values()}
            actual_names = {path.name for path in ass_files}
            if actual_names != expected_names:
                errors.append(f"{directory}: release filenames/scope differ from target-video map; expected {sorted(expected_names)}, got {sorted(actual_names)}")
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
    parser.add_argument("--ready-for-proofreading", action="store_true", help="Require prepared masters and local target-video mappings")
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

    if scalar(metadata, "schema_version") != "7":
        errors.append(f"{metadata_path}: schema_version must be 7")
    work_id = scalar(metadata, "id")
    if not work_id or not re.fullmatch(r"SH\d{4,}", work_id):
        errors.append(f"{metadata_path}: invalid work id")
    project_name = scalar(metadata, "project_name")
    if not project_name or not PROJECT_NAME_RE.fullmatch(project_name):
        errors.append(f"{metadata_path}: invalid project_name")
    elif root.name != f"{work_id}--{project_name}":
        errors.append(f"{root}: directory must be {work_id}--{project_name}")
    naming = section(metadata, "naming")
    if scalar(naming, "directory", 2) != root.name or not scalar(naming, "approved_by", 2) or not scalar(naming, "approved_at", 2):
        errors.append(f"{metadata_path}: naming approval block is missing or inconsistent")
    identity = section(metadata, "identity")
    if scalar(identity, "provider", 2) != "bangumi":
        errors.append(f"{metadata_path}: identity.provider must be bangumi")
    bangumi_id = scalar(identity, "id", 2)
    if not bangumi_id or not re.fullmatch(r"[1-9]\d*", bangumi_id):
        errors.append(f"{metadata_path}: identity.id must be a Bangumi numeric ID")
    if scalar(identity, "verification", 2) != "api-verified":
        errors.append(f"{metadata_path}: identity.verification must be api-verified")
    titles = section(identity, "titles", 2)
    if not scalar(titles, "ja", 4) or not scalar(titles, "zh-Hans", 4):
        errors.append(f"{metadata_path}: Bangumi ja/name_cn identity titles are required")
    initialization = section(metadata, "initialization")
    initialization_state = scalar(initialization, "state", 2)
    for name in ("date", "platform", "total_episodes"):
        value = scalar(identity, name, 2)
        if not value or (value == "null" and initialization_state != "released-existing"):
            errors.append(f"{metadata_path}: identity.{name} is missing")
        elif value == "null":
            warnings.append(f"{metadata_path}: migrated release lacks historical identity.{name}")
    identity_date = scalar(identity, "date", 2)
    if identity_date not in {None, "null"} and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", identity_date):
        errors.append(f"{metadata_path}: identity.date must use YYYY-MM-DD")
    total_episodes = scalar(identity, "total_episodes", 2)
    if total_episodes not in {None, "null"} and (not total_episodes.isdigit() or int(total_episodes) <= 0):
        errors.append(f"{metadata_path}: identity.total_episodes must be positive")
    scope_verification = section(identity, "scope_verification", 2)
    if scalar(scope_verification, "status", 4) != "user-confirmed" or not scalar(scope_verification, "approved_by", 4):
        errors.append(f"{metadata_path}: identity scope requires recorded user confirmation")
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
        if entry["kind"] == "embedded-subtitle-track":
            if not entry["container"] or entry["stream_index"] is None:
                errors.append(f"{metadata_path}: embedded source {entry['id']} needs container and stream_index")
        elif not source_path.startswith("project/sources/") or re.match(r"^[A-Za-z]:[\\/]", source_path) or source_path.startswith("/"):
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

    work_type = scalar(metadata, "type") or ""
    videos = video_file_map(metadata)
    if not videos:
        errors.append(f"{metadata_path}: target-video episode map is empty")
    for episode, name in videos.items():
        pattern = EPISODE_PATTERNS.get(work_type)
        if not pattern or not pattern.fullmatch(episode):
            errors.append(f"{metadata_path}: invalid {work_type} episode ID {episode!r}")
        if re.match(r"^[A-Za-z]:[\\/]", name) or name.startswith("/") or "/" in name or "\\" in name:
            errors.append(f"{metadata_path}: video map must store basename only, got {name!r}")
    output_names = [f"{Path(name).stem}.zh-Hans.ass".casefold() for name in videos.values()]
    if len(output_names) != len(set(output_names)):
        errors.append(f"{metadata_path}: target video stems collide as release filenames")
    episode_count = scalar(metadata, "episode_count")
    if not episode_count or not episode_count.isdigit() or int(episode_count) != len(videos):
        errors.append(f"{metadata_path}: episode_count must match the target-video map")

    review_path = root / "review.md"
    if not review_path.is_file():
        errors.append(f"{review_path}: required control file is missing")
    for obsolete in (root / "README.md", root / "docs"):
        if obsolete.exists():
            errors.append(f"{obsolete}: obsolete parallel project documentation must be removed")
    documentation = section(metadata, "documentation")
    if scalar(documentation, "review", 2) != "review.md":
        errors.append(f"{metadata_path}: documentation.review must be review.md")
    for obsolete in ("entry", "guide", "ledger", "progress", "change_log", "issues"):
        if scalar(documentation, obsolete, 2) is not None:
            errors.append(f"{metadata_path}: documentation.{obsolete} is obsolete")
    if review_path.is_file():
        review = review_path.read_text(encoding="utf-8-sig")
        if not review.startswith("---\n") or "\n---\n" not in review[4:]:
            errors.append(f"{review_path}: YAML front matter is required")
        if scalar(review, "schema_version") != "1":
            errors.append(f"{review_path}: schema_version must be 1")
        if work_id and scalar(review, "work_id") != work_id:
            errors.append(f"{review_path}: work_id does not match project.yaml")
        for heading in ("# 当前校对轮次", "## 检查覆盖", "## 需要用户确认", "## 决策与实施", "## 验证与剩余风险"):
            if heading not in review:
                errors.append(f"{review_path}: required section is missing: {heading}")
        if "## 校对方案" not in review and "## 候选修改摘要" not in review:
            errors.append(f"{review_path}: required section is missing: ## 校对方案")

    design = section(metadata, "subtitle_design")
    profile = scalar(design, "profile", 2)
    if profile not in {"zh-mono", "zh-bilingual"}:
        errors.append(f"{metadata_path}: subtitle_design.profile must be zh-mono or zh-bilingual")
    ordinary = section(design, "ordinary_styles", 2)
    if not scalar(ordinary, "primary", 4):
        errors.append(f"{metadata_path}: subtitle_design.ordinary_styles.primary is required")
    secondary_language = scalar(section(section(metadata, "languages"), "release", 2), "secondary", 4)
    if (profile == "zh-mono") != (secondary_language in {None, "null"}):
        errors.append(f"{metadata_path}: subtitle_design.profile must match release secondary language")

    initialization_version = scalar(initialization, "skill_version", 2)
    if initialization_version not in {"1.0.0", "1.1.0"}:
        errors.append(f"{metadata_path}: initialization.skill_version must be 1.0.0 or 1.1.0")
    if initialization_state not in {"proofreading-ready", "released-existing"}:
        errors.append(f"{metadata_path}: initialization.state is invalid")
    if initialization_state == "proofreading-ready":
        for field in ("intake_approved_by", "episode_map_approved_by", "approved_at"):
            if not scalar(initialization, field, 2):
                errors.append(f"{metadata_path}: initialization.{field} is required")
    if args.ready_for_proofreading:
        if initialization_state not in {"proofreading-ready", "released-existing"}:
            errors.append(f"{metadata_path}: initialization state is not proofreading-ready")
        validate_working_masters(root, videos, errors, warnings)

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

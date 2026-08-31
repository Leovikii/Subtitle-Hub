#!/usr/bin/env python3
"""Validate current Subtitle Hub project, coverage, and release invariants."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml

from align_bilingual import AlignmentError, ordinary_master_counts, source_file_fingerprints

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
                "evidence": scalar(chunk, "evidence", 4),
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


def project_languages(metadata: str) -> tuple[str, str | None]:
    release = section(metadata, "release_languages")
    primary = scalar(release, "primary", 2) or "zh-Hans"
    secondary = scalar(release, "secondary", 2)
    return primary, None if secondary in {None, "null"} else secondary


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
        for field in ("ScriptType", "WrapStyle", "ScaledBorderAndShadow", "PlayResX", "PlayResY", "YCbCr Matrix"):
            if not re.search(rf"(?m)^{re.escape(field)}:\s*\S", text):
                errors.append(f"{master}: missing required Script Info field {field}")
        fonts = set(re.findall(r"(?m)^Style:\s*[^,]+,([^,]+)", text)) | {font.strip() for font in re.findall(r"\\fn([^\\}]*)", text) if font.strip()}
        unsupported = sorted(fonts - {"Noto Sans CJK SC", "Noto Sans CJK JP"})
        if unsupported:
            errors.append(f"{master}: master has non-Noto fonts: {', '.join(unsupported)}")
    local_paths = project_root / "project" / "local.paths.yaml"
    if local_paths.is_file():
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
            if not isinstance(local_value, str):
                errors.append(f"{local_paths}: target-video locator for {episode} must be a string")
                continue
            if local_value.startswith("ssh://"):
                parsed = urlparse(local_value)
                remote_name = Path(unquote(parsed.path)).name
                if parsed.password is not None or not parsed.hostname or not parsed.username or not remote_name or parsed.query or parsed.fragment:
                    errors.append(f"{local_paths}: invalid password-free SSH locator for {episode}")
                elif remote_name != expected_basename:
                    errors.append(f"{local_paths}: SSH video basename for {episode} does not match project.yaml")
            else:
                local_video = Path(local_value)
                if not local_video.is_file():
                    errors.append(f"{local_paths}: target video for {episode} is not readable: {local_video}")
                elif local_video.name != expected_basename:
                    errors.append(f"{local_paths}: target video basename for {episode} does not match project.yaml")


def validate_release(project_root: Path, metadata: str, errors: list[str], warnings: list[str]) -> None:
    release_language, secondary = project_languages(metadata)
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


def validate_review_coverage(project_root: Path, review_path: Path, review: str, metadata: str, errors: list[str]) -> None:
    coverage = section(review, "coverage")
    tier = scalar(coverage, "evidence_tier", 2)
    if tier not in {"A", "B", "C", "D"}:
        errors.append(f"{review_path}: release coverage requires evidence_tier A-D")
    values: dict[str, int] = {}
    fields = [
        "chinese_in_scope", "chinese_reviewed", "chinese_excluded", "source_in_scope",
        "source_aligned", "source_excluded", "source_unresolved", "static_layout_checked",
        "unresolved_p0", "unresolved_p1",
    ]
    for field in fields:
        raw = scalar(coverage, field, 2)
        if raw is None or not raw.isdigit():
            errors.append(f"{review_path}: coverage.{field} must be a non-negative integer")
            values[field] = -1
        else:
            values[field] = int(raw)
    if values.get("chinese_in_scope", 0) <= 0:
        errors.append(f"{review_path}: release coverage has no Chinese events in scope")
    if values.get("chinese_in_scope") != values.get("chinese_reviewed", 0) + values.get("chinese_excluded", 0):
        errors.append(f"{review_path}: Chinese coverage denominator is incomplete")
    if values.get("static_layout_checked", -1) < values.get("chinese_in_scope", 0):
        errors.append(f"{review_path}: static layout coverage is incomplete")
    if values.get("unresolved_p0") != 0 or values.get("unresolved_p1") != 0:
        errors.append(f"{review_path}: unresolved P0/P1 blocks release")
    if tier in {"A", "B"}:
        source_language = scalar(section(metadata, "task"), "source_language", 2) or ""
        eligible_source = any(
            "source-text-reference" in entry["roles"]
            and any(
                isinstance(language, str)
                and language.split("-", 1)[0].casefold() == source_language.split("-", 1)[0].casefold()
                for language in entry["languages"]
            )
            for entry in subtitle_entries(metadata)
        )
        if not eligible_source:
            errors.append(f"{review_path}: A/B coverage requires a matching source-text-reference")
        if values.get("source_in_scope", 0) <= 0 or values.get("source_in_scope") != (
            values.get("source_aligned", 0) + values.get("source_excluded", 0) + values.get("source_unresolved", 0)
        ):
            errors.append(f"{review_path}: A/B source-direction coverage is incomplete")
        if values.get("source_unresolved") != 0:
            errors.append(f"{review_path}: unresolved source units block A/B fidelity completion")
        alignment_source_id = scalar(coverage, "alignment_source_id", 2)
        if not alignment_source_id or alignment_source_id == "null":
            errors.append(f"{review_path}: A/B coverage requires alignment_source_id")
        if scalar(coverage, "alignment_verified", 2) != "verified":
            errors.append(f"{review_path}: A/B coverage requires alignment_verified: verified")
        source_fingerprints = section(coverage, "source_sha256", 2)
        if alignment_source_id and alignment_source_id != "null":
            try:
                actual_sources = source_file_fingerprints(project_root, alignment_source_id)
            except (AlignmentError, OSError, UnicodeError, ValueError) as error:
                errors.append(f"{review_path}: cannot verify selected alignment source: {error}")
            else:
                for episode, actual_hash in actual_sources.items():
                    match = re.search(rf"(?m)^    {re.escape(episode)}:\s*([0-9a-f]{{64}})\s*$", source_fingerprints)
                    if not match:
                        errors.append(f"{review_path}: coverage lacks a valid source SHA-256 for {episode}")
                    elif match.group(1) != actual_hash:
                        errors.append(f"{review_path}: source coverage for {episode} is stale after source change")
    elif tier in {"C", "D"} and scalar(coverage, "human_source_fidelity_review", 2) != "verified":
        errors.append(f"{review_path}: C/D release requires verified human full-source-fidelity review")
    if scalar(coverage, "human_release_review", 2) != "verified":
        errors.append(f"{review_path}: release requires verified human_release_review")
    fingerprints = section(coverage, "master_sha256", 2)
    if not fingerprints.strip():
        errors.append(f"{review_path}: release coverage requires master_sha256 fingerprints")
    else:
        for episode in video_file_map(metadata):
            match = re.search(rf"(?m)^    {re.escape(episode)}:\s*([0-9a-f]{{64}})\s*$", fingerprints)
            master = project_root / "project/workspace/episodes" / episode / "master.ass"
            if not match:
                errors.append(f"{review_path}: coverage lacks a valid SHA-256 for {episode}")
            elif not master.is_file():
                errors.append(f"{master}: release coverage master is missing")
            elif hashlib.sha256(master.read_bytes()).hexdigest() != match.group(1):
                errors.append(f"{review_path}: coverage for {episode} is stale after master change")
    try:
        counts = ordinary_master_counts(project_root)
    except (AlignmentError, OSError, UnicodeError, ValueError) as error:
        errors.append(f"{project_root}: cannot recompute final master coverage: {error}")
        return
    primary_count = sum(item["primary"] for item in counts.values())
    secondary_count = sum(item["secondary"] for item in counts.values())
    rendered_count = sum(item["rendered_dialogue"] for item in counts.values())
    if primary_count <= 0:
        errors.append(f"{project_root}: final masters contain no declared ordinary Chinese dialogue")
    if values.get("chinese_reviewed", -1) < primary_count:
        errors.append(f"{review_path}: reviewed Chinese count is below the final ordinary-dialogue denominator")
    if values.get("static_layout_checked", -1) < rendered_count:
        errors.append(f"{review_path}: static layout coverage is below the final rendered Dialogue denominator")
    _, secondary_language = project_languages(metadata)
    if secondary_language is not None and secondary_count != values.get("source_aligned"):
        errors.append(
            f"{review_path}: source_aligned={values.get('source_aligned')} but final masters contain "
            f"{secondary_count} declared ordinary secondary events"
        )
    if secondary_language is None and secondary_count:
        errors.append(f"{project_root}: monolingual masters contain declared ordinary secondary events")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Work root containing project.yaml")
    parser.add_argument("--release", action="store_true", help="Also require and inspect release artifacts")
    parser.add_argument("--ready-for-proofreading", action="store_true", help="Require prepared masters and validate optional local target-video mappings")
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
    try:
        metadata_data = yaml.safe_load(metadata)
    except yaml.YAMLError as error:
        parser.error(f"invalid project YAML: {error}")
    if not isinstance(metadata_data, dict):
        parser.error("project.yaml must contain a mapping")

    project_schema = scalar(metadata, "schema_version")
    if project_schema != "9":
        errors.append(f"{metadata_path}: upgrade required before processing; current schema_version is 9")
        result = {"project": str(root), "errors": errors, "warnings": warnings, "valid": False}
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: {errors[0]}")
            print(f"FAIL: {root}")
        return 1
    for obsolete in ("naming", "languages", "workspace", "release", "documentation"):
        if section(metadata, obsolete):
            errors.append(f"{metadata_path}: schema 9 must not repeat fixed {obsolete} configuration")
    work_id = scalar(metadata, "id")
    if not work_id or not re.fullmatch(r"SH\d{4,}", work_id):
        errors.append(f"{metadata_path}: invalid work id")
    project_name = scalar(metadata, "project_name")
    if not project_name or not PROJECT_NAME_RE.fullmatch(project_name):
        errors.append(f"{metadata_path}: invalid project_name")
    elif root.name != f"{work_id}--{project_name}":
        errors.append(f"{root}: directory must be {work_id}--{project_name}")
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
        if not entry["scope"]:
            errors.append(f"{metadata_path}: source {entry['id']} lacks an episode scope")
        if not entry["evidence"]:
            errors.append(f"{metadata_path}: source {entry['id']} lacks evidence")
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
    review = ""
    if not review_path.is_file():
        errors.append(f"{review_path}: required control file is missing")
    for obsolete in (root / "README.md", root / "docs"):
        if obsolete.exists():
            errors.append(f"{obsolete}: obsolete parallel project documentation must be removed")
    forbidden_sidecars = ("audit.json", "coverage.json", "manifest.json", "ledger.md", "progress.md", "issues.md")
    for name in forbidden_sidecars:
        for path in root.rglob(name):
            errors.append(f"{path}: project audit/control sidecar is forbidden")
    if review_path.is_file():
        review = review_path.read_text(encoding="utf-8-sig")
        if not review.startswith("---\n") or "\n---\n" not in review[4:]:
            errors.append(f"{review_path}: YAML front matter is required")
        review_schema = scalar(review, "schema_version")
        if review_schema != "3":
            errors.append(f"{review_path}: schema_version must be 3")
        if not section(review, "coverage"):
            errors.append(f"{review_path}: review schema 3 requires a coverage block")
        if scalar(review, "status") not in {"planning", "awaiting-approval", "implementing", "final-review", "released", "blocked"}:
            errors.append(f"{review_path}: schema 3 status is invalid")
        if work_id and scalar(review, "work_id") != work_id:
            errors.append(f"{review_path}: work_id does not match project.yaml")
        for heading in ("# 当前校对轮次", "## 检查覆盖", "## 决策与实施", "## 验证与剩余风险"):
            if heading not in review:
                errors.append(f"{review_path}: required section is missing: {heading}")
        if "## 校对方案" not in review and "## 候选修改摘要" not in review:
            errors.append(f"{review_path}: required section is missing: ## 校对方案")

    design = metadata_data.get("subtitle_design")
    design = design if isinstance(design, dict) else {}
    profile = design.get("profile")
    if profile not in {"zh-mono", "zh-bilingual"}:
        errors.append(f"{metadata_path}: subtitle_design.profile must be zh-mono or zh-bilingual")
    ordinary = design.get("ordinary_styles")
    ordinary = ordinary if isinstance(ordinary, dict) else {}
    primary_styles = ordinary.get("primary")
    secondary_styles = ordinary.get("secondary")
    if not isinstance(primary_styles, list) or not primary_styles or not all(isinstance(value, str) and value for value in primary_styles):
        errors.append(f"{metadata_path}: subtitle_design.ordinary_styles.primary is required")
    if not isinstance(secondary_styles, list) or not all(isinstance(value, str) and value for value in secondary_styles):
        errors.append(f"{metadata_path}: subtitle_design.ordinary_styles.secondary must be a list")
    _, secondary_language = project_languages(metadata)
    if (profile == "zh-mono") != (secondary_language in {None, "null"}):
        errors.append(f"{metadata_path}: subtitle_design.profile must match release secondary language")
    if profile == "zh-bilingual" and not secondary_styles:
        errors.append(f"{metadata_path}: bilingual profile requires an ordinary secondary style")
    if profile == "zh-mono" and secondary_styles:
        errors.append(f"{metadata_path}: monolingual profile must not declare ordinary secondary styles")
    initialization_version = scalar(initialization, "skill_version", 2)
    if initialization_version != "1.4.2":
        errors.append(
            f"{metadata_path}: initialization.skill_version must be 1.4.2; upgrade before processing"
        )
    if initialization_state not in {"proofreading-ready", "released-existing"}:
        errors.append(f"{metadata_path}: initialization.state is invalid")
    if initialization_state == "proofreading-ready":
        for field in ("approved_by", "approved_at"):
            if not scalar(initialization, field, 2):
                errors.append(f"{metadata_path}: initialization.{field} is required")
    if args.ready_for_proofreading:
        if initialization_state not in {"proofreading-ready", "released-existing"}:
            errors.append(f"{metadata_path}: initialization state is not proofreading-ready")
        validate_working_masters(root, videos, errors, warnings)

    if args.release:
        validate_release(root, metadata, errors, warnings)
        if review and scalar(review, "status") != "released":
            errors.append(f"{review_path}: release validation requires status released")
        if review:
            validate_review_coverage(root, review_path, review, metadata, errors)
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

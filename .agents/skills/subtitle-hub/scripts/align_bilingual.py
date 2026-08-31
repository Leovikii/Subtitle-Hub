#!/usr/bin/env python3
"""Plan, apply, and verify reviewed source/Chinese ordinary-dialogue mappings."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import html
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

SKILL_VERSION = "1.4.2"
SESSION_SCHEMA = 1
PACKET_SCHEMA = 1
TEXT_SUFFIXES = {".ass", ".ssa", ".srt", ".vtt"}
TAG_BLOCK = re.compile(r"\{[^}]*\}")
NONWORD = re.compile(r"[\W_]+", re.UNICODE)


class AlignmentError(RuntimeError):
    pass


@dataclass(frozen=True)
class Event:
    ordinal: int
    line_index: int
    start: int
    end: int
    style: str
    name: str
    text: str
    raw: str


@dataclass(frozen=True)
class Unit:
    unit_id: str
    episode: str
    role: str
    ordinal: int
    start: int
    end: int
    style: str
    name: str
    text: str
    source_path: str

    def as_dict(self) -> dict[str, object]:
        return {
            "unit_id": self.unit_id,
            "episode": self.episode,
            "role": self.role,
            "ordinal": self.ordinal,
            "start_cs": self.start,
            "end_cs": self.end,
            "style": self.style,
            "name": self.name,
            "text": self.text,
            "source_path": self.source_path,
        }


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_sha256(value: object) -> str:
    body = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", dir=path.parent, delete=False) as stream:
        stream.write(text)
        temporary = Path(stream.name)
    os.replace(temporary, path)


def load_yaml(path: Path) -> dict[str, object]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise AlignmentError(f"cannot read YAML {path}: {error}") from error
    if not isinstance(value, dict):
        raise AlignmentError(f"{path} must contain a YAML mapping")
    return value


def visible(text: str) -> str:
    return TAG_BLOCK.sub("", text).replace(r"\N", "\n").replace(r"\n", "\n").replace(r"\h", " ").strip()


def ass_time(raw: str) -> int:
    match = re.fullmatch(r"(\d+):(\d{2}):(\d{2})\.(\d{2})", raw.strip())
    if not match:
        raise AlignmentError(f"invalid ASS time {raw!r}")
    hours, minutes, seconds, centiseconds = map(int, match.groups())
    if minutes >= 60 or seconds >= 60:
        raise AlignmentError(f"invalid ASS time {raw!r}")
    return ((hours * 60 + minutes) * 60 + seconds) * 100 + centiseconds


def subtitle_time(raw: str) -> int:
    match = re.fullmatch(r"(?:(\d+):)?(\d{2}):(\d{2})[,.](\d{3})", raw.strip())
    if not match:
        raise AlignmentError(f"invalid subtitle time {raw!r}")
    hours = int(match.group(1) or 0)
    minutes, seconds, milliseconds = map(int, match.groups()[1:])
    if minutes >= 60 or seconds >= 60:
        raise AlignmentError(f"invalid subtitle time {raw!r}")
    return ((hours * 60 + minutes) * 60 + seconds) * 100 + (milliseconds + 5) // 10


def format_ass_time(value: int) -> str:
    seconds, centiseconds = divmod(value, 100)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"


def parse_ass(path: Path) -> list[Event]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    try:
        section_index = lines.index("[Events]")
    except ValueError as error:
        raise AlignmentError(f"{path}: missing [Events]") from error
    format_index = next((i for i in range(section_index + 1, len(lines)) if lines[i].startswith("Format:")), None)
    if format_index is None:
        raise AlignmentError(f"{path}: missing Events Format")
    names = [part.strip() for part in lines[format_index].split(":", 1)[1].split(",")]
    required = {"Start", "End", "Style", "Text"}
    if not required.issubset(names):
        raise AlignmentError(f"{path}: Events Format lacks {sorted(required - set(names))}")
    result: list[Event] = []
    for line_index in range(format_index + 1, len(lines)):
        line = lines[line_index]
        if line.startswith("[") and line.endswith("]"):
            break
        if not line.startswith("Dialogue:"):
            continue
        fields = line.split(":", 1)[1].lstrip().split(",", len(names) - 1)
        if len(fields) != len(names):
            raise AlignmentError(f"{path}: malformed Dialogue at line {line_index + 1}")
        row = dict(zip(names, fields))
        result.append(Event(
            ordinal=len(result) + 1,
            line_index=line_index,
            start=ass_time(row["Start"]),
            end=ass_time(row["End"]),
            style=row["Style"].strip() or "Default",
            name=row.get("Name", "").strip(),
            text=row["Text"],
            raw=line,
        ))
    return result


def ass_style_names(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    try:
        start = lines.index("[V4+ Styles]") + 1
    except ValueError as error:
        raise AlignmentError(f"{path}: missing [V4+ Styles]") from error
    end = next((index for index in range(start, len(lines)) if lines[index].startswith("[") and lines[index].endswith("]")), len(lines))
    names = {
        line.split(":", 1)[1].lstrip().split(",", 1)[0].strip()
        for line in lines[start:end] if line.startswith("Style:")
    }
    if not names:
        raise AlignmentError(f"{path}: contains no styles")
    return names


def parse_srt_like(path: Path) -> list[Event]:
    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    if path.suffix.lower() == ".vtt" and text.startswith("WEBVTT"):
        text = text.split("\n", 1)[1] if "\n" in text else ""
    result: list[Event] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = block.splitlines()
        time_index = next((i for i, line in enumerate(lines) if "-->" in line), None)
        if time_index is None:
            continue
        start_raw, end_raw = [part.strip().split(" ", 1)[0] for part in lines[time_index].split("-->", 1)]
        cue_text = html.unescape("\n".join(lines[time_index + 1:]))
        cue_text = re.sub(r"<[^>]+>", "", cue_text).strip()
        result.append(Event(
            ordinal=len(result) + 1,
            line_index=time_index,
            start=subtitle_time(start_raw),
            end=subtitle_time(end_raw),
            style="External",
            name="",
            text=cue_text.replace("\n", r"\N"),
            raw=block,
        ))
    if not result:
        raise AlignmentError(f"{path}: no parseable subtitle cues")
    return result


def parse_subtitle(path: Path) -> list[Event]:
    suffix = path.suffix.lower()
    if suffix in {".ass", ".ssa"}:
        return parse_ass(path)
    if suffix in {".srt", ".vtt"}:
        return parse_srt_like(path)
    raise AlignmentError(f"unsupported subtitle format: {path}")


def unit_for(event: Event, episode: str, role: str, path: Path) -> Unit:
    clean = visible(event.text)
    signature = {
        "episode": episode,
        "role": role,
        "ordinal": event.ordinal,
        "start": event.start,
        "end": event.end,
        "style": event.style,
        "name": event.name,
        "text": clean,
    }
    return Unit(
        unit_id=f"{episode}:{role}:{event.ordinal:06d}:{json_sha256(signature)[:16]}",
        episode=episode,
        role=role,
        ordinal=event.ordinal,
        start=event.start,
        end=event.end,
        style=event.style,
        name=event.name,
        text=clean,
        source_path=str(path),
    )


def project_contract(project_root: Path) -> tuple[dict[str, object], list[str], list[str], str, str | None]:
    metadata = load_yaml(project_root / "project.yaml")
    if metadata.get("schema_version") != 9:
        raise AlignmentError("project must be upgraded to schema 9")
    initialization = metadata.get("initialization")
    if not isinstance(initialization, dict) or initialization.get("skill_version") != SKILL_VERSION:
        raise AlignmentError(f"project must be upgraded to Skill {SKILL_VERSION}")
    task = metadata.get("task")
    design = metadata.get("subtitle_design")
    release = metadata.get("release_languages")
    if not isinstance(task, dict) or not isinstance(design, dict) or not isinstance(release, dict):
        raise AlignmentError("project task/subtitle_design/release_languages is malformed")
    ordinary = design.get("ordinary_styles")
    if not isinstance(ordinary, dict):
        raise AlignmentError("subtitle_design.ordinary_styles is required")
    primary = ordinary.get("primary")
    secondary = ordinary.get("secondary")
    if not isinstance(primary, list) or not primary or not all(isinstance(v, str) and v for v in primary):
        raise AlignmentError("ordinary primary styles must be a nonempty list")
    if secondary is None:
        secondary = []
    if not isinstance(secondary, list) or not all(isinstance(v, str) and v for v in secondary):
        raise AlignmentError("ordinary secondary styles must be a list")
    source_language = task.get("source_language")
    if not isinstance(source_language, str) or not source_language:
        raise AlignmentError("task.source_language is required")
    release_secondary = release.get("secondary")
    if release_secondary is not None and not isinstance(release_secondary, str):
        raise AlignmentError("release_languages.secondary is malformed")
    return metadata, primary, secondary, source_language, release_secondary


def source_entry(metadata: dict[str, object], source_language: str, selected_id: str | None) -> dict[str, object]:
    sources = metadata.get("subtitle_sources")
    if not isinstance(sources, list):
        raise AlignmentError("subtitle_sources must be a list")
    eligible = []
    for item in sources:
        if not isinstance(item, dict):
            continue
        roles = item.get("roles")
        language = item.get("language")
        languages = language if isinstance(language, list) else [language]
        same_language = any(
            isinstance(value, str) and value.split("-", 1)[0].casefold() == source_language.split("-", 1)[0].casefold()
            for value in languages
        )
        if same_language and isinstance(roles, list) and "source-text-reference" in roles:
            eligible.append(item)
    if selected_id:
        eligible = [item for item in eligible if item.get("id") == selected_id]
    if len(eligible) != 1:
        ids = [str(item.get("id")) for item in eligible]
        raise AlignmentError(f"select exactly one source-text-reference with --source-id; eligible: {ids}")
    return eligible[0]


def master_paths(project_root: Path, episodes: list[str] | None) -> dict[str, Path]:
    root = project_root / "project" / "workspace" / "episodes"
    found = {path.parent.name: path for path in sorted(root.glob("*/master.ass"))}
    if episodes:
        missing = sorted(set(episodes) - set(found))
        if missing:
            raise AlignmentError(f"missing masters for episodes: {missing}")
        found = {episode: found[episode] for episode in episodes}
    if not found:
        raise AlignmentError("no workspace masters found")
    return found


def parse_source_overrides(values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for raw in values:
        if "=" not in raw:
            raise AlignmentError("--source must be EPISODE=PATH")
        episode, path_raw = raw.split("=", 1)
        path = Path(path_raw).expanduser().resolve()
        if episode in result or not path.is_file():
            raise AlignmentError(f"invalid or duplicate source override {raw!r}")
        result[episode] = path
    return result


def source_paths(
    project_root: Path,
    entry: dict[str, object],
    masters: dict[str, Path],
    overrides: dict[str, Path],
) -> dict[str, Path]:
    raw_root = entry.get("path")
    if not isinstance(raw_root, str):
        raise AlignmentError("selected source-text-reference has no local path")
    declared = (project_root / raw_root).resolve()
    if not declared.exists():
        raise AlignmentError(f"declared source path does not exist: {declared}")
    for episode, path in overrides.items():
        if episode not in masters:
            raise AlignmentError(f"source override episode is outside scope: {episode}")
        if declared.is_file():
            if path != declared:
                raise AlignmentError(f"source override differs from the declared source file: {path}")
        else:
            try:
                path.relative_to(declared)
            except ValueError as error:
                raise AlignmentError(f"source override is outside the declared source: {path}") from error
    files = [declared] if declared.is_file() else sorted(
        path for path in declared.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
    )
    result = dict(overrides)
    for episode in masters:
        if episode in result:
            continue
        matches = [path for path in files if episode.casefold() in path.name.casefold()]
        if len(matches) == 1:
            result[episode] = matches[0]
    remaining_episodes = [episode for episode in masters if episode not in result]
    unused_files = [path for path in files if path not in result.values()]
    if len(masters) == 1 and len(files) == 1 and remaining_episodes:
        result[remaining_episodes[0]] = files[0]
        remaining_episodes = []
    if remaining_episodes:
        raise AlignmentError(
            f"cannot safely map source files for {remaining_episodes}; use --source EPISODE=PATH. "
            f"Unused files: {[path.name for path in unused_files]}"
        )
    return result


def source_file_fingerprints(project_root: Path, selected_id: str) -> dict[str, str]:
    metadata, _, _, source_language, _ = project_contract(project_root)
    entry = source_entry(metadata, source_language, selected_id)
    masters = master_paths(project_root, None)
    paths = source_paths(project_root, entry, masters, {})
    return {episode: file_sha256(path) for episode, path in paths.items()}


def ordinary_units(path: Path, episode: str, role: str, styles: set[str] | None) -> list[Unit]:
    events = parse_subtitle(path)
    selected = [event for event in events if visible(event.text) and (styles is None or event.style in styles)]
    normalized = [
        Event(index, event.line_index, event.start, event.end, event.style, event.name, event.text, event.raw)
        for index, event in enumerate(selected, start=1)
    ]
    return [unit_for(event, episode, role, path) for event in normalized]


class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))

    def find(self, value: int) -> int:
        while self.parent[value] != value:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def join(self, left: int, right: int) -> None:
        left_root, right_root = self.find(left), self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


def candidate_groups(chinese: list[Unit], source: list[Unit]) -> list[dict[str, object]]:
    all_units = chinese + source
    union = UnionFind(len(all_units))
    for left_index, left in enumerate(chinese):
        for source_offset, right in enumerate(source, start=len(chinese)):
            if left.start < right.end and right.start < left.end:
                union.join(left_index, source_offset)
    components: dict[int, list[Unit]] = {}
    for index, unit in enumerate(all_units):
        components.setdefault(union.find(index), []).append(unit)
    ordered = sorted(
        components.values(),
        key=lambda values: (min(unit.start for unit in values), min(unit.ordinal for unit in values), values[0].role),
    )
    groups = []
    for index, values in enumerate(ordered, start=1):
        zh = sorted((unit for unit in values if unit.role == "zh"), key=lambda unit: unit.ordinal)
        src = sorted((unit for unit in values if unit.role == "source"), key=lambda unit: unit.ordinal)
        groups.append({
            "group_id": f"G{index:06d}",
            "status": "pending",
            "rationale": "",
            "chinese_units": [unit.as_dict() for unit in zh],
            "source_units": [unit.as_dict() for unit in src],
        })
    return groups


def normalized_text(group: dict[str, object], key: str) -> str:
    units = group.get(key)
    if not isinstance(units, list):
        return ""
    return NONWORD.sub("", "".join(str(unit.get("text", "")) for unit in units if isinstance(unit, dict))).casefold()


def single_name(group: dict[str, object], key: str) -> str:
    units = group.get(key)
    if not isinstance(units, list) or len(units) != 1 or not isinstance(units[0], dict):
        return ""
    return str(units[0].get("name") or "").strip().casefold()


def group_episode(group: dict[str, object]) -> str:
    for key in ("chinese_units", "source_units"):
        units = group.get(key)
        if isinstance(units, list) and units and isinstance(units[0], dict):
            return str(units[0].get("episode"))
    raise AlignmentError(f"{group.get('group_id')}: mapping group has no units")


def risk_candidates(groups: list[dict[str, object]]) -> list[dict[str, object]]:
    risks: list[dict[str, object]] = []
    for index, current in enumerate(groups):
        current_zh = normalized_text(current, "chinese_units")
        current_source = normalized_text(current, "source_units")
        if not current_zh or not current_source:
            continue
        for prior in groups[max(0, index - 2):index]:
            if group_episode(prior) != group_episode(current):
                continue
            prior_zh = normalized_text(prior, "chinese_units")
            prior_source = normalized_text(prior, "source_units")
            if not prior_zh or not prior_source or prior_source == current_source:
                continue
            zh_ratio = difflib.SequenceMatcher(None, prior_zh, current_zh).ratio()
            source_ratio = difflib.SequenceMatcher(None, prior_source, current_source).ratio()
            category = None
            if prior_zh == current_zh:
                category = "reused-chinese"
            elif min(len(prior_zh), len(current_zh)) >= 6 and zh_ratio >= 0.78 and source_ratio < 0.72:
                category = "near-duplicate-chinese"
            if category:
                risks.append({
                    "risk_id": f"R{len(risks) + 1:06d}",
                    "category": category,
                    "group_ids": [prior["group_id"], current["group_id"]],
                    "status": "pending",
                    "rationale": "",
                    "message": "Chinese is repeated or highly similar while the source groups differ; review meaning explicitly.",
                })
            if prior is groups[index - 1]:
                prior_zh_name = single_name(prior, "chinese_units")
                prior_source_name = single_name(prior, "source_units")
                current_zh_name = single_name(current, "chinese_units")
                current_source_name = single_name(current, "source_units")
                if (
                    prior_zh_name and prior_source_name and current_zh_name and current_source_name
                    and prior_zh_name == current_source_name
                    and current_zh_name == prior_source_name
                    and prior_zh_name != current_zh_name
                ):
                    risks.append({
                        "risk_id": f"R{len(risks) + 1:06d}",
                        "category": "speaker-order-reversal",
                        "group_ids": [prior["group_id"], current["group_id"]],
                        "status": "pending",
                        "rationale": "",
                        "message": "Adjacent source and Chinese Name fields appear reversed; review speaker and order.",
                    })
    return risks


def context_summary(group: dict[str, object]) -> dict[str, object]:
    return {
        "group_id": group["group_id"],
        "chinese": [unit["text"] for unit in group["chinese_units"]],
        "source": [unit["text"] for unit in group["source_units"]],
    }


def ensure_session_outside_project(output_dir: Path, project_root: Path) -> None:
    try:
        output_dir.resolve().relative_to(project_root.resolve())
    except ValueError:
        return
    raise AlignmentError("alignment sessions are disposable and must be outside the project directory")


def write_plan(
    project_root: Path,
    output_dir: Path,
    source_id: str | None,
    episode_filter: list[str] | None,
    source_values: list[str],
    batch_size: int,
) -> dict[str, object]:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise AlignmentError(f"output directory must be empty: {output_dir}")
    ensure_session_outside_project(output_dir, project_root)
    metadata, primary_styles, secondary_styles, source_language, release_secondary = project_contract(project_root)
    entry = source_entry(metadata, source_language, source_id)
    masters = master_paths(project_root, episode_filter)
    overrides = parse_source_overrides(source_values)
    sources = source_paths(project_root, entry, masters, overrides)
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "schema_version": SESSION_SCHEMA,
        "skill_version": SKILL_VERSION,
        "project_root": str(project_root),
        "project_yaml_sha256": file_sha256(project_root / "project.yaml"),
        "source_id": entry.get("id"),
        "source_language": source_language,
        "release_secondary": release_secondary,
        "ordinary_styles": {"primary": primary_styles, "secondary": secondary_styles},
        "batch_size": batch_size,
        "episodes": {},
        "batches": [],
    }
    all_groups: list[dict[str, object]] = []
    for episode, master in masters.items():
        source_path = sources[episode]
        chinese = ordinary_units(master, episode, "zh", set(primary_styles))
        source = ordinary_units(source_path, episode, "source", None)
        if not chinese or not source:
            raise AlignmentError(f"{episode}: ordinary Chinese and source units must both be nonempty")
        groups = candidate_groups(chinese, source)
        start = len(all_groups)
        for local_index, group in enumerate(groups, start=1):
            group["group_id"] = f"G{start + local_index:06d}"
        all_groups.extend(groups)
        manifest["episodes"][episode] = {
            "master": str(master),
            "master_sha256": file_sha256(master),
            "source": str(source_path),
            "source_sha256": file_sha256(source_path),
            "chinese_units": len(chinese),
            "source_units": len(source),
            "groups": len(groups),
        }
    risks = risk_candidates(all_groups)
    risk_by_group: dict[str, list[dict[str, object]]] = {}
    for risk in risks:
        risk_by_group.setdefault(risk["group_ids"][-1], []).append(risk)
    for episode in masters:
        episode_groups = [group for group in all_groups if group_episode(group) == episode]
        for offset in range(0, len(episode_groups), batch_size):
            groups = episode_groups[offset:offset + batch_size]
            batch_number = len(manifest["batches"]) + 1
            filename = f"batch-{batch_number:04d}.json"
            before = episode_groups[max(0, offset - 2):offset]
            after = episode_groups[offset + batch_size:offset + batch_size + 2]
            packet_risks = [risk for group in groups for risk in risk_by_group.get(str(group["group_id"]), [])]
            packet = {
                "schema_version": PACKET_SCHEMA,
                "skill_version": SKILL_VERSION,
                "batch_id": f"B{batch_number:04d}",
                "episode": episode,
                "group_range": [groups[0]["group_id"], groups[-1]["group_id"]],
                "context_before": [context_summary(group) for group in before],
                "groups": groups,
                "context_after": [context_summary(group) for group in after],
                "risks": packet_risks,
                "auxiliary_translation": "load only for a concrete unresolved point; no auxiliary text is expanded by default",
            }
            atomic_text(output_dir / filename, json.dumps(packet, ensure_ascii=False, indent=2) + "\n")
            manifest["batches"].append({
                "batch_id": packet["batch_id"],
                "episode": episode,
                "file": filename,
                "group_range": packet["group_range"],
                "groups": len(groups),
                "status": "pending",
            })
    manifest["summary"] = {
        "episodes": len(masters),
        "chinese_units": sum(int(item["chinese_units"]) for item in manifest["episodes"].values()),
        "source_units": sum(int(item["source_units"]) for item in manifest["episodes"].values()),
        "groups": len(all_groups),
        "batches": len(manifest["batches"]),
        "risk_candidates": len(risks),
    }
    atomic_text(output_dir / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return manifest["summary"]


def load_session(project_root: Path, session: Path) -> tuple[dict[str, object], list[tuple[Path, dict[str, object]]]]:
    manifest_path = session / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise AlignmentError(f"invalid session manifest: {error}") from error
    if manifest.get("schema_version") != SESSION_SCHEMA or manifest.get("skill_version") != SKILL_VERSION:
        raise AlignmentError(f"session must use Skill {SKILL_VERSION} schema {SESSION_SCHEMA}")
    if Path(str(manifest.get("project_root"))).resolve() != project_root.resolve():
        raise AlignmentError("session belongs to a different project")
    if file_sha256(project_root / "project.yaml") != manifest.get("project_yaml_sha256"):
        raise AlignmentError("project.yaml changed after alignment planning")
    packets = []
    for entry in manifest.get("batches", []):
        if not isinstance(entry, dict) or not isinstance(entry.get("file"), str):
            raise AlignmentError("manifest contains a malformed batch entry")
        path = session / entry["file"]
        try:
            packet = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise AlignmentError(f"invalid batch packet {path}: {error}") from error
        if packet.get("schema_version") != PACKET_SCHEMA or packet.get("batch_id") != entry.get("batch_id"):
            raise AlignmentError(f"batch packet identity mismatch: {path}")
        packets.append((path, packet))
    if not packets:
        raise AlignmentError("session contains no batch packets")
    return manifest, packets


def iter_packet_groups(packets: list[tuple[Path, dict[str, object]]]) -> Iterable[dict[str, object]]:
    for _, packet in packets:
        groups = packet.get("groups")
        if not isinstance(groups, list):
            raise AlignmentError("batch groups must be a list")
        yield from groups


def validate_decisions(
    manifest: dict[str, object],
    packets: list[tuple[Path, dict[str, object]]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    groups = list(iter_packet_groups(packets))
    group_ids = [group.get("group_id") for group in groups]
    if len(set(group_ids)) != len(group_ids):
        raise AlignmentError("a mapping group is duplicated")
    declared_chinese_ids = [
        str(unit.get("unit_id")) for group in groups for unit in group.get("chinese_units", [])
        if isinstance(unit, dict)
    ]
    declared_source_ids = [
        str(unit.get("unit_id")) for group in groups for unit in group.get("source_units", [])
        if isinstance(unit, dict)
    ]
    if len(declared_chinese_ids) != len(set(declared_chinese_ids)) or len(declared_source_ids) != len(set(declared_source_ids)):
        raise AlignmentError("a Chinese or source unit is assigned to more than one mapping group")
    chinese_ids: list[str] = []
    source_ids: list[str] = []
    prior_zh: dict[str, int] = {}
    prior_source: dict[str, int] = {}
    for group in groups:
        status = group.get("status")
        rationale = str(group.get("rationale") or "").strip()
        zh = group.get("chinese_units")
        source = group.get("source_units")
        if not isinstance(zh, list) or not isinstance(source, list):
            raise AlignmentError(f"{group.get('group_id')}: malformed unit lists")
        if status == "confirmed":
            if not zh or not source:
                raise AlignmentError(f"{group.get('group_id')}: missing ordinary dialogue cannot be confirmed")
            if (len(zh), len(source)) != (1, 1) and not rationale:
                raise AlignmentError(f"{group.get('group_id')}: non-1:1 confirmation requires a rationale")
        elif status == "excluded-special":
            if zh or not source or not rationale:
                raise AlignmentError(f"{group.get('group_id')}: only source-only special text may be excluded with a rationale")
        else:
            raise AlignmentError(f"{group.get('group_id')}: unresolved status {status!r} blocks apply/verify")
        for unit in zh:
            chinese_ids.append(str(unit.get("unit_id")))
            ordinal = int(unit.get("ordinal", -1))
            episode = str(unit.get("episode"))
            if ordinal < prior_zh.get(episode, -1):
                raise AlignmentError("Chinese mapping order is not monotonic")
            prior_zh[episode] = ordinal
        for unit in source:
            source_ids.append(str(unit.get("unit_id")))
            ordinal = int(unit.get("ordinal", -1))
            episode = str(unit.get("episode"))
            if ordinal < prior_source.get(episode, -1):
                raise AlignmentError("source mapping order is not monotonic")
            prior_source[episode] = ordinal
    if len(chinese_ids) != int(manifest["summary"]["chinese_units"]):
        raise AlignmentError("Chinese mapping denominator is incomplete")
    if len(source_ids) != int(manifest["summary"]["source_units"]):
        raise AlignmentError("source mapping denominator is incomplete")
    risks = []
    for _, packet in packets:
        packet_risks = packet.get("risks", [])
        if not isinstance(packet_risks, list):
            raise AlignmentError("batch risks must be a list")
        for risk in packet_risks:
            if risk.get("status") != "cleared" or not str(risk.get("rationale") or "").strip():
                raise AlignmentError(f"{risk.get('risk_id')}: duplicate/near-duplicate risk requires an explicit disposition")
            risks.append(risk)
    return groups, risks


def current_units(manifest: dict[str, object]) -> tuple[dict[str, list[Unit]], dict[str, list[Unit]]]:
    primary = set(manifest["ordinary_styles"]["primary"])
    chinese: dict[str, list[Unit]] = {}
    source: dict[str, list[Unit]] = {}
    for episode, item in manifest["episodes"].items():
        master = Path(item["master"])
        source_path = Path(item["source"])
        chinese[episode] = ordinary_units(master, episode, "zh", primary)
        source[episode] = ordinary_units(source_path, episode, "source", None)
    return chinese, source


def packet_unit_ids(groups: list[dict[str, object]], key: str) -> list[str]:
    return [str(unit["unit_id"]) for group in groups for unit in group[key]]


def validate_unit_identity(
    manifest: dict[str, object],
    groups: list[dict[str, object]],
    chinese: dict[str, list[Unit]],
    source: dict[str, list[Unit]],
) -> None:
    actual_zh = [unit.unit_id for episode in manifest["episodes"] for unit in chinese[episode]]
    actual_source = [unit.unit_id for episode in manifest["episodes"] for unit in source[episode]]
    if packet_unit_ids(groups, "chinese_units") != actual_zh:
        raise AlignmentError("Chinese ordinary-dialogue units changed or were reordered")
    if packet_unit_ids(groups, "source_units") != actual_source:
        raise AlignmentError("source ordinary-dialogue units changed or were reordered")


def unit_key(unit: dict[str, object] | Unit) -> tuple[str, str, int]:
    if isinstance(unit, Unit):
        return unit.episode, unit.role, unit.ordinal
    return str(unit.get("episode")), str(unit.get("role")), int(unit.get("ordinal", -1))


def invalidate_changed_batches(
    session: Path,
    manifest: dict[str, object],
    packets: list[tuple[Path, dict[str, object]]],
    chinese: dict[str, list[Unit]],
    source: dict[str, list[Unit]],
) -> list[str]:
    actual = {
        unit_key(unit): unit.unit_id
        for episode in manifest["episodes"]
        for unit in chinese[episode] + source[episode]
    }
    expected_keys: set[tuple[str, str, int]] = set()
    changed: list[str] = []
    packet_by_id = {str(packet["batch_id"]): packet for _, packet in packets}
    for entry in manifest["batches"]:
        packet = packet_by_id[str(entry["batch_id"])]
        packet_changed = False
        for group in packet["groups"]:
            for key in ("chinese_units", "source_units"):
                for unit in group[key]:
                    identity = unit_key(unit)
                    expected_keys.add(identity)
                    if actual.get(identity) != unit.get("unit_id"):
                        packet_changed = True
        if packet_changed:
            entry["status"] = "invalidated"
            changed.append(str(entry["batch_id"]))
    new_keys = set(actual) - expected_keys
    if new_keys:
        affected_episodes = {key[0] for key in new_keys}
        for entry in manifest["batches"]:
            if entry.get("episode") in affected_episodes and entry["batch_id"] not in changed:
                entry["status"] = "invalidated"
                changed.append(str(entry["batch_id"]))
    if changed:
        atomic_text(session / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return changed


def master_secondary_units(path: Path, episode: str, styles: set[str]) -> list[Unit]:
    if not styles:
        return []
    return ordinary_units(path, episode, "source", styles)


def source_event_line(unit: dict[str, object], style: str) -> str:
    text = str(unit["text"]).replace("\n", r"\N")
    name = str(unit.get("name") or "").replace(",", " ")
    return (
        f"Dialogue: 0,{format_ass_time(int(unit['start_cs']))},{format_ass_time(int(unit['end_cs']))},"
        f"{style},{name},0,0,0,,{text}"
    )


def replace_secondary_events(master: Path, secondary_styles: set[str], new_lines: list[tuple[int, str]]) -> None:
    text = master.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines()
    events = parse_ass(master)
    by_line = {event.line_index: event for event in events}
    events_header = lines.index("[Events]")
    next_section = next(
        (index for index in range(events_header + 1, len(lines)) if lines[index].startswith("[") and lines[index].endswith("]")),
        len(lines),
    )
    primary_before = [event.raw for event in events if event.style not in secondary_styles]
    kept: list[str] = []
    insertion_starts: list[tuple[int, str]] = sorted(new_lines, key=lambda item: item[0])
    inserted = 0
    for index, line in enumerate(lines):
        if index == next_section:
            kept.extend(value for _, value in insertion_starts[inserted:])
            inserted = len(insertion_starts)
        event = by_line.get(index)
        if event and event.style in secondary_styles:
            continue
        if event:
            while inserted < len(insertion_starts) and insertion_starts[inserted][0] < event.start:
                kept.append(insertion_starts[inserted][1])
                inserted += 1
        kept.append(line)
    kept.extend(line for _, line in insertion_starts[inserted:])
    rendered = "\n".join(kept) + "\n"
    temporary = master.with_name(master.name + ".align-tmp")
    temporary.write_text(rendered, encoding="utf-8", newline="\n")
    try:
        after = parse_ass(temporary)
        primary_after = [event.raw for event in after if event.style not in secondary_styles]
        if primary_after != primary_before:
            raise AlignmentError(f"{master}: apply would change non-secondary Dialogue events")
        os.replace(temporary, master)
    finally:
        if temporary.exists():
            temporary.unlink()


def update_batch_statuses(session: Path, manifest: dict[str, object], packets: list[tuple[Path, dict[str, object]]]) -> None:
    packet_by_id = {str(packet.get("batch_id")): packet for _, packet in packets}
    for entry in manifest["batches"]:
        packet = packet_by_id[str(entry["batch_id"])]
        try:
            validate_decisions(
                {**manifest, "summary": {**manifest["summary"], "groups": len(packet["groups"]),
                    "chinese_units": sum(len(group["chinese_units"]) for group in packet["groups"]),
                    "source_units": sum(len(group["source_units"]) for group in packet["groups"]) }},
                [(session / entry["file"], packet)],
            )
            entry["status"] = "complete"
        except AlignmentError:
            entry["status"] = "pending"
    atomic_text(session / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


def apply_session(project_root: Path, session: Path, secondary_style: str | None) -> dict[str, object]:
    manifest, packets = load_session(project_root, session)
    update_batch_statuses(session, manifest, packets)
    groups, risks = validate_decisions(manifest, packets)
    chinese, source = current_units(manifest)
    changed = invalidate_changed_batches(session, manifest, packets, chinese, source)
    if changed:
        raise AlignmentError(f"alignment input changed after planning; re-plan affected batches: {changed}")
    validate_unit_identity(manifest, groups, chinese, source)
    secondary_styles = list(manifest["ordinary_styles"]["secondary"])
    if manifest.get("release_secondary") is None:
        raise AlignmentError("apply is only valid for a bilingual release")
    chosen = secondary_style or (secondary_styles[0] if len(secondary_styles) == 1 else None)
    if not chosen or chosen not in secondary_styles:
        raise AlignmentError("select one declared ordinary secondary style with --secondary-style")
    groups_by_episode: dict[str, list[dict[str, object]]] = {episode: [] for episode in manifest["episodes"]}
    for group in groups:
        units = group["source_units"]
        if units:
            groups_by_episode[str(units[0]["episode"])].append(group)
    for episode, item in manifest["episodes"].items():
        new_lines = []
        for group in groups_by_episode[episode]:
            if group["status"] != "confirmed":
                continue
            for unit in group["source_units"]:
                new_lines.append((int(unit["start_cs"]), source_event_line(unit, chosen)))
        master = Path(item["master"])
        if chosen not in ass_style_names(master):
            raise AlignmentError(f"{episode}: declared secondary style {chosen!r} is absent from the master")
        replace_secondary_events(master, set(secondary_styles), new_lines)
        item["applied_master_sha256"] = file_sha256(master)
    manifest["applied"] = True
    atomic_text(session / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return {"episodes": len(manifest["episodes"]), "groups": len(groups), "risks_cleared": len(risks)}


def verify_session(project_root: Path, session: Path) -> dict[str, object]:
    manifest, packets = load_session(project_root, session)
    update_batch_statuses(session, manifest, packets)
    groups, risks = validate_decisions(manifest, packets)
    chinese, source = current_units(manifest)
    changed = invalidate_changed_batches(session, manifest, packets, chinese, source)
    if changed:
        raise AlignmentError(f"alignment input changed after planning; re-plan affected batches: {changed}")
    validate_unit_identity(manifest, groups, chinese, source)
    secondary_styles = set(manifest["ordinary_styles"]["secondary"])
    release_secondary = manifest.get("release_secondary")
    episode_results = {}
    for episode, item in manifest["episodes"].items():
        mapped_source = [
            unit for group in groups if group["status"] == "confirmed"
            for unit in group["source_units"] if unit["episode"] == episode
        ]
        if release_secondary is not None:
            final_source = master_secondary_units(Path(item["master"]), episode, secondary_styles)
            expected = [(int(unit["start_cs"]), int(unit["end_cs"]), str(unit["text"])) for unit in mapped_source]
            actual = [(unit.start, unit.end, unit.text) for unit in final_source]
            if actual != expected:
                raise AlignmentError(f"{episode}: final master secondary dialogue differs from the reviewed mapping")
        episode_results[episode] = {
            "master_sha256": file_sha256(Path(item["master"])),
            "source_sha256": file_sha256(Path(item["source"])),
            "chinese_units": len(chinese[episode]),
            "source_units": len(source[episode]),
            "source_aligned": len(mapped_source),
            "source_excluded_special": len(source[episode]) - len(mapped_source),
        }
    update_batch_statuses(session, manifest, packets)
    return {
        "schema_version": 1,
        "valid": True,
        "alignment_source_id": manifest["source_id"],
        "episodes": episode_results,
        "summary": {
            "chinese_units": sum(item["chinese_units"] for item in episode_results.values()),
            "source_units": sum(item["source_units"] for item in episode_results.values()),
            "source_aligned": sum(item["source_aligned"] for item in episode_results.values()),
            "source_excluded_special": sum(item["source_excluded_special"] for item in episode_results.values()),
            "groups": len(groups),
            "risks_cleared": len(risks),
            "source_unresolved": 0,
        },
    }


def ordinary_master_counts(project_root: Path) -> dict[str, dict[str, int]]:
    _, primary, secondary, _, _ = project_contract(project_root)
    result = {}
    for episode, path in master_paths(project_root, None).items():
        events = parse_ass(path)
        result[episode] = {
            "primary": sum(event.style in set(primary) and bool(visible(event.text)) for event in events),
            "secondary": sum(event.style in set(secondary) and bool(visible(event.text)) for event in events),
            "rendered_dialogue": sum(bool(visible(event.text)) for event in events),
        }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    plan = subparsers.add_parser("plan", help="Create a disposable exhaustive mapping session")
    plan.add_argument("project", type=Path)
    plan.add_argument("--output-dir", type=Path, required=True)
    plan.add_argument("--source-id")
    plan.add_argument("--episode", action="append", default=[])
    plan.add_argument("--source", action="append", default=[], help="Explicit EPISODE=PATH source mapping")
    plan.add_argument("--batch-size", type=int, default=16)
    apply_parser = subparsers.add_parser("apply", help="Project confirmed source units without changing Chinese")
    apply_parser.add_argument("project", type=Path)
    apply_parser.add_argument("--session", type=Path, required=True)
    apply_parser.add_argument("--secondary-style")
    verify = subparsers.add_parser("verify", help="Verify the complete reviewed mapping and final master")
    verify.add_argument("project", type=Path)
    verify.add_argument("--session", type=Path, required=True)
    try:
        args = parser.parse_args()
        project_root = args.project.expanduser().resolve()
        if args.command == "plan":
            if not 1 <= args.batch_size <= 50:
                raise AlignmentError("--batch-size must be between 1 and 50")
            result = write_plan(
                project_root,
                args.output_dir.expanduser().resolve(),
                args.source_id,
                args.episode or None,
                args.source,
                args.batch_size,
            )
        elif args.command == "apply":
            result = apply_session(project_root, args.session.expanduser().resolve(), args.secondary_style)
        else:
            result = verify_session(project_root, args.session.expanduser().resolve())
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (AlignmentError, OSError, UnicodeError, ValueError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

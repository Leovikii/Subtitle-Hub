#!/usr/bin/env python3
"""Audit ASS text, timing, coverage, and static layout without media processing."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

TAG_BLOCK = re.compile(r"\{[^}]*\}")
HAN = re.compile(r"[\u3400-\u9fff]")
KANA = re.compile(r"[\u3040-\u30ff]")
POS = re.compile(r"\\pos\(([-\d.]+),([-\d.]+)\)")
MOVE = re.compile(r"\\move\(([^)]*)\)")
RESET = re.compile(r"\\r([^\\}]*)")
CLIP = re.compile(r"\\i?clip\(([^)]*)\)")
ALPHA = re.compile(r"\\(?:alpha|[1-4]a)&H([0-9A-Fa-f]{2})&")
SCALE = re.compile(r"\\fsc([xy])(-?[\d.]+)")
SIZE = re.compile(r"\\fs(-?[\d.]+)")
FADE = re.compile(r"\\(?:fad|fade)\(([^)]*)\)")
TRANSFORM = re.compile(r"\\t\(([^)]*)\)")


class AuditError(RuntimeError):
    pass


@dataclass
class Style:
    name: str
    fontsize: float
    scale_x: float
    scale_y: float
    alignment: int
    margin_l: int
    margin_r: int
    margin_v: int


@dataclass
class Event:
    index: int
    start: int
    end: int
    style: str
    layer: int
    text: str


def ass_time(value: str) -> int:
    match = re.fullmatch(r"(\d+):(\d{2}):(\d{2})\.(\d{2})", value.strip())
    if not match:
        raise AuditError(f"invalid ASS time {value!r}")
    h, m, s, cs = map(int, match.groups())
    return ((h * 60 + m) * 60 + s) * 100 + cs


def section(text: str, name: str) -> list[str]:
    lines = text.splitlines()
    try:
        start = lines.index(name) + 1
    except ValueError as error:
        raise AuditError(f"missing {name}") from error
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("[") and lines[i].endswith("]")), len(lines))
    return lines[start:end]


def script_info(text: str) -> tuple[int, int, int]:
    values = {}
    for line in section(text, "[Script Info]"):
        if ":" in line and not line.startswith(";"):
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    try:
        return int(values["PlayResX"]), int(values["PlayResY"]), int(values.get("WrapStyle", "0"))
    except (KeyError, ValueError) as error:
        raise AuditError("invalid PlayRes/WrapStyle") from error


def parse_styles(text: str) -> dict[str, Style]:
    lines = section(text, "[V4+ Styles]")
    format_line = next((line for line in lines if line.startswith("Format:")), None)
    if not format_line:
        raise AuditError("missing style Format")
    names = [value.strip() for value in format_line.split(":", 1)[1].split(",")]
    result = {}
    for line in lines:
        if not line.startswith("Style:"):
            continue
        fields = [value.strip() for value in line.split(":", 1)[1].split(",")]
        row = dict(zip(names, fields))
        try:
            style = Style(row["Name"], float(row["Fontsize"]), float(row["ScaleX"]), float(row["ScaleY"]), int(row["Alignment"]), int(row["MarginL"]), int(row["MarginR"]), int(row["MarginV"]))
        except (KeyError, ValueError) as error:
            raise AuditError(f"malformed style {fields[0] if fields else '?'}") from error
        if style.name in result:
            raise AuditError(f"duplicate style {style.name}")
        result[style.name] = style
    return result


def parse_events(text: str) -> list[Event]:
    lines = section(text, "[Events]")
    format_line = next((line for line in lines if line.startswith("Format:")), None)
    if not format_line:
        raise AuditError("missing event Format")
    names = [value.strip() for value in format_line.split(":", 1)[1].split(",")]
    events = []
    for index, line in enumerate(lines, start=1):
        if not line.startswith("Dialogue:"):
            continue
        fields = [value.strip() for value in line.split(":", 1)[1].split(",", len(names) - 1)]
        row = dict(zip(names, fields))
        try:
            events.append(Event(index, ass_time(row["Start"]), ass_time(row["End"]), row["Style"] or "Default", int(row.get("Layer", "0")), row["Text"]))
        except (KeyError, ValueError) as error:
            raise AuditError(f"malformed Dialogue at Events line {index}") from error
    return events


def visible(text: str) -> str:
    return TAG_BLOCK.sub("", text).replace(r"\N", "\n").replace(r"\n", "\n").replace(r"\h", " ")


def box(event: Event, style: Style, width: int, height: int) -> tuple[float, float, float, float]:
    clean = visible(event.text)
    lines = clean.splitlines() or [""]
    override_size = [float(value) for value in SIZE.findall(event.text) if float(value) > 0]
    fs = override_size[-1] if override_size else style.fontsize
    sx = style.scale_x / 100
    sy = style.scale_y / 100
    for axis, value in SCALE.findall(event.text):
        if float(value) > 0:
            sx, sy = (float(value) / 100, sy) if axis == "x" else (sx, float(value) / 100)
    text_w = min(width, max((len(line) for line in lines), default=0) * fs * 0.58 * sx)
    text_h = len(lines) * fs * 1.18 * sy
    pos = POS.search(event.text)
    if pos:
        cx, cy = float(pos.group(1)), float(pos.group(2))
        return cx - text_w / 2, cy - text_h / 2, cx + text_w / 2, cy + text_h / 2
    column = (style.alignment - 1) % 3
    row = (style.alignment - 1) // 3
    x1 = style.margin_l if column == 0 else (width - text_w) / 2 if column == 1 else width - style.margin_r - text_w
    y1 = height - style.margin_v - text_h if row == 0 else (height - text_h) / 2 if row == 1 else style.margin_v
    return x1, y1, x1 + text_w, y1 + text_h


def overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return max(a[0], b[0]) < min(a[2], b[2]) and max(a[1], b[1]) < min(a[3], b[3])


def finding(kind: str, severity: str, event: Event, message: str, other: int | None = None) -> dict[str, object]:
    item = {"classification": severity, "category": kind, "event": event.index, "start_cs": event.start, "style": event.style, "message": message}
    if other is not None:
        item["other_event"] = other
    return item


def audit(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    text = data.decode("utf-8-sig")
    width, height, wrap_style = script_info(text)
    styles = parse_styles(text)
    events = parse_events(text)
    findings: list[dict[str, object]] = []
    chinese = source = 0
    chinese_events: list[Event] = []
    source_events: list[Event] = []
    boxes = {}
    for event in events:
        clean = visible(event.text)
        is_chinese = bool(HAN.search(clean))
        is_source = bool(KANA.search(clean) or (re.search(r"[A-Za-zÁ-ž]", clean) and not HAN.search(clean)))
        chinese += is_chinese
        source += is_source
        if is_chinese:
            chinese_events.append(event)
        if is_source:
            source_events.append(event)
        if event.style not in styles:
            findings.append(finding("undefined-style", "confirmed", event, "event references an undefined style"))
            continue
        style = styles[event.style]
        boxes[event.index] = box(event, style, width, height)
        duration = event.end - event.start
        if duration <= 0:
            findings.append(finding("invalid-duration", "confirmed", event, "end time is not after start time"))
        elif duration < 50 and clean.strip():
            findings.append(finding("short-duration", "media-required", event, "visible text is shorter than 0.50 seconds"))
        explicit_lines = clean.count("\n") + 1
        if explicit_lines > 2:
            findings.append(finding("explicit-lines", "risk", event, f"visible text has {explicit_lines} explicit lines"))
        available = max(1, width - style.margin_l - style.margin_r)
        estimated = max((len(line) for line in clean.splitlines()), default=0) * style.fontsize * style.scale_x / 100 * 0.58
        if estimated > available:
            findings.append(finding("predicted-wrap", "risk", event, "estimated line width exceeds the style's available width"))
        x1, y1, x2, y2 = boxes[event.index]
        if x2 <= 0 or y2 <= 0 or x1 >= width or y1 >= height:
            findings.append(finding("off-screen", "confirmed", event, "estimated event box is fully outside PlayRes"))
        elif x1 < 0 or y1 < 0 or x2 > width or y2 > height:
            findings.append(finding("off-screen", "risk", event, "estimated event box crosses PlayRes boundary"))
        if any(int(value, 16) == 255 for value in ALPHA.findall(event.text)):
            findings.append(finding("hidden-alpha", "risk", event, "override sets a fully transparent alpha channel"))
        if any(float(value) <= 0 for _, value in SCALE.findall(event.text)) or any(float(value) <= 0 for value in SIZE.findall(event.text)):
            findings.append(finding("hidden-scale-size", "confirmed", event, "override uses non-positive size or scale"))
        for reset in RESET.findall(event.text):
            if reset.strip() and reset.strip() not in styles:
                findings.append(finding("undefined-reset-style", "confirmed", event, f"undefined reset style {reset.strip()!r}"))
        for match, expected, label in ((MOVE, {4, 6}, "move"), (FADE, {2, 7}, "fade")):
            for raw in match.findall(event.text):
                if len([value for value in raw.split(",") if value.strip()]) not in expected:
                    findings.append(finding("malformed-tag", "confirmed", event, f"malformed {label} tag"))
        if TRANSFORM.search(event.text) and not all(raw.strip() for raw in TRANSFORM.findall(event.text)):
            findings.append(finding("malformed-transform", "confirmed", event, "empty transform tag"))
        for raw in CLIP.findall(event.text):
            coords = [value.strip() for value in raw.split(",")]
            if len(coords) == 4:
                try:
                    x1c, y1c, x2c, y2c = map(float, coords)
                    if x2c <= x1c or y2c <= y1c:
                        findings.append(finding("empty-clip", "confirmed", event, "rectangular clip has no positive area"))
                except ValueError:
                    pass

    chinese_matches = {event.index: [] for event in chinese_events}
    source_matches = {event.index: [] for event in source_events}
    for chinese_event in chinese_events:
        for source_event in source_events:
            if chinese_event.start < source_event.end and source_event.start < chinese_event.end:
                chinese_matches[chinese_event.index].append(source_event.index)
                source_matches[source_event.index].append(chinese_event.index)
    for event in chinese_events:
        if source_events and not chinese_matches[event.index]:
            findings.append(finding("chinese-without-source", "risk", event, "Chinese event has no overlapping source-text event"))
    for event in source_events:
        if chinese_events and not source_matches[event.index]:
            findings.append(finding("source-without-chinese", "risk", event, "source-text event has no overlapping Chinese event"))

    for i, left in enumerate(events):
        if left.index not in boxes:
            continue
        for right in events[i + 1:]:
            if right.start >= left.end or left.start >= right.end or right.index not in boxes:
                continue
            if overlap(boxes[left.index], boxes[right.index]) and left.layer == right.layer:
                findings.append(finding("spatial-collision", "risk", left, "simultaneous same-layer event boxes intersect", right.index))

    counts = {name: sum(item["classification"] == name for item in findings) for name in ("confirmed", "risk", "media-required")}
    return {
        "schema_version": 1,
        "file": str(path),
        "sha256": hashlib.sha256(data).hexdigest(),
        "play_res": [width, height],
        "wrap_style": wrap_style,
        "events": len(events),
        "chinese_in_scope": chinese,
        "source_text_events": source,
        "alignment": {
            "chinese_resolved_by_time": sum(bool(value) for value in chinese_matches.values()),
            "chinese_unresolved_by_time": sum(not value for value in chinese_matches.values()),
            "source_aligned_by_time": sum(bool(value) for value in source_matches.values()),
            "source_unresolved_by_time": sum(not value for value in source_matches.values()),
            "many_to_many_groups": sum(len(value) > 1 for value in chinese_matches.values()) + sum(len(value) > 1 for value in source_matches.values()),
        },
        "static_layout_checked": len(events),
        "finding_counts": counts,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, help="Optional disposable JSON output path; stdout is the default")
    args = parser.parse_args()
    try:
        report = {"schema_version": 1, "files": [audit(path.resolve()) for path in args.files]}
    except (AuditError, OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Check or refresh Bangumi identity snapshots in project.yaml files."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

from build_subtitle_packages import (
    PackageError,
    REPOSITORY_ROOT,
    WORKS_ROOT,
    bangumi_identity,
    yaml_scalar,
)


USER_AGENT = "Subtitle-Hub/1.0 (Bangumi metadata synchronization)"
PLATFORMS = {
    "tv": {"TV", "欧美剧", "日剧", "韩剧", "国产剧"},
    "ona": {"WEB", "网络剧"},
    "movie": {"剧场版", "电影"},
    "ova": {"OVA"},
    "special": {"SP", "特别篇"},
}


class MetadataError(RuntimeError):
    pass


def fetch_json(url: str) -> dict[str, object]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.load(response)
    except (urllib.error.URLError, json.JSONDecodeError) as error:
        raise MetadataError(f"failed to read {url}: {error}") from error


def remote_identity(project_root: Path) -> tuple[str, str]:
    subject_id, _, _, api_url = bangumi_identity(project_root)
    payload = fetch_json(api_url)
    if payload.get("id") != int(subject_id):
        raise MetadataError(f"{api_url}: returned a different subject ID")
    if payload.get("type") not in {2, 6}:
        raise MetadataError(f"{api_url}: subject is not an animation or live-action entry")

    metadata = (project_root / "project.yaml").read_text(encoding="utf-8")
    project_type = yaml_scalar(metadata, "type", 0)
    identity_match = re.search(r"(?ms)^identity:\s*$.*?(?=^[^ ]|\Z)", metadata)
    identity = identity_match.group(0) if identity_match else ""
    identity_total = int(yaml_scalar(identity, "total_episodes", 2))
    platform = payload.get("platform")
    if project_type not in PLATFORMS or platform not in PLATFORMS[project_type]:
        raise MetadataError(
            f"{api_url}: platform {platform!r} does not match project type {project_type!r}"
        )
    remote_episodes = payload.get("total_episodes") or payload.get("eps")
    if remote_episodes != identity_total:
        raise MetadataError(
            f"{api_url}: episode count {remote_episodes!r} does not match identity.total_episodes {identity_total}"
        )

    title_ja = payload.get("name")
    title_zh_hans = payload.get("name_cn")
    if not isinstance(title_ja, str) or not title_ja.strip():
        raise MetadataError(f"{api_url}: missing name")
    if not isinstance(title_zh_hans, str) or not title_zh_hans.strip():
        raise MetadataError(f"{api_url}: missing name_cn; user confirmation is required")
    return title_ja, title_zh_hans


def replace_scalar(text: str, field: str, indent: int, value: str) -> str:
    pattern = re.compile(rf"^({' ' * indent}{re.escape(field)}:)\s*.*$", re.MULTILINE)
    serialized = json.dumps(value, ensure_ascii=False)
    updated, count = pattern.subn(lambda match: f"{match.group(1)} {serialized}", text, count=1)
    if count != 1:
        raise MetadataError(f"project.yaml: cannot update {field} at indentation {indent}")
    return updated


def process(project_file: Path, write: bool) -> bool:
    project_root = project_file.parent
    subject_id, current_ja, current_zh_hans, _ = bangumi_identity(project_root)
    remote_ja, remote_zh_hans = remote_identity(project_root)
    changed = (current_ja, current_zh_hans) != (remote_ja, remote_zh_hans)
    if write:
        metadata = project_file.read_text(encoding="utf-8")
        updated = replace_scalar(metadata, "ja", 4, remote_ja)
        updated = replace_scalar(updated, "zh-Hans", 4, remote_zh_hans)
        updated = replace_scalar(updated, "verification", 2, "api-verified")
        updated = replace_scalar(updated, "verified_at", 2, date.today().isoformat())
        if updated != metadata:
            project_file.write_text(updated, encoding="utf-8")
            print(
                f"updated {project_file.relative_to(REPOSITORY_ROOT)} "
                f"from Bangumi {subject_id}"
            )
        else:
            print(f"current {project_file.relative_to(REPOSITORY_ROOT)} (Bangumi {subject_id})")
    elif changed:
        print(
            f"outdated {project_file.relative_to(REPOSITORY_ROOT)}: "
            f"{current_ja!r} / {current_zh_hans!r} -> {remote_ja!r} / {remote_zh_hans!r}"
        )
    else:
        print(f"current {project_file.relative_to(REPOSITORY_ROOT)} (Bangumi {subject_id})")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if a snapshot differs")
    mode.add_argument("--write", action="store_true", help="write API titles into project.yaml")
    parser.add_argument("projects", nargs="*", type=Path, help="project.yaml paths")
    args = parser.parse_args()
    project_files = args.projects or sorted(WORKS_ROOT.glob("**/project.yaml"))
    if not project_files:
        raise MetadataError("no project.yaml files found")
    changed = False
    for path in project_files:
        changed = process(path.resolve(), args.write) or changed
    return 1 if changed and not args.write else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (MetadataError, PackageError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)

"""Validate the repository's work directory layout and identifiers."""

import re
from pathlib import Path

WORK_ID_RE = re.compile(r"SH[0-9]{4,}")
SLUG_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
EPISODE_PATTERNS = {
    "tv": re.compile(r"S[0-9]{2}E[0-9]{2,3}"),
    "ona": re.compile(r"S[0-9]{2}E[0-9]{2,3}"),
    "ova": re.compile(r"OVA[0-9]{2,3}"),
    "special": re.compile(r"SP[0-9]{2,3}"),
    "movie": re.compile(r"MOVIE"),
}


def validate_project_name(name: object) -> None:
    if not isinstance(name, str) or not 3 <= len(name) <= 48 or not SLUG_RE.fullmatch(name):
        raise ValueError("project name must be 3-48 lowercase ASCII letters/digits separated by single hyphens")


def validate_series_directory(repository: Path, series: Path) -> None:
    works = repository / "works"
    if (not (repository / "catalog.yaml").is_file() or not works.is_dir()
            or series.parent.name != "works" or series.parent != works):
        raise ValueError(f"{series}: series must be an immediate child of the repository's works directory")
    if not SLUG_RE.fullmatch(series.name):
        raise ValueError(f"{series}: series name must use lowercase ASCII letters/digits separated by single hyphens")


def validate_work_directory(root: Path, work_id: object, name: object) -> None:
    validate_series_directory(root.parent.parent.parent, root.parent)
    if not isinstance(work_id, str) or not WORK_ID_RE.fullmatch(work_id):
        raise ValueError("work ID must be SH followed by at least four ASCII digits")
    validate_project_name(name)
    if root.name != f"{work_id}--{name}":
        raise ValueError(f"{root}: directory must be {work_id}--{name}")

"""Keep project work products out of Skill installations."""

import os
import tempfile
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]


def writable_path(path: Path) -> Path:
    resolved = path.expanduser().resolve()
    parts = tuple(part.casefold() for part in resolved.parts)
    codex_root = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser().resolve()
    if (resolved.is_relative_to(SKILL_ROOT) or resolved.is_relative_to((codex_root / "skills").resolve())
            or any(pair in {(".agents", "skills"), (".codex", "skills")} for pair in zip(parts, parts[1:]))
            or any((directory / "SKILL.md").is_file() for directory in (resolved, *resolved.parents))):
        raise ValueError(f"Skill files are read-only during project execution: {resolved}")
    return resolved


def disposable_path(path: Path) -> Path:
    resolved = writable_path(path)
    temp_root = Path(tempfile.gettempdir()).resolve()
    if resolved == temp_root or not resolved.is_relative_to(temp_root):
        raise ValueError(f"disposable output must stay under the system temporary directory {temp_root}")
    return resolved


def write_disposable_text(path: Path, text: str) -> None:
    output = disposable_path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    stream = tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", dir=output.parent, delete=False)
    temporary = Path(stream.name)
    try:
        with stream:
            stream.write(text)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)

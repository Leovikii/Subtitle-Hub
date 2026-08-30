#!/usr/bin/env python3
"""Create or inspect the shared isolated Python runtime for Subtitle Hub."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
REQUIREMENTS = SKILL_ROOT / "requirements.txt"
RUNTIME_ROOT = Path.home() / ".codex" / "subtitle-hub"
VENV_ROOT = RUNTIME_ROOT / "venv"
STATE_ROOT = RUNTIME_ROOT / "state"
MARKER = RUNTIME_ROOT / "runtime.json"


def runtime_python() -> Path:
    return VENV_ROOT / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def requirements_hash() -> str:
    return hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()


def valid_runtime() -> bool:
    if not runtime_python().is_file() or not MARKER.is_file():
        return False
    try:
        marker = json.loads(MARKER.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return marker == {"schema_version": 1, "requirements_sha256": requirements_hash()}


def create_runtime() -> None:
    if valid_runtime():
        return
    RUNTIME_ROOT.mkdir(parents=True, exist_ok=True)
    staging = RUNTIME_ROOT / "venv-next"
    if staging.exists():
        shutil.rmtree(staging)
    venv.EnvBuilder(with_pip=True, clear=False).create(staging)
    staging_python = staging / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    try:
        subprocess.run(
            [str(staging_python), "-m", "pip", "install", "--disable-pip-version-check", "--requirement", str(REQUIREMENTS)],
            check=True,
        )
        if VENV_ROOT.exists():
            shutil.rmtree(VENV_ROOT)
        staging.replace(VENV_ROOT)
        STATE_ROOT.mkdir(parents=True, exist_ok=True)
        marker = {"schema_version": 1, "requirements_sha256": requirements_hash()}
        MARKER.write_text(json.dumps(marker, indent=2) + "\n", encoding="utf-8")
    except Exception:
        if staging.exists():
            shutil.rmtree(staging)
        raise RuntimeError("runtime setup failed; no incomplete environment was retained")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail unless the current locked runtime is ready")
    parser.add_argument("--remove", action="store_true", help="Remove the complete local runtime after SSH identities are revoked")
    args = parser.parse_args()
    try:
        if sys.version_info < (3, 11):
            raise RuntimeError("Subtitle Hub requires a base Python 3.11 or newer")
        if args.check and args.remove:
            raise RuntimeError("--check and --remove cannot be combined")
        if args.remove:
            identities = STATE_ROOT / "ssh"
            if identities.exists() and any(identities.iterdir()):
                raise RuntimeError("revoke registered SSH identities with remote_media.py revoke before removing the runtime")
            if RUNTIME_ROOT.exists():
                shutil.rmtree(RUNTIME_ROOT)
            print(json.dumps({"schema_version": 1, "runtime_root": str(RUNTIME_ROOT.resolve()), "removed": True}, indent=2))
            return 0
        if args.check:
            if not valid_runtime():
                raise RuntimeError("Subtitle Hub runtime is missing or outdated; run setup_runtime.py")
        else:
            create_runtime()
    except (OSError, subprocess.CalledProcessError, RuntimeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(json.dumps({
        "schema_version": 1,
        "runtime_root": str(RUNTIME_ROOT.resolve()),
        "python": str(runtime_python().resolve()),
        "state_root": str(STATE_ROOT.resolve()),
        "ready": True,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

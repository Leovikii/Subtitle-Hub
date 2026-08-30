#!/usr/bin/env python3
"""Run bounded read-only media checks on a Debian host through system OpenSSH."""

from __future__ import annotations

import argparse
import json
import math
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path, PurePosixPath
from urllib.parse import quote

HOST_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9.-]{0,251}[A-Za-z0-9])?")
USER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]{0,63}")
MARKER = "__SUBTITLE_HUB_MEDIA_{}__"
MAX_OUTPUT = {"frame": 12 * 1024 * 1024, "audio": 16 * 1024 * 1024, "subtitle": 24 * 1024 * 1024}


class RemoteMediaError(RuntimeError):
    pass


def remote_path(raw: str) -> str:
    if any(ord(char) < 32 for char in raw) or not raw.startswith("/"):
        raise RemoteMediaError("remote media paths must be absolute POSIX paths without control characters")
    path = PurePosixPath(raw)
    if ".." in path.parts or path.name in {"", ".", ".."}:
        raise RemoteMediaError(f"unsafe remote media path: {raw!r}")
    return str(path)


def ssh_uri(host: str, port: int, user: str, path: str) -> str:
    return f"ssh://{quote(user, safe='')}@{host}:{port}{quote(path, safe='/')}"


def guarded(path: str, body: str) -> str:
    quoted = shlex.quote(path)
    return (
        f"file=$(realpath -- {quoted}); "
        f"test \"$file\" = {quoted} || {{ printf 'remote path resolves outside the approved file\\n' >&2; exit 64; }}; "
        f"test -r \"$file\" || {{ printf 'remote media is not readable\\n' >&2; exit 66; }}; "
        f"{body}"
    )


def ssh_command(args: argparse.Namespace, remote: str) -> list[str]:
    host_key_mode = "ask" if args.action == "probe" else "yes"
    return [
        args.ssh,
        "-T",
        "-p", str(args.port),
        "-o", "BatchMode=no",
        "-o", "ClearAllForwardings=yes",
        "-o", "PermitLocalCommand=no",
        "-o", "PreferredAuthentications=password,keyboard-interactive",
        "-o", "PubkeyAuthentication=no",
        "-o", "NumberOfPasswordPrompts=1",
        "-o", f"StrictHostKeyChecking={host_key_mode}",
        "-o", f"ConnectTimeout={args.connect_timeout}",
        f"{args.user}@{args.host}",
        remote,
    ]


def run_ssh(args: argparse.Namespace, remote: str, *, limit: int) -> bytes:
    try:
        result = subprocess.run(
            ssh_command(args, remote), stdin=None, stdout=subprocess.PIPE, stderr=None,
            timeout=args.client_timeout, check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise RemoteMediaError(f"SSH command failed or timed out: {error}") from error
    if result.returncode != 0:
        raise RemoteMediaError(f"SSH command exited {result.returncode}")
    if len(result.stdout) > limit:
        raise RemoteMediaError(f"remote output exceeds the {limit}-byte limit")
    return result.stdout


def probe(args: argparse.Namespace) -> dict[str, object]:
    paths = [remote_path(value) for value in args.path]
    if len(paths) != len(set(paths)):
        raise RemoteMediaError("duplicate remote media path")
    blocks = []
    for index, path in enumerate(paths, start=1):
        body = (
            f"printf '{MARKER.format(index)}\\n'; "
            "stat -c '%s' -- \"$file\"; "
            "head -c 1048576 -- \"$file\" | sha256sum | cut -d ' ' -f 1; "
            "timeout 45s ffprobe -v error -show_entries "
            "'format=duration,format_name:stream=index,codec_type,codec_name,width,height:stream_tags=language,title:stream_disposition=default,forced' "
            "-of json=compact=1 \"$file\""
        )
        blocks.append(guarded(path, body))
    checks = (
        "test -r /etc/debian_version || { printf 'remote host is not Debian\\n' >&2; exit 69; }; "
        "for tool in ffprobe ffmpeg timeout realpath stat head sha256sum cut; do "
        "command -v \"$tool\" >/dev/null || { printf 'missing remote tool: %s\\n' \"$tool\" >&2; exit 69; }; done; "
    )
    raw = run_ssh(args, "set -eu; " + checks + "; ".join(blocks), limit=max(2 * 1024 * 1024, len(paths) * 512 * 1024))
    text = raw.decode("utf-8", errors="strict")
    media = []
    for index, path in enumerate(paths, start=1):
        marker = MARKER.format(index)
        start = text.find(marker + "\n")
        if start < 0:
            raise RemoteMediaError(f"probe output lacks marker for {path}")
        start += len(marker) + 1
        next_marker = text.find(MARKER.format(index + 1) + "\n", start) if index < len(paths) else len(text)
        chunk = text[start:next_marker].strip().splitlines()
        if len(chunk) < 3 or not chunk[0].isdigit() or not re.fullmatch(r"[0-9a-f]{64}", chunk[1]):
            raise RemoteMediaError(f"malformed probe envelope for {path}")
        try:
            payload = json.loads("\n".join(chunk[2:]))
        except json.JSONDecodeError as error:
            raise RemoteMediaError(f"invalid ffprobe JSON for {path}: {error}") from error
        media.append({
            "access": "ssh",
            "path": ssh_uri(args.host, args.port, args.user, path),
            "remote_path": path,
            "basename": PurePosixPath(path).name,
            "size": int(chunk[0]),
            "sha256_first_mib": chunk[1],
            "probe": payload,
        })
    return {"schema_version": 1, "action": "probe", "connection": {"host": args.host, "port": args.port, "user": args.user}, "media": media}


def local_output(raw: str, suffix: str) -> Path:
    output = Path(raw).expanduser().resolve()
    temp_root = Path(tempfile.gettempdir()).resolve()
    try:
        output.relative_to(temp_root)
    except ValueError as error:
        raise RemoteMediaError(f"output must stay under the system temporary directory {temp_root}") from error
    if output.suffix.lower() != suffix:
        raise RemoteMediaError(f"output must use {suffix}")
    output.parent.mkdir(parents=True, exist_ok=True)
    return output


def write_remote_output(args: argparse.Namespace, action: str, body: str, suffix: str) -> dict[str, object]:
    path = remote_path(args.path)
    output = local_output(args.output, suffix)
    data = run_ssh(args, guarded(path, body), limit=MAX_OUTPUT[action])
    if not data:
        raise RemoteMediaError(f"remote {action} returned no data")
    part = output.with_name(output.name + ".part")
    try:
        part.write_bytes(data)
        part.replace(output)
    finally:
        if part.exists():
            part.unlink()
    return {"schema_version": 1, "action": action, "source": ssh_uri(args.host, args.port, args.user, path), "output": str(output), "bytes": len(data)}


def validate_connection(args: argparse.Namespace) -> None:
    if not HOST_RE.fullmatch(args.host) or not USER_RE.fullmatch(args.user):
        raise RemoteMediaError("unsafe SSH host or user")
    if not 1 <= args.port <= 65535:
        raise RemoteMediaError("SSH port must be between 1 and 65535")
    if not 1 <= args.connect_timeout <= 60 or not 5 <= args.client_timeout <= 300:
        raise RemoteMediaError("SSH timeouts are outside the allowed bounds")
    if not Path(args.ssh).name.lower() in {"ssh", "ssh.exe"}:
        raise RemoteMediaError("--ssh must name the system OpenSSH client")


def add_connection(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=22)
    parser.add_argument("--user", required=True)
    parser.add_argument("--ssh", default="ssh", help="System OpenSSH client")
    parser.add_argument("--connect-timeout", type=int, default=10)
    parser.add_argument("--client-timeout", type=int, default=75)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    probe_parser = subparsers.add_parser("probe")
    add_connection(probe_parser)
    probe_parser.add_argument("--path", action="append", required=True, help="Exact absolute remote video path; repeat for multiple files")
    probe_parser.add_argument("--output", help="Optional system-temporary JSON manifest path")
    frame_parser = subparsers.add_parser("frame")
    add_connection(frame_parser)
    frame_parser.add_argument("--path", required=True)
    frame_parser.add_argument("--time", required=True, type=float)
    frame_parser.add_argument("--output", required=True)
    audio_parser = subparsers.add_parser("audio")
    add_connection(audio_parser)
    audio_parser.add_argument("--path", required=True)
    audio_parser.add_argument("--start", required=True, type=float)
    audio_parser.add_argument("--duration", required=True, type=float)
    audio_parser.add_argument("--output", required=True)
    subtitle_parser = subparsers.add_parser("subtitle")
    add_connection(subtitle_parser)
    subtitle_parser.add_argument("--path", required=True)
    subtitle_parser.add_argument("--stream", required=True, type=int)
    subtitle_parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        validate_connection(args)
        if args.action == "probe":
            result = probe(args)
        elif args.action == "frame":
            if not math.isfinite(args.time) or args.time < 0:
                raise RemoteMediaError("frame time must be nonnegative")
            body = f"exec timeout 45s ffmpeg -nostdin -v error -ss {args.time:.3f} -i \"$file\" -threads 1 -frames:v 1 -f image2pipe -vcodec mjpeg pipe:1"
            result = write_remote_output(args, "frame", body, ".jpg")
        elif args.action == "audio":
            if not math.isfinite(args.start) or not math.isfinite(args.duration) or args.start < 0 or not 0 < args.duration <= 30:
                raise RemoteMediaError("audio start must be nonnegative and duration must be within 0-30 seconds")
            body = f"exec timeout 45s ffmpeg -nostdin -v error -ss {args.start:.3f} -t {args.duration:.3f} -i \"$file\" -threads 1 -vn -ac 1 -ar 16000 -f wav pipe:1"
            result = write_remote_output(args, "audio", body, ".wav")
        else:
            if args.stream < 0:
                raise RemoteMediaError("subtitle stream index must be nonnegative")
            body = f"exec timeout 45s ffmpeg -nostdin -v error -i \"$file\" -threads 1 -map 0:{args.stream} -f ass pipe:1"
            result = write_remote_output(args, "subtitle", body, ".ass")
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.action == "probe" and args.output:
            local_output(args.output, ".json").write_text(rendered, encoding="utf-8")
    except (OSError, UnicodeError, ValueError, RemoteMediaError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

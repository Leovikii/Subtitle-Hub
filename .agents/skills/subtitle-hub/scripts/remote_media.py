#!/usr/bin/env python3
"""Run bounded read-only media checks on a Debian host through Paramiko."""

from __future__ import annotations

import argparse
import base64
import hashlib
import html
import importlib
import json
import math
import re
import secrets
import shlex
import socket
import sys
import tempfile
import time
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path, PurePosixPath
from urllib.parse import quote

PARAMIKO_VERSION = "5.0.0"
HOST_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9.-]{0,251}[A-Za-z0-9])?")
USER_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]{0,63}")
MARKER = "__SUBTITLE_HUB_MEDIA_{}__"
MAX_OUTPUT = {"frame": 12 * 1024 * 1024, "audio": 16 * 1024 * 1024, "subtitle": 24 * 1024 * 1024}
VIDEO_SUFFIXES = {".mkv", ".mp4", ".m2ts", ".ts", ".webm", ".mov"}


class RemoteMediaError(RuntimeError):
    pass


def dependency_root() -> Path:
    return (Path.home() / ".codex" / "dependencies" / "subtitle-hub" / f"paramiko-{PARAMIKO_VERSION}").resolve()


def load_paramiko():
    root = dependency_root()
    sys.path.insert(0, str(root))
    try:
        module = importlib.import_module("paramiko")
    except ModuleNotFoundError as error:
        command = f'{sys.executable} -m pip install --target "{root}" "paramiko=={PARAMIKO_VERSION}"'
        raise RemoteMediaError(f"missing Paramiko {PARAMIKO_VERSION}; install the isolated dependency with: {command}") from error
    module_file = Path(module.__file__).resolve()
    if root not in module_file.parents:
        raise RemoteMediaError(f"Paramiko must load from the isolated dependency directory {root}")
    if getattr(module, "__version__", None) != PARAMIKO_VERSION:
        raise RemoteMediaError(f"Paramiko {PARAMIKO_VERSION} is required, found {getattr(module, '__version__', 'unknown')}")
    return module


def remote_path(raw: str) -> str:
    if any(ord(char) < 32 for char in raw) or not raw.startswith("/"):
        raise RemoteMediaError("remote paths must be absolute POSIX paths without control characters")
    path = PurePosixPath(raw)
    if ".." in path.parts or path.name in {"", ".", ".."}:
        raise RemoteMediaError(f"unsafe remote path: {raw!r}")
    return str(path)


def ssh_uri(host: str, port: int, user: str, path: str) -> str:
    return f"ssh://{quote(user, safe='')}@{host}:{port}{quote(path, safe='/')}"


def host_key_file(args: argparse.Namespace) -> Path:
    override = getattr(args, "host_key_file", None)
    if override:
        return Path(override).expanduser().resolve()
    return (dependency_root().parent / "hosts" / f"{args.host}-{args.port}.json").resolve()


def fingerprint(key: object) -> str:
    digest = hashlib.sha256(key.asbytes()).digest()
    return "SHA256:" + base64.b64encode(digest).decode("ascii").rstrip("=")


def capture_host_key(args: argparse.Namespace, paramiko: object):
    transport = None
    try:
        connection = socket.create_connection((args.host, args.port), timeout=args.connect_timeout)
        transport = paramiko.Transport(connection)
        transport.start_client(timeout=args.client_timeout)
        key = transport.get_remote_server_key()
    except (OSError, paramiko.SSHException) as error:
        raise RemoteMediaError("could not complete the SSH host-key handshake") from error
    finally:
        if transport is not None:
            transport.close()
    if key.get_name() != "ssh-ed25519":
        raise RemoteMediaError(f"NAS host key must be ED25519, found {key.get_name()}")
    return key


def bootstrap(args: argparse.Namespace, paramiko: object) -> dict[str, object]:
    key = capture_host_key(args, paramiko)
    actual = fingerprint(key)
    trusted = False
    target = host_key_file(args)
    if args.accept_fingerprint:
        if args.accept_fingerprint != actual:
            raise RemoteMediaError("retrieved NAS host key does not match the approved fingerprint")
        target.parent.mkdir(parents=True, exist_ok=True)
        record = {"schema_version": 1, "host": args.host, "port": args.port, "key_type": key.get_name(), "key_base64": key.get_base64(), "fingerprint": actual}
        part = target.with_name(target.name + ".part")
        try:
            part.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            part.replace(target)
        finally:
            if part.exists():
                part.unlink()
        trusted = True
    return {"schema_version": 1, "action": "bootstrap", "connection": {"host": args.host, "port": args.port, "user": args.user}, "host_key_file": str(target), "host_fingerprint": actual, "trusted": trusted}


def load_pinned_key(args: argparse.Namespace, paramiko: object):
    path = host_key_file(args)
    if not path.is_file():
        raise RemoteMediaError("SSH host key is not trusted; run bootstrap first")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("host") != args.host or data.get("port") != args.port or data.get("key_type") != "ssh-ed25519":
        raise RemoteMediaError("pinned SSH host-key record does not match this connection")
    try:
        key = paramiko.Ed25519Key(data=base64.b64decode(str(data.get("key_base64", "")), validate=True))
    except (ValueError, TypeError, paramiko.SSHException) as error:
        raise RemoteMediaError("pinned SSH host-key record is corrupt") from error
    if fingerprint(key) != data.get("fingerprint"):
        raise RemoteMediaError("pinned SSH host-key record is corrupt")
    return key


def browser_password(prompt: str, timeout: int) -> str:
    token = secrets.token_urlsafe(32)
    state: dict[str, str] = {}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, _format: str, *_args: object) -> None:
            return

        def secure_headers(self) -> None:
            self.send_header("Content-Security-Policy", "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Cache-Control", "no-store")

        def do_GET(self) -> None:
            if self.path != f"/{token}":
                self.send_error(404)
                return
            body = ("<!doctype html><meta charset=utf-8><title>Subtitle Hub SSH</title>"
                    "<style>body{font:16px sans-serif;max-width:36rem;margin:4rem auto}input,button{font:inherit;padding:.6rem;width:100%;box-sizing:border-box;margin:.5rem 0}</style>"
                    f"<h1>Subtitle Hub SSH</h1><p>{html.escape(prompt)}</p>"
                    f"<form method=post action='/{token}'><input type=password name=password autofocus required autocomplete=current-password><button>连接</button></form>").encode("utf-8")
            self.send_response(200)
            self.secure_headers()
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self) -> None:
            if self.path != f"/{token}":
                self.send_error(404)
                return
            length = int(self.headers.get("Content-Length", "0"))
            if not 1 <= length <= 4096:
                self.send_error(400)
                return
            password = urllib.parse.parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True).get("password", [""])[0]
            if not password:
                self.send_error(400)
                return
            state["password"] = password
            body = "凭据已提交，可以关闭此页面。".encode("utf-8")
            self.send_response(200)
            self.secure_headers()
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = HTTPServer(("127.0.0.1", 0), Handler)
    server.timeout = 1
    url = f"http://127.0.0.1:{server.server_port}/{token}"
    if not webbrowser.open(url, new=1):
        server.server_close()
        raise RemoteMediaError(f"could not open the local credential page: {url}")
    deadline = time.monotonic() + timeout
    try:
        while "password" not in state and time.monotonic() < deadline:
            server.handle_request()
    finally:
        server.server_close()
    if "password" not in state:
        raise RemoteMediaError("SSH password prompt timed out")
    return state.pop("password")


def prompt_password(args: argparse.Namespace) -> str:
    prompt = f"请输入 {args.user}@{args.host}:{args.port} 的 SSH 密码。密码只保留在本次连接内存中。"
    try:
        import tkinter as tk
        from tkinter import simpledialog
    except ImportError:
        return browser_password(prompt, args.client_timeout)
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        try:
            password = simpledialog.askstring("Subtitle Hub SSH", prompt, show="*", parent=root)
        finally:
            root.destroy()
        if password:
            return password
        raise RemoteMediaError("SSH password entry was cancelled")
    except tk.TclError:
        return browser_password(prompt, args.client_timeout)


class PinnedHostPolicy:
    def __init__(self, expected: object):
        self.expected = expected

    def missing_host_key(self, _client: object, _hostname: str, key: object) -> None:
        if key.get_name() != self.expected.get_name() or key.asbytes() != self.expected.asbytes():
            raise RemoteMediaError("NAS host key changed or does not match the approved key")


def open_client(args: argparse.Namespace, paramiko: object, password: str):
    expected = load_pinned_key(args, paramiko)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(PinnedHostPolicy(expected))
    try:
        client.connect(hostname=args.host, port=args.port, username=args.user, password=password,
                       look_for_keys=False, allow_agent=False, timeout=args.connect_timeout,
                       banner_timeout=args.connect_timeout, auth_timeout=args.connect_timeout,
                       channel_timeout=args.client_timeout)
    except paramiko.AuthenticationException as error:
        client.close()
        raise RemoteMediaError("SSH authentication failed") from error
    except (OSError, paramiko.SSHException) as error:
        client.close()
        raise RemoteMediaError("SSH connection failed") from error
    return client


def run_remote(client: object, remote: str, *, limit: int, timeout: int) -> bytes:
    _stdin, stdout, stderr = client.exec_command(remote, timeout=timeout)
    channel = stdout.channel
    data = bytearray()
    diagnostics = bytearray()
    deadline = time.monotonic() + timeout
    while True:
        while channel.recv_ready():
            data.extend(channel.recv(min(65536, limit + 1 - min(len(data), limit + 1))))
            if len(data) > limit:
                channel.close()
                raise RemoteMediaError(f"remote output exceeds the {limit}-byte limit")
        while channel.recv_stderr_ready():
            chunk = channel.recv_stderr(8192)
            if len(diagnostics) < 8192:
                diagnostics.extend(chunk[:8192 - len(diagnostics)])
        if channel.exit_status_ready() and not channel.recv_ready() and not channel.recv_stderr_ready():
            break
        if time.monotonic() >= deadline:
            channel.close()
            raise RemoteMediaError("remote command timed out")
        time.sleep(0.01)
    status = channel.recv_exit_status()
    detail = diagnostics.decode("utf-8", errors="replace").strip()
    if status != 0:
        raise RemoteMediaError(f"remote command exited {status}: {detail or 'no diagnostic'}")
    return bytes(data)


def guarded(path: str, body: str) -> str:
    quoted = shlex.quote(path)
    return (f"file=$(realpath -- {quoted}); "
            f"test \"$file\" = {quoted} || {{ printf 'remote path resolves outside the approved file\\n' >&2; exit 64; }}; "
            f"test -r \"$file\" || {{ printf 'remote media is not readable\\n' >&2; exit 66; }}; {body}")


def probe(args: argparse.Namespace, client: object) -> dict[str, object]:
    paths = [remote_path(value) for value in args.path]
    if len(paths) != len(set(paths)):
        raise RemoteMediaError("duplicate remote media path")
    blocks = []
    for index, path in enumerate(paths, start=1):
        body = (f"printf '{MARKER.format(index)}\\n'; stat -c '%s' -- \"$file\"; "
                "head -c 1048576 -- \"$file\" | sha256sum | cut -d ' ' -f 1; "
                "timeout 45s ffprobe -v error -show_entries "
                "'format=duration,format_name:stream=index,codec_type,codec_name,width,height:stream_tags=language,title:stream_disposition=default,forced' "
                "-of json=compact=1 \"$file\"")
        blocks.append(guarded(path, body))
    checks = ("test -r /etc/debian_version || { printf 'remote host is not Debian\\n' >&2; exit 69; }; "
              "for tool in ffprobe ffmpeg timeout realpath stat head sha256sum cut; do command -v \"$tool\" >/dev/null || { printf 'missing remote tool: %s\\n' \"$tool\" >&2; exit 69; }; done; ")
    raw = run_remote(client, "set -eu; " + checks + "; ".join(blocks), limit=max(2 * 1024 * 1024, len(paths) * 512 * 1024), timeout=args.client_timeout)
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
        media.append({"access": "ssh", "path": ssh_uri(args.host, args.port, args.user, path), "remote_path": path,
                      "basename": PurePosixPath(path).name, "size": int(chunk[0]), "sha256_first_mib": chunk[1],
                      "probe": json.loads("\n".join(chunk[2:]))})
    return {"schema_version": 1, "action": "probe", "connection": {"host": args.host, "port": args.port, "user": args.user}, "media": media}


def discover(args: argparse.Namespace, client: object) -> dict[str, object]:
    directory = remote_path(args.directory.rstrip("/"))
    quoted = shlex.quote(directory)
    command = ("command -v find >/dev/null || { printf 'missing remote tool: find\\n' >&2; exit 69; }; "
               f"dir=$(realpath -- {quoted}); test \"$dir\" = {quoted} || {{ printf 'remote directory resolves outside the approved path\\n' >&2; exit 64; }}; "
               "test -d \"$dir\" -a -r \"$dir\" -a -x \"$dir\" || { printf 'remote directory is not readable\\n' >&2; exit 66; }; find \"$dir\" -maxdepth 1 -type f -print0")
    raw = run_remote(client, command, limit=4 * 1024 * 1024, timeout=args.client_timeout)
    paths = sorted(path for item in raw.split(b"\0") if item for path in [remote_path(item.decode("utf-8", errors="strict"))] if PurePosixPath(path).suffix.lower() in VIDEO_SUFFIXES)
    return {"schema_version": 1, "action": "discover", "connection": {"host": args.host, "port": args.port, "user": args.user},
            "directory": directory, "media": [{"path": ssh_uri(args.host, args.port, args.user, path), "remote_path": path, "basename": PurePosixPath(path).name} for path in paths]}


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


def write_remote_output(args: argparse.Namespace, client: object, action: str, body: str, suffix: str) -> dict[str, object]:
    path = remote_path(args.path)
    output = local_output(args.output, suffix)
    data = run_remote(client, guarded(path, body), limit=MAX_OUTPUT[action], timeout=args.client_timeout)
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


def add_connection(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=22)
    parser.add_argument("--user", required=True)
    parser.add_argument("--host-key-file")
    parser.add_argument("--connect-timeout", type=int, default=10)
    parser.add_argument("--client-timeout", type=int, default=120)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    bootstrap_parser = subparsers.add_parser("bootstrap"); add_connection(bootstrap_parser); bootstrap_parser.add_argument("--accept-fingerprint")
    discover_parser = subparsers.add_parser("discover"); add_connection(discover_parser); discover_parser.add_argument("--directory", required=True)
    probe_parser = subparsers.add_parser("probe"); add_connection(probe_parser); probe_parser.add_argument("--path", action="append", required=True); probe_parser.add_argument("--output")
    frame_parser = subparsers.add_parser("frame"); add_connection(frame_parser); frame_parser.add_argument("--path", required=True); frame_parser.add_argument("--time", required=True, type=float); frame_parser.add_argument("--output", required=True)
    audio_parser = subparsers.add_parser("audio"); add_connection(audio_parser); audio_parser.add_argument("--path", required=True); audio_parser.add_argument("--start", required=True, type=float); audio_parser.add_argument("--duration", required=True, type=float); audio_parser.add_argument("--output", required=True)
    subtitle_parser = subparsers.add_parser("subtitle"); add_connection(subtitle_parser); subtitle_parser.add_argument("--path", required=True); subtitle_parser.add_argument("--stream", required=True, type=int); subtitle_parser.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        validate_connection(args)
        paramiko = load_paramiko()
        if args.action == "bootstrap":
            result = bootstrap(args, paramiko)
        else:
            password = prompt_password(args)
            try:
                client = open_client(args, paramiko, password)
            finally:
                password = ""
            try:
                if args.action == "discover":
                    result = discover(args, client)
                elif args.action == "probe":
                    result = probe(args, client)
                elif args.action == "frame":
                    if not math.isfinite(args.time) or args.time < 0:
                        raise RemoteMediaError("frame time must be nonnegative")
                    result = write_remote_output(args, client, "frame", f"exec timeout 45s ffmpeg -nostdin -v error -ss {args.time:.3f} -i \"$file\" -threads 1 -frames:v 1 -f image2pipe -vcodec mjpeg pipe:1", ".jpg")
                elif args.action == "audio":
                    if not math.isfinite(args.start) or not math.isfinite(args.duration) or args.start < 0 or not 0 < args.duration <= 30:
                        raise RemoteMediaError("audio start must be nonnegative and duration must be within 0-30 seconds")
                    result = write_remote_output(args, client, "audio", f"exec timeout 45s ffmpeg -nostdin -v error -ss {args.start:.3f} -t {args.duration:.3f} -i \"$file\" -threads 1 -vn -ac 1 -ar 16000 -f wav pipe:1", ".wav")
                else:
                    if args.stream < 0:
                        raise RemoteMediaError("subtitle stream index must be nonnegative")
                    result = write_remote_output(args, client, "subtitle", f"exec timeout 45s ffmpeg -nostdin -v error -i \"$file\" -threads 1 -map 0:{args.stream} -f ass pipe:1", ".ass")
            finally:
                client.close()
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if args.action == "probe" and args.output:
            local_output(args.output, ".json").write_text(rendered, encoding="utf-8")
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, RemoteMediaError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# Project initialization and material intake

## Identity gate

### SH-ID-002 — Bangumi is the identity source

Search only to discover candidate IDs. Fetch `https://api.bgm.tv/v0/subjects/<id>` and verify `id`, `name`, `name_cn`, media/platform, date, and episode count against the requested scope. Save API `name` as `identity.titles.ja` and `name_cn` as `identity.titles.zh-Hans` without inferring either from filenames or other-language releases.

Pause before creating a formal project if `name_cn` is empty, the API is inaccessible, or plausible candidates differ by season, movie, OVA, compilation, special, remake, or scope. Present the candidate ID/title/scope evidence and ask the user. A user-confirmed draft does not satisfy the release-time `api-verified` requirement.

The distribution package is `bgm<subject-id> - <name_cn> [v<version>].zip`; release details are in `release-and-workspace.md`.

## Minimum required inputs

### SH-INIT-002 — Formal proofreading project minimum

Require:

1. A Chinese subtitle baseline to proofread, in a reliably parseable format and covering the declared work scope.
2. A per-episode baseline map and task declaration: source language, target language, primary/secondary release languages, work scope, timing authority, and confirmation that this is proofreading rather than translation from scratch.

Target video is optional. When supplied as a readable local path or as user-declared SSH-hosted media, probe it and record exact basenames, duration/track summaries, and mappings without copying it into the repository. Without video, timing and visual playback remain limited, but matching source-language subtitles/scripts still permit full B-tier translation review. Missing Chinese baseline means this is not a proofreading initialization; changing to original translation needs explicit scope.

## Text evidence tiers

### SH-EVIDENCE-001 — Tier evidence, never sample coverage

| Tier | Available text | Required review | Limitation |
| --- | --- | --- | --- |
| A | Chinese baseline + matching source text/script + auxiliary translation | Full Chinese-to-source and source-to-Chinese coverage; use auxiliary translation only to resolve ambiguity | Media truth is not implied |
| B | Chinese baseline + matching source text/script | Full bidirectional coverage for mistranslation, omission, addition, terminology, register, grammar, and continuity | Unclear source text may require human or point media evidence |
| C | Chinese baseline + auxiliary translation but no source text | Full Chinese quality and internal-consistency review; auxiliary text may raise candidates but cannot prove source fidelity | Human full-source-meaning review is required before claiming fidelity |
| D | Chinese baseline only | Full Chinese quality, structure, timing-code, and static-layout review | Human full-source-meaning review is required before release fidelity approval |

Video availability does not raise this text tier. Every visible Chinese event remains in scope at every tier; never use sampling as completion evidence.

## Optional evidence and capabilities

### SH-INIT-003 — Optional sources are functional, not ceremonial

| Input | Capability unlocked | Boundary when present or absent |
| --- | --- | --- |
| Source-language subtitle or script | Searchable source text; stronger checks for mishearing, names, numbers, omissions, register, and terminology | Match it to the target cut before using timing; without it, audio-first language review may continue but low-clarity/full-text coverage is limited |
| Target-video embedded subtitle | Same-release time boundaries, splits, speaker/sign candidates, layout/effect evidence | It may be early, short, incomplete, mistranslated, or illegally overlapping; absence does not block audio/video timing review |
| Embedded source-language subtitle | Both source-text and timing evidence | Validate those roles separately; one file does not become two independent witnesses |
| Embedded non-source-language subtitle | Timing plus translation/disambiguation evidence | Never promote it to source-text authority; if Chinese, it remains auxiliary unless the user declares it the baseline |
| SUP/PGS and OCR | Original graphic text, signs, forced subtitles, and cross-checking | OCR is candidate text until checked against the image/audio |
| Another translation or Chinese version | Ambiguity, omissions, relationship, and terminology comparison | Never use majority vote or treat it as source-language evidence |
| Official glossary / series terms / user-confirmed names | Stable terminology | Scope it; deviations from confirmed series terms require user confirmation |
| Alternate release video/subtitle | Cut-difference and compatibility investigation | Similar names or durations do not prove compatibility |
| Fonts, renderer, media probe | Visual geometry, track inventory, and local rendering | Environment capability, not source material; rendering success is not human visual approval |

Derived waveforms, frames, media summaries, and track listings are disposable. Prefer system temporary storage; keep only a small supplemental handoff note under on-demand `project/workspace/temp/notes/` when another run genuinely needs it.

## Evidence roles

### SH-SRC-002 — Assign roles explicitly

Each `subtitle_sources` entry uses a `roles` list drawn from:

- `candidate-baseline`
- `source-text-reference`
- `timing-reference`
- `translation-reference`
- `forced-signs-reference`
- `style-layout-reference`
- `secondary-language-release-source`

Record actual language separately from roles. The Chinese baseline starts only as `candidate-baseline`; assign timing or style authority only when the user confirms it. Track language classification uses standard tags/titles, the known source language, then sampled text if needed. If a selected track remains ambiguous, pause and ask. An explicitly ignored optional track is nonblocking. Write confirmed language, roles, scope, and evidence into `project.yaml`.

## Initialization gate

### SH-INIT-004 — Persist facts, not parallel status models

Initialization is ready when the baseline parses, the episode map and selected source roles are confirmed, `blocking_questions` is empty, and `--ready-for-proofreading` passes. Persist only the A–D evidence tier, timing authority, material limitations, and one project/review status; do not maintain separate structure/language/timing/visual/release readiness states.

Video plus a Chinese baseline permits Chinese, structure, timing, and local visual work when tools permit; it does not prove source-text fidelity or full listening/viewing. Missing capabilities are limitations, not invented completion states.

## Initialization sequence

### SH-INIT-005 — Safe creation order

1. Run identity discovery/check without creating the work directory.
2. Inventory the Chinese baseline and optional text/media in one system-temp JSON. Probe tracks only when video is supplied; classify only materials intended for use.
3. Present identity/scope, episode map, material roles, release languages, and proposed short name as one user decision.
4. After approval, run `scripts/init_project.py --dry-run` as an internal safety check, then run the identical command without `--dry-run`. Ask again only if the manifest materially differs from the approved plan.
5. Copy subtitle inputs into immutable `project/sources/`; record videos by basename and media facts, not by copying them.
6. Create `project.yaml`, root `review.md`, copied sources, and Noto episode masters only. Create ignored `project/local.paths.yaml` only when local or password-free SSH media references must survive the run. Create other paths with their first file and a series guide only with its first real term.
7. Run `scripts/validate_project.py`; do not begin content work until structural errors are resolved.

Initialization never modifies the user's original media or subtitle files.

## Skill 1.4.1 intake contract

### SH-INIT-012 — Shared runtime gate

Before any repository script or project initialization, locate a usable Python 3 from the Codex workspace dependencies first, then ordinary `python`, `python3`, or the Windows `py` launcher. Run `scripts/setup_runtime.py --check`. If it reports a missing or outdated environment, request approval for the dependency download and run the same script without `--check`. It creates or atomically replaces one environment at `~/.codex/subtitle-hub/venv`, keeps non-package state under the sibling `state/`, and returns the interpreter path. Run all subsequent Skill scripts with that interpreter.

The exact packages are locked in `requirements.txt`, including Paramiko and PyYAML. Never install them globally, create a project-local virtual environment, copy dependencies into a project, or maintain an alternate package path. A requirements change invalidates and rebuilds only the shared `venv`; it preserves `state`. For complete cleanup, run `remote_media.py revoke` for every registered host before base Python runs `setup_runtime.py --remove`; the remover refuses to orphan registered keys. If no compatible base Python can execute `setup_runtime.py`, stop and report the missing prerequisite rather than partially initializing a project or attempting an operating-system Python installation.

### SH-INIT-006 — Probe before asking for manual inventory

Start from the user-provided target video path(s) and Chinese baseline rather than asking the user to enumerate container tracks. Run `scripts/inventory_sources.py`; it uses `ffprobe` to record container format, duration, resolution, audio/subtitle stream index, codec, language tag/title, default/forced disposition, and a suggested source-language audio stream. It also inventories external subtitle/script files, hashes them, assigns candidate roles, and proposes episode relationships.

Container language tags may use valid BCP 47 forms. Filenames/titles are weaker signals and may use only known aliases; never interpret an arbitrary short filename token as a language. If multiple source-language audio streams exist, select one with `--audio-stream VIDEO|INDEX`. Resolve a selected track with `--track-language VIDEO|INDEX|LANGUAGE`. Unknown embedded-subtitle language blocks only when that track is selected for source, timing, translation, layout, or release use.

The disposable intake JSON uses `schema_version: 4` and `skill_version: 1.4.1`. It may contain local absolute paths or password-free SSH locators. Relevant fields are the evidence tier, videos, external sources, embedded tracks, `episode_map`, limitations, and blocking questions. Resolve the chosen mapping, target basenames, audio, timing authority, source roles, and ignored optional tracks in this same file; do not create a second mapping file. Do not initialize while a selected material question remains blocking.

### SH-INIT-011 — Guided SSH video intake

When the user declares that a project reads video from a Debian NAS over SSH, collect the host, port, username, exact absolute video paths or one containing directory, Chinese baseline mapping, intended source audio, and timing authority. For a directory, `remote_media.py discover` lists only top-level files with supported video suffixes; never recurse or search outside that approved directory. Never request or accept the password in chat, arguments, files, URLs, or project records.

`remote_media.py` has one cross-platform backend: Paramiko 5.0.0 in the shared Skill environment. It does not use or configure system OpenSSH, AskPass, SSH agents, user keys, or general known-hosts files.

Run `remote_media.py bootstrap` first. Its unauthenticated Python handshake retrieves the ED25519 host key and computes the SHA-256 fingerprint. Ask the user once to verify that fingerprint against a trusted NAS surface, then rerun with `--accept-fingerprint <SHA256:...>` to pin it under the shared `state/` root. A changed or non-ED25519 key stops the connection.

After pinning, SSH initialization opens one local Tk password dialog; when Tk is unavailable, it opens a one-use tokenized form bound only to `127.0.0.1`. The same connection generates a dedicated local ED25519 identity under `state/`, uses `sudo` to create the account home/`.ssh` when absent, and appends exactly one tagged public-key line to `authorized_keys`. It then proves a fresh key-authenticated connection before succeeding. The password exists only in the initialization process and never enters chat, arguments, environment variables, files, project records, SSH agents, or key stores. Later `discover`, `probe`, `frame`, `audio`, and `subtitle` actions use only that identity and never prompt for a password.

This one home/SSH-key enrollment is the only permitted remote setup. Do not install packages, change `sshd`, upload tools or media, or create remote work/cache directories. If enrollment or later key authentication fails, stop and report the exact limitation; never fall back to repeated password prompts. A probe must succeed from the Codex process itself before initialization may claim SSH capability.

Use only existing remote programs. One `probe` connection checks Debian and the required existing tools, probes all approved exact files, and writes the password-free result to a system-temporary JSON. It stops if a required tool is absent; never install, upgrade, configure, upload, or retry with a broader account:

```text
python scripts/remote_media.py probe --host <host> --port <port> --user <user> \
  --path </absolute/video-1.mkv> --path </absolute/video-2.mkv> \
  --output <system-temp/ssh-video-probe.json>
```

Pass that result to the ordinary intake command with `--ssh-video-probe <system-temp/ssh-video-probe.json>`. Present the proposed episode map, detected tracks/languages, chosen audio, timing authority, and password-free SSH video references in the same initialization confirmation as identity and project name. Initialization writes only those password-free locators to the existing ignored `project/local.paths.yaml`; durable `project.yaml` keeps basenames and media facts. Delete the probe JSON after its conclusions are folded into the project.

Unapproved or changed host keys, authentication failure, missing remote tools, unreadable or symlink-resolved paths, malformed probe output, or changed scope stop SSH intake. They never trigger credential persistence, remote environment setup, SFTP transfer, whole-file download, WebDAV fallback, or a second protocol implementation. The user may instead proceed text-only with the resulting media limitation.

### SH-INIT-010 — Upgrade before reopening an older project

Do not maintain old-schema execution branches and do not bulk-upgrade dormant projects. When an existing project is selected for new proofreading or release work, first compare it with the current `project.yaml` and `review.md` templates. Re-express confirmed durable facts in project schema 9 and current Skill version, fold current state and still-open decisions into review schema 3, and prepare complete Noto masters from the immutable sources or current release. Preserve source files and released subtitles unchanged; invalidate coverage fingerprints whenever a master changes. Resolve only genuinely missing or conflicting identity, scope, mapping, language, timing-authority, or naming facts with the user, then pass `validate_project.py --ready-for-proofreading` before content work. Git retains the old control history; do not create migration reports, compatibility sidecars, or per-version converters.

Example:

```text
python scripts/inventory_sources.py \
  --candidate-baseline <zh-subtitle-or-directory> \
  --optional-source <path>|<language>|<comma-separated-roles> \
  --source-language ja \
  --project-type tv \
  --output <temporary-intake.json>
```

### SH-INIT-007 — Approved episode map and IDs

Keep the approved map in intake JSON. Each entry contains `episode`, optional video ID/path, `target_basename`, Chinese baseline file ID/path, optional audio stream/language, and `timing_authority`.

Use stable internal episode IDs:

- TV/ONA: `S01E01` style; retain the actual season number when the project scope requires it.
- OVA: `OVA01`.
- Special: `SP01`.
- One film: `MOVIE`, with exactly one row.

Every entry refers to an inventoried Chinese baseline. Video/audio may be null; `target_basename` and `timing_authority` remain required. With video, recheck fingerprints and selected audio. Always check safe episode IDs and unique `<target-basename-stem>.zh-Hans.ass` names. Similar filenames or durations never prove a mapping. Delete intake after durable conclusions are written.

### SH-INIT-008 — Approve the developer-facing name before creation

The formal work directory is `<SHxxxx>--<project-name>`. Keep `project-name` short, lowercase, ASCII, and obvious to developers, for example `yamato-2199-tv`; it need not repeat the complete official title. Suggest one or more names from the verified identity/type, but ask the user to choose or approve one before running the initializer. Record the one initialization approver and date in `project.yaml`; never silently rename a work from a title guess.

The series directory is also a short developer-facing name. Reuse an established series directory when appropriate. Creating a new one requires an explicit series title and name approval; initialization rolls it back if the project transaction fails.

### SH-INIT-009 — Transactional initializer and master preparation

Run a dry run as the internal transaction check, then the identical command without `--dry-run`:

```text
python scripts/init_project.py \
  --repository-root <repository> \
  --series-dir <works/series-name> \
  --project-name <approved-short-name> \
  --approved-by <approver> \
  --type <tv|movie|ova|ona|special> \
  --bangumi-id <id> \
  --bangumi-snapshot <verified-api-json> \
  --intake <temporary-intake.json> \
  --dry-run
```

Omit `--work-id` to allocate the next repository ID. Use `--create-series --series-title ...` only for an approved new series directory. The initializer copies subtitle evidence into immutable `project/sources/`, never copies video, conditionally writes an ignored local or password-free SSH video map, and prepares one `master.ass` per episode. It fills required ASS fields and maps every retained style and nonempty inline font directly to Noto SC/JP while preserving all other rendered properties. SRT/VTT baselines produce the same Noto contract.

Initialization does not create a project README, `docs/`, or `subtitles/current/`. It promotes the staged work only if `scripts/validate_project.py --ready-for-proofreading` passes and rolls back a failed new-project/new-series transaction.

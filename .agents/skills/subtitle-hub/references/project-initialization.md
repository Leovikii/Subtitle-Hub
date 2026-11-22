# Project initialization and material intake

## Identity gate

### SH-ID-002 — Bangumi identity with a verified movie fallback

Search only to discover candidate IDs. Fetch `https://api.bgm.tv/v0/subjects/<id>` and verify `id`, `name`, `name_cn`, media/platform, date, and episode count against the requested scope. Save API `name` as `identity.titles.ja` and `name_cn` as `identity.titles.zh-Hans` without inferring either from filenames or other-language releases.

Resolve identity from available evidence while continuing read-only material inventory. If plausible matches still differ by season, format, or scope, present the verified candidates in the initialization decision and ask only for the choice the evidence cannot settle. An empty `name_cn` or inaccessible API blocks formal Bangumi initialization. Recover a transient lookup failure when possible and report a persistent verification gap if no allowed identity path remains. A user-confirmed draft does not satisfy the release-time `api-verified` requirement.

For a live-action movie with no plausible Bangumi match after Chinese/original-title and year discovery, verify its exact IMDb `tt` ID, original title, movie type, and release date on IMDb's title/release-info pages. This fallback is not a response to an API outage or a conflicting match. Include the provider, Chinese title, date basis, and single-movie scope in the same initialization confirmation; do not ask for a separate identity approval. Record `provider: imdb`, the canonical `https://www.imdb.com/title/<tt-id>/` URL, `api_url: null`, `titles.original`, the user-confirmed `titles.zh-Hans`, `total_episodes: 1`, `verification: web-verified`, `verified_by`, `verified_at`, `evidence` (official URLs and checked facts), and `fallback_reason`. Never fabricate a Bangumi ID, API verification, or Japanese title. Recheck the same identity evidence before release; the Bangumi sync command validates and skips IMDb projects without a network request or metadata rewrite.

The initializer accepts `--identity-provider bangumi|imdb`, `--identity-id`, and `--identity-snapshot`; the existing `--bangumi-id`/`--bangumi-snapshot` names remain aliases. Both snapshots contain `id`, `name` (the original title), `name_cn` (confirmed Chinese title), `date`, `platform`, and `total_episodes`; IMDb also requires `evidence` and `fallback_reason`. Use `platform: movie` for the IMDb single-movie fallback. The initializer records the approver; a snapshot alone never substitutes for the web check or user confirmation.

The distribution package is `bgm<subject-id> - <name_cn> [v<version>].zip` for Bangumi, or `imdb<tt-id> - <confirmed-Chinese-title> [v<version>].zip` for IMDb; release details are in `release-and-workspace.md`.

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
| Applicable series terms / user-confirmed names | Candidate terminology and existing decisions | Verify adopted forms against Simplified Chinese Wikipedia under SH-TRANS-007 |
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

Record actual language separately from roles. The Chinese baseline starts as `candidate-baseline`. Record any proposed timing or style authority in the combined initialization decision. Classify tracks from standard tags and titles, the known source language, and sampled text as needed. If a selected track is still materially ambiguous, include its alternatives in that decision. Leave unused optional tracks unselected and record any resulting evidence limitation. Write confirmed language, roles, scope, and evidence into `project.yaml`.

## Initialization gate

### SH-INIT-004 — Persist facts, not parallel status models

Materials are prepared when the baseline parses, the episode map and selected source roles are confirmed, `blocking_questions` is empty, and `--prepared-masters` passes. Proceed directly to SH-TRANS-007 without another routine confirmation. Formal proofreading requires prepared materials, a full-scope candidate scan, and a sourced core glossary index verified by `--ready-for-proofreading`.

Video plus a Chinese baseline permits Chinese, structure, timing, and local visual work when tools permit; it does not prove source-text fidelity or full listening/viewing. Missing capabilities are limitations, not invented completion states.

## Initialization sequence

### SH-INIT-005 — Safe creation order

1. Run identity discovery/check without creating the work directory.
2. Inventory the Chinese baseline and optional text/media in one system-temp JSON. Probe tracks only when video is supplied; classify only materials intended for use.
3. Present verified identity and scope, the episode map, material roles, timing authority, release languages, and the proposed series/project names as one decision. Include unresolved choices only if they affect this plan. Use clear defaults supported by the evidence. Reuse explicit approval that already covers the same concrete plan and ask only about remaining material choices.
4. After approval, run `scripts/init_project.py --dry-run` as an internal safety check and, when it passes, run the same command with `--dry-run` removed. Correct recoverable tool or intake issues within scope. Ask again only if identity, scope, mapping, authorities, release languages, or approved names materially change. Derived paths, assigned work IDs, and routine validation results need no confirmation.
5. Copy subtitle inputs into immutable `project/sources/`; record videos by basename and media facts, not by copying them.
6. Create `project.yaml`, root `review.md`, copied sources, and Noto episode masters. Create ignored `project/local.paths.yaml` only when local or password-free SSH media references must survive the run. Create other paths with their first file.
7. The initializer checks `--prepared-masters`. Once that passes, scan the subtitles, select core terms, and build their canonical index under SH-TRANS-007. Pass `scripts/validate_project.py PROJECT --ready-for-proofreading` before formal proofreading.

Initialization never modifies the user's original media or subtitle files.

## Skill 1.5.0-beta.1 intake contract

### SH-INIT-012 — Shared runtime gate

Before any repository script or project initialization, locate a usable Python 3 from the Codex workspace dependencies first, then ordinary `python`, `python3`, or the Windows `py` launcher. Run `scripts/setup_runtime.py --check`. If the environment is missing or outdated, run the same script with `--check` removed under existing authorization and request permissions through the platform only if required. The script creates or atomically replaces one environment at `~/.codex/subtitle-hub/venv`, keeps non-package state under the sibling `state/`, and returns the interpreter path. Continue immediately with that interpreter.

The exact packages are locked in `requirements.txt`, including Paramiko and PyYAML. Never install them globally, create a project-local virtual environment, copy dependencies into a project, or maintain an alternate package path. A requirements change invalidates and rebuilds only the shared `venv`; it preserves `state`. For complete cleanup, run `remote_media.py revoke` for every registered host before base Python runs `setup_runtime.py --remove`; the remover refuses to orphan registered keys. If no compatible base Python can execute `setup_runtime.py`, stop and report the missing prerequisite rather than partially initializing a project or attempting an operating-system Python installation.

### SH-INIT-006 — Probe before asking for manual inventory

Start from the user-provided target video path(s) and Chinese baseline rather than asking the user to enumerate container tracks. Run `scripts/inventory_sources.py`; it uses `ffprobe` to record container format, duration, resolution, audio/subtitle stream index, codec, language tag/title, default/forced disposition, and a suggested source-language audio stream. It also inventories external subtitle/script files, hashes them, assigns candidate roles, and proposes episode relationships.

Container language tags may use valid BCP 47 forms. Filenames/titles are weaker signals and may use only known aliases; never interpret an arbitrary short filename token as a language. If multiple source-language audio streams exist, select one with `--audio-stream VIDEO|INDEX`. Resolve a selected track with `--track-language VIDEO|INDEX|LANGUAGE`. Unknown embedded-subtitle language blocks only when that track is selected for source, timing, translation, layout, or release use.

The disposable intake JSON uses `schema_version: 4` and `skill_version: 1.5.0-beta.1`. It may contain local absolute paths or password-free SSH locators. Relevant fields are the evidence tier, videos, external sources, embedded tracks, `episode_map`, limitations, and blocking questions. Resolve the chosen mapping, target basenames, audio, timing authority, source roles, and ignored optional tracks in this same file; do not create a second mapping file. Do not initialize while a selected material question remains blocking.

### SH-INIT-011 — Guided SSH video intake

When the user declares that a project reads video from a Debian NAS over SSH, collect the host, port, username, exact absolute video paths or one containing directory, Chinese baseline mapping, intended source audio, and timing authority. For a directory, `remote_media.py discover` lists only top-level files with supported video or text-subtitle suffixes, in separate `media` and `subtitles` lists; never recurse or search outside that approved directory. Never request or accept the password in chat, arguments, files, URLs, or project records.

`remote_media.py` has one cross-platform backend: Paramiko 5.0.0 in the shared Skill environment. It does not use or configure system OpenSSH, AskPass, SSH agents, user keys, or general known-hosts files.

For an already enrolled connection, proceed directly to `discover` or `probe` with the existing pinned key and identity. For a first connection, `remote_media.py bootstrap` retrieves the ED25519 host key and computes the SHA-256 fingerprint. Ask the user to verify that exact fingerprint against a trusted NAS surface once, then rerun with `--accept-fingerprint <SHA256:...>` to pin it under the shared `state/` root. A changed or non-ED25519 key stops the connection.

After pinning, SSH initialization opens one local Tk password dialog; when Tk is unavailable, it opens a one-use tokenized form bound only to `127.0.0.1`. The same connection generates a dedicated local ED25519 identity under `state/`, uses `sudo` to create the account home/`.ssh` when absent, and appends exactly one tagged public-key line to `authorized_keys`. It then proves a fresh key-authenticated connection before succeeding. The password exists only in the initialization process and never enters chat, arguments, environment variables, files, project records, SSH agents, or key stores. Later `discover`, `probe`, `frame`, `audio`, and `subtitle` actions use only that identity and never prompt for a password.

This one home/SSH-key enrollment is the only permitted remote setup. Do not install packages, change `sshd`, upload tools or media, or create remote work/cache directories. If enrollment or later key authentication fails, stop and report the exact limitation; never fall back to repeated password prompts. A probe must succeed from the Codex process itself before initialization may claim SSH capability.

Use only existing remote programs. One `probe` connection checks Debian and the required existing tools, probes all approved exact files, and writes the password-free result to a system-temporary JSON. It stops if a required tool is absent; never install, upgrade, configure, upload, or retry with a broader account:

```text
python scripts/remote_media.py probe --host <host> --port <port> --user <user> \
  --path </absolute/video-1.mkv> --path </absolute/video-2.mkv> \
  --output <system-temp/ssh-video-probe.json>
```

Pass that result to the ordinary intake command with `--ssh-video-probe <system-temp/ssh-video-probe.json>`. Present the proposed episode map, detected tracks/languages, chosen audio, timing authority, and password-free SSH video references in the same initialization confirmation as identity and project name. Initialization writes only those password-free locators to the existing ignored `project/local.paths.yaml`; durable `project.yaml` keeps basenames and media facts. Delete the probe JSON after its conclusions are folded into the project.

For an external ASS/SSA/SRT/VTT baseline in the approved directory, use `remote_media.py subtitle --copy-text --path <exact-path> --output <system-temp/original-basename>` to read one size-bounded file unchanged through the same pinned connection. Embedded subtitle extraction uses `--stream <index>` instead. Neither action writes remote files.

Unapproved or changed host keys, authentication failure, missing remote tools, unreadable or symlink-resolved paths, malformed probe output, or changed scope stop the affected SSH operation. Continue independent text and identity work. If proceeding text-only changes the user's approved media or timing scope, put that tradeoff in the combined initialization decision or request approval for the changed scope. SSH failures never trigger credential persistence, remote environment setup, SFTP transfer, whole-file download, WebDAV fallback, or a second protocol implementation.

### SH-INIT-010 — Upgrade before reopening an older project

Do not maintain old-schema execution branches and do not bulk-upgrade dormant projects. When an existing project is selected for new proofreading or release work, first compare it with the current `project.yaml` and `review.md` templates. Re-express confirmed durable facts in project schema 9 and current Skill version, fold current state and still-open decisions into review schema 3, and prepare complete Noto masters from the immutable sources or current release. Preserve source files and released subtitles unchanged; invalidate coverage fingerprints whenever a master changes. Resolve only genuinely missing or conflicting intake facts with the user. Complete SH-TRANS-007 and pass `validate_project.py --ready-for-proofreading` before content work. Before reusing earlier line-by-line decisions, recheck their terminology against the completed glossary. Git retains the old control history.

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

The formal work directory is `<SHxxxx>--<project-name>`. Keep `project-name` short, lowercase, ASCII, and obvious to developers, for example `yamato-2199-tv`. Propose the name from the verified identity and type in the combined initialization decision. Record its approver and date in `project.yaml`. Reuse an explicitly approved name for the same plan.

The series directory is also a short developer-facing name. Reuse an established series directory when appropriate. Include any new series title and directory name in the same initialization decision. Initialization rolls back a new series if the project transaction fails.

### SH-INIT-009 — Transactional initializer and master preparation

Run a dry run as the internal transaction check, then the identical command without `--dry-run`:

```text
python scripts/init_project.py \
  --repository-root <repository> \
  --series-dir <works/series-name> \
  --project-name <approved-short-name> \
  --approved-by <approver> \
  --type <tv|movie|ova|ona|special> \
  --identity-provider <bangumi|imdb> \
  --identity-id <id> \
  --identity-snapshot <verified-identity-json> \
  --intake <temporary-intake.json> \
  --dry-run
```

Omit `--work-id` to allocate the next repository ID. Use `--create-series --series-title ...` only for an approved new series directory. The initializer copies subtitle evidence into immutable `project/sources/`, never copies video, conditionally writes an ignored local or password-free SSH video map, and prepares one `master.ass` per episode. It fills required ASS fields and maps every retained style and nonempty inline font directly to Noto SC/JP while preserving all other rendered properties. SRT/VTT baselines produce the same Noto contract. Initialization registers source-text roles but never merges source events, copies a prior Chinese line, or claims semantic alignment; A/B pairing begins with the reviewed mapping contract after initialization.

Initialization does not create a project README, `docs/`, or `subtitles/current/`. It checks `scripts/validate_project.py --prepared-masters` and rolls back a failed new-project/new-series transaction.

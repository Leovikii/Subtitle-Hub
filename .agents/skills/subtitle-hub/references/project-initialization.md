# Project initialization and material readiness

## Identity gate

### SH-ID-002 — Bangumi is the identity source

Search only to discover candidate IDs. Fetch `https://api.bgm.tv/v0/subjects/<id>` and verify `id`, `name`, `name_cn`, media/platform, date, and episode count against the requested scope. Save API `name` as `identity.titles.ja` and `name_cn` as `identity.titles.zh-Hans` without inferring either from filenames or other-language releases.

Pause before creating a formal project if `name_cn` is empty, the API is inaccessible, or plausible candidates differ by season, movie, OVA, compilation, special, remake, or scope. Present the candidate ID/title/scope evidence and ask the user. A user-confirmed draft does not satisfy the release-time `api-verified` requirement.

The distribution package is `bgm<subject-id> - <name_cn> [v<version>].zip`; release details are in `release-and-workspace.md`.

## Minimum required inputs

### SH-INIT-002 — Formal proofreading project minimum

Require all three:

1. Exact target video(s), readable and playable, with the intended dialogue audio; an external audio track is acceptable only when its episode match is established.
2. A Chinese subtitle baseline to proofread, in a reliably parseable format and covering the declared work scope.
3. A per-episode video/subtitle map and task declaration: source language, target language, primary/secondary release languages, work scope, and confirmation that this is proofreading rather than translation from scratch.

Do not copy video into the repository. Record exact basenames, duration/track summaries when known, and mappings without local absolute paths or download locations. Missing video blocks target-sync and visual completion. Missing Chinese baseline means this is not a proofreading initialization; changing to original translation needs explicit scope.

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

Record actual language separately from roles. Track language classification uses, in order: standard language tags and titles; work/audio source language; sampled text compared with actual speech. If tags are missing/`und`, conflict with content, multiple tracks are plausible, or the agent cannot decide reliably, pause and ask the user. Write the confirmed language, roles, scope, confirmer, date, and evidence into `project.yaml`; do not leave it only in chat.

## Readiness model

### SH-INIT-004 — Compute per dimension

Report each dimension as `ready`, `limited`, or `blocked` without adding these values to review-stage enums:

- `structure`: baseline parses and episode/language/style/event structure is inspectable.
- `language`: actual source-language audio is accessible and can be reviewed; matching text/script strengthens this dimension.
- `timing`: exact target video is accessible for speech, waveform, shots, and neighboring events.
- `visual`: target video, correct fonts, ASS renderer, and local evidence path are available.
- `release`: required dimensions for this round are covered, release checks pass, and P0/P1 disposition is valid.

Readiness is derived from `project.yaml`, current local availability, and recorded review coverage. Do not persist a second overall readiness truth. Put durable source limitations in `project.yaml`; reflect their current impact in `review.md` as `in-progress` or `blocked`.

The ordinary minimum `video + Chinese baseline` permits structure, Chinese expression, punctuation, internal terminology consistency, numeric candidates, and audio/video timing/visual work when tools permit. It does not justify claiming full source-text search, exact name spelling, low-clarity speech coverage, or visual approval without those capabilities.

## Initialization sequence

### SH-INIT-005 — Safe creation order

1. Run identity discovery/check without creating the work directory.
2. Inventory media/subtitles in a staging directory; classify languages and roles, asking only for unresolved material decisions.
3. Present identity/scope, episode map, material roles, release languages, and proposed short name as one user decision.
4. After approval, run `scripts/init_project.py --dry-run` as an internal safety check, then run the identical command without `--dry-run`. Ask again only if the manifest materially differs from the approved plan.
5. Copy subtitle inputs into immutable `project/sources/`; record videos by basename and media facts, not by copying them.
6. Create `project.yaml`, root-level `review.md`, copied sources, local mapping, and episode masters only. Other directories are created with their first output.
7. Run `scripts/validate_project.py`; do not begin content work until structural errors are resolved.

Initialization never modifies the user's original media or subtitle files.

## Skill 1.1 intake contract

### SH-INIT-006 — Probe before asking for manual inventory

Start from the user-provided target video path(s) and Chinese baseline rather than asking the user to enumerate container tracks. Run `scripts/inventory_sources.py`; it uses `ffprobe` to record container format, duration, resolution, audio/subtitle stream index, codec, language tag/title, default/forced disposition, and a suggested source-language audio stream. It also inventories external subtitle/script files, hashes them, assigns candidate roles, and proposes episode relationships.

Container language tags may use valid BCP 47 forms. Filenames and track titles are weaker signals and may use only known language aliases; never interpret an arbitrary two- or three-letter filename token as a language. If multiple source-language audio streams exist, select the intended one with `--audio-stream VIDEO|INDEX`. Resolve missing or conflicting track language with `--track-language VIDEO|INDEX|LANGUAGE`. Unknown embedded-subtitle language is blocking because its source/timing/translation role cannot otherwise be assigned safely.

The emitted intake JSON uses `schema_version: 2` and `skill_version: 1.1.0`. It may contain local absolute paths and is disposable. Relevant fields are `target_videos`, `external_source_groups`, `embedded_subtitle_tracks`, `proposed_episode_map`, per-dimension `readiness`, `blocking_questions`, `required_confirmations`, and `optional_requests`. Do not initialize while `blocking_questions` is non-empty or timing readiness is not `ready`.

Example:

```text
python scripts/inventory_sources.py \
  --target-video <video-or-directory> \
  --candidate-baseline <zh-subtitle-or-directory> \
  --optional-source <path>|<language>|<comma-separated-roles> \
  --source-language ja \
  --project-type tv \
  --output <temporary-intake.json>
```

### SH-INIT-007 — Approved episode map and IDs

Convert the proposal into a user/developer-approved UTF-8 TSV with this exact header:

```text
episode<TAB>video<TAB>subtitle<TAB>audio_stream<TAB>audio_language
```

Use stable internal episode IDs:

- TV/ONA: `S01E01` style; retain the actual season number when the project scope requires it.
- OVA: `OVA01`.
- Special: `SP01`.
- One film: `MOVIE`, with exactly one row.

Every row must refer to a video and Chinese baseline already present in the intake. The initializer rechecks file fingerprints, audio-stream presence/language, episode safety, and uniqueness of the resulting `<video-stem>.zh-Hans.ass` filenames. Similar filenames or durations alone never prove a mapping.

### SH-INIT-008 — Approve the developer-facing name before creation

The formal work directory is `<SHxxxx>--<project-name>`. Keep `project-name` short, lowercase, ASCII, and obvious to developers, for example `yamato-2199-tv`; it need not repeat the complete official title. Suggest one or more names from the verified identity/type, but ask the user to choose or approve one before running the initializer. Record the approver and date in `project.yaml`; never silently rename a work from a title guess.

The series directory is also a short developer-facing name. Reuse an established series directory when appropriate. Creating a new one requires an explicit series title and name approval; initialization rolls it back if the project transaction fails.

### SH-INIT-009 — Transactional initializer and master preparation

Run a dry run as the internal transaction check, then the identical command without `--dry-run`:

```text
python scripts/init_project.py \
  --repository-root <repository> \
  --series-dir <works/series-name> \
  --project-name <approved-short-name> \
  --project-name-approved-by <approver> \
  --type <tv|movie|ova|ona|special> \
  --bangumi-id <id> \
  --bangumi-snapshot <verified-api-json> \
  --scope-approved-by <approver> \
  --intake <temporary-intake.json> \
  --intake-approved-by <approver> \
  --episode-map <approved-map.tsv> \
  --dry-run
```

Omit `--work-id` to allocate the next repository ID. Use `--create-series --series-title ... --series-name-approved-by ...` only for an approved new series directory. The initializer copies external subtitle evidence into immutable `project/sources/`, never copies video, writes ignored local video mappings, and prepares one `master.ass` per episode. ASS/SSA baselines are copied byte-for-byte. SRT/VTT baselines are converted deterministically to UTF-8 ASS using `Noto Sans CJK SC`; this fallback is a working baseline, not a claim that styling was human-approved.

Initialization does not create a project README, `docs/`, or `subtitles/current/`. It promotes the staged work only if `scripts/validate_project.py --ready-for-proofreading` passes and rolls back a failed new-project/new-series transaction.

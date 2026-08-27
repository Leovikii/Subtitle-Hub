# Project initialization and material readiness

## Identity gate

### SH-ID-002 — Bangumi is the identity source

Search only to discover candidate IDs. Fetch `https://api.bgm.tv/v0/subjects/<id>` and verify `id`, `name`, `name_cn`, media/platform, date, and episode count against the requested scope. Save API `name` as `identity.titles.ja` and `name_cn` as `identity.titles.zh-Hans` without inferring either from filenames or other-language releases.

Pause before creating a formal project if `name_cn` is empty, the API is inaccessible, or plausible candidates differ by season, movie, OVA, compilation, special, remake, or scope. Present the candidate ID/title/scope evidence and ask the user. A user-confirmed draft does not satisfy the release-time `api-verified` requirement.

The distribution package is `bgm<subject-id> - <name_cn> [v<version>].zip`; normalization and release details are in `release-and-packaging.md`.

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

Derived waveforms, frames, media summaries, and track listings live in `project/workspace/temp/` and are not unique durable evidence.

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

Readiness is derived from `project.yaml`, current local availability, and recorded review coverage. Do not persist a second overall readiness truth. Put durable limitations in `ledger.tsv`; use `in-progress` with the item reference when limited work continues, or `blocked` when the stage cannot proceed.

The ordinary minimum `video + Chinese baseline` permits structure, Chinese expression, punctuation, internal terminology consistency, numeric candidates, and audio/video timing/visual work when tools permit. It does not justify claiming full source-text search, exact name spelling, low-clarity speech coverage, or visual approval without those capabilities.

## Initialization sequence

### SH-INIT-005 — Safe creation order

1. Run identity discovery/check without creating the work directory.
2. Inventory media/subtitles in a staging directory; classify languages and roles, asking only for unresolved material decisions.
3. Produce a readiness report and explicit episode map.
4. Run `scripts/init_project.py --dry-run`, inspect its manifest, then run without `--dry-run` only after identity and minimum inputs pass.
5. Copy subtitle inputs into immutable `project/sources/`; record videos by basename and media facts, not by copying them.
6. Create the control files and workspace skeleton from `assets/templates/`.
7. Run `scripts/validate_project.py`; do not begin content work until structural errors are resolved.

Initialization never modifies the user's original media or subtitle files.

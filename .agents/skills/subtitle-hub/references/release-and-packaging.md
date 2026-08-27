# Versioning, release, rollback, and packaging

## SH-REL-002 — Stable release directories

Maintain:

```text
subtitles/current/VERSION + *.ass
subtitles/previous/VERSION + *.ass
```

`subtitles/current/VERSION` is the published-version authority. Do not create version-number directories or copy the current version into READMEs/YAML. A first `1.0.0` baseline may have no previous directory; after the first content replacement, a complete previous directory is mandatory forever.

Use SemVer without `v`: PATCH for fixes that preserve scope/contract; MINOR for backward-compatible scope/language/compatible-source expansion; MAJOR for incompatible layout/naming/scope/format contract. Documentation, Skill, tooling, or directory-only migration does not change subtitle content version.

## SH-REL-003 — Released filenames and language metadata

Name each release file `<target-video-stem>.<primary-language>.ass`; Simplified Chinese primary is `.zh-Hans.ass`. Never append secondary language or maintain aliases such as `chi`, `zho`, `zh-CN`, or `chs`.

Each released ASS has exactly one version, language-list, and primary-language field. Add the secondary-language field only for a bilingual release:

```ass
; Subtitle-Hub-Version: <VERSION>
; Subtitle-Hub-Languages: zh-Hans[, <secondary>]
; Subtitle-Hub-Primary-Language: zh-Hans
; Subtitle-Hub-Secondary-Language: <secondary>
```

The last field is omitted for a monolingual release; its language-list field contains only `zh-Hans`.

Values must match `project.yaml` and the same-directory VERSION.

## SH-REL-004 — ASS header and credits

Use this Script Info order, omitting optional lines only when truly absent:

```ass
[Script Info]
; Subtitle-Hub-Version: <version>
; Subtitle-Hub-Languages: <primary>[, <secondary>]
; Subtitle-Hub-Primary-Language: <primary>
; Subtitle-Hub-Secondary-Language: <secondary>
; Subtitle-Hub-Timing-Note: <optional durable timing provenance>
; Subtitle-Hub-Source-Credit: <complete identifiable original production credits>
Title: bgm<subject-id> - <name_cn> - <episode-id>
ScriptType: v4.00+
WrapStyle: <preserved>
ScaledBorderAndShadow: <preserved>
PlayResX: <preserved>
PlayResY: <preserved>
YCbCr Matrix: <preserved>
```

Omit the secondary-language line, and omit the comma/secondary value from the language list, for a monolingual release.

Use `MOVIE` for a single film's episode ID. Preserve valid ScriptType, WrapStyle, resolution, border/shadow, and matrix values. Remove Aegisub project garbage, local media paths, websites, default/blank editor fields, and empty boilerplate.

When the baseline contains identifiable original production credits, preserve the full subtitle group and translation/listening/proofreading/timing/effects/encoding/source roles and people. Merge them into exactly one non-rendered `Subtitle-Hub-Source-Credit`. Never reduce to group name only. Do not invent credits from a filename/directory. Remove disclaimers/websites; keep engineering provenance in project control files, not Events.

Events must keep the required `Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text`. Never represent credits/provenance as Comment, `Source-Metadata`, zero-duration, or hidden Events.

## SH-REL-005 — Structural normalization boundary

Do not establish a repository-wide ASS style sheet. A release normalization may delete only styles proven unused by Dialogue/Comment Style fields, every `\r<StyleName>` reset, and empty Style's implicit `Default`. Revalidate all references. Otherwise preserve `[V4+ Styles]` onward, including order, retained styles, comments, events, effects, and attachments, except separately approved font mappings or precisely identified metadata-event cleanup.

Do not merge equivalent styles, rename styles, or alter retained size/color/margins/alignment/border/shadow without an explicit visual-change round and review.

## SH-REL-006 — Transaction and rollback

1. Freeze a complete checked candidate in `project/workspace/build/` (or a same-volume candidate directory used for atomic promotion).
2. Select SemVer and write it to every ASS marker plus candidate VERSION.
3. Validate scope, names, languages, structure, audio/visual coverage, ledgers, and rollback chain.
4. Delete the older `subtitles/previous/` only after resolving and confirming its exact path.
5. Rename the complete old `current/` directory to `previous/`; do not copy files or repackage it.
6. Rename the complete validated candidate directory to `current/`.
7. Commit/push relevant release and control changes; let GitHub Actions generate the ZIP. Do not commit a locally generated distribution ZIP.
8. Verify the generated ZIP name/version, internal VERSION, ASS count/markers, and CHECKSUMS.

If promotion fails after rotation, restore the just-rotated `previous/` directory to `current/`; never leave a mixed current. A deliberate rollback swaps current/previous roles so the withdrawn version remains traceable, regenerates the package, and records the transaction.

## SH-REL-007 — Distribution package

Use `packages/bgm<subject-id> - <name_cn> [v<version>].zip`. Values come from the API-verified `project.yaml` identity and current VERSION. Normalize `name_cn` to NFC; replace Windows-forbidden `<>:\"/\\|?*` with space-hyphen-space, collapse whitespace, remove trailing spaces/dots, and keep the UTF-8 filename at or below 240 bytes without otherwise translating or reordering the title.

The ZIP contains current ASS files, VERSION, and generated `CHECKSUMS.sha256` only—no source subtitles, video maps, masters, temporary evidence, fonts, or archives. Noto fonts are an external installation dependency.

`.github/scripts/build_subtitle_packages.py` is the deterministic package implementation. It must sort deterministically and use stable timestamps/compression. Automatic runs are triggered by current VERSION changes on main (or manually), confirm the triggering commit is still current before build and push, and update packages only when content changes. For any version beyond an initial 1.0.0, validate a distinct, self-consistent previous release before packaging.

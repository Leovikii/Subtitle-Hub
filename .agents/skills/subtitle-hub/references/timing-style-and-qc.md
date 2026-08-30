# Timing, Chinese-primary style, and quality control

## SH-QC-007 — One frozen industry basis

The sole external industry basis is Netflix's [Simplified Chinese Timed Text Style Guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215986007-Simplified-Chinese-Timed-Text-Style-Guide). It informs Chinese readability, punctuation, line treatment, and presentation principles. Routine work uses the values below and does not re-query or compile other guides.

Netflix does not mandate this repository's exact ASS font, sizes, margins, outlines, or bilingual baselines. `Noto Sans CJK SC/JP`, sizes `62/46`, mono margins `96/96/70`, bilingual vertical baselines `130/68`, and visible separation `12–20 px` are Subtitle Hub engineering adaptations for 1920×1080 ASS delivery.

## SH-TIME-002 — Timing order and fallback

Confirm frame rate/time base; inventory target-video tracks; map source text to the target cut; compare speech starts/ends; account for shots and first-visible information; then evaluate reading speed and bilingual pairing. Never reveal information early merely to add reading time.

When embedded timing is absent or clearly wrong, use: actual source-language audio/waveform/speech boundaries; shot and visible-information boundaries; the numeric baseline below; then verified adjacent rhythm. Do not infer compatibility from filenames or similar duration.

## SH-TIME-003 — Numeric baseline

| Metric | Normal target |
| --- | --- |
| Chinese ordinary dialogue | one primary line |
| Secondary dialogue | one line below Chinese |
| Chinese CPL | target ≤ 16 full-width equivalents; 17–18 warning |
| Adult Chinese CPS | target ≤ 9 |
| Child Chinese CPS | target ≤ 7 only for a declared child audience |
| Minimum duration | about 5/6 second; 20 frames at 24 fps |
| Maximum duration | 7 seconds |
| Neighbor gap | 2 frames, checked against reliable same-release rhythm |

Count visible Chinese after stripping ASS tags and controls; prefer rendered/weighted width over Unicode length. These values detect risk and never authorize bulk retiming or rewriting.

## SH-TIME-004 — Mandatory correction floor

Unparseable times, `end <= start`, or times outside media duration are P0. The following are P1 unless structurally stricter: unintended unrelated overlap or broken bilingual pairing; at least 10 visible ordinary Chinese characters under 1 second; ordinary adult dialogue clearly above about 12 CPS without verified rapid speech; over 7 seconds without continuing speech or visual reason; clear speech-boundary error/early reveal; disappearance before a continuous utterance finishes; mismatched Chinese/secondary boundaries or segmentation.

Confirm against the fallback evidence, fix only the event and necessary neighbors, and recheck the next start, gap, speaker change, and shot. Never hide a failure by deleting meaning, raising thresholds, or splitting without a natural boundary.

## SH-TIME-005 — Segmentation

Split at semantic pauses, clause boundaries, breath, or speaker changes. Do not split names/terms, number+unit, preposition+object, conjunction+clause, pronoun+predicate, modal/negative+verb, collocations, or idioms. Correct an end shorter than actual speech before considering accurate condensation or meaningful segmentation.

## SH-LAYOUT-002 — Bilingual ordinary dialogue

Chinese is above and visually primary; the source language is below at about 70–77% of Chinese size. At 1920×1080 use Chinese `62`, `MarginV=130` (allowed 125–135), and secondary `46`, `MarginV=68` (allowed 65–70), with about 12–20 px visible separation. Prefer matching boundaries. Evidence-backed one-to-many, many-to-one, or cross-event pairing is allowed when meaning/order are complete, timing remains readable, and no duplicate, omission, or collision is introduced.

This differs intentionally from mono Chinese. If Chinese needs two lines, prefer meaningful resplitting or accurate condensation; ASS has no portable style-level line-spacing control, and `\fsp` is character spacing, not line spacing.

## SH-LAYOUT-003 — Ordinary versus special

Normalize size, margins, alignment, colors, outline, shadow, scale, spacing, position, motion, karaoke, and effects only for declared ordinary styles. Do not standardize those properties for notes, signs, songs, titles, credits, broadcasts, positioned text, multiple-speaker layouts, or effects. Preserve useful baseline/embedded-reference design unless a concrete defect or target-video incompatibility is confirmed. Global font-family replacement under `SH-LAYOUT-004` is the sole exception to this property boundary. A non-source embedded track remains valid timing/layout and disambiguation evidence.

## SH-LAYOUT-004 — Fonts

Every master and release uses static `Noto Sans CJK SC` for Simplified Chinese/English and `Noto Sans CJK JP` for Japanese in every retained style and nonempty inline `\fn`. This global font-only rule includes special subtitles and changes no other property. Resolve Japanese from the confirmed role, style label, or visible kana; use SC otherwise. Do not use ASS `[Fonts]`. Font normalization needs no separate screenshot gate.

## SH-LAYOUT-005 — Mono ordinary Chinese baseline

At 1920×1080 use one coherent ordinary style: `Noto Sans CJK SC`, size `62`, bottom center (`Alignment=2`), margins `96/96/70`, opaque white fill, opaque near-black `3 px` outline, `Shadow=0`, scale `100/100`, spacing `0`. Scale by PlayRes; allowed size is 58–64, bottom margin 65–85, and outline 2.5–3.5, but keep one value across a work and record any confirmed override in `project.yaml`.

Use the mono profile when the actual release has no secondary dialogue track, regardless of optional evidence. At final review check representative bright/dark scenes, long lines, bilingual separation where applicable, and ordinary overrides without generating screenshots unless a concrete question remains.

## SH-QC-002 — Severity

| Severity | Release disposition |
| --- | --- |
| P0 | Corrupt/missing/unrenderable, illegal time, wrong release content: must fix |
| P1 | Confirmed meaning/name/term error, severe desync, correction-floor or obvious readability failure: fix or obtain owner waiver |
| P2 | Punctuation, segmentation, width, mild register, ordinary layout: should fix or track |
| P3 | Optional polish or low-confidence candidate: may defer |

## SH-QC-003 — Machine and local checks

Check ASS structure/times, filenames/scope, style references, bilingual mapping, overlaps, hidden text, fonts, punctuation/spacing, terminology candidates, width/CPS/duration/gaps, source coverage, version markers, and rollback structure. Use the terminology audit routed from `proofreading-and-approval.md` when confirmed entity forms exist. Machine checks prove structure or declared-form counts, or raise candidates; they never prove translation, register, sync, obstruction, unknown aliases, or full playback.

## SH-QC-008 — Text-first evidence escalation

Resolve each dimension with the cheapest sufficient evidence, then stop: subtitle text/timecodes/static geometry; user-confirmed timing authority; same-cut embedded evidence; source text and auxiliary translations; one candidate frame/minimal waveform/one-point render/concrete scene context; human final review.

Do not run ASR, VAD, OCR generation, full-track extraction, full-video frame processing, scene detection or bulk rendering. Video is optional and may be used only for a flagged short/invalid duration, conflicting timing evidence, suspicious special-subtitle placement/effect, or unresolved scene meaning. `ffprobe` is allowed only when video is supplied. Never imply full listening/viewing from point checks.

### SH-QC-010 — Read-only SSH media points

For a project whose ignored local map contains an SSH video locator, use `scripts/remote_media.py` only after text/timecode/static geometry has identified a concrete media-required point. `frame` returns one JPEG for one timestamp; `audio` returns at most 30 seconds of mono audio for a bounded timing question; `subtitle` returns one selected embedded text track. Keep each output under the system temporary directory, use it locally, record only the time point and conclusion in `review.md`, then delete it. Do not batch points, upload ASS to the server, render on a remote file, extract a full audio track, or persist remote output.

The remote command uses the existing Debian tools through system OpenSSH, user-confirmed then strict host-key checking, password authentication, one connection attempt, concurrency one, one decode thread, and both remote and client timeouts. It resolves the exact approved file and rejects symlink or path changes before reading. All remote media outputs travel over stdout; no command may create files, caches, logs, directories, packages, containers, services, or configuration on the NAS. The server filesystem may update access time under its own mount policy; the Skill never changes that policy. If the connection or required command fails, record the limitation and stop media escalation rather than installing tools or downloading the video.

## SH-QC-009 — Full static layout audit

Audit every rendered ASS event without video before selecting media points. Report structure-proven defects as `confirmed`, heuristic geometry/wrap findings as `risk`, and points that need media as `media-required`.

Check explicit and predicted wrapping, ordinary-dialogue line count, bilingual vertical stacking, simultaneous time-and-space collisions, off-screen or fully hidden text, zero/abnormal alpha/scale/size, undefined `\rStyle`, and malformed or suspicious `\pos`, `\move`, `\clip`, `\fad`, `\fade`, and `\t`. Account for PlayRes, alignment, margins, style fields, event overrides, and intentional special positioning. A time overlap alone is not a spatial collision.

Run the full audit once against the final master. Candidate construction then proves that rendered Events and referenced style properties did not change; it does not repeat the same geometry audit. Only non-rendering release cleanup authorized by `SH-REL-008` may differ.

Use actual media for speech, timing, early reveals, pairing, positioned/animated text, obstruction, multiple speakers, songs, and special layout. Record candidate-point coverage honestly. Keep visual evidence local; do not batch-upload screenshots, frames, contact sheets, or Base64 images. Only at explicit user request may one message show at most two compressed screenshots for one point.

## SH-QC-006 — Release gate

Before final review require complete scope; P0 zero; P1 zero or waiver; correction-floor disposition; valid bilingual pairing; structure pass; every substantive row approved and verified; truthful coverage; correct version/header/font/credit/cleanup/previous contract; a local package-plan check with no ZIP writes; and updated `review.md`. `human_release_review` includes playback only when video is available and the round claims timing/visual completion; otherwise it explicitly accepts the recorded media limitations. Release only after it passes. GitHub Actions builds packages, verifies checksums, removes stale packages, and regenerates indexes after the release push.

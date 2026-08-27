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

Chinese is above and visually primary; the source language is below at about 70–77% of Chinese size. At 1920×1080 use Chinese `62`, `MarginV=130` (allowed 125–135), and secondary `46`, `MarginV=68` (allowed 65–70), with about 12–20 px visible separation using the actual fonts/renderer. Paired events have identical boundaries and one-to-one mapping.

This differs intentionally from mono Chinese. If Chinese needs two lines, prefer meaningful resplitting or accurate condensation; ASS has no portable style-level line-spacing control, and `\fsp` is character spacing, not line spacing.

## SH-LAYOUT-003 — Ordinary versus special

Normalize only declared ordinary styles. Do not standardize notes, signs, songs, titles, credits, broadcasts, positioned text, multiple-speaker layouts, motion, karaoke, or effects. Preserve useful baseline/embedded-reference design unless a concrete defect or target-video incompatibility is confirmed. A non-source embedded track remains valid timing/layout and disambiguation evidence.

## SH-LAYOUT-004 — Fonts

Use static `Noto Sans CJK SC` for Simplified Chinese and English, and `Noto Sans CJK JP` for Japanese. Do not use ASS `[Fonts]`. Decorative families are permitted only when their form carries narrative meaning. When replacing fonts, update style `Fontname` and inline `\fn` together; check long lines and positioned/effect events locally. No separate screenshot approval is required.

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

Check ASS structure/times, filenames/scope, style references, bilingual mapping, overlaps, hidden text, fonts, punctuation/spacing, terminology candidates, width/CPS/duration/gaps, source coverage, version markers, and rollback structure. Machine checks prove structure or raise candidates; they never prove translation, register, sync, obstruction, or full playback.

Use actual media for speech, timing, early reveals, pairing, positioned/animated text, obstruction, multiple speakers, songs, and special layout. Record candidate-point coverage honestly. Keep visual evidence local; do not batch-upload screenshots, frames, contact sheets, or Base64 images. Only at explicit user request may one message show at most two compressed screenshots for one point.

## SH-QC-006 — Release gate

Before final review require complete scope; P0 zero; P1 zero or explicit waiver; correction-floor and early-disappearance disposition; equal bilingual boundaries; structure pass; every substantive row approved and verified; truthful machine/human coverage; correct version/header/font/credit/cleanup/previous-release contract; a successful local package-plan check with no ZIP writes; and `review.md` updated from proposals to actual results. Then request one final review and release only after it passes. GitHub Actions performs final package construction, CRC/checksum verification, stale-package removal, and index regeneration after the release push.

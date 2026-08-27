# Timing, segmentation, layout, styles, and fonts

## SH-TIME-002 — Timing order

Confirm frame rate/time base; inventory target-video embedded tracks; map source text to the target cut; compare starts/ends with actual speech; account for shots and first-visible information; then evaluate Chinese reading speed and bilingual pairing. Starts normally sit close to the first speech frame, but never reveal a joke or plot point early merely to add reading time.

When embedded timing is absent or clearly wrong, use this fallback order:

1. Actual source-language audio, waveform, and speech boundaries.
2. Shot boundaries and the first/last visible position of relevant information.
3. Built-in duration/CPS/gap baselines below.
4. Rhythm of adjacent events already verified against the target video.

Do not infer compatibility from filenames, titles, or similar durations.

## SH-TIME-003 — Built-in numeric baseline

| Metric | Normal target | Use |
| --- | --- | --- |
| Chinese dialogue lines | 1 | One Chinese primary line in ordinary bilingual dialogue |
| Secondary lines | 1 | Below Chinese |
| Simultaneous dialogue lines | 2 total | More requires manual resplitting/layout |
| Chinese CPL | target ≤ 16 full-width equivalents | 17–18 warning; longer requires manual review |
| Adult Chinese CPS | target ≤ 9 | Candidate above target; correction floor below |
| Child Chinese CPS | target ≤ 7 | Only when project declares child audience |
| Minimum duration | about 5/6 second; 20 frames at 24 fps | Candidate when shorter |
| Maximum duration | 7 seconds | Candidate when longer |
| Neighbor gap | 2 frames | Review against reliable same-release rhythm |

Count visible Chinese after stripping ASS override tags and line controls. Prefer actual rendered/weighted width over Unicode length. These numbers detect risk; ordinary exceedance never authorizes bulk retiming or rewriting.

## SH-TIME-004 — Mandatory correction floor

Treat unparseable times, `end <= start`, or times outside valid media duration as P0. Treat the following as P1 unless a stricter structural classification applies:

- unintended same-logical-track overlap that displays unrelated dialogue together or breaks bilingual pairing;
- ordinary Chinese dialogue with at least 10 visible characters shown for under 1 second;
- ordinary adult dialogue clearly above about 12 CPS, absent a verified exceptional rapid utterance;
- duration over 7 seconds without continuing speech, cross-shot dialogue, screen text, or another audio/visual reason;
- start clearly before/after speech, end dragging into the next sentence, or early reveal;
- subtitle disappearing before the same continuous utterance finishes;
- Chinese and its paired secondary event having different time boundaries or mismatched segmentation.

Once triggered, use the fallback evidence order, fix only the confirmed event and necessary neighbors, and recheck the next start, two-frame gap, speaker change, and shot. Extend Chinese and paired secondary text together to a reliable speech end when the same utterance continues. Do not hide the error by deleting meaning, raising thresholds, splitting where no natural boundary exists, or making text disappear and return.

## SH-TIME-005 — Segmentation

Split at semantic pauses, clause boundaries, source punctuation, breath, or speaker changes. Do not split names/terms, number+unit, preposition+object, conjunction+following clause, subject pronoun+predicate, modal/negative+main verb, fixed collocations, or idioms. Geometry follows language structure. A continuous sentence cannot be split merely because it is long; first correct an end that is shorter than the actual speech, then consider accurate condensation or meaningful segmentation.

## SH-LAYOUT-002 — Chinese-primary bilingual layout

Chinese stays above and visually primary; English/Japanese stays below, normally at about 70–77% of Chinese size with slightly lower visual weight but clear readability. Keep stable horizontal centering and vertical positions. At 1920×1080 use a practical starting pair of Chinese 62 with `MarginV=130` and secondary 46 with `MarginV=68`; adjust within Chinese 125–135 and secondary 65–70 to achieve about 12–20 px of visible separation with the actual fonts/renderer. Paired events share identical boundaries and a one-to-one mapping.

This bilingual height is intentionally different from the monolingual Chinese baseline. If Chinese needs two lines, prefer resplitting or accurate condensation rather than creating routine three-line bilingual dialogue. ASS has no portable style-level line-spacing field: `\fsp` is character spacing and must not be used as a substitute. Let the chosen font's natural line metrics handle an exceptional two-line Chinese event and check it in the final review.

For multiple speakers, prefer consecutive bilingual pairs with real speech timing. If speech truly overlaps, use project-defined concise speaker cues and perform local visual review; do not stack four routine dialogue lines.

## SH-LAYOUT-003 — Ordinary versus special styles

Normalize ordinary Chinese dialogue to `SH-LAYOUT-005`. Do not extend that normalization to notes, signs, songs, titles, credits, broadcasts, positioned text, multiple-speaker layouts, motion, karaoke, or effects. For those special events, preserve useful baseline/embedded-reference colors, sizes, margins, alignment, border, fades, position, and motion unless clearly defective or incompatible.

Do not copy coordinates blindly across different PlayRes, aspect, crop, or renderer assumptions. Screen text follows its visible interval and avoids key image information. A non-source-language embedded track remains valid timing/layout and disambiguation evidence.

## SH-LAYOUT-004 — Fonts and glyphs

Use static `Noto Sans CJK SC` for Simplified Chinese and English, and static `Noto Sans CJK JP` for Japanese. English uses the SC family's Latin glyphs. Do not use ASS `[Fonts]`. Ordinary dialogue uses a modern sans-serif; do not retain unregistered niche fonts solely because the baseline used them.

Serif, Mincho/Song, Kai, rounded, handwriting, or decorative fonts are permitted only when the font itself carries narrative meaning, such as letters, inscriptions, historical documents, or native title art. Record the exact project style/scenes/reason. Songs, broadcasts, alien speech, and screen text do not automatically justify a font exception.

When replacing fonts, change style `Fontname` and inline `\fn` together. Ordinary dialogue then follows `SH-LAYOUT-005`; special styles preserve their remaining geometry and effects. Build a risk list for long lines, `\pos`, `\move`, `\clip`, scale, fades, lyrics, and karaoke. Check static overflow and locally inspect only concrete risk points. Font/size/dialogue-margin normalization does not require a separate screenshot approval; it is covered by the proofreading-plan approval and release-candidate final review.

## SH-LAYOUT-005 — Ordinary Chinese dialogue baseline

Use one coherent style across a work. Scale these 1920×1080 values proportionally to PlayResY:

| Property | Baseline | Allowed adjustment |
| --- | --- | --- |
| Font | `Noto Sans CJK SC` | No ordinary-dialogue exception |
| Size | 62 | 58–64 for actual weight/density; keep one value across episodes |
| Placement | bottom center (`Alignment=2`) | Fixed unless a scene requires a separately named special style |
| Bottom margin, Chinese-only | 70 (6.5% of height) | 65–85; use when the released subtitle has no secondary dialogue line |
| Bottom margin, bilingual Chinese | 130 | 125–135; pair with the secondary baseline in `SH-LAYOUT-002` |
| Side margins | 96 (5% of width) | Increase for compatibility; do not reduce below 5% without project evidence |
| Fill | opaque white | May use a consistent near-white |
| Outline | opaque near-black, 3 px | 2.5–3.5 px according to weight; no routine translucent outline |
| Shadow | 0 | At most a subtle 1 px if an established project design needs it |
| Scale/spacing | 100/100/0 | Avoid condensed or expanded ordinary dialogue |

This is a desktop/ASS safe-area and readability baseline, not a claim that one streaming service mandates it. Determine monolingual versus bilingual from the actual release languages, not from whether optional source text exists: a project without a releasable secondary subtitle uses the Chinese-only height. Favor one Chinese line; use meaningful segmentation before reducing size. At final review check representative bright/dark scenes, long lines, bilingual separation where applicable, and any ordinary-dialogue overrides. Do not generate screenshots unless a concrete question remains unresolved.

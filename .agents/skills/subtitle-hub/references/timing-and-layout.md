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

Chinese stays above and visually primary; English/Japanese stays below, normally at about 65–80% of Chinese size with slightly lower visual weight but clear readability. Keep stable horizontal centering and vertical positions. Paired events share identical boundaries and a one-to-one mapping. If Chinese needs two lines, prefer resplitting or accurate condensation rather than creating routine three-line bilingual dialogue.

For multiple speakers, prefer consecutive bilingual pairs with real speech timing. If speech truly overlaps, use project-defined concise speaker cues and perform local visual review; do not stack four routine dialogue lines.

## SH-LAYOUT-003 — Style and embedded-reference policy

Start from the candidate Chinese subtitle's reviewed styles, not a universal repository style sheet. Preserve useful colors, sizes, margins, alignments, borders, shadows, fades, positioning, motion, karaoke, and project effects unless the task explicitly changes them. Use target-video embedded subtitles to inform same-release timing, splits, screen-text positions, and effects. A non-source-language embedded track can still be valuable for timing/layout and translation disambiguation.

Do not copy embedded styles or coordinates directly when PlayRes, video resolution/aspect, crop, safe area, renderer assumptions, or target language width differs. Compare coordinate systems and revalidate locally. For an obvious timing/layout failure, use the built-in baseline and actual audio/video rather than silently preserving a broken inherited design.

Dialogue should stay within the shot when speech does; speech crossing a cut may cross it. Screen text should match its visible interval and avoid key image information. Project guides define top communication, broadcast, signs, songs, notes, and special-scene priority.

## SH-LAYOUT-004 — Fonts and glyphs

Use static `Noto Sans CJK SC` for Simplified Chinese and English, and static `Noto Sans CJK JP` for Japanese. English uses the SC family's Latin glyphs. Do not use ASS `[Fonts]`. Ordinary dialogue uses a modern sans-serif; do not retain unregistered niche fonts solely because the baseline used them.

Serif, Mincho/Song, Kai, rounded, handwriting, or decorative fonts are permitted only when the font itself carries narrative meaning, such as letters, inscriptions, historical documents, or native title art. Record the exact project style/scenes/reason. Songs, broadcasts, alien speech, and screen text do not automatically justify a font exception.

When replacing fonts, change style `Fontname` and inline `\fn` together while preserving size, weight, scale, spacing, alignment, margins, border, shadow, colors, and effects. Build a risk list for long lines, `\pos`, `\move`, `\clip`, scale, fades, lyrics, and karaoke. Check static overflow and locally render the available risk points. Effect tags remaining does not prove visual equivalence, and partial sampling does not prove full-film visual approval.

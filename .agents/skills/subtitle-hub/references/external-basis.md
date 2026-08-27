# Embedded industry baseline and provenance

## SH-QC-007 — Routine use

The operational values are embedded in `chinese-language.md` and `timing-and-layout.md`. Routine proofreading, initialization, QC, and issue logs cite stable Skill rule IDs and do not re-query Netflix, BBC, DCMP, or other external guides.

Consult external material only for a deliberate baseline audit, a proposed threshold change, a new delivery format/client, or a contradiction not covered here. Such a change is a Skill-maintenance task and must record access date, exact external source, adopted point, repository adjustment, compatibility impact, and user approval where it changes the standard.

## Current provenance (baseline frozen 2026-08-26)

- Netflix Simplified Chinese and general timing guides informed 16 Chinese CPL, adult 9 CPS, child 7 CPS, minimal punctuation, natural breaks, about 5/6-second minimum, 7-second maximum, and two-frame gaps.
- BBC subtitle guidance informed source fidelity, register preservation, language-first line breaking, and readable sans-serif practice; its English WPM values are not converted into Chinese CPS.
- DCMP Captioning Key informed accuracy, consistency, clarity, readability, equivalence, and meaning-preserving compression; its English presentation rates are not Chinese thresholds.
- Noto CJK and SIL OFL sources informed the repository's cross-platform SC/JP static-font choice. No platform is claimed to require these exact fonts.

Repository adaptations are authoritative: Chinese-primary bilingual layout uses one Chinese line plus one secondary line; target-video evidence outranks mechanical numeric cleanup; correction-floor errors cannot be excused by embedded provenance; and `Noto Sans CJK SC/JP` is an engineering choice.

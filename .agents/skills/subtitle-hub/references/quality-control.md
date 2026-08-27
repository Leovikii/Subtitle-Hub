# Quality control and evidence

## SH-QC-007 — Frozen internal baseline

Routine work uses this Skill's embedded timing, text, and style values and does not re-query Netflix, BBC, DCMP, or similar guides. Consult external material only for a deliberate Skill baseline audit, a new delivery format, or an uncovered contradiction.

## SH-QC-002 — Severity

| Severity | Meaning | Release disposition |
| --- | --- | --- |
| `P0` | Corrupt/missing/unrenderable file, illegal time, wrong release content | Must fix |
| `P1` | Confirmed mishearing/mistranslation, critical omission/name/term error, severe desync, mandatory timing-floor or obvious unreadability failure | Must fix or obtain a recorded project-owner waiver |
| `P2` | Punctuation, segmentation, width, mild register, or ordinary layout issue | Should fix; otherwise track |
| `P3` | Optional polish, preference, low-confidence candidate | May defer |

## SH-QC-003 — Machine checks

Check encoding and ASS sections; event field counts/times; Script Info contract; required Events `Format`; filename/episode completeness; style and `\rStyle` references; bilingual counts/boundaries/mapping; illegal times and unintended overlaps; invisible/hidden text; allowed fonts and no `[Fonts]`; prohibited punctuation/spacing; terminology candidates; CPL/width/CPS/duration/gaps; source coverage; version markers; and release rollback structure.

The header must contain exactly the applicable Subtitle Hub fields and no Aegisub garbage, absolute paths, websites, disclaimers, or empty editor metadata. When the source has identifiable production credits, preserve the full group/person/role information in exactly one `Subtitle-Hub-Source-Credit`. Do not accept `Source-Metadata` or provenance events.

Machine checks may prove structure or produce candidates. They never prove translation accuracy, natural register, sync to sound, lack of image obstruction, or full-playback quality. Report numeric candidates separately from `SH-TIME-004` floor violations.

## SH-QC-004 — Audio/visual checks

Use actual media for homophones, speaker/voice-over, speech boundaries, embedded timing quality, early reveals, rapid readability, bilingual meaning pairing, top/positioned/animated text, screen obstruction, multiple speakers, songs, foreign speech, and special layout. A candidate-point check is recorded as candidate-point coverage, not full playback.

### Visual evidence transport

Perform checks locally at candidate timestamps. Prefer playback/render inspection and record episode, timestamp, and text conclusion. Do not create an image merely to prove that a check happened; use a temporary local image only when a concrete visual question cannot otherwise be resolved.

Never batch-upload screenshots, consecutive frames, contact sheets, Base64 images, or other large visual evidence to chat because this can trigger CDN HTTP 413. Only when the user explicitly asks to see one point may one message contain at most two compressed necessary screenshots. Images supplement, not replace, continuous media/audio review.

When local fonts/rendering/media access is missing, record the limitation and do not claim visual pass. Ordinary dialogue font/size/safe-margin normalization is reviewed in the proofreading plan and release-candidate final review, not through a separate screenshot approval.

## SH-QC-005 — Candidate lifecycle

Use `candidate` for detector findings and `confirmed` after evidence. Move substantive subtitle proposals to `awaiting-approval`; after approval use `in-progress`, then `applied`, and finally `verified` after checking the disposition. Illegal time and directly provable bilingual boundary mismatch may be confirmed from event data. Semantic, sync, overlap intention, and readability generally need context/audio/video. Recheck neighbors after a timing-floor fix and record old/proposed/actual values and evidence in the same ledger row.

Zero machine candidates means only that the current rules found none, not that the work has no language or visual errors.

## SH-QC-006 — Release gate

Before presenting the release candidate require:

- complete target scope; P0 = 0; P1 = 0 or each has an explicit owner waiver with reason and impact;
- every timing-floor trigger fixed or explicitly waived with audio/visual evidence;
- explicit review of early-disappearing same-utterance candidates;
- paired Chinese/secondary boundaries equal;
- structure checks pass and every substantive change has an approved and verified ledger row;
- review, metadata, ledger dispositions, and coverage truthfully distinguish machine/human work;
- the build uses the version, filenames, header, font, credit, and previous-release contracts;
- no video, download locator, temporary comment, engineering provenance, or unauthorized credit enters release artifacts;
- the generated ZIP's name, VERSION, count, ASS markers, and checksums are reproducible and verified;
- `review.md` has been updated from proposed to actual results, including every individually listed dialogue change and each batch's actual count.

After these checks, ask for one final review of the complete candidate. Release only after the user passes it; do not insert another routine approval gate between plan approval and this final review.

Pure header/style cleanup must prove Events bytes unchanged except separately approved inline font mappings and precisely identified metadata-event removal. Remove an unused style only after closing references from Dialogue/Comment Style fields, `\r<Style>`, and the implicit `Default` style for empty Style fields. Without independent visual review, do not merge, rename, or alter retained styles.

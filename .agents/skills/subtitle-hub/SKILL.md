---
name: subtitle-hub
description: Initialize, audit, proofread, build, validate, or release Subtitle Hub projects and Chinese-primary ASS subtitles. Use for repository work involving identity, sources, translation, timing, layout, control files, or releases.
metadata:
  version: "1.4.1"
---

# Subtitle Hub

This Skill is the repository standard. Do not reconstruct rules from history or re-query external platform guides during routine work.

## Route by task

- Intake or initialization: [project-initialization.md](references/project-initialization.md).
- Translation, Chinese, terminology, plans, approval, or records: [proofreading-and-approval.md](references/proofreading-and-approval.md).
- Timing, styles, fonts, static audit, or visual review: [timing-style-and-qc.md](references/timing-style-and-qc.md).
- Workspace, candidate, promotion, package, or release: [release-and-workspace.md](references/release-and-workspace.md).

For an existing work read the nearest `series-guide.md` if present, then `project.yaml` and root `review.md`.

## Lifecycle

0. For an existing project, require project schema 9, review schema 3, and `initialization.skill_version: "1.4.1"`. If any differ, upgrade that project to the current templates before audit, editing, build, validation, or release; never execute an older contract in place. Do not upgrade dormant projects proactively.
1. Inventory the Chinese baseline and available text. Probe tracks only for supplied video. Resolve identity, scope, source roles, episode mapping, timing authority, release languages, and short name in one confirmation.
2. Dry-run internally, initialize transactionally, and pass `--ready-for-proofreading`. Ask again only if the result materially differs from the approval.
3. Audit the complete scope without editing masters. Put the categorized proposal in `review.md`, list every semantic edit separately, batch only bounded same-rule mechanical work, and pause for approval.
4. Implement the approved scope continuously, update the same rows, verify the complete Noto master, and build the candidate without routine interruptions.
5. Request one release-candidate final review. Promote only after approval.

Stop elsewhere only for a blocking identity/source-language ambiguity, material scope expansion, unresolved series term, or P1 waiver.

## Authority and boundaries

Priority: current user instruction; confirmed `project.yaml` overrides; confirmed series terminology; this Skill; the single style basis in `timing-style-and-qc.md`.

- `project.yaml` is durable project truth. `review.md` is the sole current state, proposal, decision, result, and verification surface; Git preserves closed history.
- Keep `project/sources/` immutable. Edit only workspace masters, never `subtitles/current/`.
- Review every visible Chinese event. Evidence shortage lowers the tier; sampling never proves completion. Automated findings remain candidates unless structure proves the defect.
- Use text first and media only for a concrete unresolved timing, special-subtitle, local-layout, or scene-context point. Never imply unperformed listening, viewing, or human review.
- For user-declared SSH video, use only `scripts/remote_media.py` with its isolated Paramiko 5.0.0 backend and pinned ED25519 host key. Accept the password only through its local graphical prompt; it may exist only in that Python process, never in chat, arguments, environment variables, files, or project records. Never install remote tools, upload media, write remote outputs, or broaden approved paths.
- Create paths with their first file. `temp/` permits only on-demand `tools/` and `notes/`; never create archives, logs, intermediates, screenshot trees, audit sidecars, copied shared tools, or project reports.
- Keep only `project.yaml` and root `review.md` as project control files. Intake, mappings, raw audits, frames, waveforms, and renders are disposable system-temp data.
- Keep visual evidence local. Only at explicit user request show at most two compressed screenshots for one point.

## Chinese-primary invariant

Every master and release uses `Noto Sans CJK SC/JP` globally across retained styles and nonempty inline fonts. Normalize other properties only for declared ordinary dialogue. Preserve the position, size, color, motion, karaoke, and effects of notes, signs, songs, titles, credits, broadcasts, and other special subtitles unless a concrete defect is confirmed.

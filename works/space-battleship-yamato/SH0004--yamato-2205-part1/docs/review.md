---
schema_version: 1
work_id: "SH0004"
updated_at: "2026-08-27"
baseline_release: null
target_release: "1.0.0"
overall_status: released

active_round:
  id: content-audit-20260827
  scope: "S03E01–S03E04 approved first-round audit changes and 1.0.0 release"
  status: completed

stages:
  source_inventory: verified
  baseline_setup: verified
  translation_review: candidate-review
  timing_review: candidate-review
  typography_review: verified
  visual_review: candidate-review
  release_qc: verified

episodes:
  S03E01: { status: released }
  S03E02: { status: released }
  S03E03: { status: released }
  S03E04: { status: released }
---

# 当前校对轮次

## 目标与范围

按 Skill 1.0 对 4 集中文底稿进行首轮机器结构/可读性候选检查，并用同片英文 ASS 做时间轴、分段和译义辅助比对。用户已明确批准本轮全部候选范围；E04 短句边界已由用户听审确认并记录为豁免，不自动改写其自然截断。

## 检查覆盖

- 机器检查：4 个 master 与英文参考均完成 ASS 解析；以普通中文 `常规` 和英文 `def2` 事件为语义/时间候选集合；运行 `validate_project.py --ready-for-proofreading` 通过。
- 机器结果：最新重审的 S03E01–E04 中文普通对白分别 278/284/248/309 条，英文参考分别 268/295/229/261 条；未发现 P0 非法时间。E01–E03 的 P1 为 0，E04 的 P1 仅为 `SH0004-R1-TIME-002`。详细候选见 `project/workspace/temp/review/machine-audit.tsv` 与 `pair-audit.tsv`。
- 人工覆盖：已完成项目身份、范围、来源角色和音轨选择确认；用户已听审并确认 E04 短句自然截断；另完成 E01、E04 代表性本地渲染检查。字体迁移后代表性静态渲染已在本机复核。本轮尚未完成全片听审、连续观看或逐条原语音核验，不能据此宣称翻译、同步、排版通过。
- OCR 日文：仍仅为图像疑难点参考，不作为可检索原文或批量修订依据。

## 候选修改摘要

- `SH0004-R1-TERM-001`：13 处“迪斯拉”已按系列确认术语 `YAMATO-TERM-0016` 统一为“德斯拉”。
- `SH0004-R1-SEM-001` 至 `005`：S03E01 的 5 处语义/中文表达已按获批方案实施，集中在 00:43、01:05、01:45、13:14、15:52；英文仍仅作辅助，后续原语音抽查仍可发现问题。
- `SH0004-R1-TIME-001`：S03E01 10:20–10:25 已拆为日向、飞鸟两条独立事件，采用英文参考的边界并完成邻接检查；日语音频仍是最终同步依据。
- `SH0004-R1-TIME-002`：S03E04 16:41 的 10 字中文事件虽达到 Skill 的时长候选阈值，但用户听审确认该句在原音中自然截断；原时间轴保留，无需延长或重分段。
- `SH0004-R1-TYPE-001`：已将中文/英文样式迁移至 `Noto Sans CJK SC`、日文参考样式迁移至 `Noto Sans CJK JP`；完成字体引用检查，并在 E01、E04 代表性时间点复核可见性、位置、宽度和特效。
- `SH0004-R1-MACHINE-001`：其余机器发现为 P2 可读性、标点、长时长和重叠候选；用户批准逐点复核范围，但未授权批量自动改写，现保留为后续证据驱动候选。

## 需要用户确认

无需新增确认。用户已明确批准本轮全部候选范围并授权继续处理；字体迁移已按该批准完成。该批准覆盖 `SH0004-R1-TERM-001`、`SH0004-R1-SEM-001` 至 `005`、`SH0004-R1-TIME-001` 至 `002`、`SH0004-R1-TYPE-001` 和 `SH0004-R1-MACHINE-001`；机器候选仍不等于自动改写授权。用户已确认 `SH0004-R1-TIME-002` 为原音自然截断，原时间轴保留。

## 决策与实施

已实施并记录获批的术语统一、E01 五处语义表达优化、E01 日向/飞鸟分段、普通对白的安全空格/省略号整理，以及 Noto 字体迁移。SH0004-R1-TIME-002 按用户确认改为 `waived/closed` 并保留原时间轴。首发 `1.0.0` 候选已规范化、校验并发布到 `subtitles/current/`，未创建 previous；本地不生成 ZIP。

## 验证与剩余风险

项目 readiness 与 release 校验均通过；最新机器审查中 E01–E03 为 P0/P1 `0/0`，E04 的唯一 P1 已按用户音频确认记录为 `waived/closed`。字体引用检查及 E01、E04 代表性静态渲染通过。用户已审核通过并授权发布 1.0.0；记录中的机器候选、OCR 原文限制和未进行的全片连续听审仍是覆盖说明，不被发布动作改写为虚假的全片人工覆盖。

## 用户反馈

用户确认 S03E04 `00:16:41.34–00:16:42.25` 的“哪怕就剩我一个人也要……”在原音中本来就是未说完的自然截断，原时间轴无需调整。核查音频片段仍保留在 `project/workspace/temp/review/attachments/S03E04-00-16-39.50-to-00-16-43.00-ja-audio.wav`。

代表性静态渲染已记录：E01 `project/workspace/temp/review/attachments/S03E01-00-10-24-static-noto.png`，E04 `project/workspace/temp/review/attachments/S03E04-00-16-41.70-static-noto.png`。1.0.0 发布文件位于 `subtitles/current/`，无 previous 属于首发基线的正常状态。

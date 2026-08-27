---
schema_version: 1
work_id: "SH0005"
updated_at: "2026-08-27"
baseline_release: null
target_release: "1.0.0"
overall_status: released

active_round:
  id: content-audit-20260827
  scope: "S03E05–S03E08 approved first-round audit changes and 1.0.0 release"
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
  S03E05: { status: released }
  S03E06: { status: released }
  S03E07: { status: released }
  S03E08: { status: released }
---

# 当前校对轮次

## 目标与范围

按 Skill 1.0 对 4 集中文底稿进行首轮机器结构/可读性候选检查，并用同片英文 ASS 做时间轴、分段和译义辅助比对。用户已明确批准本轮全部候选范围；已实施可由现有证据确认的术语与 E07 重复微切片处理，其余候选继续保留为逐点证据审查对象。

## 检查覆盖

- 机器检查：4 个 master 与英文参考均完成 ASS 解析；以普通中文 `常规` 和英文 `def2` 事件为语义/时间候选集合；运行 `validate_project.py --ready-for-proofreading` 通过。
- 机器结果：最新重审的 S03E05–E08 中文普通对白分别 321/308/316/336 条，英文参考分别 278/239/252/239 条；未发现 P0/P1 非法或时长底线问题。详细候选见 `project/workspace/temp/review/machine-audit.tsv` 与 `pair-audit.tsv`。
- 人工覆盖：已完成项目身份、范围、来源角色和音轨选择确认，并对获批 E07 时间链及字体迁移后的代表性渲染进行了局部本地检查；本轮尚未完成全片听审、连续观看或逐条原语音核验，不能据此宣称翻译、同步、排版通过。
- OCR 日文：仍仅为图像疑难点参考，不作为可检索原文或批量修订依据。

## 候选修改摘要

- `SH0005-R1-TERM-001`：12 处“迪斯拉”已按系列确认术语 `YAMATO-TERM-0016` 统一为“德斯拉”。
- `SH0005-R1-TIME-001`：S03E07 已处理 7 组相同文本重复微切片链，共移除 13 个冗余片段，并完成局部邻接检查。
- `SH0005-R1-TIME-002`：与上述微切片直接重叠的 10 个时长/CPS 候选已随获批链条处理；未进行阈值驱动的独立删译或广泛改轴。
- `SH0005-R1-TYPE-001`：已将中文/英文样式迁移至 `Noto Sans CJK SC`、日文参考样式迁移至 `Noto Sans CJK JP`；完成字体引用检查，并在 E07 代表性时间点复核可见性、位置、宽度和特效。
- `SH0005-R1-MACHINE-001`：其余机器发现为 P2 可读性、长时长、CPS 和标点候选；用户批准逐点复核范围，但未授权批量自动改写，现保留为后续证据驱动候选。

## 需要用户确认

无需新增确认。用户已明确批准本轮全部候选范围并授权继续处理；字体迁移已按该批准完成。该批准覆盖 `SH0005-R1-TERM-001`、`SH0005-R1-TIME-001` 至 `002`、`SH0005-R1-TYPE-001` 和 `SH0005-R1-MACHINE-001`；机器候选仍不等于自动改写授权。

## 决策与实施

已实施并记录获批的术语统一、S03E07 七组重复微切片链的合并清理，以及 Noto 字体迁移；本轮代表性静态渲染已完成。剩余 P2 候选未作批量自动改写。首发 `1.0.0` 候选已规范化、校验并发布到 `subtitles/current/`，未创建 previous；本地不生成 ZIP。

## 验证与剩余风险

项目 readiness 与 release 校验均通过；最新机器审查中 E05–E08 的 P0/P1 均为 `0/0`。字体引用检查及 E07 代表性静态渲染通过。用户已审核通过并授权发布 1.0.0；记录中的机器候选、OCR 原文限制和未进行的全片连续听审仍是覆盖说明，不被发布动作改写为虚假的全片人工覆盖。

代表性静态渲染已记录：E07 `project/workspace/temp/review/attachments/S03E07-00-18-30-static-noto.jpg`。1.0.0 发布文件位于 `subtitles/current/`，无 previous 属于首发基线的正常状态。

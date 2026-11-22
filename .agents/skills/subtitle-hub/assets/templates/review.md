---
schema_version: 3
work_id: "{{WORK_ID}}"
updated_at: "{{UPDATED_AT}}"
baseline_release: null
target_release: null
status: planning
scope: "{{SCOPE}}"

terminology_preflight:
  episodes: []
  term_ids: []
  evidence: null

coverage:
  evidence_tier: {{EVIDENCE_TIER}}
  timing_authority: {{TIMING_AUTHORITY_YAML}}
  alignment_source_id: null
  alignment_verified: pending
  master_sha256: {}
  source_sha256: {}
  chinese_in_scope: 0
  chinese_reviewed: 0
  chinese_excluded: 0
  source_in_scope: 0
  source_aligned: 0
  source_excluded: 0
  source_unresolved: 0
  static_layout_checked: 0
  human_source_fidelity_review: not-required
  human_release_review: pending
  unresolved_p0: 0
  unresolved_p1: 0

episodes:
{{EPISODES_YAML}}
---

# 当前校对轮次

## 目标与范围

已完成素材盘点、身份与命名确认、素材导入和 Noto 母本准备。按 SH-TRANS-007 完成术语表并通过内容门禁后开始逐句校对。

## 检查覆盖

- 机器检查：{{MACHINE_COVERAGE}}
- 人工确认：{{HUMAN_COVERAGE}}
- 未覆盖：字幕内容尚未进入正式校对；不得声称语言、时间轴、排版或全片观看通过

## 校对方案

尚未生成修改候选。{{INITIALIZATION_SUMMARY}} 后续在同一张表记录条目、范围、类别、修改前、建议结果、证据、风险、决定、状态、实际结果和验证。重译、删减、增译和对白改正逐条列出；只有同规则同类别的机械修改可以合并。

## 决策与实施

已实施用户批准的建项与母本准备。按证据直接完成术语表，遇到需要用户裁决的实质冲突时集中确认。

## 验证与剩余风险

项目结构、素材登记、母本存在性和解析性已验证；内容校对与发布尚未开始。

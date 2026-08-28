---
schema_version: 2
work_id: "{{WORK_ID}}"
updated_at: "{{UPDATED_AT}}"
baseline_release: null
target_release: null
overall_status: in-progress

active_round:
  id: initialization
  scope: "{{SCOPE}}"
  status: completed

stages:
  source_inventory: verified
  baseline_setup: verified
  translation_review: not-started
  timing_review: not-started
  typography_review: not-started
  visual_review: not-started
  release_qc: not-started

coverage:
  evidence_tier: {{EVIDENCE_TIER}}
  timing_authority: {{TIMING_AUTHORITY_YAML}}
  master_sha256: {}
  chinese_in_scope: 0
  chinese_reviewed: 0
  chinese_excluded: 0
  source_in_scope: 0
  source_resolved: 0
  source_unresolved: 0
  static_layout_checked: 0
  media_candidates: 0
  media_checked: 0
  human_source_fidelity_review: not-required
  human_final_playback: pending
  unresolved_p0: 0
  unresolved_p1: 0

episodes:
{{EPISODES_YAML}}
---

# 当前校对轮次

## 目标与范围

完成 Skill 1.2.0 素材盘点、身份/命名确认、素材导入和可写主稿准备。

## 检查覆盖

- 机器检查：{{MACHINE_COVERAGE}}
- 人工确认：{{HUMAN_COVERAGE}}
- 未覆盖：字幕内容尚未进入正式校对；不得声称语言、时间轴、排版或全片观看通过

## 校对方案

尚未生成字幕修改候选。{{INITIALIZATION_SUMMARY}} 后续方案须在同一张表中列出条目、范围、类别、修改前、建议修改、证据、风险、决定、状态、实际结果和验证；重译、删减、增译及对白改正逐条列出，只有同类且同规则的机械修改可以合并。

## 决策与实施

已实施用户批准的建项与基线准备，没有修改用户原始视频或字幕。下一次人工停顿只在完整校对方案提交审批时发生。

## 验证与剩余风险

项目结构、素材登记、主稿存在性和解析性已验证；发布仍处于未开始状态。

---
schema_version: 1
work_id: SH0002
updated_at: "2026-08-27"
baseline_release: 2.0.0
target_release: 2.0.1
overall_status: released

active_round:
  id: control-plane-consolidation-20260827
  scope: CONTROL
  status: completed

stages:
  source_inventory: verified
  baseline_setup: verified
  translation_review: not-applicable
  timing_review: not-applicable
  typography_review: not-applicable
  visual_review: not-applicable
  release_qc: verified

episodes:
  MOVIE: { status: released }
---

# 当前校对轮次

## 目标与范围

将拆分的项目控制面收敛为当前报告与统一台账；不修改字幕内容、发布目录或版本。

## 检查覆盖

- 机器检查：控制文件 schema、台账字段和历史条目数量迁移
- 人工检查：用户已批准控制面收敛方案
- 未覆盖：字幕语言、时间轴、排版和全片观看；本轮不作相关声明

## 候选修改摘要

本轮没有字幕候选。控制面迁移条目为 `SH0002-CTRL-20260827`；统一台账迁移后共 32 条。

## 需要用户确认

无；用户已于 2026-08-27 明确批准实施本次改进。

## 决策与实施

- 用 `docs/review.md` 取代 `docs/progress.yaml` 和逐轮临时报告。
- 用 `docs/ledger.tsv` 取代 `docs/issues.tsv` 与 `docs/change-log.tsv`。
- 历史条目保留原 ID 和事实；没有记录过的历史审批使用 `not-recorded`，不补造授权。

## 验证与剩余风险

迁移已完成：初始化行为测试、Skill 链接与规则 ID 检查、统一台账 schema、三个项目发布验证和分发包检查均通过；字幕文件未改动。历史审批未记录的条目继续明确标记为 not-recorded，不据此推断人工批准。

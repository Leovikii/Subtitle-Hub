---
schema_version: 1
work_id: SH0003
updated_at: "2026-08-27"
baseline_release: 2.0.0
target_release: 2.0.1
overall_status: released

active_round:
  id: skill-1.0-finalization-20260827
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
  S02E01: { status: released }
  S02E02: { status: released }
  S02E03: { status: released }
  S02E04: { status: released }
  S02E05: { status: released }
  S02E06: { status: released }
  S02E07: { status: released }
  S02E08: { status: released }
  S02E09: { status: released }
  S02E10: { status: released }
  S02E11: { status: released }
  S02E12: { status: released }
  S02E13: { status: released }
  S02E14: { status: released }
  S02E15: { status: released }
  S02E16: { status: released }
  S02E17: { status: released }
  S02E18: { status: released }
  S02E19: { status: released }
  S02E20: { status: released }
  S02E21: { status: released }
  S02E22: { status: released }
  S02E23: { status: released }
  S02E24: { status: released }
  S02E25: { status: released }
  S02E26: { status: released }
---

# 当前校对轮次

## 目标与范围

完成仓库级 Subtitle Hub Skill 1.0 的媒体探测、命名审批、事务建项、就绪验证与目录同步闭环；迁移本项目描述符但不修改字幕、发布目录或版本。

## 检查覆盖

- 机器检查：27 项隔离行为测试、schema 6 项目检查、当前/上一发布检查、打包检查与派生目录检查
- 人工检查：用户已批准完成 Skill 1.0 迁移与既有项目描述符升级
- 未覆盖：字幕语言、时间轴、排版和全片观看；本轮不作相关声明

## 候选修改摘要

本轮没有字幕候选。Skill 1.0 完成条目为 `SH0003-SKILL-100-20260827`。

## 需要用户确认

无；用户已于 2026-08-27 明确批准持续实施至完整可用的 1.0。

## 决策与实施

- 将项目描述符升级为 schema 6，登记既有短项目名、审批来源、Skill 版本与 `target-video` 映射。
- 新建项统一为主动媒体探测、阻塞问题解决、素材/集映射审批、短项目名审批、dry-run、事务创建和就绪验证。
- 根目录目录文件改为从已发布 `project.yaml` 派生；仍只维护现有四个项目控制文件。

## 验证与剩余风险

Skill 1.0 验证已通过，当前和 previous 发布内容未改变。历史项目未保留 Bangumi 首播日期，继续以 `released-existing` 警告表示，不从其他字段推定；本轮未覆盖字幕语言、时间轴、排版或全片观看。

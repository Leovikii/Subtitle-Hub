---
schema_version: 1
work_id: SH0002
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
  MOVIE: { status: released }
---

# 当前校对轮次

## 目标与范围

完成仓库级 Subtitle Hub Skill 1.0 的媒体探测、命名审批、事务建项、就绪验证与目录同步闭环；迁移本项目描述符但不修改字幕、发布目录或版本。

## 检查覆盖

- 机器检查：27 项隔离行为测试、schema 7 项目检查、当前/上一发布检查、打包检查与派生目录检查
- 人工检查：用户已批准完成 Skill 1.0 迁移与既有项目描述符升级
- 未覆盖：字幕语言、时间轴、排版和全片观看；本轮不作相关声明

## 候选修改摘要

本轮没有字幕候选。Skill 1.0 完成条目为 `SH0002-SKILL-100-20260827`。

## 需要用户确认

无；用户已于 2026-08-27 明确批准持续实施至完整可用的 1.0。

## 决策与实施

- 将项目描述符升级为 schema 7，统一保存身份、素材、样式 profile、持久限制与项目覆盖项。
- 新建项统一为主动媒体探测、阻塞问题解决、素材/集映射审批、短项目名审批、dry-run、事务创建和就绪验证。
- 根目录目录文件改为从 `project.yaml` 派生；项目只维护 `project.yaml` 与根目录 `review.md` 两个控制文件。

## 验证与剩余风险

Skill 1.0 验证已通过，当前和 previous 发布内容未改变。历史项目未保留 Bangumi 首播日期，继续以 `released-existing` 警告表示，不从其他字段推定；本轮未覆盖字幕语言、时间轴、排版或全片观看。

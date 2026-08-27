---
schema_version: 1
work_id: "SH0005"
updated_at: "2026-08-27"
baseline_release: "1.0.0"
target_release: "1.0.1"
overall_status: in-progress

active_round:
  id: dialogue-style-1.1-20260827
  scope: "S03E05–S03E08 ordinary Chinese dialogue style normalization"
  status: awaiting-review

stages:
  source_inventory: verified
  baseline_setup: verified
  translation_review: not-applicable
  timing_review: not-applicable
  typography_review: candidate-review
  visual_review: not-started
  release_qc: not-started

episodes:
  S03E05: { status: released }
  S03E06: { status: released }
  S03E07: { status: released }
  S03E08: { status: released }
---

# 当前校对轮次

## 目标与范围

按 Skill 1.1 修复 1.0.0 普通中文对白紧贴底边的问题。范围只包括四集 `常规` 样式定义及其 1281 条引用事件；本项目没有可发布副语，按单中文字幕高度处理。不改对白文字、时间轴、事件样式名或特殊字幕。

## 检查覆盖

- 机器检查：四个 master 的 PlayRes 均为 1920×1080；`常规` 均为 Noto Sans CJK SC 55、底部居中、左右/底边距 10、描边/阴影 2/2。
- 引用范围：S03E05 321、E06 308、E07 316、E08 336，共 1281 条。
- 未覆盖：尚未修改 master、构建 1.0.1 或执行发行前人工终审；本轮不声明排版通过。

## 校对方案

| item_id | 类别 | 范围 | 修改前 | 建议修改 | 依据与风险 |
| --- | --- | --- | --- | --- | --- |
| `SH0005-STYLE-110-001` | 正文样式（同类机械批次） | S03E05–E08 `常规` 样式，1281 条引用；排除电文、标题、episode、ED、staff、`005`、歌曲及所有定位/特效事件 | Noto Sans CJK SC 55；Alignment 2；MarginL/R/V 10/10/10；Outline/Shadow 2/2 | 单中文基线：字号 62；Alignment 2；MarginL/R/V 96/96/70；白字；不透明近黑描边 3；Shadow 0；其余字段与事件不变 | `SH-LAYOUT-005`；改善底部安全区和正文一致性。风险是长句宽度变化，只在实施后做溢出扫描并纳入发行前终审，不另设截图审批。 |

## 需要用户确认

请确认是否批准 `SH0005-STYLE-110-001`。批准后将连续修改、做结构/溢出检查、构建 1.0.1，并只在完整发行候选终审时再次暂停。

## 决策与实施

待批准，master 和 `subtitles/current/` 均未修改。

## 验证与剩余风险

1.0.0 仍是当前发布。Skill 1.1、目录清理和项目描述符验证已完成且未改变任何字幕/master/发布文件。方案获批后的最终终审将重点检查长句、明暗场景可读性和底部安全距离；不会批量生成截图。

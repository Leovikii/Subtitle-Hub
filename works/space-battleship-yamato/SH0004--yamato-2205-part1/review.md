---
schema_version: 1
work_id: "SH0004"
updated_at: "2026-08-27"
baseline_release: "1.0.0"
target_release: "1.0.1"
overall_status: released

active_round:
  id: dialogue-style-1.1.0-20260827
  scope: "S03E01–S03E04 ordinary Chinese dialogue style normalization"
  status: completed

stages:
  source_inventory: verified
  baseline_setup: verified
  translation_review: not-applicable
  timing_review: not-applicable
  typography_review: verified
  visual_review: final-review-passed
  release_qc: verified

episodes:
  S03E01: { status: released }
  S03E02: { status: released }
  S03E03: { status: released }
  S03E04: { status: released }
---

# 当前校对轮次

## 目标与范围

按 Skill 1.1.0 修复 1.0.0 普通中文对白紧贴底边的问题，并清理 workspace 中不会进入发布 Events 的旧署名/免责声明事件。样式范围只包括四集 `常规` 定义及其 1119 条引用；事件清理范围为与 1.0.0 当前发布逐条比对后确认多出的 29 条署名/免责声明事件。不改实际对白文字、对白时间轴、事件样式名或特殊字幕。

## 检查覆盖

- 机器检查：四个 master 与候选均为 1920×1080；`常规` 已统一为 Noto Sans CJK SC 62、底部居中、左右/底边距 96/96/70、描边/阴影 3/0。
- 引用范围：S03E01 278、E02 284、E03 248、E04 309，共 1119 条。
- 实施结果：`常规` 长句按既有 ASCII 语义空格在 72 条事件中插入 `\\N`；清理 29 条已与 1.0.0 对齐的发布署名/免责声明事件；对白时间和可见文字保持等价。
- 本地视觉抽查：已在目标视频本地渲染检查 S03E01 00:02:42.34 与 S03E04 00:06:08.52（明暗背景候选效果），未生成对话附件。
- 宽度候选：仍有 101 条 `常规` 事件超过 16 CPL 等效阈值，包含无安全断点或已有多行事件；未擅自删减、改译或强制三行化，列为发行前人工终审风险。

## 校对方案

| item_id | episode/time or bounded scope | category | before | proposed result | evidence/rationale | severity/risk | decision | status | actual result | verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SH0004-STYLE-110-001` | S03E01–E04 `常规` 样式及其 1119 条引用；排除背景、广播、画中字、标题、staff、注释、歌曲及所有定位/特效事件 | 正文样式 | Noto Sans CJK SC 55；Alignment 2；MarginL/R/V 10/10/10；Outline/Shadow 2/2 | 字号 62；Alignment 2；MarginL/R/V 96/96/70；白字；不透明近黑描边 3；Shadow 0；其余字段与事件不变 | `SH-LAYOUT-005`；修复正文贴近底边并统一 1920×1080 单中文字幕基线。 | P2；长句宽度变化须扫描，风险限于排版，不涉及文本/时间轴 | approved（用户本轮要求按 Skill 1.1.0 优化） | verified | 已按方案实施 | 候选宽度、结构和本地视觉检查已完成 |
| `SH0004-STYLE-110-002` | S03E01–E04 `常规` 事件中超过 16 个全角等效宽度、且已有单个 ASCII 空格可作为语义停顿的位置 | 普通对白分行（确定性排版批次） | 长句保持单行，部分事件在新字号下超过 16 CPL | 仅在已有 ASCII 空格处插入一个 `\\N`，选择两行均不超过 16 CPL 的最平衡断点；不改可见文字、时间、样式或已有多行事件 | `SH-TIME-003`、`SH-TIME-005`；以现有译文的语义空格作为候选断点。无法安全分行的残余仅记录，不自动改写 | P2；分行可能影响阅读节奏，残余需人工判断 | approved（用户本轮要求按 Skill 1.1.0 优化） | verified-with-residuals | 已按方案实施 | 事件文本等价、宽度及本地视觉检查已完成 |
| `SH0004-REL-110-001` | S03E01–E04；与 1.0.0 当前发布逐条比对多出的 29 条 `staff`/`staff0` 署名及 S03E04 单条字幕组免责声明事件 | 发布元数据事件删除（确定性批次） | workspace 中存在署名、空署名尾段及“本字幕由……制作上传/仅供观看/禁止用于商业活动”事件；1.0.0 当前发布不含这些事件 | 从 master 与候选中删除这 29 条发布署名/免责声明 Events；保留署名到 canonical `Subtitle-Hub-Source-Credit` 头字段的既有发布边界 | `SH-REL-004`、`SH-REL-002`；仅删除与当前发布的差异中可识别的发布来源事件，不删除对白 | P1 release-boundary cleanup；`005`/staff 特殊事件需逐条核对 | approved（用户本轮要求按 Skill 1.1.0 优化） | verified | 已按方案实施；修复发行产物时恢复 1.0.0 原始署名到 master 与 1.0.1 头字段 | 候选事件序列、样式引用及 8 个当前 ASS 的署名字段检查已通过 |

## 需要用户确认

用户已于 2026-08-27 通过完整 1.0.1 发行候选，批准发布。

## 决策与实施

已完成清理已核实的 29 条发布元数据事件、样式统一及 72 条确定性分行；此前误遗漏的 1.0.0 原始署名已恢复到 master 与 1.0.1 当前 ASS 的 `Subtitle-Hub-Source-Credit` 头字段。未恢复署名 Events。

## 验证与剩余风险

1.0.1 当前 ASS 已完成署名修复，1.0.0 仍保存在 `subtitles/previous/`。101 条宽度候选按用户终审接受并保留为后续优化线索；本轮未作未经证据支持的重译或强制三行化。视觉核对仅在本地按候选时间点完成，未批量生成或发送截图。

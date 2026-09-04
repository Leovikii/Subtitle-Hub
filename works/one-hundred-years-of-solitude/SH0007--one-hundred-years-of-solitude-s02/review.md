---
schema_version: 3
work_id: "SH0007"
updated_at: "2026-09-05"
baseline_release: "1.0.1"
target_release: "1.0.2"
status: released
scope: "S02E01-S02E08"
coverage:
  evidence_tier: A
  timing_authority: "S02E01-S02E08=embedded Simplified Chinese subtitle track"
  alignment_source_id: optional-source-001
  alignment_verified: verified
  master_sha256:
    S02E01: 2d0028efae3db1adb1dfaa9ee03aa5b20e0f637b3422ba4b7fd3619707f6b4aa
    S02E02: f3cf71528d208284bc7f70e38a1b1bff6b434801c49109bb581fba392f05916b
    S02E03: 21a52905ab7fffde9cfe40c8b9e1c9580e092f9573bbdefda763807af37763f2
    S02E04: 15fb76d3375a210acae6bb77027cb3d890a41ba973756bc692f9fee70d5db902
    S02E05: 2dee7a50ae9a3d17b9f3d0bb2cabe9a3179ec3d77203d777fe379d6bf6567197
    S02E06: 5634726476d8da9496c6b0c54335fc5d95550e92c603510f82af6ec5ae998905
    S02E07: c3437abba4b9fb3548eaf90a07f8c99bc6a179ce89d090828dad770dfd3ecc90
    S02E08: 444b5bcfa6e4a2cf89e3c25b83cf581391d098168ff23dde87ac4a3523328b53
  source_sha256:
    S02E01: 52197d49d77e02e92298349c9ab8fb7f32eabdf5e115501bd7f59fc2c309f196
    S02E02: d812e13ee5205cbc44a98ac206f7a9a0dadd9c5c57de9c2248ed02a46472e659
    S02E03: 9d523685f9bde932a000e491bfd48e2f20d327da6ac016b8ceabf9063767d674
    S02E04: 895258b40c21eb65a7fbb3ef4c43e9a0afcc579fb10858a5ad7b31832a379d61
    S02E05: 93de44c6f8e76438c9b214aadb41c7835e02de9984a0e1aadcbc71087926c8b5
    S02E06: 77c86978680529c8389680ead142c6abeade9d356478feb44252f6359a7b1242
    S02E07: d0c2c24787dd2cd3e3261238da983a40bdb9289d7f014786d602583bf8fa5178
    S02E08: f07659c51a40338c4130792f0f39faba959f5618b92b7c8c0e476a99ebd8e9f6
  chinese_in_scope: 4409
  chinese_reviewed: 4409
  chinese_excluded: 0
  source_in_scope: 4590
  source_aligned: 4352
  source_excluded: 238
  source_unresolved: 0
  static_layout_checked: 8999
  human_source_fidelity_review: not-required
  human_release_review: verified
  unresolved_p0: 0
  unresolved_p1: 0
episodes:
  S02E01: { status: released, chinese_units: 501, source_units: 520 }
  S02E02: { status: released, chinese_units: 498, source_units: 522 }
  S02E03: { status: released, chinese_units: 513, source_units: 561 }
  S02E04: { status: released, chinese_units: 514, source_units: 554 }
  S02E05: { status: released, chinese_units: 543, source_units: 609 }
  S02E06: { status: released, chinese_units: 599, source_units: 680 }
  S02E07: { status: released, chinese_units: 517, source_units: 546 }
  S02E08: { status: released, chinese_units: 724, source_units: 804 }
---

# 当前校对轮次

## 目标与范围

将《百年孤独 第二季》S02E01–S02E08 从 `1.0.1` 更新为 `1.0.2`，修复 `ES-Main-2L` 在超宽播放画布中未自动换行而落位过低的问题，同时保持普通中西字幕逐条同轴。

## 检查覆盖

- 全季共有 789 条 `ES-Main-2L`：E01 75、E02 75、E03 100、E04 78、E05 83、E06 131、E07 75、E08 172；现状均无显式 `\\N`，完全依赖播放器自动换行。
- 用户截图中的 E05 00:05:52.25 为直接证据：长西语在超宽画布上渲染为单行，但仍使用低位 `ES-Main-2L`（MarginV 5），相对标准 `ES-Main`（MarginV 18）低 13 个脚本单位。
- 本轮不改字幕文本含义、时间轴、中文、特殊字幕、字号、颜色或特效；只确定普通西语的行数和分行点。

## 校对方案

| item_id | 范围 | 类别 | 修改前 | 建议结果 | 证据与边界 | 风险 | 决定/状态 | 实际结果/验证 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| LAYOUT-001 | 全季初始 789 条 `ES-Main-2L`，加审计发现的 139 条自动换行风险，共 928 条 | 普通双语布局 | 低位样式依赖自动换行；超宽画布可能退化为低位单行，标准画布另有单行样式自动换行风险 | 在自然空格处加入显式 `\\N` 并均衡分行；标准双行使用 `ES-Main-2L`，极长句用紧凑/窄体双行；使行数不随画布变化 | 用户已批准进入 1.0.2 优化；截图确认条件性缺陷；显式换行避免宽画布退化及意外第三行 | P1 | approved / verified | implemented / 913 条标准双行、14 条紧凑双行、1 条八次口号窄体双行；均恰好两行 |
| LAYOUT-002 | 全季最终 3,424 条 `ES-Main` | 普通双语布局 | 标准单行样式 | 保持单行且无显式 `\\N`；保留 MarginV 18 | 维持统一单行基线，避免无必要的低位样式 | P1 | approved / verified | implemented / 3,424 条固定单行，自动换行风险 0 |

## 决策与实施

用户已于 2026-09-05 明确同意进入 `1.0.2` 优化；本轮机械布局方案已按批准范围实施，只编辑工作母本，不直接编辑 `subtitles/current/`。新增普通样式 `ES-Main-2L-Compact`（14 条，极长双行）与 `ES-Main-2L-Narrow`（1 条八次重复口号），均保持 Noto 字体与低位双行基线。

## 验证与剩余风险

- 全量事件不变量通过：相对 `1.0.1`，4,352 条普通西语文本（忽略新增换行控制符）、4,352 对中西时间、全部中文、`CN-Special`、`ES-Special` 及事件数均零变化。
- 全量静态审计覆盖 8,999 个渲染事件：confirmed=0、risk=0、media-required=0；无自动第三行、无低位单行、无中西空间碰撞。
- `1.0.2` 完整候选已构建到 `project/workspace/build/current-candidate/`，共 8 个 ASS 与 VERSION；Noto 字体、结构、master-render invariant、项目验证及本地 package-plan check 均通过。构建器仅在未引用的分集删除紧凑样式定义，不改变渲染结果。
- 用户已于 2026-09-05 完成发行前终审并批准发布与推送；`1.0.2` 候选已晋升为当前发行版，本地不写 ZIP。

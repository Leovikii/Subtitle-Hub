---
schema_version: 3
work_id: "SH0007"
updated_at: "2026-09-05"
baseline_release: "1.0.0"
target_release: "1.0.1"
status: released
scope: "S02E01-S02E08"
coverage:
  evidence_tier: A
  timing_authority: "S02E01-S02E08=embedded Simplified Chinese subtitle track"
  alignment_source_id: optional-source-001
  alignment_verified: verified
  master_sha256:
    S02E01: 42ad863fa5b72411af1137845fbcdc29b27bd6a2975bbb4c5ef1e5800cf8ac12
    S02E02: 297166ca78091e97952a9bbac5c4e56b54508abe3e02f7ce8f357e26172d8fa3
    S02E03: 83ed99e3439fc917570cf8c177956568e3b7e071e5e81674b985ca53f78a67ee
    S02E04: 3df997e5309248b03ab26239616f448440fc2c05722bef9370d560eb67d535ce
    S02E05: 36d5e8dfc717f9100ac993afb31490ef90c1c5448fb535c287c8653023f2f196
    S02E06: dd489e38b1f239e9fa250bc6a726b6754ea95217e1e670c40d3c8bdc974f18bf
    S02E07: 5109e623666aac4627b56c6130b85bd98cb5c228b345377a63d4c2204a182d4d
    S02E08: 9a44e31cb2023b19d910d35b67710250646bfde791d97bcf75e2e7a99383eb05
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

将《百年孤独 第二季》S02E01–S02E08 从 `1.0.0` 更新为 `1.0.1`。修复普通中西正文出现和消失时间不一致的问题；继续以同切版内嵌简体中文字幕为唯一时间轴权威。

## 检查覆盖

- 已重新检查 8 集全部普通正文时间关系：中文普通事件 4,352 条，西语普通事件 4,558 条，组成 4,158 个既有审核语义组。
- 4,158 组包括 3,187 个 `1:1` 以及 971 个 `1:N`、`N:1` 或 `N:M`；仅 436 个 `1:1` 已有完全相同的起止时间，其余普通配对需要同步。
- 57 条 `CN-Special` 与 238 条 `ES-Special` 属特殊内容，不纳入普通正文同轴改写，其文本、时间和特殊属性保持不变。
- 本轮不改中文文本、中文时间、译名或特殊字幕，不执行 ASR、VAD、OCR 或全片媒体处理。

## 校对方案

| item_id | 范围 | 类别 | 修改前 | 建议结果 | 证据与边界 | 风险 | 决定/状态 | 实际结果/验证 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TIME-001 | 全季 4,352 条中文普通正文及 4,558 条西语来源单位 | 双语时间轴/分段 | 普通中西事件沿用各自来源边界，出现/消失存在差异 | 以每条中文普通事件为显示单元；在每个既有审核语义组内按原顺序重分段西语，使西语普通显示事件数与中文相同，并逐条采用对应中文起止时间；中文与特殊字幕不变 | 用户明确指定中文时间轴为标准；`SH-TIME-004` 将中西边界或分段不匹配列为 P1；只在已审核语义组内合并/拆分，不跨组、不增删源文意义 | P1；须验证文本守恒、逐条同轴、可读性和无碰撞 | approved / verified（用户 2026-09-05 明确要求） | implemented / 4,352 对普通中西事件全部逐条同轴；中文及特殊事件零变化；仅 E05 一处单词级 `N:1`（`Aureliano.`）为保持中文两段权威时间，在连续两段重复显示同一姓名 |

## 决策与实施

用户已明确批准 `TIME-001`。已只修改 `project/workspace/episodes/*/master.ass`：4,558 个西语来源单位在 4,158 个审核语义组内重分段为 4,352 个普通显示事件，与 4,352 条中文普通正文逐条同轴；中文正文、`CN-Special`、`ES-Special` 均与 `1.0.0` 完全一致。

## 验证与剩余风险

- 同轴验证通过：4,352 对普通中西事件起止时间完全相同，时间不匹配 0；每条中文普通正文均有且仅有一条西语正文。
- 文本与边界验证通过：中文正文及全部特殊事件相对 `1.0.0` 零变化；西语顺序和文字守恒，只有 E05 一处极短 `N:1` 姓名按上表说明重复显示。
- 全量静态审计覆盖 8,999 个渲染事件：confirmed=0、media-required=0；928 个 predicted-wrap 均由普通西语 2L 样式承接，不构成中西空间碰撞。Noto 字体、ASS 结构及候选 master-render invariant 通过。
- 用户已于 2026-09-05 完成发行前终审并批准发布与推送；`1.0.1` 候选已晋升为当前发行版，本地不写 ZIP。

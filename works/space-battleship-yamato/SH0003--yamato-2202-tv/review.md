---
schema_version: 3
work_id: SH0003
updated_at: "2026-08-31"
baseline_release: 2.0.1
target_release: 2.0.2
status: released
scope: S02E01-S02E26

coverage:
  evidence_tier: A
  timing_authority: target-video-ssh-probed
  master_sha256:
    S02E01: e2fd225d4550a6c612bf294d3972b470f5629aac559ba7aa10033a3f158bd5b6
    S02E02: af2d985dfe3d7ff8a14063037d8416e8e00345344f721ea6d119de807e7e599c
    S02E03: 4c78b62720de8ff333aea9f47f53863ad88ae02a95cfaf35132df4199f11af6a
    S02E04: 529a47ca7866e632ad80d13e46d8217441d12c80da23bcdfdb3688cd4f61c4f1
    S02E05: 127ae7e9fc72bf4a27d49bcc31f2b1931c8ba148ece050c78907a030e8ff76b3
    S02E06: ecd0532007308206146122b811dbc6a506c4b67c3c9683fdbd416defcf6bd80a
    S02E07: fa53c45355e696aa303c171ff313f1a0a65d825c5a9ad0a8d6e34a5672820e89
    S02E08: d74e7de6de7c8ea050ae482717474c51f91e21a69c09142695a450c374be51d0
    S02E09: 798579b975236f7abb7526959d0a6ced74c650c922d3b167facaeca4c349f8e9
    S02E10: 35f3aa36dce3bb48e3e7eaf46c677d3cd73308c39f0e5cbf011a801ecfd8b096
    S02E11: 268f06327ecac5381ce6bc7ee8957e3ce0a3c34614e398ce03cc81ac5a4003c6
    S02E12: 1b9ca104adcca02ed0720a628ca9b00350e712c029c396f0a1925983db2d9172
    S02E13: be59b21b8e59b7dd118421c249f25632c5d4f8b40b5846d9fd1861e56dc3a549
    S02E14: debfe7ac662448e7885ea1fdd874b49919064740dee3f533aeeaf97f3adf28a9
    S02E15: d3bd87bd2ef08e59c84e4f9ae9fc772301921a3355734b993ba137b77e321529
    S02E16: d6d9e2decc6d77b51dff30c2cdbe2723900a6d684ac5b2702dfd8cc42679b95f
    S02E17: 6d30da14af0ccea05d40cd5ecea589601a3f8a04b820cd8980637467cd832de1
    S02E18: fa9169fe2806f2c4073f77bc933e1b88000bebc99aa9d7625b7c5c3dedb01de7
    S02E19: 0279474705493155e22b3f3848acdf3b751ece36ab64777d5a21184c2564a7a0
    S02E20: 36247bfcdc72171fc6b958d290dc2e68312511daf7d9d090f0f7d49772c35537
    S02E21: 1ea94638bd23428a7f030d38bb307f4a81b3ab7b4b9dc03fea1b79d2f8ba0dbb
    S02E22: 20e429aa27ecc0e2e3441df9e50e8213b44033c1bf4115245ba99576022e9278
    S02E23: 20470b7cf7133098ae98a71fbd41ea3bb6d6671be6518d9f095b144a8fbfa4ed
    S02E24: 03a49fe65111d7f08a3352af609a5cbcb57fd07a0e72a9b7434479e09e0ebe2b
    S02E25: 3adf8090c9d2994de93ab628bc1316153132024293eac5ca4eb635638ee23b50
    S02E26: 2dc6678c36decff72c64c9f3a1ecc5b0c20fbdb6dede2280cbd7dd0eca91c33e
  chinese_in_scope: 11317
  chinese_reviewed: 11317
  chinese_excluded: 0
  source_in_scope: 5766
  source_aligned: 5766
  source_unresolved: 0
  static_layout_checked: 12042
  human_source_fidelity_review: targeted-only; full-meaning-review-not-claimed
  human_release_review: verified
  unresolved_p0: 0
  unresolved_p1: 0

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

以 2.0.1 当前发布为基线，对《宇宙战舰大和号2202 爱的战士们》全 26 集进行新一轮中文字幕校对，目标发行版本为 2.0.2。保留日文副字幕和既定双语发布契约；仅在本方案获批、证据支持后修改工作区母本。

## 检查覆盖

- 机器检查：26 个 master 共 12,044 个 Event；6,417 个可见中文字幕和 6,101 个源语文本单位纳入范围；12,044 个 Event 已完成 ASS、时间码、字体、样式引用、静态布局和中日事件关系候选审计。
- 候选统计：中文无重叠源语 977 条、源语无重叠中文 8 条、短时长 14 条（7 个中日配对）、越界风险 295 条、空间碰撞风险 82 条、四行显式换行风险 1 条；这些均是候选，不等同于语义或画面缺陷。
- 文本证据：日文官方 WEBrip CC 为源文本，英文嵌入字幕为辅助翻译/时间/布局参考，系列术语表为已确认术语依据。术语声明形式的禁用命中为 0。
- 媒体检查：SSH 用户 `Viki` 及主机指纹 `SHA256:/2UaP4O8ZNJD+DbiaxNTSKqRey/5u1WfcYbbzHPXrKU` 已固定；Season 2 - Star Blazers 2202 Warriors of Love 的 26 个目标视频均已映射并完成只读轨道探测。已对关键复制候选取得局部画面/嵌入字幕证据，但未作全片播放声明。
- 未覆盖：全片播放/听辨未执行；本轮不将机器事件配对表述为全片人工源语复核，未确认的启发式时长/布局候选按限制保留。

## 漏检复盘（本轮诊断）

S02E17 的错误没有被上一轮候选扫描发现，原因不是源语证据缺失，而是检查层级不足：`audit_subtitle.py` 只按语言类别、时间重叠、结构和静态几何产生候选；相邻重复扫描只比较相邻中文字符串是否完全相同。Event 93 与 Event 94 的中文字符串不同，因此不会进入“完全重复”候选；Event 94 又与同时间段的日文事件重叠，所以会被记录为“按时间已配对”，但时间重叠不代表语义对应。本轮已把逐事件双向事件闭合和近邻意义错配作为人工优先核对项，并修正该事件；覆盖数字已按最终母本复算，仍不把机器配对等同于全片人工听辨。

本例暴露的 Skill 修补点是强制逐事件双向语义闭合：每个中文事件必须关联日文事件并检查说话者、动作、对象、否定、数量、因果、语气、遗漏和新增；每个日文事件必须反向关联中文事件；另加“中文虽不同但与相邻/近邻源语意义不对应”的候选类别。完全重复检测只能作为第一层，不得作为源语忠实度检查的替代。对于用户特别指出的自动化双语合并风险，应将“上下中文完全相同且相邻日文不同”列为 P1 优先候选，并在检查中保留其相邻事件上下文。

## 校对方案

| item_id | episode/time or bounded scope | category | before | proposed result | evidence/rationale | severity/risk | decision | status | actual result | verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SH0003-CONTRACT-202-001` | 项目控制面 | Skill 契约迁移 | 旧轮次控制面 | schema 9 / review 3；目标版本 2.0.2 | `SH-INIT-010`、`SH-CTRL-003`；不改变字幕内容 | P1 workflow gate | approved（按本次任务执行） | verified | 已完成 | `validate_project.py --ready-for-proofreading` 通过，仅保留历史日期警告 |
| `SH0003-FONT-202-001` | S02E01–S02E26 全部 master | 全局字体机械规范 | 旧字体及混合内联字体 | 仅按 `SH-LAYOUT-004` 统一为 Noto Sans CJK SC/JP | 当前 Skill 的全局字体规则；不改变文字、时间、样式或特效 | P1 rendering consistency | approved（按当前 Skill 必需） | verified | 26 个 master 已完成机械迁移 | 母本字体扫描通过；candidate 尚待构建 |
| `SH0003-AUDIT-202-001` | S02E01–S02E26 全范围 | 全量静态质量审计 | 2.0.1 无本轮完整审计结论 | 保留候选并按本表逐项处理；不批量改写 | `SH-QC-009`、`SH-QC-003`；结构证明与启发式风险分开记录 | P1/P2/P3 依确认结果 | approved（用户授权直接完成本轮） | verified | 26 个母本共 12,042 个 Event 完成 ASS、时间码、字体、样式引用和静态布局审计；0 confirmed、1,361 risk、14 media-required | 最终 `audit_subtitle.py` 结果已复算；机器结果不替代全片播放或听辨 |
| `SH0003-MEDIA-202-000` | 用户指定 SSH 目录 `/srv/dev-disk-by-uuid-60648e5c-2568-40fd-b0f1-bf799dba4b94/Anime/Uchuu Senkan Yamato 2199 (Star Blazers Space Battleship Yamato 2199)/Season 2 - Star Blazers 2202 Warriors of Love/` | 视频路径/轨道探测 | 根目录 `discover` 返回 0 个可识别视频；准确 Season 2 目录此前未知 | 使用用户提供的准确目录和 `remote_media.py`；保持 SSH 文件映射为本机忽略数据，不修改 NAS | `SH-QC-010`；26 个文件与 S02E01–S02E26 一一对应 | P1 workflow gate | approved（按用户指定路径继续） | verified | Season 2 已发现 26/26；全部为 1920×1080 AV1、2–3 条 Opus 音轨、2 条 ASS 字幕轨；默认日语音轨和英文 Dialogue 轨，时长探测通过 | 26 个 `probe` 结果、`validate_project.py --ready-for-proofreading` 通过；仅作轨道/时长核验，未作全片播放声明 |
| `SH0003-TERM-202-001` | S02E01–S02E26；系列术语 `YAMATO-TERM-0001`–`0021` 的已声明字面形式 | 术语闭合审计 | 已确认形式尚未与本轮人工源语复核合并 | 逐实体核对全范围短名、称谓和派生词；只改证据确认的上下文，不做子串替换 | `SH-TRANS-007`、`SH-TRANS-010`；禁用形式命中 0，但机器扫描不能解决实体歧义 | P1/P2 | approved（按用户授权直接完成本轮） | verified | 已声明术语的禁用字面命中为 0；本轮未引入新的专名形式 | 全范围字面扫描；结论限于已声明形式，不宣称发现未知别名闭合 |
| `SH0003-ALIGN-202-001` | S02E01–S02E26；11,317 中文 / 5,766 源语单位 | 全范围源语对照 | 只有时间重叠候选；中文无源语重叠候选 975 条、源语无时间重叠候选 8 条 | 按日文官方 CC 为主、英文为辅完成双向事件闭合；对说话者、动作、对象、否定、数量、因果、语气、分段和时间保留高风险语义修订 | `SH-TRANS-008`、`SH-TRANS-001`；英文仅作辅助，不以多数译本裁决 | P1/P2 | approved（用户已授权直接完成本轮） | verified | 11,317 个可见中文事件完成文本/结构核对；5,766 个源语单位均已归入对应中文、跨事件配对或保留的非中文口令事件；确认的语义修改已逐条列出 | 最终 master 审计：12,042 Events、0 confirmed；8 个 `ワープ！` 与保留的 `WARP！` 对应，非漏译 |
| `SH0003-ALIGN-202-002` | S02E17 `00:05:01.46–00:05:07.54`；CN Event 94 / `JP-SYNC-0046` | 源语—中文语义错配/上一句意义复制 | `伤员经历连续跃迁一定很痛苦吧？`；上一条 CN Event 93 已表达连续跃迁对伤员的影响；日文为 `医療室に行けばいいのに 自分から こんな所に… バカみたい` | 改为 `明明去医务室就好了 却自己跑到这种地方来……像个傻瓜似的`，保留停顿和贬语语气；不得沿用上一条“连续跃迁”意义 | `SH-TRANS-001`、`SH-TRANS-002`、`SH-TRANS-008`；工作区母本、JapaneseAux 和官方日文 CC 均确认当前事件内容不对应；附图为用户提供的单点证据 | P1 | approved（用户授权直接完成本轮） | verified | 已按日文改为 `明明去医务室就好了 却自己跑到这种地方来……像个傻瓜似的` | 对照前后事件、JapaneseAux 和官方日文 CC；已复查目标点，不宣称全片听辨 |
| `SH0003-SPECIAL-202-001` | S02E01–S02E26；Title、OPED、ScreenTextCN、TranslatorNote 等特殊事件 | 特殊字幕规范审查 | 特殊字幕存在歌曲、片头片尾、标题、画中文字、注释及动画效果；机器布局候选不能直接视为错误 | 按 `SH-LAYOUT-003` 保留位置、字号、颜色、运动、卡拉 OK 和效果；只有确认遮挡、越界、不可读或源文错误时逐事件修正；全局字体规则除外 | 用户明确要求；`SH-LAYOUT-003`、`SH-LAYOUT-004`；特殊字幕不套用普通对白基线 | P1/P2/P3 依具体证据 | approved（按审查原则完成本轮） | verified | 已核对 S02E05 `00:22:38.48` 标题和 S02E08 `00:18:58.35` 四行说明点；未确认遮挡/越界，保留原有特殊定位/行数 | 本地帧点检完成；仅为代表点结论，未宣称全范围视觉播放 |
| `SH0003-DUP-202-000` | S02E01–S02E26；9 个相邻重复中文候选 | 重复译文/源文不一致扫描 | 中文事件与前一中文事件相同，但相邻日文原文存在差异；该模式高度疑似自动化双语合并的机械复制 | 作为 P1 优先候选逐条核对对象、动作、否定、语气和省略；仅确认语义不同才重译；歌曲/口令的有意重复不改写 | `SH-TRANS-001`、`SH-TRANS-008`；本地扫描仅产生候选，但“上下中文完全相同且日语不同”不得被普通重复清单掩盖 | P1 优先候选 | approved（用户授权直接完成本轮） | verified | 9 组均已逐条核对：S02E04、S02E06、S02E11、S02E12、S02E18、S02E19 已修订或删除；S02E04、S02E07、S02E09 的剩余候选确认是同义口令/语气变体并保留 | 修改后仅保留 3 组同义候选；无“上一句意义机械复制”未处理项 |
| `SH0003-DUP-202-001` | S02E04 `00:19:23.36`；CN Event 255 | 重复译文候选 | `岛先生！`；前句相同；日文由 `島さん…` 变为 `島さん！` | 当前事件保留 `岛先生！`；差异落在前一事件的迟疑语气，已由 `001A` 单独处理 | `SH-TRANS-001`；源文语气变化明确，但中文标点受项目覆盖规则约束 | P2 | approved（按用户授权直接完成本轮） | verified | 当前事件无需改写，保留 `岛先生！` | 与 `島さん！` 逐事件对照；前一事件已改为迟疑语气 |
| `SH0003-DUP-202-001A` | S02E04 `00:19:22.18`；CN Event 254 | 语气/重复译文修订 | `岛先生！`；日文为 `島さん…` | 改为 `岛先生……`，保留后一事件 `岛先生！` 的呼喊区分 | `SH-TRANS-001`、`SH-ZH-002`；源文先迟疑后呼喊，中文现状丢失了停顿信息 | P2 | approved（用户授权直接完成本轮） | verified | 已改为 `岛先生……` | 与日文源文和后一事件对照；符合项目标点覆盖项 |
| `SH0003-DUP-202-002` | S02E04 `00:19:49.32`；CN Event 262 | 重复译文候选 | `启动飞轮`；前句相同；日文由无感叹号变为 `フライホイール始動！` | 保留同一系统口令，不因日语句末标点差异改译 | `SH-TRANS-009`；项目普通对白省略句末标点 | P2/P3 | approved（按用户授权直接完成本轮） | verified | 保留 `启动飞轮` | 与相邻日文对照；内容相同，差异仅为标点 |
| `SH0003-DUP-202-003` | S02E06 `00:07:47.64`；CN Event 43 | 疑似复制/漏译 | `我……`；前句相同；本条日文为 `うおおおお！ あたしは…`，比前句多出呼喊 | 补足为 `啊啊啊！我……`，不能保留上一句的机械复制 | `SH-TRANS-001`、`SH-TRANS-002`、`SH-TIME-004`；官方日语副轨明确含呼喊 | P1 | approved（用户授权直接完成本轮） | verified | 已改为 `啊啊啊！我……` | 目标点、JapaneseAux 源文及相邻分段复核 |
| `SH0003-DUP-202-004` | S02E07 `00:16:13.08`；CN Event 168 | 重复译文候选 | `辅助引擎 启动`；前句相同；日文由 `補助エンジン始動！` 变为 `補助エンジン始動` | 保留同一启动口令，不因仅标点差异改写 | `SH-TRANS-009`；源文内容相同 | P2/P3 | approved（按用户授权直接完成本轮） | verified | 保留 `辅助引擎 启动` | 与相邻日文对照；确认是同义口令变体 |
| `SH0003-DUP-202-005` | S02E09 `00:17:09.31`；CN Event 205 | 重复译文候选 | `雪！`；前句相同；日文为同一呼喊的长短变体 `雪ぃ〜！` / `雪！` | 保留同一人物连续呼喊，不把长音效果强行变成新增语义 | `SH-TRANS-001`；不批量把语气效果变成新增语义 | P2/P3 | approved（按用户授权直接完成本轮） | verified | 保留 `雪！` | 与相邻日文和场景上下文对照 |
| `SH0003-DUP-202-006` | S02E11 `00:13:06.06`；CN Event 158 | 疑似复制/语气错译 | `啊？`；前句 `00:13:04.35` 同为反应词；本点无 JapaneseAux 或官方日语 CC 单位 | 删除该孤立复制事件；不凭空保留无源语气 | `SH-TRANS-001`、`SH-SRC-003`、`SH-TRANS-008`；嵌入英文 Dialogue 轨该点无字幕，下一源语为 `Impressive` | P1/P2 | approved（用户授权直接完成本轮） | verified | 已删除 `00:13:06.06` 孤立复制事件 | 与 JapaneseAux、英文嵌入轨和相邻事件复核；无残留孤立事件 |
| `SH0003-DUP-202-007` | S02E12 `00:05:52.69`；CN Event 44 | 疑似复制/语气候选 | `啊`；前句相同；本点无 JapaneseAux 或目标嵌入英文 Dialogue 单位；前句为 `あっ…` | 删除该孤立重复事件；不凭空补译无源反应 | `SH-TRANS-001`、`SH-SRC-003`；目标嵌入英文 Dialogue 轨该点无字幕 | P2，若为无依据增译则 P1 | approved（用户授权直接完成本轮） | verified | 已删除 `00:05:52.69` 孤立复制事件 | 与 JapaneseAux、英文嵌入轨和相邻事件复核；无残留孤立事件 |
| `SH0003-DUP-202-008` | S02E18 `00:05:31.38`；CN Event 35 | 重复译文候选 | `能治好吗？`；前句相同；日文为 `治るのか…`，比前句多出迟疑尾音 | 改为 `能治好吗……`，使后一事件不再把迟疑误写成同一明确问句 | `SH-TRANS-001`、`SH-ZH-002`；命题相同但语气信息不同 | P2 | approved（用户授权直接完成本轮） | verified | 已改为 `能治好吗……` | 与日文源文和前一事件对照 |
| `SH0003-DUP-202-009` | S02E19 `00:22:06.24`；CN Event 221 | 重复译文候选 | `雪`；前句相同；日文由 `雪！` 变为 `雪…` | 改为 `雪……`，区分前句呼喊与后一事件的迟疑/确认 | `SH-TRANS-001`、`SH-ZH-002`；语气差异可能影响人物状态 | P2 | approved（用户授权直接完成本轮） | verified | 已改为 `雪……` | 与日文源文和前一事件对照 |
| `SH0003-MEDIA-202-001` | S02E01–S02E26；OPED 294 条歌曲/片尾越界风险，另 S02E05 `00:22:38.48` 标题风险 | 歌曲/标题越界候选 | 特殊样式启发式 off-screen 风险；不证明实际不可见 | 保留有意歌曲/标题效果；未确认缺陷不移动、不删减 | `SH-QC-009`、`SH-LAYOUT-003`、`SH-QC-010`；特殊字幕不得按普通对白基线化 | P1/P2/P3 依画面结论 | approved（按限制完成本轮） | verified | 已核对 S02E05 `00:22:38.48` 标题及代表性特殊点；未确认发布阻断级越界/隐藏缺陷 | 静态几何与代表性本地帧点检通过；未宣称全范围视觉播放 |
| `SH0003-LAYOUT-202-001` | S02E01–S02E26；空间碰撞风险 82 条，其中 Title/OPED 76 条、普通/画中字样候选 6 条 | 同层空间碰撞候选 | 启发式碰撞记录，特殊样式占多数 | 保留特殊样式；未确认真实遮挡前不移动、删减或合并 | `SH-QC-009`、`SH-LAYOUT-003`；时间重叠不等于空间碰撞 | P2/P3，若遮挡正文则 P1 | approved（按限制完成本轮） | verified | 未确认发布阻断级真实遮挡；保留原有特殊定位 | 静态布局审计通过；未宣称全范围视觉播放 |
| `SH0003-LAYOUT-202-002` | S02E08 `00:18:58.35`，OPED Event 204 | 多行特殊字幕布局 | 1 条事件含 4 个显式行，文本为“反加米拉斯破坏解放军：/反对加米拉斯内部旧德斯拉体制下的霸权主义/并支持各殖民星独立运动的加米拉斯反政府武装。/他们的目标是让加米拉斯恢复到更久远的加米拉斯大公国时代模样。” | 保留四行特殊设计；只有确认遮挡、越界或不可读时才改动 | `SH-QC-009`、`SH-TIME-005`；单点画面左上方为空区，没有具体缺陷证据 | P2/P1 依画面结论 | approved（按限制完成本轮） | verified | 已核对 `00:18:58.35`、`00:18:59.50`：目标画面左上方为空区，未确认遮挡/越界，保留四行设计 | 本地帧点检完成；未做全范围特殊字幕播放声明 |
| `SH0003-MEDIA-202-002` | S02E01–S02E26；7 个中日配对、14 个 Event，机器判定可见时长 < 0.50 秒 | 时长/语音边界媒体候选 | 自动候选，未证明为错误 | 不因数值候选批量改时；仅修已确认的语义/语气错误 | `SH-TIME-002`、`SH-TIME-004`、`SH-QC-010`；短时长不自动等于 P1 | P1/P2/P3 依媒体结论 | approved（不批量处理未确认候选） | verified | 未发现结构性 P0 或已确认的 correction-floor P1；短时长候选保留为后续局部媒体复核项 | 母本时间码/读速检查通过；本轮不宣称全片听辨 |

## 需要用户确认

用户已授权完成本轮校对并直接生成 2.0.2；全范围源语对照、术语闭合、重复译文专项审查、特殊字幕布局和时长候选处理均按该授权实施。SSH 主机指纹及准确的 Season 2 目录已确认，26 集探测完成，不再等待连接确认。

## 决策与实施

本轮已完成 schema 9 / review 3 契约升级、Noto SC/JP 字体机械迁移、全范围静态候选审计和批准的字幕修订：修正 S02E04、S02E06、S02E11、S02E12、S02E17、S02E18、S02E19 的语义/语气或孤立复制问题；已构建 2.0.2 candidate。

## 验证与剩余风险

当前为 `released`。2.0.2 candidate 已完成结构验证，随后按 release contract 轮换为 current，并保留 2.0.1 为 previous；未执行全片播放/听辨，局部媒体证据和未确认启发式候选不被扩写为全片视觉结论。

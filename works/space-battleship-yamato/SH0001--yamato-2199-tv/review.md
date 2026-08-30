---
schema_version: 3
work_id: SH0001
updated_at: "2026-08-31"
baseline_release: 2.0.1
target_release: 2.0.2
status: released
scope: S01E01-S01E26

coverage:
  evidence_tier: A
  timing_authority: target-video-ssh-probed
  master_sha256:
    S01E01: 37f5d3b40d790f51961d250196ccab7786e6ea94108fe81f3c2cefc500567a0e
    S01E02: 56a04c0bfb3822a57e593ba30f7ae68e286cdba06937b3ae8d7bf380276e5111
    S01E03: 7607286cadf8dc0b52a9e1473d61cadb2226a803c652650068435d46d0d2c8a5
    S01E04: 500d4cdad9a468d3d2665ef2069507a5422fb295a94e3b55ea3fe39979f54faa
    S01E05: 5fde64bff693a8626ad3f8b186f0eb331cb7c0f46dc8b7a80c57283bc7076940
    S01E06: 4279ae6dec1d6d7c0cb05c8f5880bc52e3fa9eeb611f6758efe422201f4d7c3b
    S01E07: 43ed1f8fbecda4aa21c79630fcd5f58e099ac780edc8ab7ef7c05d3987381f59
    S01E08: cd4a57d434e962a6495e72004df44d3a1a6cbf050fc88168511ceb89ade148a9
    S01E09: c92de8e30f3ebe395fe0daad3d9fae23481a477808fdea012127a13f4d631efa
    S01E10: c445a4fa39e773268ebacd932f4670a51ef2c3ac057c87ea6f0c330c7eb243b2
    S01E11: eb3914b43e51c08732645195df5afb764f75bc923c8e91c4477d76a676631cd2
    S01E12: 83079cda10929a88a851945c9c3f5b18ebb5073da6e0a3fd526f36e34c3f9b05
    S01E13: 64fcbbd1b919e144b60fbe365fb8d964aa3b89cede296855c61da0f11467caff
    S01E14: eb9a6a917af880bf8bc9c5e624c758ae3e7ec6e723b265791f2d9099eb359eaa
    S01E15: c54839c61f57bb099512159a58ea9d74bb97825f23c393e72d00d68487dc5de1
    S01E16: c8a37d7a8a2bbf1496a86147e47f6cc5ccae3589003c537a64072c5cfd1fcc5d
    S01E17: da005342ebb60a86e958dcf71c717b7118b09570c7a91b9b031cce9c6ca7469c
    S01E18: d31be4048f967beedd7d1937ded1b2ecace66c9735b5f4994aca6d95869b1f67
    S01E19: ddec729fca28b86c7a786c29366b9a7f847b68e8c7e0fc65936e623032d23214
    S01E20: 8ddeb3211b79e3ba10c6a1a36bea639f98ccdf2ffc4dba0eec1dc3380d6960bc
    S01E21: 3a6641b49060ea0d0b6d626961683d0ab8d5c71aa803db1d95515538750e8e56
    S01E22: 56e6333988f0a5f12bdbc4a7f803d311b58ce85d20f74ad896391b96025ac54f
    S01E23: 8abf32f9af4dc9eeb6e46ad6c4b11d00064b7ac0154ceedb4706bdf5d27cbb15
    S01E24: 43fa4d5c4a1431e93787b3b95ea28ce89fe9d8e36fa5c9b02e06766d5035bf63
    S01E25: f6a196a49bd3fbd2397b327796281131bf19bd18927318e38d6d44d901690c45
    S01E26: 418325bf24dbcfda8d96698b101f20098ff20207fdd82fd96c43163f767f71e4
  chinese_in_scope: 15777
  chinese_reviewed: 15777
  chinese_excluded: 0
  source_in_scope: 7974
  source_aligned: 7974
  source_unresolved: 0
  static_layout_checked: 17027
  human_source_fidelity_review: targeted-only; full-meaning-review-not-claimed
  human_release_review: verified
  unresolved_p0: 0
  unresolved_p1: 0

episodes:
  S01E01: { status: released }
  S01E02: { status: released }
  S01E03: { status: released }
  S01E04: { status: released }
  S01E05: { status: released }
  S01E06: { status: released }
  S01E07: { status: released }
  S01E08: { status: released }
  S01E09: { status: released }
  S01E10: { status: released }
  S01E11: { status: released }
  S01E12: { status: released }
  S01E13: { status: released }
  S01E14: { status: released }
  S01E15: { status: released }
  S01E16: { status: released }
  S01E17: { status: released }
  S01E18: { status: released }
  S01E19: { status: released }
  S01E20: { status: released }
  S01E21: { status: released }
  S01E22: { status: released }
  S01E23: { status: released }
  S01E24: { status: released }
  S01E25: { status: released }
  S01E26: { status: released }
---

# 当前校对轮次

## 目标与范围

以 2.0.1 当前发布为基线，对《宇宙战舰大和号2199》TV 全 26 集进行新一轮中文字幕校对，目标发行版本为 2.0.2。保留日文副字幕和既定双语发布契约；仅在本方案获批、证据支持后修改工作区母本。

## 检查覆盖

- 机器检查：26 个 master 共 17,027 个 Event；15,777 个可见中文字幕和 7,974 个源语文本单位纳入范围；17,027 个 Event 已完成 ASS、时间码、字体、样式引用、静态布局和中日事件关系候选审计。
- 候选统计：中文无重叠源语 1,046 条、源语无重叠中文 67 条、短时长 178 条（89 个中日配对）、越界风险 8 条、空间碰撞风险 18 条；这些均是候选，不等同于语义或画面缺陷。
- 文本证据：日文官方 WEBrip CC 为源文本，英文嵌入字幕为辅助翻译/时间参考，系列术语表为已确认术语依据。术语声明形式的禁用命中为 0。
- 媒体检查：SSH 用户 `Viki` 及主机指纹 `SHA256:/2UaP4O8ZNJD+DbiaxNTSKqRey/5u1WfcYbbzHPXrKU` 已固定；Season 1 的 26 个目标视频均已映射并完成只读轨道探测。已按候选点取得局部画面，但未作全片播放声明。
- 未覆盖：全片播放/听辨未执行；本轮不将机器事件配对表述为全片人工源语复核，未确认的启发式时长/布局候选按限制保留。

## 校对方案

| item_id | episode/time or bounded scope | category | before | proposed result | evidence/rationale | severity/risk | decision | status | actual result | verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SH0001-CONTRACT-202-001` | 项目控制面 | Skill 契约迁移 | 旧轮次控制面 | schema 9 / review 3；目标版本 2.0.2 | `SH-INIT-010`、`SH-CTRL-003`；不改变字幕内容 | P1 workflow gate | approved（按本次任务执行） | verified | 已完成 | 三项目 `validate_project.py --ready-for-proofreading` 通过，仅保留历史日期警告 |
| `SH0001-FONT-202-001` | S01E01–S01E26 全部 master | 全局字体机械规范 | 旧字体及混合内联字体 | 仅按 `SH-LAYOUT-004` 统一为 Noto Sans CJK SC/JP | 当前 Skill 的全局字体规则；不改变文字、时间、样式或特效 | P1 rendering consistency | approved（按当前 Skill 必需） | verified | 26 个 master 已完成机械迁移 | 母本字体扫描通过；candidate 尚待构建 |
| `SH0001-AUDIT-202-001` | S01E01–S01E26 全范围 | 全量静态质量审计 | 2.0.1 无本轮完整审计结论 | 保留候选并按本表逐项处理；不批量改写 | `SH-QC-009`、`SH-QC-003`；结构证明与启发式风险分开记录 | P1/P2/P3 依确认结果 | approved（用户授权直接完成本轮） | verified | 26 个母本完成结构、时间、字体、样式引用和静态布局审计；无确认结构缺陷，启发式/媒体候选按本表保留或延后 | `audit_subtitle.py`：17,027 Events、0 confirmed、1,139 risk、178 media-required；机器结果不替代逐条源语人工复核 |
| `SH0001-MEDIA-202-000` | 用户指定 SSH 目录 `/srv/dev-disk-by-uuid-60648e5c-2568-40fd-b0f1-bf799dba4b94/Anime/Uchuu Senkan Yamato 2199 (Star Blazers Space Battleship Yamato 2199)/Season 1/` | 视频路径/轨道探测 | 根目录 `discover` 返回 0 个可识别视频；Season 1 下的 2199 TV 文件未写入本机映射 | 使用用户指定目录和 `remote_media.py`；保持 SSH 文件映射为本机忽略数据，不修改 NAS | `SH-QC-010`；26 个文件与 S01E01–S01E26 一一对应 | P1 workflow gate | approved（按用户指定路径继续） | verified | Season 1 已发现 26/26；全部为 1920×1080 AV1、双 Opus 音轨、2 条 ASS 字幕轨；默认日语音轨和英文 Dialogue 轨，时长探测通过 | 26 个 `probe` 结果、`validate_project.py --ready-for-proofreading` 通过；仅作轨道/时长核验，未作全片播放声明 |
| `SH0001-TERM-202-001` | S01E01–S01E26；系列术语 `YAMATO-TERM-0001`–`0021` 的已声明字面形式 | 术语闭合审计 | 已确认形式尚未与本轮人工源语复核合并 | 逐实体核对全范围短名、姓氏、称谓和派生词；只改证据确认的上下文，不做子串替换 | `SH-TRANS-007`、`SH-TRANS-010`；禁用形式命中 0，但机器扫描不能解决实体歧义 | P1/P2 | approved（用户授权直接完成本轮） | verified | 本轮新增歌词仅使用“大和号”“伊斯坎达尔”等已确认形式；未发现禁用形式或新的未分类专名命中 | 全范围字面扫描与母本复核；术语结论限于已声明形式，不宣称发现未知别名闭合 |
| `SH0001-ALIGN-202-001` | S01E01–S01E26；15,777 中文 / 7,974 源语单位 | 全范围源语对照 | 只有时间重叠候选；中文未解析候选 1,046 条、源语无时间重叠候选 67 条 | 按日文官方 CC 为主、英文为辅完成双向事件闭合；对说话者、动作、对象、否定、数量、因果、语气、分段和时间保留高风险语义修订 | `SH-TRANS-008`、`SH-TRANS-001`；英文仅作辅助，不以多数译本裁决 | P1/P2 | approved（用户已授权直接完成本轮） | verified | 15,777 个可见中文事件完成文本/结构核对；7,974 个源语单位均已归入对应中文、跨事件配对或保留的非中文专名/口令事件；确认的语义修改已逐条列出 | 最终 master 审计：17,027 Events、0 confirmed；源语候选已分类，不宣称全片播放或全片听辨 |
| `SH0001-DUP-202-000` | S01E01–S01E26；5 个相邻重复中文候选 | 重复译文/源文不一致扫描 | 中文事件与前一中文事件相同，但相邻日文原文存在差异 | 逐条核对对象、动作、语气和省略；只有确认语义不同才重译，不把同义口令或仅语气差异批量改写 | `SH-TRANS-001`、`SH-TRANS-008`；本地扫描仅产生候选 | P1/P2 | approved（用户授权直接完成本轮） | verified | 5 组均已对照日文决定：S01E02、S01E18、S01E21 为同一口令/语气变体而保留；S01E14、S01E22 已修订对象或说话功能 | 修改后重复扫描仅保留 3 组同义口令候选；无“上一句意义机械复制”未处理项 |
| `SH0001-DUP-202-001` | S01E02 `00:19:37.21`；CN Event 519 | 重复译文候选 | `拔锚！大和号出发！`；前句同译文；日文由 `発進！` 变为 `発進します！` | 保留同一出发口令的中文，不为日语礼貌尾形制造虚假语义差异 | 相邻 JP 均表达 `抜錨！ ヤマト発進`，后句仅为礼貌/播报变体 | P2 | approved（按用户授权直接完成本轮） | verified | 保留 `拔锚！大和号出发！` | 与前后日文事件对照；确认不是上一句意义机械复制 |
| `SH0001-DUP-202-002` | S01E14 `00:14:58.06`；CN Event 377 | 对象指示/重复译文修订 | `现在就交给你了`；日文为 `これは お前が持っていろ` | 改为 `这个你拿着` | 日文明确指向“这个”，且为直接要求；不能与后一条 `それは あなたが持っていて` 共用译文 | P1 | approved（用户授权直接完成本轮） | verified | 已改为 `这个你拿着` | 与日文 `これは お前が持っていろ` 对照；后一事件已单列修订 |
| `SH0001-DUP-202-002A` | S01E14 `00:15:04.02`；CN Event 378 | 对象指示/语气修订 | `现在就交给你了`；日文为 `それは あなたが持っていて` | 改为 `那个你拿着吧` | 日文对象为“那个”，语气比前句缓和；现译文同时丢失指示对象和差异 | P1 | approved（用户授权直接完成本轮） | verified | 已改为 `那个你拿着吧` | 与日文源文逐事件对照，未改时间轴或布局 |
| `SH0001-DUP-202-003` | S01E18 `00:14:28.15`；CN Event 410 | 重复译文候选 | `开炮！`；前句相同；日文仅有拉长语气 `撃ち〜方 始め！` | 保留同一开炮口令，不把表演性拉长音强行增译 | 相邻 JP 语义相同，差异主要是呼喊效果 | P2/P3 | approved（按用户授权直接完成本轮） | verified | 保留 `开炮！` | 与日文语义及相邻上下文对照，未发现复制了不同意义 |
| `SH0001-DUP-202-004` | S01E21 `00:21:04.63`；CN Event 444 | 重复译文候选 | `出港准备！`；前句相同；日文由 `出航用意！` 变为 `出航よお〜い！` | 保留同一出航口令；日语长音只改变呼喊表现，不新增可译命题 | 相邻 JP 均为出航口令 | P2 | approved（按用户授权直接完成本轮） | verified | 保留 `出港准备！` | 与相邻日文逐事件对照；不是机械复制不同内容 |
| `SH0001-DUP-202-005` | S01E22 `00:20:48.95`；CN Event 605 | 命令/执行报告修订 | `开始跃迁！`；日文为命令 `ワープに入れ！` | 改为 `进入跃迁！` | 命令对象是“进入跃迁”，不是“开始跃迁”；保留必要强制语气 | P1 | approved（用户授权直接完成本轮） | verified | 已改为 `进入跃迁！` | 与 `ワープに入れ！` 对照 |
| `SH0001-DUP-202-005A` | S01E22 `00:20:50.87`；CN Event 606 | 命令/执行报告修订 | `开始跃迁！`；日文为执行陈述 `ワープに入る！` | 改为 `进入跃迁` | 去除与前一句相同的命令感，保留执行报告语气 | P1 | approved（用户授权直接完成本轮） | verified | 已改为 `进入跃迁` | 与 `ワープに入る！` 对照；符合项目普通对白标点覆盖项 |
| `SH0001-TAG-202-001` | S01E11 `00:22:23.24`，Title Event 609 | 已确认 malformed ASS 标签 | `\fad( 500，500)` | 修为 `\fad(500,500)`，保留事件文字、位置和时长 | 静态结构审计确认 malformed fade；当前内容为 `[第十一话 曾经见过的世界 ]` | P1 rendering | approved（用户授权直接完成本轮） | verified | 已修为 `\fad(500,500)` | 母本与候选标签结构扫描通过 |
| `SH0001-LYRICS-202-001` | S01E04 `00:00:14.24`；日文 `さらば 地球よ` | 歌词增译候选 | 仅有日文歌词，无对应中文主字幕 | 补为 `再见了 地球`，保持原曲顺序、时间边界和双语层级 | `SH-TRANS-008`；为单独语义增译，不与其他歌词合并 | P2/P1（发布内容完整性） | approved（用户授权直接完成本轮） | verified | 已新增中文歌词事件 `再见了 地球` | 与同系列 OP 双语母本及日文歌词逐条对照 |
| `SH0001-LYRICS-202-002` | S01E04 `00:00:21.71`；日文 `旅立つ船は` | 歌词增译候选 | 仅有日文歌词，无对应中文主字幕 | 补为 `出航的舰船` | 同上；保持原曲时间边界 | P2/P1 | approved（用户授权直接完成本轮） | verified | 已新增中文歌词事件 `出航的舰船` | 与日文歌词逐条对照 |
| `SH0001-LYRICS-202-003` | S01E04 `00:00:28.97`；日文 `宇宙戦艦「ヤマト」` | 歌词增译候选 | 仅有日文歌词，无对应中文主字幕 | 补为 `宇宙战舰 大和号` | 同上；舰名使用系列规范“大和号” | P2/P1 | approved（用户授权直接完成本轮） | verified | 已新增中文歌词事件 `宇宙战舰 大和号` | 与 `YAMATO-TERM-0002` 和日文歌词对照 |
| `SH0001-LYRICS-202-004` | S01E04 `00:00:44.32`；日文 `宇宙の彼方 イスカンダルへ` | 歌词增译候选 | 仅有日文歌词，无对应中文主字幕 | 补为 `向着宇宙的彼方伊斯坎达尔前进` | 同上；使用“伊斯坎达尔”规范形式 | P2/P1 | approved（用户授权直接完成本轮） | verified | 已新增中文歌词事件 `向着宇宙的彼方伊斯坎达尔前进` | 与 `YAMATO-TERM-0003` 和日文歌词对照 |
| `SH0001-LYRICS-202-005` | S01E04 `00:00:47.94`；日文 `運命 背負い 今とび立つ` | 歌词增译候选 | 仅有日文歌词，无对应中文主字幕 | 补为 `背负着使命 即刻启程` | `SH-TRANS-008`；独立登记 | P2/P1 | approved（用户授权直接完成本轮） | verified | 已新增中文歌词事件 `背负着使命 即刻启程` | 与日文歌词逐条对照 |
| `SH0001-LYRICS-202-006` | S01E04 `00:00:52.66`；日文 `必ずここへ 帰って来ると` | 歌词增译候选 | 仅有日文歌词，无对应中文主字幕 | 补为 `一定会再次回到这里` | 同上；保持原曲时间边界 | P2/P1 | approved（用户授权直接完成本轮） | verified | 已新增中文歌词事件 `一定会再次回到这里` | 与日文歌词逐条对照 |
| `SH0001-LYRICS-202-007` | S01E04 `00:01:00.00`；日文 `手をふる 人に 笑顔で答え` | 歌词增译候选 | 仅有日文歌词，无对应中文主字幕 | 补为 `挥着手 用微笑回答别人` | 同上；保持原曲时间边界 | P2/P1 | approved（用户授权直接完成本轮） | verified | 已新增中文歌词事件 `挥着手 用微笑回答别人` | 与日文歌词逐条对照 |
| `SH0001-LYRICS-202-008` | S01E04 `00:01:09.42`；日文 `銀河をはなれ イスカンダルへ` | 歌词增译候选 | 仅有日文歌词，无对应中文主字幕 | 补为 `离开银河向着伊斯坎达尔前进` | 同上；使用“伊斯坎达尔”规范形式 | P2/P1 | approved（用户授权直接完成本轮） | verified | 已新增中文歌词事件 `离开银河向着伊斯坎达尔前进` | 与 `YAMATO-TERM-0003` 和日文歌词对照 |
| `SH0001-LYRICS-202-009` | S01E04 `00:01:16.64`；日文 `はるばるのぞむ 宇宙戦艦「ヤマト」` | 歌词增译候选 | 仅有日文歌词，无对应中文主字幕 | 补为 `不远万里 宇宙战舰 大和号` | 同上；舰名使用“大和号”规范形式 | P2/P1 | approved（用户授权直接完成本轮） | verified | 已新增中文歌词事件 `不远万里 宇宙战舰 大和号` | 与 `YAMATO-TERM-0002` 和日文歌词对照 |
| `SH0001-MEDIA-202-001` | 全范围；89 个中日配对、178 个 Event，机器判定可见时长 < 0.50 秒 | 时长/语音边界媒体候选 | 自动候选，未证明为错误 | 不因数值候选批量改时；仅保留已修复的语义/标点问题，未确认的短时长交由后续媒体复核 | `SH-TIME-002`、`SH-TIME-004`、`SH-QC-010`；短于 0.5 秒不自动等于 P1 | P1/P2/P3 依媒体结论 | approved（不批量处理未确认候选） | verified | 未发现结构性 P0 或已确认的 correction-floor P1；短时长候选保留为后续局部媒体复核项 | 母本时间码/读速检查通过；本轮不宣称全片听辨 |
| `SH0001-LAYOUT-202-001` | S01E04 `00:09:10.55`、`00:17:39.34`；S01E05 `00:22:21.90`；S01E06 `00:22:20.52`；S01E09 `00:22:24.48`；S01E11 `00:21:15.09`；S01E25 `00:24:12.99`；S01E26 `00:01:34.53` | 越界/隐藏布局候选 | 8 条启发式 off-screen 风险 | 保留有意特殊定位；未取得足以确认其余候选为缺陷的证据，不移动特殊字幕 | `SH-QC-009`、`SH-LAYOUT-003`；特殊字幕不做基线化 | P1/P2/P3 依画面结论 | approved（按限制完成本轮） | verified | 已核对 S01E04 `00:09:10.55`，其余为静态几何候选；未确认 P0/P1 越界/隐藏缺陷 | ASS 几何审计及该媒体点通过；未宣称全范围视觉播放 |
| `SH0001-LAYOUT-202-002` | S01E04 `00:22:19.46`；S01E20 `00:25:00.10`；S01E25 OP/ED `00:01:33.40–00:02:43.89` | 同层空间碰撞候选 | 18 条启发式碰撞记录，主要为特殊样式/歌曲 | 保留特殊字幕/歌曲的原位置和效果；时间重叠不单独认定为空间碰撞 | `SH-QC-009`、`SH-LAYOUT-003`；时间重叠不等于空间碰撞 | P2/P3，若遮挡正文则 P1 | approved（按限制完成本轮） | verified | 未确认发布阻断级真实遮挡；未做批量移动、删减或合并 | 静态布局审计通过；媒体限制和后续局部复核范围已记录 |

## 需要用户确认

用户已授权完成本轮校对并直接生成 2.0.2；本表中的语义修订、歌词补译、malformed fade 修复、术语/重复译文核对和保守的特殊字幕处理均按该授权实施。SSH 主机指纹及 Season 1 的 26 个目标视频探测结果已确认，不再等待连接确认。

## 决策与实施

本轮已完成 schema 9 / review 3 契约升级、Noto SC/JP 字体机械迁移、全范围静态候选审计和批准的字幕修订：S01E04 补齐 9 条中文片头歌词，S01E10 修正人名中点，S01E11 修复 malformed fade，S01E14 区分两个指示对象，S01E22 区分命令与执行报告；已构建 2.0.2 candidate。

## 验证与剩余风险

当前为 `released`。2.0.2 candidate 已完成结构验证，随后按 release contract 轮换为 current，并保留 2.0.1 为 previous；未执行全片播放/听辨，局部媒体证据和未确认启发式候选不被扩写为全片视觉结论。

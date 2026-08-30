---
schema_version: 3
work_id: "SH0004"
updated_at: "2026-08-31"
baseline_release: "1.0.2"
target_release: "1.1.0"
status: released
scope: "S03E01–S03E04 full current release"

coverage:
  evidence_tier: C
  timing_authority: "target-video SSH mapping; embedded English ASS is the auxiliary timing reference; Japanese audio stream #1 is the meaning authority"
  master_sha256:
    S03E01: b7555584fc524c5937cfd54c6bb6cba595f37d83caeedf608fa99ef611d98ccf
    S03E02: 268f12e6e1ae541c3d37142cf151fe5dd58c909a72a0fe7318846866e0b8fcc3
    S03E03: 94ae183b6f96b7e88d36fa140a56d6f7c2be8fbf44ab4daf3fadb1303e6a1a5a
    S03E04: a76baf78da85f06cf7aa818c128980d0d52c4f3d034a298ca8bfe184d67bc1c1
  chinese_in_scope: 2387
  chinese_reviewed: 2387
  chinese_excluded: 0
  source_in_scope: 0
  source_aligned: 0
  source_unresolved: 0
  static_layout_checked: 9846
  human_source_fidelity_review: verified
  human_release_review: verified
  unresolved_p0: 0
  unresolved_p1: 0

episodes:
  S03E01: { status: released }
  S03E02: { status: released }
  S03E03: { status: released }
  S03E04: { status: released }
---

# 当前校对轮次

## 目标与范围

以 1.0.2 发布为基线，对《宇宙战舰大和号2205 新的旅程》前篇 S03E01–S03E04 进行 1.1.0 新一轮校对。范围包含四集全部可见中文字幕、已确认系列术语、文本质量、事件分段/间距、现有时间轴的具体点位核对和静态布局候选。方案、全范围人工审核和发行终审均已由用户确认，1.1.0 已发布到 `subtitles/current/`。

## 检查覆盖

- 机器检查：四个 master 共 9,846 个 Event、2,387 个可见中文字幕 Event，9,846 个 Event 已完成 ASS 结构、时间码、字体、样式引用和静态布局审计。
- 文本证据：当前没有可靠可搜索的日语字幕文本；嵌入英文 ASS 仅作辅助翻译、时间轴和语境线索，日语 PGS/OCR 仅作图像参考。日语音轨 stream #1 是实际语义依据，因此本轮保持 C-tier，不能把英文、OCR 或抽查结果写成全范围源语证明。
- 媒体映射：NAS 目录已按用户给定路径固定，S03E01–S03E04 均已匹配并完成只读轨道探测；视频为 1920×1080，日语 Opus stream #1，英文 ASS 为辅助轨道。后续只用 `scripts/remote_media.py` 核对具体候选点，不全片提取音频、不批量截图。
- 静态候选：最终 master 审计保留 14 个可见中文短时长 media-required 候选；它们已按批准方案逐点处理，未凭数值阈值删除意义。大量 off-screen、hidden-alpha、预测换行和同层碰撞结果集中在有意的片头、片尾、卡拉 OK、字幕特效或隐藏动画事件，未按普通对白批量修复。
- 覆盖结论：2,387 个可见中文字幕 Event 已完成本轮中文质量、术语、标点、分段和结构复核；源语文本不可搜索，`source_aligned` 仍为 0，证据等级保持 C。用户已确认 `ゲシュタム` 的规范简中为“格什塔姆”，本轮无未决 P1。

## 校对方案

| item_id | episode/time or bounded scope | category | before | proposed result | evidence/rationale | severity/risk | decision | status | actual result | verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SH0004-CONTRACT-141-001` | 项目控制面与四个 master | 当前 Skill 契约复核 | 项目已从上一轮迁移到 schema 9 / review schema 3 / Skill 1.4.1；本轮 master 指纹为上方基线 | 保持当前项目 schema、Noto SC/JP 全局字体、`review.md` 单一状态面；只在 workspace master 实施获批修改 | `SH-INIT-010`、`SH-CTRL-003`；不恢复旧 schema，不新建台账或项目脚本 | P1 workflow gate | approved（按当前 Skill 执行） | verified | 按当前 Skill 1.4.1 保持 schema 9、review schema 3 和单一控制面。 | setup_runtime.py --check、validate_project.py --ready-for-proofreading 通过。 |
| `SH0004-MEDIA-141-001` | 用户指定 NAS 目录；S03E01–S03E04 | 视频路径与轨道角色 | 已完成目录发现、文件匹配和轨道探测 | 保留本机忽略的 SSH 映射；日语音轨 stream #1 作意义依据，英文 ASS 作辅助翻译/时间轴，日语 PGS/OCR 仅作图像参考；不修改 NAS | `SH-INIT-011`、`SH-QC-010`；主机指纹为 `SHA256:/2UaP4O8ZNJD+DbiaxNTSKqRey/5u1WfcYbbzHPXrKU`，仅在具体候选点调用 `remote_media.py` | P1 workflow gate | approved（用户已确认连接与目录） | verified | 已匹配并确认 4/4 NAS 视频；本轮不宣称全片听辨。 | project.yaml 与本机 SSH 映射一致；未修改 NAS。 |
| `SH0004-FONT-141-001` | S03E01–S03E04 全部 retained styles 与非空 inline `\fn` | 全局字体机械规范 | 1.0.2 master 已完成上一轮 Noto 迁移；本轮需按 1.4.1 再验 | 保持 `Noto Sans CJK SC`（中文/英文）与 `Noto Sans CJK JP`（日文）；不改文字、时间、颜色、位置、特效或普通/特殊样式属性 | `SH-LAYOUT-004`；字体规则是全局字体例外，不授权其他布局批改 | P1 rendering consistency | approved（当前 Skill 必需） | verified | 8 个 master 与候选保持 Noto Sans CJK SC/JP；未改其他样式属性。 | 8 个 master 与 8 个候选均通过 audit_subtitle.py；候选字体变更为 0。 |
| `SH0004-AUDIT-141-001` | S03E01–S03E04 全范围 | 全量静态质量审计 | 已审计 9,846 Event；机器报告存在大量特效隐藏缩放、透明度、预测换行和同层碰撞候选 | 将结构性结果与 media-required/risk 分开；保留有意特殊事件，只处理获媒体证据支持的具体缺陷 | `SH-QC-009`、`SH-QC-003`；机器检查只能证明结构或提出候选，不能证明画面遮挡、语义或同步 | P1/P2/P3 依证据 | approved | verified | 完成全量 master 审计；结构性结果与 media-required/risk 分离，未批量改特殊事件。 | 8 个 master 与 8 个候选的 audit_subtitle.py 均退出码 0。 |
| `SH0004-ALIGN-141-001` | S03E01–S03E04；2,388 中文 Event | 全范围中文质量复核 | C-tier；尚未逐事件完成意义、语气、术语、语法、标点、分段和内部一致性复核 | 批准后逐一复核所有可见中文；英文只作辅助，日语音频只用于明确的高风险/低清晰度点；每个重译、删减、增译、意义修正另列行 | `SH-TRANS-008`、`SH-TRANS-009`、`SH-TRANS-001`；不把英文时间重叠当成源语对照完成 | P1/P2 | approved | verified | 完成 2,387/2,387 个可见中文 Event 的 C-tier 质量复核；源语忠实度未宣称。 | 逐事件对照 master 与候选完成；术语审计通过，保留 C-tier 源语证据限制。 |
| `SH0004-TERM-141-001` | S03E01–S03E04；系列 `YAMATO-TERM-0009`、`YAMATO-TERM-0010` 及全范围中文专名候选 | 已确认术语闭合 | 本轮需重新扫描完整形式集；上一轮未留下本轮术语覆盖结论 | 对完整已声明形式集逐实体扫描中文与辅助来源；只按 confirmed `term_id` 修正，记录每个表面形式的数量、排除项和剩余未分类命中；不做短字符串子串替换 | `SH-TRANS-007`、`SH-TRANS-010`；系列表规定“大和号”“伊斯坎达尔”“加米拉斯”“宇宙复原系统”“波动防御壁” | P1/P2 | approved | verified | 已完成全范围系列术语扫描与获批修正；大和号、伊斯坎达尔、加米拉斯及相关装置术语已核对。 | audit_terms.py schema-1 manifest 通过；禁用完整表面形式命中 0，候选审计通过。 |
| `SH0004-TERM-141-002` | S03E03 `00:20:55.14`、`00:22:35.96`；S03E04 `00:19:28.82` | 系列专名与听译误写 | `Geas Tam Out反应`；`Geas Tam Jump（跃迁）了！？`；`Geas Tam壁功率降低`。英文辅助轨道写作 `Geshtam` | 分别改为 `检测到多个格什塔姆反应！`、`格什塔姆跃迁？`、`格什塔姆防御壁输出下降`，并将 `ゲシュタム` / `Geshtam` / “格什塔姆”登记为系列 `YAMATO-TERM-0022` | 用户确认日文原词与专名含义；同版英文三处稳定写作 `Geshtam`；`SH-TRANS-007`、`SH-TRANS-010` | P1 | approved（用户确认“格什塔姆”并要求写入系列表） | verified | 三处 workspace master 已按具体语境改为规范中文，不保留误写 `Geas Tam`。 | 全范围检索 `Geas Tam` 为 0；`YAMATO-TERM-0022` 已写入系列表；术语审计与候选验证通过。 |
| `SH0004-E01-141-001` | S03E01 `00:10:10.30`、`00:11:52.70` | 确定性间距机械修复 | `明早0600`（2 处） | `明早 0600`；保持精确时间值和原事件边界 | `SH-ZH-003`；数字与中文语义边界需一个 ASCII 空格 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E01-141-002` | S03E01 `00:14:05.45` | 错字/清晰度 | `到也不是不能理解他们的心情` | `倒也不是不能理解他们的心情` | 中文语境与固定搭配；英文仅表明为理解对方感受，不能替代中文修订依据 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E01-141-003` | S03E01 `00:18:25.17` | 系列舰名 | `还偏偏是大和` | `还偏偏是大和号` | `YAMATO-TERM-0002`；英文 `Yamato, of all places` 与上下文均指舰名，不是普通地点名 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E02-141-001` | S03E02 `00:03:31.91` | 重复字/语病 | `发生发生了冲突` | `发生了冲突` | 明确的同字重复；不改变“与波拉联邦发生冲突”的意义 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E02-141-002` | S03E02 `00:17:59.89` | 呼号/术语可读性 | `宾馆长机通知各机` | 倾向 `Hotel 长机通知各机`；若日语音轨确认其为约定呼号则保留专名大小写，不译作普通“宾馆” | 英文辅助为 `Hotel leader to all units`；当前译文可能把 NATO 呼号误读为普通地点词，需音频/上下文确认 | P2 | approved | verified | 两处通信事件均统一保留 Hotel 呼号：Hotel 长机通知各机；Hotel 长机 Clear For Take Off。 | 与同集英文辅助轨道及通信语境对照；两处 master/candidate 文本一致，audit_subtitle.py 通过。 |
| `SH0004-E02-141-003` | S03E02 `00:19:52.65` | 呼号/术语可读性 | `宾馆长机 Clear For Take Off` | `Hotel 长机 Clear For Take Off` | 与同集 `00:17:59.89` 同一通信呼号；英文辅助为 `Hotel leader, clear for take-off.`，按同一呼号机械统一 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E02-TERM-141-003` | S03E02 `00:19:21.87` | 系列装置术语 | `宇宙逆转系统` | `宇宙复原系统` | `YAMATO-TERM-0009`；英文辅助为 `Cosmo Reverse`，与全项目同一装置；按系列确认 canonical form 统一 | P1/P2 | approved | verified | 已完成全范围系列术语扫描与获批修正；大和号、伊斯坎达尔、加米拉斯及相关装置术语已核对。 | audit_terms.py schema-1 manifest 通过；禁用完整表面形式命中 0，候选审计通过。 |
| `SH0004-MAGELLAN-141-001` | S03E02 `00:03:55.13`；S03E03 `00:13:20.79`、`00:13:51.64`；S03E04 `00:14:50.17`、`00:18:01.57` | 星系名称一致性 | `麦哲伦星云` 与 `麦哲伦银河` 混用 | 统一为 `麦哲伦星云`，除非日语音轨/明确画面信息证明此处是不同对象；保持 S03E01 画面文字现有 `麦哲伦星云` | 英文辅助在对应点均为 `Magellanic Cloud`；同一作品内已有两种中文形式，当前没有系列 term_id，故先列为 bounded context decision | P2；若对象误判则 P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E03-141-001` | S03E03 `00:05:00.40` | 动作语义 | `就这样一个不留的推到你们` | `就这样把你们一个不留地击落` | 英文辅助为 `We'll knock all of them down the same way!`；当前“推到”既有错字又弱化战斗动作，需实际音轨确认对象与动作 | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E03-141-002` | S03E03 `00:19:41.54–00:19:47.68` 三个相邻事件 | 语义与跨事件分段 | `在那儿` / `本应就那附近的` / `我们犹如母亲般的行星` | 维持三个事件的时间顺序，重排为 `就在那附近` / `本应存在的我们的母星` 一类自然表达；不提前显示信息 | 英文辅助为 `Right around there, that was our home planet.`；当前语序和“犹如母亲般”造成误读，需音频确定时态与称呼 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E03-141-003` | S03E03 `00:20:06.56` | 错字/清晰度 | `这样下去地表不知到将会变成什么样子` | `这样下去地表不知道会变成什么样子` | `不知到` 为明确错字；改写同时避免“将会”堆叠，保留对地表恶化的疑问 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E03-141-004` | S03E03 `00:20:10.37` | 孤立重复/无依据文本 | `将地下` | 删除孤立片段；由下一事件完整表达 `请将王都地下的圣窟开放吧` | 英文辅助从 `00:20:09.80` 直接表达 opening the entrance beneath the capital；当前片段既不成句又重复“地下”，需音频确认无独立发声 | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E04-141-001` | S03E04 `00:01:34.56` | 重复字/语病 | `银河派出的的探测机已经二次检查过了` | `银河派出的探测机已经二次检查过了` | 明确的 `的的` 重复；不改“银河系统复核”的事实 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E04-141-002` | S03E04 `00:01:55.56` | 语义/语法 | `还未存能做到这种事的星球在么……` | `还存在能做到这种事的星球吗……` | 英文辅助为 `Is there a planet capable of doing such a thing?`；当前“未存”破坏句意，疑问形式也不自然 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E04-141-003` | S03E04 `00:05:51.49` | 语法/人称 | `那可不是能由姐姐你能决定的！` | `那可不是姐姐你能决定的！` | 英文辅助为 `That's not for you to decide, sister!`；当前 `由` 与 `能` 叠加，破坏句法 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E04-141-004` | S03E04 `00:09:06.56` | 错字/句式 | `想我这种迟钝——` | `像我这种迟钝——` | `像……这种` 为明确句式；下一事件继续表达“没用的男人为何出生” | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E04-141-005` | S03E04 `00:15:51.42–00:15:54.68` 两个事件 | 传送门语义 | `冲入大门了的话` / `那舰船就只能前进了` | `一旦进入传送门` / `那舰船就只能继续前进了` | 英文辅助为 `Once the ship enters the gate, we have no choice but to go forward.`；前文已称“亚空间传送门”，当前“大门”与假设句式均不自然 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E04-141-006` | S03E04 `00:18:24.07` | 冗余/清晰度 | `但大和号不仅仅只是一艘战舰` | `但大和号不仅仅是一艘战舰` | `不仅仅` 与 `只` 重复；不改变“大和号也是人类希望”的后续信息 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E04-141-007` | S03E04 `00:19:14.16–00:19:20.03` 两个事件 | 语义与跨事件分段 | `冲田的孩子们……` / `和又一代的孩子们 出发了吗……` | 建议重排为 `冲田的孩子们，` / `以及他们的孩子们，都在向前迈进……`；保留后代与“向前迈进”信息，不写成疑问 | 英文辅助为 `Okita's children and their children are taking a step forward.`；当前“又一代”“出发了吗”均偏离意义 | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0004-E04-TERM-141-008` | S03E04 `00:06:48.00`、`00:16:27.46` | 系列专名错写 | `伊斯坎德尔`（2 处） | `伊斯坎达尔` | `YAMATO-TERM-0003`；两处均位于伊斯坎达尔相关叙述，属于同一专名的明显错写 | P1/P2 | approved | verified | 已完成全范围系列术语扫描与获批修正；大和号、伊斯坎达尔、加米拉斯及相关装置术语已核对。 | audit_terms.py schema-1 manifest 通过；禁用完整表面形式命中 0，候选审计通过。 |
| `SH0004-MEDIA-141-002` | S03E01 `00:10:14.85`、`00:12:01.07`、`00:13:44.34`、`00:14:17.40`、`00:17:05.53`；S03E02 `00:05:19.07`、`00:07:45.52`、`00:08:27.77`、`00:16:11.49`、`00:16:52.39`、`00:18:15.45`、`00:20:31.06`；S03E03 `00:12:07.35`、`00:20:10.00`、`00:20:18.28`；S03E04 `00:08:30.31`、`00:14:07.63`、`00:14:38.31`、`00:16:06.89`、`00:17:45.97` | 时长/语音边界媒体候选 | 20 个可见中文 Event 小于 0.50 秒；机器候选不等于错误 | 逐点检查实际语音起止、阅读负担、下一事件间隔和镜头信息；只修有明确 speech-boundary/reading failure 的 Event 及必要邻居，不为达到数值阈值删除意义 | `SH-TIME-002`、`SH-TIME-004`、`SH-QC-010`；短时长可能是口令、反应词或有意切分 | P1/P2/P3 依点位证据 | approved | verified | 20 个初始短时长候选中，已按英文时间轴与必要点位证据修正明确边界问题；其余保留自然短促对白，最终仍有 14 个 media-required 候选。 | 时间轴修正已与嵌入英文 ASS 对照；master/candidate 审计通过，未因阈值删除意义。 |

## 发行终审结论

1. 1.1.0 候选仅做规范化头部、来源署名保留、非渲染 Comment 清理和未使用样式清理；用户已通过终审。
2. “格什塔姆”三处已按用户确认修正并写入系列术语表，无专名豁免项。
3. 用户在获知 C-tier 源语复核门禁后明确确认已审核全部字幕；`human_source_fidelity_review` 与 `human_release_review` 均记为 `verified`。
4. 用户已在 2026-08-31 通过终审并明确要求发布 1.1.0；本轮不生成 ZIP。

## 决策与实施

方案已获批并完成实施：未修改 `project/sources/`；四个 workspace master 已按逐项决定完成中文修订、术语统一和明确时间轴异常修正。1.1.0 候选保留所有 rendered Dialogue，清理仅限非渲染 Comment、未使用样式和规范化头部；已提升为 `subtitles/current/`，1.0.2 完整保留在 `subtitles/previous/`，未生成 ZIP。

## 验证与剩余风险

当前状态为 `released`。用户已确认“格什塔姆”、全部其余修改、全范围字幕审核及正式发行；candidate/master rendered Dialogue 不变量、来源署名、版本、字体与回滚目录均通过验证。视觉证据未上传聊天。

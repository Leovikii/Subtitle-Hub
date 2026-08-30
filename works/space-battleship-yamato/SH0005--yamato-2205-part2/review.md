---
schema_version: 3
work_id: "SH0005"
updated_at: "2026-08-31"
baseline_release: "1.0.2"
target_release: "1.1.0"
status: released
scope: "S03E05–S03E08 full current release"

coverage:
  evidence_tier: C
  timing_authority: "target-video SSH mapping; embedded English ASS is the auxiliary timing reference; Japanese audio stream #1 is the meaning authority"
  master_sha256:
    S03E05: 104ad9ceac5e07ef088a1a9065efaeb37652d5d55bbed4a8fcc74367e0a6181a
    S03E06: 6425888ada184e00676b8db0e145488c80df831671848db0c99fd1f03dd6411c
    S03E07: dda9f379a52c812adb84b3d3211acf476a7ec1f01d933f231aed31943943f32c
    S03E08: b5f25f65945abffd24c2667e94f7e82b5c13bbfbc65650c53dd75d8ce4636b37
  chinese_in_scope: 2319
  chinese_reviewed: 2319
  chinese_excluded: 0
  source_in_scope: 0
  source_aligned: 0
  source_unresolved: 0
  static_layout_checked: 10393
  human_source_fidelity_review: verified
  human_release_review: verified
  unresolved_p0: 0
  unresolved_p1: 0

episodes:
  S03E05: { status: released }
  S03E06: { status: released }
  S03E07: { status: released }
  S03E08: { status: released }
---

# 当前校对轮次

## 目标与范围

以 1.0.2 发布为基线，对《宇宙战舰大和号2205 新的旅程》后篇 S03E05–S03E08 进行 1.1.0 新一轮校对。范围包含四集全部可见中文字幕、已确认系列术语、文本质量、事件分段/间距、现有时间轴的具体点位核对和静态布局候选。方案、全范围人工审核和发行终审均已由用户确认，1.1.0 已发布到 `subtitles/current/`。

## 检查覆盖

- 机器检查：四个 master 共 10,393 个 Event、2,319 个可见中文字幕 Event，10,393 个 Event 已完成 ASS 结构、时间码、字体、样式引用和静态布局审计。
- 文本证据：当前没有可靠可搜索的日语字幕文本；嵌入英文 ASS 仅作辅助翻译、时间轴和语境线索，日语 PGS/OCR 仅作图像参考。日语音轨 stream #1 是实际语义依据，因此本轮保持 C-tier，不能把英文、OCR 或抽查结果写成全范围源语证明。
- 媒体映射：NAS 目录已按用户给定路径固定，S03E05–S03E08 均已匹配并完成只读轨道探测；视频为 1920×1080，日语 Opus stream #1，英文 ASS 为辅助轨道。后续只用 `scripts/remote_media.py` 核对具体候选点，不全片提取音频、不批量截图。
- 静态候选：最终 master 审计中的 3 个小于 0.50 秒事件均为仅源语事件，不属于中文发布分母；大量 off-screen、hidden-alpha、预测换行和同层碰撞结果集中在有意的片头、片尾、卡拉 OK、字幕特效或隐藏动画事件，未按普通对白批量修复。
- 术语结论：`波动护盾` 5 处、`波动防壁` 1 处、`宇宙恢复系统` 1 处、`星球恢复系统` 1 处已分别统一为系列确认形式；`Geas Tam` 1 处已按用户确认改为“格什塔姆”。
- 覆盖结论：2,319 个可见中文字幕 Event 已完成本轮中文质量、术语、标点、分段和结构复核；源语文本不可搜索，`source_aligned` 仍为 0，证据等级保持 C。本轮无未决 P1。

## 校对方案

| item_id | episode/time or bounded scope | category | before | proposed result | evidence/rationale | severity/risk | decision | status | actual result | verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SH0005-CONTRACT-141-001` | 项目控制面与四个 master | 当前 Skill 契约复核 | 项目已从上一轮迁移到 schema 9 / review schema 3 / Skill 1.4.1；本轮 master 指纹为上方基线 | 保持当前项目 schema、Noto SC/JP 全局字体、`review.md` 单一状态面；只在 workspace master 实施获批修改 | `SH-INIT-010`、`SH-CTRL-003`；不恢复旧 schema，不新建台账或项目脚本 | P1 workflow gate | approved（按当前 Skill 执行） | verified | 按当前 Skill 1.4.1 保持 schema 9、review schema 3 和单一控制面。 | setup_runtime.py --check、validate_project.py --ready-for-proofreading 通过。 |
| `SH0005-MEDIA-141-001` | 用户指定 NAS 目录；S03E05–S03E08 | 视频路径与轨道角色 | 已完成目录发现、文件匹配和轨道探测 | 保留本机忽略的 SSH 映射；日语音轨 stream #1 作意义依据，英文 ASS 作辅助翻译/时间轴，日语 PGS/OCR 仅作图像参考；不修改 NAS | `SH-INIT-011`、`SH-QC-010`；主机指纹为 `SHA256:/2UaP4O8ZNJD+DbiaxNTSKqRey/5u1WfcYbbzHPXrKU`，仅在具体候选点调用 `remote_media.py` | P1 workflow gate | approved（用户已确认连接与目录） | verified | 已匹配并确认 4/4 NAS 视频；本轮不宣称全片听辨。 | project.yaml 与本机 SSH 映射一致；未修改 NAS。 |
| `SH0005-FONT-141-001` | S03E05–S03E08 全部 retained styles 与非空 inline `\fn` | 全局字体机械规范 | 1.0.2 master 已完成上一轮 Noto 迁移；本轮需按 1.4.1 再验 | 保持 `Noto Sans CJK SC`（中文/英文）与 `Noto Sans CJK JP`（日文）；不改文字、时间、颜色、位置、特效或普通/特殊样式属性 | `SH-LAYOUT-004`；字体规则是全局字体例外，不授权其他布局批改 | P1 rendering consistency | approved（当前 Skill 必需） | verified | 8 个 master 与候选保持 Noto Sans CJK SC/JP；未改其他样式属性。 | 8 个 master 与 8 个候选均通过 audit_subtitle.py；候选字体变更为 0。 |
| `SH0005-AUDIT-141-001` | S03E05–S03E08 全范围 | 全量静态质量审计 | 已审计 10,393 Event；机器报告的 3 个短时长事件均为日文源语事件，另有特效透明度、预测换行和同层碰撞候选 | 将结构性结果与 media-required/risk 分开；保留有意特殊事件，只处理获媒体证据支持的具体缺陷 | `SH-QC-009`、`SH-QC-003`；机器检查只能证明结构或提出候选，不能证明画面遮挡、语义或同步 | P1/P2/P3 依证据 | approved | verified | 全量静态审计完成；3 个小于 0.50 秒的事件均为源语事件，不属于中文字幕分母。 | 8 个 master 与 8 个候选的 audit_subtitle.py 均退出码 0。 |
| `SH0005-ALIGN-141-001` | S03E05–S03E08；2,319 中文 Event | 全范围中文质量复核 | C-tier；尚未逐事件完成意义、语气、术语、语法、标点、分段和内部一致性复核 | 批准后逐一复核所有可见中文；英文只作辅助，日语音频只用于明确的高风险/低清晰度点；每个重译、删减、增译、意义修正另列行 | `SH-TRANS-008`、`SH-TRANS-009`、`SH-TRANS-001`；不把英文时间重叠当成源语对照完成 | P1/P2 | approved | verified | 完成 2,319/2,319 个可见中文 Event 的 C-tier 质量复核；源语忠实度未宣称。 | 逐事件对照 master 与候选完成；术语审计通过，保留 C-tier 源语证据限制。 |
| `SH0005-TERM-141-001` | S03E05–S03E06；6 个事件：S03E05 `00:17:14.86`、`00:18:23.43`、`00:19:18.11`；S03E06 `00:19:39.55`、`00:19:43.05`、`00:21:08.39` | 已确认防御术语闭合 | `波动护盾` 5 处、`波动防壁` 1 处 | 六处统一为 `波动防御壁`；不改变时间、出力数值或普通对话布局 | `YAMATO-TERM-0010`、`SH-TRANS-007`、`SH-TRANS-010`；系列规范已确认 canonical form，两个旧形式均为禁用/待替换形式 | P1 terminology | approved | verified | 6 处旧防御术语已统一为波动防御壁；2 处复原系统称呼已统一为宇宙复原系统。 | audit_terms.py schema-1 manifest 通过；禁用完整表面形式命中 0，候选审计通过。 |
| `SH0005-TERM-141-002` | S03E07 `00:08:17.83`、`00:10:15.65` | 已确认装置术语与上下文术语 | `宇宙恢复系统`；`星球恢复系统` | 两处均统一为 `宇宙复原系统`；第二处需保留“通过该系统复原双子星”的完整意义 | `YAMATO-TERM-0009`、英文 `Cosmo Reverse System` 辅助文本及相邻语境；前一形式为系列禁用形式，后一形式是同一装置的未统一表达 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-TERM-141-003` | S03E06 `00:20:17.63` | 系列专名与听译误写 | `Geas Tam壁展开 跟上大和号`；英文辅助写作 `Deploy the Geshtam wall and follow the Yamato.` | `展开格什塔姆防御壁 跟上大和号`，并将 `ゲシュタム` / `Geshtam` / “格什塔姆”登记为系列 `YAMATO-TERM-0022` | 用户确认日文原词与专名含义；同版英文写作 `Geshtam`；`SH-TRANS-007`、`SH-TRANS-010` | P1 | approved（用户确认“格什塔姆”并要求写入系列表） | verified | workspace master 已按具体语境改为规范中文，不保留误写 `Geas Tam`。 | 全范围检索 `Geas Tam` 为 0；`YAMATO-TERM-0022` 已写入系列表；术语审计与候选验证通过。 |
| `SH0005-E05-141-001` | S03E05 `00:05:21.78` | 语义/语气 | `就算打成这样 也无所谓是吗` | `都伤成这样了，他们还在观望……` | 英文辅助为 `After this much damage, and they're still watching...`；当前将“仍在观望”误成“不在乎” | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E05-141-002` | S03E05 `00:05:42.25` | 词义/清晰度 | `你的那份感情是比这噪音更危险的东西` | `你的情绪比这噪音更危险` | 英文辅助为 `Your feelings are more dangerous than this noise.`；“情绪”更明确指向当下失控状态，去掉拖沓的“那份/东西” | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E05-141-003` | S03E05 `00:06:09.07` | 语义误译 | `没想到竟然是胆小鬼` | `没想到竟然这么不堪一击` | 英文辅助为 `It's unexpectedly weak.`；当前把“脆弱/不堪一击”误译为人格评价“胆小鬼” | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E05-141-004` | S03E05 `00:06:10.78` | 句式/语气 | `命令航空队追击` | `要下令航空队追击吗？` | 英文辅助带疑问号 `Pursuit order to the aerial unit?`；当前把询问误成命令 | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E05-141-005` | S03E05 `00:09:11.50–00:09:16.59` | 语义/人物状态 | `不只迪乌苏拉三世` / `听说德斯拉总统也受了很重的伤` | `迪乌苏拉三世也受了重创` / `听说德斯拉总统也受了很重的伤` | 英文辅助为 `The condition of the Deusula III is obvious, and I heard His Excellency Desler was badly hurt.`；当前“不只”无所指且弱化舰船受损事实 | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E05-141-006` | S03E05 `00:11:20.68` | 人名间距机械修复 | `还有古代 进这个男人` | `还有古代进这个男人` | `YAMATO-TERM-0012`；人名不可被空格拆开，且当前不是“古代”加普通动词 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E05-141-007` | S03E05 `00:12:39.00` | 数值/时间信息 | `距到达杀伤区 还有180秒` | `距进入杀伤区还有 0800 秒` | 英文辅助明确为 `0800 seconds till it enters the kill zone.`；当前漏掉前导 0、动词关系和规范间距 | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E05-141-008` | S03E05 `00:17:52.02` | 语气/措辞 | `热血沸腾说的就是这种情况吧` | `这就是所谓的“热血沸腾”吗……` | 英文辅助为 `“Blood-curdling,” is that what this is called…?`；保留原有双关方向，修复中文问句和尾音节奏 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E05-141-009` | S03E05 `00:18:09.38` | 语义误译 | `报告` | `请允许我发言！` | 英文辅助为 `Allow me to speak freely!`；当前“报告”不是请求发言 | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E05-141-010` | S03E05 `00:21:27.07` | 口号语义/一致性 | `全员来承担` | `大家共同承担` | 英文辅助为 `We're all in this together!`；中文需自然表达共同承担处境，后续相同语句逐条登记，不隐藏语义改译 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E06-141-001` | S03E06 `00:01:45.23–00:01:50.77` | 重复文本/跨事件语义 | `把加米拉斯` / `把母亲般的加米拉斯破坏的敌人` | `加米拉斯……` / `就是毁灭我们母星加米拉斯的敌人` | 英文辅助为 `Garmillas... That's the enemy who destroyed our mother planet of Garmillas.`；当前首行残句且第二行重复“把” | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E06-141-002` | S03E06 `00:01:56.99` | 语义/清晰度 | `请用那认识到战争空虚之处的心领导民众吧` | `请用一颗明白战争毫无意义的心来引导民众吧` | 英文辅助为 `bearing a heart that recognizes the meaninglessness of war`；当前“那……之处的心”不自然且关系不清 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E06-141-003` | S03E06 `00:02:10.00` | 语法 | `贵军残忍的摧毁了加米拉斯星` | `贵军残忍地摧毁了加米拉斯星` | 明确的副词结构错误；不改变控诉内容 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E06-141-004` | S03E06 `00:06:14.16` | 重复字/清晰度 | `但大和号也有不小的的损伤` | `但大和号也受了不小的损伤` | 明确的 `的的` 重复；改为自然动词结构，不改变受损事实 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E06-141-005` | S03E06 `00:06:27.68` | 口号语义/一致性 | `全员来承担` | `大家共同承担` | 与英文 `We're all in this together!` 对齐；不得因前后重复而漏掉独立事件 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E06-141-006` | S03E06 `00:06:30.51–00:06:33.10` | 口号语义/句式 | `由全员来承担` / `那时候不是这么决定了吗` | `由大家共同承担` / `我们不是这样决定的吗` | 当前口号结构不自然；英语上下文是对既有共同决定的追问 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E06-141-007` | S03E06 `00:06:48.86` | 引号/口号语义 | `请问 全员来承担”究竟是什么意思` | `请问“大家共同承担”究竟是什么意思` | 当前缺少左引号且口号沿用不自然形式；不把标点问题隐藏在批量替换中 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E06-141-008` | S03E06 `00:07:24.65` | 语气/逻辑 | `就算你们不这么一个劲的说` / `我也能理解现在的状况` | `不用一直强调` / `我明白现在的状况` | 英文辅助为 `Slow down. I do understand the situation.`；当前让步句把“够了/不必反复说”写成条件句 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E06-141-009` | S03E06 `00:08:36.51` | 人名错字 | `我不认为斯塔萨女王会听得进去` | `我不认为斯塔莎女王会听得进去` | 同集同一人物的规范形式为“斯塔莎”；英文 `Starsha` 仅作辅助，系列角色连续性支持修正 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E06-141-010` | S03E06 `00:12:39.05` | 语义/重复字 | `加米拉斯把你们的的故乡毁灭了` | `加米拉斯侵入并毁灭了你们的故乡` | 英文辅助为 `Garmillas invaded and brought ruin to your homeland.`；当前有 `的的`，并漏掉侵入/带来毁灭的动作关系 | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E06-141-011` | S03E06 `00:13:18.79` | 标点/引用 | `和出身没关系”吗` | `“和出身没关系”吗` | 当前仅有右引号；该事件是在复述前一句话，补齐成对引号 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E07-141-001` | S03E07 `00:02:58.47–00:03:02.68` | 语义遗漏 | `但我们出现的时期` / `进化的时间长短并不相同` | `但我们的出生时期` / `以及成长进化所需的时间并不相同` | 英文辅助为 `time of birth, and the time necessary for us to grow and evolve differ`；当前遗漏“出生”和“成长所需时间” | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E07-141-002` | S03E07 `00:03:22.07–00:03:26.14` | 错字/清晰度 | `也是一个贪婪 妄图支配一切` / `且及其利己主义的长子` | `也是一个贪婪、妄图支配一切` / `且极其自私的长子` | 英文辅助为 `A greedy, controlling and very selfish first son.`；`及其`为错字，`利己主义的`在此处生硬 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E07-141-003` | S03E07 `00:02:18.84`、`00:04:57.84`、`00:08:38.22`、`00:09:02.54`、`00:09:38.37` | 确定性间距机械修复 | `接受 仪式`、`接受 仪式`、`进行 仪式 吧`、`这就是 仪式`、`进行 仪式` | 分别去除词内/词组间多余空格：`接受仪式`、`进行仪式吧`、`这就是仪式`、`进行仪式`；保持时间与意义 | `SH-ZH-003`；中文词组不以 ASCII 空格断开，5 处为明确排版错误 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E07-141-004` | S03E07 `00:08:17.83` | 系列装置术语 | `只要使用宇宙恢复系统的话` | `只要使用宇宙复原系统` | `YAMATO-TERM-0009`；canonical form 为“宇宙复原系统”，当前“恢复”是禁用形式，句末“的话”需结合下一句重排 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E07-141-005` | S03E07 `00:09:02.54–00:09:11.24` | 语义/跨事件分段 | `这就是 仪式` / `为了永远保存生命和文明而不断重复地` / `伊斯坎达尔所进行的虐杀` | `这就是仪式` / `为了永远保存生命和文明而一再重复的` / `伊斯坎达尔式虐杀` | 英文辅助为 `That is the ritual... repeated over and over... Genocide by Iscandar.`；当前副词悬空，语句连接不完整 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E07-141-006` | S03E07 `00:09:38.37–00:09:55.64` | 语义遗漏/人物设定 | `那么由谁来进行 仪式` / `派出大军将生命和文明葬送的呢` / `和只有在特定环境下才能生存的脆弱` / `方便管理的奴隶` | 保留问句并补足 `强健的肉体`、`只能在特定环境下生存的弱点` 与 `这样的奴隶便于控制` 等信息；具体分段以音轨为准 | 英文辅助明确包含 strong body、weakness、easy to manipulate；当前文本缺失/错接，不能只修表面字词 | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E07-141-007` | S03E07 `00:10:15.65` | 系列装置术语/上下文 | `通过星球恢复系统` | `通过宇宙复原系统` | 英文辅助为 `Utilizing the Cosmo Reverse`；与同集 `宇宙恢复系统` 指同一装置，`星球恢复`为未统一表达 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E07-141-008` | S03E07 `00:14:22.11` | 错字/身份语义 | `作为被认命了管理圣窟的王族` | `作为被任命管理圣窟的王族` | `任命`为明确正确字；英文为 `royal family, which manages Sanktel`，不改变身份内容 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E07-141-009` | S03E07 `00:15:17.79–00:15:23.29` | 语义/名词清晰度 | `这里的都是拒绝变化沉浸在幸福的过去里的群体` | `这里的都是拒绝改变、沉浸在幸福过去中的记忆集合` | 英文辅助为 `These collections of memories indulge themselves in happiness, and they refuse to change.`；当前“群体”丢失记忆集合设定且语序生硬 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E07-141-010` | S03E07 `00:15:54.49` | 语气/动作 | `现在将让渡伊斯坎达尔` | `我会交出伊斯坎达尔……` | 英文辅助为 `I'll surrender Iscandar...`；当前“现在将让渡”不自然且缺少第一人称决定语气 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E07-141-011` | S03E07 `00:16:24.76` | 通讯指令 | `接到这里来` | `请接通` | 英文辅助为 `Patch me through.`；当前直译成“接到这里来”不符合通讯口令 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E08-141-001` | S03E08 `00:00:08.05` | 指令语义/语法 | `全员对冲击对闪光防御` | `全员准备应对冲击和闪光` | 英文辅助为 `All hands, prepare for shock and flash.`；当前重复“对”造成病句 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E08-141-002` | S03E08 `00:02:49.96` | 副词/清晰度 | `为了保持你的自我 彻底的抗争下去` | `为了保持自我，抗争到底` | 英文辅助为 `Fight every inch of the way so you can be yourself.`；当前“彻底的”结构错误且表达拖沓 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E08-141-003` | S03E08 `00:06:29.55–00:06:33.60` | 亲属关系语义 | `和自己兄弟相爱的人那便是亲人` | `爱上地球人兄弟的人，就会成为家人` | 英文辅助为 `a person who falls in love with an Earthling's sibling becomes family`；当前误读成“爱上自己兄弟”，改变亲属关系 | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E08-141-004` | S03E08 `00:06:08.28` | 语义误译 | `大和号在不断回复“请待机”` | `大和号一再通知我们撤离` | 英文辅助为 `Yamato is repeatedly telling us to escape.`；当前把 escape 误为 standby，且“回复”不合语境 | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E08-141-005` | S03E08 `00:08:53.07` | 句式/清晰度 | `但是 不能就这样白白的把伊斯坎达尔交出去` | `但是不能白白把伊斯坎达尔交出去` | 英文辅助为 `we can't let them have Iscandar like this`；去掉多余结构助词，保留“不甘心交出”的态度 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E08-141-006` | S03E08 `00:09:21.10` | 动作/措辞 | `把呼吸配合起来` | `让呼吸合拍` | 英文辅助为 `coordinate our breathing`；当前“把呼吸配合”搭配不自然，需保留团队协作意味 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E08-141-007` | S03E08 `00:10:40.59` | 错字/清晰度 | `没办法在提高了` | `没办法再提高了` | 明确的 `在/再` 错字；不改变动力限制 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E08-141-008` | S03E08 `00:13:45.15` | 指令语义 | `向先行的移民船团也传达下去` | `也通知前方的移民船团这样做` | 英文辅助为 `Tell the advanced migrant ships to do the same!`；当前未表达“让先行船团也散开”的指令对象和动作 | P1/P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E08-141-009` | S03E08 `00:16:27.69` | 语气/口吻 | `在地球要开心呦` | `在地球上要开心哦` | 英文辅助为 `Sasha, make sure to have fun on Earth, okay?`；修复介词和语气字形，保留亲昵口吻 | P2 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |
| `SH0005-E08-141-010` | S03E08 `00:17:17.91` | 语义/重复文本 | `人们 人们所能做到的` | `这就是一个人能为另一个人做到的最好事情了` | 英文辅助为 `That's the best one human can do for another human.`；当前重复“人们”并未表达施受关系与“最好” | P1 | approved | verified | 已按获批方案在对应 workspace master 实施，未改变项目范围。 | 对应事件已与 master 和候选逐项对照；audit_subtitle.py 通过。 |

## 发行终审结论

1. 1.1.0 候选仅做规范化头部、来源署名保留、非渲染 Comment 清理和未使用样式清理；用户已通过终审。
2. “格什塔姆”一处已按用户确认修正并写入系列术语表，无专名豁免项。
3. 用户在获知 C-tier 源语复核门禁后明确确认已审核全部字幕；`human_source_fidelity_review` 与 `human_release_review` 均记为 `verified`。
4. 用户已在 2026-08-31 通过终审并明确要求发布 1.1.0；本轮不生成 ZIP。

## 决策与实施

方案已获批并完成实施：未修改 `project/sources/`；四个 workspace master 已按逐项决定完成中文修订、术语统一和明确时间轴异常处理。1.1.0 候选保留所有 rendered Dialogue，清理仅限非渲染 Comment、未使用样式和规范化头部；已提升为 `subtitles/current/`，1.0.2 完整保留在 `subtitles/previous/`，未生成 ZIP。

## 验证与剩余风险

当前状态为 `released`。用户已确认“格什塔姆”、全部其余修改、全范围字幕审核及正式发行；candidate/master rendered Dialogue 不变量、来源署名、版本、字体与回滚目录均通过验证。视觉证据未上传聊天。

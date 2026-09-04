---
schema_version: 3
work_id: "SH0007"
updated_at: "2026-09-04"
baseline_release: null
target_release: "1.0.0"
status: released
scope: "S02E01-S02E08"
coverage:
  evidence_tier: A
  timing_authority: "S02E01-S02E08=embedded Simplified Chinese subtitle track"
  alignment_source_id: optional-source-001
  alignment_verified: verified
  master_sha256:
    S02E01: b33290ca4ff59f4047fb6245e1c2891a6153d36d882b363ac64966fadfb82c70
    S02E02: 22aa4f3d14562931b18806271a1a85d6050df4aff2ad26d7058cd5c5f2a43942
    S02E03: 598684c132d65a1b86d5f8392ab597b3cc3a6246aee346bd94af1215ab01b2f4
    S02E04: c409f8bdd895965d56bd2211f3cc5c0f807ee3c6171372b5e0750bce9ddc4189
    S02E05: 68d9ad49253894887db044c0dcdec02e664a65acbef0bfc57dc3b72c9045c2b6
    S02E06: 4e06489395e39eedb5e2b02f2fdaa7a6f082372b97327dc1eecbb8b9474ca0c5
    S02E07: 4b8aae2b139064ac793686f37cf3be941ba16b9c26c550e84db8ea1a14317a8f
    S02E08: 0801908c2a703b1566197c7f2ae588d37d4abe7ff0c96116a935a18f0d8ee1cf
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
  source_in_scope: 4796
  source_aligned: 4558
  source_excluded: 238
  source_unresolved: 0
  static_layout_checked: 9205
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

以 Bangumi `534091` 建立《百年孤独 第二季》S02E01–S02E08 独立项目；以同切版内嵌简体中文字幕为主语言和时间轴权威，以普通 Latin America 西语字幕为来源文本及发布副语言，生成中文在上、西语在下的双语 ASS，候选版本为 `1.0.0`。

## 检查覆盖

- 已检查 8 集全部 4,409 条可见中文字幕的文本、结构、时间码及静态布局，未以抽查代替全文覆盖。
- 已双向核对 4,796 条西语来源单位：4,558 条进入普通语义映射；238 条为歌曲、口号、叫卖、群众/画内/环境声或非情节性短反应，拟以 `ES-Special` 原样保留并逐项记为 `excluded-special`。
- 中文无普通西语对应的 57 条已逐条检查：50 条为片名、章节、画面文字或译者署名；7 条为同切版可见次要/背景对白（G000072、G000103、G000153、G000173、G000335、G000545、G003998）。英文普通轨确认后者实际存在，但普通西语轨无可安全投影的西语，拟以 `CN-Special` 保留，不虚构翻译。
- 对齐覆盖 4,158 组、87 个有界批次；初始形状为 3,187 个 1:1、238 个 0:1、57 个 1:0，其余为经语义确认的 1:N、N:1 或 N:M。
- 五组重复风险均为真实不同对白：G000471/G000472、G001136/G001137、G001407/G001409、G002934/G002935/G002936；实施时记录理由，不删事件。
- 全季结构、非法时间及结构确定型静态布局 finding 为 0。未执行全片播放、ASR、VAD、OCR 或批量视频处理。

## 校对方案

### A. 系列术语机械统一

| item_id | 范围 | 修改前 → 建议结果 | 证据与边界 | 风险 | 决定/状态 | 实际结果/验证 |
| --- | --- | --- | --- | --- | --- | --- |
| TERM-001 | 全季 102 处（E01 8/E02 21/E03 7/E04 16/E05 11/E06 11/E07 9/E08 19） | 已确认 José Arcadio / Arcadio 实体中的 `阿卡蒂奥` → `阿尔卡蒂奥` | `SOLITUDE-TERM-001/002/010`；含实际全名、简称及“第二”，逐事件确认实体，不作无边界扩张 | P1，同规则机械批次 | approved / verified | implemented / 旧形须为 0 |
| TERM-002 | 全季 55 处（5/6/3/9/2/2/15/13） | `乌苏拉` → `乌尔苏拉`，含全名及 `阿玛兰妲·乌苏拉` | `SOLITUDE-TERM-005` 及已确认复合姓名 | P1，机械批次 | approved / verified | implemented / 旧形须为 0 |
| TERM-003 | E01 3/E04 1/E07 2/E08 9，共 15 处 | `梅贾德斯` → `梅尔基亚德斯` | `SOLITUDE-TERM-003`；对应 `Melquíades` | P1 | approved / verified | implemented / 旧形须为 0 |
| TERM-004 | E01 2/E03 1/E05 3/E08 2，共 8 处 | `皮拉`、`皮拉·特内拉` → `庇拉尔`、`庇拉尔·特尔内拉` | `SOLITUDE-TERM-017`；简称/全名均已对齐实体 | P1 | approved / verified | implemented / 两旧形须为 0 |
| TERM-005 | E04 1 处 | `彼得罗·克莱斯皮` → `皮耶特·克雷斯皮` | `SOLITUDE-TERM-015` | P1 | approved / verified | implemented / 精确复查 |
| TERM-006 | 全季 8 处；E08 含全名 1 处 | `盖里奈多` → `格林列尔多`；`盖里奈多·马奎斯` → `格林列尔多·马尔克斯` | `SOLITUDE-TERM-021`；对应 `Gerineldo Márquez` | P1 | approved / verified | implemented / 旧形须为 0 |
| TERM-007 | E01 1/E07 1/E08 3，共 5 处 | `奥雷里亚诺·巴比罗尼亚` → `奥雷里亚诺·巴比伦` | `SOLITUDE-TERM-025`；明确排除另一实体 `毛里修奥·巴比罗尼亚` 7 处 | P1，定界批次 | approved / verified | implemented / 旧全名 0，排除项仍 7 |
| TERM-008 | E01 2 处 | `何塞·拉奎`、`何塞·拉奎·蒙卡达` → `何塞·拉克尔`、`何塞·拉克尔·蒙卡达` | `SOLITUDE-TERM-031`；对应简称/全名 | P1 | approved / verified | implemented / 两旧形须为 0 |
| TERM-009 | 全季 28 处（E04 4/E05 15/E06 4/E07 4/E08 1） | `雷娜塔` → `雷纳塔` | `SOLITUDE-TERM-024`；对应 `Renata`，`Meme` 仍为 `梅梅` | P1 | approved / verified | implemented / 旧形须为 0 |
| TERM-010 | E04 00:35:40 G001760 | `奥雷利亚诺` → `奥雷里亚诺` | 同事件 `Aureliano` 及全季规范形式 | P1 | approved / verified | implemented / 错字须为 0 |

### B. 逐条语义修正

| item_id | 集数/时间/组 | 修改前 → 建议结果 | 证据与理由 | 风险 | 决定/状态 | 实际结果/验证 |
| --- | --- | --- | --- | --- | --- | --- |
| SEM-001 | E02 00:11:27 G000588 | `何塞·阿卡蒂奥招募人手、购买工具` → `何塞·阿尔卡蒂奥第二招募人手、购买工具` | `José Arcadio Segundo`，人物身份遗漏；并应用 TERM-001 | P1 | approved / verified | implemented / 来源复核 |
| SEM-002 | E03 00:10:37 G001013 | `您看起来比他说的更年轻漂亮多了` → `您看起来比他说的更年轻、更和蔼` | `amable` 是和蔼/亲切，并非漂亮 | P1 | approved / verified | implemented / 比较对象、语气复核 |
| SEM-003 | E04 00:01:56 G001420 | `小心点 梅梅` → `规矩点 梅梅` | `Ordenado, Meme` 是要求守规矩，不是安全提醒 | P1 | approved / verified | implemented / 相邻对白复核 |
| SEM-004 | E04 00:02:57 G001434 | `它来了！是真的！` → `就是他 你没听见吗？` | `¡Así es él, no me oyes!`；原译丢失人物指称和反问 | P1 | approved / verified | implemented / 相邻列车场景复核 |
| SEM-005 | E04 00:18:09 G001609 | `我儿子知道 他必须严肃对待自己的学业` → `我儿子知道 如果想去罗马 就必须严肃对待学业` | `si quiere ir a Roma` 是剧情相关条件 | P1 | approved / verified | implemented / 条件、目的地复核 |
| SEM-006 | E04 00:33:26 G001753 | `过来` → `请在这里签字` | 邮差递包裹场景；`¿Me firma aquí?`，原中文来自相邻催促 | P1 | approved / verified | implemented / 重建相邻映射 |
| SEM-007 | E06 00:38:39 G002729 | `警察说他是个偷鸡贼 / 他当时正翻过围栏` → `警察说他是个偷鸡贼 / 他当时正翻过围栏 还说就是他偷了拉克尔家的鸡` | 漏译 `El mismo le robó a Raquel` | P1 | approved / verified | implemented / 三句来源与可读性复核 |
| SEM-008 | E06 00:56:45 G002911 | `火车不来的话 该有人告诉我们才对` → `要是火车不去首都 我们早该听说了` | `Ya nos hubiéramos enterado de que no viene a la capital` | P1 | approved / verified | implemented / 前后地名复核 |
| SEM-009 | E07 00:16:25 G003147 | `但你若没空 我可以跟你丈夫谈` → `但如果你愿意 我可以跟你丈夫谈` | `si quiere` 是“如果您愿意” | P1 | approved / verified | implemented / 沟通意图复核 |
| SEM-010 | E07 00:22:59 G003205 | `连直肠和地洞都分不清的女人` → `连直肠和斋日都分不清的女人` | `témporas` 为天主教四季斋日，不是地洞 | P1 | approved / verified | implemented / 宗教词义复核 |
| SEM-011 | E07 00:47:25 G003393–G003394 | `到了午夜 / 又努力向那些 / 在唱机旁哭泣的孤独女郎兜售好运` → `直到午夜 他仍努力用好运说辞 / 安慰那些在唱机旁哭泣的孤独女郎` | `todavía a la medianoche trataba de consolar con prédicas de buena suerte`；原译句法残缺且动作错 | P1 | approved / verified | implemented / 合并语义并检查 CPS |
| SEM-012 | E08 00:30:09 G003681 | `我还会说德语和法语 拉丁语也比你强` → `我还会说德语、英语和法语 拉丁语也比你强` | `alemán, inglés y francés`，漏掉英语 | P1 | approved / verified | implemented / 列举与比较复核 |
| SEM-013 | E08 00:43:44 G003820 | `那一晚 还有接下来的晚上` → `那天下午以及之后几个下午` | `Ni esa tarde ni las siguientes` 为下午，不是夜晚 | P1 | approved / verified | implemented / 时间连续性复核 |
| SEM-014 | E08 00:59:09 G003933 | `世上无难事 只怕有心人` → `法国人的字典里没有“不可能”` | `“Imposible” no es francés` 是法语双关；原译抹去笑点 | P2 | approved / verified | implemented / 与上下句复核 |
| SEM-015 | E08 01:04:20 G003988 | `这小镇什么也不会发生 这破房子也不会…` → `这小镇和这破房子不会有事 没有你它们也撑过了这么多年` | 原译句子残缺，漏掉 `sobrevivieron años sin ti` | P1 | approved / verified | implemented / 争执语气复核 |
| SEM-016 | E08 01:09:58 G004040 | `我明早就搭第一班船离开` → `我明早就搭第一班船去比利时` | `Me voy a Bélgica`，目的地影响后续情节 | P1 | approved / verified | implemented / 目的地复核 |

### C. 映射、特殊字幕与样式

| item_id | 范围 | 建议结果 | 证据与边界 | 风险 | 决定/状态 | 实际结果/验证 |
| --- | --- | --- | --- | --- | --- | --- |
| MAP-001 | G000141–142、G000408–411、G000715–716、G002015–018、G002976–979、G003385–387、G004007–008 | 对语序相反或叙述/祷词并行处合并为 N:M reviewed group，写 split/merge rationale；不改已有中文意义 | 双向检查确认意义完整，逐事件硬配会错配 | P1 对齐门禁 | approved / verified | implemented / unit 唯一、单调、无遗漏 |
| MAP-002 | 五组重复风险 | 确认为真实不同对白并逐组写理由，不删不并 | 两次呼喊、暗语/正常语、两次“它来了”、三次“八八八”均有不同时间/行为 | P1 对齐门禁 | approved / verified | implemented / 风险清零且事件数不减 |
| SPECIAL-001 | 全季 57 条中文无普通西语项 | 50 条片名/章节/画面文字/署名及 7 条次要背景对白改用 `CN-Special`，保留文字、时间及特殊属性 | 普通西语无安全可投影文本；英文/SDH 只确认存在，不据此虚构西语 | P1 | approved / verified | implemented / 普通中文 1:0 为 0 |
| SPECIAL-002 | 全季 238 条西语无中文项 | 逐项 `excluded-special`；以 `ES-Special` 原样保留歌曲、口号、叫卖、群众/画内/环境声及非情节性短反应，不增造中文 | 全文及相邻窗口确认非需补译的主对白 | P2 | approved / verified | implemented / 238 条有原因，unresolved=0 |
| STYLE-001 | 全季普通对白 | 中文 `Noto Sans CJK SC` 62/MarginV 130；`ES-Main` 46/MarginV 68；1920×1080、白字近黑 3 px 描边、无阴影，中文在上西语在下 | `SH-LAYOUT-002/004` 与已确认 zh-bilingual | P1 | approved / verified | implemented / 字体、引用、间距验证 |
| STYLE-002 | 全季特殊字幕 | `CN-Special`、`ES-Special` 仅统一字体为 Noto Sans CJK SC；位置、颜色、字号、效果不批量标准化 | `SH-LAYOUT-003/004` | P1 | approved / verified | implemented / 渲染属性无越权变化 |

## 决策与实施

用户已批准完整方案。10 组术语批次、16 条逐项语义修正、特殊字幕分流、映射重建与西语投影均已完成；所有表内 `approved / verified` 均按批准方案实施并验证，建议结果即实际结果。对齐最终为 4,088 个 reviewed group，中文普通单位 4,352、西语单位 4,796，其中 4,558 已对齐、238 为有界特殊项、未解决 0；五组重复风险已逐项清除。`1.0.0` 完整候选已构建到 `project/workspace/build/current-candidate/`，共 8 个 ASS 与 VERSION。

## 验证与剩余风险

- P0=0、P1=0；术语审计 forbidden hits=0，未分类已知实体形式=0。
- alignment verify 通过：中文普通 4,352、西语 4,796、对齐 4,558、特殊排除 238、source unresolved=0；上方记录最终 master/source 指纹。
- 最终静态审计覆盖 9,205 个渲染事件，confirmed finding=0、media-required=0。普通西语中的 1,521 个显式换行已在不改变语义的前提下展平；1,155 个可能自动换行的长西语事件使用 `ES-Main-2L` 低位样式。中文 `Default` 与 `ES-Main`/`ES-Main-2L` 的空间碰撞为 0；剩余 810 个 predicted-wrap 风险均是已由 2L 样式承接的预期换行，不构成重叠。
- Noto 全局字体、ASS 结构、候选 master-render invariant、项目 `--ready-for-proofreading` 与本地 package-plan check 均通过；没有写 ZIP。
- 时间轴沿用用户确认的同切版内嵌简中权威；未声称全片播放或听辨。用户已于 2026-09-04 完成发行前终审并批准发布；`1.0.0` 候选已晋升为当前发行版。

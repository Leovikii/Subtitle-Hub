# 《宇宙战舰大和号》系列用语规范

本文件遵循仓库 `$subtitle-hub` Skill 的 `SH-TRANS-007`，是本系列唯一活动术语表。SH0001、后续 2202、2205、3199 等项目必须先读取本表；项目不得复制本表，差异只能在项目 `project.yaml` 中按 `term_id` 明确覆盖。

## 来源

| source_id | 类型 | 标题 | URL 或仓库路径 | 核验日期 | 用途与限制 |
| --- | --- | --- | --- | --- | --- |
| `YAMATO-SRC-WIKI-ZH-2199` | 中文维基 | 宇宙战舰大和号2199 | https://zh.wikipedia.org/wiki/宇宙戰艦大和號2199 | 2026-08-26 | 用于发现中文名、人物名和设定术语候选；页面存在个别译名变体，不能单独决定批量替换。 |
| `YAMATO-SRC-BANGUMI-54552` | 条目数据库 | 宇宙戦艦ヤマト2199 | https://bgm.tv/subject/54552 | 2026-08-26 | 核对作品中文名、原名、TV 类型和 26 集范围。 |
| `YAMATO-SRC-SH0001-JA` | 原语字幕 | SH0001 日语 WEBrip CC | SH0001--yamato-2199-tv/project/sources/subtitles/ja/official-webrip-cc | 2026-08-26 | 核对 2199 中实际出现的日文专名；具体语境仍需结合音轨。 |
| `YAMATO-SRC-SH0001-GUIDE` | 仓库基线 | SH0001 项目确认规则 | SH0001--yamato-2199-tv/project.yaml | 2026-08-26 | 继承已经明确采用且与原词对应的系列译名；不表示 1.0.0 每个事件均已完成术语审计。 |
| `YAMATO-SRC-BANGUMI-84701` | 条目数据库 | 宇宙戦艦ヤマト2199 星巡る方舟 | https://bgm.tv/subject/84701 | 2026-08-26 | 核对《星巡的方舟》中文名、剧场版类型和单片范围。 |
| `YAMATO-SRC-BANGUMI-246898` | 条目数据库 | 宇宙戦艦ヤマト2202 愛の戦士たち | https://bgm.tv/subject/246898 | 2026-08-26 | 核对 2202 TV 中文名、TV 类型和 26 集范围，排除七章剧场上映条目。 |
| `YAMATO-SRC-SH0002-JA` | 原语字幕 | SH0002 日语正文与 BDSUP OCR | SH0002--yamato-2199-odyssey-celestial-ark/project/sources/subtitles/ja | 2026-08-26 | 核对电影实际出现的日文专名；OCR 只作交叉验证。 |
| `YAMATO-SRC-SH0003-JA` | 原语字幕 | SH0003 日语官方 WEBrip CC | SH0003--yamato-2202-tv/project/sources/subtitles/ja/official-webrip | 2026-08-26 | 核对 2202 实际出现的日文专名；具体语境仍需结合音轨。 |
| `YAMATO-SRC-SH0003-BASELINE` | 仓库基线 | SH0003 迁入成品 | SH0003--yamato-2202-tv/subtitles/current | 2026-08-26 | 继承旧工程已经逐项审查并统一的系列译名；迁入发现的冲突仍须在项目统一台账逐事件核对。 |

## 规范术语

| term_id | 类别 | 日文原词 | 规范简体中文 | 禁用或待替换形式 | 适用范围 | source_id | 状态 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `YAMATO-TERM-0001` | 系列名 | `宇宙戦艦ヤマト` | 宇宙战舰大和号 | 宇宙战舰YAMATO | 全系列 | `YAMATO-SRC-WIKI-ZH-2199` | `confirmed` | 数字续作直接附在系列名后。 |
| `YAMATO-TERM-0002` | 舰名 | `ヤマト` | 大和号 | Yamato、大和（单独作舰名时） | 全系列 | `YAMATO-SRC-WIKI-ZH-2199` | `confirmed` | 普通叙述保留“号”；画面标签受空间限制时另行登记。 |
| `YAMATO-TERM-0003` | 星球/文明 | `イスカンダル` | 伊斯坎达尔 | 伊斯坎达、伊斯康达尔 | 全系列 | `YAMATO-SRC-SH0001-JA` | `confirmed` | 中文形式同时参考中文维基；派生形式为“伊斯坎达尔人”“伊斯坎达尔星”。 |
| `YAMATO-TERM-0004` | 星球/文明 | `ガミラス` | 加米拉斯 | 加美拉斯、卡米拉斯 | 全系列 | `YAMATO-SRC-SH0001-JA` | `confirmed` | 中文形式同时参考中文维基；人、语言和帝国等派生词保持同一词干。 |
| `YAMATO-TERM-0005` | 技术 | `次元波動エンジン` | 次元波动引擎 | 次元波动发动机 | 2199 重制系列 | `YAMATO-SRC-SH0001-JA` | `confirmed` | 上下文已经明确时可以简称“波动引擎”。 |
| `YAMATO-TERM-0006` | 装置 | `波動コア` | 波动核心 | 波动核 | 2199 重制系列 | `YAMATO-SRC-SH0001-JA` | `confirmed` | 不与波动引擎混用。 |
| `YAMATO-TERM-0007` | 武器 | `波動砲` | 波动炮 | 波动大炮 | 全系列 | `YAMATO-SRC-SH0001-JA` | `confirmed` | 完整名称按作品设定另增条目。 |
| `YAMATO-TERM-0008` | 武器 | `遊星爆弾` | 游星炸弹 | 行星炸弹 | 全系列 | `YAMATO-SRC-SH0001-JA` | `confirmed` | “游星”是系列专名，不改写为普通天文学用词。 |
| `YAMATO-TERM-0009` | 装置 | `コスモリバースシステム` | 宇宙复原系统 | 宇宙恢复系统、宇宙回复系统 | 2199 重制系列 | `YAMATO-SRC-SH0001-JA` | `confirmed` | 中文维基页面存在“回复/恢复”等变体；中文形式沿用 SH0001 已确认的“复原”。 |
| `YAMATO-TERM-0010` | 防御技术 | `波動防壁` | 波动防御壁 | 波动护盾、波动防壁 | 2199 重制系列 | `YAMATO-SRC-SH0001-JA` | `confirmed` | 中文形式沿用项目已确认规范；SH0001 1.0.0 尚有混用，已登记候选问题，不得无审查批改。 |
| `YAMATO-TERM-0011` | 人名 | `沖田十三` | 冲田十三 | 冲田十三郎 | 全系列同角色 | `YAMATO-SRC-WIKI-ZH-2199` | `confirmed` |  |
| `YAMATO-TERM-0012` | 人名 | `古代進` | 古代进 | 古代晋 | 全系列同角色 | `YAMATO-SRC-WIKI-ZH-2199` | `confirmed` |  |
| `YAMATO-TERM-0013` | 人名 | `島大介` | 岛大介 | 岛大助 | 全系列同角色 | `YAMATO-SRC-WIKI-ZH-2199` | `confirmed` |  |
| `YAMATO-TERM-0014` | 人名 | `森雪` | 森雪 | 森雪儿 | 全系列同角色 | `YAMATO-SRC-WIKI-ZH-2199` | `confirmed` |  |
| `YAMATO-TERM-0015` | 人名 | `真田志郎` | 真田志郎 | 真田四郎 | 全系列同角色 | `YAMATO-SRC-WIKI-ZH-2199` | `confirmed` |  |
| `YAMATO-TERM-0016` | 人名 | `デスラー` | 德斯拉 | 迪斯拉、戴斯拉 | 2199 重制系列 | `YAMATO-SRC-SH0003-BASELINE` | `confirmed` | SH0002 1.0.0 尚有 3 处“迪斯拉”，已登记候选，不得无审查批改。 |
| `YAMATO-TERM-0017` | 文明/国家 | `ガトランティス` | 加特兰蒂斯 | 加特兰提斯、加特兰迪斯 | 2199 重制系列 | `YAMATO-SRC-SH0003-JA` | `confirmed` | 人、军队和帝国等派生词保持同一词干。 |
| `YAMATO-TERM-0018` | 人名 | `テレサ` | 特蕾莎 | 特雷莎 | 2202 及同角色 | `YAMATO-SRC-SH0003-BASELINE` | `confirmed` | 与星球“特蕾莎特”区分。 |
| `YAMATO-TERM-0019` | 人名 | `ズォーダー` | 佐达 | 兹沃达、佐尔达 | 2202 及同角色 | `YAMATO-SRC-SH0003-BASELINE` | `confirmed` | 身份称谓可以写作“佐达大帝”。 |
| `YAMATO-TERM-0020` | 星球 | `テレザート` | 特蕾莎特 | 特雷萨特、特雷莎特 | 2202 及同地点 | `YAMATO-SRC-SH0003-JA` | `confirmed` | 不简化为角色名“特蕾莎”。 |
| `YAMATO-TERM-0021` | 角色/机器人 | `アナライザー` | 分析士 | 分析器 | 2199 重制系列 | `YAMATO-SRC-SH0003-BASELINE` | `confirmed` | 作为角色名使用，不按普通名词直译。 |

## 待用户确认

无。SH0002 与 SH0003 的既有成品冲突已在历史提交中关闭，不构成系列规范待决项。尚未收入本表的音译人名和新续作术语不等于已经确认；引入新项目时必须先完成差异审计再扩充。

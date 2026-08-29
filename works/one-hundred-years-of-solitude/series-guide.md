# 百年孤独 系列术语规范

本文件是本系列唯一活动术语表，遵循 `$subtitle-hub` 的 `SH-TRANS-007`。所有术语、地名、人名、家族名、机构名及其他专有名词，优先以中文维基百科《百年孤独》小说词条定名；词条没有对应项时，使用本文件登记的最新可核实中文译本作为后备来源。

## 外部定名依据

| source_id | 类型 | 标题 | URL | 核验日期 | 用途与限制 |
| --- | --- | --- | --- | --- | --- |
| `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | 中文百科词条 | 百年孤独 | https://zh.wikipedia.org/wiki/百年孤独 | 2026-08-29 | 优先术语定名依据；采用词条的简体中文字段。词条括号说明、早期译名和繁体字段不直接复制进字幕。 |
| `SOLITUDE-SRC-NOVEL-LATEST-CN` | 中文小说译本 | 百年孤独 | https://weread.qq.com/web/bookDetail/8bc329705e46708bcb0c164 | 2026-08-29 | 维基百科小说词条未覆盖专名时的后备定名依据；[哥伦比亚]加西亚·马尔克斯著、范晔译，南海出版公司，2024年12月出版记录，ISBN `978-7-5735-1092-1`。仅采用译文中的专名，不将书目宣传文字带入字幕。 |

## 术语使用规则

1. 发现字幕译名与小说词条不一致时，采用小说词条的简体中文译名。
2. 小说词条没有明确简体中文对应项时，查用 `SOLITUDE-SRC-NOVEL-LATEST-CN`；若字幕译名与该译本冲突，采用该译本形式；已经一致的内容不改。
3. 电视剧词条、官方字幕、条目数据库和其他译本可以作为文本或身份材料，但不参与系列术语定名。
4. 小说词条与最新中文译本都没有对应项的剧集专名，不根据西语拼写、电视剧词条或常见译法自行改名，保留项目现行形式并记录证据边界。
5. 同一人物的简称、全名和称谓按已确认 canonical 形式保持一致；括号解释、早期译名和繁体字不进入字幕。
6. 每个术语都保留稳定 `term_id`、类别、原文、规范简体中文、变体、范围、证据和状态；只有 `confirmed` 项可作为机械替换依据。

## 小说词条规范术语

| term_id | 类别 | 原文 | 规范简体中文 | 禁用或待替换形式 | 适用范围 | source_id | 状态 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `SOLITUDE-TERM-001` | 作品标题 | `Cien años de soledad` | `百年孤独` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-002` | 地名 | `Macondo` | `马孔多` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-003` | 家族名 | `Buendía` | `布恩迪亚` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-004` | 人物 | `José Arcadio Buendía` | `何塞·阿尔卡蒂奥·布恩迪亚` | `何塞·阿卡蒂奥·布恩迪亚` | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-005` | 人物 | `Úrsula Iguarán` | `乌尔苏拉·伊瓜兰` | `乌苏拉·伊瓜兰` | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-006` | 人物 | `José Arcadio` | `何塞·阿尔卡蒂奥` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-007` | 人物/称谓 | `Coronel Aureliano Buendía` | `奥雷里亚诺·布恩迪亚上校` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-008` | 人物 | `Amaranta` / `Amaranta Buendía` | `阿玛兰妲` / `阿玛兰妲·布恩迪亚` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-009` | 人物 | `Rebeca` | `丽贝卡` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-010` | 人物 | `Remedios Moscote` | `蕾梅黛丝·摩斯科特` | `蕾梅蒂斯·摩斯科特` | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-011` | 人物 | `Arcadio` | `阿尔卡蒂奥` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-012` | 人物 | `Santa Sofía` | `桑塔索菲亚` | `圣塔苏菲亚` | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-013` | 人物 | `Aureliano José` | `奥雷里亚诺·何塞` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-014` | 人物 | `José Arcadio Segundo` | `何塞·阿尔卡蒂奥第二` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-015` | 人物 | `Aureliano Segundo` | `奥雷里亚诺第二` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-016` | 人物 | `Melquíades` | `梅尔基亚德斯` | `梅贾德斯` | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-017` | 人物 | `Pilar Ternera` | `庇拉尔·特尔内拉` | `皮拉·特内拉` | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-018` | 人物 | `Pietro Crespi` | `皮耶特·克雷斯皮` | `彼得罗·克莱斯皮` | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-019` | 人物 | `Nicanor Ulloa` | `尼卡诺尔·乌略亚` | `尼卡诺·乌略亚` | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-020` | 人物 | `Nicanor` | `尼卡诺尔` | `尼卡诺` | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-021` | 人物 | `Gerineldo Márquez` | `格林列尔多·马尔克斯` | `盖里奈多·马奎斯`、`盖里奈多` | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-022` | 人物 | `Fernanda del Carpio` | `费尔南达·德尔·卡皮奥` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-023` | 人物 | `Petra Cotes` | `佩特拉·科特斯` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |
| `SOLITUDE-TERM-024` | 人物/昵称 | `Renata Remedios “Meme” Buendía` | `雷纳塔·蕾梅黛丝`；昵称 `梅梅` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL`；`SOLITUDE-SRC-NOVEL-LATEST-CN` | confirmed |
| `SOLITUDE-TERM-025` | 人物 | `Aureliano Babilonia` | `奥雷里亚诺·巴比伦` | 无 | 全系列 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | confirmed |

## 小说词条未给出直接对应项的专名及后备译本核对

以下项目经小说词条之外的后备译本核对。`confirmed` 项只在字幕形式确实冲突时提出修改；`no-novel-correspondence` 项没有可移植的小说译名，不因音译推测而改动。

| term_id | 原文 | 后备译本规范简体中文 | SH0006 当前形式 | 状态 | 证据 |
| --- | --- | --- | --- | --- | --- |
| `SOLITUDE-TERM-026` | `Apolinar Moscote` | `阿波利纳尔·摩斯科特` | `阿波利纳·摩斯科特` | confirmed | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-027` | `Prudencio Aguilar` | `普鲁邓希奥·阿基拉尔` | `普鲁丹修·阿圭拉`、`普鲁丹修` | confirmed | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-028` | `Visitación` | `比西塔西翁` | `比希塔森` | confirmed | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-029` | `Cataure` | `卡塔乌雷` | `卡陶雷` | confirmed | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-030` | `Catarino` | `卡塔利诺` | `卡塔里诺` | confirmed | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-031` | `José Raquel Moncada` | `何塞·拉克尔·蒙卡达` | `何塞·拉奎·蒙卡达` | confirmed | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-032` | `Victoriano Medina` | `维多利奥·梅迪纳` | `维托里亚诺·梅迪纳` | confirmed | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-033` | `Rebeca Montiel` | `丽贝卡·蒙铁尔` | `丽贝卡·蒙铁尔` | confirmed-consistent | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-034` | `Coronel Carmona` | 无对应小说人物 | `卡莫纳` | no-novel-correspondence | `SOLITUDE-SRC-NOVEL-LATEST-CN`；剧集专名保留现行形式 |

状态只使用 `confirmed`、`confirmed-consistent`、`provisional`、`no-novel-correspondence` 或 `pending-user-confirmation`。歧义项确认前不得批量替换。

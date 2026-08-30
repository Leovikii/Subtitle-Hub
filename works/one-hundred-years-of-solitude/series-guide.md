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
| `SOLITUDE-TERM-026` | `Apolinar Moscote` | `阿波利纳尔·摩斯科特` | `阿波利纳尔·摩斯科特` | confirmed-consistent | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-027` | `Prudencio Aguilar` | `普鲁邓希奥·阿基拉尔` | `普鲁邓希奥·阿基拉尔`、`普鲁邓希奥` | confirmed-consistent | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-028` | `Visitación` | `比西塔西翁` | `比西塔西翁` | confirmed-consistent | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-029` | `Cataure` | `卡塔乌雷` | `卡塔乌雷` | confirmed-consistent | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-030` | `Catarino` | `卡塔利诺` | `卡塔利诺` | confirmed-consistent | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-031` | `José Raquel Moncada` | `何塞·拉克尔·蒙卡达` | `何塞·拉克尔·蒙卡达`、`何塞·拉克尔` | confirmed-consistent | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-032` | `Victoriano Medina` | `维多利奥·梅迪纳` | `维多利奥·梅迪纳` | confirmed-consistent | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-033` | `Rebeca Montiel` | `丽贝卡·蒙铁尔` | `丽贝卡·蒙铁尔` | confirmed-consistent | `SOLITUDE-SRC-NOVEL-LATEST-CN` |
| `SOLITUDE-TERM-034` | `Coronel Carmona` | 无对应小说人物 | `卡莫纳` | no-novel-correspondence | `SOLITUDE-SRC-NOVEL-LATEST-CN`；剧集专名保留现行形式 |

状态只使用 `confirmed`、`confirmed-consistent`、`provisional`、`no-novel-correspondence` 或 `pending-user-confirmation`。歧义项确认前不得批量替换。

## SH0006 全季实际表面形式闭合清单

以下清单来自 S01E01–S01E08 工作母本的完整双向文本扫描（2026-08-30）。只登记实际出现的源文或中文字幕表面形式；同一事件中出现全名和简称时分别记录。数量是中文字幕 `CN-Main` 可见事件数，源文数量以对应扫描结果为准。未列入本节的已确认形式，均按上表中的规范全名或已登记变体处理。

| term_id | 已确认实体 | 实际出现的源文形式 | 实际出现的中文形式 | 中文字幕事件数 | 处理状态与边界 |
| --- | --- | --- | --- | ---: | --- |
| `SOLITUDE-TERM-005` | Úrsula Iguarán | `Úrsula`、`Úrsula Iguarán` | `乌尔苏拉`、`乌尔苏拉·伊瓜兰`、`乌尔苏拉·伊瓜兰·布恩迪亚` | `乌尔苏拉` 短称 69；规范全名及扩展称谓保留实体映射 | 旧形式 `乌苏拉` 已清零；完整姓名及扩展称谓保留实体映射。 |
| `SOLITUDE-TERM-017` | Pilar Ternera | `Pilar`、`Pilar Ternera` | `庇拉尔`、`庇拉尔·特尔内拉` | `庇拉尔` 短称 11；规范全名 5 | 旧形式 `皮拉` 已清零；11 个短称均与源文 `Pilar` 对齐。 |
| `SOLITUDE-TERM-021` | Gerineldo Márquez | `Gerineldo`、`Gerineldo Márquez` | `格林列尔多·马尔克斯` | 规范形式 3；旧缺字形式 0 | 全季完整事件边界检查未发现独立的 `格林列尔多·马尔克` 错字；不按字符串前缀扫描规范形式。 |
| `SOLITUDE-TERM-025` | Aureliano Babilonia | `Aureliano Babilonia` | `奥雷里亚诺·巴比伦` | 1 | 旧形式 `奥雷里亚诺·巴比罗尼亚` 已清零；与源文同一事件对齐。 |
| `SOLITUDE-TERM-012` | Santa Sofía de la Piedad | `Santa Sofía de la Piedad` | `桑塔索菲亚·德拉·皮埃达` | 2 | 这是已确认人物的扩展全名；小说词条/后备译本的细分写法尚未形成变更决定，暂保留并标记为 `provisional`。 |
| `SOLITUDE-TERM-020` | Nicanor / Nicanor Reyna | `Nicanor`、`Nicanor Reyna` | `尼卡诺尔`、`尼卡诺尔·雷纳` | `尼卡诺尔·雷纳` 1 | 全名与神父称谓的简称属于同一人物；`尼卡诺`只作为独立称谓候选检查，不能把`尼卡诺尔`的前缀误判为禁用形式。 |
| `SOLITUDE-TERM-009` | Rebeca / Rebeca Montiel | `Rebeca`、`Rebeca Montiel` | `丽贝卡`、`丽贝卡·蒙铁尔`、`丽贝卡·布恩迪亚` | `丽贝卡·布恩迪亚` 3 | `丽贝卡·布恩迪亚`是剧情中的婚后家族名组合，登记为实体变体，不因与娘家名不同而改写。 |
| `SOLITUDE-TERM-031` | José Raquel Moncada | `José Raquel`、`José Raquel Moncada` | `何塞·拉克尔`、`何塞·拉克尔·蒙卡达` | 简称 3；全名 2 | 简称、全名和将军称谓均已确认指向同一人物；保留短称，不盲目补全。 |

## 无小说词条对应的剧集专名闭合登记

以下表面形式在完整范围内实际出现，但中文维基百科小说词条没有对应人物。依据系列规则不凭西语拼写臆造小说译名；它们是项目现行形式的排除项或待确认项，不纳入本轮机械替换。

| 实体源文 | 实际中文形式 | 实际出现范围 | 状态 | 说明 |
| --- | --- | --- | --- | --- |
| `Roque Carnicero` | `罗克·卡尼塞罗`、`卡尼塞罗` | S01E07–S01E08，3 条 | `no-novel-correspondence` | 简称已由同一源文上下文确认。 |
| `Alirio Noguera` / `Noguera` | `艾利洛·诺盖拉`、`诺盖拉` | S01E05–S01E06，9 条 | `no-novel-correspondence` | 全名与姓氏简称已由源文对齐，暂不按音译另改。 |
| `Gregorio Stevenson` | `格雷戈·史蒂文森` | S01E07，2 条 | `no-novel-correspondence` | 剧集人物，小说词条无对应项。 |
| `Napoleón Bonaparte` | `拿破仑·波拿巴` | S01E07，1 条 | `no-novel-correspondence` | 历史人物画面文字，保留现行形式。 |
| `Gabriel García Márquez` | `加夫列尔·加西亚·马尔克斯` | S01E01–S01E08，8 条 | `no-novel-correspondence` | 作者署名画面文字，不作为剧中人物译名处理。 |

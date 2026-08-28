# 百年孤独 系列用语规范

本文件是本系列唯一活动术语表，遵循 `$subtitle-hub` 的 `SH-TRANS-007`。项目不得复制本表；差异只能在项目 `project.yaml` 通过 `term_id` 明确覆盖。

## 来源

| source_id | 类型 | 标题 | URL 或仓库路径 | 核验日期 | 用途与限制 |
| --- | --- | --- | --- | --- | --- |
| `SOLITUDE-SRC-BANGUMI-276863` | 条目数据库 | Cien años de soledad / 百年孤独 | https://bgm.tv/subject/276863 | 2026-08-28 | 核对作品身份、欧美剧类型和条目总集数；本项目范围由用户确认只处理 S01E01–S01E08。 |
| `SOLITUDE-SRC-NETFLIX-BILINGUAL` | 官方双语字幕 | 百年孤独 Netflix 中西双语字幕 | `SH0006--one-hundred-years-of-solitude-s01/project/sources/subtitles/zh-Hans/official-netflix-bilingual` | 2026-08-28 | 西语原文与中文字幕官方译本；中文字幕提供本项目唯一时间轴。 |
| `SOLITUDE-SRC-WIKIPEDIA-ZH-TV` | 中文百科词条 | 百年孤独 (电视剧) | https://zh.wikipedia.org/wiki/百年孤独_(电视剧) | 2026-08-28 | 与本版本中文字幕比对作品标题、地点和角色译名；词条内部存在个别译名不一致，冲突项不直接确认。 |
| `SOLITUDE-SRC-WIKIPEDIA-NOVEL` | 中文百科词条 | 百年孤独 | https://zh.wikipedia.org/wiki/百年孤独 | 2026-08-28 | 用户指定的小说词条；作为系列冲突专名的优先外部基准。词条中的括号说明不直接复制进字幕。 |

## 规范术语

| term_id | 类别 | 西语原词 | 规范简体中文 | 禁用或待替换形式 | 适用范围 | source_id | 状态 | 备注 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SOLITUDE-TERM-001` | 作品标题 | `Cien años de soledad` | `百年孤独` | 无 | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-ZH-TV`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 本版本与中文维基词条一致。 |
| `SOLITUDE-TERM-002` | 地名 | `Macondo` | `马孔多` | 无 | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-ZH-TV`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 本版本与中文维基词条一致。 |
| `SOLITUDE-TERM-003` | 人物 | `Coronel Aureliano Buendía` | `奥雷里亚诺·布恩迪亚上校` | 无 | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 小说词条人物标题写作“奥雷里亚诺·布恩迪亚（上校）”；字幕采用自然称谓顺序。 |
| `SOLITUDE-TERM-004` | 人物 | `Amaranta` | `阿玛兰妲` | 无 | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-ZH-TV`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 本版本与中文维基词条一致。 |
| `SOLITUDE-TERM-005` | 人物 | `Rebeca` | `丽贝卡` | 无 | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-ZH-TV`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 本版本与中文维基词条一致。 |
| `SOLITUDE-TERM-006` | 人物 | `Melquíades` | `梅尔基亚德斯` | `梅贾德斯` | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 按用户决定采用小说词条译名；已在 SH0006 全季统一替换。 |
| `SOLITUDE-TERM-007` | 人物 | `José Arcadio Buendía` | `何塞·阿尔卡蒂奥·布恩迪亚` | `何塞·阿卡蒂奥·布恩迪亚` | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 按用户决定采用小说词条译名；已在 SH0006 全季统一替换。 |
| `SOLITUDE-TERM-008` | 人物 | `Úrsula Iguarán` | `乌尔苏拉·伊瓜兰` | `乌苏拉·伊瓜兰` | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 按用户决定采用小说词条译名；已在 SH0006 全季统一替换。 |
| `SOLITUDE-TERM-009` | 人物 | `Remedios Moscote` | `蕾梅黛丝·摩斯科特` | `蕾梅蒂斯·摩斯科特` | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 采用小说词条人物译名；电视剧词条内部变体不采用。 |
| `SOLITUDE-TERM-010` | 人物 | `Gabriel García Márquez` | `加夫列尔·加西亚·马尔克斯` | `加夫列尔·贾西亚·马尔奎斯` | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 采用小说词条及本版本片尾一致的译名。 |
| `SOLITUDE-TERM-011` | 人物 | `Pilar Ternera` | `庇拉尔·特尔内拉` | `皮拉·特内拉` | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 采用小说词条译名；已在 SH0006 全季统一替换。 |
| `SOLITUDE-TERM-012` | 人物 | `Pietro Crespi` | `皮耶特·克雷斯皮` | `彼得罗·克莱斯皮` | 系列及本项目 S01E01–S01E08 | `SOLITUDE-SRC-WIKIPEDIA-NOVEL`；`SOLITUDE-SRC-NETFLIX-BILINGUAL` | confirmed | 采用小说词条译名；已在 SH0006 全季统一替换。 |

状态只使用 `confirmed`、`provisional` 或 `pending-user-confirmation`。歧义项确认前不得批量替换。

## 已确认的小说词条冲突处理

| term_id | 原词 | 本版本译名 | 维基词条译名或冲突 | 影响项目 | 待确认问题 |
| --- | --- | --- | --- | --- | --- |
| `SOLITUDE-TERM-PENDING-001` | `José Arcadio Buendía` | 何塞·阿卡蒂奥·布恩迪亚 | 何塞·阿尔卡蒂奥·布恩迪亚 | SH0006 | 已按用户决定采用小说词条译名并在项目中统一替换。 |
| `SOLITUDE-TERM-PENDING-002` | `Úrsula Iguarán` | 乌苏拉·伊瓜兰 | 乌尔苏拉·伊瓜兰 | SH0006 | 已按用户决定采用小说词条译名并在项目中统一替换。 |
| `SOLITUDE-TERM-PENDING-003` | `Apolinar Moscote` | 阿波利纳·摩斯科特 | 小说主词条未找到明确对应项；电视剧词条为阿波利纳尔·摩斯科特 | SH0006 | 暂不静默替换；该项仍需以可定位的小说词条证据解决。 |
| `SOLITUDE-TERM-PENDING-004` | `Remedios Moscote` | 蕾梅黛丝·摩斯科特 | 演员表为“蕾梅黛丝·摩斯科特”，第 5 集标题为“蕾梅蒂斯·摩斯科特” | SH0006 | 已按用户决定采用小说词条译名并在项目中统一替换。 |
| `SOLITUDE-TERM-PENDING-005` | `Gabriel García Márquez` | 加夫列尔·加西亚·马尔克斯 | 词条部分位置同本版本，正文另有“加夫列尔·贾西亚·马奎斯” | SH0006 | 已按用户决定采用小说词条及片尾一致形式并在项目中统一替换。 |

本项目中出现的其他人物译名在该电视剧词条中未找到明确对应，不作为“完全相同”项自动加入术语表。

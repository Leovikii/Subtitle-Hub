---
schema_version: 3
work_id: SH0006
updated_at: "2026-08-29"
baseline_release: 1.0.1
target_release: 1.0.2
status: released
scope: S01E01-S01E08

coverage:
  evidence_tier: B
  timing_authority: user-confirmed Chinese subtitle timing
  master_sha256:
    S01E01: e24ce8e4fce93ec715cb2d0427296f4ccd109dec101b6c973074d4391071de6d
    S01E02: 0d10e4c1c351bb5016a14418335e0892cafffdd2b5288c7938e9432a2f577241
    S01E03: 2fda434485aa04b5cb9a3ed093523b4dbb50c68e1c97667b542dc0eb63487d84
    S01E04: c8e6c240bbc6beff04b9791f4e796cfbf9b7dca3bbeaec767057e6a79c2774fa
    S01E05: 0c09af00c07867c08953404870d9b3e14f3dc8a3bb33a2130c2ee1d47c57e90c
    S01E06: fa65a0d412eb6af21bdee6254308eaafa85ec4dd845adb64af65a119b5bab326
    S01E07: ba6b258ac61291503495823b2177b5adbd2d99e115949cd47e201a529b3f3681
    S01E08: 2664ef9138755ca4ebcbcd1e7e2f188d627a2027ff8f8935ca0804efc30c4c32
  chinese_in_scope: 3844
  chinese_reviewed: 3844
  chinese_excluded: 0
  source_in_scope: 3599
  source_aligned: 3599
  source_unresolved: 0
  static_layout_checked: 7443
  human_source_fidelity_review: not-claimed
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
---

# 当前校对轮次

## 目标与范围

基于已发布的 1.0.1，按 `$subtitle-hub` Skill 1.3.2 对 S01E01–S01E08 全部母本重新执行文本、术语、双语结构和静态布局检查，目标为 1.0.2。4 项获批修订已实施到工作母本，1.0.2 候选已人工审核通过并提升为正式发布版本；`project/sources/` 保持不变。

项目继续使用用户批准的无视频例外：截图确认的 Netflix 视频文件名仅用于目标身份和集数映射；中文事件起止时间仍是唯一时间轴权威；西语为源文本参照，并删除与中文内容不匹配的西语无障碍片段。没有视频或音频，因此不宣称播放、听辨或视觉核验完成。

## 检查覆盖

- 8 集共 3,844 条可见中文 `Dialogue` 事件，排除 0 条；本轮完成全范围结构、术语表面形式、时间码、字体、样式引用和静态布局检查。
- 源文共 3,599 条事件，完成双向事件结构扫描；源文与中文字幕的不同事件切分仍按已确认的中西双语映射解释，不据此擅自改动时间轴。
- 全部 7,443 条 `Dialogue` 完成静态审计：结构性确认错误 0；预测换行风险 228；中文无源重叠风险 252；西语无中文重叠风险 6；需媒体才能定性的候选 4。上述风险不等同于确认缺陷。
- 术语审计使用临时 schema-1 manifest `audit_terms.py` 完成双向扫描。实施后禁用形式命中 0；`乌苏拉`、`皮拉`、`奥雷里亚诺·巴比罗尼亚` 均无残留。`格林列尔多·马尔克`以完整事件匹配检查，未误报正确的`格林列尔多·马尔克斯`，旧错字无残留。
- 已将全季实际出现的简称、全名、婚后家族名、称谓和剧集专名写入系列 `series-guide.md`；未出现的别名未被虚构，小说词条没有对应项的剧集专名列为保留/排除项。

## 校对方案

规则优先级为用户已确认的系列术语与本轮项目覆盖项：小说词条 canonical 形式优先；小说词条没有对应项时沿用已登记的范晔译本后备形式；不改中文时间轴；不将源文省略的人名强行补入；短名和称谓只在已确认实体后纳入批量。

| item_id | 集数/时间或范围 | 类别 | 修改前 | 建议结果 | 证据/理由 | 严重性/风险 | 决定 | 状态 | 实际结果 | 验证 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SH0006-TERM-1.0.2-001` | 全季；S01E01 10 条、E02 15 条、E03 6 条、E04 8 条、E05 11 条、E06 2 条、E07 12 条、E08 5 条，共 69 条 | 人名表面形式批次 | `乌苏拉` | `乌尔苏拉` | 源文实体为 `Úrsula`；系列词条 canonical 为 `乌尔苏拉·伊瓜兰`。排除已正确的 `乌尔苏拉·伊瓜兰`、`乌尔苏拉·伊瓜兰·布恩迪亚` 及其称谓 | P1 | 已批准 | implemented-verified | 已替换 69 条 | 术语审计禁用命中 0；时间字段保持不变 |
| `SH0006-TERM-1.0.2-002` | S01E02 8 条、S01E05 1 条、S01E07 2 条，共 11 条 | 人名短称批次 | `皮拉` | `庇拉尔` | 全部与源文 `Pilar` 对齐；系列词条 canonical 为 `庇拉尔·特尔内拉`。排除已有规范全名 `庇拉尔·特尔内拉` | P1 | 已批准 | implemented-verified | 已替换 11 条 | 术语审计禁用命中 0；全名和简称映射保留 |
| `SH0006-TERM-1.0.2-003` | S01E05 00:07:58.42–00:08:00.71 | 人名错字 | `格林列尔多·马尔克` | `格林列尔多·马尔克斯` | 同时段源文为 `Gerineldo Márquez`；现行形式漏掉姓氏末字。仅改这一完整事件，不按前缀批量处理 | P1 | 已批准 | implemented-verified | 已替换 1 条 | 完整事件匹配通过；无双“斯”或旧形残留 |
| `SH0006-TERM-1.0.2-004` | S01E08 00:49:36.46–00:49:38.04 | 人名错译/术语冲突 | `奥雷里亚诺·巴比罗尼亚` | `奥雷里亚诺·巴比伦` | 同时段源文为 `Aureliano Babilonia`；系列小说词条 canonical 为 `奥雷里亚诺·巴比伦` | P1 | 已批准 | implemented-verified | 已替换 1 条 | 术语审计禁用命中 0；全季无旧形 |

## 已登记但本轮不擅自改名的实际形式

这些形式已完成实体归属登记，不构成待改字幕项：

- `桑塔索菲亚·德拉·皮埃达` 2 条：`Santa Sofía de la Piedad` 的扩展全名；与 `SOLITUDE-TERM-012` 关联，细分写法暂无充分冲突证据，暂保留为 `provisional`。
- `尼卡诺尔·雷纳` 1 条：`Nicanor Reyna` 的全名；与 `SOLITUDE-TERM-020` 的 `尼卡诺尔` 关联，登记为全名/称谓变体。
- `丽贝卡·布恩迪亚` 3 条：`Rebeca` 的婚后家族名组合；与 `SOLITUDE-TERM-009` / `SOLITUDE-TERM-033` 关联，保留。
- `何塞·拉克尔` 5 条：`José Raquel Moncada` 的简称；与 `SOLITUDE-TERM-031` 关联，保留简称及将军称谓。
- `罗克·卡尼塞罗`、`卡尼塞罗` 共 3 条；`艾利洛·诺盖拉`、`诺盖拉` 共 9 条；`格雷戈·史蒂文森` 2 条：均为小说词条没有对应项的剧集专名，按系列规则保留。
- `拿破仑·波拿巴` 1 条及 `加夫列尔·加西亚·马尔克斯` 8 条：画面文字中的历史人物/作者署名，非本剧人物术语，保留。

## 决策与实施

本轮 4 个字幕修改项已获用户批准并实施到 8 个工作母本；中文时间轴、事件结构和西语文本未改动。1.0.2 候选已通过用户发行前人工核对，正式目录已完成轮换；`subtitles/previous/` 保留 1.0.1。

## 验证与剩余风险

- 项目已满足 schema 9、review schema 3 和 Skill 1.3.2；`validate_project.py --ready-for-proofreading` 已通过。
- 变更后术语双向审计已完成，所有已登记禁用形式为零；8 个 1.0.2 发布文件已由发行验证器通过，发布 Events 与母本的渲染内容一致。
- `validate_project.py --release` 已通过，确认 `current=1.0.2`、`previous=1.0.1`、版本标记、文件名、字体和发布结构有效。`build_subtitle_packages.py --check` 仅报告旧的 1.0.1 ZIP 为 stale；未在本地写入或删除 ZIP，交由 GitHub Actions 重建。
- 无视频/音频，因此本轮不宣称时间轴播放核验、听辨、镜头边界、画面遮挡或全片视觉核验。现有静态审计中的风险候选仅作记录，不自动改写。

## 发行前审核

状态：用户已通过 1.0.2 发行前人工核对；1.0.2 已发布，1.0.1 已保留为回滚版本。

## 后续门禁

1.0.2 已完成正式目录轮换。已运行本地 `build_subtitle_packages.py --check`；ZIP、校验和及目录索引由 GitHub Actions 负责。

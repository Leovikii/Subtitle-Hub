---
schema_version: 3
work_id: SH0006
updated_at: "2026-08-29"
baseline_release: 1.0.0
target_release: 1.0.1
status: released
scope: S01E01-S01E08

coverage:
  evidence_tier: B
  timing_authority: user-confirmed Chinese subtitle timing
  master_sha256:
    S01E01: fd758550ac59f2cd75fb551f63eee600a8fde6aa4e3b16c00fd6e6aa4631805c
    S01E02: 14abcb3db8bd76c03a6aa3f67846e04630a212393ce14ae59c01d8a68ab6f68a
    S01E03: 3f4e8186a32757899387a2b0a3874d5aa25264dac1689e246d7b6080489f3729
    S01E04: 08cc5ae84d8ac48e8a18152152299b481f3b2c621baf95ce4e018784562b75ab
    S01E05: 53500ea8283f303f9bf1d81652520eddd5308646f4d22e7e206e58b06e0e471c
    S01E06: 9ca418a156226df316bf33d40c2d8de09845eaf6359064e46449571ad9093782
    S01E07: f5daddf6063771666a6b25bdaf52897de16f79dc04515d9e681ba80533724c8b
    S01E08: 59fdf30883a7611b134c7083c04f51347b46784128901481c94dcb344622c6d5
  chinese_in_scope: 3844
  chinese_reviewed: 3844
  chinese_excluded: 0
  source_in_scope: 3599
  source_aligned: 3599
  source_unresolved: 0
  static_layout_checked: 7443
  human_source_fidelity_review: not-required
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

按 Subtitle Hub Skill 1.3.0 重新审查并校对 S01E01–S01E08 全部字幕，目标版本为 1.0.1。中文事件的起止时间完全沿用用户确认的中文时间轴；西语仅作为源文本参照，并同步到中文事件结构。保留西语中与中文内容对应的无障碍文本，删除无中文对应的多余听觉无障碍/描述性片段。

项目按用户批准的无视频例外执行：截图确认的八个 Netflix 视频文件名用于目标身份和集数映射，但未提供视频二进制。本轮不宣称音频、镜头、播放或全片视觉核验；静态排版审计仅依据 ASS 几何和事件结构完成。

## 检查覆盖

- 中文覆盖：8 集共 3,844 条可见中文 Dialogue 事件，全部逐事件检查，排除 0 条。
- 源文本覆盖：3,599 条西语事件均完成双向事件结构对照，当前未留下未解析源文本单元。
- 静态覆盖：母本全部 7,443 条 Dialogue 事件完成结构、时间、字体、样式引用、双语堆叠和静态布局审计。
- 证据等级：B（中文底稿与匹配西语源文本；完成双向文本覆盖；中文时间轴由用户确认；无视频导致不作人工源语听辨和播放核验声明）。
- 自动审计候选已逐项判断：预测换行、跨语言边界和短时长候选主要是双语事件切分或特殊/无障碍文本，不在缺乏视频证据时批量改写。

## 校对方案

用户已批准：中文译本以西语匹配字幕核对；专有名词优先采用中文维基百科《百年孤独》小说词条；小说词条没有对应项时采用范晔译、南海出版公司 2024 年版；中文时间轴为唯一权威；西语多余无障碍文本删除。所有实质修改逐项登记如下。

| item_id | 集数/时间或范围 | 类别 | 修改前 | 建议结果 | 证据/理由 | 严重性/风险 | 决定 | 状态 | 实际结果 | 验证 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SH0006-TERM-GUIDE-001 | 全系列术语表 | 规范收敛 | 多来源混用 | 仅以中文维基百科小说词条定名 | 用户批准术语表规则 | P1 | 已批准 | implemented-verified | series-guide 已收敛为小说词条主依据并登记后备译本 | 旧形扫描通过 |
| SH0006-TERM-002 | S01E03 00:01:53–00:01:57 | 人名 | 尼卡诺·乌略亚 | 尼卡诺尔·乌略亚 | 小说词条规范形式 | P1 | 已批准 | implemented-verified | 已替换 | 文本扫描通过 |
| SH0006-TERM-003 | 全季 | 人名 | 盖里奈多·马奎斯、盖里奈多 | 格林列尔多·马尔克斯、格林列尔多 | 小说词条规范形式 | P1 | 已批准 | implemented-verified | 已统一 | 旧形无残留 |
| SH0006-TERM-004 | S01E07–S01E08 | 人名/称谓 | 尼卡诺神父 | 尼卡诺尔神父 | 小说词条规范形式 | P1 | 已批准 | implemented-verified | 已替换 | 全季扫描通过 |
| SH0006-TERM-005 | 全季 | 后备专名 | 多项与范晔译本不一致 | 采用范晔译本形式；无对应项保留剧集现行名 | 用户批准后备来源规则 | P1 | 已批准 | implemented-verified | 后备冲突项已实施 | 术语扫描通过 |
| SH0006-TERM-006 | S01E03–S01E06 | 人名 | 阿波利纳·摩斯科特 | 阿波利纳尔·摩斯科特 | 范晔译本 | P1 | 已批准 | implemented-verified | 5 处已替换 | 无旧形残留 |
| SH0006-TERM-007 | S01E01–S01E08 | 人名 | 普鲁丹修·阿圭拉、普鲁丹修 | 普鲁邓希奥·阿基拉尔、普鲁邓希奥 | 范晔译本 | P1 | 已批准 | implemented-verified | 9 处已统一 | 无旧形残留 |
| SH0006-TERM-008 | S01E02–S01E07 | 人名 | 比希塔森 | 比西塔西翁 | 范晔译本 | P1 | 已批准 | implemented-verified | 13 处已替换 | 无旧形残留 |
| SH0006-TERM-009 | S01E02–S01E03 | 人名 | 卡陶雷 | 卡塔乌雷 | 范晔译本 | P1 | 已批准 | implemented-verified | 7 处已替换 | 无旧形残留 |
| SH0006-TERM-010 | S01E02–S01E07 | 人名 | 卡塔里诺 | 卡塔利诺 | 范晔译本 | P1 | 已批准 | implemented-verified | 19 处已替换 | 无旧形残留 |
| SH0006-TERM-011 | S01E08 | 人名 | 何塞·拉奎·蒙卡达 | 何塞·拉克尔·蒙卡达 | 范晔译本 | P1 | 已批准 | implemented-verified | 2 处已替换 | 文本扫描通过 |
| SH0006-TERM-012 | S01E08 00:16:09.58–00:16:13.42 | 人名 | 维托里亚诺·梅迪纳上校 | 维多利奥·梅迪纳上校 | 范晔译本 | P1 | 已批准 | implemented-verified | 1 处已替换 | 文本扫描通过 |
| SH0006-TERM-013 | S01E03 | 人名 | 丽贝卡·蒙铁尔 | 保持不变 | 范晔译本一致 | P2 | 已确认 | confirmed-consistent | 保持 | 对照通过 |
| SH0006-TERM-014 | S01E07 | 剧集专名 | 卡莫纳 | 保持不变 | 小说和后备译本无对应人物，禁止臆改 | P2 | 已确认 | confirmed-consistent | 保持 | 边界记录完整 |
| SH0006-REV-001 | S01E01 00:07:55.58–00:08:01.00 | 重复/分段 | 第一事件重复刺绣信息 | 第一事件改为“白天 他照料自己养的斗鸡” | 西语两事件分别表达斗鸡和刺绣 | P2 | 已批准 | implemented-verified | 已修订 | 事件结构通过 |
| SH0006-REV-002 | S01E01 00:10:57.71–00:11:07.67 | 漏译/重复 | 过来 小可爱；后续重复短句 | “过来 小可爱 你中毒了”；删除无源重复事件 | 对齐西语 `Venga acá. Está envenenado.` | P1 | 已批准 | implemented-verified | 已修订 | 源文本覆盖通过 |
| SH0006-REV-003 | S01E01 00:26:18.75–00:26:23.75 | 双语错配/分段 | 中文按不自然顺序分两事件 | 合并为完整中文句，西语保持自然顺序 | 保持中文时间范围并修复中西语义错位 | P1 | 已批准 | implemented-verified | 已修订 | 双语结构通过 |
| SH0006-REV-004 | S01E02 00:02:45.83–00:02:49.88 | 误译 | 穿尖头靴戴耳环的阿拉伯人 | 穿拖鞋戴耳环的阿拉伯人 | `pantuflas` 为拖鞋 | P1 | 已批准 | implemented-verified | 已修订 | 逐事件对照通过 |
| SH0006-REV-005 | S01E05 00:11:20.25–00:11:22.67 | 错字 | 改死 | 该死 | 固定表达 | P2 | 已批准 | implemented-verified | 已修订 | 字符扫描通过 |
| SH0006-REV-006 | S01E05 00:48:46.67–00:48:51.88 | 语病/信达雅 | 浸染在自己的血液里中毒而死 | 蕾梅黛丝因自己的血液中毒而死 | 修复施受关系和中文语病 | P2 | 已批准 | implemented-verified | 已修订 | 逐事件对照通过 |
| SH0006-REV-007 | S01E06 00:19:56.04–00:19:59.75 | 误译 | 喝下瓶中的液体 | 服下瓶中的药丸 | `globulitos` 为药丸 | P1 | 已批准 | implemented-verified | 已修订 | 源文本一致 |
| SH0006-REV-008 | S01E06 00:34:22.71–00:34:26.92 | 误译/动作类型 | 一系列武装起义 | 全国各地正在协调一系列武装袭击 | `atentados` 指袭击 | P1 | 已批准 | implemented-verified | 已修订 | 逐事件对照通过 |
| SH0006-REV-009 | S01E07 00:15:51.88–00:15:53.12 | 双语错配 | 她晕倒了 | 醒醒 | `Despierta` 为唤醒指令 | P1 | 已批准 | implemented-verified | 已修订 | 逐事件对照通过 |
| SH0006-REV-010 | S01E08 00:11:32.50–00:11:36.08 | 重复/语病 | 深沉的愤怒愤怒于这人为带来的死亡 | 只有深沉的愤怒 源于这场人为制造的死亡 | 修复重复词和搭配 | P2 | 已批准 | implemented-verified | 已修订 | 逐事件对照通过 |

## 决策与实施

以上用户批准范围已连续实施于 8 个工作母本；没有编辑 `project/sources/` 或 `subtitles/current/`。母本已按新版规范全局使用 `Noto Sans CJK SC`，中文时间轴保持不变，西语事件按中文结构同步，未匹配的西语 SDH 片段按批准规则删除。Renata Remedios “Meme” Buendía 的昵称“梅梅”本季没有出现在字幕中，因此没有增译或补入。

本轮实际静态审计结果：结构性确认错误 0；预测换行风险 228；中文无源时间重叠候选 252；西语无中文重叠候选 6；短时长媒体候选 4。它们均不是在无视频条件下可直接确认的字幕错误，已保留为限制说明或候选风险，不伪称已完成视觉核验。

## 验证与剩余风险

- `project.yaml` 已迁移至 schema 9；无视频项目的 `project/local.paths.yaml` 已移除。
- 8 个母本均可解析，PlayRes 为 1920×1080，WrapStyle 为 0，样式和内联字体均为 Noto 字体，未发现旧术语残留。
- 1.0.1 候选已构建于 `project/workspace/build/current-candidate/`：8 个文件，版本头为 1.0.1；候选共 7,443 条事件、3,844 条中文事件和 3,599 条西语事件。
- 候选与母本的可见事件（时间、样式、文本）逐集完全一致；候选文件名、双语头字段、ASS 结构、Noto 字体和目标视频映射已检查。
- 候选静态审计确认错误 0；风险候选为预测换行 228、中文无源重叠 252、西语无中文重叠 6、短时长 4。风险候选不等同于缺陷，需视频或人工画面证据才能升级。
- 项目门禁通过；仓库 `$subtitle-hub` 技能测试 43/43 通过。
- 当前 P0/P1 未解决数为 0；静态风险不等同于确认缺陷。
- 用户已批准发行 1.0.1，`human_release_review` 已记录为 `verified`；本次发布仍明确接受无视频、无音频和无播放核验限制。

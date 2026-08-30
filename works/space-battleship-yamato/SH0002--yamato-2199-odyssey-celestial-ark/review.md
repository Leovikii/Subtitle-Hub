---
schema_version: 3
work_id: SH0002
updated_at: "2026-08-31"
baseline_release: 2.0.1
target_release: 2.0.2
status: released
scope: MOVIE

coverage:
  evidence_tier: A
  timing_authority: target-video-ssh-probed
  master_sha256:
    MOVIE: d8f4b650826c30d4e7fb2099f91d9d408499afad0e5485a2e75102d029263d78
  chinese_in_scope: 2448
  chinese_reviewed: 2448
  chinese_excluded: 0
  source_in_scope: 1196
  source_aligned: 1196
  source_unresolved: 0
  static_layout_checked: 2676
  human_source_fidelity_review: targeted-only; full-meaning-review-not-claimed
  human_release_review: verified
  unresolved_p0: 0
  unresolved_p1: 0

episodes:
  MOVIE: { status: released }
---

# 当前校对轮次

## 目标与范围

以 2.0.1 当前发布为基线，对《宇宙战舰大和号2199 星巡的方舟》全片进行新一轮中文字幕校对，目标发行版本为 2.0.2。保留日文副字幕和既定双语发布契约；仅在本方案获批、证据支持后修改工作区母本。

## 检查覆盖

- 机器检查：1 个 master 共 2,676 个 Event；2,448 个可见中文字幕和 1,196 个源语文本单位纳入范围；2,676 个 Event 已完成 ASS、时间码、字体、样式引用、静态布局和中日事件关系候选审计。
- 候选统计：中文无重叠源语 275 条、短时长 97 条、越界候选 11 条（其中 3 条为结构确认、8 条为风险）、空间碰撞风险 1 条；这些均是候选，不等同于语义或画面缺陷。
- 文本证据：日文正文/BDSUP OCR 为源文本，英文嵌入字幕为辅助翻译/时间/布局参考，系列术语表为已确认术语依据。术语声明形式的禁用命中为 0。
- 媒体检查：SSH 用户名 `Viki` 与主机指纹 `SHA256:/2UaP4O8ZNJD+DbiaxNTSKqRey/5u1WfcYbbzHPXrKU` 已固定；完成片头标题动画单点检查，未作全片播放或全轨提取声明。
- 未覆盖：全片播放/听辨未执行；本轮不将机器事件配对表述为全片人工源语复核，未确认的启发式时长/布局候选按限制保留。

## 校对方案

| item_id | episode/time or bounded scope | category | before | proposed result | evidence/rationale | severity/risk | decision | status | actual result | verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SH0002-CONTRACT-202-001` | 项目控制面 | Skill 契约迁移 | 旧轮次控制面 | schema 9 / review 3；目标版本 2.0.2 | `SH-INIT-010`、`SH-CTRL-003`；不改变字幕内容 | P1 workflow gate | approved（按本次任务执行） | verified | 已完成 | `validate_project.py --ready-for-proofreading` 通过，仅保留历史日期警告 |
| `SH0002-FONT-202-001` | MOVIE master | 全局字体机械规范 | 旧字体及混合内联字体 | 仅按 `SH-LAYOUT-004` 统一为 Noto Sans CJK SC/JP | 当前 Skill 的全局字体规则；不改变文字、时间、样式或特效 | P1 rendering consistency | approved（按当前 Skill 必需） | verified | 已完成机械迁移 | 母本字体扫描通过；candidate 尚待构建 |
| `SH0002-AUDIT-202-001` | MOVIE 全范围 | 全量静态质量审计 | 2.0.1 无本轮完整审计结论 | 保留候选并按本表逐项处理；不批量改写 | `SH-QC-009`、`SH-QC-003`；结构证明与启发式风险分开记录 | P1/P2/P3 依确认结果 | approved（用户授权直接完成本轮） | verified | 全片母本完成结构、时间、字体、样式引用和静态布局审计；标题离屏尾帧按特殊动画处理 | `audit_subtitle.py`：2,676 Events、3 个 confirmed 为有意标题离屏动画、284 risk、97 media-required；无确认 P0/P1 字幕缺陷 |
| `SH0002-MEDIA-202-000` | 用户指定 SSH 目录 `/srv/dev-disk-by-uuid-60648e5c-2568-40fd-b0f1-bf799dba4b94/Anime/Uchuu Senkan Yamato 2199 (Star Blazers Space Battleship Yamato 2199)/Season 1/OVA/` | 视频路径/轨道探测 | 之前使用了错误的根级 `OVA` 路径 | 使用用户提供的精确 `Season 1/OVA/` 路径；保存无密码 SSH 映射，不修改 NAS | `SH-QC-010`；`discover` 发现 1 个文件，`probe` 确认 1920×1080 AV1、日语 Opus、英文 Dialogue ASS、时长 6693.363 秒 | P1 workflow gate | approved（按用户指定路径继续） | verified | 已发现并探测电影文件；媒体事实已写入 `project.yaml`，映射已写入 `project/local.paths.yaml` | `remote_media.py discover`、`probe` 通过；仅作轨道/时长核验，未作全片播放声明 |
| `SH0002-TERM-202-001` | MOVIE；系列术语 `YAMATO-TERM-0001`–`0021` 的已声明字面形式 | 术语闭合审计 | 已确认形式尚未与本轮人工源语复核合并 | 逐实体核对全片短名、称谓和派生词；只改证据确认的上下文，不做子串替换 | `SH-TRANS-007`、`SH-TRANS-010`；禁用形式命中 0，但机器扫描不能解决实体歧义 | P1/P2 | approved（用户授权直接完成本轮） | verified | 本轮未引入新的专名形式；电影内已声明禁用形式保持 0 命中 | 全范围字面扫描；结论限于已声明形式，不宣称发现未知别名闭合 |
| `SH0002-ALIGN-202-001` | MOVIE；2,448 中文 / 1,196 源语单位 | 全范围源语对照 | 只有时间重叠候选；中文无源语重叠候选 275 条 | 按日文正文/BDSUP OCR 为主、英文为辅完成双向事件闭合；确认的意义修改逐条登记 | `SH-TRANS-008`、`SH-TRANS-001`；OCR/英文仅作辅助，不以多数译本裁决 | P1/P2 | approved（用户已授权直接完成本轮） | verified | 2,448 个可见中文事件完成文本/结构核对；1,196 个源语单位均已归入对应中文或合法跨事件配对 | 最终 master 审计：2,676 Events、3 个 confirmed 均为有意标题动画；未宣称全片播放或全片听辨 |
| `SH0002-DUP-202-001` | MOVIE `01:03:52.12`；CN Event 1705 | 重复译文/源文不一致候选 | `梅里亚！`；前一条同译文但日文为 `うっ… メリア！`，本条为 `メリア！` | 当前事件保留 `梅里亚！`；差异落在前一事件的受伤/惊讶发声 | `SH-TRANS-001`、`SH-TRANS-009`；短语相同不代表语气信息相同 | P2 | approved（用户授权直接完成本轮） | verified | 当前事件无需改写，仍为 `梅里亚！` | 与 `メリア！` 逐事件对照；前一事件已单列修订 |
| `SH0002-DUP-202-001A` | MOVIE `01:03:43.71`；CN Event 1704 | 语气/重复译文修订 | `梅里亚！`；日文为 `うっ… メリア！` | 改为 `呃……梅里亚！`，保留受伤/惊讶反应后再呼喊姓名 | `SH-TRANS-001`、`SH-ZH-002`；源文明确有前置发声，中文现状漏译 | P1 | approved（用户授权直接完成本轮） | verified | 已改为 `呃……梅里亚！` | 与日文源文对照；未改时间轴和特殊布局 |
| `SH0002-MEDIA-202-001` | MOVIE `00:03:55.04–00:03:55.46`；Title Events 211–221 | 片头动画越界/隐藏布局 | 3 条结构确认、8 条启发式 off-screen 风险，均为标题动画事件 | 保留标题离屏动画，不按普通对白规则移动或删减 | `SH-QC-009`、`SH-QC-010`；特殊标题不按普通样式基线化 | P2/P3 | approved（用户授权直接完成本轮） | verified | SSH 单点 `00:03:55.04` 显示标题仍在画面内，后续事件为连续放大下移至画外的有意收尾 | 本地临时帧点检完成；仅确认该动画点，不作全片视觉播放声明 |
| `SH0002-LAYOUT-202-001` | MOVIE `00:55:51.16`；Book01 Event 1477 | 同层空间碰撞候选 | 1 条启发式空间碰撞风险，文字为 `海伦——` | 保留原有特殊定位；只有确认真实遮挡才改动，不因启发式候选移动字幕 | `SH-QC-009`；时间重叠不等于空间碰撞 | P2/P3，若遮挡正文则 P1 | approved（按限制完成本轮） | verified | 未确认发布阻断级真实遮挡；未移动或删减该特殊事件 | 静态布局审计通过；未宣称全范围视觉播放 |
| `SH0002-MEDIA-202-002` | MOVIE；97 条短时长候选（含中日配对） | 时长/语音边界媒体候选 | 自动候选，未证明为错误 | 不因数值候选批量改时；仅修已确认的 `梅里亚` 语气漏译 | `SH-TIME-002`、`SH-TIME-004`、`SH-QC-010`；短于 0.5 秒不自动等于 P1 | P1/P2/P3 依媒体结论 | approved（不批量处理未确认候选） | verified | 未发现结构性 P0 或已确认的 correction-floor P1；短时长候选保留为后续局部媒体复核项 | 母本时间码/读速检查通过；本轮不宣称全片听辨 |

## 需要用户确认

用户已授权完成本轮校对并直接生成 2.0.2；全范围源语对照、术语闭合、片头标题动画和保守的时长/布局处理均按该授权实施。电影路径已由用户确认并完成 `discover`/`probe`，不再等待媒体路径确认。

## 决策与实施

本轮已完成 schema 9 / review 3 契约升级、Noto SC/JP 字体机械迁移、全范围静态候选审计和批准的字幕修订：将 `うっ… メリア！` 修为 `呃……梅里亚！`，保留当前事件 `梅里亚！`，并确认片头标题为有意的连续缩放下移动画；已构建 2.0.2 candidate。

## 验证与剩余风险

当前为 `released`。2.0.2 candidate 已完成结构验证，随后按 release contract 轮换为 current，并保留 2.0.1 为 previous；未执行全片播放/听辨，局部媒体证据和未确认启发式候选不被扩写为全片视觉结论。

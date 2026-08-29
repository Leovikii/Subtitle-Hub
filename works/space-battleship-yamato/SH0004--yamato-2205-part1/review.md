---
schema_version: 3
work_id: "SH0004"
updated_at: "2026-08-29"
baseline_release: "1.0.1"
target_release: "1.0.2"
status: released
scope: "S03E01–S03E04 full current release; Skill 1.3.1 contract migration, source-credit repair, and no-video downgrade"

coverage:
  evidence_tier: C
  timing_authority: "approved 1.0.1 timing retained; no local video/audio available"
  master_sha256:
    S03E01: 3f9c51793bac54c86a6538f59ee7136b2de0b4b24405f064c1a389f92156f281
    S03E02: a0a9b99a964eb0351d0d4ed705b1639affce16dab12f9cc309e7e65f87219087
    S03E03: 64cbd2a632f5fa72278ea56592fb801cf4348c090b088c369fccdec4934242de
    S03E04: e575cd6068a39f54d190053ddb95db5d948ce1acff2d8f5dd4857f96919c82de
  chinese_in_scope: 2388
  chinese_reviewed: 2388
  chinese_excluded: 0
  source_in_scope: 0
  source_aligned: 0
  source_unresolved: 0
  static_layout_checked: 9847
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

按 Skill 1.3.1 升级项目契约，并修复 1.0.1 成品遗漏的原始署名元数据。完整范围为四集全部可见中文字幕的静态审计、master/candidate 一致性检查及 1.0.2 发布轮换；不改对白文字、对白时间轴、事件样式或特殊字幕。

## 检查覆盖

- 机器检查：四个 master 共 9,847 个 Event、2,388 个可见中文字幕 Event，`audit_subtitle.py` 已完成全量静态检查。
- 人工/用户依据：1.0.1 已通过的字幕内容、已批准时间轴和辅助译本角色继续有效；当前无本地视频或音频，不宣称本轮新增听辨或视觉复核。
- 署名依据：逐集从保留的 1.0.0 canonical `Subtitle-Hub-Source-Credit` 恢复，不恢复署名 Events。
- 审计结论：无结构性非法时间；特效绘制事件的隐藏缩放属于保留特效风险，短时长/碰撞/越界等媒体相关候选未在失效视频路径下擅自改写。
- 覆盖限制：英文辅助译本或 OCR 不能替代源语证据；用户已完成发行终审并接受无视频与 C-tier 证据限制，Agent 不将辅助译本或 OCR 宣称为源语证明。

## 校对方案

| item_id | episode/time or bounded scope | category | before | proposed result | evidence/rationale | severity/risk | decision | status | actual result | verification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `SH0004-CONTRACT-131-001` | 项目控制面：`project.yaml` 与 `review.md` | Skill 契约迁移 | schema 7 / review 1 / Skill 1.1.0 | schema 9 / review 3 / Skill 1.3.1；删除项目内重复的固定 release/package 配置 | `SH-INIT-010`、`SH-CTRL-003`；保留身份、素材映射、来源角色和已确认限制 | P1 workflow gate；不改变字幕内容 | approved（用户要求按新 Skill 更新） | verified | 已完成迁移 | `--ready-for-proofreading` 已通过 |
| `SH0004-FONT-131-001` | S03E03 `0:13:01.95` 注释/对白；S03E04 `0:02:31.57`、`0:05:13.14` | 全局字体机械规范 | 日文片段或日文中点在混合中文事件中缺少明确 SC/JP 边界 | 仅补充 `Noto Sans CJK JP` 与 `Noto Sans CJK SC` 内联边界；不改变可见文字、时间、样式或特效 | `SH-LAYOUT-004`；新版 candidate builder 的 Noto-normalization gate | P2 rendering consistency | approved（按当前 Skill 必需的机械修复） | verified | 已修复 S03E03 的日文姓名/注释片段及 S03E04 的两个日文中点边界 | 两次 candidate 构建均报告 0 style/inline font changes；master/candidate rendered Events invariant 通过 |
| `SH0004-CREDIT-131-001` | S03E01–E04；四个 master/current ASS | 发布元数据修复 | 1.0.1 成品缺少已确认的原始 `Subtitle-Hub-Source-Credit` | 从 1.0.0 canonical 头字段逐集恢复到 master，candidate 再生成 1.0.2；不恢复署名/免责声明 Events | `SH-REL-003`；原始字段已在 `subtitles/previous/` 保留，逐集精确复核 | P1；署名不可静默丢失 | approved（用户明确要求升级） | verified | 已恢复四个 master 的署名元数据并发布到 current | 1.0.2 candidate/current 四个 ASS 均保留且各自仅有一个 canonical 署名字段 |
| `SH0004-MEDIA-131-001` | 项目媒体契约与 S03E01–E04 映射 | 可用性降级 | 项目仍声明 `user-provided-local-video`，并保留已失效文件指纹/音轨 | 改为 `not-provided`；保留原视频 basename 和已批准时间轴，清除指纹、选定音轨及本地路径依赖 | 用户最新确认视频路径已失效；符合无视频项目契约 | P1 workflow truthfulness | approved（用户明确要求降级） | verified | 已降级为无视频；英文辅助字幕文件仍保留 | `validate_project.py --ready-for-proofreading` 通过；无 `project/local.paths.yaml` |
| `SH0004-AUDIT-131-001` | S03E01–E04 全部可见中文字幕 Events | 全量静态质量审计 | 旧轮次仅记录部分样式/宽度检查 | 新版审计逐事件记录中文覆盖、结构、时间码、字体、样式引用、布局风险；不凭抽查宣称全量 | `SH-QC-009`、`SH-TRANS-008`；文本优先，媒体仅处理明确疑点 | P1/P2 按发现分级 | approved（用户明确要求升级） | verified-with-risks | 已完成 2,388 个中文字幕 Event 的全量静态检查；媒体候选保留 | 9,847 个 Event 已检查；未修改特效和未确认的媒体候选 |

## 需要用户确认

用户已于 2026-08-29 明确要求按 Skill 1.3.1 将 2205 更新到 1.0.2；本轮目标为契约迁移、全量静态审计和已确认署名元数据修复。

## 决策与实施

已完成 schema 9/review 3 契约迁移、全量静态审计、原始署名恢复、S03E03/S03E04 字体边界修复和无视频降级；1.0.2 candidate 已通过检查并已事务性轮换为 current，1.0.1 保留为 previous。压缩包由 GitHub Actions 负责，本地不生成或检查 ZIP。

## 验证与剩余风险

1.0.2 已完成新版全量静态审计、候选结构验证、署名检查、无视频契约验证和用户发行终审；current/previous 轮换完成。C-tier 源语忠实度仍不由英文辅助译本或 OCR 证明，发布记录保留该证据限制。视觉证据仅保留本地候选点，不在对话中批量附图。

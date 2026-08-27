# Subtitle Hub Agent Instructions

本仓库所有建项、素材清点、字幕校对、构建、验证和发布工作必须使用仓库级 `$subtitle-hub` Skill：`.agents/skills/subtitle-hub/SKILL.md`。Skill 是仓库级规范唯一事实源；不得另建并行规范，也不得从历史台账引用还原旧标准。

按 Skill 路由读取当前任务所需 reference，再读取系列 `series-guide.md`（若存在）、作品 `project.yaml`、`docs/project-guide.md`、`docs/review.md` 和 `docs/ledger.tsv`。

规则优先级为：用户当次明确要求、项目确认覆盖项、系列确认术语、Skill、外部参考。只有 `docs/project-guide.md` 可以补充或覆盖 Skill/系列规则；偏离系列译名必须记录用户确认。项目当前状态和本轮报告只以 `docs/review.md` 为准，逐项候选、决定、修改和验证只以 `docs/ledger.tsv` 为准。

## 不可违反的工作边界

- `project/sources/` 是只读来源，不得原地修改。
- 不得直接编辑 `subtitles/current/`；修订、构建和发布轮换必须按 Skill 在 `project/workspace/` 中完成。
- 自动检测结果只是候选问题，未经证据确认不得批量改写；不得虚构人工复核或全片观看覆盖。
- 实质字幕修改必须先写入 `docs/ledger.tsv` 并在 `docs/review.md` 提交用户审批；只实施明确批准的条目或批次。工作结束前更新同一条 ledger 记录和 `review.md`，不得另建问题、修改或轮次报告。
- 视觉核对必须在本地按候选时间点完成，不得在聊天或对话中批量附加视频截图、连续帧、联系表或其他大量图像证据，以免触发 Cloudflare CDN `413 Payload Too Large`。默认只在报告中记录时间点、文字结论和本地证据路径；只有用户明确要求查看单点证据时，才可在单条消息中附加不超过 2 张经过压缩的必要截图。

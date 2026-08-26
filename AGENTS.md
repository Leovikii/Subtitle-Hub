# Subtitle Hub Agent Instructions

本仓库的字幕工程由 AI agent 与人工审阅者共同维护。开始任何字幕校对、构建或发布工作前，必须按顺序阅读：

1. `docs/README.md`；
2. `docs/workflow.md`；
3. 当前作品的 `project.yaml`；
4. 当前作品的 `docs/README.md` 和 `docs/project-guide.md`；
5. 当前作品的 `docs/progress.yaml`、`docs/issues.tsv` 和 `docs/change-log.tsv`；
6. 若本轮正在等待人工反馈，只读取 `project/workspace/temp/review/` 中与当前 `active_round` 对应的审核报告。

规则优先级从高到低为：用户当次明确要求、项目补充规范、仓库全局规范、外部行业参考。低优先级规则不得覆盖高优先级规则；发生冲突时必须记录依据和处理结果。

项目内只有 `docs/project-guide.md` 可以补充或覆盖全局规则。`progress.yaml` 和台账记录控制面事实；开发者审核报告只是临时反馈文件，不构成规范。当前状态只以 `docs/progress.yaml` 为准，确认后的人工反馈必须回写控制面。

## 不可违反的工作边界

- `project/sources/` 是只读来源，不得原地修改。
- 已发布的 `subtitles/v*/` 不得覆盖；修订必须在 `project/workspace/` 完成并发布为新版本。
- 仓库不假定存在跨作品通用的字幕处理 pipeline。项目专用、一次性或低复用价值的脚本只能放在 `project/workspace/temp/tools/`，不得散落到项目根目录、`docs/` 或 `sources/`。
- 未审中间字幕、映射表、调试输出和运行日志必须放在 `project/workspace/temp/` 对应子目录；通过项目检查的待发布构建才可进入 `project/workspace/build/`。
- `project/workspace/temp/` 可以按轮次整体清理，但清理前必须把需要长期保留的结论迁入项目 `docs/`，并确认没有把主稿、未登记修改或唯一证据留在临时区。
- `project/archive/` 只保存经清单和校验值冻结的历史工程档案。除非为追溯而明确解包，否则不得把归档脚本当作当前工具运行。
- 不得仅凭文件名、标题或另一版本字幕断定时间轴兼容。
- 不得以“时间轴来自目标视频内嵌字幕”为由保留非法、非预期重叠、明显不同步或明显不可读的事件；触发全局时间轴纠错底线时必须回到实际音画局部修正并复核。
- 不得把现有中文范本当作原文证据；有原语音轨或原语字幕时必须回到原语核对。
- 自动检测结果只是候选问题，未经证据确认不得批量改写。
- 每项实质修改必须写入项目 `docs/change-log.tsv`；未解决问题写入 `docs/issues.tsv`；工作结束前更新 `docs/progress.yaml`。
- 不得声称“人工复核通过”或“全片观看通过”，除非确实完成相应检查并留下记录。

## 双语字幕的统一设计

仓库只维护一套以简体中文为主的视觉设计规范。中文是主字幕，英语或日语是副字幕并位于中文下方。副语可参考本语种的语言规则，但不得建立独立视觉体系，也不得牺牲中文的语义完整性、可读性和排版稳定性。

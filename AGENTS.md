# Subtitle Hub Agent Instructions

本仓库的字幕工程由 AI agent 与人工审阅者共同维护。开始任何字幕校对、构建或发布工作前，必须按顺序阅读：

1. `docs/README.md`；
2. `docs/workflow.md`；
3. 当前系列目录的 `series-guide.md`（若存在）；
4. 当前作品的 `project.yaml`；
5. 当前作品的 `docs/README.md` 和 `docs/project-guide.md`；
6. 当前作品的 `docs/progress.yaml`、`docs/issues.tsv` 和 `docs/change-log.tsv`；
7. 若本轮正在等待人工反馈，只读取 `project/workspace/temp/review/` 中与当前 `active_round` 对应的审核报告。

规则优先级从高到低为：用户当次明确要求、项目明确覆盖项、系列用语规范、仓库全局规范、外部行业参考。低优先级规则不得覆盖高优先级规则；发生冲突时必须记录依据和处理结果。

项目内只有 `docs/project-guide.md` 可以补充或覆盖系列或全局规则，并且偏离系列译名时必须记录用户确认。`progress.yaml` 和台账记录控制面事实；开发者审核报告只是临时反馈文件，不构成规范。当前状态只以 `docs/progress.yaml` 为准，确认后的人工反馈必须回写控制面。

建立新作品前必须按 `docs/project-identity.md` 通过 Bangumi API 检索并核对动画条目。`project.yaml` 的日文标题和简体中文标题必须来自对应条目的 `name` 与 `name_cn`，不得从文件名、搜索摘要或其他语言标题推定。Bangumi ID 与 `name_cn` 共同决定成品包名。若 `name_cn` 为空，或候选可能指向不同季度、电影版、总集篇或同名作品，必须暂停建项，请用户确认 Bangumi ID、中文标题和作品范围后才能继续。

## 不可违反的工作边界

- `project/sources/` 是只读来源，不得原地修改。
- 不得直接编辑 `subtitles/current/`。修订必须在 `project/workspace/` 完成；从第二个正式版本起，发布事务必须先删除更旧的 `subtitles/previous/`，再把完整的 `current/` 直接重命名为 `previous/`，最后把候选目录重命名为新的 `current/`。
- 发布版本的唯一事实源是 `subtitles/current/VERSION`；该文件必须与成品 ASS 同目录并随目录轮换。项目目录和成品目录不得包含版本号；自动生成的分发 ZIP 必须在文件名末尾包含同一版本号。每个正式 ASS 必须含与 `VERSION` 一致的 `Subtitle-Hub-Version` 标记。
- 成品外挂字幕文件名只声明主字幕语言，固定使用 `<video-stem>.<primary-language>.ass`。语言标签统一采用 BCP 47；简体中文主字幕必须使用 `.zh-Hans.ass`，不得把副语追加为第二语言后缀，也不得并行维护 `chi`、`zho`、`zh-CN` 或 `chs` 等文件名代码。
- 正式字幕字体遵循 `docs/timing-and-layout.md#9-字体与字形`：简体中文及英文使用 `Noto Sans CJK SC`，日文使用 `Noto Sans CJK JP`。不得保留未登记的小众字体或使用 ASS `[Fonts]` 区段；字体替换后必须复核字宽、换行和定位特效风险，不能把“特效标签仍存在”等同于视觉无变化。
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
- 视觉核对必须在本地按候选时间点完成，不得在聊天或对话中批量附加视频截图、连续帧、联系表或其他大量图像证据，以免触发 Cloudflare CDN `413 Payload Too Large`。默认只在报告中记录时间点、文字结论和本地证据路径；只有用户明确要求查看单点证据时，才可在单条消息中附加不超过 2 张经过压缩的必要截图。

## 双语字幕的统一设计

仓库只维护一套以简体中文为主的视觉设计规范。中文是主字幕，英语或日语是副字幕并位于中文下方。副语可参考本语种的语言规则，但不得建立独立视觉体系，也不得牺牲中文的语义完整性、可读性和排版稳定性。

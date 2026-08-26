# SH0001《宇宙战舰大和号2199》TV

本项目收录 TV 正篇 26 集的简体中文主字幕、日语副字幕工程和最终 ASS 字幕，不包含 OVA 或剧场版。

## 项目标识

- 内部 ID：`SH0001`
- 豆瓣 ID：`10549231`
- IMDb ID：待补充
- Bangumi ID：待补充

外部 ID 的权威记录位于 [project.yaml](project.yaml)。开始校对前必须先阅读仓库 [全局规范](../../../docs/README.md) 和本项目 [AI agent 控制面](docs/README.md)。

## 目录

- `docs`：AI agent 长期基准，包括项目补充规范、统一进度、修改台账和问题台账；
- `project/sources`：保持原貌的日语、英语和旧简日双语参考字幕，以及片源文件名清单；
- `project/workspace/episodes`：从迁入成品建立的下一轮人工校订主稿；
- `project/workspace/temp`：本项目的一次性工具、中间文件、未审候选和日志，可按轮次清理；
- `project/workspace/build`：通过本轮检查的待发布构建，可重新生成且不纳入 Git；
- `project/archive`：带清单和校验值的冻结历史工程压缩档案；
- `subtitles`：正式发布且不可覆盖的最终字幕版本。

当前推荐版本为 `subtitles/v1.0.0/`，发布范围、机器检查和人工检查覆盖记录见 [release.yaml](subtitles/v1.0.0/release.yaml)。旧质量报告已经压缩到项目历史文档档案，不属于当前 AI agent 控制面。

## 片源说明

正式字幕文件名与对应的 `[Sav1our]` MKV 主文件名一致，仅扩展名由 `.mkv` 改为 `.ass`。仓库仅记录对应文件名，不提供视频文件、种子、磁力链接或下载地址。

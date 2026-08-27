# SH0003《宇宙战舰大和号2202 爱的战士们》TV

本项目收录《宇宙战舰大和号2202 爱的战士们》TV 版 26 集的简体中文主字幕、日语副字幕工程和最终 ASS 字幕，不包含七章剧场上映版或后续总集篇。

## 项目标识

- 内部 ID：`SH0003`
- Bangumi：[`246898`](https://bgm.tv/subject/246898)
- 日文标题：`宇宙戦艦ヤマト2202 愛の戦士たち`
- 简中标题：`宇宙战舰大和号2202 爱的战士们`

外部 ID 的权威记录位于 [project.yaml](project.yaml)。开始校对前必须使用仓库 [`$subtitle-hub` Skill](../../../.agents/skills/subtitle-hub/SKILL.md)，再读取上级 [系列用语规范](../series-guide.md) 以及本项目的 [补充规范](docs/project-guide.md)、[进度](docs/progress.yaml)、[问题台账](docs/issues.tsv) 和 [修改台账](docs/change-log.tsv)。

## 目录

- `docs`：AI agent 五文件控制面；
- `project/sources`：保持原貌的日语、英语和中文范本；
- `project/workspace/episodes`：26 集下一轮校订主稿；
- `project/workspace/temp`：一次性工具、中间文件、审核候选和日志；
- `project/workspace/build`：可重新生成的待发布构建；
- `project/archive`：唯一冻结历史工程 ZIP，内含逐文件清单；
- `subtitles/current`：当前最终字幕及唯一版本文件；首次升级后必须保留 `subtitles/previous`；
- 仓库根目录 `packages`：自动生成的当前字幕 ZIP。

当前下载包位于 [packages](../../../packages)，命名模式见 `project.yaml`；文件名末尾版本由 Actions 从 `subtitles/current/VERSION` 自动生成。

## 片源说明

正式字幕文件名保留对应 `[Sav1or]` MKV 的完整 stem，再追加主字幕语言后缀 `.zh-Hans.ass`。日语副字幕记录在项目元数据和 ASS 内，不追加到外挂字幕文件名。仓库只在 `project.yaml` 记录片源文件名，不保存视频、种子、磁力链接或下载地址。

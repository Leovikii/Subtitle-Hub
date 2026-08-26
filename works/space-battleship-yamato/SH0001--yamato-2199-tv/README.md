# SH0001《宇宙战舰大和号2199》TV

本项目收录 TV 正篇 26 集的简体中文主字幕、日语副字幕工程和最终 ASS 字幕，不包含 OVA 或剧场版。

## 项目标识

- 内部 ID：`SH0001`
- IMDb：`tt2496120`，`Space Battleship Yamato 2199`
- Bangumi：`54552`
- 豆瓣：`10549231`（用户提供的可选映射，不作为主动检索门禁）

外部 ID 的权威记录位于 [project.yaml](project.yaml)。开始校对前必须先阅读仓库 [全局规范](../../../docs/README.md)、上级 [系列用语规范](../series-guide.md) 和本项目 [AI agent 控制面](docs/README.md)。

## 目录

- `docs`：AI agent 长期基准，包括项目补充规范、统一进度、修改台账和问题台账；
- `project/sources`：保持原貌的日语、英语和旧简日双语参考字幕；来源说明与片源文件名统一记录在 `project.yaml`；
- `project/workspace/episodes`：从迁入成品建立的下一轮人工校订主稿；
- `project/workspace/temp`：本项目的一次性工具、中间文件、未审候选和日志，可按轮次清理；
- `project/workspace/build`：通过本轮检查的待发布构建，可重新生成且不纳入 Git；
- `project/archive`：带清单和校验值的冻结历史工程压缩档案；
- `subtitles/current`：稳定路径下的当前最终字幕，目录内 `VERSION` 是唯一版本源；首次升级后，`subtitles/previous` 必须保留被替换的完整上一版；
- 仓库根目录 `packages`：GitHub Actions 自动生成的当前字幕 ZIP。

当前推荐成品固定在 [subtitles/current](subtitles/current)，版本读取 [subtitles/current/VERSION](subtitles/current/VERSION)。发布范围、来源、机器检查与人工检查覆盖均集中在 [project.yaml](project.yaml)；旧质量报告和被合并的旧发布元数据已经压缩到项目历史文档档案，不属于当前 AI agent 控制面。

当前下载包：[tt2496120--Space Battleship Yamato 2199.zip](<../../../packages/tt2496120--Space Battleship Yamato 2199.zip>)。

## 片源说明

正式字幕文件名保留对应 `[Sav1our]` MKV 主文件名的 stem，再追加 `.zh-Hans.ja.ass`，表示简体中文主字幕与日语副字幕。仓库仅在 `project.yaml` 记录对应文件名，不提供视频文件、种子、磁力链接或下载地址。

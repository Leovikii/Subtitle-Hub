# 旧工程迁移记录

迁入来源：`C:\Users\Vki\Documents\Codex\2026-08-24\2199-cloudflare313`

迁移日期：2026-08-26

## 已迁入

- 日语官方 WEBrip CC：26 个 SRT；
- 内嵌英文参考字幕：26 个 dialogue ASS 和 26 个 signs ASS；
- 诸神旧字幕：26 个日文 ASS 和 26 个简日双语 ASS；
- TV 审查表：19 份，已排除第一字段为《星巡的方舟》的记录；
- 历史处理与审查脚本：17 个，原样保存；
- 正式 TV 字幕：26 个 ASS 及质量说明；
- 下一轮工作主稿：由 26 个正式字幕复制建立。

## 后续工程区收束

2026-08-26 按仓库工程区规范进一步整理：

- 长期主稿保留在 `project/workspace/episodes/`；
- 建立 `project/workspace/temp/`，分别收纳项目专用工具、中间文件、未审候选和日志；
- 待发布构建从旧 `project/build/` 调整到 `project/workspace/build/`；
- 17 个历史脚本、19 份历史审查表和 3 份旧说明文件压缩到 `project/archive/SH0001-legacy-engineering-20260826.zip`；
- 压缩包经解包和逐文件 SHA-256 验证后，移除原来散落的 legacy 副本及空 `project/pipeline/`。

归档清单、校验值、限制和恢复方式见 [engineering-archive.md](engineering-archive.md)。

## 未重复迁入

- `review_work/english_tv` 与 `sources/tv_english_embedded` 内容重复；
- `review_work/backups` 属于阶段性备份，后续由 Git 历史承担版本追踪；
- `sources/movie`、`review_work/english_movie` 和剧场版成品不属于 SH0001；
- 视频、种子、磁力链接和下载地址不进入仓库。

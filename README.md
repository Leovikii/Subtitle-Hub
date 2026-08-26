# Subtitle Hub

Subtitle Hub 同时承担两项职责：

1. 保存可追溯、可继续校订的字幕工程；
2. 长期存档经过审核的最终字幕产物。

工程按作品归档。每个作品使用仓库内部 ID 作为唯一标识，IMDb 和 Bangumi 用于主动身份核验；豆瓣只在用户提供时作为可选外部映射。仓库不保存视频、种子、磁力链接或下载地址；片源清单中的原始文件名仅用于说明字幕兼容性。

同一系列目录使用唯一的 `series-guide.md` 统一人名、地名、组织、舰船和技术术语。面向用户的成品包名直接采用“IMDb ID 在前、IMDb 条目名称在后”，例如 `tt2496120--Space Battleship Yamato 2199.zip`。

AI agent 和校对者开始工作前必须阅读 [全局字幕规范](docs/README.md)。

最终字幕固定保存在各项目的 `subtitles/current/`，版本号由目录内 `VERSION` 和 ASS 内标记共同声明；从第二个正式版本起，`subtitles/previous/` 强制保留被替换的完整上一版。仓库级 `packages/` 保存由 GitHub Actions 从当前成品自动生成的稳定命名 ZIP，供检索和下载；ZIP 不是另一套发布事实源。

当前已收录作品见 [CATALOG.md](CATALOG.md)。

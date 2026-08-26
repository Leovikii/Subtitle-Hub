# Subtitle Hub

Subtitle Hub 同时承担两项职责：

1. 保存可追溯、可继续校订的字幕工程；
2. 长期存档经过审核的最终字幕产物。

工程按作品归档。每个作品使用仓库内部 ID 作为仓库标识，使用 Bangumi 动画条目作为唯一外部身份与中日标题来源。仓库不保存视频、种子、磁力链接或下载地址；片源清单中的原始文件名仅用于说明字幕兼容性。

同一系列目录使用唯一的 `series-guide.md` 统一人名、地名、组织、舰船和技术术语。面向用户的成品包名采用 Bangumi ID、简体中文标题和当前版本，例如 `bgm54552 - 宇宙战舰大和号2199 [v1.0.1].zip`。

AI agent 和校对者开始工作前必须阅读 [全局字幕规范](docs/README.md)。

最终字幕固定保存在各项目的 `subtitles/current/`，版本号由目录内 `VERSION` 和 ASS 内标记共同声明；从第二个正式版本起，`subtitles/previous/` 强制保留被替换的完整上一版。仓库级 `packages/` 保存由 GitHub Actions 从当前成品自动生成的规范命名 ZIP，供检索和下载；ZIP 不是另一套发布事实源。

正式 ASS 统一使用 `Noto Sans CJK SC`（简体中文及英文）与 `Noto Sans CJK JP`（日文）静态字体。字体不嵌入字幕 ZIP，使用前应在系统或播放器字体目录中一次安装这两套字体；具体规则与兼容性见 [字体与字形规范](docs/timing-and-layout.md#9-字体与字形)。

当前已收录作品见 [CATALOG.md](CATALOG.md)。

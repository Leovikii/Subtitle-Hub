# 成品版本、命名与存档规范

## 1. 单一当前版本

每个作品只维护一套当前推荐成品，使用不含版本号的稳定路径：

```text
subtitles/
├─ current/      # 当前完整成品集
│  ├─ VERSION    # 当前唯一版本号，SemVer，不加 v 前缀
│  └─ *.ass
└─ previous/     # 上一完整版本；首次基线后尚不存在，首次升级起必须存在
   ├─ VERSION
   └─ *.ass
```

不得建立 `v1.2.3/` 一类版本目录，也不得在项目 README、仓库目录或多个 YAML 中复制当前版本号。`subtitles/current/VERSION` 是当前版本唯一事实源；进度文件中的基线版本只用于说明当前工作轮次，不构成发布声明。

仓库不逐版存档字幕，但必须保证至少一个真实旧版可追溯回滚。从第二个正式版本开始，`previous/` 是强制目录：每次发布先删除更旧的 `previous/`，再把包含 `VERSION` 和全部 ASS 的旧 `current/` 直接重命名为 `previous/`。不得为轮换重新压缩、重新打包或逐文件复制。首次建立 1.0.0 等基线时没有真实旧版，因此暂时不存在 `previous/`；第一次发布内容不同的新版本后，此豁免永久结束。

## 2. 版本递增

使用 SemVer `MAJOR.MINOR.PATCH`，不写前导 `v`：

- `PATCH`：纠错、润色、时间轴或样式修复，不改变作品范围和成品契约；
- `MINOR`：增加集数、语言组合或兼容片源等向后兼容扩展；
- `MAJOR`：语言布局、命名契约、作品范围或格式发生不兼容变化。

新项目或迁入项目的首次正式基线统一为 `1.0.0`。纯目录迁移、文档整理或自动化调整不改变字幕内容版本。版本只在一组经过发布门禁的字幕内容真正成为新 `current/` 时递增；因此自动门禁可以明确区分“尚无真实旧版的首次基线”和“必须存在 previous 的后续版本”。

## 3. ASS 内版本标记

每个正式 ASS 的 `[Script Info]` 段必须包含：

```ass
; Subtitle-Hub-Version: 1.2.3
```

当前成品的标记值必须与同目录 `VERSION` 完全一致；旧版标记同样必须与 `previous/VERSION` 一致。不得把版本号写入 `Title`、样式名、事件文本或文件名。发布打包脚本会拒绝当前成品缺失、重复或不一致的版本标记。

## 4. 成品文件名

文件名必须由“目标视频文件名去掉视频扩展名”加“语言组合后缀”和字幕扩展名组成：

```text
<video-stem>.<primary-language>.<secondary-language>.ass
```

语言标签采用 ASCII 的 BCP 47 标签并保持顺序：主字幕在前、副字幕在后。本仓库常用：

- 简体中文主字幕 + 日语副字幕：`.zh-Hans.ja.ass`；
- 简体中文主字幕 + 英语副字幕：`.zh-Hans.en.ass`。

不得使用“简日双语”等本地化文字后缀，也不得使用含义不明确的 `chs`、`jp`、`bilingual`。ASCII 后缀可降低跨平台、压缩工具和媒体库扫描器的兼容风险；视频 stem 仍原样保留，以便精确识别适配片源。

## 5. 项目元数据

作品根目录 `project.yaml` 是唯一项目描述文件，集中记录作品身份、外部 ID、语言、字幕来源、片源文件名、工作区、发布路径、审核覆盖、自动包和历史工程档案。不得另建 `source-catalog.yaml`、片源 `manifest.yaml`、`latest.yaml`、逐版本 `release.yaml` 或仓库内 `checksums.sha256`。

逐文件校验值属于可重复生成的分发包内容，由打包脚本写入 ZIP 内的 `CHECKSUMS.sha256`。项目的 AI agent 规范、进度和台账继续保留在固定的五文件 `docs/` 控制面，不并入元数据。

## 6. 发布事务与回滚

发布必须作为一个完整事务执行：

1. 冻结并验证 `workspace/build/` 的完整目标成品集；
2. 确定新 SemVer，在所有候选 ASS 写入相同版本标记；
3. 验证文件名、集数、语言组合、结构、音画抽查和台账；
4. 删除更旧的 `previous/`，再将完整旧 `current/` 直接重命名为 `previous/`；
5. 把新成品和新 `VERSION` 写入同盘候选目录，验证通过后把该目录直接重命名为 `current/`；
6. 运行仓库打包脚本；
7. 核对 ZIP 内 `VERSION`、字幕数量、版本标记和 `CHECKSUMS.sha256`，提交成品、版本文件、元数据/台账必要更新及生成包。

任何一步失败都不得留下新旧字幕混合的 `current/`。候选目录未能成为 `current/` 时，必须把刚轮换的 `previous/` 直接重命名回 `current/`。主动回滚时交换 `current/` 与 `previous/` 的角色，确保被撤下版本仍可追溯，再重新生成仓库分发包；回滚本身必须登记台账。

## 7. 仓库分发包

仓库根目录 `packages/` 只保存自动生成的当前分发包：

```text
packages/<imdb-id>--<IMDb-title>.zip
```

包名直接取自 `project.yaml` 中已经核验的 IMDb ID 和 IMDb 条目名称，具体消歧与最小文件系统字符处理见 [作品身份规范](project-identity.md)。包名不含内部 ID 或版本号；版本从包内 `VERSION` 读取。ZIP 只包含当前 ASS、`VERSION` 和自动生成的 `CHECKSUMS.sha256`，不包含来源字幕、视频文件名清单、工程主稿、临时报告或历史档案。

`.github/scripts/build_subtitle_packages.py` 必须使用确定性排序、固定时间戳和稳定压缩参数，使相同输入产生相同 ZIP。GitHub Actions 在 `main` 的 `current/` 或 `previous/` 变化后运行门禁，并只在当前分发包确有变化时提交 `packages/`；包目录本身不触发工作流，避免提交循环。

打包前必须同时检查回滚链：当前版本不是首次 `1.0.0` 时，`previous/` 必须存在；`previous/VERSION` 必须与其中全部 ASS 标记一致，并且不得等于当前版本。此检查失败时不得生成或更新下载包。

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

当前成品的标记值必须与同目录 `VERSION` 完全一致；旧版标记同样必须与 `previous/VERSION` 一致。不得把版本号写入 `Title`、样式名、事件文本或字幕文件名。发布打包脚本会拒绝当前成品缺失、重复或不一致的版本标记。

## 4. 成品文件名

文件名必须由“目标视频文件名去掉视频扩展名”加“主字幕语言后缀”和字幕扩展名组成：

```text
<video-stem>.<primary-language>.ass
```

语言标签统一采用 BCP 47，并且只声明播放器应识别的主字幕语言。本仓库简体中文主字幕统一使用：

- 简体中文主字幕：`.zh-Hans.ass`。

副语种不得进入文件名：简日和简英双语都使用 `.zh-Hans.ass`。完整语言组合必须记录在 `project.yaml`，并在 ASS 的 `[Script Info]` 中使用不可渲染注释 `Subtitle-Hub-Languages`、`Subtitle-Hub-Primary-Language` 和 `Subtitle-Hub-Secondary-Language`。不得并行维护 `chi`、`zho`、`zh-CN`、`chs`、“简日双语”或 `bilingual` 等另一套代码。视频 stem 仍原样保留，以便精确识别适配片源。

正式简日双语 ASS 必须包含：

```ass
; Subtitle-Hub-Languages: zh-Hans, ja
; Subtitle-Hub-Primary-Language: zh-Hans
; Subtitle-Hub-Secondary-Language: ja
```

简英双语只把副语值改为 `en`。语言标记必须与 `project.yaml` 一致，并且每项恰好出现一次。

### 4.1 ASS 头部规范

正式 ASS 的 `[Script Info]` 使用固定结构顺序：

```ass
[Script Info]
; Subtitle-Hub-Version: <version>
; Subtitle-Hub-Languages: <primary>, <secondary>
; Subtitle-Hub-Primary-Language: <primary>
; Subtitle-Hub-Secondary-Language: <secondary>
; Subtitle-Hub-Timing-Note: <optional project-specific provenance>
; Subtitle-Hub-Source-Credit: <complete original production credits; omit only when absent>
Title: bgm<subject-id> - <name_cn> - <episode-id>
ScriptType: v4.00+
WrapStyle: <preserved value>
ScaledBorderAndShadow: <preserved value>
PlayResX: <preserved value>
PlayResY: <preserved value>
YCbCr Matrix: <preserved value>
```

`Subtitle-Hub-Timing-Note` 只在确有需要长期保留的定时依据时出现。原稿存在可明确识别的制作署名时，`Subtitle-Hub-Source-Credit` 必须出现；原稿确无署名时才省略。两者均不得写入本地绝对路径、下载位置或可清理临时报告。单部电影的 `episode-id` 使用 `MOVIE`。

正式 ASS 必须完整保留原稿中可明确识别的字幕制作署名：不仅包括字幕组名称，也包括翻译、听译、校对、时间轴、特效、压制、片源等人员与分工；不得擅自缩减、概括或只留下组名。全部署名只能合并写入 `[Script Info]` 中唯一一条 `Subtitle-Hub-Source-Credit`，不得再以 `Comment:`、`Source-Metadata`、零时长事件或其他形式写入 `[Events]`。无法从原稿明确识别署名时省略该字段，不得从文件名或来源目录推定。字幕组网站、交流学习/非商业免责声明、免责文字，以及中文底稿、原语文件和时间轴参考等工程溯源说明不属于成品署名：前者删除，后者由 `project.yaml` 与项目文档记录，不进入正式 ASS。`[Events]` 中的 `Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text` 是 ASS 必需结构，必须保留。

标准化时必须保留现有 `ScriptType`、`WrapStyle`、`ScaledBorderAndShadow`、`PlayResX`、`PlayResY` 和 `YCbCr Matrix` 的有效值，只调整字段顺序。默认值或空白工程字段 `Original Script`、`Original Translation`、`Original Timing`、`Original Editing`、`Script Updated By`、`Update Details`、`Timer: 100.0000` 和空 `Synch Point` 不进入正式成品；Aegisub 自动生成说明、网址及整个 `[Aegisub Project Garbage]` 区段必须删除，避免发布本地音视频路径和编辑器状态。

本规范不建立跨作品统一样式表，也不授权修改仍被引用的样式。正式发布候选可以删除经静态引用闭包证明完全未使用的 `Style:` 定义，以清除不会参与渲染的历史垃圾；除此之外，从 `[V4+ Styles]` 开始的内容和顺序必须保持不变，包括 `Format`、所有保留样式、注释事件、对白、特效和附件区段。

未使用样式的判定必须同时扫描：

- 全部 `Dialogue` 和 `Comment` 事件的 `Style` 字段；
- 全部事件文本中的 `\r<StyleName>` 样式重置；
- 空 Style 事件对 `Default` 样式的隐式依赖。

只有在上述引用集合中均未出现的样式才能删除。删除后必须重新验证每个事件和 `\r` 重置均能解析到保留样式。除批准的内联字体映射和已明确识别的 `Source-Metadata` 清理外，必须证明 `[Events]` 字节未改变；清理器不得凭文本内容删除普通注释事件。不得自动合并参数相同的样式，不得重命名样式，不得修改保留样式的字体、颜色、字号、边距、对齐、描边或阴影；这些操作属于独立视觉修改，必须另立审核轮次并完成渲染复核。

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
6. 提交并推送成品、版本文件和元数据/台账必要更新，由 GitHub Actions 运行仓库打包脚本；本机不得生成并提交 ZIP；
7. 核对 Actions 生成 ZIP 的文件名版本、包内 `VERSION`、字幕数量、版本标记和 `CHECKSUMS.sha256`。

任何一步失败都不得留下新旧字幕混合的 `current/`。候选目录未能成为 `current/` 时，必须把刚轮换的 `previous/` 直接重命名回 `current/`。主动回滚时交换 `current/` 与 `previous/` 的角色，确保被撤下版本仍可追溯，再重新生成仓库分发包；回滚本身必须登记台账。

## 7. 仓库分发包

仓库根目录 `packages/` 只保存自动生成的当前分发包：

```text
packages/bgm<subject-id> - <name_cn> [v<version>].zip
```

包名直接取自 `project.yaml` 中由 Bangumi API 核验的条目 ID 和 `name_cn`，采用 ` - ` 分隔身份与简中标题，并在末尾以 `[v<version>]` 标注版本；版本只能读取 `subtitles/current/VERSION`，不得在 README 或其他元数据中复制当前版本号。具体消歧、元数据同步和文件系统字符处理见 [作品身份规范](project-identity.md)。包名不含内部 ID 或日文标题；文件名版本便于用户直接识别，仍必须与包内 `VERSION` 一致。ZIP 只包含当前 ASS、`VERSION` 和自动生成的 `CHECKSUMS.sha256`，不包含来源字幕、视频文件名清单、工程主稿、临时报告、字体或历史档案。

正式 ASS 统一引用 [字体规范](timing-and-layout.md#9-字体与字形) 中的 Noto Sans CJK SC/JP 静态字体。字体不嵌入 ASS，也不重复放入每个字幕 ZIP；发布说明必须让用户能够识别这一外部字体依赖。任何项目字体例外必须先登记在项目 `docs/project-guide.md`，否则打包门禁应拒绝非标准字体。

`.github/scripts/build_subtitle_packages.py` 必须使用确定性排序、固定时间戳和稳定压缩参数，使相同输入产生相同 ZIP。GitHub Actions 只在 `main` 中 `subtitles/current/VERSION` 发生变动时自动运行；字幕、元数据、脚本或 workflow 本身的普通变动不得自动打包，发布者必须以版本号变动明确启动一次正式构建，也可以按需手动触发。工作流在构建前和推送前必须分别确认触发提交仍是远端 `main` 的最新提交；迟到、排队或已被后续提交取代的运行必须正常退出，不得回写旧版本产物。只有当前分发包确有变化时才提交 `packages/`，包目录本身不触发工作流，避免提交循环。

打包前必须同时检查回滚链：当前版本不是首次 `1.0.0` 时，`previous/` 必须存在；`previous/VERSION` 必须与其中全部 ASS 标记一致，并且不得等于当前版本。此检查失败时不得生成或更新下载包。

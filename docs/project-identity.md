# 作品身份、Bangumi 元数据与成品名称规范

## 1. 建项前置门禁

本仓库以日本动画字幕为主要范围，Bangumi 是作品身份和中日标题的唯一外部元数据源。创建作品目录前，AI agent 必须先发现候选 Bangumi ID，再通过公开 API `https://api.bgm.tv/v0/subjects/<id>` 读取完整条目并与实际作品范围逐项核对。不得从文件名、搜索摘要、IMDb、英文发行名或模型记忆推定正式标题。检索必须区分：

- TV 季度、OVA、电影、总集篇和剧场先行版；
- 原作、重制版、续作和同名作品；
- 首播年份、集数、媒介类型和原始标题；
- 系列名与本季度完整中文名。

搜索结果页只用于发现候选，正式值必须取自 API 返回的 `id`、`name` 和 `name_cn`；同时核对 `platform`、`date`、`eps` 或 `total_episodes`。API 当前不可访问时不得新建正式包，也不得用另一网站悄悄补值。可以保留待确认草稿，但必须标记 `access-blocked`。

## 2. 必须暂停的歧义

出现以下任一情况时，AI agent 必须暂停建项并向用户同时给出候选 ID、候选中文名和产生歧义的证据：

- 平台条目的年份、集数或媒介类型互相冲突；
- 中文名无法区分季度、电影版或总集篇；
- 候选不是完整作品条目，而是单集、特别篇或合集；
- 同一平台存在两个同样合理的候选；
- API 的 `name_cn` 为空、明显不完整，或需要在多个中文标题间作实质选择。

只有用户确认 Bangumi ID、中文标题和作品范围后才能继续创建项目、系列术语表或正式包。确认结果写入 `project.yaml`，不能只留在聊天或临时报告中。

## 3. project.yaml 身份快照

项目唯一元数据文件使用一个 `identity` 块集中记录：

- `provider: bangumi`；
- Bangumi 条目 ID、人工详情页 URL 和 API URL；
- API `name` 原样保存为 `titles.ja`；
- API `name_cn` 原样保存为 `titles.zh-Hans`；
- 核验状态和核验日期。

不得另设顶层 `titles`，也不得保留 IMDb、豆瓣或另一套标题字段。仓库内部 ID、作品类型和集数继续使用项目顶层字段；建项时必须与 API 的类型和集数交叉核对。在线元数据先通过仓库 CLI 同步为受版本控制的快照，再由打包脚本读取；打包不得每次联网，以保证相同提交产生相同产物。

核验状态只使用：

- `api-verified`：agent 已从对应 Bangumi API 条目读取并核对；
- `user-confirmed`：用户明确提供或确认，但 agent 无法独立访问详情页；
- `access-blocked`：已发现候选，但当前环境无法读取足够证据；
- `pending-user-confirmation`：存在歧义，必须停止建项。

`access-blocked` 不是猜测 ID 或标题的许可。后续发现 API 标题变化时更新同一个 `project.yaml`，不得另建身份说明文件；标题变化只有经核验提交后才影响分发包。

`user-confirmed` 只能用于保留待恢复核验的项目草稿；正式打包要求 `api-verified`，不得仅凭人工输入绕过 API 身份门禁。

标准同步命令为：

```text
python .github/scripts/sync_bangumi_metadata.py --check
python .github/scripts/sync_bangumi_metadata.py --write
```

`--check` 只比较仓库快照与 API；`--write` 更新中日标题和核验日期。脚本必须同时拒绝 ID、类型或集数不匹配的条目。

## 4. 面向用户的成品包名

ZIP 固定命名为：

```text
bgm<subject-id> - <name_cn> [v<version>].zip
```

例如：

```text
bgm54552 - 宇宙战舰大和号2199 [v1.0.1].zip
```

`bgm` 前缀和条目 ID 位于最前，以 ` - ` 连接 API 的 `name_cn`，并在末尾使用 `[v<version>]` 标注版本。包名不得加入仓库内部 ID、日文标题、语言说明或发布组名称。文件名版本用于快速识别，仍须与包内 `VERSION` 一致；语言信息从字幕文件名读取。

`name_cn` 先规范化为 Unicode NFC。若含 Windows 禁止字符 `<>:"/\\|?*`，打包脚本只把这些字符替换为带空格的 ASCII 连字符 ` - `，并合并连续空白、移除末尾空格和句点；除此之外不得改写、翻译或重排标题。完整 ZIP 文件名的 UTF-8 编码不得超过 240 字节。Bangumi ID、`name_cn` 或当前版本改变时，自动打包必须删除旧的生成包，只保留新名称。

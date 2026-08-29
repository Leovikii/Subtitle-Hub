# Subtitle Hub

Subtitle Hub 是一个面向中文字幕校对、维护与发布的开放仓库。它既保存可追溯、可继续修订的字幕工程，也归档已经发布的简体中文主字幕与分发包。

仓库按作品整理内容，并使用 Bangumi 条目统一作品身份与官方标题。这里不提供视频、种子、磁力链接或片源下载地址；仓库中出现的原始文件名只用于说明字幕与目标视频的匹配关系。

## 内容入口

[作品目录](CATALOG.md) 是当前项目、字幕版本、校对状态与发布包的统一入口。

## Subtitle Hub Skill

[`subtitle-hub` Skill 1.3.1](.agents/skills/subtitle-hub/SKILL.md) 集中了项目初始化、素材盘点、全文字幕校对、时间轴与排版检查、构建验证和发布流程。仓库规范只在该 Skill 中维护；本 README 只提供面向用户的简介、安装和使用入口。

### 在本仓库中使用

克隆仓库并在 Codex 中打开仓库根目录后，Codex 会自动发现位于 `.agents/skills/subtitle-hub/` 的仓库级 Skill，无需另行安装。可在提示词中显式调用：

```text
$subtitle-hub 初始化一个新的字幕项目，并引导我提供必要素材。
```

也可以直接说明具体任务，例如：

```text
$subtitle-hub 盘点这个项目的素材，并评估可用的校对能力层级。
$subtitle-hub 校对当前中文字幕，记录问题并生成可验证的候选版本。
```

开始新项目时，至少准备待校对的中文字幕，并说明逐集范围与时间轴依据；有目标视频时一并提供，Skill 才会主动探测音轨、字幕轨、语种和时长。原语字幕或台本可以在无视频时提供完整的原意对照能力，其他语种译本用于歧义交叉核对，内嵌字幕用于同源时间轴、版式或辅助译本参考。Skill 会按现有材料提出映射和能力等级，再一次确认关联作品、范围、发布语言和简短项目名。

### 单独安装 Skill

如果希望在其他仓库或本地任务中使用，可以通过 Codex 自带的 `$skill-installer` 从 [Subtitle Hub Skill 源目录](https://github.com/Leovikii/Subtitle-Hub/tree/main/.agents/skills/subtitle-hub) 安装：

```text
$skill-installer 请从 https://github.com/Leovikii/Subtitle-Hub/tree/main/.agents/skills/subtitle-hub 安装 Subtitle Hub Skill。
```

安装完成后，从下一轮对话开始使用 `$subtitle-hub` 调用。Skill 的设计与发现机制可参考 OpenAI 官方文档：[Build skills](https://learn.chatgpt.com/docs/build-skills)。

## 许可

本仓库采用 [GNU General Public License v3.0](LICENSE)。

# Subtitle Hub 全局字幕规范

本目录是所有字幕校对、优化、构建和发布工作的全局规范入口，主要面向 AI agent，同时供人工审阅者核查。

规范使用以下约束词：

- **必须（MUST）**：不满足就不能发布；
- **应当（SHOULD）**：默认遵守，偏离时必须在项目文档中说明；
- **可以（MAY）**：根据内容和项目需要选择。

## 必读顺序

1. [workflow.md](workflow.md)：标准工作流和发布门禁；
2. [workspace-and-artifacts.md](workspace-and-artifacts.md)：项目工程区、临时工具、中间产物和历史归档；
3. [source-and-translation.md](source-and-translation.md)：来源权重、原语核对和翻译纠错；
4. [timing-and-layout.md](timing-and-layout.md)：时间轴、断句和中主副辅双语布局；
5. [chinese-style.md](chinese-style.md)：简体中文文本与标点规范；
6. [quality-control.md](quality-control.md)：自动检查、人工检查和问题分级；
7. [project-documentation.md](project-documentation.md)：项目文档、进度和修改台账；
8. [references.md](references.md)：公开行业参考及本仓库取舍。

## 规则优先级

1. 用户当次明确要求；
2. 作品 `docs/project-guide.md` 中明确列出的项目覆盖项；
3. 本目录的全局规范；
4. Netflix、BBC、DCMP 等外部参考。

外部规范用于形成可查询的质量基线，不代表本仓库是任何平台的交付项目。不同来源出现冲突时，不能机械选择更严格的数值，而应优先保证原意、目标片源同步、中文可读性和双语视觉稳定。

## 统一设计原则

- 只维护一套以简体中文为主的字幕设计规范。
- 中文主字幕位于上方，英语或日语副字幕位于下方。
- 时间轴、分轴和画面布局以中文阅读体验为主，副语不得迫使中文过度压缩或错误断句。
- 其他语言规范只用于拼写、标点、专名等语言正确性，不单独决定字体、位置、行数或时间轴。
- 双语字幕默认一条中文配一条副语，起止时间完全一致。

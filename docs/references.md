# 行业参考与本仓库取舍

访问日期均为 2026-08-26。外部页面可能更新，使用前应核对其最新版本。

## R1 Netflix 简体中文字幕规范

[Chinese (Simplified) Timed Text Style Guide](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215986007-Chinese-Simplified-Timed-Text-Style-Guide)

采用的参考点：简体中文每行 16 字、通常最多两行、成人 9 字符/秒、儿童 7 字符/秒、极简标点、自然断行、剧情相关画面文字优先和语言语气忠实。

本仓库调整：因为产物是中英或中日双语，总行数优先分配为“一行中文主字幕 + 一行副字幕”；不套用单语双说话人一人一行的布局。

## R2 Netflix 通用和时间轴规范

- [Timed Text Style Guide: General Requirements](https://partnerhelp.netflixstudios.com/hc/en-us/articles/215758617-Timed-Text-Style-Guide-General-Requirements)
- [Timed Text Style Guide: Subtitle Timing Guidelines](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines)

采用的参考点：约 5/6 秒最小时长（24 fps 为 20 帧）、7 秒最大时长、2 帧间隔、入点接近发声首帧、结合镜头切换处理时间轴、画面文字尽量匹配实际显示时长。

本仓库调整：可靠的目标视频内嵌轨优先于机械阈值。数值通常用于发现候选问题，是否改轴必须结合实际音画判断；但非法、非预期重叠、明显不可读或严重不同步的事件触发仓库纠错底线，不得以内嵌来源为由保留。

## R3 BBC Subtitle Guidelines

[BBC Subtitle Guidelines](https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/)

采用的参考点：尽量忠实保留原语、不要无谓简化、保留人物语域、在语义自然位置换行、语言结构优先于几何形状，以及时间判断必须综合语速、镜头和画面。其 Typography 章节同时说明在线字幕通常应使用平台可读的无衬线字体，非平台字体可能降低清晰度；本仓库据此采用开放授权、跨平台且覆盖中日文地区字形的现代黑体。

BBC 的英语词/分钟指标不直接换算为中文字符/秒，只作为“不能只看字符数”的方法论参考。

## R4 DCMP Captioning Key

- [Elements of Quality Captioning](https://dcmp.org/learn/599-captioning-key---elements-of-quality-captioning)
- [Presentation Rate](https://dcmp.org/learn/601-captioning-key---presentation-rate)

采用的参考点：准确、一致、清晰、可读、等值；字幕应与声音同步并尽量保留原始内容，压缩时必须保留意义、内容和关键术语。

DCMP 面向同语字幕和无障碍字幕，其英语 WPM 数值不作为本仓库中文翻译字幕的硬阈值。

## R5 Noto Sans CJK

- [Noto CJK 官方仓库](https://github.com/notofonts/noto-cjk)
- [SIL Open Font License 1.1](https://openfontlicense.org/open-font-license-official-text/)

采用的参考点：使用覆盖简体中文、日文和拉丁字符的现代无衬线字体，并分别采用 SC 与 JP 地区字形。正式依赖静态字体，不把可变字体或历史 ASS `[Fonts]` 嵌入作为最低兼容方案。

Noto Sans CJK 是本仓库的工程选择，不代表 BBC、Netflix 或其他平台指定该字体。外部行业参考提供的是无衬线、清晰、可预测回退等原则，本仓库再结合开源授权和中日双语覆盖确定具体字体。

## 用户提供的参考指南

设计过程参考了《主流流媒体平台 中文字幕商业规范指南.md》。该文件是汇总性参考，不作为平台官方规范复制入仓库。附件中的 16 CPL、两行、时长、间隔、断句和极简标点被逐项与公开来源核对；其中 12–16 中文 CPS 与 Netflix 当前公开的成人 9、儿童 7 字符/秒不一致，因此本仓库采用较保守的 Netflix 中文检查基线。

## 使用外部规范的原则

- 外部规范是证据，不是可以脱离项目复制的指令。
- 平台专属规则不能自动覆盖作品补充规范。
- 不同指标冲突时，优先保证原意、目标片源同步、中文主字幕可读性和双语视觉稳定。
- 每次引用会影响实际修改的外部规则时，应在修改台账中写明参考编号。

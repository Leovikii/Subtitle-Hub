# SH0001 历史工程归档

## 归档状态

- 归档日期：2026-08-26；
- 状态：已生成、解包并逐文件验证；
- 压缩包：[SH0001-legacy-engineering-20260826.zip](../project/archive/SH0001-legacy-engineering-20260826.zip)；
- 外部清单：[SH0001-legacy-engineering-20260826.manifest.tsv](../project/archive/SH0001-legacy-engineering-20260826.manifest.tsv)；
- 压缩包大小：1,967,950 字节；
- 压缩包 SHA-256：`2bd01f8d6e9cb95f7f862e78a8ad4a00d4ce7a074c4b4b9f147acde5975e1206`；
- 外部清单 SHA-256：`551b8d59d21d5d57e5aee30fdac4cfff872efdd10c1e974ef4da547c4553709b`。

压缩包内另含同内容的 `MANIFEST.tsv`。归档时已按清单重新解包，39 个历史源文件的路径、大小和 SHA-256 全部一致；压缩包共有 40 个文件条目（39 个历史文件和 1 个内部清单），另有 4 个目录条目。

## 内容范围

| 原位置 | 数量 | 内容 | 当前定位 |
| --- | ---: | --- | --- |
| `project/pipeline/legacy/` | 17 | 旧处理、验证和审查脚本 | 一次性历史工具 |
| `docs/review-ledgers/legacy/` | 19 | TV 历史候选表和实施明细 | 历史审查证据 |
| `docs/legacy/` | 2 | 旧三语审查方案和综合报告 | 旧工程说明 |
| `docs/legacy-scripts.md` | 1 | 历史脚本用途说明 | 旧工程说明 |

源文件合计 39 个、5,105,419 字节。完成归档验证后，以上散落副本以及空的旧 `project/pipeline/` 已从活动工程中移除。

## 使用限制

- 这些脚本包含旧绝对路径、旧目录结构，并有同时处理 TV 和剧场版的历史假设，不能在当前工程直接运行。
- 历史候选表只说明旧规则曾发现或处理的项目，不代表当前规范下已经人工复核。
- 旧方案和报告用于追溯 v1.0.0 形成过程，不覆盖当前全局规范和项目补充规范。
- 当前校对不得把压缩包内任一文件当作活动主稿、现行 pipeline 或发布输入。

## 恢复方法

确需追溯时，将压缩包解压到 `project/workspace/temp/intermediate/legacy-restore/`，使用外部清单核对逐文件 SHA-256 后只读检查。不得解压回原路径，不得覆盖 `workspace/episodes/`、`sources/`、`docs/` 或 `subtitles/`。追溯结束后可以删除整个 `legacy-restore/`。

# 项目文档、进度与台账规范

## 1. 标准位置

每个作品的人工可读工程文档统一放在作品根目录 `docs/`：

```text
docs/
├─ project-guide.md
├─ progress.yaml
├─ change-log.tsv
├─ issues.tsv
├─ release-changelog.md
├─ migration.md
├─ reports/
├─ review-ledgers/
└─ engineering-archive.md            # 仅在存在历史工程归档时建立
```

项目根目录只保留一个必要的 `README.md` 作为入口。其他来源、工作区、审查、脚本和发布子目录不再分散放置说明文档；只有独立使用该目录时确实无法理解其用途，才允许保留简短 README。

## 2. project-guide.md

必须说明：

- 作品范围和不包含内容；
- 中文主字幕和副语类型；
- 时间轴主参考、原语主参考、中文底稿；
- 样式名称、位置和特殊画面处理；
- 全局规范的项目覆盖项；
- 当前基线和下一目标版本；
- 已知限制与不得自动处理的部分。

## 3. progress.yaml

必须同时记录整体阶段和逐集状态。推荐状态值：

- `not-started`
- `in-progress`
- `candidate-review`
- `blocked`
- `baseline-released`
- `verified`

进度必须反映实际完成的检查，不能因旧版本已经发布就自动标记新一轮校对完成。

## 4. change-log.tsv

每个实质修改事件一行，使用稳定列：

```text
change_id batch_id date episode start end category severity before after source_ref rationale status agent reviewer
```

- `source_ref` 指向原语来源、音轨、术语决策或画面证据；
- `before` 和 `after` 保存足够审阅的文本；
- `category` 使用全局错误类型；
- `status` 使用 `applied`、`verified`、`reverted`；
- 批量修改共享 `batch_id`，但不省略逐事件行。

## 5. issues.tsv

未解决问题一行一个，使用：

```text
issue_id date episode start end category severity description evidence proposed_action status owner resolution
```

状态使用 `candidate`、`confirmed`、`in-progress`、`blocked`、`fixed`、`verified`、`wont-fix`。`wont-fix` 必须记录理由。

## 6. reports、review-ledgers 与工程归档

- `reports/` 保存面向人类的阶段或发布检查报告；
- `review-ledgers/` 只保存需要跨轮次追踪或支持发布审计的候选表和实施明细；普通未审输出留在 `project/workspace/temp/review/`；
- 停止维护的旧脚本、旧审查表和旧工程说明不应继续散落在 `docs/` 或活动工作区，应按 [工程区与归档规范](workspace-and-artifacts.md) 压缩到 `project/archive/`；
- 存在历史档案时，以 `engineering-archive.md` 记录范围、清单、校验值、恢复方式和不可直接运行的限制；
- 报告必须写明生成时间、输入版本、检查范围、工具检查和人工检查的区别。

## 7. 模板

新项目可以复制：

- [templates/project-guide.template.md](templates/project-guide.template.md)
- [templates/progress.template.yaml](templates/progress.template.yaml)
- [templates/change-log.template.tsv](templates/change-log.template.tsv)
- [templates/issues.template.tsv](templates/issues.template.tsv)

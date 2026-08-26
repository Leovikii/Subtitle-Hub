# AI agent 基准文档与开发者审核文档规范

## 1. 两种面向对象

项目文档分为两个彼此隔离的层面：

| 层面 | 面向对象 | 路径 | 生命周期 | 是否构成工作基准 |
| --- | --- | --- | --- | --- |
| AI agent 控制面 | AI agent、维护者 | 项目 `docs/` | 长期维护并纳入 Git | 是 |
| 开发者审核面 | 人工审核者 | `project/workspace/temp/review/` | 本轮临时文件，反馈回写后可清理 | 否 |

AI agent 每次开工必须读取控制面，防止在长轮次优化中遗忘规则、范围、进度和未解决问题。开发者审核报告只用于呈现候选修改、机器检查和待决事项，不能直接成为新规则或当前进度。

人工反馈确认后，必须回写控制面：

- 新增或调整规则 → `docs/project-guide.md`；
- 更新工作范围和完成度 → `docs/progress.yaml`；
- 已实施修改 → `docs/change-log.tsv`；
- 未解决或被退回的问题 → `docs/issues.tsv`。

完成回写后，审核报告及附件可以从临时区清理。不得要求后续 AI agent 依赖一份旧审核报告才能理解当前项目。

## 2. AI agent 控制面固定结构

项目 `docs/` 根目录只保留以下五个活动文件：

```text
docs/
├─ README.md          # 控制面入口，不复制规则和进度
├─ project-guide.md   # 唯一项目补充/覆盖规范
├─ progress.yaml      # 当前进度唯一事实源
├─ change-log.tsv     # 已实施修改台账
└─ issues.tsv         # 未解决问题台账
```

旧迁移说明、旧审查报告、旧发布总结等历史文件必须移出活动控制面，进入 `project/archive/`。若旧发布元数据引用活动控制面外的历史报告，应在采用本规范时执行一次登记在案的结构迁移：先归档并验证报告，再删除引用或改为明确的覆盖范围字段。完成迁移后不得保留兼容性报告目录。

来源、工作区、构建和发布目录不得散落现行规范或进度文档。项目根目录可以保留一个简短 `README.md` 作为作品入口。

## 3. README.md：控制面入口

项目 `docs/README.md` 必须包含：

- 全局规范入口和规则优先级；
- 四类基准文件的用途；
- 开发者审核临时区位置；
- “当前状态只以 progress.yaml 为准”的声明。

它不得复制项目具体规则、逐集状态、问题数量或审核结论，避免形成第二份事实源。

## 4. project-guide.md：唯一项目规范

只有 `project-guide.md` 可以补充或覆盖全局规范。必须使用固定章节：

1. 范围与语言；
2. 来源权威分工；
3. 本项目重点风险；
4. 样式与特殊布局；
5. 项目补充和覆盖规则表；
6. 工程区约束；
7. 已知限制和禁止自动处理项。

规则表固定列为：

```text
rule_id type global_ref scope rule rationale
```

- `type` 只能是 `supplement` 或 `override`；
- `global_ref` 指向被细化或覆盖的全局文档章节；
- `scope` 说明适用集数、样式、场景或版本；
- `rule` 使用可执行的“必须/不得/可以”语言；
- `rationale` 说明作品或片源为何需要该规则。

项目规范不得保存当前进度、阶段结论、逐条问题、版本更新记录或大段历史过程。

## 5. progress.yaml：当前进度唯一事实源

`progress.yaml` 只描述当前活动轮次和逐集状态。历史轮次结束后将有效结论写回台账；不得在进度文件中叠加多套 `inherited_*`、`previous_*` 或自由命名阶段。

固定顶层字段：

```text
schema_version work_id updated_at baseline_release target_release overall_status active_round stages episodes
```

固定阶段：

```text
source_inventory baseline_setup translation_review timing_review typography_review visual_review release_qc
```

阶段和逐集状态只能使用 `not-started`、`in-progress`、`candidate-review`、`blocked`、`verified`、`not-applicable`。`baseline-released` 和 `released` 只用于 `overall_status`。

每次开始、暂停、完成、退回或改变范围时，必须更新 `updated_at`、`active_round` 和受影响的逐集状态。审核报告中的勾选和统计不能代替进度更新。

## 6. change-log.tsv：已实施修改台账

固定列为：

```text
change_id batch_id date episode start end category severity before after source_ref rationale status agent reviewer
```

- 每个实质字幕修改事件一行；批量规则可以共享 `batch_id`，但不得省略逐事件明细；
- 文档架构、迁移和发布元数据变更可以使用 `episode=ALL`；
- `source_ref` 必须指向原语、音轨、画面、术语决策或现行规则，不得只指向可清理的临时报告；
- `status` 只能使用 `applied`、`verified`、`reverted`；
- 未实施候选进入 `issues.tsv`，不得提前写入本表。

## 7. issues.tsv：问题台账

固定列为：

```text
issue_id date episode start end category severity description evidence proposed_action status owner resolution
```

状态只能使用 `candidate`、`confirmed`、`in-progress`、`blocked`、`fixed`、`verified`、`wont-fix`。`fixed` 表示已修改但尚未复核；`verified` 表示修改或处置已经复核。`wont-fix` 必须记录理由和批准人。

自动检查的大量原始输出先留在开发者审核临时区，确认需要跨轮次跟踪后才按实际问题粒度写入本表。

## 8. 开发者审核面

统一位置：

```text
project/workspace/temp/review/
├─ review-<round-id>-<scope>.md
└─ attachments/
```

审核报告是本轮临时工程文件，默认不纳入 Git。它可以复制或导出给开发者审阅，但不得被 `project-guide.md`、正式字幕或发布元数据建立运行时依赖。

报告必须写明：

- 报告 ID、项目 ID、轮次、范围、基线和生成日期；
- 机器检查与人工检查各自实际覆盖范围；
- 候选修改、证据、风险和需要开发者回答的问题；
- 建议回写到规范、进度、修改台账或问题台账的内容；
- 报告状态：`draft`、`awaiting-review`、`feedback-received` 或 `closed`。

开发者反馈不能只留在报告内。agent 必须把确认结果回写控制面，再把报告标为 `closed` 或清理。若某份报告因审计要求必须长期保存，应经用户明确要求后压缩到 `project/archive/`，而不是放回活动 `docs/`。

## 9. 模板

新项目必须从以下模板建立控制面和审核报告：

- [templates/project-docs-readme.template.md](templates/project-docs-readme.template.md)
- [templates/project-guide.template.md](templates/project-guide.template.md)
- [templates/progress.template.yaml](templates/progress.template.yaml)
- [templates/change-log.template.tsv](templates/change-log.template.tsv)
- [templates/issues.template.tsv](templates/issues.template.tsv)
- [templates/report.template.md](templates/report.template.md)

---
report_id: "{{REPORT_ID}}"
work_id: "{{WORK_ID}}"
round_id: "{{ROUND_ID}}"
scope: "{{SCOPE}}"
baseline: "{{BASELINE}}"
created_at: "{{CREATED_AT}}"
status: draft
machine_coverage: none
human_coverage: none
---

# 审核报告

## 审核目的与范围

说明需要人工判断的事项和不覆盖的内容。

## 输入与检查覆盖

列出主稿、目标片源、参考字幕及机器/人工检查的实际范围。

## 候选修改与证据

按集数与时间点记录候选、文字结论、风险和本地证据路径。不得在对话中批量附图。

## 需要开发者确认

无。

## 建议回写控制面

- `project-guide.md`：
- `progress.yaml`：
- `change-log.tsv`：
- `issues.tsv`：

## 反馈与关闭

记录反馈和回写结果。完成回写后改为 `closed`，即可清理本报告及附件。

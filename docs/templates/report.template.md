---
report_id: <WORK_ID-REVIEW-ID>
work_id: <WORK_ID>
round_id: <ROUND-ID>
scope: <episode/range/all>
baseline: <version-or-source>
created_at: <YYYY-MM-DD>
status: draft
machine_coverage: none
human_coverage: none
---

# <审核报告标题>

## 审核目的与范围

说明本报告需要开发者判断什么，以及不覆盖哪些内容。

## 输入与检查覆盖

列出主稿版本、片源、参考字幕和机器/人工检查的实际范围。

## 候选修改与证据

按可复核粒度列出候选、证据、风险和建议。

## 需要开发者确认

列出明确问题；没有则写“无”。

## 建议回写控制面

- `project-guide.md`：
- `progress.yaml`：
- `change-log.tsv`：
- `issues.tsv`：

## 反馈与关闭

记录开发者反馈，以及是否已经回写控制面。完成回写后将状态改为 `closed`，本报告即可清理。

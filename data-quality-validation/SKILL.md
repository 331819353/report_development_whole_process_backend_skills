---
name: data-quality-validation
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于真实数据质量规则设计、执行和可信度验收。用户提到数据质量、完整性、筛选前数据完整性、筛选数据粒度、唯一性、及时性、准确性、异常值、重复数据、缺失数据、数据延迟、口径漂移、跨源一致性、接口正常但数据不可信、生产数据校验、质量规则、数据质量报告时触发；不负责API契约或页面展示核对。"
---

# Data Quality Validation

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Overview

Use this skill to design or execute data quality checks for report delivery and production acceptance. It focuses on whether data is trustworthy, not merely whether APIs return successfully.

## Inputs

- Data model, source table/API metadata, metric dictionary, API samples, production exports, SQL snippets, data files, reconciliation rules, refresh SLA, or incident examples.
- Optional: expected thresholds, source owner, refresh schedule, historical baseline, business calendar, and critical metric list.

Use `$delivery-artifact-template-management` when producing a reusable data-quality rule matrix.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Define quality scope.
   Identify critical metrics, dimensions, source tables/APIs, response fields, reporting period, data grain, and consumers.

2. Classify checks.
   Cover completeness, filter-scope completeness, uniqueness, timeliness, accuracy, validity, range/outlier, referential integrity, drift/口径漂移, cross-source consistency, and permission-sensitive data leakage.

   When the report has filters, completeness must be checked before filter linkage: option dimensions, fact rows, required fields, permission-scoped rows, default and non-default filter states, empty-state combinations, and resolver/API branches must exist at the grain needed by every affecting primary filter.

3. Write executable rules.
   For each rule, specify data object, field/metric, condition, threshold, frequency, owner, SQL/API/check expression, and failure action.

4. Compare against business expectation.
   Check totals, subtotals, TopN, rankings, period-over-period values, and cross-report numbers against source-of-truth or approved baseline.

5. Assess failures.
   Classify as blocker/high/medium/low. Distinguish source-data issue, transformation issue, API aggregation issue, frontend display issue, permission filter issue, or stale cache.

6. Define monitoring.
   For production-bound data, link quality rules to SLA alerts and `$production-observability-feedback`.

## Required Output

- Data quality scope: source objects, metrics, periods, grain, consumers.
- Rule matrix: rule ID, dimension, field/metric, expression, threshold, frequency, owner, evidence.
- Execution result: passed/failed/blocked/not run, sample records, counts, timestamps, query/API evidence.
- Trust conclusion: pass / partial / fail / blocked, with impact on report acceptance.
- Defects or blockers: likely owner, reproduction query/API, expected vs actual, retest criteria.
- Production monitoring handoff: quality rules that need scheduled checks or alerting.

## Quality Checklist

- Quality checks cover real business correctness, not only non-empty responses.
- Filter-related quality checks prove the data can support filtering before UI binding is accepted; a single default snapshot is not sufficient for affecting filters unless the component is explicitly invariant.
- Time freshness and late-arriving data rules are explicit.
- Cross-source and cross-report reconciliation is included when figures must match.
- Failures include evidence and likely owner.
- Acceptance is not marked ready when critical data-quality checks are not run.

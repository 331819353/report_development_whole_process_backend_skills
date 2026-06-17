---
name: production-observability-feedback
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于报表上线后的监控、运维、埋点和运营反馈闭环。用户提到上线后监控、接口监控、前端错误监控、性能监控、页面埋点、用户行为反馈、异常告警、数据刷新SLA、可用性、接口耗时、失败率、前端白屏、生产验收时触发；不替代联调测试。"
---

# Production Observability Feedback

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Overview

Use this skill to design post-release monitoring and feedback loops for report systems. It extends delivery beyond integration testing into production quality and usage effectiveness.

## Inputs

- Frontend/backend URLs, API list, data refresh rules, deployment topology, logs/metrics platform, analytics tool, alert channel, owner roster, SLA, release version, known risks, or production incidents.
- Optional: existing monitoring config, SLO targets, user roles, feedback channels, and support process.

Read `references/01-observability-feedback-template.md` when producing a reusable monitoring plan.
Use `$environment-profile-contract` when monitoring depends on test/production runtime profile separation, endpoint ownership, or release acceptance configuration.
Use `$report-delivery-pipeline-governance` when production feedback must route back into defect retest, release readiness, or next delivery iteration.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Define monitored surfaces.
   Include page availability, API availability/latency/errors, frontend runtime errors, white screen, asset loading, data refresh SLA, data quality rules, export jobs, SSO/auth failures, and user behavior events.

2. Define metrics and thresholds.
   Specify indicator, threshold, severity, frequency, owner, alert channel, evidence, and escalation path.

3. Define instrumentation.
   List frontend events, API logs, trace IDs, request IDs, custom metrics, dashboard panels, synthetic probes, and data refresh jobs.

   For backend/data-service surfaces, require structured logging configuration and safe fields: log level/format, requestId/traceId propagation, redaction rules, request/auth/validation/query/cache/pool/export/job/error log points, slow-query/report thresholds, sampling, retention, and error-envelope correlation.

4. Define alert response.
   For every alert, include triage owner, diagnosis evidence, rollback/fallback, user communication, and retest/closure criteria.

5. Define feedback loop.
   Capture user behavior, low-usage pages, failed searches/filters, export frequency, feedback tickets, and requested improvements. Route product changes to `$change-impact-analysis`.

6. Link to delivery versions and delivery pipeline.
   Every production result must state release version, frontend/backend/API/data versions, and whether the issue belongs to current or older release.
   Route production issues to `$report-delivery-pipeline-governance` for retest/release-chain closure and to `$change-impact-analysis` before implementation changes.

## Required Output

- Monitoring scope: pages, APIs, jobs, data refresh, SSO, exports, roles.
- Metric/alert matrix: indicator, threshold, severity, owner, channel, response.
- Instrumentation plan: logs, metrics, traces, frontend events, synthetic checks.
- Backend logging plan when backend/data-service is in scope: structured fields, log levels, request/trace id propagation, redaction, required log points, slow-query/report thresholds, sample safe log lines, retention, and owner dashboard/query paths.
- Data refresh SLA and data-quality monitoring plan.
- User behavior and feedback loop: event names, dashboard, review cadence, owner actions.
- Incident/defect closure process: evidence, likely owner, rollback, retest, version linkage.
- Production readiness conclusion: ready / partial / blocked.

## Quality Checklist

- API success, page rendering, data freshness, and business data quality are monitored separately.
- Alerts have thresholds, owners, and response playbooks.
- Frontend events avoid collecting sensitive data.
- Backend logs avoid secrets, tokens, raw personal data, raw SQL values, raw permission scopes, and full report payloads while retaining enough request/query/cache/pool/export/error context for diagnosis.
- User feedback routes to change-impact analysis before implementation.
- Production conclusions link to exact delivery/release versions.

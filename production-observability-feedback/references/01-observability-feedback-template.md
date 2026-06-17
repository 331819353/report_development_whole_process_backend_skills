# Observability and Feedback Template

## Monitoring Matrix

| Monitor ID | Surface | Indicator | Threshold | Severity | Frequency | Evidence/source | Alert channel | Owner | Response playbook | Release/rollback link | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## Instrumentation Plan

| Event/metric/log | Location | Fields | Sampling | Privacy note | Consumer dashboard | Owner |
| --- | --- | --- | --- | --- | --- | --- |

For report release monitoring, include API latency/error/timeout, slow query count, cache hit rate, export task count/backlog/failure, data refresh delay, core metric anomaly, permission errors, and release-smoke synthetic checks when in scope.

## Backend Structured Logging Plan

| Log ID | Log point | Required fields | Level | Sampling/threshold | Redaction/privacy | Retention/query path | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| LOG-001 | request ingress/egress | requestId, traceId, service, env, version, method, route, status, latencyMs | info/warn/error | all errors, all slow, sample success if needed | no tokens/cookies/raw payloads |  |  |
| LOG-002 | auth/permission/validation | requestId, route, reasonCode, status, tenant/user/role hash when safe | info/warn | all rejects | no raw token or raw permission scope |  |  |
| LOG-003 | query/cache/pool | requestId, reportId, widgetId, queryId, dataVersion, source, cacheStatus, durationMs, rowCount, poolWaitMs | info/warn/error | warn above slow thresholds | no raw SQL values or sensitive filters |  |  |
| LOG-004 | export/job/error | requestId, taskId, jobStatus, exportRowCount, errorCode, sanitizedMessage | info/warn/error | all lifecycle and all failures | no sensitive file path or raw export payload |  |  |

## Feedback Loop

| Feedback source | Signal | Review cadence | Owner | Decision rule | Routed workflow | Status |
| --- | --- | --- | --- | --- | --- | --- |

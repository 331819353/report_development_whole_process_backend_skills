# Data Service Design Template

Use this template when the user asks for 数据服务设计, 后端方案, API服务设计, query-service design, or a production-bound backend/data-service handoff.

## Stable IDs

Use these prefixes consistently:

- Service layers: `SVC-001`
- Data-service decisions: `ADR-DS-001`
- API rows: `API-001`
- Source models: `SRC-001`
- Logical models: `LGM-001`
- Response models: `RSP-001`
- Metrics: `MET-001`
- Permission rules: `PERM-001`
- Data quality rules: `DQ-001`
- Source/response mappings: `MAP-001`
- Presentation boundary rules: `PRES-001`
- Cache/precompute rules: `CACHE-001`
- Snapshot/version contracts: `SNAP-001`
- Async jobs/exports: `JOB-001`
- Observability signals: `OBS-001`
- Code file ledgers: `CODELOG-001`
- Environments/source modes: `ENV-001`
- SSO/auth decisions: `SSO-001`
- Database role/runtime decisions: `DB-001`
- Gaps: `GAP-001`
- Risks: `RISK-001`

## 1. 数据服务设计总览

Open with 3-7 concise bullets:

- service purpose and business/module scope;
- upstream technical-solution linkage, such as `ARC-*`, `ADR-*`, `API-*`, `LGM-*`, `NFR-*`, `GAP-*`;
- selected backend/data-service stack;
- core architecture and query-service approach;
- runtime/security/observability/release approach;
- readiness verdict and top blockers.

## 2. 输入、范围与上游衔接

| Input ID | Source | Upstream artifact | Authority | Covered scope | Uncertainty/GAP |
| --- | --- | --- | --- | --- | --- |
| IN-001 | technical solution / API inventory / data model / prototype / source doc / existing code | ARC-*/ADR-*/API-*/LGM-* | authoritative / supporting / obsolete / TBD |  | none / TBD(GAP-*) |

State:

- in scope;
- out of scope;
- expected consumers: frontend, API docs, testing, operations, downstream services;
- authoritative stack or default stack decision;
- implementation mode: design only / API documentation / implementation / repair.

## 3. 服务边界与分层架构

| Layer ID | Layer | Responsibility | Inputs | Outputs | Owner/source | Status |
| --- | --- | --- | --- | --- | --- | --- |
| SVC-001 | API/controller | routes, validation handoff, auth middleware, error envelope, health/readiness | HTTP request | service request / response envelope | ADR-* | ready / partial / blocked |
| SVC-002 | application/service | use-case orchestration, query context, idempotency, audit hooks | API request | query/export/action command | ADR-* | ready / partial / blocked |
| SVC-003 | metadata/governance | report/dataset/dimension/metric/filter/sort metadata and whitelist | metadata source | governed query metadata | LGM-* / MET-* | ready / partial / blocked |
| SVC-004 | query/planning | parameter guardrails, permission injection, sync/async decision, query grade | QueryContext | QueryPlan | API-* / NFR-* | ready / partial / blocked |
| SVC-005 | repository/source adapter | DB/upstream/file access, source predicates, pooling, retries | QueryPlan | source rows / aggregates | SRC-* | ready / partial / blocked |
| SVC-006 | transformation/formatter | source-to-response mapping, DTO, precision/unit/enum/defaults | source result | RSP-* | RSP-* | ready / partial / blocked |
| SVC-007 | cache/precompute | Redis/cache/precompute lookup, invalidation, fallback | QueryContext | cache hit/miss/value | NFR-* | ready / partial / blocked |
| SVC-008 | async/export | task lifecycle, queue/worker, file write, retention, download | ExportRequest | TaskStatus/file | NFR-* | ready / partial / blocked |
| SVC-009 | security/permission | identity, tenant/org/data scope, field/action/export permission, masking | auth context | permission predicates and field rules | PERM-* | ready / partial / blocked |
| SVC-010 | operations/runtime | logs, metrics, traces, pools, health, release, rollback | runtime events | evidence/alerts | NFR-* | ready / partial / blocked |

Use a Mermaid or text diagram when helpful, but keep the table as the stable contract.

## 4. 技术栈与运行时决策

| Decision ID | Area | Decision | Type | Reason | Impact | Status |
| --- | --- | --- | --- | --- | --- | --- |
| ADR-DS-001 | backend/data-service | Python + Flask + connection pools + Redis | default / override / existing |  | API docs, implementation, ops | ready / partial / blocked |

Required areas:

- HTTP framework and service composition;
- database/upstream client and pooling;
- Redis/cache/precompute;
- async job/export worker;
- auth/SSO middleware;
- Python/Flask SSO and multi-database baseline when applicable;
- config/secrets/environment;
- logging/metrics/tracing;
- deployment/runtime target;
- testing and contract validation.

## 5. QueryContext 与参数护栏

Every data-bearing endpoint must construct a query context before reading business data.

| Context area | Fields | Source | Validation/defaulting | Downstream use | Status |
| --- | --- | --- | --- | --- | --- |
| client params | reportId, filters, dimensions, metrics, page, sort, drilldown, export fields | request | whitelist, required filters, max limits | query planner | ready / partial / blocked |
| data version | snapshotDate, latestPeriod, loadBatch, dataVersion, sourceVersion | request/default/source metadata | default latest, reject invalid/expired | source predicate/cache key | ready / partial / blocked |
| permission scope | tenantId, userId, roleHash, org/data range, field visibility, export permission | auth/permission service | backend injected only | SQL predicates/cache key/masking | ready / partial / blocked |
| guardrails | date range, max page size, max IN, max dimensions/metrics, query grade | metadata/NFR | sync/async/reject decision | planner/export | ready / partial / blocked |

## 6. API Family And Service Mapping

| API ID | Family | Endpoint | Consumer | Service mapping | Request model | Response envelope | Runtime policy | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| API-001 | metadata / filter / query / dashboard / detail / export / action / health |  | page/component/service | controller -> service -> planner -> repository -> formatter | QueryContext/PageRequest/ExportRequest | Page<T>/OptionItem/KpiCard/SeriesData/TaskStatus/Meta/Error | sync/cache/async/TBD | ready / partial / blocked |

Custom endpoint shapes require a reason:

- different source grain;
- different permission lifecycle;
- different latency/SLA;
- different mutation/action semantics;
- legacy compatibility.

## 7. Source Adapter And Transformation Design

| Mapping ID | API/Model | Response field | Source field/formula | Transform/default/null rule | Unit/precision/enum | Compatibility | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MAP-001 | RSP-001 |  | SRC-* |  |  | unchanged / additive / breaking | ready / partial / blocked |

Rules:

- existing response fields are stable contracts;
- source/table/upstream replacement belongs in adapters, aliases, serializers, or mapping code;
- breaking changes require versioning, deprecation, frontend/test impact, and rollback/compatibility plan;
- contract tests should cover default, filtered, empty, no-permission, and source-replacement states.

## 8. Data Vs Presentation Boundary

Data services should keep display composition flexible for frontend implementation.

| Boundary ID | API/Model | Backend returns | Frontend owns | Server-owned text exception | Status |
| --- | --- | --- | --- | --- | --- |
| PRES-001 | API-*/RSP-* | structured values, units, enums, status codes, reason codes, message keys, message params, column metadata | title/copy composition, conclusion wording, styling, layout, localization, emphasis, line breaks | legal/audit/notification/error/governed explanation only, with reason | ready / partial / blocked |

Rules:

- Prefer structured fields such as `value`, `unit`, `ratio`, `trendDirection`, `delta`, `thresholdLevel`, `reasonCode`, `messageKey`, and `messageParams`.
- Do not return avoidable concatenated strings such as `"完成率 85%，较上月提升 3%"` when frontend can compose from structured fields.
- Do not return HTML, Markdown, rich text, style class names, or pre-highlighted conclusion text from data APIs unless the endpoint is explicitly a content/notification service.
- Display labels, enum labels, column names, error messages, no-permission messages, audit text, or regulated statements may be backend/server-owned when documented.
- If a conclusion is generated by backend because it is governed, model-produced, or audit-bound, return the conclusion type, source, confidence/status, variables, and raw evidence fields alongside the text.

## 9. Redis, Cache, And Precompute Design

Connection-pool lifecycle contract:

- Database/upstream pool owner:
- Pool config keys and max size, such as `STARROCKS_POOL_MAX`:
- Acquire timeout, idle timeout, validation, and safe shutdown:
- Release/close pattern: context manager / `try-finally` / `defer` / `using` / framework-owned:
- Exception cleanup coverage: `ApiError`, timeout, cancellation, validation error after acquire, formatter error, early return, generic exception:
- Repeated-failure proof: simulate repeated `ApiError` and confirm active/idle pool counts return to normal and later requests can acquire a connection:

| Cache ID | Role | Key dimensions | Value shape/size | TTL/invalidation | Miss/stampede behavior | Fallback | Metrics | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CACHE-001 | metadata / permission / result / widget / snapshot / rate-limit / lock / idempotency / job-progress | tenant, user/role, report, dataVersion, filters, page/sort |  | TTL+jitter/source-version/publish rollback | singleflight/lock/warmup | stale last-success / bypass / fail closed | hit ratio, latency, errors | ready / partial / blocked |

Required Redis operational contract:

- pool size and timeouts;
- retry/backoff limits;
- permission/tenant safety;
- max value size;
- no request-path `KEYS` or broad `SCAN`;
- lock TTL and owner token when locks are used;
- durable-store boundary for audit/export records.

## 10. Snapshot And Data-Version Contract

| Contract ID | Snapshot role | Version fields | Producer/default source | Consumers | Grain/permission scope | Cache/source lookup | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SNAP-001 | overview payload / canonical shared dataset / local demo artifact | snapshotDate/latestPeriod/loadBatch/dataVersion | metadata/source/precompute/cache | API-* |  | source predicate / precompute key / cache key | ready / partial / blocked |

No endpoint may depend on hidden controller memory, frontend call order, or another endpoint's undocumented response payload for production correctness.

## 11. Permission, Security, And Audit

| Rule ID | Area | Decision | Applies to | Evidence/source | Status |
| --- | --- | --- | --- | --- | --- |
| PERM-001 | auth / tenant / row / field / action / export / masking / audit |  | API-*/field/export/task | IN-* | ready / partial / blocked |

Cover:

- identity source and token/header contract;
- tenant/org/data-scope injection;
- field visibility and masking;
- export/download permission;
- secret/config handling;
- query/export/download/config-change audit;
- no-permission and unauthorized response shape.

## 11A. Python Flask SSO And Multi-Database Contract

Use this section when Python/Flask, SSO, or multiple databases are in scope.

| Contract ID | Area | Decision | Config/env | Runtime owner | Status |
| --- | --- | --- | --- | --- | --- |
| SSO-001 | SSO token validation | `Access-Token`, optional `Application-Key`, token-check service, local user mapping, 401/403 split | `SSO_VALIDATE_URL`, `SSO_TOKEN_HEADER`, `APPLICATION_KEY_HEADER` | middleware + SSO service + permission service | ready / partial / blocked |
| DB-001 | SQLite role | local/test/fixture/demo only unless explicitly approved | `SQLITE_DATABASE_URL` | sqlite repository / fixture setup | ready / partial / blocked |
| DB-002 | MySQL role | users, roles, permissions, configs, ordinary business data | `MYSQL_DATABASE_URL`, pool vars | MySQL repository / SQLAlchemy engine | ready / partial / blocked |
| DB-003 | Oracle role | enterprise legacy/core source integration | `ORACLE_DATABASE_URL`, pool vars | Oracle repository / SQLAlchemy engine | ready / partial / blocked |
| DB-004 | StarRocks role | analytics/report/metric/wide-table aggregation queries | `STARROCKS_DATABASE_URL`, `STARROCKS_POOL_SIZE` | StarRocks repository / SQLAlchemy engine | ready / partial / blocked |

Required decisions:

- app factory, versioned Blueprint, service, repository, db engine/session, schema, middleware, utils, SQL, tests, and deployment file ownership;
- SSO token validation sequence and public-route allowlist;
- local user, role, permission, org/data-scope mapping;
- per-database SQLAlchemy engine/session lifecycle and guaranteed release/close behavior;
- SQL directory split by database/dialect and no raw user-controlled SQL;
- dependency and deployment baseline: requirements, WSGI, Gunicorn, Docker, Nginx/gateway, health/readiness, env profile separation;
- test proof for missing token, invalid token, valid-token/no-permission, and at least one declared database-backed query path.

## 12. Export And Long-Running Work

| Job ID | Work type | Trigger | Queue/worker limit | State store | Retention | Permission/audit | Failure behavior | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| JOB-001 | export / report generation / refresh / snapshot publish | API-* / scheduled |  | DB/Redis boundary |  | recheck at create/download | timeout/retry/dead-letter/queue-full | ready / partial / blocked |

Large export/report generation should be create task -> poll status -> download, with isolated workers and bounded queues.

## 13. Observability, Health, And Operations

| Signal ID | Signal | Source | Target/threshold | Owner | Evidence/handoff | Status |
| --- | --- | --- | --- | --- | --- | --- |
| OBS-001 | latency P95/P99, error rate, cache hit, pool usage, queue length, slow query/report, stale fallback, source freshness | logs/metrics/traces |  |  | dashboard/log/query | ready / partial / blocked |

| Log ID | Log point | Required fields | Level | Sampling/threshold | Redaction/privacy | Status |
| --- | --- | --- | --- | --- | --- | --- |
| LOG-001 | request ingress/egress | timestamp, service, environment, releaseVersion, requestId, traceId, method, route, status, latencyMs, user/tenant/role hash when safe | info | all requests or sampled by route | no tokens, secrets, raw PII, or full payloads | ready / partial / blocked |
| LOG-002 | validation/auth/permission | requestId, route, validation error code, auth result, permission decision code, no-permission reason code | info/warn | all rejections | no raw token or raw permission scope | ready / partial / blocked |
| LOG-003 | query plan and execution | requestId, reportId, widgetId, queryId, dataVersion/snapshotDate/loadBatch, source/upstream, query template/hash, durationMs, rows, page, cache status | info/warn/error | warn above slow-query/report threshold | no raw SQL with sensitive literals | ready / partial / blocked |
| LOG-004 | cache/pool/export/job/error | requestId, cache key hash, hit/miss/stale, pool acquire wait, active/idle counts when safe, export task id/status, errorCode, sanitized error summary | info/warn/error | warn on saturation/retry/stale/error | no sensitive file path or raw export payload | ready / partial / blocked |

Required operations:

- request id / trace id;
- redacted logs;
- log level/env config such as `LOG_LEVEL`, `LOG_FORMAT`, `REQUEST_ID_HEADER`, `TRACE_ENABLED`, `SLOW_QUERY_MS`, `SLOW_REPORT_MS`, `LOG_SAMPLE_RATE`, and redaction toggles;
- health/readiness endpoints;
- source freshness and data quality signals;
- pool/cache/queue metrics;
- slow-report governance;
- alert owner and runbook boundary;
- deployment/rollback evidence.

## 13A. Code File Change Ledgers

Use this section only when backend implementation or repair changes code.

| Ledger ID | Code file | Ledger path | Pre-change read evidence | Appended version | Changed ranges / anchors | Affected contracts | Verification | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CODELOG-001 |  | `__change_logs__/<file>.changes.md` | yes / no |  | route/service/repository/query/logging anchors | API/env/source/permission/logging |  | ready / partial / blocked |

Rules:

- Every changed backend code file needs a same-directory sidecar ledger.
- The ledger must be read before editing and appended after editing.
- Version entries must include feature list, code ranges/stable anchors, modified content, affected contracts, verification, and rollback notes.
- Chat summaries, commit messages, and delivery indexes do not replace file-level ledgers.

## 14. Environment, Deployment, And Source Mode

| Env ID | Environment | Source mode | Config/secrets | Base URL | Health path | Rollback | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ENV-001 | local / test / production | SQLite fixture / authoritative DB / upstream API / mixed | .env.test/.env.production/external secrets |  |  |  | ready / partial / blocked |

Production-bound handoff should separate test and production profiles and prove which source mode is active.

## 15. Gap, Risk, And Readiness

| GAP ID | Category | Missing decision/fact | Impact | Owner question | Blocks | Status |
| --- | --- | --- | --- | --- | --- | --- |
| GAP-001 | source / metric / permission / runtime / cache / export / env / observability / deployment |  |  |  | API-*/SVC-*/ENV-* | open / assumed / blocked / resolved |

| Risk ID | Category | Description | Impact | Probability | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RISK-001 | performance / security / source / permission / export / deployment / schedule |  | High / Medium / Low | High / Medium / Low |  |  | open / mitigated / accepted / blocked |

End with handoff verdict:

- overall data-service readiness: `ready`, `partial`, or `blocked`;
- API documentation handoff;
- backend implementation handoff;
- frontend integration handoff;
- testing integration handoff;
- operations/release handoff;
- exact blocker and next owner action.

---
name: api-documentation-design
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于生成或重构可交付的API/接口文档。用户提到接口文档、API文档、接口说明、OpenAPI/Swagger、前后端接口约定、prototype PRD 执行包、docs/prototype-data-summary.md、Mock API To HTTP API Replacement Matrix、Metric To Interface/Source Mapping、请求响应示例、鉴权/错误码/分页/筛选、快照接口、snapshotDate/dataVersion/loadBatch、字段口径、响应字段兼容、新增字段命名、默认后端技术栈、Python/Flask/连接池/Redis、已有路由补文档、接口交付验收时触发；只写文档契约，不实现后端代码或前端接入。"
---

# API Documentation Design

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Overview

Use this skill independently when the task is to turn known or inferred API intent into precise API documentation. The input can be an API inventory, backend routes, product requirements, frontend integration needs, source/data models, OpenAPI fragments, tests, or prior docs.

Do not implement backend code merely because this skill is triggered. Produce documentation that is ready for implementation, frontend integration, testing, or delivery.

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Targeted Reading Consumption

For PRD/prototype-derived report APIs, read `prd/execution/prd-targeted-reading-analysis.md` before documenting endpoint details. The API document must include consumed `SRC-*` / `READ-*` rows, source-authority notes, non-authority materials, and open `ENTRY-*` / `GAP-*` rows that affect request/response examples, field semantics, auth/permission, cache, export, detail/drilldown, and conclusion-rule payloads. Do not call an API document handoff-ready when targeted reading is missing, generic, or disconnected from endpoint decisions.

For completed-prototype handoff, also load `backend-development-workflow/references/00-prototype-downstream-handoff-contract.md` and include prototype baseline/version, fixed child-backend status, upstream stable IDs, mock replacement row, consumer data key, table-content evidence, request-param predicate mapping, source/code/test trace, and verification in endpoint documentation.

## Core Workflow

1. Collect inputs and select the documentation mode.
   Use inventory-to-document, route-to-document, requirement-to-contract, contract-refresh, async-job, webhook/callback, streaming, or file-transfer mode based on the available artifacts.

   Use `$quality-gate-validation` when input authorities conflict or the document will drive frontend, backend, tests, or release acceptance. Check endpoint boundaries, backend reuse pattern, request/response models, auth, pagination/sorting/filter rules, SQL/index feasibility, Redis/cache decisions, pools, performance limits, and unresolved `ENTRY-*` findings before marking an endpoint ready. If Redis is named, use `$redis-cache-design-patterns` to document role, key template, TTL/invalidation, permission-safety dimensions, miss/stampede behavior, fallback, pool/timeouts, and observability.
   For prototype-derived report APIs, collect `prd/execution/*`, `docs/prototype-data-summary.md`, the `Mock API To HTTP API Replacement Matrix`, and `Metric To Interface / Source Mapping` before endpoint details. These artifacts define component data keys, mock endpoint replacement, filter/action/export/detail/conclusion payload obligations, and metric/source traceability. Missing or stale files keep the document `partial` or `blocked`.

2. Establish shared conventions.
   Define base URL, version, auth, headers, common request model groups, response envelope, errors, pagination, sorting, filters, date/time format, enum format, numeric display/precision contract, file behavior, default/max page size, global filter execution, component-internal local filter scope, Redis/cache expectations, connection-pool expectations, large-result handling, and export limits before documenting endpoint details. Redis/cache expectations must be specific enough for implementation, not a placeholder.

   For interface implementation handoff, document the minimal implementation convention before endpoint details: table content must be understood first; every client-visible filter is a request param mapped to a source predicate; simple table retrieval endpoints query source-aligned rows only through projection, predicates, stable ordering, and pagination; hidden joins, aggregation, exact counts, totals, rankings, formulas, chart/KPI derivation, and broad in-memory reshaping require an explicit derived/summary/precompute exception or `GAP-*`.

   When the backend follows Python/Flask SSO conventions, document the SSO headers and failure semantics in common conventions before endpoint details: `Access-Token`, optional `Application-Key` when IAMA/clientId is active, token validation owner, public-route allowlist, 401 token-invalid behavior, 403 permission-denied behavior, logout/re-login expectations, and token/log redaction rules.

   For filter-bearing endpoints, document data completeness before binding: option source, source/provider execution stage, required response fields, row grain, default request/response example, at least one non-default request/response example, empty/no-permission example when relevant, and resolver/API branch behavior. If only one default snapshot exists for an affecting filter, keep the endpoint `partial` or `blocked`.

   When the API document will drive default backend implementation, state the default backend stack as `Python + Flask + database/upstream connection pools + Redis`, including which layer owns routing, pool configuration, Redis cache/precompute, timeout/fallback, and observability. Use another stack only with a user/existing-project override reason.

   Define response-field compatibility conventions before endpoint details. Existing response field names, nesting, types, units, precision, enum meanings, nullability, formulas, grain, numeric display semantics, and empty/no-permission behavior are stable across source/table/upstream replacement. New fields are additive by default and must follow the project naming convention; if no convention exists, use stable English lowerCamel field codes. Breaking changes require versioning, deprecation/migration notes, and downstream impact.
   For prototype-to-real API replacement, document the original mock endpoint/local dataset, replacement API, source model, component data key, consuming slot/component, request mapping, response mapping, compatibility status, and `GAP-*` for each unmapped item. Do not derive endpoint response shapes from visual labels alone when the prototype data summary provides data keys and sample structures.

   For metric-bearing response fields, apply `$metric-number-display-contract` before examples: value type, raw unit, display unit, display scale, screen precision, tooltip precision, export precision, rounding mode, null display, true-zero display, denominator-zero behavior, negative-zero handling, small-nonzero behavior when relevant, formula precision policy, and formatter owner. Percent/rate fields must state whether the payload is raw `0-1`, numeric percent `0-100`, or display string; formatted-only values are not sufficient when consumers need sorting, filtering, thresholds, exports, or localization.

   For snapshot/latest-period reports, document the snapshot role and shared data-version context before endpoint details: `snapshotDate`, `latestPeriod`, `loadBatch`, `dataVersion`, report version, or source version. Related data-bearing endpoints must consume that context through request params, backend-defaulted params, backend-injected scope, or an explicitly declared canonical/shared snapshot dataset before querying or deriving results, and include it in source/provider predicates, precompute lookups, and cache keys. A snapshot/dashboard aggregate endpoint may be reused by metrics, trends, rankings, tables, drilldowns, or exports only when the document states the matching grain, filters, permission scope, fields, cache key, and invalidation behavior.

3. Document endpoint behavior.
   For each endpoint, capture purpose, trigger, method/path, auth, request params/body, response schema, examples, errors, pagination/performance limits, source mode, compatibility notes, and status.
   Include whether the endpoint powers metrics, filter options, page/component datasets, export, detail/drilldown, toolbar action, or conclusion-rule inputs, and cite the prototype replacement row when applicable.

4. Trace dependencies.
   Link response fields to models, routes, repositories, source systems, upstream APIs, formulas, or explicit pending items. Avoid silently inventing fields or business rules.

5. Expose unresolved items.
   Mark partial or blocked endpoint behavior when source fields, formulas, auth values, permissions, samples, or performance decisions are missing.

6. Prepare handoff.
   Include enough examples and edge states for frontend contract validation, backend implementation, integration tests, runtime QA, and delivery review.

7. Mark production readiness when the API document is production-bound.
   Apply `$quality-gate-validation` before calling the API document production-ready. API documentation is only `partial` when authoritative source, auth/permission, environment/base URL, health/runtime evidence, observability, performance/export limits, version compatibility, or testing handoff is missing.

## References

- Read `$artifact-readability-standard` for human-readable and AI-extractable API document structure.
- Read `$quality-gate-validation` for authority conflicts, endpoint-contract readiness, design reasonableness, production readiness, and release acceptance.
- Read [references/01-inputs-and-traceability.md](references/01-inputs-and-traceability.md) when identifying source artifacts, authority, dependency trace, or unresolved model/API items.
- Read `$metric-number-display-contract` for metric unit, scale, precision, percent/rate, rounding, tooltip/export precision, and formatter ownership.
- Read `$environment-profile-contract` when base URLs, test/production profiles, auth endpoints, source mode, proxy/CORS, or release handoff matter.
- Read `$sql-query-optimization` for database-backed endpoint SQL feasibility and query-shape risks.
- Read `$backend-development-workflow` `references/minimal-interface-implementation-principles.md` when the API document will drive backend implementation or table-backed mock-to-real replacement.
- Read `$redis-cache-design-patterns` when Redis/cache behavior is part of the API contract.
- Read `$delivery-artifact-template-management` when creating the API document skeleton, common conventions, overview tables, and appendix.
- Read [references/03-endpoint-detail-rules.md](references/03-endpoint-detail-rules.md) when writing endpoint-level request, response, example, auth, error, performance, and compatibility sections.
- Read [references/04-handoff-quality-gate.md](references/04-handoff-quality-gate.md) before final delivery or when preparing frontend/backend/testing handoff.
- Read [references/05-output-and-quality-gates.md](references/05-output-and-quality-gates.md) before finalizing required outputs and quality checks.

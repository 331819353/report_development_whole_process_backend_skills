# API Documentation Output And Quality Gates

## Required Outputs

- API documentation grouped by module, domain, page, resource, or service boundary.
- Common conventions plus endpoint details.
- Backend reuse pattern and common request/response model family for production-bound endpoints.
- Response compatibility rules for source/table replacement: unchanged fields, additive fields, naming convention, deprecation/versioning, and compatibility notes.
- Numeric display/precision contract for metric-bearing fields: value type, raw/display unit, scale, screen/tooltip/export precision, rounding, null/zero/denominator-zero, negative-zero, formula precision, and formatter owner.
- Parameter-driven data-version, scope-filtering, snapshot role/reuse, and endpoint-dependency contract when snapshot/latest-period semantics exist.
- Backend stack/cache/pool notes when the document feeds backend implementation.
- SSO/auth header contract when protected APIs are documented: `Access-Token`, optional `Application-Key`, 401 vs 403, and frontend recovery expectation.
- Dependency trace from endpoint response to the relevant implementation/model/source/contract artifacts.
- Design reasonableness status with `DESIGN-*` findings when endpoint design affects downstream usability.
- Production closed-loop readiness when the API document is production-bound.
- Unresolved item list with endpoint impact and owner/confirmation question.


## Quality Checklist

- Every expected endpoint appears in the API document or is explicitly removed with a reason.
- Entry conflicts across requirements, API inventories, data/source models, frontend contracts, route code, OpenAPI snippets, and runtime samples are resolved or listed as `ENTRY-*`; unresolved `P0`/`P1` findings keep affected endpoints `partial` or `blocked`.
- API design reasonableness is checked; unresolved `P0`/`P1` `DESIGN-*` findings keep affected endpoints `partial` or `blocked`.
- Production-bound endpoints identify backend reuse pattern, reusable request model, reusable response envelope, and service-layer mapping, or explain why a custom shape is required.
- Request params cover required filters, drilldowns, pagination, sorting, exports, defaults, and invalid-param behavior.
- Filter-bearing endpoints include data-completeness evidence before frontend binding: option data, row grain, fields, default/non-default examples, empty/no-permission examples when relevant, and resolver/API branch behavior.
- Database-backed request params document SQL predicate shape, index support, and SQL pushdown scope for global/page-level filters; unresolved index or non-sargable filter behavior keeps the endpoint `partial` or `blocked`.
- API docs state where global filters, component-internal filters, sorting, pagination, ranking, Top/Bottom, and aggregation execute. Page/API-level full-materialize-then-filter behavior keeps the endpoint `partial` or `blocked` unless it is a documented component-internal filter over already fetched component data, tiny static enum, or bounded lookup.
- Snapshot/latest-period API docs state shared data-version fields, classify the snapshot role, and prove that metrics/trends/rankings/tables/drilldowns/exports either validly reuse the declared snapshot or avoid undocumented dependency on frontend call order/controller memory.
- Data-bearing endpoint docs show how data-version, business filters, and backend-injected permission/data scope become source-side predicates, upstream provider params, precompute lookup keys, declared snapshot reuse rules, or Redis/cache key segments. Response-only metadata does not satisfy this check.
- Default-backend API documents include Python/Flask, connection-pool, and Redis/cache ownership, or a named override reason.
- Redis-backed endpoint docs include Redis role, key dimensions, TTL/invalidation, permission safety, miss/stampede behavior, fallback, pool/timeouts, and observability.
- Collection/list/table endpoints document default page size, maximum page size, stable sort, total-count behavior, cursor/keyset need when applicable, and large-result handling. Missing pagination/performance behavior keeps production-bound endpoints `partial` or `blocked`.
- API implementation documents may use JSON only as response examples. If local/mock data is needed for backend/API development, the documented simulation source is SQLite with schema, seed rows, and indexes rather than JSON files.
- Each data-bearing endpoint identifies the served component/component group and frontend compute policy; broad page-level responses that require frontend business calculation stay `partial` or `blocked`.
- Each data-bearing endpoint identifies the data-vs-presentation boundary; backend-composed display copy, conclusion paragraphs, HTML/Markdown, combined value+unit strings, or style-implied labels require a documented server-owned text exception.
- Response schemas include field names, types, nullability, units, precision, enums, nesting, empty states, and examples.
- Response schemas for metric-bearing fields include numeric display contracts and do not rely on formatted-only strings when numeric behavior is needed.
- Response schemas preserve existing field contracts across source/table/upstream replacement. Any rename, removal, type/unit/precision/enum/nullability/formula/grain drift, or empty/no-permission behavior change is documented as a breaking change with version/deprecation/migration notes before `ready`.
- Newly added response fields are additive, conventionally named, source-traced, typed, permission/sensitivity-aware, and documented as stable/experimental/deprecated/pending before handoff.
- Auth, permission, no-data, invalid-param, unauthorized, no-permission, and upstream/backend failure behavior are documented when relevant.
- Protected Python/Flask SSO APIs document backend token validation and do not rely on frontend-only login state.
- Production-bound API documents include source authority, runtime/environment notes, auth/permission behavior, Redis/cache and connection-pool behavior when relevant, observability/performance constraints, version compatibility, and testing handoff before `ready`.
- Pending items remain visible and do not masquerade as confirmed API behavior.

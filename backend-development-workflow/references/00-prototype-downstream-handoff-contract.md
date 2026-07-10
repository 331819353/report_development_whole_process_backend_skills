# Prototype Downstream Handoff Contract

Use this contract whenever backend or data-service work starts from the completed report prototype workflow. The backend consumes data, API, filter, interaction, permission, and conclusion-input contracts; it does not translate visible UI fields directly into endpoints.

## Applicability Guard

Apply this contract only when `backendEntryMode = prototype-derived`. If no prototype handoff exists and the user wants real backend development, use `01-standalone-new-project-contract.md`; missing prototype files are not gaps or blockers for that mode.

## Required Upstream Baseline

Record one `prototypeBaselineRecord` before endpoint design or code edits:

| Field | Required evidence |
| --- | --- |
| Prototype version | Repository/path, branch or commit, `DELIVERY_INDEX.md` entry, and delivery timestamp when available. |
| PRD validation | Result of `report-prd-document-generation/scripts/validate_prd_bundle.py <bundle-root> --strict`, or `GAP-PRD-VALIDATION-*`. |
| Stage PRD | Current `prd/children/prd-child-backend.md`; missing/stale means `partial` or `blocked`, not permission to infer from the UI. |
| Data handoff | Current `docs/prototype-data-summary.md`, Metric To Interface And Source Mapping, Mock API To HTTP API Replacement Matrix, and backend method candidates. |
| Technical baseline | Current technical solution, API inventory, data model/source map, permission and environment contracts when available. |

The backend must read the fixed PRD core, especially targeted reading, metric mounting, data/API, interaction, conclusion, workflow execution, and child-backend files. `prd-child-prototype.md` and configured component maps are context for consumers and response shape, not source-table authority.

## Consumption Matrix

Create `prototypeContractConsumptionMatrix` before endpoint design. Each row includes upstream file/ID, source authority, backend target, request/response fields, source object, implementation action, verification, status, and `ENTRY-*` / `GAP-*`.

Required coverage:

| Upstream contract | Backend obligation |
| --- | --- |
| `SRC-*`, `READ-*`, `ENTRY-*`, `GAP-*` | Preserve source authority, conflicts, non-authority evidence, and start blockers. |
| `MET-*`, `OBJ-*`, `DATA-DESIGN-*` | Confirm grain, keys, source fields, units/precision, freshness, quality/null rules, and permission scope. |
| `API-*` and mock replacement rows | Map each mock endpoint/data key to target HTTP API, request DTO, response DTO, source/model/repository method, error/permission/cache behavior, and verification. |
| `FILTER-*`, pills, toolbar actions | Expose client-visible filters as request parameters mapped to source predicates; preserve reset/default/stale semantics without hidden business logic. |
| `INT-*` | Support declared payload fields, context inheritance, detail/export scope, permission, and error behavior. |
| `RULE-*` | Supply only required metric/evidence fields and freshness/permission states unless the contract explicitly assigns conclusion computation to backend. |
| `PAGE-*`, `BLK-*`, `SLOT-*`, component maps | Use only to identify consumers, data keys, response needs, pagination/sort, and endpoint ownership; do not encode layout in APIs. |

## Minimal Interface Boundary

The existing minimal-interface principles remain mandatory:

- Inspect every involved table/view/fixture/upstream object before work: representative rows, grain, keys, filter fields, permission fields, result bounds, nulls, and gaps.
- Client-visible filters are request parameters and source predicates.
- Simple table retrieval is projection + predicates + stable order + bounded pagination.
- Do not add hidden joins, aggregation, totals, exact counts, rankings, formulas, broad in-memory filtering, or response reshaping.
- Use field aliases/serialization only for explicit response compatibility. Route derived/aggregate requirements to an explicit technical design, model/view/precompute, or `GAP-*`.

## Backend-Owned Work

- API inventory/docs, source/model mapping, DTO/schema, route/service/repository implementation, permission injection, pools/timeouts/logging/health/env, tests, and runtime verification.
- `mockToRealBackendMatrix` for every affected mock endpoint/data key/filter/interaction/conclusion/export/detail path.
- `prototypeConfigurationTraceMatrix` from upstream API/data/filter/interaction/rule IDs to API docs, code paths, source objects, and verification.
- `tableContentUnderstandingMatrix` and `requestParamPredicateMatrix` for every involved source object.
- Response compatibility and numeric precision contracts consumed by frontend and testing.

## Start And Ready Gates

- Run the strict PRD validator when available and record its result.
- Do not start when the child-backend PRD, targeted reading, data/API contract, data summary, replacement rows, source authority, or table-content evidence is missing for the affected scope.
- Validate contracts against source samples, OpenAPI/docs, runtime responses, frontend consumers, and test expectations.
- Preserve stable upstream IDs in API inventory, docs, code/test references, and handoff artifacts.
- Parent PRD/prototype changes make affected backend rows stale until re-consumed.

## Required Handoff Evidence

- `prototypeBaselineRecord`
- `prototypeContractConsumptionMatrix`
- `prototypeConfigurationTraceMatrix`
- `mockToRealBackendMatrix`
- `tableContentUnderstandingMatrix`
- `requestParamPredicateMatrix`
- API/source/code/test/runtime evidence
- Open `ENTRY-*` / `GAP-*` and owner
- Final `ready`, `partial`, or `blocked` decision

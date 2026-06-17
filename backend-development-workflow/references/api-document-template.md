# Backend API Document Template

Use this structure when a backend workflow must output interface documentation.

## 1. Overview

- Service name:
- Purpose:
- Runtime:
- Base URL:
- Auth mode:
- Mode: data-service-design / API documentation / implementation / repair
- Upstream technical solution: ARC-* / ADR-* / API-* / LGM-* / NFR-* / GAP-*

## 1a. Data-Service Design Summary

- Service boundary:
- Consumers:
- Backend stack decision:
- Layered architecture:
- Query-service chain:
- Data-vs-presentation boundary:
- Runtime model:
- Security/permission model:
- Observability and deployment:
- Readiness:

## 2. Input Files

| File | Format | Role | Key Fields | Parsing Notes |
| --- | --- | --- | --- | --- |

## 3. Data Sources

| Source | Type | Used By APIs | Key/Join Fields | Freshness | Fallback |
| --- | --- | --- | --- | --- | --- |

## 4. Data Models

### Raw Model: `{SourceModelName}`

| Field | Type | Required | Description | Example |
| --- | --- | --- | --- | --- |

Relationships:

- 

Example:

```json
{}
```

### Response Model: `{ResponseModelName}`

| Field | Type | Required | Description | Example |
| --- | --- | --- | --- | --- |

Example:

```json
{}
```

## 5. Source-To-Response Transformations

Use this section whenever source data and mock/frontend/API display shape differ.

| Source Field | Source Example | Response Field | Response Example | Rule |
| --- | --- | --- | --- | --- |
| `biz_date` | `20260529` | `period` | `202605` | Convert `YYYYMMDD` to `YYYYMM`; aggregate daily rows by month when endpoint grain is monthly. |

Document:

- Date/period normalization:
- Aggregation grain:
- Field rename/mapping:
- Enum code-to-label mapping:
- Unit conversion and precision:
- Derived formulas:
- Default/fill behavior:
- Sort/group rules:
- Filter/sort/page execution stage:

## 6. Contract Verification

### Mock/Frontend Contract Alignment

| Frontend/Mock Field | API Field | Type Match | Unit/Precision | Empty-State Shape | Notes |
| --- | --- | --- | --- | --- | --- |

### Mandatory Mock-To-SQLite-To-Authoritative-Source Gate

Use this section when backend work starts from frontend/prototype mock data.

- Mock contract validation: pass / partial / fail
- SQLite fixture database path:
- SQLite schema/DDL path:
- SQLite seed data path or migration:
- SQLite indexes and constraints:
- JSON response example path(s), if any:
- JSON purpose: API example / assertion snapshot only
- Authoritative source type: production database / upstream API / event-derived read model / existing service / explicitly SQLite-backed
- Authoritative source locator: table/view/query/API/path/topic/client
- Runtime source implementation:
- Default runtime data source:
- SQLite-only mode allowed only for:
- Mock vs SQLite comparison:
- SQLite vs authoritative source comparison:
- Authoritative source replacement status: complete / partial / blocked
- Authoritative source replacement blockers:

### Transformation Test Samples

| Case | Input Source Rows | Request Params | Expected Response | Checks |
| --- | --- | --- | --- | --- |
| Date normalization | `{"biz_date":"20260529","amount":100}` | `period=202605` | `{"period":"202605","amount":100}` | `YYYYMMDD -> YYYYMM`; amount reconciles. |

### Reconciliation Checks

- Totals/counts:
- Derived KPI formulas:
- Filtered result consistency:
- Empty-state behavior:

### Performance Limits

- Default page size:
- Maximum page size:
- Stable default sort:
- Total-count behavior:
- Cursor/keyset pagination need:
- Maximum export rows:
- Cache/precompute strategy:
- Redis/cache strategy:
- Cache key dimensions:
- Cache TTL and invalidation:
- Database connection pool:
- Pool min/max/acquire timeout/idle timeout:
- Pool release/close guarantee for `ApiError`, timeout, cancellation, early return, and generic exception paths:
- StarRocks pool max config such as `STARROCKS_POOL_MAX` and repeated-failure exhaustion test:
- Refresh cadence:
- Timeout behavior:
- Large-file/database fallback:
- SQL pushdown scope: filters / sorting / pagination / joins / aggregation / counts / Top-Bottom
- Global filter SQL `WHERE` rules:
- Component-internal local filter scope:
- Full-materialize-then-filter check: pass / partial / blocked
- Index-backed filters and sorts:
- Non-sargable predicates avoided or unresolved:
- Required indexes/generated columns/full-text/precompute:

## 7. API Inventory

| Method | Path | API family | Served component | Purpose | Auth | Request Model | Response Model | Service mapping | Runtime policy | Filter/sort/page execution stage | Frontend compute policy | Data-vs-presentation policy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## 8. API Contracts

### `{METHOD} {PATH}`

Purpose:

Served component or component group:

API family:

Auth:

Data source:

Service-layer mapping:

Transformation:

Filter/sort/page execution stage:

Frontend compute policy:

Data-vs-presentation policy:

Contract verification:

Request:

| Location | Field | Type | Required | Source field / SQL predicate / index support | Description |
| --- | --- | --- | --- | --- | --- |

Response:

| Field | Type | Description |
| --- | --- | --- |

Success example:

```json
{}
```

Error examples:

```json
{
  "error": {
    "code": "BAD_REQUEST",
    "message": "Invalid request"
  }
}
```

## 9. Error Codes

| Code | HTTP Status | Meaning | Recovery |
| --- | --- | --- | --- |

## 10. Startup And Smoke Test

- Install:
- Run:
- Health check:
- Example curl:
- Data-source mode checked:
- Authoritative-source endpoint checked:

## 11. Production Closed-Loop Readiness

- Runtime backend URL or deployment target:
- Health/readiness evidence:
- API document version aligned with implementation:
- Auth/permission behavior verified:
- Source mode and authoritative source evidence:
- Config/environment notes:
- Observability notes: logs, request ID, metrics/traces, alert owner:
- Performance/export limits:
- Rollback or restore path:
- Testing handoff: test account/data, smoke cases, contract cases, known blockers:
- Readiness: ready / partial / blocked:

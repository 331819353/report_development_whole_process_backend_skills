# Minimal Interface Implementation Principles

Use this reference whenever backend work includes API implementation, mock-to-real replacement, database-backed route work, or endpoint repair.

The default implementation mode is source-aligned, parameter-driven, and query-only. Broader report-query, OLAP, aggregation, cache, or adapter guidance is an exception path, not the starting point.

## Core Rule

Implement the smallest truthful API that exposes the requested table-backed data:

1. Client-visible filters are request parameters.
2. Table retrieval only queries rows. Do not add extra business processing, joins, aggregation, rollups, totals, rankings, formulas, or in-memory reshaping during retrieval.
3. Understand every involved table's data content before designing or editing the interface.

Permission scope, tenant scope, auth context, and safety guardrails are still backend-owned, but they must be documented as injected scope rather than hidden client filters.

## Table Content Understanding Gate

Before endpoint design or code edits, produce a table-content understanding note for every table/view/fixture/upstream object that may be queried.

Minimum evidence:

| Area | Required evidence |
| --- | --- |
| Source object | physical name, database/source, owner if known, layer/type, and environment/source mode |
| Business meaning | what one row represents and which page/API need it may satisfy |
| Grain and keys | primary key, natural key, partition/date field, tenant/org/permission fields, and row uniqueness expectation |
| Columns | field list or inspected schema, data type, nullable status when available, enum-like fields, measure-like fields, and large/sensitive columns |
| Sample content | representative rows for default state and at least one non-default filter state when relevant |
| Filter support | which request filters can map directly to source fields, operators, allowed/default values, and whether option data exists |
| Result bounds | expected row volume, partition/range constraints, page-size limit, stable ordering field, and export boundary |
| Gaps | unresolved source, key, grain, filter, permission, sample, or freshness facts as `GAP-*` |

Do not proceed from "table name exists" to implementation. If row grain, keys, filter fields, or representative samples are unknown, keep the endpoint `partial` or `blocked`.

## Request Parameter Rule

Every filter that changes business data must be visible in the API request contract:

- Put client-selected filters in path, query, or body params with name, type, required/default behavior, allowed values, and invalid-param response.
- Map each filter param to a source field and predicate shape before implementation.
- Keep pagination, sorting, keyword, and date/version values as explicit params when they affect the returned rows.
- Keep backend-injected tenant, user, role, org/data-permission, masking, and field-visibility scope separate from client params, but document how they constrain the query.
- Do not hardcode UI defaults, previous endpoint state, controller memory, or local application variables as hidden filters.
- Do not claim filter readiness when only the selected UI state changes but the backend request and source predicate do not change.

## Query-Only Retrieval Rule

For minimal interface implementation, repository/source access is a bounded row query:

```text
request params
-> validation/defaults
-> backend-injected auth/permission scope
-> single source/table query with projection + predicates + stable order + pagination
-> serializer aliases to stable API field names
-> response rows + metadata
```

Allowed by default:

- explicit column projection;
- `WHERE` predicates from request params and backend-injected scope;
- source-compatible sorting;
- bounded pagination or cursor;
- safe SQL aliases that preserve existing API field names;
- light serialization such as type conversion required by the API framework, null preservation, masking required by permission, and response envelope metadata.

Blocked by default unless a named exception is approved:

- `GROUP BY`, `HAVING`, window functions, totals, subtotals, rankings, Top/Bottom computation, exact total counts, metric formulas, ratio calculation, or period rollups;
- joining multiple business tables to synthesize a new result shape;
- application-memory filtering, grouping, sorting, pagination, deduplication, aggregation, or formula calculation after loading broad rows;
- deriving chart series, KPI cards, summary conclusions, or business paragraphs from detail rows inside the interface implementation;
- changing response field names to match source column names;
- treating another endpoint response, controller memory, JSON array, or previous frontend call as the data source.

If the consuming UI needs aggregate/derived data, first check whether a source table already stores that grain. If yes, query that source-aligned table directly with params. If no, record a `GAP-*` or route to data-model/precompute/design work instead of hiding aggregation inside the simple interface.

## Multi-Table Exception Rule

The default interface should query one authoritative table/view/fixture/upstream object. Multi-table access is an exception and needs explicit evidence:

- each involved table has passed the table-content understanding gate;
- join keys and cardinality are known;
- the join is required to return requested source fields, not to create hidden business metrics;
- permission and tenant scope are safe on every table;
- duplication risk and row-grain after join are documented;
- the route remains query-only and does not aggregate unless routed through a separate approved design path.

If these are not proven, split endpoints, query an existing source-aligned serving table, or mark the work blocked.

## Readiness Blockers

Do not mark an interface implementation, API document, or handoff `ready` when any of these are true:

- table content was not inspected for every source object;
- filters are not request params or cannot map to source predicates;
- implementation loads broad rows then filters/sorts/pages in memory;
- SQL contains unjustified `GROUP BY`, `HAVING`, aggregate functions, window functions, or exact count queries for a simple table retrieval endpoint;
- service/controller code computes totals, rates, rankings, trend series, or summary cards from retrieved rows;
- a multi-table join lacks content evidence, join cardinality, or permission-scope proof;
- response fields come from unknown source columns or undocumented formulas;
- pagination/result bounds are missing.

## Required Handoff Evidence

Every implementation/handoff should include:

- table-content understanding matrix for every source object;
- request-parameter-to-source-field mapping;
- query-only proof: projection, predicates, ordering, pagination, and absence of hidden aggregation/processing;
- backend-injected permission/scope proof;
- representative default and non-default request examples when filters exist;
- open `GAP-*` rows for any missing source/content/filter/permission facts.

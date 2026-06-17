# SQL Query Writing Optimization

Use this shared reference when designing, documenting, implementing, or validating database-backed data-service APIs.

Scope: SQL writing and query-shape optimization only. Index creation, table design, database parameters, partitioning, and cache configuration may be related decisions, but they are not the main scope of this reference.

Core principle: read fewer rows, read fewer columns, do less sorting/grouping, and avoid large intermediate result sets.

## Required Query Decisions

For every production-bound or high-volume database-backed endpoint, record these decisions or mark them as gaps.

| Area | Required Decision |
| --- | --- |
| Projection | Returned columns, excluded large columns, and whether `SELECT *` is avoided. |
| Predicate shape | Direct column predicates, date/range rewrite, type-consistent parameters, and whether predicates are sargable. |
| Join shape | Join keys, tenant/permission keys, one-to-many cardinality, aggregation-before-join need, and Cartesian-product prevention. |
| Dedup/order | Whether `DISTINCT`, `ORDER BY`, `UNION`, or random sort is really required. |
| Pagination | Default/max page size, stable sort, total-count strategy, and cursor/keyset need for deep pages. |
| Aggregation/window | Filter-before-aggregation/window rule, `WHERE` vs `HAVING`, group-by column count, and Top N strategy. |
| Dynamic SQL | Optional-filter generation strategy, parameter binding, and avoidance of universal nullable-OR predicates. |
| Verification | `EXPLAIN` / `EXPLAIN ANALYZE` evidence, scanned rows, access method, join order, sort/temp usage, and row-estimate accuracy. |

## Projection Rules

- Do not use `SELECT *` for API queries.
- Select only fields needed by the response model, sorting, filtering, grouping, or permission checks.
- Avoid loading large text, JSON, blob, or remark columns unless the endpoint explicitly returns them.
- For list/table APIs, separate summary/list queries from detail queries when large columns are needed only after drilldown.

## Predicate Rules

- Prefer direct predicates: `col = ?`, `col IN (...)`, `col >= ? AND col < ?`, and anchored prefix search when supported.
- Keep column types and parameter types consistent. Avoid implicit casts caused by sending strings for numeric/date columns.
- Do not wrap indexed columns in functions for normal filters, such as `DATE(created_at) = ?`, `YEAR(biz_date) = ?`, `LOWER(name) = ?`, or `TO_CHAR(period) = ?`, unless a matching function/generated/full-text index or precompute path is confirmed.
- Rewrite date, month, and period filters to ranges, such as `created_at >= ? AND created_at < ?`.
- Avoid arithmetic on filtered columns, such as `amount * rate > ?`; move the calculation to the parameter side or a precomputed/generated column when possible.
- Avoid leading-wildcard search such as `LIKE '%keyword'` or `LIKE '%keyword%'` on large tables unless full-text/search-index support is documented.
- Do not use universal optional-filter templates such as `(:param IS NULL OR col = :param)` for high-volume queries. Generate only the predicates needed for the request, with safe parameter binding.

## Join Rules

- Join after filtering whenever semantics and the execution plan allow it.
- Always document complete join conditions, including tenant, organization, partition, effective-date, and composite-key fields when applicable.
- Prevent Cartesian products. Any join without a complete `ON` condition is a blocker.
- Check one-to-many joins before aggregating. If only counts/sums are needed, aggregate the many side first and then join.
- Do not use `JOIN + DISTINCT` just to check existence. Use `EXISTS` when the response does not need columns from the joined table.
- Prefer `NOT EXISTS` over `NOT IN` when null values may appear in the subquery.
- Do not put right-table filter conditions in `WHERE` when a `LEFT JOIN` must preserve unmatched left rows; place those filters in the `ON` clause or document the intended inner-join behavior.
- Avoid functions or casts on join fields unless the matching indexed/generated form is confirmed.

## Sort, Dedup, And Set Rules

- Do not add `DISTINCT` to hide join duplication. Fix the join grain or aggregate first.
- Do not add `ORDER BY` when the caller does not need deterministic order.
- Use stable ordering for pageable results; include a tie-breaker such as primary key when sort fields can duplicate.
- Prefer `UNION ALL` over `UNION` when deduplication is not required.
- Avoid `ORDER BY RAND()` / `RANDOM()` on large tables; use a preselected sample key, materialized sample, or bounded sampling strategy.
- Split broad `OR` conditions into separate `UNION ALL` branches only when it improves predicate selectivity and duplicate handling is clear.

## Pagination And Result Bound Rules

- Every list/table endpoint needs bounded page size and maximum page size.
- Use cursor/keyset pagination for deep paging, frequently updated datasets, or high-volume scroll.
- Do not return export-sized result sets through synchronous list APIs.
- When the UI needs only first N / Top N, push the limit into SQL instead of returning all rows.
- Document total-count strategy: exact, approximate, cached, skipped, or async.

## Aggregation And Window Rules

- Filter rows in `WHERE` before aggregation; use `HAVING` only for aggregate conditions.
- Group by the minimal set of columns needed by the response grain.
- Filter before window functions when the filter is semantically independent from the window result.
- For Top N, use `ORDER BY ... LIMIT/TOP/FETCH FIRST` with a supported sort path rather than sorting a large unbounded set and trimming later.
- Avoid repeated scalar subqueries per row. Aggregate once and join the result when many rows share the same lookup.

## CTE, Subquery, And Complex SQL Rules

- Use CTEs for clarity, but do not assume a CTE is faster. Some databases materialize CTEs or prevent predicate pushdown.
- Remove useless nested subqueries that do not reduce rows, columns, or complexity.
- For overly complex queries, consider a two-step pattern: first select bounded IDs, then query details by those IDs.
- If a query becomes hard to reason about, capture the row grain at each step and check whether each step reduces rows or columns.

## Verification Rules

Use the database's plan tool, such as `EXPLAIN` or `EXPLAIN ANALYZE`, for important or risky queries. Check:

- Scanned rows vs returned rows.
- Access method: index seek/range scan vs full scan.
- Join order and join type.
- Extra sort, temp table, hash aggregation, or materialization.
- Filter ratio and whether filters are applied early.
- Estimated rows vs actual rows where runtime analysis is available.
- Whether pagination, Top N, and aggregation are pushed down before large intermediate results are formed.

## Red Flags

Mark the endpoint/query `partial` or `blocked` when any red flag affects production-bound behavior and no accepted mitigation is documented.

- `SELECT *` in a list/table/chart API.
- Global filters applied after loading broad rows into application memory.
- Functions, casts, or arithmetic on high-cardinality filtered/joined columns.
- Leading-wildcard search on large tables without search-index support.
- Missing or incomplete `JOIN ON` conditions.
- One-to-many join multiplication hidden with `DISTINCT`.
- `NOT IN` over nullable values.
- Unbounded synchronous list/export response.
- Deep offset pagination on large or changing datasets.
- Repeated scalar subqueries across many rows.
- Required ordering/deduplication performed on a large unbounded intermediate result.
- No `EXPLAIN` / slow-query evidence for a risky P0 endpoint.

## Handoff Checklist

- Query purpose and response grain are clear.
- Projection lists only necessary fields.
- Filters are source-side, sargable, type-consistent, and permission-aware.
- Joins have complete keys and understood cardinality.
- Aggregation, ranking, pagination, and Top N execute before response construction.
- Expensive optional filters are generated only when requested.
- Total-count, export, and deep-page behavior are explicitly bounded.
- Plan evidence or slow-query risk is recorded for P0/high-volume endpoints.

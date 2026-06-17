# OLAP Data Modeling Optimization

Use this shared reference when a report, BI, dashboard, data service, metric system, detail traceability flow, trend analysis, or user/operation analysis needs a 数据模型文件, data-source mapping, metric contract, or model optimization review.

Scope: OLAP model design and query-facing model organization. This reference focuses on business process modeling, grain, facts, dimensions, metric definitions, layers, summaries, wide tables, history, quality, traceability, and maintainability. It does not focus on database parameters, storage engine tuning, machine resources, or index implementation details.

Core principle: organize data by business process, unified grain, conformed dimensions, and governed metric definitions so analysis queries scan less data, join less at runtime, avoid repeated calculation, and keep one trusted口径.

## Modeling Flow

Do not start from table fields. Model in this order:

1. Business questions and users.
2. Subject areas/domains.
3. Business processes.
4. Analysis grain.
5. Fact models.
6. Dimension models.
7. Metric system.
8. Data layers.
9. Summary tables, wide tables, and application models.
10. Quality, lineage, and traceability checks.
11. Query-pattern-based optimization.

## Business Question And Subject Area Rules

- Start with who consumes the model, which decisions they make, which metrics they need, which dimensions they slice by, and how often the result is queried.
- Create an analysis matrix before model tables: analysis object, common metrics, common dimensions, filters, and traceability needs.
- Divide subject areas by business boundary, such as user, product, order, transaction, payment, refund, marketing, traffic, inventory, supply chain, finance, customer service, task, or risk.
- A subject area owns metric口径, source ownership, permission scope, refresh cadence, and quality rules for that domain.
- Do not turn the model into a field warehouse. A model that cannot name its business process and consuming question is `partial` or `blocked`.

## Grain Rules

- Define grain before fields. Every fact, summary, wide, and response/view model must answer: one row represents what?
- Record unique key, natural key, business time field, partition/date field, and whether measures are additive, semi-additive, or non-additive.
- Keep one model at one grain. Do not mix order grain, order-item grain, payment-flow grain, user-day grain, and product-day grain in one table/model.
- Do not join models of different grains and aggregate measures without first aligning grain. This is a common cause of duplicated amount, duplicated order count, and join multiplication.
- If a frequently used metric requires repeated `COUNT DISTINCT`, consider whether a summary model at the needed grain should be created.

## Fact Model Rules

Design fact models around business processes, not source-system table names.

Fact model types:

| Type | When To Use | Required Notes |
| --- | --- | --- |
| Transaction fact | One business event or action, such as order, payment, refund, click, login, approval, or task completion. | Event time, business key, dimension keys, measures, status, source trace. |
| Periodic snapshot fact | State captured at fixed intervals, such as inventory, balance, asset, account, membership, or store status. | Snapshot time, semi-additive behavior, period aggregation rule. |
| Accumulating snapshot fact | Process with lifecycle milestones, such as order fulfillment, complaint handling, task SLA, or approval flow. | Start/end/milestone times, duration metrics, current status. |
| Factless fact | Event or relationship without natural measures, such as sign-in, enrollment, tag assignment, coupon received, or activity participation. | Relationship keys, event time, count semantics. |

Fact fields should include:

- Business keys and degenerate dimensions when useful for traceability, such as order ID, payment ID, invoice number, ticket number, or tracking number.
- Dimension foreign keys, not every descriptive dimension field.
- Business time fields and ingestion/ETL time fields for late-arriving data and replay.
- Core measures and statuses.
- Source system and audit fields.

Keep low-level DWD facts narrow and traceable. Avoid stuffing every dimension name, long text, address, phone number, remark, JSON blob, or display label into base facts.

## Dimension Model Rules

- Build conformed dimensions for commonly shared analysis perspectives, such as date, region, city, organization, channel, customer, user, product, SKU, project, task, and status.
- Avoid multiple competing definitions for the same dimension, such as several city/channel/category tables with different hierarchy or historical behavior.
- Prefer star-schema usability for OLAP: dimension tables may denormalize stable hierarchy fields, such as category level 1/2/3 or province/city/district, when this reduces repeated joins and BI complexity.
- Do not blindly flatten every field. Very wide, frequently changing, low-use, sensitive, or long-text dimension attributes should stay bounded or be kept in detail/application-specific layers.
- Decide historical behavior explicitly:
  - Type 1 / overwrite when only current value matters.
  - Type 2 / historical version when analysis needs the state at event time.
  - Type 3 / limited previous values when only a small amount of change history is needed.
- For "state at event time", either store key historical attributes on the fact or join to a slowly changing dimension by effective time.
- Use bridge tables for many-to-many relationships, such as user-tags, order-coupons, product-activities, content-topics, or employee-departments. Do not store comma-separated IDs as the analytic model.
- For many-to-many measures, document allocation or aggregation rules to prevent duplicated amounts after joins.

## Metric System Rules

Separate metric types:

- Atomic metrics: base measures such as pay amount, order count, refund amount, user count, click count, exposure count.
- Derived metrics: atomic metric plus condition, period, segment, or scope, such as 7-day pay amount or app-channel pay amount.
- Composite metrics: metrics calculated from other metrics, such as conversion rate, refund rate, customer unit price, retention rate.

Every metric must define:

- Business meaning.
- Formula.
- Grain.
- Supported dimensions.
- Time口径 and business time field.
- Filter/scope conditions.
- Deduplication rule.
- Source dependency.
- Refresh frequency.
- Owner.
- Additivity: additive, semi-additive, or non-additive.
- Reconciliation rule.

Additivity rules:

- Additive metrics, such as amount/count/quantity, can be summed across normal dimensions when grain is aligned.
- Semi-additive metrics, such as inventory, balance, or assets, may aggregate by product/store/account but should not be blindly summed across time. Use end-of-period, average, min, max, or another documented rule.
- Non-additive metrics, such as conversion rate, refund rate, customer unit price, or retention rate, must not be summed. Store numerator and denominator so totals can be recomputed after aggregation.
- Do not give different metrics the same vague name, such as "sales amount", when one means order amount, pay amount, shipped amount, net amount, tax-included amount, or freight-excluded amount.

## Time And Period Rules

- Build or reference a date/time dimension when reports use calendar, fiscal, holiday, workday, week, month, quarter, promotion, school term, or season logic.
- Every fact and metric must name its business time field, such as order creation time, pay success time, completion time, refund success time, event time, or snapshot date.
- Do not mix time口径 silently. Refund amount by refund date and net pay amount by original order/pay date are different valid metrics and need different names or explicit notes.
- Keep business time, ingestion time, ETL time, and partition date distinguishable.
- Late-arriving and backfill strategy must be documented for important facts and summaries: replay window, overwrite behavior, affected layers, and reconciliation rule.

## Layering Rules

Recommended layers:

| Layer | Role | Notes |
| --- | --- | --- |
| ODS | Original/source-aligned data | Keep raw fields for traceability and replay; not for direct business analysis. |
| DWD | Cleaned detail facts | Model by business process; standardize types, statuses, time fields, deduplication, and core口径. |
| DIM | Conformed dimensions | Unified codes, hierarchy, names, SCD/history behavior, reuse across domains. |
| DWS | Shared summary layer | Pre-aggregate common subject/object/period grains and governed metrics for reuse. |
| ADS | Application/report layer | Serve concrete dashboards, APIs, exports, and high-frequency scenarios; may denormalize for query performance. |

Layering should match complexity. Small scopes may use `ODS -> DWD/DIM -> ADS`; complex multi-team metric systems usually need `ODS -> DWD -> DIM -> DWS -> ADS`.

Do not query ODS directly from production reports unless the source is explicitly accepted as the analytic source. Do not put every business rule only in ADS. Common metrics should be governed in DWS and consumed by ADS.

## Summary And Wide Table Rules

- Build DWS summaries for high-frequency, fixed口径, repeated aggregations. Do not repeatedly scan large DWD facts for the same dashboard metric.
- Choose summary grain from query patterns, not guesswork: user-day, product-day, shop-day, channel-day, city-day, category-day, city-category-day, project-month, task-owner-day, etc.
- Avoid dimension-combination explosion. A summary table with too many dimensions can become sparse, huge, and hard to reuse.
- Store numerator and denominator for ratio metrics in summaries; do not store only the final rate.
- Precompute multi-period metrics when they are common and expensive, such as 1d/7d/30d, MTD, QTD, YTD, or rolling periods.
- Use ADS/wide tables for fixed, high-frequency, page-oriented, export-oriented, profile-oriented, or API-serving scenarios.
- Keep wide tables bounded by subject/application. Do not build an all-in-one table mixing unrelated users, orders, products, payments, refunds, logistics, service, marketing, traffic, inventory, and finance.
- Manage wide-table fields in blocks, such as base attributes, lifecycle, activity, transaction, preference, risk, and display fields.
- DWD should stay clean and less redundant; DWS may moderately denormalize frequent dimensions; ADS may denormalize for query speed and page/API convenience.

## Update, Deduplication, And History Rules

- Classify table/model update mode: full, incremental, zipper/SCD, snapshot, or event/flow.
- Preserve both business time and load/ETL time where late-arriving data, replay, or backfill matters.
- DWD should deduplicate known duplicate sources before upper-layer reporting. Do not push repeated `COUNT DISTINCT` patches into every report if the detail model is dirty.
- Deduplication must name the key and tie-breaker, such as event ID, order item ID, payment ID, request ID, or composite natural key.
- Important summary and ADS models must support rerun/backfill for recent N days or another explicit window when late data is expected.

## Naming And Null Rules

- Use consistent table/model naming by layer and purpose, such as `ods_{source}_{object}`, `dwd_fact_{business_process}_{grain}`, `dim_{dimension}`, `dws_{subject}_{object}_{period}`, and `ads_{application}_{period}`.
- Name fields with business meaning, not vague words: prefer `pay_amount`, `refund_amount`, `pay_user_count`, `order_create_time`, `pay_success_time`, `is_new_user`.
- Amount fields should name the money semantics: original, discount, coupon, freight, pay, refund, net, tax-included, or tax-excluded.
- Boolean fields should follow one convention, such as `is_new_user`, `is_member`, `is_deleted`, or `is_valid`.
- Null and default values must be intentional. Unknown dimension keys, such as unknown channel/city/category, should use a consistent unknown value. Do not mix `NULL`, `0`, `-1`, and `unknown` without a documented rule.
- Distinguish unknown from truly zero. In summaries, amount/count nulls often become 0; in details, null may preserve important source meaning.

## Quality And Traceability Rules

Every model should include quality rules that match its risk:

- Primary/natural key uniqueness.
- Core fields not null.
- Valid enum/status values.
- Amount/range checks, such as refund amount not exceeding pay amount beyond accepted tolerance.
- Dimension referential hit rate, such as SKU/city/channel matching conformed dimensions.
- Freshness SLA.
- Core metric fluctuation monitoring.
- Reconciliation from ADS -> DWS -> DWD -> ODS.

Traceability must support drilling from application metric to shared summary, detail fact, and original source where the source exists. If a dashboard metric cannot trace to detail or accepted source logic, mark it `partial` or `blocked`.

## Common Anti-Patterns

Mark model design `partial` or `blocked` when these appear without an accepted reason:

- One super-wide table attempts to serve every domain.
- Tables/models are created before business question, subject area, process, and grain are defined.
- A fact table mixes multiple grains.
- Reports query raw ODS/source tables directly for governed metrics.
- Each ADS/report recalculates the same core metric independently.
- Ratio metrics are summed or averaged without numerator/denominator.
- Snapshot or semi-additive metrics are summed across time without a rule.
- Many-to-many IDs are stored as comma-separated strings.
- Historical reports depend only on current dimension values when historical state matters.
- Summary models combine too many dimensions and explode row count.
- Wide tables contain unmanaged field blocks, sensitive long text, or rarely used changing attributes.
- Quality rules, freshness, owner, and lineage are missing.

## Handoff Checklist

- Business questions, subject areas, business processes, and consumers are named.
- Every fact/logical/response model has grain, keys, time口径, owner, refresh, and status.
- Facts are process-based and preserve traceability.
- Dimensions are conformed, hierarchy-aware, and history-aware.
- Metrics have formulas, additivity, numerator/denominator where needed, source dependency, owner, and reconciliation.
- Layering decision is explicit: ODS, DWD, DIM, DWS, ADS, or accepted simplification.
- Summary/wide/application models are justified by query pattern or serving need.
- Many-to-many, late-arriving data, deduplication, null/default, and SCD/history rules are documented.
- Quality rules and lineage make ADS -> DWS -> DWD -> ODS traceable.

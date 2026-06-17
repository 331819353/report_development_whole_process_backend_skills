# Pending List Template

Use this exact table for 待补充数据模型清单.

| ID | Category | Severity | Affected model/API/page | Missing or ambiguous item | Impact | Current assumption or fallback | Owner | Confirmation question | Status | Resolution note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

## ID Rules

- Use `GAP-001`, `GAP-002`, and so on.
- Keep existing gap IDs stable when updating.
- Do not reuse obsolete or resolved IDs for new issues.

## Row Writing Rules

Each row must answer:

1. What is missing or ambiguous?
2. Where does it affect the solution?
3. What breaks if it is wrong?
4. Can work continue under an assumption?
5. Who should answer?
6. What exact question should be asked?

Required cells must not be blank. Use `none` when intentionally not applicable. Use `TBD` only when the same row includes impact, owner, and a concrete confirmation question.

## Good Row Pattern

| ID | Category | Severity | Affected model/API/page | Missing or ambiguous item | Impact | Current assumption or fallback | Owner | Confirmation question | Status | Resolution note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GAP-001 | metric-formula | High | MET-001 / API-001 / 经营总览 | 毛利率口径缺少分母是否含税说明 | Risks wrong metric result and API文档 | Assumed grossMarginRate = grossProfit / revenueBeforeTax until confirmed | business | 毛利率分母使用含税收入还是不含税收入？ | assumed | none |

## Bad Row Patterns

Avoid:

- "指标待确认" with no affected API/model.
- "权限待确认" with no data scope.
- "数据源缺失" with no owner question.
- "需求不清" with no affected page/module/API.
- "交互待确认" with no trigger, parameter, or expected result.
- "性能待确认" with no affected API, volume, latency, cache, or export limit.
- Multiple unrelated missing items in one row.
- Assumptions that are not reusable in downstream docs.

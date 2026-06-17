# Impact Matrix Template

| Change ID | Changed object | Old value/behavior | New value/behavior | Source of truth | Affected artifact | Affected object | Impact type | Severity | Required action | Owner workflow | Regression cases | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CHG-001 | 指标口径 |  |  |  | API清单 / 数据模型 / 页面 / 测试矩阵 |  | breaking / data-change / doc-only | high / medium / low |  |  |  | open / partial / ready / blocked |  |

## Impact Type Values

- `breaking`: contract or behavior changes in a way that existing consumers may fail.
- `behavior-change`: user-visible behavior changes without contract failure.
- `data-change`: displayed values, grain, filters, permissions, or historical calculation change.
- `visual-change`: layout, chart, label, screenshot baseline, or visibility change.
- `test-only`: test data, expected result, or automation selector change.
- `doc-only`: documentation wording or version index update.

## Owner Workflow Values

Use the smallest owning workflow:

- `$report-requirement-structure-extraction`
- `$technical-solution-workflow`
- `$metric-governance-lineage`
- `$api-inventory-design`
- `$api-documentation-design`
- `$data-model-source-mapping`
- `$backend-development-workflow`
- `$frontend-development-workflow`
- `$permission-matrix-validation`
- `$testing-integration-workflow`
- `$delivery-version-management`

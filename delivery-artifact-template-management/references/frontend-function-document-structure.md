# Function Description Structure

Use this structure for 前端功能说明. Omit sections only when they truly do not apply.

```markdown
# 前端功能说明

## 一页摘要

- 本次交付范围:
- 面向用户/测试对象:
- 关键功能:
- 数据来源/接口模式:
- 当前 readiness: ready / partial / blocked
- 主要限制或阻塞:

## Document Metadata

- Project:
- Version/commit:
- Date:
- Author/source:
- Runtime environment:
- Provider contract version/source:

## Frontend Scope

- Pages/routes/modules:
- Included interactions:
- Out of scope:

## Feature Inventory

先用 1-2 句话说明本次页面/模块的整体使用路径，再给出明细表。

| Module | User purpose | Main components | Data provider | Key interactions | States | Verification |
|---|---|---|---|---|---|---|

## Page Or Module Details

### <Page Or Module Name>

- Purpose:
- Main components:
- Data/provider mapping:
- Control semantics and schema impact:
- Provider evidence:
- Filters and defaults:
- Non-default perspective behavior:
- Interactions:
- States:
- Export/download/refresh:
- Permissions:
- Known limitations:

## Data And Filter Linkage Summary

- Control semantics summary:
- Perspective switches and schema impact:
- Navigation metric lineage:
- Filter defaults/options/provider params:
- Non-default perspective verification:
- Cross-perspective consistency verification:

## Verification Summary

- Commands:
- URL/container:
- Browser/runtime evidence:
- Network/provider evidence:
- Screenshots/logs when available:

## Production Handoff

- Backend/API base URL:
- Provider/source mode:
- Auth/env behavior:
- Retained mock/offline/demo source:
- Runtime QA evidence:
- Testing handoff:
- Defect retest notes:
- Readiness: ready / partial / blocked / not needed
- Blockers:

## Testing Notes
```

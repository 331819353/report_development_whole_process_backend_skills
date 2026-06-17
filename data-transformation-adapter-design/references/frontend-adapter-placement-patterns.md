# Adapter Placement Patterns

Choose the narrowest existing boundary that keeps visual components stable.

## Preferred Locations

- Request/service module: best for REST, BFF, or backend API calls.
- GraphQL hook/composable: map query result data before returning it to UI code.
- Store selector/getter: useful when shared state feeds many components.
- Data-source resolver: useful for dashboard/report systems with registry-driven widgets.
- SDK wrapper: normalize third-party or internal SDK return shapes in one place.
- File/parser module: normalize JSON, CSV, XLSX, or generated static data near the loader.
- Stream/event adapter: map WebSocket/SSE events into append/update/remove UI operations.

## Avoid

- Repeating field mapping in several components.
- Letting chart/table/card components know provider-specific field names.
- Mixing semantic conversion with purely visual formatting.
- Hiding missing fields behind constants without documenting the assumption.

## Component Boundary

Keep formatting that is purely visual in the component. Keep semantic conversion, enum mapping, unit conversion, pagination normalization, and stale-data policy in the adapter or data layer.

Keep business computation out of the frontend unless it is explicitly bounded and documented. APIs/providers should return component-ready totals, rates, ranks, grouped rows, chart series, table rows, and pagination metadata. Adapters should not aggregate broad result sets, compute business formulas, apply business filters, or split one page-level payload into several unrelated component models. If unavoidable, document the exception, input size bound, owner, and backend/API gap.

Adapters also must not normalize a full-materialize-then-filter provider path for global/page scope. If the current request fetches all candidate rows and then applies global filters, permission scope, pagination, ranks, groups, or aggregates locally, move those inputs into the provider/API/resolver call or record a blocking provider gap. Component-internal filters may use local filtering only on the already fetched component dataset, and only when they are display/interactivity controls rather than API-level scope.

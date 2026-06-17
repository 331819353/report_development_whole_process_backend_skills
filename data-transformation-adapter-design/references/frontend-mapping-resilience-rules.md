# Mapping And Resilience Rules

## Mapping Rules

- Map provider field names to UI view model names explicitly.
- Normalize units, precision, date/period formats, enum/status labels, and boolean flags.
- Preserve source identifiers needed for drilldown, row actions, exports, or reverse lookup.
- Normalize pagination into a single local shape: items, page, pageSize, total, hasMore when applicable.
- Normalize collection order only when the UI expects sorted data or the provider does not guarantee order.

## Resilience Rules

- Handle null, missing optional fields, empty arrays, malformed rows, unknown enum values, and partial responses.
- Keep fallback values visibly safe: empty string, `null`, `0`, `[]`, or `Unknown` only when the UI can distinguish them correctly.
- Do not hide required missing fields. Return a blocked/missing-information note when a component cannot be correct without them.
- Avoid broad `any` in TypeScript where mapping correctness matters.
- Remove stale mock imports only after the adapter fully replaces the mock path.

## Runtime Lifecycle Rules

- Protect against stale responses after rapid filter, route, tab, or pagination changes by using cancellation, request sequence IDs, or stale-result checks.
- Debounce high-frequency inputs such as keyword search when the provider should not be called on every keystroke.
- Keep cache keys explicit: include filters, route params, permission scope, pagination, sorting, and user/session dimensions when they affect the result.
- Define cache invalidation for refresh, export, mutation, logout, permission changes, and provider errors.
- For realtime feeds, map connect/update/remove/error events and cleanup subscriptions on component unmount, route change, filter change, and logout.
- Do not keep previous data silently during refresh unless the UI marks it as stale or refreshing.

## Verification Samples

Check at least representative success, empty, partial, malformed, stale-response, cache-hit/cache-miss, and auth/error cases when evidence is available.

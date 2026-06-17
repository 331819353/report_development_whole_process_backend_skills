# Comparison Checklist

## UI Contract

- Consuming pages/components and the source files they import.
- View model fields, nested paths, arrays, chart series, table columns, KPI props, and interaction payloads.
- Filter defaults, route params, pagination, sorting, search, date ranges, export params, and drilldown params.
- Loading, empty, error, partial, stale, no-permission, token-invalid, and retry state inputs.
- Lifecycle expectations for rapid filter changes, request cancellation, stale-response guards, cache reuse, cache invalidation, and realtime unsubscribe.

## Provider Contract

- Provider path or call name, method/query/mutation/subscription, input params, auth/client initialization.
- Response envelope, data path, pagination metadata, total fields, status code, error envelope, and message fields.
- Field names, types, units, precision, enum/status dictionaries, date/period format, nullability, and sort order.
- Empty result shape, partial data behavior, timeout/failure behavior, retry/idempotency rule, freshness/cache rule, and permission/auth behavior.
- Provider concurrency behavior: whether old requests can be cancelled, ignored, deduplicated, or subscribed/unsubscribed safely.

## Decision Rules

- Pass: all required UI fields and behaviors are provided directly or through a documented adapter.
- Partial: provider is usable but needs adapter work, optional fields, lifecycle guards, cache rules, or unresolved edge-state behavior.
- Blocked: required fields, params, auth, provider availability, or authoritative samples are missing.

Do not silently invent fields, enum meanings, formulas, or source-side filters. Mark them as missing information.

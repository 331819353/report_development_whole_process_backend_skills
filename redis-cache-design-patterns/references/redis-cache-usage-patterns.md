# Redis Cache Usage Patterns

Use this reference when a technical solution, API inventory, API document, backend implementation, or performance review names Redis for cache, precompute, hot query acceleration, rate limiting, locks, idempotency, or job progress.

Redis is a shared infrastructure component, not a generic place to put any data. A Redis design is incomplete until key dimensions, TTL/invalidation, permission safety, miss behavior, and observability are clear.

## When Redis Is Appropriate

Use Redis when one or more of these are true:

- The same metadata, dictionary, permission summary, report definition, or filter options are read frequently and change slowly.
- A dashboard/widget/query result is expensive but can tolerate a defined freshness window or stale last-success fallback.
- A canonical snapshot or precomputed result needs fast lookup by data-version, tenant, permission scope, and filters.
- Export/report jobs need lightweight status/progress, idempotency keys, deduplication, or short-lived task state.
- The service needs rate limits, concurrency semaphores, request coalescing, or distributed locks.

Do not use Redis as the primary durable store for regulated business facts, long-retention audit logs, or data that must survive Redis eviction/restart unless the project explicitly provisions Redis persistence and accepts the operational risk.

## Key Design

Use stable, readable, versioned key names:

```text
{env}:{app}:{domain}:{entity}:{version}:{scope_hash}:{param_hash}
```

Include every value that changes the result:

- environment and app/report code;
- tenant, user, role, permission/data-scope hash when data differs;
- report version, source version, `snapshotDate`, `latestPeriod`, `loadBatch`, or `dataVersion`;
- filter params, route/drilldown params, pagination/sort, locale/unit/format, field visibility, and feature flags;
- schema/result version so old values do not break after response-shape changes.

Prefer a hashed suffix for long parameter sets, but keep a small human-readable prefix for operations and debugging. Store the canonical param summary in the value or logs when traceability matters.

## TTL And Invalidation

- Define TTL per data class. Metadata/dictionaries can usually live longer than personalized query results.
- Add TTL jitter to avoid synchronized expiry and cache avalanches.
- Use source-version, report publish/rollback, permission change, and manual refresh events for explicit invalidation when available.
- For high-value dashboards, consider warmup after publish, after source refresh, or before expected peak traffic.
- Return freshness metadata such as `fromCache`, `cacheAge`, `dataFreshnessTime`, `dataVersion`, and `stale` when users need to trust the number.
- Stale last-success fallback is acceptable only when the API contract states stale tolerance and the response marks stale status.

## Miss And Stampede Protection

- Expensive cache misses need protection: singleflight/request coalescing, short lock with timeout, stale-while-revalidate, warmup, or precompute.
- Use distributed locks only around the expensive rebuild path. Keep lock TTL short and always handle lock acquisition failure.
- Avoid dogpile behavior where many requests rebuild the same key after expiry.
- For absent data that is valid to cache, use a short negative-cache TTL to reduce repeated source hits.
- Do not cache errors broadly unless the degraded behavior, TTL, and user-visible status are explicit.

## Access Patterns

- Use `MGET`/pipeline for many independent keys in one request, but keep batch sizes bounded.
- Avoid `KEYS` in production paths. Use explicit key registries, tagged key sets, or bounded `SCAN` only for admin/maintenance.
- Use hashes for small grouped objects with related fields; strings for serialized result blobs; sorted sets for leaderboards/rankings when the ranking semantics are stable; streams only when the service owns consumer groups and retention.
- Compress only large values after measuring CPU tradeoff. Keep max value size and serialization format documented.
- Use Lua scripts for small atomic multi-key operations such as token bucket counters or conditional unlock, but keep scripts simple and versioned.
- Prefer cache-aside for query results unless the project has a controlled write-through/write-behind model.

## Security And Permission Safety

- Never share permission-sensitive or tenant-scoped values through a key that omits tenant/user/role/data-scope dimensions.
- Do not store secrets, access tokens, raw personal identifiers, or full sensitive payloads unless encryption, masking, retention, and access controls are explicitly approved.
- Audit or log only redacted key prefixes and request IDs when keys include sensitive dimensions.
- Use separate namespaces or logical databases for environments only when operations can enforce separation reliably; key prefixes are still required.

## Rate Limit, Lock, And Job State

- Rate-limit keys must include the correct subject: user, tenant, IP, route, report, or API client.
- Token bucket or leaky bucket implementations need window size, burst size, TTL, and overload response.
- Idempotency keys need request hash, owner, terminal state, TTL, and replay behavior.
- Job progress keys are short-lived state, not the durable job record. Persist durable job ownership, audit, result file, and terminal status in the authoritative store when required.

## Pooling And Timeouts

- Redis clients need bounded connection pools, connect/read/write timeouts, retry/backoff limits, and safe shutdown.
- Do not let Redis calls wait indefinitely inside request threads.
- Decide degraded behavior when Redis is slow or unavailable: bypass cache, stale fallback, partial response, rate-limit failure, or hard error.
- Health checks should include lightweight Redis readiness when Redis is required for correctness, and should not run expensive scans.

## Observability

Track:

- hit/miss ratio by cache family;
- Redis latency and error rate;
- rebuild count, lock wait time, lock failure, stale fallback count;
- key cardinality, memory usage, eviction count, expired count;
- pool usage, acquire timeout, blocked clients;
- top hot keys and large values when available.

Every Redis-backed API handoff should include the cache family, key template, TTL/invalidation, permission-safety dimensions, miss behavior, fallback, and metrics to watch.

## Anti-Patterns

- Redis key omits tenant, role, data-scope, source version, or filters that change the result.
- Using Redis as an undocumented cross-endpoint source of truth.
- Caching one user's permission-filtered result and serving it to another user.
- Broad `KEYS` or unbounded `SCAN` in request paths.
- Infinite TTL for mutable business data without source-version invalidation.
- Cache rebuild stampede after TTL expiry.
- Distributed locks without TTL or ownership token.
- Storing large unbounded result sets instead of paginating, summarizing, or precomputing.
- Treating Redis availability as guaranteed without timeout, fallback, and observability.

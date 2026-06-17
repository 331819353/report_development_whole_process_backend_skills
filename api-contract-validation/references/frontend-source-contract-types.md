# Source Contract Types

Use this reference to avoid binding the skill to 数据服务 by default. Choose the evidence type that matches the project.

## Provider Types

- REST/backend API: OpenAPI, API文档, route code, sample response, network trace.
- BFF or gateway: frontend-facing endpoint docs, aggregation rules, upstream dependency notes, error envelope.
- GraphQL: query/mutation document, variables, fragments, schema/introspection sample, pagination convention.
- SDK/client package: TypeScript declarations, usage examples, initialization options, returned promise/stream shape.
- Static JSON/file/source module: fixture file, generated data file, local import, CSV/XLSX/asset parser, build-time loader.
- Realtime feed: WebSocket, SSE, polling source, event schema, subscribe/unsubscribe rules, stale data behavior.
- Data-source registry: project-specific resolver, composable, store, or dashboard data-source config.

## Authority Order

Prefer runtime evidence when verifying implemented behavior, but prefer documented contracts when deciding whether implementation is allowed.

1. User-provided authoritative docs or schema.
2. Implemented provider code and typed clients.
3. Runtime network or SDK traces.
4. Existing mock/static data and consuming UI code.
5. Reasonable assumptions clearly marked as missing information.

## Data-Service Rule

When the provider is 数据服务, use API文档, API清单, backend health checks, and auth rules as provider evidence. Do not require 数据服务 evidence for static, SDK, GraphQL, or local-only frontend work.

## Production Evidence Rule

When the frontend contract note is used for production acceptance, record the actual provider/source mode, runtime locator, auth/env behavior, retained mock/offline/demo status, runtime evidence, and testing handoff. Static, SDK, GraphQL, realtime, and local-file providers can still be valid production providers only when that provider mode is explicit and accepted for the delivery scope.

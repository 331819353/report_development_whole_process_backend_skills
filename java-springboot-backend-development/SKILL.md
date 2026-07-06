---
name: java-springboot-backend-development
description: "[后端阶段] 本阶段版本仅服务后端/数据服务设计、API文档/契约、接口实现、运行验证和后端交付；不承接原型设计、前端代码或测试执行。用于按 Java 17+ + Spring Boot 3.x 沉淀后端项目架构、目录结构、RESTful API、统一响应、全局异常、Spring Security/JWT/SSO、DTO/VO、MyBatis/JPA、Redis、Profile、Maven/Docker 和工程命名约定。用户提到 Java后端、Spring Boot后端、SpringBoot项目目录结构、Spring MVC、ApiResponse、GlobalExceptionHandler、SecurityConfig、JwtAuthenticationFilter、海尔IAM/IAMA、Access-Token、Application-Key、clientId、401/403、application-dev/test/prod.yml、Mapper/Repository、Controller/Service分层、Swagger/Knife4j、本地启动或打包部署时触发。"
---

# Java Spring Boot Backend Development

## Stage Scope

Classification: 后端阶段.

Use this copy only inside the backend/data-service skill bundle. Treat frontend, prototype, and testing work as contracts, evidence, handoff notes, or blockers; do not edit those stages from this skill.

## Positioning

Use this skill as the architecture and engineering baseline for Java backend development when the target should follow Java 17+ and Spring Boot 3.x conventions.

It complements `$backend-development-workflow`: load this skill when the backend target is Java/Spring Boot, or when the user asks for Spring Boot project structure, REST API implementation, Spring Security/JWT/SSO, unified response, exception handling, environment profiles, Maven/Docker commands, or directory conventions. Use `$haier-sso-integration` for Haier IAM/IAMA tokenUrl, code exchange, token check, `Access-Token`, `Application-Key`, and clientId rules; use `$api-documentation-design` for formal API docs, `$api-contract-validation` for producer/consumer contract checks, `$performance-optimization` for SQL/Redis/pool tuning, and `$runtime-url-smoke-test` for live URL verification.

## Reference Map

| Need | Read |
| --- | --- |
| Stack, directory structure, layering, response/exception/auth/SSO, profiles, Maven/Docker, naming, commands, readiness blockers | `references/01-java-springboot-backend-standard.md` |
| Haier IAM/IAMA SSO endpoints and integration choices | `$haier-sso-integration` |

## Anti-Laziness Gate

For non-trivial work, apply `$quality-gate-validation` `references/anti-laziness-execution-gate.md` before final output, handoff, or readiness. Do not mark the result ready while `LAZY-*` findings remain open, when available local evidence was not inspected, when owning skills were skipped, or when proof is limited to generic statements such as "checked", "optimized", "looks good", or "implemented".

## Workflow

1. Confirm whether the task is a new Spring Boot project, an existing project repair, a migration into this architecture, API implementation, or a handoff/README update.
2. Inspect existing stack before imposing defaults. Prefer Java 17+, Spring Boot 3.x, Spring MVC, Maven/Gradle, MyBatis/MyBatis-Plus or Spring Data JPA, Redis, Spring Security + JWT/SSO, Jakarta Validation, springdoc-openapi/Knife4j, Lombok/MapStruct, SLF4J + Logback, JUnit 5/Mockito, and Docker when no project override exists.
3. Align directories and ownership: `common`, `config`, `controller`, `service`, `service/impl`, `mapper` or `repository`, `entity`, `dto`, `vo`, `converter`, `filter`, `interceptor`, `aspect`, `util`, `job`, and `resources/mapper`.
4. Keep controllers thin. Put request binding, validation, and route annotations in controllers; business orchestration and transactions in services; persistence in mappers/repositories; DTO/Entity/VO conversion in converters.
5. Define unified API behavior: `ApiResponse<T>`, HTTP status plus business code, `BizException`, `GlobalExceptionHandler`, validation exception handling, empty/error states, and no internal stack traces in frontend responses.
6. Define auth/security behavior when protected APIs are in scope: `Authorization: Bearer <token>` or `Access-Token`, `JwtAuthenticationFilter`/SSO filter, `SecurityConfig`, whitelist routes, stateless session policy, local user/role mapping, 401 token-invalid behavior, and 403 permission-denied behavior. When Haier IAM/IAMA is in scope, load `$haier-sso-integration` and keep `clientId`/`Application-Key` server-side.
7. Define environment/profile behavior: `application.yml`, `application-dev.yml`, `application-test.yml`, `application-prod.yml`, env-var based secrets, `SPRING_PROFILES_ACTIVE`, datasource/Redis settings, and production secret redaction.
8. Apply minimal interface implementation before controller/service/mapper edits: inspect table content, make client-visible filters request DTO/query params, map them to source predicates, and keep simple table retrieval query-only without hidden joins, aggregation, exact counts, formulas, totals, rankings, or broad in-memory processing.
9. If implementation is requested, edit code through `$code-change-ledger-management`, preserve project patterns, and add/update tests when behavior changes.
10. Run available Maven/Gradle build, tests, package, startup, and `$runtime-url-smoke-test` when a URL is produced.
11. Route API contract, data adapter, numeric display, Redis/cache, SQL performance, deployment readiness, and production observability to the owning skills when the task exceeds Spring Boot architecture baseline.

## Required Output

- Target mode: new project, existing repair, migration, API implementation, or handoff documentation.
- Stack and override decision.
- Directory/file plan with layer ownership.
- REST API and response/exception contract: `ApiResponse<T>`, `BizException`, validation handling, HTTP/business codes, and frontend-visible error behavior.
- Security/JWT/SSO plan when applicable: `SecurityConfig`, filter chain, token header, whitelist, IAM/IAMA token check or local JWT bridge, server-side `clientId`/`Application-Key`, 401/403 behavior, and redaction.
- Data access plan: MyBatis/MyBatis-Plus mapper XML or JPA repository, entity/DTO/VO/converter boundaries, transactions, pagination/export when applicable.
- Minimal interface proof: table-content evidence, request-param-to-source-field mapping, query-only mapper/repository boundary, and derived/summary exceptions or gaps.
- Profile/config plan: dev/test/prod YAML, datasource/Redis/env vars, Maven/Gradle commands, Docker/Docker Compose when applicable.
- Verification commands, runtime URL/smoke result when available, blockers, and readiness.

## Quality Gate

- Do not put business orchestration, SQL, permission checks, and response formatting all inside controllers.
- Do not return `Entity` directly to frontend or use request DTOs as database entities.
- Do not expose raw exceptions, stack traces, SQL errors, tokens, secrets, or personal data in API responses or logs.
- Do not mark protected APIs ready without backend token validation, whitelist rules, local user/permission mapping, and explicit 401/403 behavior.
- Do not make the browser provide authoritative `Application-Key`, `clientId`, client secret, or SSO credentials; Java backend must resolve those from server-side config or a trusted tenant/app registry.
- Do not hardcode production datasource, Redis, JWT secret, or credentials in committed YAML.
- Do not concatenate user-controlled values into SQL.
- Do not implement table-backed APIs before inspecting table content and mapping filters as request params/source predicates.
- Do not hide joins, aggregation, exact counts, formulas, totals, rankings, or broad in-memory processing inside Controller/Service/Mapper code for a simple source-query endpoint.
- Do not mark implementation ready without build/test/startup evidence or exact blockers.
- Do not ignore existing project conventions; use this baseline only when the project has no stronger local standard.

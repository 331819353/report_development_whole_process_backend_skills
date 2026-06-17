# Java Spring Boot Backend Standard

Source distilled from `/Users/susanmartinez/Downloads/Java-SpringBoot项目目录结构说明.md`.

## Stack Baseline

| Category | Standard |
| --- | --- |
| Language | Java 17+ |
| Framework | Spring Boot 3.x, Spring MVC |
| Build | Maven or Gradle |
| Data access | MyBatis, MyBatis-Plus, or Spring Data JPA |
| Database | MySQL or PostgreSQL by default; adapt to project source systems |
| Cache | Redis when cache/session/rate-limit/precompute is needed |
| Security | Spring Security + JWT or enterprise SSO/IAM bridge |
| Validation | Hibernate Validator / Jakarta Validation |
| API docs | springdoc-openapi or Knife4j |
| Utilities | Lombok, Hutool, MapStruct when allowed by project |
| Logs | SLF4J + Logback |
| Tests | JUnit 5, Mockito, Spring Boot Test |
| Deployment | Docker, Docker Compose, jar packaging |

Prefer existing project stack when authoritative. Use this standard as a default only when the project does not already define stronger conventions.

## Request And Response Contract

Map frontend request-wrapper concepts to Spring Boot server-side ownership:

| Frontend request concept | Spring Boot owner |
| --- | --- |
| Request interceptor | Filter, Interceptor, or Spring Security filter |
| Token injection | Parse `Authorization: Bearer <token>` or SSO `Access-Token` request header |
| Response interceptor | Unified `ApiResponse<T>` response envelope |
| Error toast/message | `@RestControllerAdvice` global exception handling |
| Status handling | HTTP status plus business code |
| Re-login | Return 401; frontend clears token and redirects |

Core files:

- `filter/JwtAuthenticationFilter.java` or `filter/SsoAuthenticationFilter.java`
- `config/SecurityConfig.java`
- `common/response/ApiResponse.java`
- `common/exception/GlobalExceptionHandler.java`
- `common/exception/BizException.java`

Response shape:

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

Common business codes:

| Code | Meaning |
| --- | --- |
| 200 | Success |
| 400 | Invalid parameter |
| 401 | Not logged in or token expired |
| 403 | Permission denied |
| 404 | Resource not found |
| 429 | Too many requests |
| 500 | System error |

## Auth, Security, And SSO

Protected APIs should define:

- Header: `Authorization: Bearer <token>` for local JWT, or `Access-Token: {token}` for IAM/IAMA SSO.
- Token parsing and validation owner, usually `JwtAuthenticationFilter`, `SsoAuthenticationFilter`, token utility, auth service, or IAM/IAMA gateway.
- `SecurityContextHolder` population after a valid token.
- Stateless session policy for JWT APIs.
- Whitelist routes such as `/auth/login`, `/doc.html`, `/swagger-ui/**`, and `/v3/api-docs/**`.
- 401 for token missing/invalid/expired; 403 for authenticated but unauthorized.
- Token, secret, credential, and personal data redaction in logs.

Do not leave token parsing as a placeholder in production-bound code.

When Haier IAM/IAMA SSO is in scope, use `$haier-sso-integration` for the authoritative endpoint and response details. The Java/Spring Boot baseline should still enforce these backend rules:

- Prefer official Java SDK integration when `iam-auth-sdk-starter` is approved; otherwise use a small IAMA HTTP gateway.
- Frontend-facing login/tokenUrl endpoint accepts the frontend code and returns canonical IAMA fields: `resultCode`, `resultMsg`, `access_token`, `expires_in`, `token_type`, `refresh_token`, and `account`.
- Browser business requests carry `Access-Token`; they do not provide authoritative `Application-Key`, `clientId`, or `clientSecret`.
- Java backend resolves `clientId` from `application-*.yml`, environment variables, secret manager, or a trusted tenant/app registry.
- Java backend calls token check with server-resolved `client_id` and `Application-Key`, plus the frontend-provided `Access-Token`.
- Valid token means upstream check returns `resultCode == "0"` and `data == true`.
- After token validity, map account to local user, role, org, data scope, and permission context before entering business services.
- 401 means missing/invalid/expired/unverifiable token; 403 means valid identity without business permission.
- Public routes, health checks, preflight, tokenUrl, Swagger/Knife4j, and static assets must be explicitly allowlisted.

## Global Exceptions

Use `BizException` for business failures and `@RestControllerAdvice` for global handling.

Recommended handlers:

- `BizException`
- `MethodArgumentNotValidException`
- `BindException`
- `ConstraintViolationException`
- generic `Exception` fallback with a frontend-safe message

Do not expose stack traces, raw SQL errors, internal class names, token payloads, or secrets to frontend responses.

## Directory Structure

Standard layout:

```text
src/main/java/com/company/project/
  ProjectApplication.java
  common/
    constant/
    enums/
    exception/
    response/
    result/
  config/
    CorsConfig.java
    RedisConfig.java
    SecurityConfig.java
    IamSsoConfig.java
    OpenApiConfig.java
  controller/
  service/
    impl/
  mapper/
  repository/
  entity/
  dto/
  vo/
  converter/
  filter/
    SsoAuthenticationFilter.java
  interceptor/
  aspect/
  util/
  job/
src/main/resources/
  application.yml
  application-dev.yml
  application-test.yml
  application-prod.yml
  mapper/
src/test/java/com/company/project/
pom.xml
Dockerfile
docker-compose.yml
```

Directory ownership:

| Directory | Responsibility |
| --- | --- |
| `common/` | shared response, exception, constants, enums, pagination/result objects |
| `config/` | Security, Redis, CORS, OpenAPI, and framework configuration |
| `controller/` | HTTP routes, request binding, validation, response return |
| `service/` | business interfaces and orchestration |
| `service/impl/` | implementation and transaction boundaries |
| `mapper/` | MyBatis/MyBatis-Plus data access |
| `repository/` | Spring Data JPA repositories when JPA is used |
| `entity/` | database table mapping objects |
| `dto/` | request objects; do not reuse as entities |
| `vo/` | frontend response view objects; do not expose entities directly |
| `converter/` | DTO/Entity/VO mapping, preferably MapStruct when available |
| `filter/` | JWT auth and trace filters |
| `interceptor/` | login/permission/request logging interceptors |
| `aspect/` | operation logs, permissions, idempotency |
| `util/` | JWT, date, string, crypto utilities |
| `job/` | scheduled jobs |

For IAM/IAMA SSO, keep account-center gateway/client code out of controllers. Use a dedicated auth service, gateway/client, filter, or interceptor, then attach only normalized local user context to downstream business services.

Layering:

```text
Controller -> Service -> Mapper/Repository -> Database
```

Rules:

- Controllers only receive requests, validate parameters, and return results.
- Services orchestrate business logic, domain rules, and transactions.
- Mapper/Repository owns persistence only.
- Entity is not returned to frontend directly.
- DTO is not used as database entity.

## RESTful API And Naming

REST examples:

| Operation | Method | URL |
| --- | --- | --- |
| list | GET | `/employees` |
| detail | GET | `/employees/{id}` |
| create | POST | `/employees` |
| update | PUT | `/employees/{id}` |
| delete | DELETE | `/employees/{id}` |
| batch delete | DELETE | `/employees/batch` |
| export | GET | `/employees/export` |
| import | POST | `/employees/import` |

Naming:

| Type | Example |
| --- | --- |
| Controller | `EmployeeController` |
| Service | `EmployeeService` |
| Service implementation | `EmployeeServiceImpl` |
| Mapper | `EmployeeMapper` |
| Repository | `EmployeeRepository` |
| Entity | `Employee` |
| DTO | `EmployeeSaveDTO`, `EmployeeQueryDTO` |
| VO | `EmployeeDetailVO`, `EmployeeListVO` |
| Converter | `EmployeeConverter` |
| Config | `SecurityConfig` |
| Exception | `BizException` |
| Util | `JwtUtil` |

Method names:

- `list` or `page` for lists/pages.
- `detail` or `getById` for detail.
- `create` or `save` for create.
- `update` for update.
- `delete` or `remove` for delete.
- `enable` / `disable` for state changes.
- `importData` / `exportData` for import/export.

## Validation And Transactions

Validation:

- POST/PUT body: `@Valid @RequestBody`.
- GET query: DTO is acceptable.
- Required values: `@NotNull`, `@NotBlank`.
- String length: `@Size`.
- Numeric range: `@Min`, `@Max`.
- Email: `@Email`.

Transactions:

- Put `@Transactional(rollbackFor = Exception.class)` on service implementation methods.
- Use transactions for multiple writes, multi-table writes, inventory/balance/state transitions, or any all-or-nothing business operation.
- Keep read-only query paths outside write transactions unless project conventions require otherwise.

## Profiles And Configuration

Use profiles:

- `application.yml` for shared config.
- `application-dev.yml` for local development.
- `application-test.yml` for test deployment.
- `application-prod.yml` for production.

Activation:

```bash
java -jar app.jar --spring.profiles.active=prod
export SPRING_PROFILES_ACTIVE=prod
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```

Production rules:

- Inject datasource, Redis, JWT secret, and credentials through environment variables or secret manager.
- Inject SSO/IAM/IAMA `clientId`, `clientSecret`, auth host, and enabled profile through environment variables or secret manager.
- Do not commit `application-local.yml`, `application-secret.yml`, `.env`, or raw production credentials.
- Keep dev/test/prod datasource and Redis database separation explicit.

## Build, Run, And Deploy

Common Maven commands:

```bash
mvn spring-boot:run
mvn spring-boot:run -Dspring-boot.run.profiles=dev
mvn clean compile
mvn test
mvn clean package
mvn clean package -DskipTests
java -jar target/app.jar --spring.profiles.active=prod
```

Docker baseline:

```dockerfile
FROM eclipse-temurin:17-jre
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Docker Compose should define app env vars and local dependencies such as MySQL and Redis. Use project-specific image names, ports, volumes, networks, and secret handling.

## Logging

Use SLF4J parameterized logs:

```java
log.info("开始处理业务，id={}", id);
log.error("处理业务异常，id={}", id, e);
```

Log levels:

| Level | Use |
| --- | --- |
| `debug` | local debugging and key variables |
| `info` | normal business flow |
| `warn` | recoverable or non-blocking issues |
| `error` | system exceptions and failures requiring investigation |

Never log raw tokens, passwords, secrets, raw personal data, or unredacted external payloads.

## README Handoff

Recommended README sections:

- Project name and project introduction.
- Stack.
- Environment requirements: JDK 17+, Maven 3.8+, MySQL 8+, Redis 6+.
- Local startup command.
- Package and deployment command.
- Directory structure.
- API document URL: `/swagger-ui/index.html` or `/doc.html`.
- FAQ and known blockers.

## Readiness Checklist

- Directory layering matches the selected Spring Boot convention.
- `ApiResponse<T>`, `BizException`, and global exception handling exist or are explicitly planned.
- Protected APIs define security filter chain, JWT or SSO validation, whitelist, local user/permission mapping, and 401/403 behavior.
- IAM/IAMA integrations keep `clientId`, `Application-Key`, and `clientSecret` server-side, and expose only approved frontend tokenUrl/browser request contracts.
- DTO/VO/entity boundaries are clear.
- Mapper/Repository choice is explicit; SQL/XML/repository ownership is clear.
- Transactions exist for multi-write or critical state transitions.
- Profiles separate dev/test/prod and production secrets are externalized.
- Build/test/package/startup commands are known and have been run when implementation changed.
- Swagger/Knife4j/OpenAPI path is documented when API handoff is in scope.

# Haier IAM Script Integration Reference

This reference is distilled from the uploaded `@haier/iam` browser SDK document. Use it when implementing script-tag SSO in frontend projects.

## SDK Script

Default version:

```html
<script src="https://r.haier.net/assets/prod/s01996-front/haier-iam/1.9.4/browser/index.min.js"></script>
```

Version `1.9.4` is the recommended browser SDK version from the source document. The browser build exposes the SDK at `window.__USERCENTER__`.

## Typical File Placement

For Vue/Vite projects, place the SDK script in the project-level `index.html`, usually before the closing `</body>` tag or before the app's module script if the project requires the SDK to be available before app bootstrap.

```html
<!-- index.html -->
<script src="https://r.haier.net/assets/prod/s01996-front/haier-iam/1.9.4/browser/index.min.js"></script>
```

Place the initialization and first `login()` call in `App.vue`, or in a small IAM adapter imported by `App.vue` when the codebase already separates authentication bootstrap logic.

```vue
<!-- App.vue -->
<script setup>
import { onMounted } from "vue";

onMounted(async () => {
  const iamSdk = window.__USERCENTER__;

  if (!iamSdk) {
    throw new Error("Haier IAM SDK is not loaded");
  }

  await iamSdk.configUserCenter({
    ssoUrl: "https://iam-test.haier.net",
    clientId: "your client id",
    tokenUrl: "https://your-backend.example.com/api/token",
    redirectUri: window.location.href,
  });

  const loginResult = await iamSdk.login();
  if (loginResult.success) {
    const { token, userInfo } = loginResult;
    console.log(token, userInfo);
  } else {
    console.error(loginResult.errorMessage, loginResult.result);
  }
});
</script>
```

## Minimal Browser Integration

If the script may load after app bootstrap, wait for the global with a bounded timeout before configuration:

```js
function waitForUserCenter(timeoutMs = 8000) {
  const startedAt = Date.now();

  return new Promise((resolve, reject) => {
    const tick = () => {
      if (window.__USERCENTER__) {
        resolve(window.__USERCENTER__);
        return;
      }
      if (Date.now() - startedAt > timeoutMs) {
        reject(new Error("Haier IAM SDK did not load"));
        return;
      }
      window.setTimeout(tick, 50);
    };

    tick();
  });
}
```

```js
const iamSdk = await waitForUserCenter();

await iamSdk.configUserCenter({
  ssoUrl: "https://iam-test.haier.net",
  clientId: "your client id",
  tokenUrl: "https://your-backend.example.com/api/token",
  redirectUri: window.location.href,
  exitUrl: "https://your-app.example.com/logout-success",
  onUserInfoChange: userInfo => {
    if (userInfo) {
      console.log(userInfo);
    }
  },
  extra: {
    // isOversea: true,
    // debugLog: true,
    // locationParseEnableHash: true,
  },
});

const loginResult = await iamSdk.login();
if (loginResult.success) {
  const { token, userInfo } = loginResult;
  console.log(token, userInfo);
} else {
  const { errorMessage, result } = loginResult;
  console.error(errorMessage, result);
}
```

`appId` is optional:

```js
await iamSdk.configUserCenter({
  ssoUrl: "https://iama.haier.net",
  clientId: "your client id",
  tokenUrl: "https://your-backend.example.com/api/token",
  // appId: "your feishu/ihaier app id",
});
```

Only include `appId` when the ihaier/Feishu container flow requires it and the product side has supplied a real value. Do not keep placeholder `appId` values in source code.

## Config Fields

Required:

- `ssoUrl`: Account-center login domain. Production is `https://iama.haier.net`; test is `https://iam-test.haier.net`. Do not add a trailing slash and do not use protocol-relative URLs such as `//iama.haier.net`.
- `clientId`: App client id or K Code from IAM app management.
- `tokenUrl`: Business backend token service address. Use HTTPS.

Common optional fields:

- `appId`: Feishu/ihaier app id. Optional.
- `redirectUri`: Redirect target after login. Defaults to the current URL when omitted.
- `exitUrl`: Redirect target after logout.
- `tokenRequestHeaderKey`: Request header name for the token. Default is `Access-Token`.
- `project`: Custom login project name.
- `clearUrlParamCode`: Clear code from the URL after web login. Defaults to `true`.
- `onTokenChange`: Callback when token changes.
- `onUserInfoChange`: Callback when user info changes.
- `extra.isOversea`: Overseas environment flag.
- `extra.debugLog`: Enable SDK debug logs.
- `extra.locationParseEnableHash`: Enable hash-router parsing.
- `extra.enableAuthTicket`: Enable third-party ticket login, available from version `1.9.4`.
- `extra.getTicketFromUrlFirst`: Prefer reading third-party ticket from URL, available from version `1.8.5`.

## Login And Logout

Call `login()` when the page loads. Do not pre-check local token existence as the main branch.

```js
const res = await iamSdk.login();
if (res.success) {
  const { token } = res;
  localStorage.setItem("haier_iam_access_token", token || "");
} else {
  const { errorMessage, errorCode, result } = res;
}
```

The backend `tokenUrl` used by login should return these canonical fields to the frontend-facing auth contract: `resultCode`, `resultMsg`, `access_token`, `expires_in`, `token_type`, `refresh_token`, and `account`. SDK adapters may expose `token`/`userInfo` internally, but API design should not replace the canonical field names with only local aliases.

When token expiry or API 401 happens:

```js
const res = await iamSdk.login({ invalidateToken: true });
```

For explicit logout:

```js
const ok = await iamSdk.logout();
if (ok) {
  // local cleanup or navigation
}
```

## Generic Fetch 401 Pattern

Adapt this pattern to the target project's request client instead of forcing a new HTTP layer.

```js
const TOKEN_STORAGE_KEY = "haier_iam_access_token";
const TOKEN_REQUEST_HEADER_KEY = "Access-Token";

function persistIamAuth(token) {
  localStorage.setItem(TOKEN_STORAGE_KEY, token || "");
}

function clearIamAuth() {
  localStorage.removeItem(TOKEN_STORAGE_KEY);
}

async function requestWithIam(input, init = {}) {
  const headers = new Headers(init.headers || {});
  const token = localStorage.getItem(TOKEN_STORAGE_KEY) || window.__USERCENTER__?.getToken?.();

  if (token) {
    headers.set(TOKEN_REQUEST_HEADER_KEY, token);
  }

  let response = await fetch(input, { ...init, headers });

  if (response.status === 401) {
    clearIamAuth();
    const loginResult = await window.__USERCENTER__.login({ invalidateToken: true });

    if (loginResult.success && loginResult.token) {
      persistIamAuth(loginResult.token);
      headers.set(TOKEN_REQUEST_HEADER_KEY, loginResult.token);
      response = await fetch(input, { ...init, headers });
    }
  }

  if (response.status === 403) {
    window.__USERCENTER__?.notPermission?.(() => {
      // custom no-permission handling
    });
  }

  return response;
}
```

Guard concurrent 401 responses so multiple failed requests do not trigger several simultaneous login refreshes. Use the target request client pattern, but keep a single shared refresh promise when possible.

Backend-facing header contract:

- Send `Access-Token: {token}` with every authenticated backend request.
- Do not send `Application-Key` or `clientId` from the frontend for token check. Backend code resolves `clientId` from server-side config or a trusted tenant/app registry and uses it as upstream `Application-Key`.
- If the backend returns 401 or a normalized token-invalid response, clear stale browser auth state and trigger `login({ invalidateToken: true })`.
- Clear the stored token on logout.

## TypeScript Global Declaration

Use a local declaration file such as `src/types/haier-iam.d.ts` when the project is TypeScript.

```ts
export interface HaierIamBackendLoginResponse {
  resultCode: string;
  resultMsg: string;
  access_token: string;
  expires_in: string;
  token_type: string;
  refresh_token: string;
  account: unknown;
}

export interface HaierIamLoginSuccess {
  success: true;
  userInfo?: HaierIamUserInfo;
  token?: string;
}

export interface HaierIamLoginFail {
  success: false;
  errorMessage?: string;
  errorCode?: number;
  result?: Record<string, unknown>;
}

export type HaierIamLoginResponse = HaierIamLoginSuccess | HaierIamLoginFail;

export interface HaierIamUserInfo {
  id?: string;
  account?: string;
  userName?: string;
  avatar?: string;
  activeState?: number;
  extension?: string;
  instanceId?: string;
  nickName?: string;
  userType?: number;
  phone?: string;
  email?: string;
  sourceCode?: string;
}

export interface HaierIamConfig {
  ssoUrl: string;
  tokenUrl: string;
  clientId: string;
  appId?: string;
  redirectUri?: string;
  exitUrl?: string;
  tokenRequestHeaderKey?: string;
  project?: string;
  clearUrlParamCode?: boolean;
  onTokenChange?: (token?: string) => void;
  onUserInfoChange?: (userInfo?: HaierIamUserInfo) => void;
  extra?: {
    enableAuthTicket?: boolean;
    disableWriteThirdToken?: boolean;
    tokenUrlRequestIgnoreHeaders?: string[];
    isOversea?: boolean;
    overseaShareTokenKeyOrders?: Array<
      "haier-user-center-access-token-global" | "haier-user-center-access-token"
    >;
    debugLog?: boolean;
    oauthLoginPagePrefix?: string;
    oauthLogoutPagePrefix?: string;
    locationParseEnableHash?: boolean;
    getTicketFromUrlFirst?: boolean;
  };
}

export interface HaierIamSdk {
  configUserCenter(options: HaierIamConfig): Promise<void>;
  login(params?: { force?: boolean; invalidateToken?: boolean }): Promise<HaierIamLoginResponse>;
  reLogin(params?: Record<string, unknown>): Promise<boolean>;
  logout(params?: Record<string, unknown>): Promise<boolean>;
  getConfig(): HaierIamConfig | undefined;
  getToken(): string | undefined;
  getUserInfo(): HaierIamUserInfo | undefined;
  requestUserInfoAndUpdate(): Promise<HaierIamUserInfo | undefined>;
  removeTokenPayload(): void;
  notPermission(callBack?: Function): void;
}

declare global {
  interface Window {
    __USERCENTER__?: HaierIamSdk;
    FORCE_IAM_DEBUG?: number;
  }
}
```

## Debug Mode

Supported debug switches, in priority order:

1. URL params: `?iam_debug=1` or `?iamDebug=1`.
2. Global variable: `window.FORCE_IAM_DEBUG = 1`.
3. Config: `extra.debugLog: true`.

## API Quick Reference

- `configUserCenter(options)`: Initialize or merge SDK configuration.
- `login(params?)`: SDK helper that may return `{ success: true, token, userInfo }` or `{ success: false, errorMessage, result }`. The backend `tokenUrl` response contract still uses `resultCode`, `resultMsg`, `access_token`, `expires_in`, `token_type`, `refresh_token`, and `account`.
- `reLogin(params?)`: Re-login helper, commonly used for expired auth.
- `logout(params?)`: Logout.
- `getConfig()`: Read initialized config.
- `getToken()`: Read token stored by the SDK.
- `getUserInfo()`: Read user info stored by the SDK.
- `requestUserInfoAndUpdate()`: Fetch latest user info and update SDK storage.
- `removeTokenPayload()`: Clear local login state.
- `notPermission(callback?)`: Handle no-permission state, defaults to alert behavior.

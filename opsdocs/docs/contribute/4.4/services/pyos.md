# pyos (abcdesktop control plane) - Full Documentation and Specification

## 1. Executive summary

pyos is the backend control plane for abcdesktop. It exposes a CherryPy HTTP API used to authenticate users, create/resume/remove cloud desktops, launch applications in those desktops, manage user desktops, and perform operator actions.

At runtime, pyos sits between:

- Clients (web frontend and admin tools)
- Identity providers (OAuth2, LDAP/AD, anonymous, prelogin/logmein flows)
- Infrastructure services (Kubernetes, MongoDB, Memcached, DNS helpers)

The main service process is started by `od.py` and mounts API endpoints under `/API`.

## 2. Scope and responsibility

### 2.1 What pyos does

- Exposes REST-like endpoints for authentication, desktop lifecycle, app lifecycle, state storage, metrics, and admin operations.
- Loads and validates configuration (`od.config` by default, or `OD_CONFIG_PATH`).
- Initializes shared services:
  - Authentication and JWT
  - MongoDB datastore
  - Memcached cache/session helpers
  - Accounting and message progress channels
  - Fail2ban-like abuse controls
  - GeoIP/ASN support
  - Optional internal DNS integration
- Selects and uses a Kubernetes orchestrator implementation for desktop/app pods.
- Starts background watchers (Mongo change stream, Kubernetes watcher) and stops them cleanly on process shutdown.

### 2.2 What pyos does not do directly

- It is not the desktop runtime itself. User desktops run as pods/containers managed by the orchestrator.
- It is not a reverse proxy or edge TLS terminator.
- It is not the frontend UI; it serves API responses consumed by other components.

## 3. Startup and lifecycle (od.py)

`od.py` is the process entrypoint and boot coordinator.

### 3.1 Boot sequence

1. Configure logging from the same configuration source used by CherryPy settings.
2. Load settings and materialize all global runtime configuration.
3. Initialize core services (auth, datastore, cache, accounting, prelogin/logmein, etc.).
4. Verify/init infrastructure integration (Kubernetes detection).
5. Build app catalog cache and start Kubernetes watcher object.
6. Configure CherryPy, mount `/API`, subscribe signal handlers and service watcher plugin.
7. Start CherryPy engine and block.

### 3.2 Request/response handling behaviors in od.py

- Unified JSON error handling:
  - `request.error_response` maps runtime exceptions to JSON `{status, message}`.
  - `error_page.default` returns JSON for unhandled errors.
- Request tracing (`before_handler` tool):
  - Logs path and request JSON.
  - Redacts sensitive fields (`password`, authorization token fields in `result.authorization`).
- Response tracing (`on_end_request` tool):
  - Logs response body up to configurable `max_log_body_size`.
  - Can be disabled per response with `cherrypy.response.notrace = True`.
- Health and version helpers:
  - `/API/healthz` returns `OK` (with response trace disabled).
  - `/API/version` returns content of `version.json` with fallback values.

### 3.3 Signal and graceful shutdown

`SIGTERM`, `SIGQUIT`, and `SIGINT` trigger engine exit. A CherryPy plugin (`ODCherryWatcher`) starts/stops service-side threads together with the web engine lifecycle.

## 4. Architecture

### 4.1 Layered model

- HTTP layer:
  - CherryPy app mounted at `/API`.
  - Controller auto-discovery and route attachment.
- Controller layer:
  - Per-domain controllers in `controllers/`.
  - Security checks and request policy enforcement via `BaseController`.
- Service layer:
  - Shared singleton service container (`ODServices`).
  - Encapsulates auth, data stores, tracking, DNS, key mgmt, cache, etc.
- Domain/orchestration layer:
  - Desktop/application lifecycle logic in composer and orchestrator modules.
  - Kubernetes-backed execution model.
- Data/integration layer:
  - MongoDB, Memcached, external auth providers, GeoIP/ASN DB, optional internal DNS.

### 4.2 Dynamic controller registration

Controllers are loaded by class discovery in `controllers/` where class names match `*Controller`. The route prefix is class name without `Controller`, lowercased.

Examples:
- `AuthController` -> `/API/auth/*`
- `ComposerController` -> `/API/composer/*`
- `ManagerController` -> `/API/manager/*`

## 5. Security and trust model

### 5.1 Authentication model

Authentication is pluggable via manager/provider config. Supported patterns include:

- External OAuth2
- Explicit LDAP/Active Directory
- Implicit/anonymous
- Optional prelogin/logmein flows

JWT is used for user and desktop tokens with configurable key files and expiration.

### 5.2 Controller security controls

`BaseController` provides:

- Required environment checks for authenticated routes (`validate_env`).
- IP ban checks and login ban checks (fail2ban service integration).
- API-key checks (`X-API-Key` / `X-Api-Key`) for protected admin routes.
- IP/CIDR filtering (`permitip` lists).
- Per-method request allow/deny gates (`requestsallowed`).

### 5.3 Proxy header spoofing protection

`X-Forwarded-For` is validated against `trusted_proxy_cidr`. If proxy hops in header are not trusted and header is present, request can be treated as spoofed and source is failed/banned.

### 5.4 Sensitive data logging controls

Request tracing masks known sensitive fields. Response tracing can be disabled for selected routes.

## 6. Configuration specification

### 6.1 Source and format

- Default file: `od.config` (CherryPy INI-like config dictionary syntax).
- Override path: `OD_CONFIG_PATH` environment variable.
- Selected values may also be overridden by dedicated environment variables (example: Mongo and memcache values).

### 6.2 Important config domains

- Core host/routing:
  - `default_host_url`
  - `websocketrouting`
  - `trusted_proxy_cidr`
- Auth:
  - `authmanagers`, provider config refs
  - `auth.prelogin`, `auth.logmein`
  - JWT config blocks
- Infrastructure:
  - MongoDB URL/params
  - Memcache host/port
  - Kubernetes namespace and service domain behavior
- Desktop behavior:
  - Pod templates, volumes, mounts, node selectors, DNS policy, persistence options
  - Security policy label matching
  - Environment variables for desktop containers
- Frontend behavior metadata:
  - Dock entries/icons
  - Menu config, notification config, tips/welcome

### 6.3 Initialization order matters

Settings init is ordered to satisfy dependencies. For example:
- stack/domain values before DB/cache resolution checks
- desktop init before controller wrapping defaults
- host URL setup before websocket routing checks

## 7. Service container specification (ODServices)

`ODServices` centralizes all long-lived service objects and starts/stops dependent threads.

Initialized services include:

- `datastore`: Mongo client wrapper
- `sharecache`: Memcached wrapper
- `messageinfo`: progress/notification manager
- `auth`: authentication tool bound into CherryPy
- `accounting`: accounting counters
- `internaldns`: optional internal DNS helper
- `jwtdesktop`: desktop JWT helper
- `keymanager`: desktop key operations
- `locator`: public and AD-site-aware geolocation helper
- `prelogin`, `logmein`
- `fail2ban`
- `asnumber`: ASN DB lookup (`ipasn_db.dat`)
- `authorized_keys`
- `apps`: application catalog/cache and watcher
- `kuberneteswatcher`

Threaded runtime behaviors:
- On start: Mongo watcher and Kubernetes watcher start (if initialized).
- On stop: both are stopped with guarded error handling.

## 8. API surface (controller domains)

This section summarizes route domains and key capabilities.

### 8.1 Auth controller (`/API/auth/*`)

Primary responsibilities:

- Return auth configuration for clients.
- Login/logout/disconnect/token refresh.
- OAuth callback flow and redirect page rendering.
- Prelogin and logmein support.
- Authorized key export route.
- Label query and secret building utility route.

Notable security behaviors:

- Enforces spoofing checks and fail2ban interactions.
- Optional prelogin verification path before credential auth.

### 8.2 Composer controller (`/API/composer/*`)

Primary responsibilities:

- Launch/resume desktop sessions.
- Run applications in user desktop context.
- List application/container states.
- Fetch logs and env, stop/remove containers.
- List secrets and return desktop description metadata.

This is the main user session orchestration API domain.

### 8.3 Manager controller (`/API/manager/*`)

Primary responsibilities:

- Operational/admin endpoints:
  - health, echo HTTP, app list rebuild
  - AD site cache update
  - garbage collection
  - datastore CRUD-like routes
  - desktop/image/ban management routes
  - dry-run desktop path

This domain is protected by API-key and/or CIDR policies as configured.

### 8.4 Other controllers

- Core controller: key/message info helpers.
- Accounting controller: metrics exports.
- Store controller: key/value user store operations and collection reads.
- User controller: user identity/location helpers.
- Key controller: key generation endpoint.

## 9. Data and external dependencies

### 9.1 Persistent and shared stores

- MongoDB: metadata and history (applications, profiles, desktop state/history, fail2ban data, etc.).
- Memcached: short-lived shared state/caching/session helpers.

### 9.2 Runtime infrastructure dependencies

- Kubernetes API (cluster config must be available in runtime environment).
- DNS resolution for configured service hostnames.
- Optional LDAP/AD infrastructure depending on auth provider setup.

### 9.3 Geo and ASN data

- GeoLite2 ASN/City MMDB files used by geolocation flows.
- `ipasn_db.dat` generated from RouteViews rib data for ASN lookup service.

## 10. Observability

- Configurable Python logging with structured context filters.
- Per-record context enrichment includes node/hostname, user id, and source ip where applicable.
- Optional Graylog integration via `graypy` (through logging configuration).
- Request and response tracing hooks in API layer.

## 11. Error model

- API errors are normalized as JSON with status and message.
- Controller logic frequently raises CherryPy HTTP errors for validation/security failures.
- Some route helpers return `Results.success/error(...)` standardized payloads.

## 12. Docker image specification

Two image definitions are provided for different trade-offs.

---

## 13. Dockerfile.ubuntu deep specification

### 13.1 Base and shell

- Base image: `ubuntu:24.04`
- Shell switched to bash for `source` command usage.

### 13.2 System packages

Installs:

- Python runtime and virtualenv toolchain
- Build/dev dependencies for Python extensions and auth libs
- Kerberos/SASL/LDAP/GSS support packages
- Utility tools (`curl`, `wget`, `cntlm`, ldap tools)

### 13.3 Geo databases

Downloads GeoLite2 ASN and City MMDB files into `/usr/share/geolite2`.

### 13.4 NTLM support

Copies prebuilt Debian packages from multi-stage source image `ghcr.io/abcdesktopio/ntlm_auth:ubuntu_24.04`, installs them, then updates dynamic linker config for Samba libs.

This image is designed to support NTLM/SSO-related features.

### 13.5 Application install model

- Workdir: `/var/pyos`
- Copies project files and entrypoint script.
- Creates venv at `/var/pyos`.
- Activates venv and installs Python requirements.

### 13.6 ASN database build

Inside venv:

- Download latest v4/v6 rib archive.
- Convert to `ipasn_db.dat`.
- Remove intermediate archive.

### 13.7 Slim-down phase

Removes build-time development packages and runs autoremove/cleanup.

### 13.8 Runtime command

- Copies `ntlm_auth` binary to project path expected by auth module.
- Ensures `/var/pyos/logs` exists.
- Starts with `/docker-entrypoint.sh`.

`docker-entrypoint.sh` behavior:

- `cd /var/pyos`
- `source bin/activate`
- run `./od.py`

### 13.9 Operational profile

Best when you need:

- Maximum auth compatibility (Kerberos/LDAP/NTLM stack)
- Production-like enterprise integration features

---

## 14. Dockerfile.alpine deep specification

### 14.1 Base

- Base image: `python:alpine`
- Lighter image profile, musl-based userspace.

### 14.2 Installed packages

- Runtime tools/libraries: `bash`, `curl`, `cntlm`, Kerberos libs, `wget`
- Build/development packages for Python extensions (`gcc`, `musl-dev`, `krb5-dev`, `openldap-dev`, `geoip-dev`)
- Python ldap/gssapi Alpine packages where available

### 14.3 Geo and ASN data

- Downloads GeoLite2 ASN/City to `/usr/share/geolite2`.
- Builds `ipasn_db.dat` similarly to Ubuntu image.

### 14.4 NTLM note

NTLM auth support installation is intentionally commented out in this Dockerfile. Comments explicitly suggest using the Ubuntu image for SSO feature completeness.

### 14.5 Application install and run

- Workdir `/var/pyos`, copy full source.
- Upgrade pip, install requirements.
- Remove dev packages after build.
- Ensure log dir exists.
- Run command is direct: `./od.py`.

### 14.6 Operational profile

Best when you need:
- Smaller image footprint
- Simpler/non-SSO deployments

Potential trade-off:
- Reduced compatibility for some enterprise auth edge cases compared with Ubuntu build.

## 15. Ubuntu vs Alpine comparison

- Auth/SSO capability:
  - Ubuntu image is the primary full-feature path (includes ntlm_auth flow).
  - Alpine image is explicitly limited for NTLM/SSO in current Dockerfile.
- Build ecosystem:
  - Ubuntu relies on apt/deb packages and glibc ecosystem.
  - Alpine relies on apk/musl and can differ in native dependency behavior.
- Startup model:
  - Ubuntu uses entrypoint script + venv activation.
  - Alpine runs `od.py` directly in image Python environment.

## 16. Known constraints and assumptions

- Kubernetes must be reachable and configured at runtime.
- MongoDB and Memcached hostnames must resolve from pod/container network.
- Misconfigured `trusted_proxy_cidr` may weaken or over-trigger spoofing controls.
- Auth provider configuration quality directly affects login behavior.
- Configuration correctness is critical; several init paths intentionally exit on fatal validation errors.

## 17. Minimal runtime sequence (end-to-end)

1. Client calls auth endpoints.
2. pyos validates security constraints and authenticates user through configured manager/provider.
3. pyos prepares resources and issues JWT user token.
4. Client calls composer launch/run APIs with token context.
5. pyos orchestrator finds or creates desktop pod and manages app containers.
6. State/progress/telemetry are recorded through cache/datastore/accounting services.
7. Admin/operator APIs are available via manager routes with separate access policies.

## 18. Source files used for this specification

Primary runtime entrypoint:
- `od.py`

Container definitions:

- `Dockerfile.ubuntu`
- `Dockerfile.alpine`
- `docker-entrypoint.sh`

Key architecture modules reviewed:

- `oc/od/settings.py`
- `oc/od/services.py`
- `oc/od/base_controller.py`
- `oc/od/composer.py`
- `oc/od/orchestrator.py`
- selected controller files under `controllers/`

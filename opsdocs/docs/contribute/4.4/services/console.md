---
title: abcdesktop.io Console Service | abcdesktop.io
description: Architecture and developer reference for the abcdesktop.io console web service: landing page, session management, application listing, and administrative functions.
keywords: console, web service, developer, architecture, abcdesktop, Kubernetes, contribute
tags:
  - contribute
  - console
  - service
---

# Console - abcdesktop Administration Console
 
## Project Specification
 
### Purpose
 
`console` is a web-based administration interface for the abcdesktop platform. It is a single-page React application built with Vite, served by a lightweight nginx container. It communicates exclusively with `pyos` — the abcdesktop control plane — through its `/API/manager/` endpoints, using an API key for authentication.
 
---
 
## Architecture Overview
 
```
┌─────────────────┐
│   Admin         │
│   (Browser)     │
└────────┬────────┘
         │ HTTP /console
         ▼
┌─────────────────────────────────────────────────────────┐
│                    route (OpenResty)                    │
│               proxy_pass → console upstream             │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                console (nginx:alpine-slim)               │
│   Serves static React/Vite SPA from /usr/share/nginx/html│
│   Base path: /console/                                  │
└────────┬────────────────────────────────────────────────┘
         │ fetch /API/manager/* + X-API-KEY header
         ▼
┌─────────────────────────────────────────────────────────┐
│                   pyos (Python/CherryPy)                │
│   - Desktop management                                  │
│   - Application (image) management                     │
│   - Ban management                                      │
└─────────────────────────────────────────────────────────┘
```
 
---
 
## Application Structure
 
```
console/
├── Dockerfile                  # Multi-stage build: Node builder → nginx:alpine-slim
├── docker-entrypoint.sh        # Starts nginx in foreground mode
├── Makefile                    # Dev helper commands (build, run, stop, exec, logs)
└── app/                        # React/Vite source
    ├── index.html
    ├── vite.config.js          # base: '/console/'
    ├── package.json
    └── src/
        ├── main.jsx
        ├── App.jsx             # Router: 4 pages
        ├── Layout.jsx          # Sidebar + Outlet
        ├── pages/
        │   ├── desktops.jsx    # Desktop management page
        │   ├── apps.jsx        # Application management page
        │   ├── banIp.jsx       # IP ban management page
        │   └── banLogin.jsx    # Login ban management page
        ├── services/           # API call layer (fetch wrappers)
        │   ├── desktopsService.js
        │   ├── appsService.js
        │   ├── banService.js
        │   └── permitRequestService.js
        ├── hooks/              # Custom React hooks
        │   ├── usePermitRequest.js
        │   ├── useEntityManager.js
        │   └── useResourcesUsage.js
        ├── components/         # Reusable UI components
        └── utils/
            └── constraints.js  # API base URL + runtime config loading
```
 
---
 
## Pages
 
### Desktops Page (`/`)
 
The default landing page, which lists all active user desktop pods in the abcdesktop cluster.
 
**Features:**
- List all desktops with name, status, pod IP, node, and creation timestamp
- Delete a single desktop via the red trash icon on its row
- Bulk-delete by selecting multiple rows
- Expand a desktop row to view detailed information across 6 tabs:
  - **Metadata** – labels, annotations, UID, namespace
  - **Spec** – node assignment, restart policy, container specs (init / standard / ephemeral)
  - **Status** – phase, QoS class, container states, restart counts
  - **Volumes** – volume names, types, and configuration details
  - **Containers & Pods** – running containers and application pods
  - **Resources Usage** – live CPU % and RAM (MB) charts, polled every 5 seconds
### Applications Page (`/apps`)
 
Manages the application images (Docker-based apps) available in the abcdesktop platform.
 
**Features:**
- List installed applications with icon, name, and short ID
- View full application JSON descriptor by clicking the app name
- Add an application via:
  - **App Store modal** — browse and search the curated application catalog
  - **JSON modal** — paste raw JSON or upload a `.json` file
- Delete a single application via the trash icon
- Bulk-delete by selecting multiple rows
### Ban IP Page (`/banIp`)
 
Manages IP address bans. IP bans prevent connections from specific IPv4 addresses from reaching the platform.
 
**Features:**
- List currently banned IPs with ban date and TTL in seconds
- Add a ban by entering an IPv4 address (`X.X.X.X` format)
- Remove a ban (unban) via the trash icon
### Ban Login Page (`/banLogin`)
 
Manages user login bans. Login bans prevent specific usernames from authenticating, regardless of the source IP address.
 
**Features:**
- List currently banned logins with ban date and TTL in seconds
- Add a ban by entering a username
- Remove a ban (unban) via the trash icon
---
 
## Authentication
 
All API requests to `pyos` are authenticated with an `X-API-KEY` header. The key is stored in the browser's `localStorage` under the key `apiKey`.
 
On first access (or when the stored key is invalid), an **API Key modal** is displayed, prompting the admin to enter a valid key. Validity is checked against the `/API/manager/healtz` endpoint.
 
```
GET /API/manager/healtz
X-API-KEY: <admin-api-key>
```
 
The key must be configured on the `pyos` side in the `od.config` file. If no `apikey` is specified, the **API Key modal** does not appear and the administrator has unrestricted access to the console.

!!! note 
    More information on the API key is available on [this page](https://www.abcdesktop.io/advanced/4.4/controllers/controllers/#access-control-filter)
 
---
 
## pyos API Endpoints Used
 
### Desktop Endpoints
 
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/API/manager/desktop` | List all active desktops |
| `GET` | `/API/manager/desktop/{id}` | Get raw JSON for a specific desktop |
| `DELETE` | `/API/manager/desktop/{id}` | Delete a desktop |
| `GET` | `/API/manager/desktop/{id}/pod` | List application pods of a desktop |
| `DELETE` | `/API/manager/desktop/{id}/pod/{podId}` | Delete a specific pod |
| `GET` | `/API/manager/desktop/{id}/resources_usage` | Get global resource usage for a desktop |
| `GET` | `/API/manager/desktop/{id}/{type}/{objectId}/resources_usage` | Get per-container or per-pod resource usage (`type` = `container` or `pod`) |
 
### Application Endpoints
 
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/API/manager/buildapplist` | List all installed applications |
| `GET` | `/API/manager/image/{id}` | Get full JSON descriptor of an application |
| `PUT` | `/API/manager/image` | Add a new application (JSON body) |
| `DELETE` | `/API/manager/image/{id}` | Delete an application |
 
### Ban Endpoints
 
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/API/manager/ban/{type}` | List bans (`type` = `ipaddr` or `login`) |
| `POST` | `/API/manager/ban/{type}/{id}` | Add a ban |
| `DELETE` | `/API/manager/ban/{type}/{id}` | Remove a ban |
 
### Utility Endpoints
 
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/API/manager/healtz` | Health check / API key validation |
 
---
 
## Resources Usage Monitoring
 
The `useResourcesUsage` hook polls the backend every **5 seconds** to collect CPU and RAM metrics for a desktop or one of its containers.
 
**Metrics used (cgroup-based):**
 
| Metric | Description |
|--------|-------------|
| `cpuacct.usage` | Cumulative CPU time in nanoseconds |
| `cpu.cfs_quota_us` | CPU quota in microseconds per 100ms period |
| `memory.usage_in_bytes` | Current memory usage in bytes |
| `memory.limit_in_bytes` | Memory limit in bytes (used to bound Y-axis) |
 
**CPU % computation:**
 
```
cpuLimit = cpu.cfs_quota_us / 100000   (normalize to seconds)
cpuPercent = (ΔcpuNano / 1e9) / (Δtime_sec × cpuLimit) × 100
```
 
**Chart retention:** The last 60 data points are kept (5 minutes of history at 5-second intervals).
 
---
 
## Runtime Configuration
 
At startup, the app fetches a runtime config file from `console/config/versionConfig.json`. This JSON file is expected to contain:
 
| Key | Description |
|-----|-------------|
| `ABCDESKTOP_VERSION` | Version string exposed to the UI |
| `ABCDESKTOP_APPLICATIONS_LIST_URL` | URL of the external applications catalog (used by the App Store modal) |
 
These values are stored on `window` and consumed throughout the application.
 
---
 
## Docker Image
 
### Build Process
 
The image uses a **multi-stage build**:
 
1. **Builder stage** (`ubuntu:latest` by default):
   - Installs Node.js 20 via the NodeSource repository
   - Copies the `app/` directory
   - Runs `npm install` and `npm run build` (Vite production build)
   - Output is placed in `app/dist/`
2. **Runtime stage** (`nginx:alpine-slim`):
   - Copies the built static files from `app/dist/` into `/usr/share/nginx/html`
   - Exposes port `80`
   - Entrypoint runs `nginx -g 'daemon off;'`
### Build Arguments
 
| Argument | Default | Description |
|----------|---------|-------------|
| `BASE_IMAGE` | `ubuntu` | Base OS image for the builder stage |
| `TAG` | `latest` | Tag of the base OS image |
 
### Supported Platforms
 
The CI pipeline builds for `linux/amd64` and `linux/arm64`.
 
---
 
## Frontend Dependencies
 
### Runtime
 
| Package | Version | Role |
|---------|---------|------|
| `react` | ^18.3.1 | UI framework |
| `react-dom` | ^18.3.1 | DOM rendering |
| `react-router-dom` | ^6.30.3 | Client-side routing (HashRouter) |
| `react-bootstrap` | ^2.10.10 | UI component library |
| `bootstrap` | ^5.3.7 | CSS framework |
| `bootstrap-icons` | ^1.13.1 | Icon set |
| `recharts` | ^3.1.0 | CPU/RAM time-series charts |
| `@table-library/react-table-library` | ^4.1.15 | Data table with expand/select |
| `perfect-scrollbar` | ^1.5.6 | Custom scrollbar |
| `@emotion/react` | ^11.14.0 | CSS-in-JS (peer dependency) |
 
### Development
 
| Package | Role |
|---------|------|
| `vite` + `@vitejs/plugin-react` | Build tool and dev server |
| `eslint` | Linting |
| `cypress` | End-to-end tests |
 
---
 
## CI/CD Pipeline
 
The GitHub Actions workflow (`.github/workflows/docker-image.yml`) runs on every push, pull request, and nightly schedule:
 
1. Build a test image tagged `console:test.<branch>`
2. Spin up a Minikube cluster
3. Deploy a full abcdesktop stack using the test image
4. Wait for the `/console` endpoint to become reachable
5. Run Cypress end-to-end tests
6. On success, build and push the final multi-arch image tagged `console:<branch>` to `ghcr.io/abcdesktopio/console`
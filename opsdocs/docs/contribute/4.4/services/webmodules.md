# WebModules - abcdesktop Frontend Web Content

## Project Specification

### Purpose

`webModules` is the frontend web content repository for the abcdesktop platform. It contains all the HTML, JavaScript, CSS (written in LESS), images, and supporting assets that make up the user-facing desktop interface. It is served by an nginx container (`oc.nginx`) and constitutes the client side that users interact with directly in their browser.

---

## Architecture Overview

```
┌─────────────────┐
│   User          │
│   (Browser)     │
└────────┬────────┘
         │ HTTP /
         ▼
┌─────────────────────────────────────────────────────────┐
│                    route (OpenResty)                    │
│               proxy_pass → website upstream             │
└────────┬────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│              oc.nginx (nginx:alpine-slim)                │
│   Serves static HTML/CSS/JS from /usr/share/nginx/html  │
│   Built from webModules source via transpile pipeline   │
└────────┬────────────────────────────────────────────────┘
         │ fetch /API/*  (odApiClient)
         ▼
┌─────────────────────────────────────────────────────────┐
│                   pyos (Python/CherryPy)                │
│   Auth, desktop launch, application management, etc.    │
└─────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```
webModules/
├── Dockerfile              # Main image: builder → nginx:alpine-slim
├── Dockerfile.builder      # Builder image: Ubuntu + Node.js + less
├── Makefile                # Build orchestration (css, svg, ui, prod, dev, clean…)
├── mkversion.sh            # Generates version.json at build time
├── package.json            # npm dependencies (jQuery, Bootstrap, xterm, noVNC…)
├── index.mustache.html     # Login/welcome page template (Mustache)
├── description.mustache.html # App description page template
│
├── js/                     # JavaScript modules (ES modules + legacy)
│   ├── scripts.js          # Main entry point — imports and wires all modules
│   ├── odapiclient.js      # Low-level API client (all /API/* calls)
│   ├── auth.js             # Authentication manager (managers & providers)
│   ├── launcher.js         # Desktop launch logic, JWT, refresh
│   ├── welcomesystem.js    # Login screen UI controller
│   ├── connectloader.js    # Desktop connection lifecycle
│   ├── broadway-vnc.js     # VNC/Broadway display integration (noVNC)
│   ├── appstore.js         # Application store UI
│   ├── appSelector.js      # Application selector in taskbar
│   ├── menu.js             # Top menu and taskbar
│   ├── settings.js         # Settings panel (tabbed)
│   ├── settings_tabs/      # Settings sub-modules (audio, printer, screen…)
│   ├── clipboard.js        # Clipboard sync between browser and desktop
│   ├── upload.js           # File upload to user's container
│   ├── download.js         # File download from user's container
│   ├── printer.js          # Printer management
│   ├── printSystem.js      # Print job lifecycle
│   ├── webshell.js         # Integrated xterm.js terminal
│   ├── speaker/main.js     # Audio output (WebAudio/WebSocket)
│   ├── microphone/main.js  # Microphone input (Web Audio Worklet)
│   ├── screenRecord.js     # Screen recording
│   ├── snapshot.js         # Desktop snapshot/screenshot
│   ├── shareSystem.js      # Desktop sharing
│   ├── gamepad.js          # Gamepad input forwarding
│   ├── geolocation.js      # Browser geolocation forwarding
│   ├── liveaudio.js        # Live audio streaming
│   ├── broadcastsystem.js  # Desktop broadcast notifications
│   ├── notificationsystem.js # In-page notification toasts
│   ├── tipsinfo.js         # Contextual tips overlay
│   ├── welcomeinfo.js      # Welcome/news information panel
│   ├── system.js           # System-level events and state
│   ├── taskstate.js        # Task/application state tracking
│   ├── quickSupport.js     # Quick support / remote assistance
│   ├── supportSystem.js    # Support system integration
│   ├── logmein.js          # LogMeIn SSL mutual auth support
│   ├── jwtstorage.js       # JWT token storage helpers
│   ├── ocuaparser.js       # User-Agent parsing
│   ├── speedtest_worker.js # Web Worker for speedtest endpoint
│   ├── windowMessage.js    # Cross-window postMessage handling
│   ├── desktopfeatures.js  # Feature detection and capability flags
│   ├── languages.js        # i18n language loading
│   ├── runtime.js          # Runtime configuration loader
│   └── noVNC/              # Embedded noVNC library (VNC client)
│
├── css/                    # LESS stylesheets (compiled to CSS at build time)
│   ├── base.less           # Base layout
│   ├── globale.less        # Global imports
│   ├── loginScreen.less    # Login/welcome screen
│   ├── menu.less           # Top menu and taskbar
│   ├── appstore.less       # Application store
│   ├── settings.less       # Settings panel
│   ├── settings_parts/     # Per-tab settings styles
│   ├── upload.less         # File upload overlay
│   ├── notification.less   # Notification toasts
│   └── animations/         # CSS animation keyframes
│
├── i18n/                   # Internationalization
│   ├── list.json           # Language code → file mapping
│   ├── en-EN.mustache.json # English strings
│   ├── fr-FR.mustache.json # French strings
│   ├── ro-RO.mustache.json # Romanian strings
│   └── zh-CN.mustache.json # Chinese (Simplified) strings (not ready yet)
│
├── img/                    # Static icons and images
│   ├── top/                # Toolbar icons (SVG)
│   ├── settings/           # Settings panel icons (SVG)
│   ├── welcome/            # Auth provider logos (SVG)
│   ├── appstore/           # App category icons (SVG)
│   ├── error/              # Error state illustrations (SVG)
│   └── abcdesktop*.ico     # Favicon variants
│
├── mimetypes/              # ~500 MIME type icons (SVG) for the file manager
│
├── tips/                   # Contextual tips templates (Mustache/SVG)
│
├── identification/         # Session error / "cannot open session" static site
│
└── transpile/              # Build toolchain
    ├── index.js            # CLI transpiler (svg, css, ui, prod flags)
    ├── config/
    │   ├── ui.json         # Branding: name, colors, URLs
    │   └── modules.json    # JS/CSS bundle definitions
    ├── production-transformer.js # Prod bundle builder
    └── native/             # Optional C++ N-API SVG replacer
```

---

## Build Pipeline

The `transpile/index.js` tool drives the entire build. It is invoked by `make` with different targets.

### Build Steps

```
make prod
└── transpile/index.js --svg --css --user-interface --prod
    │
    ├── --svg      Replace @tertiary color token in all SVG files
    │              (reads color from ui.json)
    │
    ├── --css      Compile all LESS files → CSS
    │              Output: css/css-dist/
    │
    ├── --user-interface
    │              Render Mustache templates into final HTML files
    │              (index.html, app.html, description.html…)
    │              Injects: project name, colors, i18n URLs, JS/CSS bundles
    │
    └── --prod     Bundle all JS modules into a minified app.js
                   Inject into index.html instead of individual <script> tags
```

### Make Targets

| Target | Description |
|--------|-------------|
| `make install` | Install npm dependencies (root, transpile, noVNC) |
| `make dev` | Build SVG + CSS + UI (no minification) |
| `make prod` | Full production build (minified JS, SVG, CSS, UI) |
| `make css` | Compile LESS → CSS only |
| `make svg` | Recolor SVG files with `@tertiary` from `ui.json` |
| `make ui` | Render Mustache templates only |
| `make clean` | Remove all build artifacts (`css-dist/`, `index.html`, `app.js`…) |
| `make oc.nginx.builder` | Build the `oc.nginx.builder` Docker image |
| `make oc.nginx` | Build the final `oc.nginx` Docker image |

---

## Customization: `transpile/config/ui.json`

`ui.json` is the **branding configuration file**. Editing it and rebuilding the image is the primary way to customise the frontend appearance.

### Structure

```json
{
  "name": "abcdesktop.io",
  "projectNameSplitedHTML": "<span id='projectNameSplitedStagea'>a</span>...",
  "colors": [ ... ],
  "urlcannotopensession": "/identification/site/",
  "urlusermanual":  "https://www.abcdesktop.io/",
  "urlusersupport": "https://www.abcdesktop.io/",
  "urlopensourceproject": "https://www.abcdesktop.io/"
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `name` | Project name displayed on the login screen |
| `projectNameSplitedHTML` | HTML markup for the animated login logo (one `<span>` per letter/word) |
| `urlcannotopensession` | Redirect URL when a session cannot be opened |
| `urlusermanual` | Link to the user manual |
| `urlusersupport` | Link to user support |
| `urlopensourceproject` | Link to the open-source project page |

### Color Tokens

All LESS stylesheets and SVG icons use these color tokens. Changing them in `ui.json` and rebuilding recolors the entire UI:

| Token | Default | Description |
|-------|---------|-------------|
| `@primary` | `#474B55` | Main background / surface color |
| `@secondary` | `#2D2D2D` | Secondary background |
| `@tertiary` | `#65AECD` | Accent / highlight color (also applied to SVG icons) |
| `@quaternary` | `#1E1E1E` | Deepest background |
| `@svgColor` | `#FFFFFF` | Default SVG fill color |
| `@danger` | `#CD3C14` | Error / destructive action color |
| `@success` | `#32C832` | Success state color |
| `@info` | `#527EDB` | Informational color |
| `@warning` | `#FFCC00` | Warning state color |
| `@blue` | `#4BB4E6` | Blue accent |
| `@green` | `#50BE87` | Green accent |
| `@purple` | `#A885D8` | Purple accent |

!!! note 
    More information about UI customization and how to apply your own look & feel on [this page](https://abcdesktop.pepins.net/advanced/4.4/configure/customfrontend/)

---

## JavaScript Modules

### Entry Point: `js/scripts.js`

`scripts.js` is the main ES module. It imports all other modules, builds the global `window.od` object, and wires up the application lifecycle on `DOMContentLoaded`.

Key globals exposed on `window.od`:

| Global | Source | Description |
|--------|--------|-------------|
| `window.od.broadway` | `broadway-vnc.js` | VNC/Broadway display instance |
| `window.od.ocrun` | `launcher.js` | Launch an application |
| `window.od.docker_logoff` | `launcher.js` | Log off the current session |
| `window.od.connectLoader` | `connectloader.js` | Desktop connection manager |
| `window.od.isTactile` | browser | `true` if touch device |
| `window.od.currentUser` | `launcher.js` | Currently authenticated user object |

### API Client: `js/odapiclient.js`

`odApiClient` is a singleton that wraps all `/API/*` calls to `pyos`. It is organized into sub-clients:

| Sub-client | Namespace | Example methods |
|------------|-----------|-----------------|
| Authentication | `odApiClient.auth` | `getauthconfig()`, `login()`, `logout()`, `refreshtoken()` |
| Desktop | `odApiClient.desktop` | `createdesktop()`, `getdesktop()`, `destroy()` |
| Applications | `odApiClient.app` | `getlist()`, `launch()` |
| File system | `odApiClient.files` | `list()`, `read()`, `write()` |
| Settings | `odApiClient.settings` | `get()`, `set()` |
| System | `odApiClient.system` | `info()`, `version()` |

The JWT user token is automatically stored in and read from `localStorage` under the key `abcdesktop_jwt_user_token`. It is refreshed automatically when 85% of its TTL has elapsed.

### Authentication: `js/auth.js`

`AuthManager` handles the login screen. It supports multiple authentication **managers** (e.g., `explicit`, `implicit`, `external`), each with one or more **providers** (e.g., LDAP, Active Directory, Google, GitHub, anonymous). Managers and providers are dynamically instantiated from the pyos auth configuration returned by `/API/auth/getauthconfig`.

### Key Feature Modules

| Module | Description |
|--------|-------------|
| `broadway-vnc.js` | Integrates noVNC (RFB) for X11 display streaming over WebSocket (`/websockify`) |
| `webshell.js` | Embeds an xterm.js terminal, connected to `/terminals` WebSocket |
| `speaker/main.js` | Receives audio from the desktop container via WebSocket (`/sound`) using Web Audio API |
| `microphone/main.js` | Captures browser microphone via AudioWorklet, streams to `/microphone` WebSocket |
| `gamepad.js` | Captures Gamepad API events and forwards them to `/gamepad` WebSocket |
| `clipboard.js` | Synchronises clipboard between browser and X11 session |
| `upload.js` | Drag-and-drop or dialog file upload to the user's home directory via `/filer` |
| `download.js` | File download from the user's home directory via `/filer` |
| `printer.js` | Lists and manages printers; integrates with CUPS via `/printerfiler` |
| `screenRecord.js` | Records the desktop session using `jsmpeg-player` (MPEG-TS over WebSocket) |
| `snapshot.js` | Captures a screenshot of the desktop via `/snapshot` |
| `shareSystem.js` | Generates a shareable desktop session link |
| `speedtest_worker.js` | Web Worker running a bandwidth test against the `/speedtest` endpoint |
| `geolocation.js` | Reads browser geolocation and forwards to the user session |
| `languages.js` | Detects browser locale, loads the matching i18n JSON from `/i18n/` |
| `tipsinfo.js` | Renders contextual SVG/HTML tips overlays |
| `broadcastsystem.js` | Listens for admin broadcast messages via WebSocket (`/broadcast`) |

---

## Internationalisation (i18n)

The i18n system uses Mustache templates. Language files are located in `i18n/` and selected at runtime based on the browser locale.

**Supported locales:**

| Locale code | File |
|-------------|------|
| `en`, `en-us`, `en-gb`, `en-en` | `en-EN.json` |
| `fr`, `fr-fr` | `fr-FR.json` |
| `ro`, `ro-ro` | `ro-RO.json` |

The default locale is `en`. Adding a new language requires creating a new `.mustache.json` file and registering it in `i18n/list.json`.

---

## Static Assets

### Icons and Images

| Directory | Content |
|-----------|---------|
| `img/top/` | ~60 toolbar SVG icons (fullscreen, logout, clipboard, printer, mic, etc.) |
| `img/settings/` | ~20 settings panel SVG icons |
| `img/welcome/` | Auth provider logos (Google, GitHub, LDAP, AD, Orange, anonymous…) |
| `img/appstore/` | App category icons (dev, doc, design, education, games, utils) |
| `img/error/` | Error state illustrations |
| `img/abcdesktop*.ico` | Favicons in multiple sizes (32, 48, 64, 128, 256 px) |

### MIME Type Icons

The `mimetypes/` directory contains over **500 SVG icons** mapping MIME types to visual representations. These are used by the file manager (`/filer`) to display file type icons.

---

## Docker Images

### Two-Image Strategy

webModules uses a **two-image build strategy** to keep the final image small:

**1. Builder image** (`Dockerfile.builder` → `oc.nginx.builder`):  
Installs Ubuntu + Node.js + `less` + build tools. This image is reused across builds to avoid reinstalling dependencies on every push.

**2. Runtime image** (`Dockerfile` → `oc.nginx`):  
Takes the builder image as base, copies the sources, runs `make prod`, then copies the resulting static files into a clean `nginx:alpine-slim` image.

### Build Arguments

| Argument | Used in | Description |
|----------|---------|-------------|
| `BASE_IMAGE` | Both | Base OS image (default: `ubuntu`) |
| `BASE_IMAGE_RELEASE` | Both | Tag of the base image (e.g., `latest`, `3.3`) |
| `NODE_MAJOR` | Both | Node.js major version (e.g., `20`, `24`) |
| `BRANCH` | Both | Git branch name (embedded in `version.json`) |
| `TARGET` | `Dockerfile` | Build mode: `dev` or `prod` |

### Supported Platforms

Both images are built for `linux/amd64` and `linux/arm64`.

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/main.yml`) runs on every push, pull request, and twice daily (cron):

1. Build and push `oc.nginx.builder:<branch>` (multi-arch) to `ghcr.io`
2. Build and push `oc.nginx:<branch>` (multi-arch, `TARGET=prod`) to `ghcr.io`
3. Run **Trivy** vulnerability scanner on the produced image (CRITICAL and HIGH severities)
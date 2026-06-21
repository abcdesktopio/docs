---
title: Architecture Overview | abcdesktop.io
description: Architectural overview of abcdesktop.io: multi-container Kubernetes user pods, pyos control plane, router, MongoDB, and the HTML5 WebSocket rendering pipeline.
keywords: architecture, Kubernetes, pyos, router, MongoDB, memcached, WebSocket, noVNC, container isolation, MVC, cloud-native desktop
tags:
  - architecture
---

# Architecture Overview

abcdesktop.io is architected around Kubernetes-native workload isolation. Every user session and every application runs as a dedicated container inside the cluster. This design enforces **Remote Browser Isolation (RBI)** and **Remote Application Isolation (RAI)**: application code executes exclusively on the server side, and only rendered pixel output is streamed to the client over an encrypted WebSocket connection. The result is a zero-client-footprint desktop platform in which the endpoint device acts purely as a display terminal.

## Pods and Services

The following flowchart illustrates all abcdesktop.io services and the interconnections between them:

``` mermaid
---
config:
  theme: redux
---
flowchart TD
    route["route"] --> desktop["user1 desktop"] & website["website"] & API["pyos"] & console["console"] & speedtest["speedtest"]
    API --> mongodb["mongodb"] & kubernetes["kubernetes"] & memcache["memcached"] & ldap["ldap"]
    n1["users"] --> route
    route@{ shape: proc}
    desktop@{ shape: procs}
    n1@{ shape: sm-circ}
     route:::Sky
     desktop:::Ash
     desktop:::Sky
     website:::Sky
     API:::Sky
     console:::Sky
     speedtest:::Aqua
     mongodb:::Aqua
     kubernetes:::Aqua
     memcache:::Aqua
     ldap:::Aqua
    classDef Ash stroke-width:1px, stroke-dasharray:none, stroke:#999999, fill:#EEEEEE, color:#000000
    classDef Peach stroke-width:1px, stroke-dasharray:none, stroke:#FBB35A, fill:#FFEFDB, color:#8F632D
    classDef Aqua stroke-width:1px, stroke-dasharray:none, stroke:#46EDC8, fill:#DEFFF8, color:#378E7A
    classDef Sky stroke-width:1px, stroke-dasharray:none, stroke:#374D7C, fill:#E2EBFF, color:#374D7C
    click route "https://github.com/abcdesktopio/route"
    click desktop "https://github.com/abcdesktopio/oc.user"
    click website "https://github.com/abcdesktopio/webmodules"
    click API "https://github.com/abcdesktopio/pyos"
    click console "https://github.com/abcdesktopio/console"
    click speedtest "https://github.com/librespeed/speedtest"
    click mongodb "https://www.mongodb.com/"
    click kubernetes "https://kubernetes.io/"
    click memcache "https://www.memcached.org/"
    click ldap "https://github.com/rroemhild/docker-test-openldap"

```

The abcdesktop.io project provides container images for `route`, `console`, `website`, `pyos`, and `user` (oc.user).

The `kubernetes`, `mongodb`, `memcached`, `speedtest`, and `ldap` components are third-party projects and are not maintained by the abcdesktop.io project. These third-party products are required dependencies for full abcdesktop.io functionality; however, the abcdesktop.io project authors are not responsible for them.

## Desktop Creation Workflow

The following sequence diagram describes the full `create desktop` workflow, from initial HTTP request through WebSocket session establishment:

``` mermaid
---
config:
  theme: redux-color
---
sequenceDiagram
    actor Alice
    Alice->> Router: GET /
    Router->>Website: GET /
    destroy Website
    Website->>Router: HTML Content
    Router->>Alice: HTML Content
    Alice->>Router: Logme in (Alice, password)
    Router->>Pyos: Logme in (Alice, password)
    Note over Router,Pyos: 1. Authentication
    Create participant LDAP
    Pyos->>LDAP: BIND LDAP_SEARCH Alice
    destroy LDAP
    LDAP->>Pyos: dn, cn, group
    Pyos->>Kubernetes: (option) Create user secrets
    Kubernetes->>Pyos: (option) Secrets created
    Pyos->>Router: User Alice JWT
    Router->>Alice: User Alice JWT
    Alice->>Router: Create Desktop (User Alice JWT)
    Note over Router,Pyos: 2. Create a desktop
    Router->>Pyos: Create Desktop (User Alice JWT)
    Pyos->>Pyos: Verify User Alice JWT
    Pyos->>Kubernetes: Create Alice POD YAML
    Kubernetes->>Pyos: POD Created
    Pyos->>Kubernetes: Is Alice Pod Ready ?
    Create participant PodAlice
    Kubernetes->>PodAlice: Are you Ready ?
    PodAlice->>Kubernetes: I'm Ready
    destroy Kubernetes
    Kubernetes->>Pyos: Alice Pod is Ready
    Pyos->>Pyos: Crypt Pod's ip address
    destroy Pyos
    Pyos->>Router: Desktop Alice JWT
    Router->>Alice: Desktop Alice JWT
    Alice->>Router: WebSocket connect(Desktop Alice JWT)
    Note over Router,PodAlice: 3. Connect websocket to Alive Pod
    Router->>Router: Verify Alice Desktop JWT
    Router->>Router: Uncrypt Alice Desktop JWT Pod ip address
    Router->>PodAlice: WebSocket connect
    PodAlice->>Router: Connected
    Router->>Alice: Connected
    Alice-->PodAlice: Established
```

The workflow consists of three distinct phases:

1. **Authentication** — The user submits credentials through the router. `pyos` authenticates against the configured provider (LDAP, LDAPS, Active Directory, or OpenID Connect) and issues a signed user JWT.
2. **Desktop provisioning** — `pyos` validates the user JWT, constructs the user pod manifest, submits it to the Kubernetes API server, and waits for the pod to reach the `Ready` state. The pod's internal IP address is then encrypted and embedded in a Desktop JWT, which is returned to the client. This prevents clients from directly addressing pod IP addresses.
3. **WebSocket session establishment** — The client presents the Desktop JWT to the router. The router verifies the JWT signature, decrypts the pod IP address, and establishes a proxied WebSocket connection between the client and the user pod. From this point forward, only rendered graphical output flows to the client — enforcing the Remote Browser Isolation and Remote Application Isolation security model.

Security considerations:
- All JWTs are signed with RSA private keys.
- Desktop JWT payloads are additionally encrypted with a separate RSA key pair, preventing clients from inspecting or tampering with pod addressing information.

## Core Services

### abcdesktop.io-Provided Services

The following services are built and maintained by the abcdesktop.io project:

| Service | Description |
|---|---|
| **router** | NGINX-based HTTP reverse proxy with Lua scripting. Routes HTTP/WebSocket requests to user pods, the website service, `pyos`, and `console`. Handles JWT validation and pod IP address decryption. |
| **website** | Static web server delivering the HTML5 frontend (HTML, JavaScript, and SVG assets) to the client browser. |
| **pyos** | The abcdesktop.io control plane. Manages authentication, user session lifecycle, and Kubernetes resource provisioning (pods, ephemeral containers, secrets, PVCs). |
| **oc.user** | The user desktop container image. Provides the X11 display server, VNC server, and all inter-container services within the user pod. Each authenticated user runs a dedicated instance of this image. |
| **console** | Web-based administration console for managing applications, users, and cluster resources. |

### Third-Party Services

The following third-party services are required or optional dependencies:

| Service | Description |
|---|---|
| **MongoDB** | Persistent data store used by `pyos` to record user login history, application registry, and desktop configuration. |
| **Memcached** | In-memory cache used by `pyos` to store transient session progress messages during the authentication and desktop provisioning phases. |
| **Speedtest** | Self-hosted HTML5 network speed test (librespeed). Used to assess the network connection quality between the client and the cluster. |
| **LDAP** | Optional directory service. A test OpenLDAP instance is provided for development and evaluation deployments. |
| **Kubernetes** | The orchestration platform. All abcdesktop.io workloads run as standard Kubernetes resources. |

## Additional Projects

- **Helm chart** — Deploy abcdesktop.io via Helm: [abcdesktop Helm chart on Artifact Hub](https://artifacthub.io/packages/helm/abcdesktop/abcdesktop)

## Component Role Details

### pyos

`pyos` is the stateless control plane of the abcdesktop.io platform. It is responsible for the full lifecycle of user sessions and application containers. Its core responsibilities include:

**Authentication:**
- OpenID Connect / OAuth 2.0 providers
- LDAP and LDAPS bind authentication
- Microsoft Active Directory (with Kerberos and NTLM support)
- Anonymous (no-auth) mode

**Kubernetes resource management (create, read, update, and delete):**
- User desktop pods and ephemeral application containers
- Kubernetes Secrets for JWT keys and user credentials
- ConfigMaps, Events, PersistentVolumeClaims, and pod logs

`pyos` requires the following namespaced Kubernetes RBAC permissions:
- `pods`, `pods/exec`, `pods/ephemeralcontainers`, `pods/log`
- `events`
- `secrets`
- `configmaps`
- `persistentvolumeclaims`

`pyos` runs under a `ServiceAccount` named `pyos-serviceaccount`, bound to the `pyos-role` Role. In specific storage configurations, you may optionally grant `pyos` full resource management access to the non-namespaced `persistentvolumes` resource.

> The `Role`, `RoleBinding`, and `ServiceAccount` manifests are embedded in the `abcdesktop.yaml` deployment file and are created automatically during installation.

### router

The `router` pod is an NGINX server extended with Lua scripting. It serves as the single ingress point for all client traffic:
- Routes HTTP requests to the `website` service, `pyos`, and `console`.
- Routes WebSocket connections to individual user desktop pods, using the decrypted pod IP address from the Desktop JWT.
- Enforces JWT signature verification on all authenticated endpoints.

### website

The `website` pod is a static web server. It delivers the abcdesktop.io HTML5 frontend assets — HTML pages, JavaScript modules, and SVG icons — to the client browser. It does not process authentication or application logic.

### MongoDB

`mongo` is used exclusively by `pyos` to persist the following data:
- User login history and session records
- Desktop background image and color configuration per user
- The installed application registry (OCI image metadata)

### memcached

`memcached` is an in-memory key-value cache used by `pyos` to store transient progress messages during the login and desktop provisioning workflow. Cache data is written and read exclusively by the control plane; it is never exposed to clients.

### oc.user

[`oc.user`](https://github.com/abcdesktopio/oc.user) is the user desktop container image. It provides:
- An X11 display server and VNC server for rendering graphical output
- A WebSocket-to-VNC bridge for transmitting rendered frames to the client browser
- Inter-container services: file transfer (filer), printing (CUPS), and audio (PulseAudio)

Each authenticated user receives a dedicated instance of `oc.user` running as a Kubernetes pod. Applications launched within the session run as additional containers (pods or ephemeral containers) alongside the `oc.user` pod, providing per-application kernel-level isolation — the foundation of Remote Application Isolation (RAI).

The image `abcdesktopio/oc.user.ubuntu:{{ abcdesktop.latest_release }}` is based on Ubuntu `24.04`. For details, see the [oc.user](https://github.com/abcdesktopio/oc.user) repository.

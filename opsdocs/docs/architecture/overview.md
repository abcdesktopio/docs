---
tags:
  - architecture
---

# Architecture overview

## Pods and services

This flowchart describes all abcdesktop services

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

The project abcdesktop provides container images for `route`, `console`, `website`, `pyos`, and `user`

The projects `kubernetes`, `mongodb`, `memcached`, `speedtest` and `ldap` are not part of the abcdesktop project.
Items on this page refer to third-party products or projects that provide functionality required by abcdesktop.io. The abcdesktop project authors are not responsible for those third-party products or projects.

## Create desktop workflow

This workflow describes the `create desktop` process

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

1. The user logs in and receives a user JWT.
2. A user pod is created and a Desktop JWT is issued.
3. The user connects to their own pod.

	- All JWTs are signed with RSA keys.
	- All desktop JWT payloads are encrypted with a separate RSA key pair.

## Services infrastructure

The service infrastructure is based on:

- Router (nginx with Lua scripting) [router](https://github.com/abcdesktopio/router)
- Website service [webmodules](https://github.com/abcdesktopio/webmodules)
- Database service (third-party product) [MongoDB](https://github.com/abcdesktopio/mongo)
- Memcached service (third-party project) [Memcached](https://github.com/abcdesktopio/oc.memcached)
- pyos Core service (abcdesktop control plane) [pyos](https://github.com/abcdesktopio/pyos)
- User pod [user](https://github.com/abcdesktopio/oc.user)

## Additional services

- Console service (abcdesktop admin console) [console](https://github.com/abcdesktopio/console)
- Speedtest service (self-hosted HTML5 speed test, third-party project) [librespeed](https://github.com/librespeed/speedtest)
- LDAP service (optional, third-party project) [rroemhild/docker-test-openldap](https://github.com/rroemhild/docker-test-openldap)


## Additional Projects

- Helm charts (install helm chart) [helm chart](https://artifacthub.io/packages/helm/abcdesktop/abcdesktop)


## Roles summary

### pyos

`pyos` is the core abcdesktop service and acts as a control plane. `pyos` is a stateless service; its roles are:

- Authenticate user on authenticate providers
  - OpenID Provider
  - LDAP and LDAPS
  - Active Directory
  - Anonymous (no auth)
- Create/Read/Update/Delete user's Pod in Kubernetes
- Create/Read/Update/Delete user's applications as `ephemeral container` or as `pod`

> When a new user is authenticated, a dedicated user pod is created.
> When the user starts an application (like LibreOffice for example) a dedicated container is created. It can be a `pod` or an `ephemeral container`

pyos requires `rbac.authorization.k8s.io` roles to perform `CRUD` operations on the following namespaced resources:
- 'pods', 'pods/exec', 'pods/ephemeralcontainers', 'pods/log'
- 'events'
- 'secrets'
- 'configmaps'
- 'persistentvolumeclaims'

pyos runs as a `ServiceAccount` named `pyos-serviceaccount`, with `pyos-role`.
Optionally, you can also grant pyos `CRUD` access to `['persistentvolumes']` resources in particular cases. Note that `persistentvolumes` are not namespaced.

The `Role`, `RoleBinding`, and `ServiceAccount` are embedded in the `abcdesktop.yaml` file.



### router

The `router` pod acts as an HTTP routing web server. It routes HTTP requests to user pods, the `website` service, `pyos`, and `console`.

### website

The `website` pod acts as a web server and delivers HTML, JavaScript, and SVG files.

### mongo database

`mongo` is used by `pyos` to store persistent information.
The stored data includes:

- User login history
- Image and background color configuration per desktop
- Installed applications


### memcached

`memcache` stores progress message text during the login process. Cache data is written and read exclusively by the control plane.


### oc.user

[`oc.user`](https://github.com/abcdesktopio/oc.user) is the name of the user's container image. `oc.user` runs the X11 graphical service. `oc.user` is based on the Ubuntu distribution.

* The image `abcdesktopio/oc.user.ubuntu:{{ abcdesktop.latest_release }}` is based on Ubuntu `24.04`. For more details, see the [oc.user](https://github.com/abcdesktopio/oc.user) image repository.


### applications

All applications are `ephemeral containers` or `pods`, and share a graphical socket ( `unix` or `tcp` ) with the user's pod.


# Architecture in docker mode

## Pods 

This flowchart describes the all abcdesktop services

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

## Create desktop workflow

This workflow describes the `create desktop` process 

``` mermaid
---
config:
  theme: redux-color
---
sequenceDiagram
    actor Alice
    Alice-- HTTPS GET / -->>Router: HTTPS GET /
    Router->>Website: HTTP GET /
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
    Pyos->>Pyos: Crypt Pop ip address
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

1. User login, get a user JWT
2. Create a user POD and get a Desktop JWT
3. User is connecting to his own POD

	- All JWT are signed with RSA keys. 
	- All desktop's JWT payload are encrypted with another RSA keys

## Services infrastructure

The service infrastructure is based on :

- Router nginx with lua script [Nginx container](/core/nginx)
- Website service [webmodules](https://github.com/abcdesktopio/webmodules)
- Database service (external projet) [MongoDB](/core/mongodb/)
- Memcached service (external projet) [Memcached](/core/memcached/)
- Pyos Core service (abcdesktop control plane) [Pyos](/core/pyos/)
- Pod user [user](/core/user)

## Additional services

- Console service (abcdesktop admin console) [Pyos](/core/pyos/)
- Speedtest service (speedtest service, self-hosted speed test for HTML5, external projet) [librespeed](https://github.com/librespeed/speedtest)
- LDAP service (for demo, optional) [rroemhild/docker-test-openldap](https://github.com/rroemhild/docker-test-openldap]
  

## Additional projet

- Helm charts (install helm chart) [helm chart](https://artifacthub.io/packages/helm/abcdesktop/abcdesktop)


## Roles summary

### pyos

`pyos` is the core abcdesktop service act as a control plane. Pyos is a stateless services, Pyos's roles are :

- Authenticate user on authenticate providers
 - OAuth 2.0 Provider : Google, Facebook, Orange
 - LDAP and LDAPS
 - Active Directory
 - Anonymous (no auth)
- Start/Stop user's Pod in Kubernetes 
- Start/Stop user's applications as `ephemeral container` or as `pod`

> When a new user is authenticated, a dedicated user pod is created.
> When the user starts an application (like LibreOffice for example) a dedicated container is created. It can be a `pod` or an `ephemeral container`


### router

`router` pod act as a `http router` web server. It routes HTTP requets to `user's pods`, `web site`, or `pyos`.

### website

`website` pod act as web server and delivers `html`, `javascript`, `svg` files. 

### mongo database

`mongo` is used by pyos to store informations. 
The informations are :

- User logins history
- Images and background colors configuration per desktop
- Installed applications 


### memcached

`memcache` stores progress text message information during login process. `memcache` datas are set and get only by the control plane.


### oc.user

[`oc.user`](https://github.com/abcdesktopio/oc.user) is the name of the user's container image. `oc.user` runs the X11 graphical service. `oc.user` is based on ubuntu distribution. 

* The image `abcdesktopio/oc.user.ubuntu:4.1` is based on `ubuntu` distribution `24.04`. Get more details about [oc.user](https://github.com/abcdesktopio/oc.user) image.


### applications

All applications are `ephemeral containers` or `pods`, and share a graphical socket ( `unix` or `tcp` ) with the user's pod. 

---
tags:
  - mongodb
---

# MongoDB

## Overview

In abcdesktop, MongoDB serves as the **primary database** for the control plane (`pyos`). It stores all persistent application data: user profiles, login history, application inventory, desktop session states, and fail2ban data.

MongoDB is deployed as a **ReplicaSet** (name: `rs0`), with **authentication enabled** and inter-member communication secured by a **keyfile**.

![](./drawio/abcdesktop-architecture.drawio)

---

## Kubernetes Resource Architecture

The following diagram shows all Kubernetes resources involved in the MongoDB deployment:

![](./drawio/mongodb-statefulset-overview.drawio)

---

## MongoDB-related Kubernetes Resources

=== "Secret `secret-mongodb`"

    This `Opaque` secret holds **all credentials** required for MongoDB initialization and access.

    | Key | Value (from manifest) | Purpose |
    |---|---|---|
    | `MONGO_ROOT_USERNAME` | `root` | MongoDB superuser |
    | `MONGO_ROOT_PASSWORD` | `Oge5iQw9dGBvRDd` | Root password |
    | `MONGO_USERNAME` | `pyos` | Application user |
    | `MONGO_PASSWORD` | `Az4MeYWUjZDg4Zjhk` | Application user password |
    | `MONGO_USERS_LIST` | `pyos:readWrite:Az4MeYWUjZDg4Zjhk` | `user:role:password` list |
    | `MONGO_DBS_LIST` | `image,fail2ban,loginHistory,applications,profiles,desktop` | Databases to initialize |
    | `MONGODB_URL` | `mongodb://pyos:...@mongodb` | Connection URL for pyos |

    > ⚠️ **Security note**: passwords are stored in plaintext in the manifest (`stringData`). In production, a secrets manager (Vault, Sealed Secrets, External Secrets Operator, etc.) is strongly recommended.

    The secret is mounted inside the MongoDB pod with the following path mapping:

    ![](./drawio/secret-mongodb-mounts.drawio)

=== "ConfigMap `configmap-mongodb-scripts`"

    This ConfigMap contains **4 key files** injected into the pod:

    ??? note "`mongod.conf` — MongoDB daemon configuration"
        ```yaml
        net:
        bindIp: 0.0.0.0
        port: 27017
        replication:
        replSetName: rs0
        security:
        authorization: enabled
        keyFile: /etc/mongodb/mongod.keyfile
        storage:
        dbPath: /data/db
        ```

        Notable settings:

        - Listens on all interfaces (`0.0.0.0:27017`)
        - ReplicaSet named `rs0`
        - Authentication enabled, keyfile required

    ??? note "`init-container.sh` — Configuration file preparation"
        Script executed by the **InitContainer** before MongoDB starts:

        - Copies `mongod.conf` and `mongod.keyfile` to `/work/config`
        - Applies required permissions (`chmod 400` on the keyfile)
        - Creates and prepares `/data/db` and `/var/log/mongodb`
        - Ensures the `mongodb` OS user owns all relevant directories

    ??? note "`init.js` — Database and user initialization"
        JavaScript script executed automatically by MongoDB on **first startup** (via `/docker-entrypoint-initdb.d/`):

        1. Reads the database list (`MONGO_DBS_LIST`) and user list (`MONGO_USERS_LIST`) from mounted secret files
        2. Authenticates as root against the `admin` database
        3. For each listed database, creates the corresponding users with their defined roles
        4. Handles duplicates gracefully (idempotent: does not fail if the user already exists)

    ??? note "`init-replica.sh` — ReplicaSet initialization"
        Bash script executed by the **`replica-manager` sidecar**, only on pod `mongodb-od-0`:

        1. Builds the member list dynamically based on the configured replica count
        2. Waits until all members respond to ping
        3. Checks whether the ReplicaSet is already initialized
        4. If not: calls `rs.initiate()` with the dynamically built configuration
        5. Waits for a PRIMARY to be elected
        6. Displays the final ReplicaSet state

=== "StatefulSet `mongodb-od`"

    The StatefulSet is the core of the deployment, configured with **1 replica** (scalable).

    ```mermaid
    sequenceDiagram
        participant K8s as Kubernetes Scheduler
        participant IC as InitContainer<br/>prepare-config
        participant MDB as Container<br/>mongodb
        participant RM as Sidecar<br/>replica-manager

        K8s->>IC: Start InitContainer
        IC->>IC: Copy mongod.conf + keyfile
        IC->>IC: chmod 400 keyfile
        IC->>IC: Prepare /data/db
        IC-->>K8s: Done (exit 0)

        K8s->>MDB: Start mongodb container
        MDB->>MDB: Launch mongod --config=/etc/mongodb/mongod.conf
        MDB->>MDB: Execute /docker-entrypoint-initdb.d/init.js
        Note over MDB: Creates users & databases

        K8s->>RM: Start replica-manager sidecar
        RM->>RM: Check hostname == mongodb-od-0
        RM->>MDB: Ping (wait for availability)
        RM->>MDB: rs.status() — check RS state
        RM->>MDB: rs.initiate({_id:'rs0', members:[...]})
        RM->>MDB: Wait for PRIMARY election
        RM-->>RM: sleep infinity (stay alive)
    ```

    !!! note Container image
        ```
        ghcr.io/abcdesktopio/mongo:safe8.0
        ```

        Custom image based on MongoDB 8.0, hosted on GitHub Container Registry. The `safe` tag indicates a hardened image.

=== "Service `mongodb`"

    The manifest uses a **headless Service** (implicit for a StatefulSet with `serviceName: mongodb`), making each pod individually addressable via DNS:

    ```
    mongodb-od-0.mongodb.abcdesktop.svc.cluster.local:27017
    ```

    `pyos` connects using the simplified URL defined in the secret:
    ```
    mongodb://pyos:Az4MeYWUjZDg4Zjhk@mongodb
    ```

---

## MongoDB Startup Sequence

![](./drawio/mongodb-startup.drawio)

---

## Security and Authentication

![](./drawio/mongodb-authentication.drawio)

**Security model summary:**

- **Root**: used only during initialization (`init.js`, `init-replica.sh`). Credentials are read from files (via `*_FILE` env vars), never passed as plaintext environment variables to the main container.
- **pyos**: application user with `readWrite` role on all business databases.
- **Keyfile**: separate Kubernetes secret (`abcdesktop-mongod-keyfile`), mounted read-only with `chmod 400`. Required for intra-ReplicaSet communication.

---

## Databases and Users

At initialization, `init.js` creates the following structure:

| Database | Likely role in abcdesktop |
|---|---|
| `image` | Catalogue of available application images |
| `fail2ban` | IP blocking after failed authentication attempts |
| `loginHistory` | User login history |
| `applications` | Published application metadata |
| `profiles` | User profiles and preferences |
| `desktop` | Active desktop session states |

---

## Connection Flow from pyos

```mermaid
sequenceDiagram
    participant PyOS as pyos-od
    participant SVC as Service mongodb<br/>(ClusterIP)
    participant MDB0 as mongodb-od-0<br/>(PRIMARY)

    PyOS->>SVC: Connect via MONGODB_URL\nmongodb://pyos:...@mongodb
    SVC->>MDB0: Forward port 27017
    MDB0->>MDB0: Authenticate pyos on each DB
    MDB0-->>PyOS: Connection established (readWrite)

    PyOS->>MDB0: Read/write on image, profiles, desktop...
```

The connection URL is injected into `pyos` via the `secret-mongodb` secret, key `MONGODB_URL`.

---

## Volumes and Data Persistence

![](./drawio/mongodb-volumes-mounts.drawio)

!!! warning
    ⚠️ **Critical point**: the `data` volume (mounting `/data/db`) is an **`emptyDir`**. This means **MongoDB data is not persisted** across pod restarts. In production, this volume must be replaced with a `PersistentVolumeClaim` (PVC) backed by an appropriate StorageClass.

---

## Allocated Resources

=== "Container `mongodb`"

    | Resource | Request | Limit |
    |---|---|---|
    | CPU | 100m | 500m |
    | Memory | 128Mi | 512Mi |

=== "Sidecar `replica-manager`"

    | Resource | Request | Limit |
    |---|---|---|
    | CPU | 100m | 500m |
    | Memory | 128Mi | 512Mi |

---

## Observations and Recommendations

=== "🔴 Critical"

    - **Non-persistent data**: `/data/db` is an `emptyDir`. Any pod loss causes a total loss of all MongoDB data. Replace with a PVC backed by a suitable StorageClass.
    - **Plaintext passwords in the manifest**: credentials are defined in `stringData`. Use Sealed Secrets, Vault, or the External Secrets Operator in production.

=== "🟡 Important"

    - **Single replica**: `replicas: 1` with a single-member ReplicaSet provides no high availability. Scale to 3 members for production environments.
    - **`imagePullPolicy: Always`**: forces an image pull on every pod start, which can slow restarts and requires permanent network access to `ghcr.io`.

=== "🟢 Good practices observed"

    - Credentials are read from files (via `*_FILE` env vars), never passed as plaintext env vars to the main container.
    - `init-replica.sh` is idempotent: can be safely re-executed.
    - `init.js` is idempotent: handles duplicate user errors gracefully.
    - Clear role separation: root for initialization, `pyos` for the application layer.
    - Keyfile used to secure intra-ReplicaSet communication.
    - ReadinessProbe configured on port 27017.

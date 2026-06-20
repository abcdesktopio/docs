---
tags:
  - faq
  - mongodb
---

# MongoDB

## How to Increase the MongoDB Replica Count

### With a Helm Installation

To change the replica count for MongoDB using the Helm installation, extract the values file from the Helm chart if you have not already done so:

```bash
helm show values abcdesktop/abcdesktop  > abcdesktop-values.yaml
```

Edit the `mongo` section and update the `replicaCount` key to the desired value:

```yaml
mongo:
  enabled: true
  keysgenerator:
    image: ghcr.io/abcdesktopio/keysgenerator
    tag: {{ abcdesktop.latest_release }}
    mongodkeylength: 756
  # data:
  #   initContainerScriptPath: "data/mongo/init-container.sh"
  #   configFilePath: "data/mongo/etc/mongodb/mongod.conf"
  #   initScriptPath: "data/mongo/docker-entrypoint-initdb.d/init.js"
  #   initReplicaScriptPath: "data/mongo/docker-entrypoint-initdb.d/init-replica.sh"
  image:
    repository: ghcr.io/abcdesktopio/mongo
    tag: "safe8.0"
    pullPolicy: Always
  replicaCount: 3
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 128Mi
  # Persistence - MongoDB data storage configuration
  persistence:
    # enabled: true for persistent volume, false for non-persistent volume (emptyDir)
    enabled: false
    # Storage class to use (leave empty for default class)
    storageClass: ""
    # Persistent volume size
    size: 8Gi
    # Mount path in the container (do not change)
    mountPath: /data/db
```

Then apply the updated values:

```bash
NAMESPACE=abcdesktop
helm upgrade --install my-abcdesktop abcdesktop/abcdesktop \
    --version {{ abcdesktop.latest_release }} \
    --create-namespace \
    -n ${NAMESPACE} \
    -f abcdesktop-values.yaml
```
where `NAMESPACE` and `my-abcdesktop` are your deployment namespace and release name.

### With a Scripted Installation

- Open your [abcdesktop.yaml](https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-{{ abcdesktop.latest_release }}.yaml) file and locate the `StatefulSet` named `mongodb-od`:


```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
 name: mongodb-od
```


- In the spec of the `StatefulSet` named `mongodb-od`, update the `replicas` count:


```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb-od
  labels:
    run: mongodb-od
    type: database
    abcdesktop/role: mongodb
    netpol/mongodb: 'true'
    netpol/dns: 'true'
spec:
  serviceName: mongodb
  replicas: 3
```

- In the `name: replica-manager` container definition, update the `REPLICAS` environment variable to match the same value:

```yaml
 env:
   - name: NAMESPACE
     valueFrom:
       fieldRef:
         fieldPath: metadata.namespace
   - name: SERVICE
     value: mongodb
   - name: STATEFULSET_NAME
     value: mongodb-od
   - name: REPLICAS
     value: "3"
```

- Apply your changes to the `abcdesktop` namespace:

```
NAMESPACE=abcdesktop
kubectl apply -f abcdesktop.yaml -n $NAMESPACE
```

- Verify the number of running replicas:

```bash
kubectl get statefulset -l run=mongodb-od -n abcdesktop
```

The output should show all replicas in the `READY` state:

```
NAME         READY   AGE
mongodb-od   3/3     18h
```

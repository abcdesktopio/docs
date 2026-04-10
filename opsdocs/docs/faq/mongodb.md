---
tags:
  - faq
  - mongodb
  - JFV
  - AD
---

# Mongodb

## How to increase the `mongodb` number of `replicats` ?

### With helm installation

To change the replicat number of mongodb using the helm installation, extract the values file from helm if not already done:

```bash
helm show values abcdesktop/abcdesktop  > abcdesktop-values.yaml
```

Then edit the mongo section to update the `replicaCount` key to the wanted value.

```yaml
mongo:
  enabled: true
  keysgenerator:
    image: ghcr.io/abcdesktopio/keysgenerator
    tag: 4.3
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
and apply it:

```bash
NAMESPACE=abcdesktop
helm upgrade --install my-abcdesktop abcdesktop/abcdesktop \
    --version 4.4 \
    --create-namespace \
    -n ${NAMESPACE} \
    -f abcdesktop-values.yaml
```
where `NAMESPACE` and `my-abcdesktop` are your deployment namespace and instance name.

### With a scripted installation

- Open your [abcdesktop.yaml](https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-{{ abcdesktop.latest_release }}.yaml) file and look for the `StatefulSet` mongodb-od


```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
 name: mongodb-od
```


- In the specs of the the `StatefulSet` mongodb-od, change the number of the `replicas`


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

- In the `name: replica-manager`, update the variable `REPLICAS` with the same value

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

- Apply your changes to the abcdesktop namespace

```
NAMESPACE=abcdesktop
kubectl apply -f abcdesktop.yaml -n $NAMESPACE
```

- Check the number of `replicas`

```bash
kubectl get statefulset -l run=mongodb-od -n abcdesktop
```

You should read on stdout

```
NAME         READY   AGE
mongodb-od   3/3     18h
```











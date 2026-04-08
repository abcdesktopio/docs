---
tags:
  - faq
  - mongodb
---

# Mongodb


## How to increase the `mongodb` number of `replicats`

- Open your [abcdesktop.yaml](https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-{{ abcdesktop.latest_release }}.yaml) file and look for the `StatefulSet` mongodb-od


```
apiVersion: apps/v1 
kind: StatefulSet
metadata:
 name: mongodb-od
```


- In the specs of the the `StatefulSet` mongodb-od, change the number of the `replicas` 


```
apiVersion: apps/v1 
kind: StatefulSet
metadata:
  name: mongodb-od
  labels:
    run: mongodb-od
    type: database
    abcdesktop/role: mongodb
    netpol/mongodb: 'true'
spec:
  serviceName: mongodb
  replicas: 3
```

- In the `name: replica-manager`, update the variable `REPLICAS` with the same value

```
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

```
kubectl get statefulset -l run=mongodb-od -n abcdesktop
```

You should read on stdout

```
NAME         READY   AGE
mongodb-od   3/3     18h
```











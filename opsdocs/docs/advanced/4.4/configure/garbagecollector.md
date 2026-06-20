# Garbage Collector Configuration

## Overview

The garbage collector is a maintenance service that terminates user desktop pods that have been idle for longer than a configurable duration. It is invoked via an HTTP request to the `pyos` API endpoint `/API/manager/garbagecollector`.

## API Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `expirein` | integer (seconds) | Yes | — | Sessions idle for longer than this duration are candidates for deletion. |
| `force` | boolean | No | `False` | If `True`, deletes sessions regardless of current connection status. If `False`, active sessions are preserved. |
| `nodename` | string | No | `None` | Restricts deletion to pods running on the specified node. Useful during node maintenance or `kubectl drain` operations. |

The endpoint returns a JSON array listing all deleted pod names.

> **Warning:** Calling `/API/manager/garbagecollector?expirein=0&force=true` immediately terminates **all** active user sessions.

## Deploying the Garbage Collector as a Kubernetes CronJob

The recommended deployment pattern is a Kubernetes `CronJob` that invokes the garbage collector API on a scheduled interval.

Create a file named `cronjob.yaml`:

```
apiVersion: batch/v1
kind: CronJob
metadata:
  name: abcdesktop-cleaner
spec:
  schedule: "*/5 * * * *"
  failedJobsHistoryLimit: 2
  jobTemplate:
    spec:
      activeDeadlineSeconds: 60
      backoffLimit: 0
      template:
        metadata:
          labels:
            name: abcdesktop-cleaner
            netpol/pyos: 'true'
            netpol/dns: 'true'
        spec:
          containers:
          - name: abcdesktop-cleaner
            image: busybox
            args:
            - /bin/sh
            - -c
            - wget -q -t 3 -O- "http://${PYOS_ADDR}:${PYOS_PORT}/API/manager/garbagecollector?expirein=${EXPIREIN}&force=${FORCE}"
            env:
            - name: PYOS_ADDR
              value: 'pyos.abcdesktop.svc.cluster.local'
            - name: PYOS_PORT
              value: '8000'
            - name: EXPIREIN
              value: '900'
            - name: FORCE
              value: 'false'
          restartPolicy: OnFailure
          dnsPolicy: ClusterFirst
```

### Default Values

- **Schedule:** `*/5 * * * *` — runs every five minutes.
- **`expirein`:** `900` seconds (15 minutes) — sessions idle for longer than 900 seconds are candidates for deletion.
- **`force`:** `false` — active sessions are never deleted.

### Deletion Logic

| Condition | `force` | Result |
|---|---|---|
| User is not connected AND idle time > `expirein` | any | Pod is deleted |
| User is connected AND idle time > `expirein` | `true` | Pod is deleted |
| User is connected AND idle time > `expirein` | `false` | Pod is preserved |
| Idle time ≤ `expirein` | any | No action |

## Applying the CronJob

Deploy the CronJob to your namespace:

```
kubectl apply -f cronjob.yaml -n abcdesktop
```

Expected output:

```
cronjob.batch/abcdesktop-cleaner configured
```

## Monitoring CronJob Execution

After a few minutes, verify the job execution history:

```
kubectl get jobs -n abcdesktop
```

Expected output:

```
NAME                          STATUS     COMPLETIONS   DURATION   AGE
abcdesktop-cleaner-29350635   Complete   1/1           5s         13m
abcdesktop-cleaner-29350640   Complete   1/1           5s         8m56s
abcdesktop-cleaner-29350645   Complete   1/1           5s         3m56s
```

List completed cleaner pods:

```
kubectl get pods -n abcdesktop
```

Expected output:

```
NAME                                READY   STATUS      RESTARTS   AGE    IP           NODE       NOMINATED NODE   READINESS GATES
abcdesktop-cleaner-29350665-lnk6g   0/1     Completed   0          12m    10.0.2.199   abc3ws03   <none>           <none>
abcdesktop-cleaner-29350670-c8dtj   0/1     Completed   0          7m9s   10.0.2.252   abc3ws03   <none>           <none>
abcdesktop-cleaner-29350675-hlj8z   0/1     Completed   0          2m9s   10.0.2.72    abc3ws03   <none>           <none>
[...]
```

The garbage collector CronJob is now running every five minutes and automatically reclaiming idle desktop pod resources.

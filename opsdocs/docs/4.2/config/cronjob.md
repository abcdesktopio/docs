# Configure the garbage collector

## Create a `cronjob`


Call the garbagecollector api


- Create a yaml manifest file named `cronjob.yaml`

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

The default values are  

- `schedule`: `*/5 * * * *` to run each five minutes

- `env:`

```
- name: "EXPIREIN'
  value: '900'
```

`EXPIREIN` is a value in seconds.
If the time of the last login on the desktop is more than `EXPIREIN` then a desktop can be deleted or not. 
The time of the last login starts when the user logs in.
abcdesktop calcs the duration between the current time and the last login time on the desktop.
- If the user is NOT connected to the desktop and if the duration time is more than `EXPIREIN`, then the desktop is deleted.
- If the user is connected and if the duration time is is more than `EXPIREIN` and if `FORCE` is `true`, then the desktop is deleted.
- If the user is connected and if the duration time is more than `EXPIREIN` and if `FORCE` is `false`, then the desktop is NOT deleted.

```
- name: "FORCE'
  value: 'false'
```

`FORCE` to delete the user's pod even if the user is connected. `false` is the default value, if a user is connected to his desktop then the `garbagecollector` keep this desktop running. By setting `FORCE` to `true`, the desktop will be deleted every time the `EXPIREIN` value is reached, regardless of the connection status.


## Apply your `cronjob`

Run the `kubectl` command line to apply your manifest file in you namespace.

```
kubectl apply -f cronjob.yaml -n abcdesktop
```

The output looks similar to the following:


```
cronjob.batch/abcdesktop-cleaner configured
```

## Check the jobs status

After few minutes, you can check the job status 

Run the `kubectl` command line to get your jobs in you namespace.


```
kubectl get jobs -n abcdesktop
```

The output looks similar to the following:

```
NAME                          STATUS     COMPLETIONS   DURATION   AGE
abcdesktop-cleaner-29350635   Complete   1/1           5s         13m
abcdesktop-cleaner-29350640   Complete   1/1           5s         8m56s
abcdesktop-cleaner-29350645   Complete   1/1           5s         3m56s
```

You can also get your pods in your namespace

```
kubectl get pods -n abcdesktop
```

The output looks similar to the following:

```
NAME                                READY   STATUS      RESTARTS   AGE    IP           NODE       NOMINATED NODE   READINESS GATES
abcdesktop-cleaner-29350665-lnk6g   0/1     Completed   0          12m    10.0.2.199   abc3ws03   <none>           <none>
abcdesktop-cleaner-29350670-c8dtj   0/1     Completed   0          7m9s   10.0.2.252   abc3ws03   <none>           <none>
abcdesktop-cleaner-29350675-hlj8z   0/1     Completed   0          2m9s   10.0.2.72    abc3ws03   <none>           <none>
[...]
```


Great, you add a `garbagecollector` using a kubernetes `cronjob` in your namespace.
Each five minutes the `garbagecollector` checks if desktop pod have to de deleted.
The desktop pod is checked for deletion by the garbage collector every five minutes.

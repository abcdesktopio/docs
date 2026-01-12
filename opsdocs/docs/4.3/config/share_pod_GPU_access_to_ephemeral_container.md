
# Troubleshooting get nvidia GPU access to ephemeral container with CDI enabled


abcdesktop uses `ephemeral container` or `pod` as applications. nvidia adds support for [Container Device Interface](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html). 



## installed packages


nvidia-container-toolkit=1.18.1-1  

```
libnvidia-container-tools                        1.18.1-1                                amd64        NVIDIA container runtime library (command-line tools)
nvidia-container-toolkit                         1.18.1-1                                amd64        NVIDIA Container toolkit
nvidia-container-toolkit-base                    1.18.1-1                                amd64        NVIDIA Container Toolkit Base
```


nvidia/gpu-operator version=v25.10.1

```bash
helm install --wait --generate-name      -n gpu-operator --create-namespace      nvidia/gpu-operator      --version=v25.10.1      --set driver.enabled=false --set toolkit.enabled=false
```

> Note: in this case nvidia driver and the nvidia toolkit is already installed


cdi enabled

```bash
kubectl patch clusterpolicies.nvidia.com/cluster-policy --type='json' -p='[{"op": "replace", "path": "/spec/cdi/enabled", "value":true}]'
```

Read the `clusterpolicies.nvidia.com/cluster-policy`

```bash
kubectl get clusterpolicies.nvidia.com/cluster-policy -o json | jq ."spec.cdi"
```

You should get 

```json
{
  "default": false,
  "enabled": true
}
```


## Troubleshooting with a simple-pod with `nvidia.com/gpu`


- Create a file simple-pod.yaml

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: simple-pod
spec:
  containers:
    - name: cuda-container
      image: ubuntu
      command: ["sh", "-c", "sleep 3600"]
      resources:
        limits:
          nvidia.com/gpu: 1
        requests:
          nvidia.com/gpu: 1
  restartPolicy: Never
```

- Create `simple-pod`

```bash
kubectl create -f simple-pod.yaml 
pod/simple-pod created
```

- Exec command in `simple-pod`

List devices

```bash
kubectl exec -it simple-pod -- ls -la /dev/dri
```

The devices `/dev/dri/card1` and `/dev/dri/renderD128` are listed

```
total 0
drwxr-xr-x 2 root root       80 Jan 12 17:16 .
drwxr-xr-x 6 root root      480 Jan 12 17:16 ..
crw-rw---- 1 root root 226,   1 Jan 12 17:16 card1
crw-rw---- 1 root root 226, 128 Jan 12 17:16 renderD128
```

Get GPU UUID from `nvidia-smi` command line

```bash
kubectl exec -it simple-pod -- nvidia-smi -L
```

It returns in this my own case

```
GPU 0: Quadro M620 (UUID: GPU-b5aebea9-8a25-fb21-631b-7e5da5a60ccb)
```


### Create an ephemeral container inside `simple-pod`

Create a yaml file `custom-profile-nvidia-gpu.yaml` and replace `GPU-b5aebea9-8a25-fb21-631b-7e5da5a60ccb` by your own gpu uuid 

```yaml
env:
- name: NVIDIA_VISIBLE_DEVICES
  value: GPU-b5aebea9-8a25-fb21-631b-7e5da5a60ccb
- name: NVIDIA_DRIVER_CAPABILITIES
  value: all
``` 

Run a debug ephemeral container in `simple-pod`

```bash
kubectl debug -it simple-pod --image=ubuntu --target=cuda-container --profile=general --custom=custom-profile-nvidia-gpu.yaml -- nvidia-smi -L
```

> This command failed, `/usr/bin/nvidia-smi` doesn't exist


Run a debug ephemeral container in `simple-pod`

```bash
kubectl debug -it simple-pod --image=ubuntu --target=cuda-container --profile=general --custom=custom-profile-nvidia-gpu.yaml -- ls -la /dev
```

```
Targeting container "cuda-container". If you don't see processes from this container it may be because the container runtime doesn't support this feature.
Defaulting debug container name to debugger-nzrlt.
total 4
drwxr-xr-x 5 root root    380 Jan 12 17:47 .
drwxr-xr-x 1 root root   4096 Jan 12 17:47 ..
crw--w---- 1 root tty  136, 0 Jan 12 17:47 console
lrwxrwxrwx 1 root root     11 Jan 12 17:47 core -> /proc/kcore
lrwxrwxrwx 1 root root     13 Jan 12 17:47 fd -> /proc/self/fd
crw-rw-rw- 1 root root   1, 7 Jan 12 17:47 full
drwxrwxrwt 2 root root     40 Jan 12 17:16 mqueue
crw-rw-rw- 1 root root   1, 3 Jan 12 17:47 null
lrwxrwxrwx 1 root root      8 Jan 12 17:47 ptmx -> pts/ptmx
drwxr-xr-x 2 root root      0 Jan 12 17:47 pts
crw-rw-rw- 1 root root   1, 8 Jan 12 17:47 random
drwxrwxrwt 2 root root     40 Jan 12 17:16 shm
lrwxrwxrwx 1 root root     15 Jan 12 17:47 stderr -> /proc/self/fd/2
lrwxrwxrwx 1 root root     15 Jan 12 17:47 stdin -> /proc/self/fd/0
lrwxrwxrwx 1 root root     15 Jan 12 17:47 stdout -> /proc/self/fd/1
-rw-rw-rw- 1 root root      0 Jan 12 17:47 termination-log
crw-rw-rw- 1 root root   5, 0 Jan 12 17:47 tty
crw-rw-rw- 1 root root   1, 9 Jan 12 17:47 urandom
crw-rw-rw- 1 root root   1, 5 Jan 12 17:47 zero
```

> There is no `/dev/dri` and no `nvidia` devices for this ephemeral container
> This is bad 


### Delete `simple-pod`

```bash
kubectl delete -f simple-pod.yaml
```

```
pod "simple-pod" deleted from default namespace
```



## Create a nvidia-pod with `nvidia.com/gpu` and `runtimeClassName`

- Create a file `nvidia-pod.yaml`


```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nvidia-pod
spec:
  runtimeClassName: nvidia
  containers:
    - name: cuda-container
      image: ubuntu
      command: ["sh", "-c", "sleep 3600"]
      resources:
        limits:
          nvidia.com/gpu: 1
        requests:
          nvidia.com/gpu: 1
  restartPolicy: Never
```

> `runtimeClassName` is set to `nvidia`
>  to read all classname `kubectl get runtimeclasses` returns by default `nvidia`, `nvidia-cdi`, `nvidia-legacy` (if CDI support is enabled)


- Create `nvidia-pod`

```
kubectl create -f nvidia-pod.yaml 
pod/nvidia-pod created
```

- Exec command in `nvidia-pod`

```bash
kubectl exec -it nvidia-pod -- ls -la /dev/dri
```

The devices `/dev/dri/card1` and `/dev/dri/renderD128` are listed

```
total 0
drwxr-xr-x 2 root root       80 Jan 12 17:57 .
drwxr-xr-x 6 root root      480 Jan 12 17:57 ..
crw-rw---- 1 root root 226,   1 Jan 12 17:57 card1
crw-rw---- 1 root root 226, 128 Jan 12 17:57 renderD128
```

Get GPU UUID from `nvidia-smi` command line

```
kubectl exec -it nvidia-pod -- nvidia-smi -L
```

It returns in this my own case

```
GPU 0: Quadro M620 (UUID: GPU-b5aebea9-8a25-fb21-631b-7e5da5a60ccb)
```


### Create an ephemeral container inside `simple-pod`

Create a yaml file `custom-profile-nvidia-gpu.yaml` and replace `GPU-b5aebea9-8a25-fb21-631b-7e5da5a60ccb` by your own gpu uuid 

```
env:
- name: NVIDIA_VISIBLE_DEVICES
  value: GPU-b5aebea9-8a25-fb21-631b-7e5da5a60ccb
- name: NVIDIA_DRIVER_CAPABILITIES
  value: all
``` 

Run a debug ephemeral container in `nvidia-pod`

```
kubectl debug -it nvidia-pod --image=ubuntu --target=cuda-container --profile=general --custom=custom-profile-nvidia-gpu.yaml -- nvidia-smi -L
```

This command `nvidia-smi -L` works, and returns the GPU UUID

```
Targeting container "cuda-container". If you don't see processes from this container it may be because the container runtime doesn't support this feature.
Defaulting debug container name to debugger-hm826.
GPU 0: Quadro M620 (UUID: GPU-b5aebea9-8a25-fb21-631b-7e5da5a60ccb)
```


Run a debug ephemeral container in `nvidia-pod`

```
kubectl debug -it nvidia-pod --image=ubuntu --target=cuda-container --profile=general --custom=custom-profile-nvidia-gpu.yaml -- ls -la /dev
```

```
Targeting container "cuda-container". If you don't see processes from this container it may be because the container runtime doesn't support this feature.
Defaulting debug container name to debugger-jv2k5.
total 4
drwxr-xr-x 6 root root      500 Jan 12 18:03 .
drwxr-xr-x 1 root root     4096 Jan 12 18:03 ..
crw--w---- 1 root tty  136,   0 Jan 12 18:03 console
lrwxrwxrwx 1 root root       11 Jan 12 18:03 core -> /proc/kcore
drwxr-xr-x 3 root root      100 Jan 12 18:03 dri
lrwxrwxrwx 1 root root       13 Jan 12 18:03 fd -> /proc/self/fd
crw-rw-rw- 1 root root   1,   7 Jan 12 18:03 full
drwxrwxrwt 2 root root       40 Jan 12 17:57 mqueue
crw-rw-rw- 1 root root   1,   3 Jan 12 18:03 null
crw-rw-rw- 1 root root 195, 254 Jan 12 18:03 nvidia-modeset
crw-rw-rw- 1 root root 235,   0 Jan 12 18:03 nvidia-uvm
crw-rw-rw- 1 root root 235,   1 Jan 12 18:03 nvidia-uvm-tools
crw-rw-rw- 1 root root 195,   0 Jan 12 18:03 nvidia0
crw-rw-rw- 1 root root 195, 255 Jan 12 18:03 nvidiactl
lrwxrwxrwx 1 root root        8 Jan 12 18:03 ptmx -> pts/ptmx
drwxr-xr-x 2 root root        0 Jan 12 18:03 pts
crw-rw-rw- 1 root root   1,   8 Jan 12 18:03 random
drwxrwxrwt 2 root root       40 Jan 12 17:57 shm
lrwxrwxrwx 1 root root       15 Jan 12 18:03 stderr -> /proc/self/fd/2
lrwxrwxrwx 1 root root       15 Jan 12 18:03 stdin -> /proc/self/fd/0
lrwxrwxrwx 1 root root       15 Jan 12 18:03 stdout -> /proc/self/fd/1
-rw-rw-rw- 1 root root        0 Jan 12 18:03 termination-log
crw-rw-rw- 1 root root   5,   0 Jan 12 18:03 tty
crw-rw-rw- 1 root root   1,   9 Jan 12 18:03 urandom
crw-rw-rw- 1 root root   1,   5 Jan 12 18:03 zero
```

> The devices `/dev/dri` and `nvidia*` devices are listed for this ephemeral container
> ephemeral container will work for abcdesktop


### Delete `nvidia-pod`

```
kubectl delete -f nvidia-pod.yaml
pod "nvidia-pod" deleted from default namespace
```


## Conclusion

Setting `runtimeClassName: nvidia` on pod manifest allows ephemeral containers to share the pod's GPU.


## Apply `runtimeClassName` to abcdesktop config (release >= 4.3 )


Get the `od.config` file

If you don't already have the config file `od.config`, run the command line 

```
kubectl -n abcdesktop get configmap abcdesktop-config -o jsonpath='{.data.od\.config}' > od.config
```

- Edit `od.config` and update the dictionary `desktop.pod` to add `'runtimeClassName':'nvidia'` in `spec` and save your od.config file.

```
desktop.pod : { 
  # default spec for all containers
  # can be overwritten on dedicated container spec
  # value inside mustrache like {{ uidNumber }} is replaced by context run value
  # for example {{ uidNumber }} is the uid number define in ldap server 
  'spec' : {
    'shareProcessNamespace': False,
    'securityContext': {
      'supplementalGroups': [ '{{ supplementalGroups }}' ],
      'runAsUser': '{{ uidNumber }}',
      'runAsGroup': '{{ gidNumber }}'
    },
    'tolerations': [],
    'runtimeClassName': 'nvidia'
  },
  ...
```

- Update the configmap `abcdesktop-config`

```
kubectl create -n abcdesktop configmap abcdesktop-config --from-file=od.config -o yaml --dry-run=client | kubectl replace -n abcdesktop -f -
```

- Restart deployment `pyos-od`

```
kubectl rollout restart deployment pyos-od -n abcdesktop
```

- Create a new desktop pod to check the `runtimeClassName`

## Links

- nvidia gpu-operator/23.6.2

[https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/23.6.2/cdi.html#support-for-multi-instance-gpu](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/23.6.2/cdi.html#support-for-multi-instance-gpu) 



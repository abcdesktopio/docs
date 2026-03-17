## General requirements

- kubernetes cluster `READY` to run
- `kubectl` or `minikube` command-line tool must be configured to communicate with your cluster. 
- `openssl` and `curl` command line must be installed too (only for install using kubectl). 

## Requirements for minikube 

To fix this issue

``` shell
FailedScheduling 0/1 nodes are available: 1 Insufficient cpu. preemption: 0/1 nodes are available: 1 No preemption victims found for incoming pod
```

Start minikube with enough cpu and memory resources to start all abcdesktop's pods and the user's desktop

``` shell
minikube start --cpus 4 --memory 4096
```
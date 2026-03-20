---
tags:
  - minikube
  - installation
---


## Requirements for minikube 

Start minikube with enough cpu and memory resources to start all abcdesktop's pods and the user's desktop

```
minikube start --cpus 4 --memory 4096
```

To fix this issue

```
FailedScheduling 0/1 nodes are available: 1 Insufficient cpu. preemption: 0/1 nodes are available: 1 No preemption victims found for incoming pod
```

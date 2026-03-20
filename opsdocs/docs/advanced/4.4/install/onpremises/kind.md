---
tags:
  - kind
  - installation
---

Kind is a tool for running local Kubernetes clusters using Docker container “nodes”. Kind was primarily designed for testing Kubernetes itself, but it can be used to deploy Kubernetes applications as well. To install or setup `kind`, refer to the [Kind documentation](https://kind.sigs.k8s.io/)

## Requirements

* `kind` command line
* kubectl command-line tool must be configured to communicate with your cluster.
* openssl and curl command line must be installed too (only for install using kubectl) or helm command.

## Create kind cluster

Run the command line to create 

```
kind create cluster
```

You should read on stdout

```
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.34.0) 🖼 
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Have a question, bug, or feature request? Let us know! https://kind.sigs.k8s.io/#community 🙂
```

## Run the install bash script 

```
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-{{ abcdesktop.latest_release }}.sh | bash
```

You should read on stdout

```
NAME                            READY   STATUS    RESTARTS   AGE
console-od-c96c4989d-x4256      1/1     Running   0          93s
memcached-od-6ccd5b5f67-9gznq   1/1     Running   0          93s
mongodb-od-0                    2/2     Running   0          93s
nginx-od-9c5774bdd-z49jq        1/1     Running   0          93s
openldap-od-bb485cb4b-6d5j7     1/1     Running   0          93s
pyos-od-5c5cfdbfc8-f852d        1/1     Running   0          93s
router-od-6b7456b789-rkxfd      1/1     Running   0          93s
speedtest-od-8686c67749-t4n7j   1/1     Running   0          93s
```

## How to connect 

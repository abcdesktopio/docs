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

## How to connect 

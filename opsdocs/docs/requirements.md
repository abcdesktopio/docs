---
tags:
  - installation
  - requirement
---

# Requirements

## Prerequisites for Deploying abcdesktop.io

The following prerequisites apply to all abcdesktop.io deployment scenarios, including single-node evaluation setups and production multi-node Kubernetes clusters.

- **Supported CPU architectures:** `x86-64` (amd64) and `arm-64` (arm64)
- **Minimum available disk space:** 20 GB. This capacity accommodates the core abcdesktop.io control plane container images, the `oc.user` desktop image, and the default set of sample application images. Additional disk space is required for user home directories and any application images added after initial deployment.
- **Kubernetes cluster:** version **1.28 or later**, in the `Ready` state, with `cluster-admin` privileges for the installing user. Supported distributions include kubeadm, k3s, microk8s, GKE, EKS, AKS, and OKE.

### GNU/Linux

The recommended operating system for production deployments is **Ubuntu 24.04.2 LTS**. Any Linux distribution that provides a supported Kubernetes distribution and a compatible container runtime (containerd or CRI-O) is suitable for both evaluation and production use.

### macOS

Use [Docker Desktop](https://www.docker.com/products/docker-desktop/) with the built-in Kubernetes integration enabled. Verify that the Kubernetes cluster is in the `Running` state before proceeding with the abcdesktop.io installation. On macOS, the Kubernetes cluster runs inside a Linux virtual machine managed by Docker Desktop; ensure that sufficient CPU and memory resources are allocated to this virtual machine in the Docker Desktop resource settings.

### Microsoft Windows

Use [Docker Desktop](https://www.docker.com/products/docker-desktop/) with the built-in Kubernetes integration enabled. Verify that the Kubernetes cluster is in the `Running` state before proceeding with the abcdesktop.io installation. On Windows, Docker Desktop relies on the WSL 2 (Windows Subsystem for Linux 2) backend; ensure that WSL 2 is installed and that adequate memory is allocated to the WSL 2 instance via the `.wslconfig` configuration file.

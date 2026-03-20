---
tags:
  - kind
  - installation
---

Kind is a tool for running local Kubernetes clusters using Docker container “nodes”. Kind was primarily designed for testing Kubernetes itself, but it can be used to deploy Kubernetes applications as well. To install or setup `kind`, refer to the [Kind documentation](https://kind.sigs.k8s.io/)

## Requirements

* Kubernetes cluster READY to run
* kubectl command-line tool must be configured to communicate with your cluster.
* openssl and curl command line must be installed too (only for install using kubectl) or helm command.

You can run the Quick installation process or choose the Manually installation step by step

> Linux operating system is recommanded to run abcdesktop.io.

## Quick installation

* Using [bash script](/install/{{ config.extra.abcdesktop.latest_release }}/bash/)
* Using [helm](/install/{{ config.extra.abcdesktop.latest_release }}/helm/)

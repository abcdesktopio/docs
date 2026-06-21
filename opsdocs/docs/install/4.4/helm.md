---
title: Install abcdesktop.io Using Helm | abcdesktop.io
description: Step-by-step guide to deploying abcdesktop.io on Kubernetes using the official Helm chart, including chart repository setup and values configuration.
keywords: Helm, Helm chart, install, Kubernetes, abcdesktop, deployment, values, chart
tags:
  - helm
  - installation
  - setup
  - upgrade
  - Helm
---

# Installing abcdesktop.io Using Helm

[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/abcdesktop)](https://artifacthub.io/packages/search?repo=abcdesktop)

<div class="artifacthub-widget" data-url="https://artifacthub.io/packages/helm/abcdesktop/abcdesktop" data-theme="light" data-header="false" data-stars="false" data-responsive="false"><blockquote><p lang="en" dir="ltr"><b>abcdesktop</b>: ABCDesktop helm chart</p>&mdash; Open in <a href="https://artifacthub.io/packages/helm/abcdesktop/abcdesktop">Artifact Hub</a></blockquote></div><script async src="https://artifacthub.io/artifacthub-widget.js"></script>

## Prerequisites

- A Kubernetes cluster in the `Ready` state
- The `helm` command-line tool installed and configured to communicate with your cluster

## Installing the Latest Release {{ abcdesktop.latest_release }}

![install using helm](https://github.com/abcdesktopio/helm/releases/download/abcdesktop-{{ abcdesktop.helm_latest_release }}/install-using-helm.gif)

Add the abcdesktop.io Helm repository and install the chart:

```bash
NAMESPACE=abcdesktop
helm repo add abcdesktop https://abcdesktopio.github.io/helm/
helm install my-abcdesktop abcdesktop/abcdesktop --version 4.4.1 --create-namespace -n ${NAMESPACE}
```

??? note "show details"

    ```bash
    NAME: my-abcdesktop
    LAST DEPLOYED: Tue Mar 24 14:24:17 2026
    NAMESPACE: abcdesktop
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    NOTES:
    # After installation, wait for all deployments to become available

    NAMESPACE=abcdesktop
    kubectl wait deployment -n ${NAMESPACE} --all --for condition=Available=True --timeout=300s
    kubectl get services -n ${NAMESPACE}


    # Connect to your abcdesktop instance using port-forwarding
    # Note: port-forwarding is intended for testing only
    # Adjust LOCAL_PORT if the default port is already in use

    LOCAL_PORT=30443
    NAMESPACE=abcdesktop
    kubectl port-forward $(kubectl get pods -l run=router-od -o jsonpath={.items..metadata.name} -n ${NAMESPACE} ) --address 0.0.0.0 "${LOCAL_PORT}:80" -n ${NAMESPACE}

    Open your web browser to http://localhost:30443
    ```

Once the Helm installation completes, forward the router pod's TCP port 80 to a local port (for example, 30443):

```bash
LOCAL_PORT=30443
NAMESPACE=abcdesktop
kubectl port-forward $(kubectl get pods -l run=router-od -o jsonpath={.items..metadata.name} -n ${NAMESPACE} ) --address 0.0.0.0 "${LOCAL_PORT}:80" -n ${NAMESPACE}
```

## Video: Quick Installation Using Helm

The following video demonstrates the complete Helm-based installation process:

<div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/QQTWRf5Vf8g" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>


## Helm Configuration Options

To customize default Helm chart parameters, follow these steps:

### Step 1: Export the Default Configuration

Retrieve the default values file from the chart:

~~~bash
helm show values abcdesktop/abcdesktop  > abcdesktop-values.yaml
~~~

A file named `abcdesktop-values.yaml` is created in the current directory. Its structure looks similar to the following:

~~~ yaml
imagePullSecrets: []

console:
  image: ghcr.io/abcdesktopio/console
  tag: {{ abcdesktop.latest_release }}
  replicaCount: 1
  resources:
    limits:
      cpu: 0.5
      memory: 128Mi
    requests:
      cpu: 0.1
      memory: 16Mi

memcached:
  image: ghcr.io/abcdesktopio/oc.memcached
  tag: {{ abcdesktop.latest_release }}
  replicaCount: 1
  resources:
    limits:
      cpu: 0.2
      memory: 64Mi
    requests:
      cpu: 0.1
      memory: 16Mi
...
~~~

Edit this file to override any default parameters.

!!! warning
    The values file is a YAML file. Indentation is significant — use consistent spacing to avoid parsing errors.
!!! note
    Values evolve across chart versions. As a best practice, include only the parameters you intend to override and let the chart supply all other defaults.

For example, to override only the memcached image and the console image tag while increasing the console CPU limit:

~~~yaml
console:
  tag: {{ abcdesktop.latest_release }}
  resources:
    limits:
      cpu: 99999

memcached:
  image: ghcr.io/abcdesktopio/MY.memcached
~~~

All non-overridden parameters use the chart's default values.

### Step 2: Apply the Custom Values File

Install or upgrade the chart with your custom values file:

~~~ bash
helm install my-abcdesktop abcdesktop/abcdesktop \
    --version {{ abcdesktop.latest_release }} \
    --create-namespace \
    -n ${NAMESPACE} \
    -f abcdesktop-values.yaml
~~~

## Upgrading an Existing Helm Release

To upgrade both the chart version and configuration values of an existing release:

~~~bash
helm upgrade my-abcdesktop \
    --version {{ abcdesktop.latest_release }} \
    -f abcdesktop-values \
    -n ${NAMESPACE}
~~~

---
tags:
  - helm
  - installation
  - setup
  - upgrade
---

# Installation using helm

[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/abcdesktop)](https://artifacthub.io/packages/search?repo=abcdesktop)

<div class="artifacthub-widget" data-url="https://artifacthub.io/packages/helm/abcdesktop/abcdesktop" data-theme="light" data-header="false" data-stars="false" data-responsive="false"><blockquote><p lang="en" dir="ltr"><b>abcdesktop</b>: ABCDesktop helm chart</p>&mdash; Open in <a href="https://artifacthub.io/packages/helm/abcdesktop/abcdesktop">Artifact Hub</a></blockquote></div><script async src="https://artifacthub.io/artifacthub-widget.js"></script>

## Requirements

- kubernetes cluster `READY` to run
- `helm` command-line tool must be installed. 

## Installation using helm latest release {{ abcdesktop.latest_release }}

Add the `helm` repo and then install it on Linux or macOS or read the step by step installation process [abcdesktop for kubernetes](/{{ abcdesktop.latest_release }}/setup/kubernetes_abcdesktop)

```
NAMESPACE=abcdesktop
helm repo add abcdesktop https://abcdesktopio.github.io/helm/
helm install my-abcdesktop abcdesktop/abcdesktop --version {{ abcdesktop.latest_release }} --create-namespace -n ${NAMESPACE}
```

    ??? note "show details"
    ```
    NAME: my-abcdesktop
    LAST DEPLOYED: Tue Mar 24 14:24:17 2026
    NAMESPACE: abcdesktop
    STATUS: deployed
    REVISION: 1
    TEST SUITE: None
    NOTES:
    # After installation, and wait for deployments and services

    NAMESPACE=abcdesktop
    kubectl wait deployment -n ${NAMESPACE} --all --for condition=Available=True --timeout=300s
    kubectl get services -n ${NAMESPACE}


    # To connect to your abcdesktop using a port forward  
    - port-forwarding is only for testing
    - change LOCAL_PORT if need 

    LOCAL_PORT=30443
    NAMESPACE=abcdesktop
    kubectl port-forward $(kubectl get pods -l run=router-od -o jsonpath={.items..metadata.name} -n ${NAMESPACE} ) --address 0.0.0.0 "${LOCAL_PORT}:80" -n ${NAMESPACE}

    Open your web browser to http://localhost:30443
    ```


When install your helm installation process is ready, you need to forward the pod's router tcp port 80 to your localhost port 30443 (for example)

```bash
LOCAL_PORT=30443
NAMESPACE=abcdesktop
kubectl port-forward $(kubectl get pods -l run=router-od -o jsonpath={.items..metadata.name} -n ${NAMESPACE} ) --address 0.0.0.0 "${LOCAL_PORT}:80" -n ${NAMESPACE}
```

## Video to run the quick installation process 

You can watch the youtube video sample. This video describes the Quick installation process using `helm`.

<div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/86RLis48U0I" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>


## Helm options

To modify any default parameters of the helm configuration, follow these steps:

### Step 1: Retrieve the default configuration file from helm

~~~bash
helm show values abcdesktop/abcdesktop  > abcdesktop-values.yaml
~~~

A new file named *abcdesktop-values.yaml* will be created in your current directory.

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

You can edit this file to change any default parameters of helm configuration.

!!! warning
    The values file is a YAML file, where indentation is critical.
!!! note
    Values can evolve with helm versions, so a good practice is to keep only the changed parts.

If you want to change only the memcached docker image and console image tags and CPU
limit, your *abcdesktop-values.yaml* may look like:

~~~yaml
console:
  tag: {{ abcdesktop.latest_release }}
  resources:
    limits:
      cpu: 99999

memcached:
  image: ghcr.io/abcdesktopio/MY.memcached
~~~

Non-overridden values will use the default ones.

### Step 2 - apply helm with your values file

Then apply your configuration:

~~~ bash
helm install my-abcdesktop abcdesktop/abcdesktop \
    --version {{ abcdesktop.latest_release }} \
    --create-namespace \
    -n ${NAMESPACE} \
    -f abcdesktop-values.yaml
~~~

## Helm upgrade

An installed helm chart can be upgraded (both version and values) using:

~~~bash
helm upgrade my-abcdesktop \
    --version {{ abcdesktop.latest_release }} \
    -f abcdesktop-values \
    -n ${NAMESPACE}
~~~

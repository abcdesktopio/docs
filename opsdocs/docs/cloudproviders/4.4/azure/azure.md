---
title: Deploy abcdesktop.io on Microsoft Azure AKS | abcdesktop.io
description: Step-by-step guide to deploying abcdesktop.io on Microsoft Azure Kubernetes Service (AKS), including resource group, cluster creation, and kubeconfig setup.
keywords: Azure, AKS, Microsoft Azure Kubernetes Service, cloud, deploy, abcdesktop, Kubernetes, install
tags:
  - Azure
  - AKS
  - cloud
  - installation
---

# Deploy abcdesktop on Azure with Microsoft Azure Kubernetes Service


## Requirements

- `az` command line interface [azure-cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest) installed.
- You need your `Azure Subscription Name`, `Username`, and `Password`.
- A running Azure Kubernetes Service cluster that is `ready` and running.

## Azure console overview

Create a new Azure Kubernetes Service cluster.

![azure console kubernetes create cluster](img/azure-aks-create-kubernetes-cluster.png)

> All options and features use their default values.

In this example, the Kubernetes cluster is named `abcdesktopkubernetescluster`.
This screenshot shows the Azure Kubernetes Service console, displaying the **Node pools** and **Networking** configuration.

![azure console overview](img/azure-aks-console.png)


## Check your caller-identity

If you have not already done so, run the `az login` command:

```
az login
```

The remaining steps complete in your web browser using your own credentials.


## Set your subscription for your Azure account


``` bash
az account set --subscription XXXXXX-YYYYY-ZZZZZ-AAAA-BBBBBBBBBB
```

## Create your kubernetes config 

``` bash
az aks get-credentials --name MyManagedCluster --overwrite-existing --resource-group MyResourceGroup
``` 

For example 

- `resource-group`: abcdesktop
- `name`: abcdesktopkubernetescluster

``` bash
az aks get-credentials --resource-group abcdesktop --name abcdesktopkubernetescluster --overwrite-existing
```

## Get your Kubernetes cluster information

Run the `kubectl cluster-info` command line to confirm that the `kubectl` command can communicate with your Azure cluster.

``` bash
kubectl cluster-info
```

``` bash
Kubernetes control plane is running at https://abcdesktopkubernetescluster-dns-rm7w2mot.hcp.northeurope.azmk8s.io:443
CoreDNS is running at https://abcdesktopkubernetescluster-dns-rm7w2mot.hcp.northeurope.azmk8s.io:443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy
Metrics-server is running at https://abcdesktopkubernetescluster-dns-rm7w2mot.hcp.northeurope.azmk8s.io:443/api/v1/namespaces/kube-system/services/https:metrics-server:/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
```

## Run the abcdesktop install script 


Download and extract the latest release automatically

```
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-{{ abcdesktop.latest_release }}.sh | bash
```

To get more details about the install process, please read the [Setup guide](https://www.abcdesktop.io/{{ abcdesktop.latest_release }}/setup/kubernetes_abcdesktop/)


## Connect to your abcdesktop service 

By default, the install script listens on TCP port `:30443` and uses a `kubectl port-forward` command to forward traffic to the HTTP service on port `:80`.

Open your web browser and navigate to `http://localhost:30443`.

![abcdesktop login](../img/abcdesktop-hompage-port30443.png)

 
Log in as user `Philip J. Fry` with the password `fry`

![abcdesktop login as fry](../img/abcdesktop-hompage-port30443-login-fry.png)
 
After the image-pulling process completes, you get your first abcdesktop session

![abcdesktop for fry](../img/abcdesktop-hompage-port30443-user-fry-logged.png)


## Add applications to your desktop


Using the same terminal session, run the application install script:

```
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/pullapps-{{ abcdesktop.latest_release }}.sh | bash
```

To get more details about the install applications process, please read the [Setup applications guide](https://www.abcdesktop.io/{{ abcdesktop.latest_release }}/setup/kubernetes_abcdesktop_applications/)

Then reload the web page with the desktop of `Philip J. Fry`.
New applications are now listed in the `plasmashell` dock.


![abcdesktop for fry with applications](../img/abcdesktop-hompage-port30443-login-fry-applications.png)

Start Firefox application

> The first run may require waiting for the image-pulling process to complete.

Navigate to `https://mylocation.org` to check where your pod is running. For the `North Europe` region, the desktop is located near Dublin, Ireland.


![abcdesktop for fry with applications](img/abcdesktop-firefox-azure-north-europe.png)











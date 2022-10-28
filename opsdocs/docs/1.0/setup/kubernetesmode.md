# Setup kubernetes for GNU/Linux

This section apply only to configure kubernetes for GNU/Linu. The Docker setup process for MacOS/X and for Microsoft Windows is ready to use by cheching the kubernetes options.

abcdesktop.io support docker mode and kubernetes mode. In this section we will study how abcdesktop.io is working in kubernetes mode. The abcdesktop.io kubernetes mode is recommended for enterprise use, all user containers can be distributed on different hosts.

## Requirements

[Linux Requierements](k8slinuxinstallation.md)


## Installation

The following commands will let you prepare kubernetes on one node. In this case, all applications run on a single node. To deploy a abcdesktopio on multi nodes read the next section. It's recommended to start with a single node.


### Initialize Kubernetes Master Node
#### Step 1: Disable swap memory (if running)
You need to disable swap memory on nodes as Kubernetes does not perform properly on a system that is using swap memory. Run the following command in order to disable swap memory.  

```bash
swapoff -a
```

If you have some swaps in /etc/fstab, just comment them out.
`swapoff -a` will disable all swaps temporarily.

* disable by masking it with sysctl:

```bash
systemctl mask dev-zram1.swap

Created symlink /etc/systemd/system/dev-zram1.swap → /dev/null.
```

#### Step 2: Initialize Kubernetes
Run the following command as sudo on the master node:

```bash
kubeadm init --pod-network-cidr=10.244.0.0/16
```

The process might take a minute or more depending on your internet connection.  

To be able to manage your kubernetes server, you need to run the following commands as a regular user:

```bash
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
```


#### Step 3: Remove Master Node Taint 

Taints are Kubernetes flags to prevent Pod Scheduling. Remove the taints on the master so that you can schedule pods on it.

```bash
kubectl taint node `hostname` node-role.kubernetes.io/master-
```

It should return the following string.

```
node/<your-hostname> untainted
```
Taints are Kubernetes flags to prevent Pod Scheduling.


Confirm that you now have a node in your cluster with the following command.

```bash
kubectl get nodes -o wide
```

It should return something like the following.

```
NAME              STATUS      ROLES    AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION    CONTAINER-RUNTIME
<your-hostname>   NotReady    master   2m    v1.19.3   192.168.8.2   <none>        Ubuntu 20.04.1 LTS   5.4.0-52-generic   docker://19.3.13
```

#### Step 4: Deploy a Pod Network through the master node

A pod network is a medium of communication between the nodes of a network. We are deploying a Flannel pod network on our cluster through the following command:

```bash
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```

It should return the following strings.

```
podsecuritypolicy.policy/psp.flannel.unprivileged created
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.apps/kube-flannel-ds created
```

##### Check node status

Now when you see the status of the nodes, you will see that the master-node is ready :

```bash
kubectl get nodes -o wide
```

```
NAME             STATUS   ROLES    AGE   VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION     CONTAINER-RUNTIME
<your-hostname>  Ready    master   5m    v1.19.3   192.168.8.2   <none>        Ubuntu 20.04.1 LTS   5.4.0-52-generic   docker://19.3.13
```

At this step, there is no more ```Taints``` and your node is ```Ready```. 

Next step, continue with the [setup abcdesktop](kubernetes_abcdesktop.md) for kubernetes.


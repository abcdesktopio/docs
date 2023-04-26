
# Linux Requirements

### Packages installation

To install Kubernetes on your GNU/Linux, you can read the [Kubernetes setup guide](https://kubernetes.io/docs/setup/) on the kubernetes.io web site.

### Install Kubernetes on Linux

#### Step 0: Disable swap

Execute command swapoff to disable swap.

``` bash
swapoff -a
```

Load the `overlay` and `br_netfilter` kernel modules

``` bash
modprobe overlay
modprobe br_netfilter
```

Create the `containerd.conf` to load modules

``` bash
cat >>/etc/modules-load.d/containerd.conf <<EOF
overlay
br_netfilter
EOF
```

#### Step 1: Install `containerd`

Install the containerd utility and required packages on node by running the following command as sudo in a Terminal :

Install common packages

``` bash
apt-get install -y curl gnupg2 software-properties-common apt-transport-https ca-certificates
```

Add source

``` bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmour -o /etc/apt/trusted.gpg.d/docker.gpg
add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

You will be prompted with a Y/n option in order to proceed with the installation. 

``` bash
apt update
apt install -y containerd.io
```

`containerd` will then be installed on your system. 



#### Step 2: Configure containerd 


Configure `containerd` to use `systemd` as `cgroup`. 

``` bash
containerd config default > /etc/containerd/config.toml
sed -i 's/SystemdCgroup \= false/SystemdCgroup \= true/g' /etc/containerd/config.toml
```

Enable the containerd utility by running the following command :

``` bash
systemctl restart containerd
systemctl enable containerd
```


#### Step 3: Add the Kubernetes signing key

Run the following command in order to get the Kubernetes signing key:

``` bash
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - 
```
 
 
#### Step 4: Add Xenial Kubernetes Repository
 
Run the following commands in order to add the Xenial Kubernetes repository:

``` bash
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list 
apt-get update
```

#### Step 5: Install Kubernetes


Create `kubernetes.conf` for `sysctl.d`

``` bash
cat >>/etc/sysctl.d/kubernetes.conf <<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF
```

Reload your system `sysctl` changes 

``` bash
sysctl --system
```


Install the packages `kubelet` `kubeadm` `kubectl`

``` bash
apt install -y kubelet kubeadm kubectl
```

K8s utilities will then be installed on your system.

You can check the version number of `kubeadm` and also verify the installation through the following command:

``` bash
 kubeadm version -o yaml
```

``` yaml
clientVersion:
  buildDate: "2022-10-12T10:55:36Z"
  compiler: gc
  gitCommit: 434bfd82814af038ad94d62ebe59b133fcb50506
  gitTreeState: clean
  gitVersion: v1.25.3
  goVersion: go1.19.2
  major: "1"
  minor: "25"
  platform: linux/amd64
```


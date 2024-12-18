
# Linux Requirements

### Packages installation

To install Kubernetes on your GNU/Linux, you can read the [Kubernetes setup guide](https://kubernetes.io/docs/setup/) on the kubernetes.io web site.

### Install Kubernetes on Ubuntu 22.04 

These commands install the latest Kubernetes on a single node Ubuntu 22.04.
`km` is a command tools from [https://github.com/jfv-opensource/kube-tools](https://github.com/jfv-opensource/kube-tools) repository.


Clone [kube-tools](https://github.com/jfv-opensource/kube-tools) and run `km --apply` as root.

``` bash
git clone https://github.com/jfv-opensource/kube-tools.git
cd kube-tools
./km --apply
```

kube-tools installs and configures all components.
kube-tools runs a simple hello-world pods to check the pods execution.

```
Configure repositories & install packages
2023-10-06 12:37:52 [OK] - fv-az1111-309: Updating package repository
2023-10-06 12:37:53 [OK] - fv-az1111-309: Installing base needed packages
2023-10-06 12:37:53 [OK] - fv-az1111-309: Adding docker package repository signature
Get:1 file:/etc/apt/apt-mirrors.txt Mirrorlist [142 B]
Get:6 https://download.docker.com/linux/ubuntu jammy InRelease [48.9 kB]
Hit:7 https://packages.microsoft.com/ubuntu/22.04/prod jammy InRelease
Hit:2 http://azure.archive.ubuntu.com/ubuntu jammy InRelease
Hit:3 http://azure.archive.ubuntu.com/ubuntu jammy-updates InRelease
Hit:4 http://azure.archive.ubuntu.com/ubuntu jammy-backports InRelease
Hit:5 http://azure.archive.ubuntu.com/ubuntu jammy-security InRelease
Get:8 https://download.docker.com/linux/ubuntu jammy/stable amd64 Packages [22.2 kB]
Hit:9 https://ppa.launchpadcontent.net/ubuntu-toolchain-r/test/ubuntu jammy InRelease
Fetched 71.0 kB in 1s (71.4 kB/s)
Reading package lists...
Repository: 'deb [arch=amd64] https://download.docker.com/linux/ubuntu jammy stable'
Description:
Archive for codename: jammy components: stable
More info: https://download.docker.com/linux/ubuntu
Adding repository.
Adding deb entry to /etc/apt/sources.list.d/archive_uri-https_download_docker_com_linux_ubuntu-jammy.list
Adding disabled deb-src entry to /etc/apt/sources.list.d/archive_uri-https_download_docker_com_linux_ubuntu-jammy.list
2023-10-06 12:37:59 [OK] - fv-az1111-309: Adding docker package repository
2023-10-06 12:38:00 [OK] - fv-az1111-309: Adding google package repository signature
2023-10-06 12:38:00 [OK] - fv-az1111-309: Adding google package repository
2023-10-06 12:38:03 [OK] - fv-az1111-309: Updating package repository
2023-10-06 12:38:09 [OK] - fv-az1111-309: Installing kubectl
2023-10-06 12:38:09 [OK] - fv-az1111-309: Freezing kubernetes tools version
Configure system
2023-10-06 12:38:09 [OK] - fv-az1111-309: Disabling swap in this session
2023-10-06 12:38:09 [OK] - fv-az1111-309: Disabling swap in this file /etc/fstab
2023-10-06 12:38:09 [OK] - fv-az1111-309: Enabling module overlay
2023-10-06 12:38:09 [OK] - fv-az1111-309: Enabling module br_netfilter
2023-10-06 12:38:09 [OK] - fv-az1111-309: Enabling module load for containerd
2023-10-06 12:38:24 [OK] - fv-az1111-309: Installing containerd & kubernetes tools
2023-10-06 12:38:24 [OK] - fv-az1111-309: Freezing kubernetes tools version
2023-10-06 12:38:24 [OK] - fv-az1111-309: Configuring containerd 1#2
2023-10-06 12:38:24 [OK] - fv-az1111-309: Configuring containerd 2#2
2023-10-06 12:38:24 [OK] - fv-az1111-309: Restarting containerd
2023-10-06 12:38:25 [OK] - fv-az1111-309: Enabling containerd
2023-10-06 12:38:25 [OK] - fv-az1111-309: Configuring network for kubernetes
2023-10-06 12:38:25 [OK] - fv-az1111-309: Applying system configuration
Configure kubernetes
2023-10-06 12:38:51 [OK] - fv-az1111-309: Starting master node
2023-10-06 12:38:51 [OK] - fv-az1111-309: Writting kubernetes config file to /root/.kube/config
2023-10-06 12:38:54 [OK] - fv-az1111-309: Loading network configuration into cluster
2023-10-06 12:38:54 [OK] - fv-az1111-309: Allowing pods on master because of standalone node
2023-10-06 12:38:54 [INFO] - fv-az1111-309: Waiting for node fv-az1111-309 condition=Ready during timeout=600s
2023-10-06 12:39:01 [OK] - fv-az1111-309: Your cluster is Ready
Error from server (NotFound): serviceaccounts "default" not found
2023-10-06 12:39:01 [INFO] - fv-az1111-309:  retry 1/10 default account service account is net yet created, sleeping for 5s
2023-10-06 12:39:07 [OK] - fv-az1111-309: default account service account is created
2023-10-06 12:39:07 [OK] - fv-az1111-309: create pod-helloworld
2023-10-06 12:39:12 [OK] - fv-az1111-309: pod-helloworld says hello world
2023-10-06 12:39:17 [OK] - fv-az1111-309: delete pod-helloworld
Configuration archive
2023-10-06 12:39:17 [OK] - fv-az1111-309: Generating config archive
```



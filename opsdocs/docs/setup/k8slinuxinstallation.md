
# Linux Requirements

### Packages installation

To install Kubernetes on your GNU/Linux, you can read the [Kubernetes setup guide](https://kubernetes.io/docs/setup/) on the kubernetes.io web site.

### Install Kubernetes on Linux

#### Step 1: Install Docker

Install the Docker utility and required packages on node by running the following command as sudo in a Terminal :

```
sudo apt-get install docker.io containerd gnupg openssl iptables acl python3-openssl apt-transport-https
```

You will be prompted with a Y/n option in order to proceed with the installation. Please enter Y and then hit enter to continue. Docker will then be installed on your system. You can verify the installation and also check the version number of Docker through the following command:

```
docker --version
```

#### Step 2: Enable Docker

Enable the Docker utility by running the following command on each:

```
sudo systemctl enable docker
```


#### Step 3: Add the Kubernetes signing key

Run the following command in order to get the Kubernetes signing key:
```
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - 
```


If ```curl``` is not installed on your system, you can install it through the following command as root:

```
sudo apt install curl
```

You will be prompted with a Y/n option in order to proceed with the installation. Please enter ```Y``` and then hit enter to continue. The Curl utility will then be installed on your system.
 
 
#### Step 4: Add Xenial Kubernetes Repository
 
Run the following commands in order to add the Xenial Kubernetes repository:

```
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list 
sudo apt-get update
```

#### Step 5: Install Kubernetes utilities

```
sudo apt-get install -y kubectl kubelet kubeadm
```


You will be prompted with a Y/n option in order to proceed with the installation. Please enter Y and then hit enter to continue. K8s utilities will then be installed on your system.

* Your kubernetes version must be greater than or equal to 1.15.0-00 

You can check the version number of Kubeadm and also verify the installation through the following command:

```
kubeadm version
```


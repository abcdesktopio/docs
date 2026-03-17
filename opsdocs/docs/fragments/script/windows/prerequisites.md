## Install and configure Docker Desktop

To run abcdesktop on Microsoft Windows plateform you need to use [docker desktop](https://www.docker.com/products/docker-desktop/)

Start `Docker Desktop` and wait for the docker engine to start.

![starting docker desktop](/fragments/script/windows/images/starting-docker-desktop.PNG)

Once started go to the `Settings | Kubernetes` and click on `Enable Kubernetes`, starting your cluster may take a while.

![enable kubernetes](/fragments/script/windows/images/enable-kubernetes.PNG)

Now your cluster should be correctly initialized, you can check it by opening a new PowerShell and run the command `kubectl version`

```
kubectl version
client version: V1.40.4
Kustomise Version: V9-0-4-0.202506011699445602001590025
Server Version: v1.28.2
```

![check kubectl](/fragments/script/windows/images/checking-kubernetes-start.PNG)

## Install OpenSSL

abcdesktop install process creates RSA keys using openssl, you need to install `openssl` command line.

Download the [OpenSSL v3.2.0 Light](https://www.openssl.org/source/) executable file.

![dl openssl](/fragments/script/windows/images/dl-openssl.PNG)

Then follow the install process.

![follow install step1](/fragments/script/windows/images/follow-install-step1.PNG)

Make sure to keep in mind the path where OpenSSL will be installed.

![follow install step2](/fragments/script/windows/images/follow-install-step2.PNG)

Once installed, go to "Edit the system environement variables", and click on "Environement variables".

![go to edit env variables](/fragments/script/windows/images/goto-edit-env-variable.PNG)

Go to the system variables section and search for `Path` 

![system variables](/fragments/script/windows/images/system-variables.PNG)

Click on `Edit` and add a new `Path`, you have to paste the absolute path to the bin folder of OpenSSL.

![add env variable](/fragments/script/windows/images/add-env-variable.PNG)

Now `OpenSSL` should be correctly installed, you can check it by opening a new PowerShell and run the command 

```
openssl version
```

![check openssl](/fragments/script/windows/images/checking-openssl-correctly-installed.PNG)

## Quick installation (Windows)

> Quick installation can be run on Windows operation system.

### Prerequisites

#### Install and configure Docker Desktop

To run abcdesktop on Microsoft Windows plateform you need to use [docker desktop](https://www.docker.com/products/docker-desktop/)

Start `Docker Desktop` and wait for the docker engine to start.

![starting docker desktop](./img/starting-docker-desktop.PNG)

Once started go to the `Settings | Kubernetes` and click on `Enable Kubernetes`, starting your cluster may take a while.

![enable kubernetes](./img/enable-kubernetes.PNG)

Now your cluster should be correctly initialized, you can check it by opening a new PowerShell and run the command `kubectl version`

```
kubectl version
client version: V1.40.4
Kustomise Version: V9-0-4-0.202506011699445602001590025
Server Version: v1.28.2
```

![check kubectl](./img/checking-kubernetes-start.PNG)

#### Install OpenSSL

Using your browser, look for `openssl` for Microsoft Windows.  

![search openssl](./img/search-openssl.PNG)

Download the "Win64 OpenSSL v3.2.0 Light" executable file.

![dl openssl](./img/dl-openssl.PNG)

Then follow the install process.

![follow install step1](./img/follow-install-step1.PNG)

Make sure to keep in mind the path where OpenSSL will be installed.

![follow install step2](./img/follow-install-step2.PNG)

Once installed, go to "Edit the system environement variables", and click on "Environement variables".

![go to edit env variables](./img/goto-edit-env-variable.PNG)

Go to the system variables section and search for "Path" 

![system variables](./img/system-variables.PNG)

Click on `Edit` and add a new `Path`, you have to paste the absolute path to the bin folder of OpenSSL.

![add env variable](./img/add-env-variable.PNG)

Now OpenSSL should be correctly installed, you can check it by opening a new PowerShell and run `openssl version`

![check openssl](./img/checking-openssl-correctly-installed.PNG)

### Run the install script

Download and extract the latest release automatically (Windows):

```PowerShell
$script = curl https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-3.2.ps1

Invoke-Expression $($script.Content)
```

You should read on stdout

```
[INFO] abcdesktop install script namespace=abcdesktop
[OK] kubectl version
[OK] openssl version
[OK] kubectl create namespace abcdesktop
writing RSA key
writing RSA key
[OK] abcdesktop_jwt_desktop_payload keys created
writing RSA key
[OK] abcdesktop_jwt_desktop_signing keys create
writing RSA key
[OK] abcdesktop_jwt_user_signing keys create
[OK] create secret generic abcdesktopjwtdesktoppayload
[OK] create secret generic abcdesktopjwtdesktopsigning
[OK] create secret generic abcdesktopjwtusersigning
[OK] label secret abcdesktopjwtdesktoppayload
[OK] label secret abcdesktopjwtdesktopsigning
[OK] label secret abcdesktopjwtusersigning
[OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/abcdesktop-3.2.yaml
[OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/reference/od.config.3.2
[OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/poduser-3.2.yaml
[OK] kubectl create configmap abcdesktop-config --from-file=od.config -n abcdesktop
[OK] label configmap abcdesktop-config abcdesktop/role=pyos.config
[INFO] kubectl create -f poduser.yaml
[OK] kubectl create -f poduser.yaml                                                                                     [INFO] waiting for pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 Ready                                             [OK] pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 condition met                                                   [INFO] deleting for pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 Ready                                            [OK] pod "anonymous-74bea267-8197-4b1d-acff-019b24e778c5" deleted
role.rbac.authorization.k8s.io/pyos-role created
rolebinding.rbac.authorization.k8s.io/pyos-rbac created
serviceaccount/pyos-serviceaccount created
configmap/configmap-mongodb-scripts created
configmap/nginx-config created
secret/secret-mongodb created
deployment.apps/mongodb-od created
deployment.apps/memcached-od created
deployment.apps/nginx-od created
deployment.apps/speedtest-od created
deployment.apps/pyos-od created
endpoints/desktop created
service/desktop created
service/memcached created
service/mongodb created
service/speedtest created
service/nginx created
service/pyos created
deployment.apps/openldap-od created
service/openldap created
[INFO] waiting for deployment/memcached-od available
[OK] deployment.apps/memcached-od condition met
[INFO] waiting for deployment/mongodb-od available
[OK] deployment.apps/mongodb-od condition met
[INFO] waiting for deployment/nginx-od available
[OK] deployment.apps/nginx-od condition met
[INFO] waiting for deployment/openldap-od available
[OK] deployment.apps/openldap-od condition met
[INFO] waiting for deployment/pyos-od available
[OK] deployment.apps/pyos-od condition met
[INFO] waiting for deployment/speedtest-od available
[OK] deployment.apps/speedtest-od condition met
[INFO] list all pods in namespace abcdesktop
NAME                            READY   STATUS    RESTARTS   AGE
memcached-od-5ff8844d56-x89kq   1/1     Running   0          11s
mongodb-od-77c945467d-c5cw4     1/1     Running   0          11s
nginx-od-86c5dfcc67-nfvbq       1/1     Running   0          11s
openldap-od-5bbdd75864-mzzmh    1/1     Running   0          11s
pyos-od-7646bf4786-c2hdm        1/1     Running   0          11s
speedtest-od-7f5484966f-6t4b2   1/1     Running   0          11s
[INFO] Setup done
[INFO] Checking the service url on http://localhost:30443
[INFO] service status is down
[INFO] Looking for a free TCP port from 30443
[OK] Get a free TCP port from 30443

[INFO] If you're using a cloud provider
[INFO] Forwarding abcdesktop service for you on port=30443
[INFO] For you setup is running the command 'kubectl port-forward nginx-od-86c5dfcc67-nfvbq --address 0.0.0.0 30443:80 -n abcdesktop'
[OK] Port-Forward successful
[OK] Please open your web browser and connect to

[INFO] http://localhost:30443/
```

You can open a web browser and go to the http://localhost:30443/ 

## Change the default namespace

You may need to replace the default namespace `abcdesktop` by your own. The `install-3.2.ps1` PowerShell script allows you to set the new namespace as an option.

```PowerShell
curl https://raw.githubusercontent.com/Matt307082/powershell-scripts/master/install-3.2.ps1 -OutFile install-3.2.ps1
```

Run `install-3.2.ps1`

```PowerShell
.\install-3.2.ps1 --namespace superdesktop
```

You should read on stdout

```
[INFO] abcdesktop install script namespace=superdesktop
[OK] kubectl version
[OK] openssl version
[OK] kubectl create namespace superdesktop
writing RSA key
writing RSA key
[OK] abcdesktop_jwt_desktop_payload keys created
writing RSA key
[OK] abcdesktop_jwt_desktop_signing keys create
writing RSA key
[OK] abcdesktop_jwt_user_signing keys create
[OK] create secret generic abcdesktopjwtdesktoppayload
[OK] create secret generic abcdesktopjwtdesktopsigning
[OK] create secret generic abcdesktopjwtusersigning
[OK] label secret abcdesktopjwtdesktoppayload
[OK] label secret abcdesktopjwtdesktopsigning
[OK] label secret abcdesktopjwtusersigning
[OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/abcdesktop-3.2.yaml
[OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/reference/od.config.3.2
[OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/poduser-3.2.yaml
[OK] updated abcdesktop.yaml file with new namespace superdesktop
[OK] updated abcdesktop.yaml file with new fqdn superdesktop.svc.cluster.local
[OK] updated od.config file with new namespace superdesktop
[OK] updated od.config file with new fqdn superdesktop.svc.cluster.local
[OK] updated poduser.yaml file with new superdesktop
[OK] kubectl create configmap abcdesktop-config --from-file=od.config -n superdesktop
[OK] label configmap abcdesktop-config abcdesktop/role=pyos.config
[INFO] kubectl create -f poduser.yaml
[OK] kubectl create -f poduser.yaml                                                                                     [INFO] waiting for pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 Ready                                             [OK] pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 condition met                                                   [INFO] deleting for pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 Ready                                            [OK] pod "anonymous-74bea267-8197-4b1d-acff-019b24e778c5" deleted
role.rbac.authorization.k8s.io/pyos-role created
rolebinding.rbac.authorization.k8s.io/pyos-rbac created
serviceaccount/pyos-serviceaccount created
configmap/configmap-mongodb-scripts created
configmap/nginx-config created
secret/secret-mongodb created
deployment.apps/mongodb-od created
deployment.apps/memcached-od created
deployment.apps/nginx-od created
deployment.apps/speedtest-od created
deployment.apps/pyos-od created
endpoints/desktop created
service/desktop created
service/memcached created
service/mongodb created
service/speedtest created
service/nginx created
service/pyos created
deployment.apps/openldap-od created
service/openldap created
[INFO] waiting for deployment/memcached-od available
[OK] deployment.apps/memcached-od condition met
[INFO] waiting for deployment/mongodb-od available
[OK] deployment.apps/mongodb-od condition met
[INFO] waiting for deployment/nginx-od available
[OK] deployment.apps/nginx-od condition met
[INFO] waiting for deployment/openldap-od available
[OK] deployment.apps/openldap-od condition met
[INFO] waiting for deployment/pyos-od available
[OK] deployment.apps/pyos-od condition met
[INFO] waiting for deployment/speedtest-od available
[OK] deployment.apps/speedtest-od condition met
[INFO] list all pods in namespace superdesktop
NAME                            READY   STATUS    RESTARTS   AGE
memcached-od-5ff8844d56-98t4t   1/1     Running   0          23s
mongodb-od-77c945467d-v4k58     1/1     Running   0          23s
nginx-od-7c7bf5bf48-khtvg       1/1     Running   0          23s
openldap-od-56b6564c85-t56tj    1/1     Running   0          21s
pyos-od-644c98bcd5-8gqzd        1/1     Running   0          23s
speedtest-od-894b7c886-fgt6v    1/1     Running   0          23s
[INFO] Setup done
[INFO] Checking the service url on http://localhost:30443
[INFO] service status is down
[INFO] Looking for a free TCP port from 30443
[OK] Get a free TCP port from 30443

[INFO] If you're using a cloud provider
[INFO] Forwarding abcdesktop service for you on port=30443
[INFO] For you setup is running the command 'kubectl port-forward nginx-od-86c5dfcc67-nfvbq --address 0.0.0.0 30443:80 -n superdesktop'
[OK] Port-Forward successful
[OK] Please open your web browser and connect to

[INFO] http://localhost:30443/
```

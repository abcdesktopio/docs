# abcdesktop in kubernetes mode

abcdesktop release 3.x support only kubernetes mode. All applications containers can be distributed on different hosts.

The abcdesktop infrastructure is using the contianers : 

| Container    | Role                     | Image                           | From         |
|--------------|--------------------------|---------------------------------|--------------|
| oc.pyos      | API Server               | abcdesktopio/oc.pyos:3.0        | abcdesktopio |
| oc.nginx     | web server proxy         | abcdesktopio/oc.nginx:3.0       | abcdesktopio |
| oc.speedtest | http benchmarch          | abcdesktopio/oc.speedtest       | [LibreSpeed](https://librespeed.org/) |
| oc.mongo     | json database server     | mongo                           | [MongoDB](https://www.mongodb.com/)   |
| memcached    | cache server             | memcached                       | [Memcached](https://memcached.org/)   |


## Requirements

You need to have a 

- kubernetes cluster ready to run
- `kubectl` or `microk8s` command-line tool must be configured to communicate with your cluster. 
- `openssl` and `curl` command line must be installed too.


You can run the **Quick installation process** or choose the **Manually installation step by step**


## Quick installation (Linux or macOS)

> Quick installation can be run on Linux or macOS operation system. 

Download and extract the latest release automatically (Linux or macOS):

```
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-3.1.sh | bash
```

You can read on stdout 


```
[INFO] abcdesktop install script namespace=abcdesktop
[OK] kubectl version
[OK] openssl version
[OK] kubectl create namespace abcdesktop
Generating RSA private key, 1024 bit long modulus
..........+++++
...+++++
e is 65537 (0x10001)
writing RSA key
writing RSA key
[OK] abcdesktop_jwt_desktop_payload keys create
Generating RSA private key, 1024 bit long modulus
...+++++
..................................+++++
e is 65537 (0x10001)
writing RSA key
[OK] abcdesktop_jwt_desktop_signing keys create
Generating RSA private key, 1024 bit long modulus
.....+++++
...............................................+++++
e is 65537 (0x10001)
writing RSA key
[OK] abcdesktop_jwt_user_signing keys create
[OK] create secret generic abcdesktopjwtdesktoppayload
[OK] create secret generic abcdesktopjwtdesktopsigning
[OK] create secret generic abcdesktopjwtusersigning
[OK] label secret abcdesktopjwtdesktoppayload
[OK] label secret abcdesktopjwtdesktopsigning
[OK] label secret abcdesktopjwtusersigning
##################################################################################################################################################################################################### 100.0%
[OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/abcdesktop-3.1.yaml
##################################################################################################################################################################################################### 100.0%
[OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/reference/od.config.3.1
##################################################################################################################################################################################################### 100.0%
[OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/poduser-3.1.yaml
[OK] kubectl create configmap abcdesktop-config --from-file=od.config -n abcdesktop
[OK] label configmap abcdesktop-config abcdesktop/role=pyos.config
[INFO] kubectl create -f poduser.yaml
[OK] kubectl create -f poduser.yaml
[INFO] waiting for pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 Ready
[OK] pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 condition met
[INFO] deleting for pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 Ready
[OK] pod "anonymous-74bea267-8197-4b1d-acff-019b24e778c5" deleted
[OK] role.rbac.authorization.k8s.io/pyos-role created
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
[INFO] waiting for pod/memcached-od-5ff8844d56-6dt28 Ready
[OK] pod/memcached-od-5ff8844d56-6dt28 condition met
[INFO] waiting for pod/mongodb-od-77c945467d-r82kv Ready
[OK] pod/mongodb-od-77c945467d-r82kv condition met
[INFO] waiting for pod/nginx-od-7445969696-6z88w Ready
[OK] pod/nginx-od-7445969696-6z88w condition met
[INFO] waiting for pod/openldap-od-5bbdd75864-d5bpq Ready
[OK] pod/openldap-od-5bbdd75864-d5bpq condition met
[INFO] waiting for pod/pyos-od-7584db6787-vnp64 Ready
[OK] pod/pyos-od-7584db6787-vnp64 condition met
[INFO] waiting for pod/speedtest-od-7f5484966f-jsb2m Ready
[OK] pod/speedtest-od-7f5484966f-jsb2m condition met
[INFO] list all pods in namespace abcdesktop
NAME                            READY   STATUS    RESTARTS   AGE
memcached-od-5ff8844d56-6dt28   1/1     Running   0          40s
mongodb-od-77c945467d-r82kv     1/1     Running   0          40s
nginx-od-7445969696-6z88w       1/1     Running   0          40s
openldap-od-5bbdd75864-d5bpq    1/1     Running   0          38s
pyos-od-7584db6787-vnp64        1/1     Running   0          39s
speedtest-od-7f5484966f-jsb2m   1/1     Running   0          39s
[INFO] Setup done
[INFO] Checking the service url on http://localhost:30443
[INFO] service status is down
[INFO] Looking for a free tcp port from 30443
[OK] get a free tcp port from 30443

[INFO] If you're using a cloud provider
[INFO] Forwarding abcdesktop service for you on port=30443
[INFO] For you setup is running the command 'kubectl port-forward nginx-od-b8c8c7b95-lkjl6 --address 0.0.0.0 30443:80 -n abcdesktop'
[OK] Please open your web browser and connect to

[INFO] http://localhost:30443/
```



The command above downloads the latest release (numerically) of abcdesktop.io. 
The quick installation process runs the all commands step by step:

* create the `abcdesktop` namespace
* create clusterRole and service account
* build all `rsa` keys pairs for jwt signing and payload encryption
* download the default configuration file `od.config`
* create all `services`, `deployments`, `secrets` and `configmaps`
* fetch pod user's container images


## Change the default namespace

You may need to replace the default namespace `abcdesktop` by your own. The `install-3.1.sh` bash script allow you to set the new namespace as an option.

```bash
wget https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-3.1.sh
chmod 755 install-3.1.sh 
```

Run `install-3.1.sh`

```bash
./install-3.1.sh --namespace superdesktop
```

```
[INFO] abcdesktop install script namespace=superdesktop
[OK] kubectl version
[OK] openssl version
[OK] kubectl create namespace superdesktop
[OK] create secret generic abcdesktopjwtdesktoppayload
[OK] create secret generic abcdesktopjwtdesktopsigning
[OK] create secret generic abcdesktopjwtusersigning
[OK] label secret abcdesktopjwtdesktoppayload
[OK] label secret abcdesktopjwtdesktopsigning
[OK] label secret abcdesktopjwtusersigning
[OK] use local file abcdesktop.yaml
[OK] use local file od.config
[OK] use local file poduser.yaml
[OK] updated abcdesktop.yaml file with new namespace superdesktop
[OK] updated abcdesktop.yaml file with new fqdn superdesktop.svc.cluster.local
[OK] updated od.config file with new namespace superdesktop
[OK] updated od.config file with new fqdn superdesktop.svc.cluster.local
[OK] updated poduser.yaml file with new superdesktop
[OK] kubectl create configmap abcdesktop-config --from-file=od.config -n superdesktop
[OK] label configmap abcdesktop-config abcdesktop/role=pyos.config
[INFO] kubectl create -f poduser.yaml
[OK] kubectl create -f poduser.yaml
[INFO] waiting for pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 Ready
[OK] pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 condition met
[INFO] deleting for pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 Ready
[OK] pod "anonymous-74bea267-8197-4b1d-acff-019b24e778c5" deleted
[OK] role.rbac.authorization.k8s.io/pyos-role created
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
[INFO] waiting for pod/memcached-od-5ff8844d56-b75fb Ready
[OK] pod/memcached-od-5ff8844d56-b75fb condition met
[INFO] waiting for pod/mongodb-od-77c945467d-t8cv7 Ready
[OK] pod/mongodb-od-77c945467d-t8cv7 condition met
[INFO] waiting for pod/nginx-od-b8c8c7b95-lkjl6 Ready
[OK] pod/nginx-od-b8c8c7b95-lkjl6 condition met
[INFO] waiting for pod/openldap-od-56b6564c85-2npln Ready
[OK] pod/openldap-od-56b6564c85-2npln condition met
[INFO] waiting for pod/pyos-od-67dfc48d84-kww9n Ready
[OK] pod/pyos-od-67dfc48d84-kww9n condition met
[INFO] waiting for pod/speedtest-od-894b7c886-69vc4 Ready
[OK] pod/speedtest-od-894b7c886-69vc4 condition met
[INFO] list all pods in namespace superdesktop
NAME                            READY   STATUS    RESTARTS   AGE
memcached-od-5ff8844d56-b75fb   1/1     Running   0          20s
mongodb-od-77c945467d-t8cv7     1/1     Running   0          20s
nginx-od-b8c8c7b95-lkjl6        1/1     Running   0          20s
openldap-od-56b6564c85-2npln    1/1     Running   0          18s
pyos-od-67dfc48d84-kww9n        1/1     Running   0          20s
speedtest-od-894b7c886-69vc4    1/1     Running   0          20s
[INFO] Setup done
[INFO] Checking the service url on http://localhost:30443
[INFO] service status is down
[INFO] Looking for a free tcp port from 30443
[OK] get a free tcp port from 30443

[INFO] If you're using a cloud provider
[INFO] Forwarding abcdesktop service for you on port=30443
[INFO] For you setup is running the command 'kubectl port-forward nginx-od-b8c8c7b95-lkjl6 --address 0.0.0.0 30443:80 -n superdesktop'
[OK] Please open your web browser and connect to

[INFO] http://localhost:30443/
```





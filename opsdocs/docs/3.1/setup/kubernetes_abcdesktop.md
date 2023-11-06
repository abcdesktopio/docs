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

## Manually installation step by step (Linux, macOS or Windows)

The following commands will let you deploy an abcdesktop on the master node. All applications run on a single server.  


### Install abcdesktop
#### Step 1: Create abcdesktop namespace

We will create the abcdesktop namespace and set it as default :

```
kubectl create namespace abcdesktop
```

You should read on the standard output

```
namespace/abcdesktop created
```


####  Step 2: Secure abcdesktop JWT exchange


User JWT is signed. So we need to define a (private, public) RSA keys for signing.
 Desktop JWT is encrypted AND signed. So we need to define a (private, public) RSA keys for signing, and a (private, public) RSA keys to encrypt data.

* The JWT payload is encrypted with the abcdesktop jwt desktop payload private by pyos
* The JWT payload is decrypted with the abcdesktop jwt desktop payload public keys by nginx.

> Please use the payload private as private key, and the payload public as private key. 
> Do not publish the public key. This public key must stay private, this is a special case, this is not stupid, it's only a more secure option.

* The JSON Web Tokens payload is signed with the abcdesktop jwt desktop signing private keys
* The JSON Web Tokens payload is verified with the abcdesktop jwt desktop signing public keys.

* The JSON Web Tokens user is signed with the abcdesktop jwt user signing private keys by pyos.
* The JSON Web Tokens user is verified with the abcdesktop jwt user signing public keys by pyos
> As multiple pods of pyos can run simultaneously, the same private and public keys value are stored into kubernetes secret.

The abcdesktop jwt desktop payload public key is read by `nginx lua script`. The exported the public key need the `RSAPublicKey_out` option, to use the `RSAPublicKey` format. The `RSAPublicKey` format make key file format compatible between `python 3.x jwt module` and `lua jwt lib`.


The following commands will let you create all necessary keys :

```
openssl genrsa -out abcdesktop_jwt_desktop_payload_private_key.pem 1024
openssl rsa -in abcdesktop_jwt_desktop_payload_private_key.pem -outform PEM -pubout -out  _abcdesktop_jwt_desktop_payload_public_key.pem
openssl rsa -pubin -in _abcdesktop_jwt_desktop_payload_public_key.pem -RSAPublicKey_out -out abcdesktop_jwt_desktop_payload_public_key.pem
openssl genrsa -out abcdesktop_jwt_desktop_signing_private_key.pem 1024
openssl rsa -in abcdesktop_jwt_desktop_signing_private_key.pem -outform PEM -pubout -out abcdesktop_jwt_desktop_signing_public_key.pem
openssl genrsa -out abcdesktop_jwt_user_signing_private_key.pem 1024
openssl rsa -in abcdesktop_jwt_user_signing_private_key.pem -outform PEM -pubout -out abcdesktop_jwt_user_signing_public_key.pem
```

Then, create the kubernetes secrets from the new key files:

```
kubectl create secret generic abcdesktopjwtdesktoppayload --from-file=abcdesktop_jwt_desktop_payload_private_key.pem --from-file=abcdesktop_jwt_desktop_payload_public_key.pem --namespace=abcdesktop
kubectl create secret generic abcdesktopjwtdesktopsigning --from-file=abcdesktop_jwt_desktop_signing_private_key.pem --from-file=abcdesktop_jwt_desktop_signing_public_key.pem --namespace=abcdesktop
kubectl create secret generic abcdesktopjwtusersigning --from-file=abcdesktop_jwt_user_signing_private_key.pem --from-file=abcdesktop_jwt_user_signing_public_key.pem --namespace=abcdesktop
```

You should read on the standard output :

```
secret/abcdesktopjwtdesktoppayload created
secret/abcdesktopjwtdesktopsigning created
secret/abcdesktopjwtusersigning created
```

##### Verify Secrets
You can verify secrets creation with the following command :

```
kubectl get secrets -n abcdesktop
```

You should read on the standard output :

```
NAME                          TYPE                                  DATA   AGE
abcdesktopjwtdesktoppayload   Opaque                                2      68s
abcdesktopjwtdesktopsigning   Opaque                                2      68s
abcdesktopjwtusersigning      Opaque                                2      67s
```


#### Step 3: Download user pod images

Create a pod user to make sure that Kubernetes will find the docker images at startup time. 
 
```
kubectl create -f https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/poduser-3.1.yaml
```

You should read on stdout

```
pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 created
```

You can wait for user pod is `Ready`, this while take a while, for 
container images are downloading.

```
kubectl wait --for=condition=Ready pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5  -n abcdesktop --timeout=-1s
```

```
pod/anonymous-74bea267-8197-4b1d-acff-019b24e778c5 condition met
```

You can delete the user pod `anonymous-74bea267-8197-4b1d-acff-019b24e778c5`. The container images are downloaded.

```
kubectl delete -f https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/poduser-3.1.yaml
```


### Step 4: Download and create the abcdesktop config file 

Download the od.config file. This is the main configuration file for `pyos` control plane.

```
curl https://raw.githubusercontent.com/abcdesktopio/conf/main/reference/od.config.3.1 --output od.config
```

Create the config map `abcdesktop-config` in the `abcdesktop` namespace

``` bash
kubectl create configmap abcdesktop-config --from-file=od.config -n abcdesktop
```

You should read on sdtout

```
configmap/abcdesktop-config created
```

### Step 5: Create the abcdesktop pods and services

abcdesktop.yaml file contains declarations for all roles, service account, pods, and services required for abcdesktop.

Run the command line

``` bash
kubectl create -f https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/abcdesktop-3.1.yaml
```

You should read on the standard output

``` bash
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
```

##### Verify Pods

Once the pods are created, all pods should be in `Running` status.  
For the first time, please wait for downloading all container images. 
It can take a while.

``` bash
kubectl get pods -n abcdesktop
```

You should read on the standard output

``` bash
NAME                            READY   STATUS    RESTARTS   AGE
memcached-od-5ff8844d56-jv4bh   1/1     Running   0          18s
mongodb-od-77c945467d-9xbnw     1/1     Running   0          18s
nginx-od-7445969696-mwlc9       1/1     Running   0          18s
openldap-od-5bbdd75864-c6th9    1/1     Running   0          18s
pyos-od-7584db6787-tjlvk        1/1     Running   0          18s
speedtest-od-7f5484966f-cxwpr   1/1     Running   0          18s
```

### Connect your local abcdesktop

Open your navigator to http://[your-ip-hostname]:30443/

abcdesktop homepage should be available :

![abcdesktop Anonymous login](../../setup/img/kubernetes-setup-login-anonymous-3.1.png)

Click on the **Connect with Anonymous** access button. abcdesktop service pyos is creating a new pod.

![abcdesktop main screen login pending](../../setup/img/kubernetes-setup-login-anonymous.pending-3.1.png)

Few seconds later, processes are ready to run. You should see the abcdesktop main screen, with no application in the dock.

![abcdesktop main screen ready](../../setup/img/kubernetes-setup-login-anonymous.done-3.1.png)

Also, you can run again the command 

``` bash
kubectl get pods -n abcdesktop
```

You should see that the `anonymous-XXXXX` pod have been created and is `Running`

``` bash
NAME                            READY   STATUS    RESTARTS   AGE
anonymous-50b0f                 4/4     Running   0          5m22s
memcached-od-5ff8844d56-jv4bh   1/1     Running   0          77m
mongodb-od-77c945467d-9xbnw     1/1     Running   0          77m
nginx-od-7445969696-mwlc9       1/1     Running   0          77m
openldap-od-5bbdd75864-c6th9    1/1     Running   0          77m
pyos-od-7584db6787-tjlvk        1/1     Running   0          77m
speedtest-od-7f5484966f-cxwpr   1/1     Running   0          77m
```

Great you have installed abcdesktop.io.
You just need a web browser to reach your web workspace. It' now time to add some container applications.
Read the next chapter to add applications





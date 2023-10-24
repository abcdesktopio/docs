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
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-3.0.sh | bash
```

The command above downloads the latest release (numerically) of abcdesktop.io. 
The quick installation process runs the all commands step by step:

* create the `abcdesktop` namespace
* create clusterRole and service account
* build all `rsa` keys pairs for jwt signing and payload encryption
* download the default configuration file `od.config`
* create all `services`, `deployments`, `secrets` and `configmaps`
* fetch pod user's container images


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

> Option :
> To use the namespace ```abcdestkop``` as default namespace 
>```
>kubectl config set-context $(kubectl config current-context) --namespace=abcdesktop
>```
>
>All kubectl commands will be executed with abcdesktop namespace.  
>This will avoid to add "-n abcdesktop" to all commands.
>


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
# build rsa kay pairs for jwt payload 
# 1024 bits is a smallest value, change here if need but use more than 1024
openssl genrsa  -out abcdesktop_jwt_desktop_payload_private_key.pem 1024
openssl rsa     -in  abcdesktop_jwt_desktop_payload_private_key.pem -outform PEM -pubout -out  _abcdesktop_jwt_desktop_payload_public_key.pem
openssl rsa -pubin -in _abcdesktop_jwt_desktop_payload_public_key.pem -RSAPublicKey_out -out abcdesktop_jwt_desktop_payload_public_key.pem

# build rsa kay pairs for the desktop jwt signing 
openssl genrsa -out abcdesktop_jwt_desktop_signing_private_key.pem 1024
openssl rsa     -in abcdesktop_jwt_desktop_signing_private_key.pem -outform PEM -pubout -out abcdesktop_jwt_desktop_signing_public_key.pem

# build rsa kay pairs for the user jwt signing 
openssl genrsa -out abcdesktop_jwt_user_signing_private_key.pem 1024
openssl rsa     -in abcdesktop_jwt_user_signing_private_key.pem -outform PEM -pubout -out abcdesktop_jwt_user_signing_public_key.pem

```

Then, create the kubernetes secrets from the new key files:

```
# create the kubernetes rsa keys secret for abcdesktop
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


>
>Only if you use a private registry or if the abcdesktop registry is private
>Create Secret to allow kubernetes to download abcdesktop images from docker registry.  
>For this part you need to change docker-username and docker-password by credentials provided by project owner.
>If you don't have this values, you will have to build abcdesktop images by yourself.
>
>change docker.json path if need /root/.docker/config.json 
>`kubectl create secret generic abcdesktopregistrysecret --from-file=.dockerconfigjson=/root/.docker/config.json --type=kubernetes.io/dockerconfigjson -n abcdesktop`
>
>


##### Verify Secrets
You can verify secrets creation with the following command :

```
kubectl get secrets -n abcdesktop
```

You should read on the standard output :

```
NAME                           TYPE                                  DATA   AGE
default-token-5zknd            kubernetes.io/service-account-token   3      6m6s
abcdesktopjwtdesktoppayload   Opaque                                2      68s
abcdesktopjwtdesktopsigning   Opaque                                2      68s
abcdesktopjwtusersigning      Opaque                                2      67s
```


#### Step 3: Download user pod images

Create a pod user to make sure that Kubernetes will find the docker images at startup time. 
 
```
kubectl create -f https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/poduser.yaml
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

You can delete the user pod `anonymous-74bea267-8197-4b1d-acff-019b24e778c5`. This container images are downloaded.

```
kubectl delete -f https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/poduser.yaml
```


### Step 4: Download and create the abcdesktop config file 

Download the od.config file. This is the main file for `pyos` control plane.

```
curl https://raw.githubusercontent.com/abcdesktopio/conf/main/reference/od.config.3.0 --output od.config
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
kubectl create -f https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/abcdesktop-3.0.yaml
```

You should read on the standard output

``` bash
clusterrole.rbac.authorization.k8s.io/pyos-role created
clusterrolebinding.rbac.authorization.k8s.io/pyos-rbac created
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
memcached-od-57c57c4f9d-92fs2   1/1     Running   0          59m
mongodb-od-f69ff6b5b-v6ztc      1/1     Running   0          59m
nginx-od-58f86c4dc8-8n9lf       1/1     Running   0          59m
openldap-od-d66d66bf4-84lg8     1/1     Running   0          59m
pyos-od-5586b88767-6gdtk        1/1     Running   0          59m
speedtest-od-6c59bdff75-n6s66   1/1     Running   0          59m
```

### Connect your local abcdesktop

Open your navigator to http://[your-ip-hostname]:30443/

abcdesktop homepage should be available :

![abcdesktop Anonymous login](../../setup/img/kubernetes-setup-login-anonymous.png)

Click on the **Connect with Anonymous** access button. abcdesktop service pyos is creating a new pod.

![abcdesktop main screen login pending](../../setup/img/kubernetes-setup-login-anonymous.pending.png)

Few seconds later, processes are ready to run. You should see the abcdesktop main screen, with no application in the dock.

![abcdesktop main screen ready](../../setup/img/kubernetes-setup-login-anonymous.done.png)

Great you have installed abcdesktop.io in Kubernetes mode.
You just need a web browser to reach your web workspace. It' now time to add some container applications.
Read the chapter add kubernetes contain

### Troubleshoot

All kubernetes resources can be inspected to get more informations.

First list elements you want to verify, in the following case, we will inspect pods :

```bash
kubectl get pods -n abcdesktop
```

```
NAME                            READY   STATUS             RESTARTS   AGE
nginx-od-db69c45fb-qnd4n        1/1     Running            0          92s
pyos-od-5586b88767-6gdtk        1/1     Running            0          92s
memcached-od-db69c45fb-mqt4n    1/1     Running            0          92s
mongodb-od-ff874fcb5-sm6f7      1/1     Running            0          92s
speedtest-od-55c58fdd69-5znpr   0/1     ImagePullBackOff   0          92s
```

As we can see, status is "ImagePullBackOff" for speedtest-od pod.  
We will then ask kubernetes to describe the pod with the following command :

`
kubectl describe pod speedtest-od-55c58fdd69-t99ck -n abcdesktop
`

In this case, the important information part is at the end (it's not always the case, you can also look at "Conditions:" section) :

``` bash
    Events:
      Type     Reason   Age                    From             Message
      ----     ------   ----                   ----             -------
      Warning  Failed   7m6s (x4837 over 18h)  kubelet, cube05  Error: ImagePullBackOff
      Normal   BackOff  2m9s (x4860 over 18h)  kubelet, cube05  Back-off pulling image "registry.mydomain.local:443/oc.speedtest"
```

As we can see, in this case, Kubernetes had a problem to pull oc.speedtest image from registry.

##### Verify the deployments

```bash
kubectl get deployment -n abcdesktop
```

You should read on the standard output

```
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
memcached-od   1/1     1            1           10m
mongodb-od     1/1     1            1           10m
nginx-od       1/1     1            1           4m26s
openldap-od    1/1     1            1           10m
pyos-od        1/1     1            1           3m2s
speedtest-od   1/1     1            1           10m
```


##### Verify service ports

```bash
kubectl get services -n abcdesktop
```

You should read on the standard output

```
NAME        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
desktop     ClusterIP   None             <none>        <none>            11m
memcached   ClusterIP   10.107.106.62    <none>        11211/TCP         11m
mongodb     ClusterIP   10.96.113.246    <none>        27017/TCP         11m
nginx       NodePort    10.100.253.228   <none>        80:30443/TCP      11m
openldap    ClusterIP   10.105.69.239    <none>        389/TCP,636/TCP   11m
pyos        ClusterIP   10.98.97.186     <none>        8000/TCP          11m
speedtest   ClusterIP   10.109.48.166    <none>        80/TCP            11m
```

##### Verify cluster roles 


> cluster roles are disable by default

```bash
kubectl describe ClusterRole pyos-role -n abcdesktop
```

You should read on the standard output

```
Name:         pyos-role
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources                 Non-Resource URLs  Resource Names  Verbs
  ---------                 -----------------  --------------  -----
  pods/ephemeralcontainers  []                 []              [create get list watch update patch delete]
  pods/exec                 []                 []              [create get list watch update patch delete]
  persistentvolumes         []                 []              [get list create delete]
  persistentvolumeclaims    []                 []              [get list update create delete]
  configmaps                []                 []              [get list watch create update patch delete]
  pods                      []                 []              [get list watch create update patch delete]
  secrets                   []                 []              [get list watch create update patch delete]
  events                    []                 []              [get list watch]
  pods/log                  []                 []              [get list watch]
  endpoints                 []                 []              [get list]
  nodes                     []                 []              [get watch list]
```  

##### Verify Cluster Role Bindind


> cluster roles Bindind are disable by default

```bash
kubectl describe ClusterRoleBinding pyos-rbac -n abcdesktop
```

You should read on the standard output

```
Name:         pyos-rbac
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  ClusterRole
  Name:  pyos-role
Subjects:
  Kind            Name                 Namespace
  ----            ----                 ---------
  ServiceAccount  pyos-serviceaccount  abcdesktop
```


### Read pyos logs

```bash
kubectl logs -l run=pyos-od -n abcdesktop --follow -n abcdesktop
```

You should read on the standard output

```
2023-05-17 13:29:08 od [INFO   ] __main__.trace_request:anonymous /healthz
2023-05-17 13:29:18 od [INFO   ] __main__.trace_request:anonymous /healthz
2023-05-17 13:29:28 od [INFO   ] __main__.trace_request:anonymous /healthz
2023-05-17 13:29:38 od [INFO   ] __main__.trace_request:anonymous /healthz
2023-05-17 13:29:48 od [INFO   ] __main__.trace_request:anonymous /healthz
2023-05-17 13:29:58 od [INFO   ] __main__.trace_request:anonymous /healthz
2023-05-17 13:30:08 od [INFO   ] __main__.trace_request:anonymous /healthz
2023-05-17 13:30:18 od [INFO   ] __main__.trace_request:anonymous /healthz
2023-05-17 13:30:28 od [INFO   ] __main__.trace_request:anonymous /healthz
2023-05-17 13:30:38 od [INFO   ] __main__.trace_request:anonymous /healthz
2023-05-17 13:30:48 od [INFO   ] __main__.trace_request:anonymous /healthz
```


### Rollout deployment

To rollout restart the abcdesktop deployment

```bash
kubectl rollout restart deployment -n abcdesktop
```

You should read on the standard output 

```
deployment.apps/memcached-od restarted
deployment.apps/mongodb-od restarted
deployment.apps/nginx-od restarted
deployment.apps/openldap-od restarted
deployment.apps/pyos-od restarted
deployment.apps/speedtest-od restarted
```

Check the pods status  

```bash
kubectl get pods -n abcdesktop
```

You should read on the standard output 

```
NAME                            READY   STATUS        RESTARTS   AGE
memcached-od-64c56f9458-jcf9x   1/1     Running       0          32s
mongodb-od-5b5cc9946d-q7fph     1/1     Running       0          32s
nginx-od-58bdf79df4-skjsn       1/1     Running       0          32s
openldap-od-6dcc5d7f8b-g8gvj    1/1     Running       0          32s
pyos-od-784bd7b5c5-tdzxx        1/1     Running       0          32s
speedtest-od-5ff99b6579-st9jx   1/1     Running       0          32s
```


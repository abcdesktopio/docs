# Quick installation with a bash script

## Requirements

- kubernetes cluster `READY` to run
- `kubectl` command-line tool must be configured to communicate with your cluster. 
- `openssl` and `curl` command line must be installed too (only for install using kubectl). 

You can run the **Quick installation process** or choose the **Manually installation step by step**

> Linux operating system is recommanded to run abcdesktop.io.


## Quick installation (Linux or macOS)

> Quick installation can be run on Linux or macOS operation system, using `kubectl` command

### Install using kubectl on Linux or macOS operation system

Download and extract the latest release automatically

```
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-4.3.sh | bash
```

<div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/vEEXVOT30w4" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> </iframe></div>

You can read on stdout 

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
[OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/abcdesktop-4.3.yaml
[OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/reference/od.config.4.3
[OK] kubectl create configmap abcdesktop-config --from-file=od.config -n abcdesktop
[OK] label configmap abcdesktop-config abcdesktop/role=pyos.config
role.rbac.authorization.k8s.io/pyos-role created
rolebinding.rbac.authorization.k8s.io/pyos-rbac created
serviceaccount/pyos-serviceaccount created
configmap/configmap-mongodb-scripts created
secret/secret-mongodb created
deployment.apps/mongodb-od created
deployment.apps/memcached-od created
deployment.apps/router-od created
deployment.apps/nginx-od created
deployment.apps/speedtest-od created
deployment.apps/pyos-od created
deployment.apps/console-od created
deployment.apps/openldap-od created
endpoints/desktop created
service/desktop created
service/memcached created
service/mongodb created
service/speedtest created
service/pyos created
service/console created
service/http-router created
service/website created
service/openldap created
[INFO] waiting for deployment/console-od available
[OK] deployment.apps/console-od condition met
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
[INFO] waiting for deployment/router-od available
[OK] deployment.apps/router-od condition met
[INFO] waiting for deployment/speedtest-od available
[OK] deployment.apps/speedtest-od condition met
[INFO] list all pods in namespace abcdesktop
NAME                            READY   STATUS    RESTARTS   AGE
console-od-844c749f85-vbbb7     1/1     Running   0          32s
memcached-od-d4b6b6867-tbfgf    1/1     Running   0          33s
mongodb-od-5d996fd57b-tcn45     1/1     Running   0          33s
nginx-od-796c7d7d6b-lgnjb       1/1     Running   0          33s
openldap-od-567dcf7bf6-h2nq9    1/1     Running   0          32s
pyos-od-8d4988b56-vcd7z         1/1     Running   0          32s
router-od-f5458658-b52hj        1/1     Running   0          33s
speedtest-od-7fcc9649b4-qllr7   1/1     Running   0          32s
[INFO] Setup done
[INFO] Checking the service url on http://localhost:30443
[INFO] service status is down
[INFO] Looking for a free TCP port from 30443
[OK] Get a free TCP port from 30443
[INFO] If you're using a cloud provider
[INFO] Forwarding abcdesktop service for you on port=30443
[INFO] For you setup is running the command 'kubectl port-forward nginx-od-796c7d7d6b-lgnjb --address 0.0.0.0 30443:80 -n abcdesktop'
[OK] Port-Forward successful
[OK] Please open your web browser and connect to

[INFO] http://localhost:30443/

```

The command above downloads the latest release of abcdesktop.io. 

The quick installation process runs the commands step by step :

* create the `abcdesktop` namespace
* build all `rsa` keys for jwt signing and payload encryption, using openssl command line
* create all `service account`, `services`, `deployments`, `secrets` and `configmaps` from the [abcdesktop.yaml](https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-4.3.yaml)
* download and create the default configuration file [od.config](https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/reference/od.config.4.3)

> This install process doesn't install applications for your desktop, you get a desktop with few applications in your dock

## Quick installation (Microsoft Windows)

If you are using a Microsoft Windows operating system please follow the dedicated link below  
[Quick install for windows](./kubernetes_abcdesktop_windows.md)


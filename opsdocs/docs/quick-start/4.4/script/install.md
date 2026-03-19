# Quick installation (Linux or macOS)

> Quick installation can be run on Linux or macOS operation system, using `kubectl` command

## Run the install script

Download and extract the latest release automatically

```
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-4.4.sh | bash
```

<div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/vEEXVOT30w4" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen> </iframe></div>

You can read on stdout 

??? note "show details"
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
    [OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/abcdesktop-4.4.yaml
    [OK] downloaded source https://raw.githubusercontent.com/abcdesktopio/conf/main/reference/od.config.4.4
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

The command above downloads the latest release (numerically) of abcdesktop.io. 
The quick installation process runs the commands step by step :

* create the `abcdesktop` namespace
* build all `rsa` keys for jwt signing and payload encryption, using openssl command line
* create all `service account`, `services`, `deployments`, `secrets` and `configmaps` from the [abcdesktop.yaml](https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/kubernetes/abcdesktop-4.4.yaml)
* download and create the default configuration file [od.config](https://raw.githubusercontent.com/abcdesktopio/conf/refs/heads/main/reference/od.config.4.4)

> This install process doesn't install applications for your desktop, you get a desktop with few applications in your dock

## Change the default namespace

You may need to replace the default namespace `abcdesktop` by your own during the install process. The `install-4.4.sh` bash script allow you to set the new namespace as an option.

```bash
wget https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/install-4.4.sh
chmod 755 install-4.4.sh
```

Run `install-4.4.sh`

```bash
./install-4.4.sh --namespace superdesktop
```

??? note "show details"
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
    [OK] updated abcdesktop.yaml file with new namespace superdesktop
    [OK] updated abcdesktop.yaml file with new fqdn superdesktop.svc.cluster.local
    [OK] updated od.config file with new namespace superdesktop
    [OK] updated od.config file with new fqdn superdesktop.svc.cluster.local
    [OK] kubectl create configmap abcdesktop-config --from-file=od.config -n superdesktop
    [OK] label configmap abcdesktop-config abcdesktop/role=pyos.config
    [OK] default account is created
    [OK] role.rbac.authorization.k8s.io/pyos-role created
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
    [OK] pyos-serviceaccount account is created
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
    [INFO] waiting for pod/console-od-79bf9bf475-gbb62 Ready
    [OK] pod/console-od-79bf9bf475-gbb62 condition met
    [INFO] waiting for pod/memcached-od-d4b6b6867-c8b4p Ready
    [OK] pod/memcached-od-d4b6b6867-c8b4p condition met
    [INFO] waiting for pod/mongodb-od-5d996fd57b-z2pjl Ready
    [OK] pod/mongodb-od-5d996fd57b-z2pjl condition met
    [INFO] waiting for pod/nginx-od-57dccb8cf9-txgzc Ready
    [OK] pod/nginx-od-57dccb8cf9-txgzc condition met
    [INFO] waiting for pod/openldap-od-6955699d5-qhjzr Ready
    [OK] pod/openldap-od-6955699d5-qhjzr condition met
    [INFO] waiting for pod/pyos-od-777747f64b-r87x5 Ready
    [OK] pod/pyos-od-777747f64b-r87x5 condition met
    [INFO] waiting for pod/router-od-59d67d664f-f56m8 Ready
    [OK] pod/router-od-59d67d664f-f56m8 condition met
    [INFO] waiting for pod/speedtest-od-67db77f86f-wqkb7 Ready
    [OK] pod/speedtest-od-67db77f86f-wqkb7 condition met
    [INFO] list all pods in namespace superdesktop
    NAME                            READY   STATUS    RESTARTS   AGE
    console-od-79bf9bf475-gbb62     1/1     Running   0          12s
    memcached-od-d4b6b6867-c8b4p    1/1     Running   0          13s
    mongodb-od-5d996fd57b-z2pjl     1/1     Running   0          13s
    nginx-od-57dccb8cf9-txgzc       1/1     Running   0          13s
    openldap-od-6955699d5-qhjzr     1/1     Running   0          12s
    pyos-od-777747f64b-r87x5        1/1     Running   0          13s
    router-od-59d67d664f-f56m8      1/1     Running   0          13s
    speedtest-od-67db77f86f-wqkb7   1/1     Running   0          13s
    [INFO] Setup done
    [INFO] Checking the service url on http://localhost:30443

    [OK] Please open your web browser and connect to http://localhost:30443/
    ```

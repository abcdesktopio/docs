Uninstall abcdesktop for kubernetes

# Command to uninstall abcdesktop release 3.2 

To uninstall abcdesktop. Choose run run the `uninstall-3.2.sh` bash script using a curl.

## Quick uninstallation abcdesktop (Windows)

If you are using a Windows operating system please click on the link below  
[Quick uninstall for windows](./uninstall_kubernetes_windows.md)

## Quick uninstallation abcdesktop (Linux or macOS)

> Quick uninstallation can be run on Linux or macOS operation system. 


Download and extract the uninstall bash script (Linux or macOS):

```bash
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-3.2.sh | bash
```

You should read on stdout 

```bash
abcdesktop uninstall script namespace=abcdesktop
[OK] kubectl version
[OK] kubectl get namespace abcdesktop
[OK] delete pods --selector="type=x11server" -n abcdesktop
[OK] use local file abcdesktop.yaml
role.rbac.authorization.k8s.io "pyos-role" deleted
rolebinding.rbac.authorization.k8s.io "pyos-rbac" deleted
serviceaccount "pyos-serviceaccount" deleted
configmap "configmap-mongodb-scripts" deleted
configmap "nginx-config" deleted
secret "secret-mongodb" deleted
deployment.apps "mongodb-od" deleted
deployment.apps "memcached-od" deleted
deployment.apps "nginx-od" deleted
deployment.apps "speedtest-od" deleted
deployment.apps "pyos-od" deleted
endpoints "desktop" deleted
service "desktop" deleted
service "memcached" deleted
service "mongodb" deleted
service "speedtest" deleted
service "nginx" deleted
service "pyos" deleted
deployment.apps "openldap-od" deleted
service "openldap" deleted
[OK] kubectl delete -f abcdesktop.yaml
[OK] kubectl delete secrets --all -n abcdesktop
[OK] kubectl delete configmap --all -n abcdesktop
[OK] kubectl delete pvc --all -n abcdesktop
[INFO] deleting namespace abcdesktop
[OK] namespace "abcdesktop" deleted
```

Please wait for the output message: 

```
[OK] namespace "abcdesktop" deleted
```

Great, you have uninstalled abcdesktop for kubernetes.


## uninstall with a dedicated namespace


```bash
wget https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-3.2.sh
chmod 755 uninstall-3.2.sh
```

Run the `uninstall-3.2.sh` command line with your own namespace

```
./uninstall-3.2.sh --namespace superdesktop
```

You should read on stdout

```
abcdesktop uninstall script namespace=superdesktop
[OK] kubectl version
[OK] kubectl get namespace superdesktop
[OK] delete pods --selector="type=x11server" -n superdesktop
[OK] use local file abcdesktop.yaml
[OK] updated abcdesktop.yaml file with new namespace superdesktop
role.rbac.authorization.k8s.io "pyos-role" deleted
rolebinding.rbac.authorization.k8s.io "pyos-rbac" deleted
serviceaccount "pyos-serviceaccount" deleted
configmap "configmap-mongodb-scripts" deleted
configmap "nginx-config" deleted
secret "secret-mongodb" deleted
deployment.apps "mongodb-od" deleted
deployment.apps "memcached-od" deleted
deployment.apps "nginx-od" deleted
deployment.apps "speedtest-od" deleted
deployment.apps "pyos-od" deleted
endpoints "desktop" deleted
service "desktop" deleted
service "memcached" deleted
service "mongodb" deleted
service "speedtest" deleted
service "nginx" deleted
service "pyos" deleted
deployment.apps "openldap-od" deleted
service "openldap" deleted
[OK] kubectl delete -f abcdesktop.yaml
[OK] kubectl delete secrets --all -n superdesktop
[OK] kubectl delete configmap --all -n superdesktop
[OK] kubectl delete pvc --all -n superdesktop
[INFO] deleting namespace superdesktop
[OK] namespace "superdesktop" deleted
```

Great, you have uninstalled abcdesktop for kubernetes with a dedicated namespace.


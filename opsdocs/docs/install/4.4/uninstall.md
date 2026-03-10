
# Uninstall with a bash script 

To uninstall abcdesktop, run the `uninstall-4.3.sh` bash script using a curl command.

## Quick uninstallation abcdesktop (Linux or macOS)

> Quick uninstallation can be run on Linux or macOS operation system. 

Download and run the uninstall bash script (Linux or macOS):

```bash
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-4.3.sh | bash
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
secret "secret-mongodb" deleted
deployment.apps "mongodb-od" deleted
deployment.apps "memcached-od" deleted
deployment.apps "router-od" deleted
deployment.apps "nginx-od" deleted
deployment.apps "speedtest-od" deleted
deployment.apps "pyos-od" deleted
deployment.apps "console-od" deleted
deployment.apps "openldap-od" deleted
endpoints "desktop" deleted
service "desktop" deleted
service "memcached" deleted
service "mongodb" deleted
service "speedtest" deleted
service "pyos" deleted
service "console" deleted
service "http-router" deleted
service "website" deleted
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

## Quick uninstallation abcdesktop (Windows)

If you are using a Windows operating system please click on the link below  
[Quick uninstall for windows](./uninstall_kubernetes_windows.md)

Great, you have uninstalled abcdesktop for kubernetes.

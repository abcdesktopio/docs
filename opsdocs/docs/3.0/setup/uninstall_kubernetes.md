Uninstall abcdesktop for kubernetes

# Commands to uninstall abcdesktop release 3.0 

To uninstall abcdesktop. Choose run run the `uninstall-3.0.sh` bash script using a curl or run step by step uninstall commands manually.

## Quick uninstallation abcdesktop (Linux or macOS)

> Quick uninstallation can be run on Linux or macOS operation system. 


Download and extract the uninstall bash script (Linux or macOS):

```bash
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-3.0.sh | bash
```

You should read on stdout 

```bash
starting abcdesktop uninstall commands start at 1669824908 epoch seconds
stop and remove abcdesktop user pods
pod "anonymous-33c30478-5cc0-4e18-b128-735694c98f3c" deleted
remove all services, pods
clusterrole.rbac.authorization.k8s.io "pyos-role" deleted
clusterrolebinding.rbac.authorization.k8s.io "pyos-rbac" deleted
serviceaccount "pyos-serviceaccount" deleted
storageclass.storage.k8s.io "storage-local-abcdesktop" deleted
configmap "nginx-config" deleted
deployment.apps "memcached-od" deleted
secret "mongodb-secret" deleted
deployment.apps "mongodb-od" deleted
daemonset.apps "daemonset-nginx" deleted
deployment.apps "speedtest-od" deleted
daemonset.apps "daemonset-pyos" deleted
endpoints "desktop" deleted
service "desktop" deleted
service "memcached" deleted
service "mongodb" deleted
service "speedtest" deleted
service "nginx" deleted
service "pyos" deleted
deployment.apps "openldap-od" deleted
service "openldap" deleted
remove all secrets
secret "abcdesktopjwtdesktoppayload" deleted
secret "abcdesktopjwtdesktopsigning" deleted
secret "abcdesktopjwtusersigning" deleted
remove all configmaps
configmap "abcdesktop-config" deleted
configmap "kube-root-ca.crt" deleted
remove all pvc
No resources found
remove all pv
No resources found
remove namespace
namespace "abcdesktop" deleted
abcdesktop is uninstalled, in 48 seconds
```

## Run step by step uninstall commands  

Run the bash commands from the `uninstall-3.0.sh` main content : 

```bash
echo "stop and remove abcdesktop user pods"
kubectl delete pods --selector="type=x11server" -n abcdesktop
echo "remove all services, pods"
kubectl delete -f https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/abcdesktop-3.0.yaml 
echo "remove all secrets"
kubectl delete secrets --all -n abcdesktop
echo "remove all configmaps"
kubectl delete cm --all -n abcdesktop
echo "remove all pvc"
kubectl delete pvc --all -n abcdesktop 2>/dev/null
echo "remove all pv"
kubectl delete pv --all -n abcdesktop  2>/dev/null
echo "remove namespace"
kubectl delete namespace abcdesktop
echo "abcdesktop is uninstalled"
```

The last command `kubectl delete namespace` can take few minutes.

Please wait for the output message: 

```
abcdesktop is uninstalled
```

Great, you have uninstalled abcdesktop for kubernetes.


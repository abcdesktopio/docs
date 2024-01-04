## Quick uninstallation abcdesktop (Windows)

> Quick uninstallation can be run on Windows operation system. 


Download and extract the uninstall PowerShell script (Windows):

```PowerShell
$script = curl https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-3.2.ps1 

Invoke-Expression $($script.Content)
```

You should read on stdout 

```
[INFO] abcdesktop uninstall script namespace=abcdesktop
[OK] kubectl version
[OK] kubectl get namespace abcdesktop
[OK] delete pods --selector=\
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
[INFO] delete abcdesktop related files
[OK] remove od.config abcdesktop.yaml poduser.yaml
[OK] remove *.pem
[INFO] abcdesktop was succesfully uninstalled
```

## Uninstall with a dedicated namespace


```PowerShell
curl https://raw.githubusercontent.com/Matt307082/powershell-scripts/master/uninstall-3.2.ps1 -OutFile uninstall-3.2.ps1
```

Run the `uninstall-3.2.ps1` command line with your own namespace

```PowerShell
.\uninstall-3.2.ps1 --namespace superdesktop
```

You should read on stdout

```
[INFO] abcdesktop uninstall script namespace=superdesktop
[OK] kubectl version
[OK] kubectl get namespace superdesktop
[OK] delete pods --selector=\
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
[INFO] delete abcdesktop related files
[OK] remove od.config abcdesktop.yaml poduser.yaml
[OK] remove *.pem
[INFO] abcdesktop was succesfully uninstalled
```

Uninstall abcdesktop for kubernetes

# Commands to uninstall abcdesktop release 3.0 



## Quick uninstallation abcdesktop (Linux or macOS)

> Quick installation can be run on Linux or macOS operation system. 


Download and extract the latest release automatically (Linux or macOS):

```
curl -sL https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/uninstall-3.0.sh | bash
```

## Run manually  

Run the bash commands : 

```bash
echo "starting abcdesktop uninstall commands"
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


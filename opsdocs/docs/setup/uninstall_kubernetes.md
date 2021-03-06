Uninstall abcdesktop.io for kuberntes

## Commands to uninstall abcdesktop.io 

Go to the abcdesktop directory (where the `abcdesktop.yml` is located), and run the bash commands  : 

```bash
echo "starting abcdesktop uninstall commands"
echo "stop and remove abcdesktop user pods"
kubectl delete pods --selector="type=x11server" -n abcdesktop
echo "remove all services, pods"
kubectl delete -f https://raw.githubusercontent.com/abcdesktopio/conf/main/kubernetes/abcdesktop.yaml
echo "remove all secrets"
kubectl delete secrets --all -n abcdesktop
echo "remove namespace"
kubectl delete namespace abcdesktop
echo "delete docker images"
docker images --filter=reference='abcdesktopio/*:*' --format "{{.Repository}}"  | xargs docker rmi
echo "abcdesktop is uninstalled"
```

Great, you have uninstalled abcdesktop for kubernetes.


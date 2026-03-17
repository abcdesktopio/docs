## Install using helm on Linux or macOS operation system

> Quick installation can be run using helm (version > 3)

``` shell
helm repo add abcdesktop https://abcdesktopio.github.io/helm/
helm repo update abcdesktop
helm install my-abcdesktop abcdesktop/abcdesktop --version {{ helm_version }} --create-namespace -n abcdesktop
```

``` shell
% helm repo add abcdesktop https://abcdesktopio.github.io/helm/
"abcdesktop" has been added to your repositories
% helm repo update abcdesktop                                  
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "abcdesktop" chart repository
Update Complete. ⎈Happy Helming!⎈
% helm install my-abcdesktop abcdesktop/abcdesktop --version {{ helm_version }} --create-namespace -n abcdesktop
NAME: my-abcdesktop
LAST DEPLOYED: Thu Sep 11 16:14:03 2025
NAMESPACE: abcdesktop
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

<div style="display: flex; justify-content: center;">
    <iframe width="640" height="480" 
        src="https://www.youtube.com/embed/86RLis48U0I" 
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" 
        allowfullscreen
    > </iframe>
</div>

> To get more details about the helm installation process and options, please read the documentation on [helm repository](https://github.com/abcdesktopio/helm)

When install your helm installation process is ready, you need to forward the pod's router tcp port 80 to your localhost port `30443` (for example)

``` bash
LOCAL_PORT=30443
NAMESPACE=abcdesktop
kubectl port-forward $(kubectl get pods -l run=router-od -o jsonpath={.items..metadata.name} -n ${NAMESPACE} ) --address 0.0.0.0 "${LOCAL_PORT}:80" -n ${NAMESPACE} 
```

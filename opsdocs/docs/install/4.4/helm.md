# Installation using helm lastest release {{ abcdesktop.latest_release }}

[![Artifact Hub](https://img.shields.io/endpoint?url=https://artifacthub.io/badge/repository/abcdesktop)](https://artifacthub.io/packages/search?repo=abcdesktop)

You can watch the youtube video sample. This video describes the Quick installation process using `helm`.

<div style="display: flex; justify-content: center;"><iframe width="640" height="480" src="https://www.youtube.com/embed/86RLis48U0I" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>

Add the `helm` repo and then install it on Linux or macOS or read the step by step installation process [abcdesktop for kubernetes](/{{ abcdesktop.latest_release }}/setup/kubernetes_abcdesktop)

<div class="artifacthub-widget" data-url="https://artifacthub.io/packages/helm/abcdesktop/abcdesktop" data-theme="light" data-header="false" data-stars="false" data-responsive="false"><blockquote><p lang="en" dir="ltr"><b>abcdesktop</b>: ABCDesktop helm chart</p>&mdash; Open in <a href="https://artifacthub.io/packages/helm/abcdesktop/abcdesktop">Artifact Hub</a></blockquote></div><script async src="https://artifacthub.io/artifacthub-widget.js"></script>

```
helm repo add abcdesktop https://abcdesktopio.github.io/helm/
helm install my-abcdesktop abcdesktop/abcdesktop --version {{ abcdesktop.latest_release }} --create-namespace -n abcdesktop
```

When install your helm installation process is ready, you need to forward the pod's router tcp port 80 to your localhost port 30443 (for example)

```bash
LOCAL_PORT=30443
NAMESPACE=abcdesktop
kubectl port-forward $(kubectl get pods -l run=router-od -o jsonpath={.items..metadata.name} -n ${NAMESPACE} ) --address 0.0.0.0 "${LOCAL_PORT}:80" -n ${NAMESPACE} 
```


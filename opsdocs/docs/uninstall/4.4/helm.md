---
tags:
  - uninstall
  - helm
---
# Uninstalling abcdesktop.io Using Helm

```bash
NAMESPACE=abcdesktop
helm uninstall abcdesktop -n ${NAMESPACE}
```

Set `NAMESPACE` to the Kubernetes namespace in which abcdesktop.io is deployed, and replace `abcdesktop` in the `helm uninstall` command with your Helm release name if it differs from the default.

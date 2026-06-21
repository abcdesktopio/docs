---
title: Uninstall abcdesktop.io Using Helm | abcdesktop.io
description: Procedure for completely removing an abcdesktop.io deployment from a Kubernetes cluster using Helm uninstall and namespace cleanup.
keywords: uninstall, Helm, remove, cleanup, Kubernetes, abcdesktop, namespace
tags:
  - uninstall
  - helm
  - Helm
---

# Uninstalling abcdesktop.io Using Helm

```bash
NAMESPACE=abcdesktop
helm uninstall abcdesktop -n ${NAMESPACE}
```

Set `NAMESPACE` to the Kubernetes namespace in which abcdesktop.io is deployed, and replace `abcdesktop` in the `helm uninstall` command with your Helm release name if it differs from the default.

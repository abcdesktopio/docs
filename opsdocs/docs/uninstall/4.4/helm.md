---
tags:
  - uninstall
  - helm
---

# Uninstall a helm instance

To uninstall abcdesktop instancied by helm only, run the `helm uninstall` command.

## Quick uninstallation abcdesktop (Linux or macOS)

> Quick uninstallation can be run on Linux or macOS operation system.

```bash
NAMESPACE=abcdesktop
helm uninstall abcdesktop -n ${NAMESPACE}
```

Rename the `NAMESPACE` variable to your abcdesktop namespace and abcdesktop by your instance name.

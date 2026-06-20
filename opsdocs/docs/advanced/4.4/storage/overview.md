---
tags:
  - storage
  - overview
---

# Storage Overview

abcdesktop supports several storage strategies to manage user home directories and shared data. Each option addresses different infrastructure requirements and persistence needs.

## Home Directory Storage

### No Persistence (default)

By default, user home directories are ephemeral and live only for the duration of the pod. No configuration is required.

### hostPath

Maps a user's home directory to a local directory on the Kubernetes node.

- Simple to set up, no external dependencies
- Requires the user to always land on the same node
- See [hostPath](hostpath.md)

### NFS (PersistentVolumeClaim)

Binds user home directories to an NFS server through Kubernetes PersistentVolumes and PersistentVolumeClaims.

- Fully persistent across pod restarts and node changes
- Requires an NFS server and the `nfs-subdir-external-provisioner` Helm chart
- See [NFS](nfs.md)

## I/O Optimization

### Memory-backed directories (cache)

Specific user subdirectories (e.g. `.cache`, `.local`, `.config`) can be overwritten with `emptyDir` volumes backed by memory to reduce I/O pressure on the storage backend.

- Configurable via `desktop.directorytomemoryemptydir` and `desktop.directorytomemory`
- Data is lost when the pod is deleted
- See [Cache](cache.md)

## Shared Volumes

Users belonging to the same group can share a common volume mounted inside their pods. Two backends are supported:

| Backend   | Use case                                              |
|-----------|-------------------------------------------------------|
| `hostPath` | Shared directory on a worker node, no external setup |
| `pvc`      | Shared NFS-backed PVC, accessible from any node      |

Access is controlled through `desktop.policies` rules tied to LDAP group membership.

- See [Shared Volumes](sharedvolumes.md)
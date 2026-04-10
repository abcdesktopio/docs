# Overwritten user home directory entries


 
## Overwritten user homedirectory directory entries


To reduce I/O to the storage backend, you can defined entries in the `desktop.directorytomemoryemptydir` option, and overwrite users sub directories.

```
desktop.directorytomemoryemptydir: [ '.cache', '.local', '.config' ]
desktop.directorytomemory: { 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi' } }
```

The default `desktop.directorytomemory` is a dictionary set to `{ 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi' } }`

The `desktop.directorytomemory` dictionnary is the same for all `desktop.directorytomemoryemptydir` entries.

A `kubectl describe pod` command line shows the volume for each `desktop.directorytomemoryemptydir` in this case `[ '.cache', '.local', '.config' ]`
 

The mounted volumes show that each entries `/home/fry/.cache`, `/home/fry/.config`, `/home/fry/.local` are overwritten.

```
Mounts:
  [...]
  /home/fry/.cache from cache (rw)
  /home/fry/.config from config (rw)
  /home/fry/.local from local (rw) 
``` 


The volumes are configured as an `emptyDir` (a temporary directory that shares a pod's lifetime) of `Memory` with a `SizeLimit` to `8Gi`.

```
Volumes:
  auth-localaccount-fry:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  auth-localaccount-fry
    Optional:    false
 [...]
  cache:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:     Memory
    SizeLimit:  8Gi
  local:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:     Memory
    SizeLimit:  8Gi
  config:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:     Memory
    SizeLimit:  8Gi
[...]
```    

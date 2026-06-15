---
tags:
  - storage
  - cache
  - memory
  - AD
---


# Overwritten user home directory entries

## Overwritten user homedirectory directory entries


To reduce I/O to the storage backend, you can define entries in the `desktop.directorytomemoryemptydir` option to overwrite specific user subdirectories.

```
desktop.directorytomemoryemptydir: [ '.cache', '.local', '.config' ]
desktop.directorytomemory: { 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi' } }
```

The default `desktop.directorytomemory` is a dictionary set to `{ 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi' } }`

The `desktop.directorytomemory` dictionary is the same for all `desktop.directorytomemoryemptydir` entries.

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


### Update the sound container for `.config` usage

The `s-sound` container needs to read the `$HOME/.config/pulse/cookie` file.
If you choose to use `.config` as an `emptyDir` volume, you need to add this volume to the sound container description.

- update your `desktop.pod` dictionary to add the `config` volume into the volume list `'volumes': [ 'extrausers', 'tmp', 'config', 'log' ]`

```
'sound': { 
    'volumes': [ 'extrausers', 'tmp', 'config', 'log' ],
    'image': 'ghcr.io/abcdesktopio/oc.pulseaudio:4.4',
    'imagePullPolicy': 'Always',
    'enable': True,
    'tcpport': 29788,
    'acl':  { 'permit': [ 'all' ] },
  },
``` 

After a login, you can check that the s-sound container mounts `.config` as `$HOME/.config` :

```
NAMESPACE=abcdesktop
kubectl  describe pods fry-c33ed  -n $NAMESPACE
```

You should read for the `s-sound` container the `Mounts`

```
    Mounts:
      /home/fry/.config from config (rw)
      /tmp from tmp (rw)
      /var/lib/extrausers from extrausers (rw)
      /var/log/desktop from log (rw)
```

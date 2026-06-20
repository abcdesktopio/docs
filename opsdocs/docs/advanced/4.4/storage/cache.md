---
tags:
  - storage
  - cache
  - memory
  - AD
---


# Overwriting User Home Directory Entries

## Overwriting user home directory entries with memory-backed volumes


To reduce I/O pressure on the storage backend, you can configure the `desktop.directorytomemoryemptydir` option to replace specific user subdirectories with in-memory `emptyDir` volumes. This approach is particularly useful for high-churn directories such as `.cache`, `.local`, and `.config`.

```
desktop.directorytomemoryemptydir: [ '.cache', '.local', '.config' ]
desktop.directorytomemory: { 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi' } }
```

The default value of `desktop.directorytomemory` is the dictionary `{ 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi' } }`.

This dictionary applies uniformly to every entry listed in `desktop.directorytomemoryemptydir`.

Running `kubectl describe pod` displays the volume mounted for each entry in `desktop.directorytomemoryemptydir` — in this example, `[ '.cache', '.local', '.config' ]`.
 

The mounted volumes confirm that each path — `/home/fry/.cache`, `/home/fry/.config`, and `/home/fry/.local` — has been replaced by an in-memory volume.

```
Mounts:
  [...]
  /home/fry/.cache from cache (rw)
  /home/fry/.config from config (rw)
  /home/fry/.local from local (rw) 
``` 


Each volume is configured as an `emptyDir` of type `Memory` with a `SizeLimit` of `8Gi`, meaning its contents are stored entirely in RAM and are discarded when the pod terminates.

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

The `s-sound` container requires read access to the `$HOME/.config/pulse/cookie` file. If you configure `.config` as an `emptyDir` volume, you must explicitly add the `config` volume to the sound container definition.

- Update your `desktop.pod` dictionary to include the `config` volume in the volume list: `'volumes': [ 'extrausers', 'tmp', 'config', 'log' ]`

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

After a user logs in, verify that the `s-sound` container mounts `.config` at `$HOME/.config`:

```
NAMESPACE=abcdesktop
kubectl  describe pods fry-c33ed  -n $NAMESPACE
```

In the `s-sound` container's `Mounts` section, you should see the following entry:

```
    Mounts:
      /home/fry/.config from config (rw)
      /tmp from tmp (rw)
      /var/lib/extrausers from extrausers (rw)
      /var/log/desktop from log (rw)
```

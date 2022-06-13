# User data persistence in `all-in-one` configuration 


## Requirements 

Use a Kubernetes `abcdesktop` instance 

## Goals

* keep user's data after a logoff 


## Create `/mnt/abcdesktop` directory

Create a directory `/mnt/abcdesktop`

```bash
mkdir -p /mnt/abcdesktop  
```

abcdesktop uses a `PersistentVolume` to store user data.


## Remove previous PersistentVolume and PersistentVolumeClaim

```bash
kubectl delete pvc persistentvolumeclaim-home-directory  -n abcdesktop
kubectl delete pv  pv-volume-home-directory -n abcdesktop
```

You have to delete user's pod too. Make sure that all user's pod have been removed.


## Create the PersistentVolume `pv-volume-home-directory`

```bash
kubectl create -f - <<EOF
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-volume-home-directory
  namespace: abcdesktop
  labels:
     type: local
spec:
  storageClassName: storage-local-abcdesktop
  capacity:
     storage: 10Gi
  volumeMode: Filesystem
  accessModes:
  - ReadWriteMany
  hostPath:
    path: '/mnt/abcdesktop'
EOF
```

You should read on stdout : 

```
persistentvolume/pv-volume-home-directory created
```


## Create the PersistentVolumeClaim `persistentvolumeclaim-home-directory`

```bash
kubectl create -f - <<EOF
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: persistentvolumeclaim-home-directory
  namespace: abcdesktop
spec:
  storageClassName: storage-local-abcdesktop
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 3Gi
EOF
```

You should read on stdout : 

```
persistentvolumeclaim/persistentvolumeclaim-home-directory created
```


## Update `abcdesktop.yaml` file 


### Change od.config file

Two options define the user homedirectory :  `desktop.homedirectorytype` and `desktop.persistentvolumeclaim`

#### Update `desktop.homedirectorytype`

Set the desktop.homedirectorytype to value 'persistentVolumeClaim'

```
desktop.homedirectorytype: 'persistentVolumeClaim'
```

#### Update `desktop.persistentvolumeclaim`

Set the desktop.persistentvolumeclaim to the name of the `persistentVolumeClaim` to use. In this example the name of the `persistentvolumeclaim` is `persistentvolumeclaim-home-directory`

```
desktop.persistentvolumeclaim: 'persistentvolumeclaim-home-directory'
```

#### Update `desktop.pod`


Add the `init` entry in `desktop.pod`

```
'init':       {     'image': 'busybox',
                    'enable': True,
                    'acl':  { 'permit': [ 'all' ] },
                    'pullpolicy':  'IfNotPresent',
                    'command':  [ 'sh', '-c',  'chown 4096:4096 /home/balloon /home/balloon/*' ] 
    }
```

The init entry defines the init container for the user's pod. The command runs by the init container, fixes the owner of the home directory to `userid` to `4096` and the `groupid` to `4096`.   The init command is `chown 4096:4096 /home/balloon /home/balloon/*`

Pulseaudio audio service does not start if the home directory not accessible or not own by the current user.
 

```
desktop.pod : { 
    'graphical' : { 'image': 'abcdesktopio/oc.user.20.04:dev',
                    'pullpolicy':  'IfNotPresent',
                    'enable': True,
                    'acl':  { 'permit': [ 'all' ] },
                    'waitportbin' : '/composer/node/wait-port/node_modules/.bin/wait-port',
                    'resources': { 'requests': { 'memory': "320Mi",   'cpu': "250m" },  'limits'  : { 'memory': "1Gi",    'cpu': "1000m" } },
                    'securityContext': { 'allowPrivilegeEscalation': True, 'runAsUser': 4096 },
                    'shareProcessNamespace': True,
                    'secrets_requirement' : [ 'abcdesktop/vnc', 'abcdesktop/kerberos']
    },
    'printer' :   { 'image': 'abcdesktopio/oc.cupsd.18.04:dev',
                    'pullpolicy': 'IfNotPresent',
                    'enable': True,
                    'securityContext': { 'runAsUser': 0 },
                    'resources': { 'requests': { 'memory': "64Mi",    'cpu': "125m" },  'limits'  : { 'memory': "512Mi",  'cpu': "500m"  } },
                    'acl':  { 'permit': [ 'all' ] } 
    },
    'filer' :     { 'image': 'abcdesktopio/oc.filer:dev',
                    'pullpolicy':  'IfNotPresent',
                    'enable': True,
                    'securityContext': { 'runAsUser': 4096 },
                    'acl':  { 'permit': [ 'all' ] } 
    },
    'storage' :   { 'image': 'k8s.gcr.io/pause:3.2',
                    'pullpolicy':  'IfNotPresent',
                    'enable': True,
                    'securityContext': {  'runAsUser': 4096 },
                    'acl':   { 'permit': [ 'all' ] },
                    'resources': { 'requests': { 'memory': "32Mi",    'cpu': "100m" },  'limits'  : { 'memory': "128Mi",  'cpu': "250m"  } }
    },
    'sound':      { 'image': 'abcdesktopio/oc.pulseaudio.22.04:dev',
                    'pullpolicy': 'IfNotPresent',
                    'enable': True,
                    'securityContext': {  'runAsUser': 4096 },
                    'acl':  { 'permit': [ 'all' ] },
                    'resources': { 'requests': { 'memory': "8Mi",     'cpu': "50m"  },  'limits'  : { 'memory': "64Mi",   'cpu': "250m"  } } 
    },
    'init':       { 'image': 'busybox',
                    'enable': True,
                    'acl':  { 'permit': [ 'all' ] },
                    'pullpolicy':  'IfNotPresent',
                    'command':  [ 'sh', '-c',  'chown 4096:4096 /home/balloon /home/balloon/*' ] 
    }}
```




### Restart your pyos daemon

Restart your pyos daemon, to make sure that the new parameters will be use to start the user container.

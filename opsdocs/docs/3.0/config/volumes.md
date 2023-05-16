
# Volumes to retain user's home directory files

To retain user's home directory files, you can define [PersistentVolume](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)  using `hostPath` or [PersistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) using `storageClassName` parameter.

## Define persistentVolume using `hostPath`

In your od.config file, define the new entries `desktop.homedirectorytype` `desktop.persistentvolumespec` `desktop.persistentvolumeclaimspec`


- `desktop.homedirectorytype`: 'persistentVolumeClaim'
- `desktop.persistentvolumespec`: create a new volume for the user's homeDir, for persistentVolume hostPath.
- `desktop.persistentvolumeclaimspec`: create a new volume claim for the user's homeDir


```json
# set to persistentVolumeClaim
desktop.homedirectorytype: 'persistentVolumeClaim'
# define how to create persistentvolume
desktop.persistentvolumespec: {
            'storageClassName': '',
            'capacity': { 'storage': '1Gi' },
            'accessModes': [ 'ReadWriteOnce' ], 
            'hostPath': { 'path': '/mnt/abcdesktop_volumes/{{ provider }}/{{ userid }}' } }
# define how to create persistentvolumeclaim
desktop.persistentvolumeclaimspec: {
            'storageClassName': '',
            'resources': { 
              'requests': { 
                'storage': '1Gi'
              } 
            },
            'accessModes': [ 'ReadWriteOnce' ] }
```


desktop.persistentvolumespec support template values. For example `'/mnt/abcdesktop_volumes/{{ provider }}/{{ userid }}'`. 

- `{{ provider }}` is the provider's name templated value. 
- `{{ userid }}` is the user's id templated value.


*The list of all template values can be read at the end of this chapter*

The user's home directory inside the pod is located on host to `/mnt/abcdesktop_volumes/{{ provider }}/{{ userid }}`. The directory is created automatically by kubernetes.

The `/mnt/abcdesktop_volumes/` content lists the provider name.

On the host, the new directory is created, where each home directory is located.

Read the new path for 'hostPath' persistent volumes

```bash
$ ls -la /mnt/abcdesktop_volumes/
total 20
drwxr-xr-x   5 root root 4096 mai   12 12:40 .
drwxr-xr-x 106 root root 4096 mai   11 11:34 ..
drwxr-xr-x   3 root root 4096 mai   12 12:40 anonymous
drwxr-xr-x   3 root root 4096 mai   12 12:39 github
drwxr-xr-x   5 root root 4096 mai   12 12:40 google
```

For provider `google`, all users are listed.

```bash
$ ls -la /mnt/abcdesktop_volumes/google/
total 20
drwxr-xr-x  5 root root 4096 mai   12 12:40 .
drwxr-xr-x  5 root root 4096 mai   12 12:40 ..
drwxr-x--- 16 2048 2048 4096 mai   12 12:39 103464335761332102620
drwxr-x--- 16 2048 2048 4096 mai   12 12:40 112026272437223559761
drwxr-x--- 16 2048 2048 4096 mai   12 12:39 114102844260599245242
```

For provider `google`, list the user home directory for the user `103464335761332102620`

```bash
$ ls -la /mnt/abcdesktop_volumes/google/103464335761332102620/
total 76
drwxr-x--- 16 2048 2048 4096 mai   12 12:39 .
drwxr-xr-x  5 root root 4096 mai   12 12:40 ..
-rw-------  1 2048 2048   71 mai   12 12:39 .Xauthority
-rw-rw-r--  1 2048 2048   12 janv. 27 18:36 .Xresources
drwxr-x---  3 2048 2048 4096 mai   12 12:39 .cache
drwxr-x---  6 2048 2048 4096 mai   12 12:39 .config
drwxrwxr-x  3 2048 2048 4096 janv. 27 18:36 .gconf
-rw-r-----  1 2048 2048    0 mai   12 12:39 .gtk-bookmarks
-rw-rw-r--  1 2048 2048  564 janv. 27 18:36 .gtkrc-2.0
drwxr-x---  3 2048 2048 4096 mai   12 12:39 .local
drwxr-x---  2 2048 2048 4096 mai   12 12:39 .store
drwxr-x---  2 2048 2048 4096 mai   12 12:39 .wallpapers
drwxr-x---  2 2048 2048 4096 mai   12 12:39 Desktop
drwxr-x---  2 2048 2048 4096 mai   12 12:39 Documents
drwxr-x---  2 2048 2048 4096 mai   12 12:39 Downloads
drwxr-x---  2 2048 2048 4096 mai   12 12:39 Music
drwxr-x---  2 2048 2048 4096 mai   12 12:39 Pictures
drwxr-x---  2 2048 2048 4096 mai   12 12:39 Public
drwxr-x---  2 2048 2048 4096 mai   12 12:39 Templates
drwxr-x---  2 2048 2048 4096 mai   12 12:39 Videos
```

### list of all template values

The template values can be one of them :

| var                 | description     |  
| -------------------:| ---------------:|
| cn                  | Common Name     |
| uid                 | user id         |
| gid                 | group id        |
| uidNumber           | user id number  |
| gidNumber           | group id number |
| homeDirectory       | homeDirectory   |
| loginShell          | loginShell      |
| description         | description     |
| groups              | groups          |
| gecos               | gecos           |
| provider            | provider        |
| protocol            | protocol        |
| providertype        | providertype    |
| name                | user name       |
| userid              | user id         |
| locale              | user's locale   |
| *template tag value*| tag value set by auth rules   |


> Note: `hostPath` supports file permissions and the pod's init commands `chown` or `chmod` can be used.


## Define persistentVolumeClaim using `storageClassName`


To define a `persistentVolumeClaim`, update the od.config file and set

```json
desktop.homedirectorytype: 'persistentVolumeClaim'
desktop.persistentvolumespec: None
desktop.persistentvolumeclaimspec: <YOUR_PERSISTENT_VOLULME_CLAIM_SPEC>
```

`desktop.persistentvolumeclaimspec` is a dictionary. Get more information about [PersistentVolume and PersistentVolumeClaim.](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)

For example

```json
# set to persistentVolumeClaim
desktop.homedirectorytype: 'persistentVolumeClaim'
desktop.persistentvolumespec: None
desktop.persistentvolumeclaimspec: {
            'storageClassName': 'mystorageclass',
            'resources': { 
              'requests': { 
                'storage': '1Gi'
              } 
            },
            'accessModes': [ 'ReadWriteOnce' ] }
```

Replace `mystorageclass` by storageclass of your cloud provider

```
kubectl get storageclass
```

The example output is as follows on the cloud provider [aws](https://aws.amazon.com/).

```
NAME            PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
gp2 (default)   kubernetes.io/aws-ebs   Delete          WaitForFirstConsumer   false 
```

The example output is as follows on the cloud provider [digitalocean](https://www.digitalocean.com/).

```
NAME                          PROVISIONER                    RECLAIMPOLICY          Immediate           false                  3h22m
do-block-storage (default)    dobs.csi.digitalocean.com      Delete          Immediate           true                   2d7h
do-block-storage-retain       dobs.csi.digitalocean.com      Retain          Immediate           true                   2d7h
do-block-storage-xfs          dobs.csi.digitalocean.com      Delete          Immediate           true                   2d7h
do-block-storage-xfs-retain   dobs.csi.digitalocean.com      Retain          Immediate           true                   2d7h
```

### For a self hosting kubernetes cluster

#### example with storageClassName:`csi-s3`

Use the `https://github.com/yandex-cloud/k8s-csi-s3` as a `CSI for S3` with [minio](https://min.io/) as backend. 

Follow `https://github.com/yandex-cloud/k8s-csi-s3` setup guide and test with the sample pod to make sure that fuse mounts the S3 file system.  


##### Update storageclass.yaml file

```
---
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: csi-s3
provisioner: ru.yandex.s3.csi
parameters:
  mounter: geesefs 
  # you can set mount options here, for example limit memory cache size (recommended)
  options: "--memory-limit 1000 --dir-mode 0777 --file-mode 0666 --setuid 0"
  # to use an existing bucket, specify it here:
  # bucket: abcdesktop
  csi.storage.k8s.io/provisioner-secret-name: csi-s3-secret
  csi.storage.k8s.io/provisioner-secret-namespace: kube-system
  csi.storage.k8s.io/controller-publish-secret-name: csi-s3-secret
  csi.storage.k8s.io/controller-publish-secret-namespace: kube-system
  csi.storage.k8s.io/node-stage-secret-name: csi-s3-secret
  csi.storage.k8s.io/node-stage-secret-namespace: kube-system
  csi.storage.k8s.io/node-publish-secret-name: csi-s3-secret
  csi.storage.k8s.io/node-publish-secret-namespace: kube-system
```

Update the `csi-s3` storage class to add `--setuid 0` as options

```bash
kubectl delete sc csi-s3
kubectl create -f storageclass.yaml
```


##### Update `od.config`


In your od.config file, define the entry `desktop.persistentvolumeclaimspec`

- `desktop.homedirectorytype`: 'persistentVolumeClaim' to use the persistentVolumeClaim features.
- `desktop.persistentvolumespec`: None to skip the persistent volume provisioning.
- `desktop.persistentvolumeclaimspec` create a new volume claim for the user's homeDir, the storageClassName `csi-s3`



```json
# set to persistentVolumeClaim
desktop.homedirectorytype: 'persistentVolumeClaim'
desktop.persistentvolumespec: None
desktop.persistentvolumeclaimspec: {
            'storageClassName': 'csi-s3',
            'resources': { 
              'requests': { 
                'storage': '1Gi'
              } 
            },
            'accessModes': [ 'ReadWriteOnce' ] }
```


##### The init command options with no file permissions support

By default the storageclass use `mounter: geesefs`. `geesefs` does not store file permissions and the init commands `chown` or `chmod` exit with no zero value, then the pod does not start.
All files belongs to `root`, but with correct permissions `options: "--memory-limit 1000 --dir-mode 0777 --file-mode 0666 --setuid 0"`. 

Update the 'init' in `desktop.pod` dict 

```json
'init': { 
    'image': 'busybox',
    'enable': True,
    'pullpolicy':  'IfNotPresent',
    'securityContext': {
        'runAsUser':   0,
        'runAsGroup':  0 
    },
    'acl':  { 'permit': [ 'all' ] },
    'command':  [ 'sh', '-c',  'chown {{ uidNumber }}:{{ gidNumber }} ~ || true && chmod 750 ~ || true' ] 
  }
```

Apply the new configuration file and restart pyos pods

```bash
kubectl delete configmap abcdesktop-config -n abcdesktop
kubectl create configmap abcdesktop-config --from-file=od.config -n abcdesktop
kubectl delete pods -l run=pyos-od -n abcdesktop
```

Login to abcdestkop service using your web browser.


List the persistent volumes

```
kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                             STORAGECLASS               REASON   AGE
pvc-81a65ed9-b98e-462c-86c6-36c89c3d4f1b   1Gi        RWO            Delete           Bound    abcdesktop/github-12896316-96cb5                  csi-s3                              2m46s
```


List the persistent volume claims 

```
# kubectl get pvc -n abcdesktop
NAME                                   STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS               AGE
github-12896316-96cb5                  Bound    pvc-81a65ed9-b98e-462c-86c6-36c89c3d4f1b   1Gi        RWO            csi-s3                     2m21s
```

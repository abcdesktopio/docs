
# desktop.pod

abcdesktop defines a user desktop as a group of user's containers. This is a main features of abcdesktop.
Each container offers a service. 

For example 

- `printer` is a service. `printer` service runs inside the user pod. 
- `graphical` is a service. `graphical` service runs inside the user pod and is the default service.

## containers in the user pod

- `init` contains init command for user pod
- `graphical` is the user graphical service (X11 and VNC)
- `spawner` is the command service for graphical service
- `broadcast` is the broadcast service for graphical service
- `webshell` is the shell (bash) service for graphical service
- `printer` is the printer service (cupsd)
- `printerfile` is the file service to download generated PDF file (this file transfert service is dedicated for printer service)
- `sound` is the sound service (pulseaudio) to send rtp stream from a container to the web browser via janus webrtc gateway
- `filer` is the filer service to upload and download file into the user home directory
- `storage` contains abcdesktop user secrets

Each service :

- can be enable or disable `'enable': True`
- can set dedicated `'resources'` limits resources for a container
- can set dedicated `'acl'` to start or not using rules 
- can set dedicated `'securityContext'` or use the spec `securityContext` 
- can set dedicated `'secrets_requirement`, a list of secrets to run example  `['abcdesktop/vnc', 'abcdesktop/kerberos']`


## default desktop.pod

``` json
desktop.pod : { 
  'spec' : {
    'shareProcessNamespace': True,
    'shareProcessMemory': True,
    'shareProcessMemorySize': '256Mi',
    'securityContext': { 
      'supplementalGroups':  [ '{{ supplementalGroups }}' ],
      'runAsUser': '{{ uidNumber }}',
      'runAsGroup': '{{ gidNumber }}',
      'readOnlyRootFilesystem': False, 
      'allowPrivilegeEscalation': True
    }
  },  
  'graphical' : { 
    'image': { 'default': 'abcdesktopio/oc.user.kubernetes.18.04:3.0' },
    'imagePullPolicy': 'IfNotPresent',
    'enable': True,
    'acl': { 'permit': [ 'all' ] },
    'waitportbin': '/composer/node/wait-port/node_modules/.bin/wait-port',
    'resources': { 
			'requests': { 'memory': "320Mi", 'cpu': "250m"  }, 
			'limits':   { 'memory': "1Gi",   'cpu': "1000m" } 
    },
    'shareProcessNamespace': True,
    'tcpport': 6081,
    'secrets_requirement' : [ 'abcdesktop/vnc', 'abcdesktop/kerberos']
  },
  'spawner' : { 
    'enable': True,
    'tcpport': 29786,
    'waitportbin' : '/composer/node/wait-port/node_modules/.bin/wait-port',
    'acl':  { 'permit': [ 'all' ] } 
  },
  'broadcast' : { 
    'enable': True,
    'tcpport': 29784,
    'acl':  { 'permit': [ 'all' ] } 
  },
  'webshell' : { 
    'enable': True,
    'tcpport': 29781,
    'acl':  { 'permit': [ 'all' ] } 
  },
  'printer' : { 
    'image': 'abcdesktopio/oc.cupsd.18.04:3.0',
    'imagePullPolicy': 'IfNotPresent',
    'enable': True,
    'tcpport': 681,
    # cupsd need to start as root
    'securityContext': { 'runAsUser': 0 },
    'resources': { 
      'requests': { 'memory': "64Mi", 'cpu': "125m" },  
      'limits'  : { 'memory': "512Mi",  'cpu': "500m" } 
    },
    'acl':  { 'permit': [ 'all' ] } 
  },
  'printerfile' : { 
    'enable': True,
    'tcpport': 29782,
    'acl':  { 'permit': [ 'all' ] } 
  },
  'filer' : { 
    'image': 'abcdesktopio/oc.filer:3.0',
    'imagePullPolicy':  'IfNotPresent',
    'enable': True,
    'tcpport': 29783,
    'acl':  { 'permit': [ 'all' ] } 
    },
  'storage' : { 
    'image': 'k8s.gcr.io/pause:3.8',
    'imagePullPolicy':  'IfNotPresent',
    'enable': True,
    'acl': { 'permit': [ 'all' ] },
    'resources': { 
      'requests': { 'memory': "32Mi",  'cpu': "100m" },  
      'limits'  : { 'memory': "128Mi", 'cpu': "250m" } 
    }
  },
  'sound': { 
    'image': 'abcdesktopio/oc.pulseaudio.22.04:3.0',
    'imagePullPolicy': 'IfNotPresent',
    'enable': False,
    'tcpport': 4714,
    'acl':  { 'permit': [ 'all' ] },
    'resources': { 
      'requests': { 'memory': "8Mi",  'cpu': "50m"  },  
      'limits'  : { 'memory': "64Mi", 'cpu': "250m" } 
    } 
  },
  'init': { 
    'image': 'busybox',
    'enable': True,
    # 'imagePullSecrets': [ { 'name': name_of_secret } ]
    'imagePullPolicy': 'IfNotPresent',
    'securityContext': { 'runAsUser': 0 },
    'acl':  { 'permit': [ 'all' ] },
    'command':  [ 'sh', '-c',  'chmod 750 ~ && chown {{ uidNumber }}:{{ gidNumber }} ~' ] 
  },
  'ephemeral_container': {
    'enable': True,
    'acl':  { 'permit': [ 'all' ] }
  },
  'pod_application' : {
    'enable': True,
    # 'imagePullSecrets': [ { 'name': name_of_secret } ]
    'acl':  { 'permit': [ 'all' ] } } }

```



### common options

#### enable

The container is added to the user pod if `'enable': True`

#### acl

The container is added to the user pod if `acl` matches. acl is based on tags and rules. 
Read the [authentification-rules](/config/authentification-rules/) abcdesktop documentation to defined tags.


#### pullpolicy

The image use the kubernetes pull policy values :

- `IfNotPresent` the image is pulled only if it is not already present locally.
- `Always` kubelet queries the container image registry to resolve the name to an image digest.
- `Never` the kubelet does not try fetching the image. If the image is somehow already present locally, the kubelet attempts to start the container; otherwise, startup fails. 

Read the [pullpolicy](https://kubernetes.io/docs/concepts/containers/images/) kubernetes documentation to get more details.


#### waitportbin

`waitportbin` is a binary command line, embedded inside the container, to check if the container is ready to run. Commonly it uses the `tcpport` value.

The command is run with parameters :

```bash
/composer/node/wait-port/node_modules/.bin/wait-port -t {waitportbintimeout}*1000 {container_ipaddr}:{container_tcpport}
```
 
#### waitportbintimeout

`waitportbintimeout` is the timeout in seconds for the `waitportbin` command. 
 
#### image

Image describe the container image name ( by example `'image': 'abcdesktopio/oc.user.kubernetes.18.04:3.0'`)

#### imagePullSecrets

The `imagePullSecret` entry is the list of the secret name used by kubernetes to access to the private registry.
The type of `imagePullSecret` is a list. This option is used if you need to store the abcdesktop docker image on your a private registry.

```json
 imagePullSecret : [ { 'name': name_of_secret } ]
```

- Example to build a registry Kubernetes secret named abcdesktopregistrysecret with the docker hub.

```bash
kubectl create secret docker-registry abcdesktopregistrysecret --docker-server=https://index.docker.io/v1/ --docker-username=XXXXXXX --docker-password=YYYYYYYU
```

- Example to build a registry Kubernetes secret named abcdesktopregistrysecret with your own privateregistry

```bash
kubectl create secret docker-registry abcdesktopregistrysecret --docker-server=registry.mydomain.local:443 --docker-username=XXXXXXX --docker-password=YYYYYYYU
```

The `imagePullSecret` become in this sample

```json
 imagePullSecret : [ { 'name': 'abcdesktopregistrysecret' } ]
```

#### resources

resources come from the kubernetes resources containers management. Read the [resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) kubernetes documentation to get more details.


### spec entry


`spec` entry defines the spec entry for a pod. All kubernetes entries are supported. Some of them are overwrited by abcdesktop.

- `{{ uidNumber }}` is replaced by the user's `uidNumber` on ldap if the objectClass is posixAccount or if not set by the default user id set in option `desktop.userid` 

- `{{ gidNumber }}` is replaced by the user's `gidNumber` on ldap if the objectClass is posixAccount  is replaced by the ldap gidNumber or if not set by the default group id set in option `desktop.groupid` 
- `{{ supplementalGroups }}` is replaced by the list of groups `gidNumber` is posixGroup
- `shareProcessNamespace` When process namespace sharing is enabled, processes in a container are visible to all other containers in the same pod. Read the kubernetes [shareProcessNamespace](https://kubernetes.io/docs/tasks/configure-pod-container/share-process-namespace/) details, to get more details.
- `shareProcessMemory` POSIX shared memory requires that a tmpfs be mounted at /dev/shm. The containers in a pod do not share their mount namespaces so we use volumes to provide the same /dev/shm into each container in a pod. To get more details, read [shared_memory](https://docs.openshift.com/container-platform/3.11/dev_guide/shared_memory.html). It is defined as an emptyDir volume `{ 'name': 'shm',  { 'medium': 'Memory', 'sizeLimit': shareProcessMemorySize } }`
- `shareProcessMemorySize` is the size of `shareProcessMemory`. The size is set to the `shm` volume  `'sizeLimit': shareProcessMemorySize`


```json
'spec' : {
    'shareProcessNamespace': True,
    'shareProcessMemory': True,
    'shareProcessMemorySize': '256Mi',
    'securityContext': { 
      'supplementalGroups': [ '{{ supplementalGroups }}' ],
      'runAsUser': '{{ uidNumber }}',
      'runAsGroup': '{{ gidNumber }}',
      'readOnlyRootFilesystem': False, 
      'allowPrivilegeEscalation': True
    }
```

### init container

init container run the init command. It changes access right to the user home directory. The init command runs as root by default with a securityContext `'securityContext': {'runAsUser':0, 'runAsGroup':0 }`.

The command support `{{ }}` values. Values can be 

- `'{{ uidNumber }}'`
- `'{{ gidNumber }}'`
- `'{{ uid }}'`

Values are read from the previous ldap authentification.

- `'{{ uidNumber }}'` is replaced by the ldap `uidNumber` or if not set by the default user id set in option `desktop.userid` 
- `'{{ gidNumber }}'` is replaced by the ldap gidNumber or if not set by the default group id set in option `desktop.groupid` 
- `'{{ uid }}'` is replaced by the ldap `uid` or if not set by the default user name set in option `desktop.username`

Example

``` json
 'command':  [ 'sh', '-c',  'chmod 755 ~ && chown {{ uidNumber }}:{{ gidNumber }} ~' ]
```




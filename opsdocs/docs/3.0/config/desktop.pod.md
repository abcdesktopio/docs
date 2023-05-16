
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
- `webshell` is the web socket bash shell service for graphical service
- `printer` is the printer service (cupsd)
- `printerfile` is the file service to download generated PDF file (this file transfert service is dedicated for printer service)
- `sound` is the sound service (pulseaudio) to send rtp stream from a container to the web browser via janus webrtc gateway
- `filer` is the filer service to upload and download file into the user home directory
- `storage` contains abcdesktop user secrets, like Kerberos, NTLM hashes, VNC password.

Each service :![](data:image/jpeg;base64,CiMgQ29udHJvbGxlcnMgCgojIyBDb250cm9sbGVycwphYmNkZXNrdG9wLmlvIHVzZSBhIE1vZGVs4oCTdmlld+KAk2NvbnRyb2xsZXIgKHVzdWFsbHkga25vd24gYXMgTVZDKSBpcyBhIHNvZnR3YXJlIGRlc2lnbiBwYXR0ZXJuIGNvbW1vbmx5IHVzZWQgZm9yIGRldmVsb3BpbmcgdXNlciBpbnRlcmZhY2VzIHdoaWNoIGRpdmlkZXMgdGhlIHJlbGF0ZWQgcHJvZ3JhbSBsb2dpYyBpbnRvIHRocmVlIGludGVyY29ubmVjdGVkIGVsZW1lbnRzLiBUaGlzIGlzIGRvbmUgdG8gc2VwYXJhdGUgaW50ZXJuYWwgcmVwcmVzZW50YXRpb25zIG9mIGluZm9ybWF0aW9uIGZyb20gdGhlIHdheXMgaW5mb3JtYXRpb24gaXMgcHJlc2VudGVkIHRvIGFuZCBhY2NlcHRlZCBmcm9tIHRoZSB1c2VyLgoKCnwgQ29udHJvbGxlciAgICAgICAgICAgICAgICAgIHwgIERlc2NyaXB0aW9uICAgfAp8LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS18LS0tLS0tLS0tLS0tLS0tIHwKfGBgYEFjY291bnRpbmdDb250cm9sbGVyYGBgIAl8IGFjY291bnRpbmcgZGF0YSBqc29uIGFuZCBlYm5mIGZvcm1hdCB8CnxgYGBBdXRoQ29udHJvbGxlcmBgYAkJCXwgYXV0aGVudGljYXRlIHVzZXIgIHwKfGBgYENvbXBvc2VyQ29udHJvbGxlcmBgYCAJCXwgQ1JVRCBtYWluIHNlcnZpY2VzIChsaWtlIGNyZWF0ZURlc2t0b3AsIHJ1bkFwcGxpY2F0aW9uKXwKfGBgYENvcmVDb250cm9sbGVyYGBgCQkJfCBnZXQgY29uZmlndXJhdGlvbiBhbmQgdXNlciBtZXNzYWdlIGluZm8gfAp8YGBgTWFuYWdlckNvbnRyb2xsZXJgYGAgCQl8IG1hbmFnZSBweW9zIHwKfGBgYFByaW50ZXJDb250cm9sbGVyYGBgCQl8IENSVUQgcHJpbnRlciBvYmplY3QgfAp8YGBgU3RvcmVDb250cm9sbGVyYGBgCQkJfCBDUlVEIGtleSB2YWx1ZSBkYXRhICB8CnxgYGBVc2VyQ29udHJvbGxlcmBgYAkJCXwgcmV0cmlldmUgdXNlciBpbmZvcm1hdGlvbiB8CgoKIyMgQWNjZXNzIFBlcm1pc3Npb24KClRoZSBgYGBBY2NvdW50aW5nQ29udHJvbGxlcmBgYCBhbmQgYGBgTWFuYWdlckNvbnRyb2xsZXJgYGAgYWNjZXNzIGlzIHByb3RlY3RlZCB3aXRoIGEgc291cmNlIGlwIGFkZHJlc3MgZmlsdGVyLgpUaGUgYWNjZXNzIGNvbnRyb2wgZmlsdGVyIGlzIGRlZmluZWQgaW4gYSBkaWN0aW9uYXJ5LgpFYWNoIGRpY3Rpb25hcnkgZW50cnkgdXNlIHRoZSBgYGBjb250cm9sbGVyYGBgIG5hbWUgYW5kIHdpdGggYW4gZW50cnkgYGBgcGVybWl0aXBgYGAuClRoZSBgYGBwZXJtaXRpcGBgYCBpcyBhIGxpc3Qgb2Ygc3VibmV0LCBmb3IgZXhhbXBsZSBgYGBbICcxMC4wLjAuMC84JywgJzE3Mi4xNi4wLjAvMTInIF1gYGAuCklmIGBgYHBlcm1pdGlwYGBgIGlzIG5vdCBzZXQgb3IgdGhlIGBgYGNvbnRyb2xsZXJgYGAgbmFtZSBpcyBub3Qgc2V0LCBhbGwgaXAgc291cmNlIGFkZHJlc3MgYXJlIGFsbG93ZWQgdGhlIHNlbmQgYSByZXF1ZXN0IHRvIHRoZSBjb250cm9sbGVyLgoKVGhlIGBgYGNvbnRyb2xsZXJzYGBgIGRpY3Rpb25uYXJ5IGlzIGRlZmluZWQgaW4gdGhlIGBgYG9kLmNvbmZpZ2BgYCBmaWxlLiAKQnkgZGVmYXVsdCB0aGUgY29uZmlndXJhdGlvbiBwZXJtaXQgcHJpdmF0ZSBuZXR3b3JrIGRlZmluZWQgaW4gW3JmYzE5MThdKGh0dHBzOi8vdG9vbHMuaWV0Zi5vcmcvaHRtbC9yZmMxOTE4KSBhbmQgW3JmYzQxOTNdKGh0dHBzOi8vdG9vbHMuaWV0Zi5vcmcvaHRtbC9yZmM0MTkzKS4gR2V0IG1vcmUgaW5mb3JtYXRpb24gYWJvdXQgdGhlIFtwcml2YXRlIG5ldHdvcmtdKGh0dHBzOi8vZW4ud2lraXBlZGlhLm9yZy93aWtpL1ByaXZhdGVfbmV0d29yaykuCgpCeSBkZWZhdWx0IG90aGVycyBjb250cm9sbGVycyBhY2Nlc3MgaXMgZW5hYmxlZCwgd2l0aG91dCBpcCByZXN0cmljdGlvbi4KCgpgYGAKCWNvbnRyb2xsZXJzIDogeyAKCQknQWNjb3VudGluZ0NvbnRyb2xsZXInOiAKCQkJeyAKCQkJCSdwZXJtaXRpcCc6IFsgJzEwLjAuMC4wLzgnLCAnMTcyLjE2LjAuMC8xMicsICcxOTIuMTY4LjAuMC8xNicsICdmZDAwOjovOCcsICcxNjkuMjU0LjAuMC8xNicsICcxMjcuMC4wLjAvOCcgXSAKCQkJfSwKCQknQXV0aENvbnRyb2xsZXInIDogCQl7ICdwZXJtaXRpcCc6IE5vbmUgfSwKCQknQ29tcG9zZXJDb250cm9sbGVyJyA6IAl7ICdwZXJtaXRpcCc6IE5vbmUgfSwKCQknQ29yZUNvbnRyb2xsZXInIDogCQl7ICdwZXJtaXRpcCc6IE5vbmUgfSwKCQknTWFuYWdlckNvbnRyb2xsZXInOiAKCQkJeyAKCQkJCSdwZXJtaXRpcCc6IFsgJzEwLjAuMC4wLzgnLCAnMTcyLjE2LjAuMC8xMicsICcxOTIuMTY4LjAuMC8xNicsICdmZDAwOjovOCcsICcxNjkuMjU0LjAuMC8xNicsICcxMjcuMC4wLjAvOCcgXSAKCQkJfSwKCQknUHJpbnRlckNvbnRyb2xsZXInIDogCXsgJ3Blcm1pdGlwJzogTm9uZSB9LAoJCSdTdG9yZUNvbnRyb2xsZXInIDogCXsgJ3Blcm1pdGlwJzogTm9uZSB9LAoJCSdVc2VyQ29udHJvbGxlcicgOiAJCXsgJ3Blcm1pdGlwJzogTm9uZSB9Cgl9IApgYGAKCgpJZiB0aGUgc291cmNlIGlwIGFkZHJlc3MgaXMgbm90IGFsbG93ZWQsIHRoZSByZXNwb25zZSBpcyBhIEhUVFAgc3RhdHVzIGBgYGNvZGUgNDAzIEZvcmJpZGRlbmBgYAoJCmBgYAp7InN0YXR1cyI6IDQwMywgInN0YXR1c19tZXNzYWdlIjogIjQwMyBGb3JiaWRkZW4iLCAibWVzc2FnZSI6ICJSZXF1ZXN0IGZvcmJpZGRlbiAtLSBhdXRob3JpemF0aW9uIHdpbGwgbm90IGhlbHAifSAKYGBgCg==)

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
      'supplementalGroups': [ '{{ supplementalGroups }}' ],
      'runAsUser': '{{ uidNumber }}',
      'runAsGroup': '{{ gidNumber }}',
      'readOnlyRootFilesystem': False, 
      'allowPrivilegeEscalation': True
    }
  },  
  'graphical' : { 
    'image': { 'default': 'abcdesktopio/oc.user.ubuntu:3.0' },
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
    'image': 'abcdesktopio/oc.cupsd:3.0',
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
    'image': 'abcdesktopio/oc.pulseaudio:3.0',
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
    'command':  [ 'sh', '-c',  'chmod 750 ~ && chown {{ uidNumber }}:{{ gidNumber }} ~ || true' ] 
  },
  'ephemeral_container': {
    'enable': True,
    'securityContext': { 
        'supplementalGroups': [ '{{ supplementalGroups }}' ] ,
        'readOnlyRootFilesystem': False, 
        'allowPrivilegeEscalation': True, 
        'runAsUser':                '{{ uidNumber }}',
        'runAsGroup':               '{{ gidNumber }}'
     },
    'acl':  { 'permit': [ 'all' ] }
  },
  'pod_application' : {
    'enable': True,
    'securityContext': { 
        'supplementalGroups': [ '{{ supplementalGroups }}' ] ,
        'readOnlyRootFilesystem': False, 
        'allowPrivilegeEscalation': True, 
        'runAsUser':                '{{ uidNumber }}',
        'runAsGroup':               '{{ gidNumber }}'
    },
    # 'imagePullSecrets': [ { 'name': name_of_secret } ]
    'acl':  { 'permit': [ 'all' ] } } }

```



### common options

#### enable

A container is added to the user pod if `'enable': True`

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

`waitportbintimeout` is the timeout in seconds to get `waitportbin` command result.  
 
#### image

Image describe the container image name ( by default `'image': 'abcdesktopio/oc.user.ubuntu:3.0'`)

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

Resources come from the kubernetes resources containers management. Read the [resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) kubernetes documentation to get more details.


### spec entry

`spec` entry defines the spec entry for a pod. All kubernetes entries are supported. Some of them are overwrited by abcdesktop.

- `{{ uidNumber }}` is replaced by the user's `uidNumber` on ldap if the objectClass is posixAccount or if not set by the default user id set in option `desktop.userid` 

- `{{ gidNumber }}` is replaced by the user's `gidNumber` on ldap if the objectClass is posixAccount  is replaced by the ldap gidNumber or if not set by the default group id set in option `desktop.groupid` 
- `{{ supplementalGroups }}` is replaced by the list of groups `gidNumber` is posixGroup

- `shareProcessNamespace` When process namespace sharing is enabled, processes in a container are visible to all other containers in the same pod. Read the kubernetes [shareProcessNamespace](https://kubernetes.io/docs/tasks/configure-pod-container/share-process-namespace/) details, to get more details. 


- `shareProcessMemory` Shared memory segments are used to accelerate inter-process communication at memory speed, rather than through pipes or through the network stack. Shared memory is commonly used by databases and custom-built (typically C/OpenMPI, C++/using boost libraries) high performance applications for scientific computing and financial services industries. POSIX shared memory requires that a tmpfs be mounted at /dev/shm. Containers in a pod do not share their mount namespaces so we use volumes to provide the same /dev/shm into each container in a pod. Read [shared_memory](https://docs.openshift.com/container-platform/3.11/dev_guide/shared_memory.html) to get more details. Shared memory is defined as an emptyDir volume `{ 'name': 'shm', { 'medium': 'Memory', 'sizeLimit': shareProcessMemorySize } }` minted on `/dev/shm`. Only ephemeral container application can share memory with the X11 server. To get more details about POSIX and UNIX System V shared memory objects, read the [podshmtest](https://github.com/abcdesktopio/podshmtest) repository.

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
 'command':  [ 'sh', '-c',  'chmod 755 ~ && chown {{ uidNumber }}:{{ gidNumber }} ~ || true' ]
```




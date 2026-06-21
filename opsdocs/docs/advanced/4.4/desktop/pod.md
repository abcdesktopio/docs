---
title: Desktop Pod Configuration | abcdesktop.io
description: Reference for the desktop pod configuration in abcdesktop.io: volumes, init containers, ephemeral containers, virtual printer queue, and default mount points.
keywords: pod, volumes, init container, ephemeral container, printer, abcdesktop, Kubernetes, desktop configuration
tags:
  - desktop
  - configuration
---



# Desktop configuration `desktop.pod`

This chapter describes how to configure the `desktop.pod` and `desktop.envlocal` objects in the abcdesktop config file.


## main entries in the `desktop.pod` dictionary

`desktop.pod` defines how to create the user's pod. The main sections are 

- `spec`: describes the `securityContext` and `shareProcessNamespace`
- `default_volumes` lists the available volumes in the pod
- `default_volumes_mount` lists the default mounted volumes used by the pod
- `graphical`: describes the graphical service 
  - `spawner`: describes the command service (built in `graphical`)
  - `broadcast`: describes the broadcast service (built in `graphical`)
  - `webshell`: describes the remote shell service (built in `graphical`)
- `filer`: describes the file download and upload service
- `printer`: describes the printer service 
  - `printerfile`: describes the file download service for the virtual printer queue (built in `printer`)
- `sound`: describes the sound container 
- `init`: describes the init container 
- `ephemeral_container`: describes how to start an application as an ephemeral container by default
- `pod_application`: describes how to start an application as a pod


```
desktop.pod : { 
  # default spec for all containers
  # can be overwritten on dedicated container spec
  # value inside mustache like {{ uidNumber }} is replaced by context run value
  # for example {{ uidNumber }} is the uid number define in ldap server 
  'spec' : {
    # 'imagePullSecrets': [ { 'name': name_of_secret } ],
    'shareProcessNamespace': False,
    'securityContext': {
      'supplementalGroups': [ '{{ supplementalGroups }}' ],
      'runAsUser': '{{ uidNumber }}',
      'runAsGroup': '{{ gidNumber }}'
    },
    'tolerations': []
  },
  'default_volumes': {
    'shm':        { 'name': 'shm',        'emptyDir': { 'medium': 'Memory', 'sizeLimit': '512Mi' } },
    'run':        { 'name': 'run',        'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Mi'   } },
    'tmp':        { 'name': 'tmp',        'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi'   } },
    'log':        { 'name': 'log',        'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi'   } },
    'rundbus':    { 'name': 'rundbus',    'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Mi'   } },
    'runuser':    { 'name': 'runuser',    'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Mi'   } },
    'x11socket':  { 'name': 'x11socket',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Ki'   } }
  },
  'default_volumes_mount': {
    'shm': { 'name': 'shm', 'mountPath' : '/dev/shm' },
    'run': { 'name': 'run',  'mountPath': '/var/run/desktop' },
    'tmp': { 'name': 'tmp',  'mountPath': '/tmp' },
    'log': { 'name': 'log',  'mountPath': '/var/log/desktop' },
    'rundbus':    { 'name': 'rundbus',    'mountPath': '/var/run/dbus' },
    'runuser':    { 'name': 'runuser',    'mountPath': '/run/user/' },
    'x11socket':  { 'name': 'x11socket',  'mountPath': '/tmp/.X11-unix' }
  },
  # graphical is the main abcdesktop container it include x11 service 
  'graphical' : {
    'volumes': [ 'x11socket', 'tmp', 'run', 'log', 'rundbus', 'runuser' ],
    'image': { 'default': 'ghcr.io/abcdesktopio/oc.user.ubuntu.sudo.24.04:{{ abcdesktop.latest_release }}' },
    'imagePullPolicy':  'Always',
    'enable': True,
    'acl':  { 'permit': [ 'all' ] },
    'waitportbin' : '/composer/node/wait-port/node_modules/.bin/wait-port',
    'securityContext': {
      'readOnlyRootFilesystem': False, 
      'allowPrivilegeEscalation': True,
      'supplementalGroups': [ '{{ supplementalGroups }}' ],
      'runAsUser': '{{ uidNumber }}',
      'runAsGroup': '{{ gidNumber }}',
      'runAsNonRoot': True 
    },
    'tcpport': 6081,
    'secrets_requirement' : [ 'abcdesktop/vnc', 'abcdesktop/kerberos'],
    'waitfor_services' : [ 'xserver', 'novnc', 'spawner-service', 'plasmashell' ],
    'waitfor_processes': [ 'kwin_x11', 'plasmashell', 'kactivitymanagerd'  ], 
    'waitfor_listeningservices': [ 'graphical', 'spawner' ]
  },
  # spawner core service to configure desktop
  # run inside graphical container  
  'spawner' : { 
    'enable': True,
    'tcpport': 29786,
    'waitportbin' : '/composer/node/wait-port/node_modules/.bin/wait-port',
    'acl':  { 'permit': [ 'all' ] } 
  },
  # broadcast core service for notification
  # run inside graphical container  
  'broadcast' : { 
    'enable': True,
    'tcpport': 29784,
    'acl':  { 'permit': [ 'all' ] } 
  },
  # webshell is no a container, just a service and run inside graphical container  
  # usefull to debug application and troubleshooting
  'webshell' : { 
    'enable': True,
    'tcpport': 29781,
    'acl':  { 'permit': [ 'all' ] } 
  },
  # container printer
  # printer is a cupsd service 
  'printer' : { 
    'volumes': [ 'tmp' ],
    'image': 'ghcr.io/abcdesktopio/oc.cupsd:{{ abcdesktop.latest_release }}',
    'imagePullPolicy': 'IfNotPresent',
    'enable': True,
    'tcpport': 681,
    'securityContext': { 'runAsUser': 0, 'runAsGroup': 0 },
    'acl':  { 'permit': [ 'all' ] } 
  },
  # allow to download file in the printer queue
  # use to print file from the web browser
  # printerfile is no a container, just a service 
  'printerfile' : { 
    'enable': True,
    'tcpport': 29782,
    'acl':  { 'permit': [ 'all' ] } 
  },
  # container filer
  # filer provide upload and download files features
  'filer' : { 
    'volumes': [ 'tmp', 'home', 'log'  ],
    'image': 'ghcr.io/abcdesktopio/oc.filer:{{ abcdesktop.latest_release }}',
    'imagePullPolicy':  'Always',
    'enable': True,
    'tcpport': 29783,
    'acl':  { 'permit': [ 'all' ] }
    },
  # container sound
  # sound is a pulseaudio service instance
  'sound': { 
    'volumes': [ 'tmp', 'home', 'log' ],
    'image': 'ghcr.io/abcdesktopio/oc.pulseaudio:{{ abcdesktop.latest_release }}',
    'imagePullPolicy': 'Always',
    'enable': True,
    'tcpport': 29788,
    'acl': { 'permit': [ 'all' ] },
  },
  # container init
  # a simple busybox to chowner and chmod of homedir
  # by defaul homedir belongs to root
  'init': { 
    'volumes': [ 'tmp', 'home' ],
    'image': 'busybox',
    'enable': True,
    'imagePullPolicy': 'IfNotPresent',
    'securityContext': { 'runAsUser': 0 },
    'acl':  { 'permit': [ 'all' ] },
    'command':  [ 
      'sh', 
      '-c',
      'chmod 750 ~ && chown {{ uidNumber }}:{{ gidNumber }} ~' ] 
  },
  'ephemeral_container': {
    'volumes': [ 'x11socket', 'tmp', 'run', 'log', 'rundbus', 'runuser' ],
    'enable': True,
    'imagePullPolicy': 'Always',
    'acl':  { 'permit': [ 'all' ] },
    'securityContext': { 
        'supplementalGroups': [ '{{ supplementalGroups }}' ] ,
        'readOnlyRootFilesystem': False, 
        'allowPrivilegeEscalation': True, 
        'runAsUser':'{{ uidNumber }}',
        'runAsGroup':'{{ gidNumber }}'
    }
  },
  'pod_application' : {
    'volumes': [ 'tmp', 'run', 'log', 'rundbus', 'runuser' ],
    'enable': True,
    'securityContext': {
        'supplementalGroups': [ '{{ supplementalGroups }}' ] ,
        'readOnlyRootFilesystem': False,
        'allowPrivilegeEscalation': True,
        'runAsUser':'{{ uidNumber }}',
        'runAsGroup':'{{ gidNumber }}'
    },
    'tolerations': [],
    'acl': { 'permit': ['all'] }}}
```

## `spec`

```
'spec' : {
    # 'imagePullSecrets': [ { 'name': name_of_secret } ],
    'shareProcessNamespace': False,
    'securityContext': {
      'supplementalGroups': [ '{{ supplementalGroups }}' ],
      'runAsUser': '{{ uidNumber }}',
      'runAsGroup': '{{ gidNumber }}'
    },
    'tolerations': []
}
```

`spec` describes the pod specification, following the standard Kubernetes pod specification format.

- `imagePullSecrets`: a list of secret references in the form `{ 'name': name_of_secret }` used to pull images. In most cases, these secrets are configured to pull images from a private registry. See [pull-image-private-registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/)
- `shareProcessNamespace`: a boolean that enables process namespace sharing between ephemeral containers and the graphical container. When process namespace sharing is enabled, processes in a container are visible to all other containers in the same pod. See [share-process-namespace](https://kubernetes.io/docs/tasks/configure-pod-container/share-process-namespace/)
- `securityContext`: defines privilege and access control settings for the desktop pod. The values `{{ supplementalGroups }}`, `{{ uidNumber }}`, and `{{ gidNumber }}` are substituted with LDAP-provided or default values during the desktop creation process. See [Configure a Security Context for a Pod or Container](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
- `tolerations`: [Tolerations allow the scheduler to schedule pods with matching taints.](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)





## `default_volumes` and `default_volumes_mount`

`default_volumes` describes the volumes created for the desktop pod. All Kubernetes volume types are supported. See [Types of volumes](https://kubernetes.io/docs/concepts/storage/volumes/). By default, abcdesktop creates `emptyDir` volumes on the `Memory` medium, but you can customize volumes using any Kubernetes-supported volume type.


> These volumes allow the root filesystem of the `graphical` container to be mounted as **read-only**.

```
 'default_volumes': {
    'shm':        { 'name': 'shm',        'emptyDir': { 'medium': 'Memory', 'sizeLimit': '512Mi' } },
    'run':        { 'name': 'run',        'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Mi'   } },
    'tmp':        { 'name': 'tmp',        'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi'   } },
    'log':        { 'name': 'log',        'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi'   } },
    'rundbus':    { 'name': 'rundbus',    'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Mi'   } },
    'runuser':    { 'name': 'runuser',    'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Mi'   } },
    'x11socket':  { 'name': 'x11socket',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Ki'   } }
  },
```


`default_volumes_mount` describes the mount points for the volumes defined in `default_volumes`.

```
  'default_volumes_mount': {
    'shm':        { 'name': 'shm',        'mountPath': '/dev/shm' },
    'run':        { 'name': 'run',        'mountPath': '/var/run/desktop' },
    'tmp':        { 'name': 'tmp',        'mountPath': '/tmp' },
    'log':        { 'name': 'log',        'mountPath': '/var/log/desktop' },
    'rundbus':    { 'name': 'rundbus',    'mountPath': '/var/run/dbus' },
    'runuser':    { 'name': 'runuser',    'mountPath': '/run/user/' },
    'x11socket':  { 'name': 'x11socket',  'mountPath': '/tmp/.X11-unix' }
  }
```

- The `shm` volume is shared between ephemeral container applications and the graphical pod. Applications that require shared memory access with the X11 server use this volume.
- The `run` volume is a dedicated volume for the graphical pod and typically contains PID files.
- The `tmp` volume is shared between ephemeral container applications and the graphical pod.
- The `log` volume is shared between ephemeral container applications and the pod containers. It typically contains log files.
- The `rundbus` and `runuser` volumes are used for D-Bus socket sharing.
- The `x11socket` volume is dedicated to the X11 Unix domain socket.


## `graphical` container

```
'graphical' : {
    'volumes': [ 'x11socket', 'tmp', 'run', 'log', 'rundbus', 'runuser' ],
    'image': { 'default': 'ghcr.io/abcdesktopio/oc.user.ubuntu.sudo.24.04:{{ abcdesktop.latest_release }}' },
    'imagePullPolicy':  'Always',
    'enable': True,
    'acl':  { 'permit': [ 'all' ] },
    'waitportbin' : '/composer/node/wait-port/node_modules/.bin/wait-port',
    'securityContext': {
      'readOnlyRootFilesystem': False, 
      'allowPrivilegeEscalation': True,
      'supplementalGroups': [ '{{ supplementalGroups }}' ],
      'runAsUser': '{{ uidNumber }}',
      'runAsGroup': '{{ gidNumber }}',
      'runAsNonRoot': True 
    },
    'tcpport': 6081,
    'secrets_requirement' : [ 'abcdesktop/vnc', 'abcdesktop/kerberos'],
    'waitfor_services' : [ 'xserver', 'novnc', 'spawner-service', 'plasmashell' ],
    'waitfor_processes': [ 'kwin_x11', 'plasmashell', 'kactivitymanagerd'  ], 
    'waitfor_listeningservices': [ 'graphical', 'spawner' ]
  },
  # spawner core service to configure desktop
  # run inside graphical container  
  'spawner' : { 
    'enable': True,
    'tcpport': 29786,
    'waitportbin' : '/composer/node/wait-port/node_modules/.bin/wait-port',
    'acl':  { 'permit': [ 'all' ] } 
  },
  # broadcast core service for notification
  # run inside graphical container  
  'broadcast' : { 
    'enable': True,
    'tcpport': 29784,
    'acl':  { 'permit': [ 'all' ] } 
  },
  # webshell is no a container, just a service and run inside graphical container  
  # usefull to debug application and troubleshooting
  'webshell' : { 
    'enable': True,
    'tcpport': 29781,
    'acl':  { 'permit': [ 'all' ] } 
  }
```


- `volumes` is the list of mounted volumes for this container
- `image` is the name of the image for this container
- `imagePullPolicy` is the image pull policy
- `enable` is a boolean to enable or disable this container
- `acl` is a dictionary that controls access to this container
- `securityContext` defines privilege and access control settings for the graphical container.
  - `allowPrivilegeEscalation`: Controls whether a process can gain more privileges than its parent process.
  - `readOnlyRootFilesystem`: Mounts the container's root filesystem as read-only. See [securityContext](https://kubernetes.io/docs/tasks/configure-pod-container/security-context/)
  - `supplementalGroups`: `[ '{{ supplementalGroups }}' ]` substituted with LDAP-provided or default values
  - `runAsUser`: `'{{ uidNumber }}'` substituted with LDAP-provided or default values
  - `runAsGroup`: `'{{ gidNumber }}'` substituted with LDAP-provided or default values
  - `runAsNonRoot`: boolean. See [pod-security-standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
- `tcpport` is the primary TCP port for the container
- `secrets_requirement` is a list of Kubernetes secrets to mount inside this container. By default, the graphical container mounts the secrets `abcdesktop/vnc` and `abcdesktop/kerberos`. If the `abcdesktop/kerberos` secret does not exist, it is silently omitted.
- `waitfor_services`: a list of supervisor-managed services that must be started before the container is considered ready, e.g., `[ 'xserver', 'novnc', 'spawner-service', 'plasmashell' ]`.
- `waitfor_processes`: a list of processes that must be running before the container is considered ready, e.g., `[ 'kwin_x11', 'plasmashell', 'kactivitymanagerd' ]`.
- `waitfor_listeningservices`: a list of services that must be actively listening on their TCP ports before the container is considered ready.


The following additional services run inside the graphical container.

- `spawner` describes the spawner service.
- `broadcast` describes the broadcast service  
- `webshell` describes the remote command service  




## `printer` container

```
'printer' : { 
    'volumes': [ 'tmp' ],
    'image': 'ghcr.io/abcdesktopio/oc.cupsd:{{ abcdesktop.latest_release }}',
    'imagePullPolicy': 'IfNotPresent',
    'enable': True,
    'tcpport': 681,
    'securityContext': { 'runAsUser': 0, 'runAsGroup': 0 },
    'acl':  { 'permit': [ 'all' ] } 
  },
  
# allow to download file in the printer queue
# use to print file from the web browser
# printerfile is no a container, just a service inside the printer container
'printerfile' : { 
    'enable': True,
    'tcpport': 29782,
    'acl':  { 'permit': [ 'all' ] } 
},
```

The printer container provides the print service, enabling files to be printed as PDF and downloaded from the virtual printer queue.

- `volumes` is the list of mounted volumes for this container
- `image` is the name of the image for this container
- `imagePullPolicy` is the image pull policy
- `enable` is a boolean to enable or disable this container
- `tcpport` is the primary TCP port for the container
- `securityContext`: the cups service must run as the `root` user: `{ 'runAsUser': 0, 'runAsGroup': 0 }`
- `acl` is a dictionary that controls access to this container



## `filer` container

```
'filer' : { 
    'volumes': [ 'tmp', 'home', 'log' ],
    'image': 'ghcr.io/abcdesktopio/oc.filer:{{ abcdesktop.latest_release }}',
    'imagePullPolicy':  'Always',
    'enable': True,
    'tcpport': 29783,
    'acl':  { 'permit': [ 'all' ] }
    },
```

The filer container provides file transfer capabilities, allowing users to upload and download files and directories.

- `volumes` is the list of mounted volumes for this container
- `image` is the name of the image for this container
- `imagePullPolicy` is the image pull policy
- `enable` is a boolean to enable or disable this container
- `tcpport` is the primary TCP port for the container
- `acl` is a dictionary that controls access to this container




## `sound` container


```
'sound': { 
    'volumes': [ 'tmp', 'home', 'log' ],
    'image': 'ghcr.io/abcdesktopio/oc.pulseaudio:{{ abcdesktop.latest_release }}',
    'imagePullPolicy': 'Always',
    'enable': True,
    'tcpport': 29788,
    'acl': { 'permit': [ 'all' ] },
  },
```

The sound container provides audio input and output services, including sound playback and microphone capture.

- `volumes` is the list of mounted volumes for this container
- `image` is the name of the image for this container
- `imagePullPolicy` is the image pull policy
- `enable` is a boolean to enable or disable this container
- `tcpport` is the primary TCP port for the container
- `acl` is a dictionary that controls access to this container


## `init` container


```
'init': { 
    'volumes': [ 'tmp', 'home' ],
    'image': 'busybox',
    'enable': True,
    'imagePullPolicy': 'IfNotPresent',
    'securityContext': { 'runAsUser': 0 },
    'acl':  { 'permit': [ 'all' ] },
    'command':  [ 
      'sh', 
      '-c',
      'chmod 750 ~ && chown {{ uidNumber }}:{{ gidNumber }} ~' ] 
  },
```

- `volumes` is the list of mounted volumes for this container
- `image` is the name of the image for this container
- `imagePullPolicy` is the image pull policy
- `enable` is a boolean to enable or disable this container
- `securityContext`: the init container must run as the `root` user: `{ 'runAsUser': 0 }`
- `acl` is a dictionary that controls access to this container
- `command` is the shell command executed at initialization: `[ 'sh', '-c', 'chmod 750 ~ && chown {{ uidNumber }}:{{ gidNumber }} ~' ]`


## desktop.pod with `sudo` command

```
desktop.pod : { 
  # default spec for all containers
  # can be overwritten on dedicated container spec
  # value inside mustache like {{ uidNumber }} is replaced by context run value
  # for example {{ uidNumber }} is the uid number define in ldap server 
  'spec' : {
    'shareProcessNamespace': False,
    'securityContext': {
      'supplementalGroups': [ '{{ supplementalGroups }}' ],
      'runAsUser': '{{ uidNumber }}',
      'runAsGroup': '{{ gidNumber }}'
    },
    'tolerations': []
  },
  'default_volumes': {
    'shm': { 'name': 'shm', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '512Mi' } },
    'run': { 'name': 'run', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Mi'    } },
    'tmp': { 'name': 'tmp', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi'   } },
    'log': { 'name': 'log', 'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Gi'   } },
    'rundbus': { 'name': 'rundbus',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Mi' } },
    'runuser': { 'name': 'runuser',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '8Mi' } },
    'x11socket': { 'name': 'x11socket',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Ki' } },
    'sudoers': { 'name': 'sudoers',  'emptyDir': { 'medium': 'Memory', 'sizeLimit': '1Mi' } }
  },
  'default_volumes_mount': {
    'shm': { 'name': 'shm', 'mountPath' : '/dev/shm' },
    'run': { 'name': 'run',  'mountPath': '/var/run/desktop' },
    'tmp': { 'name': 'tmp',  'mountPath': '/tmp' },
    'log': { 'name': 'log',  'mountPath': '/var/log/desktop' },
    'rundbus': { 'name': 'rundbus',  'mountPath': '/var/run/dbus' },
    'runuser': { 'name': 'runuser',  'mountPath': '/run/user/' },
    'x11socket': { 'name': 'x11socket',  'mountPath': '/tmp/.X11-unix' },
    'sudoers': { 'name': 'sudoers', 'mountPath': '/etc/sudoers.d' }
  },
  # graphical is the main abcdesktop container it include x11 service 
  'graphical' : {
    'volumes': [ 'sudoers', 'x11socket', 'tmp', 'run', 'log', 'rundbus', 'runuser' ],
    'image': { 'default': 'ghcr.io/abcdesktopio/oc.user.ubuntu.sudo.24.04:{{ abcdesktop.latest_release }}' },
    'imagePullPolicy':  'Always',
    'enable': True,
    'acl':  { 'permit': [ 'all' ] },
    'waitportbin' : '/composer/node/wait-port/node_modules/.bin/wait-port',
    'securityContext': {
      'readOnlyRootFilesystem': False, 
      'allowPrivilegeEscalation': True,
      'supplementalGroups': [ '{{ supplementalGroups }}' ],
      'runAsUser': '{{ uidNumber }}',
      'runAsGroup': '{{ gidNumber }}',
      'runAsNonRoot': True 
    },
    'tcpport': 6081,
    'secrets_requirement' : [ 'abcdesktop/vnc', 'abcdesktop/kerberos'],
    'waitfor_services' : [ 'xserver', 'novnc', 'spawner-service', 'plasmashell' ],
    'waitfor_processes' : [ 'kwin_x11', 'plasmashell', 'kactivitymanagerd'  ], 
    'waitfor_listeningservices': [ 'graphical', 'spawner' ]
  },
  # spawner core service to configure desktop
  # run inside graphical container  
  'spawner' : { 
    'enable': True,
    'tcpport': 29786,
    'waitportbin' : '/composer/node/wait-port/node_modules/.bin/wait-port',
    'acl':  { 'permit': [ 'all' ] } 
  },
  # broadcast core service for notification
  # run inside graphical container  
  'broadcast' : { 
    'enable': True,
    'tcpport': 29784,
    'acl':  { 'permit': [ 'all' ] } 
  },
  # webshell is no a container, just a service and run inside graphical container  
  # usefull to debug application and troubleshooting
  'webshell' : { 
    'enable': True,
    'tcpport': 29781,
    'acl':  { 'permit': [ 'all' ] } 
  },
  # container printer
  # printer is a cupsd service 
  'printer' : { 
    'volumes': [ 'tmp' ],
    'image': 'ghcr.io/abcdesktopio/oc.cupsd:{{ abcdesktop.latest_release }}',
    'imagePullPolicy': 'IfNotPresent',
    'enable': True,
    'tcpport': 681,
    'securityContext': { 'runAsUser': 0, 'runAsGroup': 0 },
    'acl':  { 'permit': [ 'all' ] } 
  },
  # allow to download file in the printer queue
  # use to print file from the web browser
  # printerfile is no a container, just a service 
  'printerfile' : { 
    'enable': True,
    'tcpport': 29782,
    'acl':  { 'permit': [ 'all' ] } 
  },
  # container filer
  # filer provide upload and download files features
  'filer' : { 
    'volumes': [ 'tmp', 'home', 'log'  ],
    'image': 'ghcr.io/abcdesktopio/oc.filer:{{ abcdesktop.latest_release }}',
    'imagePullPolicy':  'Always',
    'enable': True,
    'tcpport': 29783,
    'acl':  { 'permit': [ 'all' ] }
    },
  # container sound
  # sound is a pulseaudio service instance
  'sound': { 
    'volumes': [ 'sudoers', 'tmp', 'home', 'log' ],
    'image': 'ghcr.io/abcdesktopio/oc.pulseaudio:{{ abcdesktop.latest_release }}',
    'imagePullPolicy': 'Always',
    'enable': True,
    'tcpport': 29788,
    'acl': { 'permit': [ 'all' ] },
  },
  # container init
  # a simple busybox to chowner and chmod of homedir
  # by defaul homedir belongs to root
  'init': { 
    'volumes': [ 'sudoers', 'tmp', 'home' ],
    'image': 'busybox',
    'enable': True,
    'imagePullPolicy': 'IfNotPresent',
    'securityContext': { 'runAsUser': 0 },
    'acl':  { 'permit': [ 'all' ] },
    # chmod 1755 ~/.config && \
    # chmod 1755 ~/.cache && \
    #  chown {{ uidNumber }}:{{ gidNumber }} ~ ~/.config ~/.cache ~/.local
    'command':  [ 
      'sh', 
      '-c',
      'echo "$LOGNAME ALL=(ALL:ALL) ALL" > /etc/sudoers.d/$LOGNAME && \
       chmod 440 /etc/sudoers.d/* && \
       chown 0:0 /etc/sudoers.d/* && \
       chmod 755 /etc/sudoers.d && \ 
       chown 0:0 /etc/sudoers.d && \
       chmod 750 ~ && \
       chown {{ uidNumber }}:{{ gidNumber }} ~' ] 
  },
  'ephemeral_container': {
    'volumes': [ 'sudoers', 'x11socket', 'tmp', 'run', 'log', 'rundbus', 'runuser' ],
    'enable': True,
    'imagePullPolicy': 'Always',
    'acl':  { 'permit': [ 'all' ] },
    'securityContext': { 
        'supplementalGroups': [ '{{ supplementalGroups }}' ] ,
        'readOnlyRootFilesystem': False, 
        'allowPrivilegeEscalation': True, 
        'runAsUser':'{{ uidNumber }}',
        'runAsGroup':'{{ gidNumber }}'
    }
  },
  'pod_application' : {
    'volumes': [ 'sudoers', 'tmp', 'run', 'log', 'rundbus', 'runuser' ],
    'enable': True,
    # 'imagePullSecrets': [ { 'name': name_of_secret } ]
    'securityContext': {
        'supplementalGroups': [ '{{ supplementalGroups }}' ] ,
        'readOnlyRootFilesystem': False,
        'allowPrivilegeEscalation': True,
        'runAsUser':'{{ uidNumber }}',
        'runAsGroup':'{{ gidNumber }}'
    },
    'tolerations': [],
    'acl':  { 'permit': [ 'all' ] }  }  }
```


## define environment variables in the desktop

`desktop.envlocal` defines the environment variables injected into the desktop containers. It is a dictionary where each key is an environment variable name and the corresponding value is the variable's value. Only static variables are defined here; dynamic values are set programmatically by pyos at runtime.

```
# Add default environment vars 
# desktop.envlocal is a dictionary. 
# desktop.envlocal contains a (key,value) added by default as environment variables to oc.user.
desktop.envlocal :  { 
  'X11LISTEN':'tcp', 
  'WEBSOCKIFY_HEARTBEAT':'30',
  'DISABLE_REMOTEIP_FILTERING': 'enabled',
  'XDG_RUNTIME_DIR': '/tmp/runtime',
  'ABCDESKTOP_FORCE_OVERWRITE_PLASMA_CONFIG': 'true',
  'DISABLE_RTKIT': 'y'
 }
```



- Run a command inside a desktop pod to list the variable and get the value of one of them

- Identify an active desktop pod to run shell commands against.

```bash
NAMESPACE=abcdesktop
kubectl get pods -l type=x11server -n $NAMESPACE
NAME          READY   STATUS    RESTARTS   AGE
leela-debe1   3/3     Running   0          27s
```

The pod name is `leela-debe1`

- List the environment variables:

```bash
NAMESPACE=abcdesktop
kubectl exec -it leela-debe1 -n $NAMESPACE -- bash -c 'env'
Defaulted container "x-graphical" out of: x-graphical, s-sound, f-filer, i-init (init)
PYOS_PORT_8000_TCP_ADDR=10.111.133.176
NVIDIA_VISIBLE_DEVICES=all
KUBERNETES_SERVICE_PORT_HTTPS=443
OPENLDAP_PORT_636_TCP_PORT=636
ABCDESKTOP_LABEL_shipcrew=true
KUBERNETES_SERVICE_PORT=443
MEMCACHED_SERVICE_HOST=10.106.34.163
ABCDESKTOP_EXECUTE_CLASSNAME=default
...
```


- Get the value of the variable

```bash
NAMESPACE=abcdesktop
kubectl exec -it leela-debe1 -n $NAMESPACE -- bash -c 'echo $WEBSOCKIFY_HEARTBEAT'
Defaulted container "x-graphical" out of: x-graphical, s-sound, f-filer, i-init (init)
30
```

You can confirm that the `WEBSOCKIFY_HEARTBEAT` is set to `30`








 

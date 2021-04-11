# desktop options in od.config


The od.config contains options to describe how the oc.user and applications containers have to be created. Options differ if abcdesktop.io is running in ```docker mode``` or in ```kubernetes mode```.

## desktop.options

All desktop options are defined in od.config file.
Desktop options start with the prefix `desktop.`, then add the name of the option.


| Option name                           | Type | Sample | 
|---------------------------------------|----------------|---------------|
| `desktop.usex11unixsocket`     	| boolean        | True          | 
| `desktop.defaultbackgroundcolors` | list           | [ '#6EC6F0', '#333333',  '#666666', '#CD3C14', '#4BB4E6', '#50BE87', '#A885D8', '#FFB4E6' ] |
| `desktop.homedirectorytype`    	| string         | 'volume' |
| `desktop.remotehomedirectorytype` | list           | [] | 
| `desktop.persistentvolumeclaim`   | string         | None |   
| `desktop.allowPrivilegeEscalation` | boolean        | False | 
| `desktop.securityopt`             | list | [ 'no-new-privileges', 'seccomp=unconfined' ]  |
| `desktop.imagePullSecret`         | string         | None |
| `desktop.image`     				    | string        | 'abcdesktopio/oc.user.18.04:latest' |
| `desktop.imageprinter`            | string        | 'abcdesktopio/oc.cupsd.18.04:latest' |
| `desktop.useprintercontainer`     | boolean        | False |
| `desktop.soundimage`              | string        | 'abcdesktopio/oc.pulseaudio.18.04' |
| `desktop.usesoundcontainer`       | boolean        | False |
| `desktop.usecontainerimage`       | boolean        | False |
| `desktop.initcontainerimage`      | string         | 'abcdesktopio/oc.busybox' |
| `desktop.envlocal`     			    | dictionary     | `{ 'DISPLAY': ':0.0', 'USER': 'balloon', 'LIBOVERLAY_SCROLLBAR': '0','WINEARCH': 'win32','UBUNTU_MENUPROXY': '0','HOME': '/home/balloon','LOGNAME': 'balloon','PULSE_SERVER: 'localhost:4713', 'CUPS_SERVER': 'localhost:631' }` |
| `desktop.nodeselector`            		| dictionary     | `{}` | 
| `desktop.username`           			| string        | 'balloon' |
| `desktop.userid` 							| integer       | 4096 |
| `desktop.groupid`  						| integer       | 4096 |
| `desktop.userhomedirectory`      		| string        | `'/home/balloon'` |
| `desktop.useinternalfqdn`         		| boolean       | False |
| `desktop.uselocaltime`                | boolean       | False |
| `desktop.host_config`     			       | dictionary    | `{  'auto_remove'   : True, 'ipc_mode'      : 'shareable', 'network_mode'  : 'container', 'shm_size'      : '128M', 'mem_limit'     : '512M', 'cpu_period'    : 100000, 'cpu_quota'     : 150000, 'security_opt'  : [ 'seccomp=unconfined' ] }`  |
| `desktop.application_config`     			       | dictionary    | `{  'auto_remove'   : True, 'ipc_mode'      : 'shareable', 'pid_mode'      : True, 'network_mode'  : 'container', 'shm_size'      : '512M', 'mem_limit'     : '2G', 'cpu_period'    : 200000, 'cpu_quota'     : 150000, 'security_opt'  : [ 'seccomp=unconfined' ] }`  |

| `desktop.policies`     			       | dictionary    | `{ 'rules':{}, 'max_app_counter':5 }`  |



## desktop.usex11unixsocket
The ```desktop.usex11unixsocket``` force the X11 server to use local unix socket.
The name of the X11 unix socket is ```/tmp/.X11-unix/X0```

* **If this feature is enable**:
A container application need a the DISPLAY. The DISPLAY is in this case ```:0.0```. The container application and the oc.user container share the same volume ```/tmp```, and share the X11 unix socket is ```/tmp/.X11-unix/X0```.

* **If this feature is disable**:
A container application need a DISPLAY. The DISPLAY is ```:0.0``` (don't think at ```IPADDRESS_OF_X11_SERVER:0.0``` to protect X11 access control). The two containers share the same network stack by default. The X11 server NEED to listen to a TCP or UDP port.



You can disable this features, but you have to replace the default  TigerVNC by another X11 Server and a VNC Server. You can choose (x.org + x11vnc) for example, but you need more CPU ressource than TigerVNC.  

TigerVNC does not support to listen on TCP Port. TigerVNC is a X11 and a VNC Server.

Set the ```desktop.usex11unixsocket``` value to ```True``` in most case, and this should not be changed.


## desktop.shareipcnamespace
The type of desktop.shareipcnamespace is a string. The default value is 'shareable'
This option permit user contain to share the ipc namespace with application
 
| Value       | Description | 
|-------------|------------------------------|
| ```''```          | Use daemon’s default. |
| ```'none'```      |	Own private IPC namespace, with /dev/shm not mounted. |
| ```'private'```	 | Own private IPC namespace. |
| ```'shareable'```	 | Own private IPC namespace, with a possibility to share it with other containers. |
| ```'host'```	    | Use the host system’s IPC namespace. |

If not specified, daemon default is used, which can either be ```'private'``` or ```'shareable'```, depending on the daemon version and configuration. IPC (POSIX/SysV IPC) namespace provides separation of named shared memory segments, semaphores and message queues. 

Shared memory segments are used to accelerate inter-process communication at memory speed, rather than through pipes or through the network stack. Shared memory is commonly used by databases and custom-built (typically C/OpenMPI, C++/using boost libraries) high performance applications for scientific computing and financial services industries. 

If these types of applications are broken into multiple containers, you might need to share the IPC mechanisms of the containers, using "shareable" mode for the main (i.e. “donor”) container, and containers can access "container:<donor-name-or-ID>".

Default value
```desktop.shareipcnamespace : 'shareable'```


## desktop.homedirectory

This option describes how the default home directory for user user ballon should be created :

* ```None```: no dedicated volume is created, the oc.user container use a directory inside the container. All user data will be removed at logout.
* ```'volume'```: This value is only recommended in docker mode. ```'volume'```option create a dedicated volume, the oc.user container and applications may share this volume. User home data are persistent.
* ```'persistentVolumeClaim'```: This value is only avalaible in kubernetes. PersistentVolumeClaim option use a persistentVolumeClaim to create the user home directory. The persistentVolumeClaim can be mapped to differents storage data (like NFS, iSCSI, RBD...). Read more about [persistentVolumeClaim](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) on the kubernetes.io website.
You need the set the value of ```desktop.persistentvolumeclaim``` or create a default Persistent Volume Claim named ``'abcdesktop-pvc'``


## desktop.persistentvolumeclaim
This value is only avalaible in kubernetes mode.

```desktop.persistentvolumeclaim``` is the name of the Persistent Volume Claim if the ```desktop.homedirectory``` is set to ```'persistentVolumeClaim'```.
The PVC (Persistent Volume Claim) must exist.

Run the ```kubectl get pvc command``` to list the persistent volume claim

```
NAME                                   STATUS   VOLUME                     CAPACITY   ACCESS MODES   STORAGECLASS           AGE
abcdesktop-pvc                        Bound    abcdesktop-pv             5Gi        RWO            abcdesktop-standard   170d
```

## desktop.remotehomedirectorytype

desktop.remotehomedirectorytype is a list of string. Each string describe if the remount access to a directory is allowed.
example [ 'cifs', 'webdav' ]

For each entry in the desktop.remotehomedirectorytype list, abcdesktop.io try to mount the remote file system using data from the implicit auth provider.

If ```desktop.remotehomedirectorytype``` contains 'cifs' and if the authentification provider get ```homeDrive``` and ```homeDirectory``` attributs then abcdesktop request the kubernetes abcdesktop/CIFS Driver to mount the remote filesystem.
The user find a mount point named ```homeDrive``` value, and mounted to ```homeDirectory```.



## desktop.allowPrivilegeEscalation

The ```desktop.allowPrivilegeEscalation``` option allow a user to run a sudo command. The execve system call can grant a newly-started program privileges that its parent did not have, such as the setuid or setgid Linux flags.

The default value is ```False``` 
You should only set ```desktop.allowPrivilegeEscalation``` to run ```sudo``` command.

In production this value MUST be set to ```False```

## desktop.defaultbackgroundcolors 

The `desktop.defaultbackgroundcolors` allow you to change the default background color.

The default value is a list of string `[ '#6EC6F0', '#333333',  '#666666', '#CD3C14', '#4BB4E6', '#50BE87', '#A885D8', '#FFB4E6' ]`

The `desktop.defaultbackgroundcolors` length can contain up to 8 entries. To see the color 


Open the url http://localhost, in your web browser, to start a simple abcdesktop.io container. 

```
http://localhost
```

You should see the abcdesktop.io home page.

Press the `Connect with Anonymous access, have look`

At the right top corner, click on the menu and choose ```Settings```, then click on ```Screen Colors```

You should see the default background colors, for example :
![defaultbackgroundcolors](img/newbackgroundcolors.png)


## desktop.imagePullSecret


The `desktop.imagePullSecret` is the name of the secret used by Kubernetes to access to the private registry.
The type of `desktop.imagePullSecret` is a string. This option is only available in Kubernetes mode, and anly used if you need to store the abcdesktop docker image on a private registry. 

* Example to build a registry Kubernetes secret named abcdesktopregistrysecret with the docker hub.

```
kubectl create secret docker-registry abcdesktopregistrysecret --docker-server=https://index.docker.io/v1/ --docker-username=XXXXXXX --docker-password=YYYYYYYU
```

* Example to build a registry Kubernetes secret named abcdesktopregistrysecret with your own privateregistry

```
kubectl create secret docker-registry abcdesktopregistrysecret --docker-server=registry.mydomain.local:443 --docker-username=XXXXXXX --docker-password=YYYYYYYU
```


## desktop.image

The `desktop.image` is the name of the X11 server container
The default value is `abcdesktopio/oc.user.18.04`

## desktop.printerimage

The `desktop.printerimage` is the name of the  printer container
The default value is `abcdesktopio.oc.cupds.18.04`

## desktop.useprintercontainer

The `desktop.useprintercontainer` is boolean, to use printer `cupsd` service as an separated container.
This value is only available in kubernetes mode.  The default value is `False`.

## desktop.soundimage

The `desktop.soundimage` is the name of the sound container image
The default value is `abcdesktopio/oc.pulseaudio.18.04`

## desktop.usesoundcontainer

The `desktop.usesoundcontainer` is boolean, to use pulseaudio service as a separated container.
This value is only available in kubernetes mode. The default value is `False`.

## desktop.useinitcontainer

The `desktop.useinitcontainer` is boolean, to use init container. The default value is `False`.
The code call the `desktop.initcontainercommand` list .


The initcontainerimage is a busybox shell, for example to make sure that the home directory belongs to user [balloon](balloon.md). 

> `/home/balloon` must belong to `balloon` default user and `balloon` default group.

## desktop.initcontainercommand
The `desktop.initcontainercommand` runs the command at init container. The default value is `None`, the default type is `list`.

desktop.initcontainercommand example :

```
desktop.initcontainercommand : [ 'sh', '-c', 'chown 4096:4096 /home/balloon' ]
```

This option is used when presistent volume data mount a nfs storage. The uid and gid of /home/balloon must be set to the default value of `(balloon:balloon) (4096:4096)`. 


 

## desktop.initcontainerimage

The `desktop.initcontainerimage` is the name of the init container image. The default value is `busybox`. 


## desktop.envlocal

```desktop.envlocal``` is a dictionary. ```desktop.envlocal``` contains a (key,value) added as environment variables to oc.user.


The default value is :

```
{ 
		'DISPLAY': ':0.0', 
		'USER': 'balloon', 
		'LIBOVERLAY_SCROLLBAR': '0',
		'WINEARCH': 'win32',
		'UBUNTU_MENUPROXY': '0',
		'HOME': '/home/balloon',
		'LOGNAME': 'balloon',
		'PULSE_SERVER: '/tmp/.pulse.sock', 
		'CUPS_SERVER': '/tmp/.cups.sock' 
}
``` 

> Add ```'CUPS_SERVER: '/tmp/.cups.sock'```  only if ```desktop.useprintercontainer``` is True.
> Add ```'PULSE_SERVER: '/tmp/.pulse.sock'``` only if ```desktop.usesoundcontainer``` is True.

## desktop.nodeselector
```desktop.nodeselector``` is a dictionary. This option permits to assign user pods to nodes.
It specifies a map of key-value pairs. For the pod to be eligible to run on a node, the node must have each of the indicated key-value pairs as labels (it can have additional labels as well). 
The most common usage is one key-value pair. 

```
{ 'disktype': 'ssd' }
```

## desktop.username

```desktop.username``` describes the [balloon](balloon.md) user created inside the oc.user container.
The type of desktop.username is string. The default value is 'balloon'.

If you change this value, you have to rebuild your own oc.user file
The script oc.user in Dockerfile oc.user :

```
ENV BUSER balloon
RUN groupadd --gid 4096 $BUSER
RUN useradd --create-home --shell /bin/bash --uid 4096 -g $BUSER --groups lpadmin,sudo $BUSER
```

Read the dedicated page on [balloon](balloon.md) to gaet more information about user balloon, uid, and gid.

## desktop.userid
 
```desktop.userid``` describes the ```uid``` of the user created inside the oc.user container.
	The type of desktop.userid is integer. The default value is 4096.

If you change this value, you have to rebuild your own oc.user file
The script oc.user in Dockerfile oc.user :

```
ENV BUSER balloon
RUN useradd --create-home --shell /bin/bash --uid 4096 -g $BUSER --groups lpadmin,sudo $BUSER
```
Read the dedicated page on [balloon](balloon.md) to gaet more information about user balloon, uid, and gid.
 
## desktop.groupid

`desktop.groupid` describes the `gid` of the user created inside the oc.user container. The type of desktop.userid is integer. The default value is 4096.

If you change this value, you have to rebuild your own oc.user file
The script oc.user in Dockerfile oc.user :

```
RUN groupadd --gid 4096 $BUSER
```

Read the dedicated page on [balloon](balloon.md) to gaet more information about user balloon, uid, and gid.

## desktop.userhomedirectory 

`desktop.userhomedirectory` describes the `homedirectory` of the user created inside the oc.user container. The type of `desktop.userhomedirectory` is string. The default value is `/home/balloon`.

If you change this value, you have to rebuild your own oc.user file
The script oc.user in Dockerfile oc.user :

```
ENV BUSER balloon
RUN groupadd --gid 4096 $BUSER
RUN useradd --create-home --shell /bin/bash --uid 4096 -g $BUSER --groups lpadmin,sudo $BUSER
```

Read the dedicated page on [balloon](balloon.md) to gaet more information about user balloon, uid, and gid.


## desktop.uselocaltime

The `desktop.uselocaltime` is boolean, to use host value of `/etc/localtime`.
The default value is `False`.
If `desktop.uselocaltime` is True, this add a volume mapping from host file  `/etc/localtime` to container file `/etc/localtime`.


## desktop.policies
The `desktop.policies` is a dictionary.


## desktop.application_configy
Default application host_config dictionary, maps the dictionary as arguments from docker API 
[create_host_config](https://docker-py.readthedocs.io/en/stable/api.html#docker.api.container.ContainerApiMixin.create_host_config)

Define how the application can be run, read [host_config](config/host_config)  description page to get more informations

## desktop.host_config
Default desktop oc.user host_config dictionary, maps the dictionary as arguments from docker API 
[create_host_config](https://docker-py.readthedocs.io/en/stable/api.html#docker.api.container.ContainerApiMixin.create_host_config)

Define how the oc.user container can be run, read [host_config](config/host_config) description page to get more informations

# Experimental features

## desktop.desktopuseinternalfqdn

WARNING `desktop.desktopuseinternalfqdn` is an **experimental feature**, keep this value to False in production

`desktop.desktopuseinternalfqdn` describes the content of the payload data in the JWT Desktop Token.
The default value is `False`. 

Nginx front end act as a reverse proxy. This reverse proxy use the FQDN of the user's pod to route http request.
If this value is set to `False` the payload data in the JWT Desktop Token contains the **IP Address of the user Pod**.
If this value is set to `True` the payload data in the JWT Desktop Token contains the **FQDN of the user Pod**.

If you CAN NOT add `endpoint_pod_names` in the coredns configuration, you MUST set `desktop.desktopuseinternalfqdn` to `False`.
This choice is less secure.

To set `desktop.desktopuseinternalfqdn` to `True` value, you have to update the `coredns` ConfigMap.

```
kind: ConfigMap
apiVersion: v1
metadata:
  name: coredns
  namespace: kube-system
data:
  Corefile: |
    .:53 {
        log
        errors
        health
        ready
        kubernetes cluster.local in-addr.arpa ip6.arpa {
           endpoint_pod_names
           pods insecure
           fallthrough in-addr.arpa ip6.arpa
           transfer to * 
           ttl 30
        }
        prometheus :9153
        forward . /etc/resolv.conf
        cache 30
        loop
        reload
        loadbalance
    }
```


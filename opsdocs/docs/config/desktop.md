# desktop options in od.config


The od.config contains options to describe how the oc.user and applications containers have to be created. Options differ if abcdesktop.io is running in ```docker mode``` or in ```kubernetes mode```.

## desktop.options


| Option name                           | Type           | Default Value | 
|---------------------------------------|----------------|---------------|
| ```desktop.container_autoremove```   	| boolean        | True          |
| ```desktop.usex11unixsocket```     	| boolean        | True          | 
| ```desktop.userusehostsharememory```  | string         | True          |
| ```desktop.defaultbackgroundcolors``` | list           | [ '#6EC6F0', '#333333',  '#666666', '#CD3C14', '#4BB4E6', '#50BE87', '#A885D8', '#FFB4E6' ] |
| ```desktop.homedirectorytype```    	| string         | 'volume' |
| ```desktop.remotehomedirectorytype``` | list           | [] |
| ```desktop.capabilities```            | dictionary     | ```{}``` | 
| ```desktop.shareipcnamespace```   		| string         | 'shareable' |  
| ```desktop.persistentvolumeclaim```   | string         | None |   
| ```desktop.allowPrivilegeEscalation```| boolean        | False | 
| ```desktop.securityopt```             | list | [ 'no-new-privileges', 'seccomp=unconfined' ]  |
| ```desktop.imagePullSecret```         | string         | None |
| ```desktop.image```     				    | string        | 'abcdesktopio:oc.user.18.04:latest' |
| ```desktop.imageprinter```            | string        | 'abcdesktopio:oc.cupsd.18.04:latest' |
| ```desktop.useprintercontainer```     | boolean        | False |
| ```desktop.soundimage```              | string        | 'abcdesktopio:oc.pulseaudio.18.04' |
| ```desktop.usesoundcontainer```       | boolean        | False |
| ```desktop.usecontainerimage```       | boolean        | False |
| ```desktop.initcontainerimage```      | string         | 'abcdesktopio:oc.busybox' |
| ```desktop.envlocal```     			    | dictionary     | ```{ 'DISPLAY': ':0.0', 'USER': 'balloon', 'LIBOVERLAY_SCROLLBAR': '0','WINEARCH': 'win32','UBUNTU_MENUPROXY': '0','HOME': '/home/balloon','LOGNAME': 'balloon','PULSE_SERVER: 'localhost:4713', 'CUPS_SERVER': 'localhost:631' }``` |
| ```desktop.nodeselector```            | dictionary     | ```{}``` | 
| ```desktop.username```            		| string        | 'balloon' |
| ```desktop.userid``` 						| integer       | 4096 |
| ```desktop.groupid```  					| integer       | 4096 |
| ```desktop.userhomedirectory ```      | string        | '/home/balloon' |
| ```desktop.useinternalfqdn```         | boolean       | False |
| ```desktop.uselocaltime```            | boolean       | False |


## desktop.container_autoremove
The ```desktop.container_autoremove``` is use to remove or not remove an abcdesktop container application.

> When an application container is exited, 
> do we need to remove the container, by running the ```docker rm``` command ?

By default the container_autoremove is ```True```. But if you need to keep your application container to post-mortem debugging or to get some value, set this value to ```False```. Set this value to ```False``` only to troubleshoot an application. 

In production this value MUST be set to ```True```


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

## desktop.userusehostsharememory

The default value is ```True```. When ```desktop.userusehostsharememory``` is ```True```, oc.user desktop container and all user's container application add the shared memory volume mapping to the host.

```
/dev/shm:/dev/shm
```

```/dev/shm``` is an implementation of shared memory concept. Sometimes when the application running inside a Docker container consumes too much memory space, it has to be configured to access the host’s shared memory. Shared memory is memory that may be accessed by multiple programs. It is efficient for passing data between programs. You can check the size of Linux’s shared memory by using this command:

```
df /dev/shm
```

On Linux, to change the size of /dev/shm, run this:
```
mount -o remount,size=2G /dev/shm
```

### Mozilla Firefox browser and Chrome issue :

* After release 59, the Firefox browser in a container may crash when it has less than 2GB of shared memory – this is a pretty widely reported issue and is easily mitigated with a docker run flag (--shm-size=2g or -v /dev/shm:/dev/shm). 
Mozilla Firefox release 59.02 works fine with ```--shm-size=2g```. This value is set in the image label ```oc.shm_size ``` ( see [Applications](/applications) chapter ).

* If you need to run Firefox browser release 60 and above, add the ```-v /dev/shm:/dev/shm```, by setting ```desktop.userusehostsharememory``` to ```True```.



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






## desktop.capabilities

This value is only avalaible in kubernetes, and only to troubleshoot an application.
> This is a Security note for developers
> ```TODO SECURITY Next Realease 1.1```
> add the same value in docker mode
> 
This value is added to the oc.user pod, as securityContext attribut :

```
securityContext:
      capabilities:
        desktop.capabilities
```

For example 

```
desktop.capabilities: { 'add': [ "SYS_ADMIN", "SYS_PTRACE" ]}
```
Permit the oc.user to call ptrace:

*  "SYS_PTRACE": Trace arbitrary processes using ptrace
*  "SYS_ADMIN": Perform a range of system administration operations.

Read the docker run command informations [Docker run reference](https://docs.docker.com/engine/reference/run/) 

By default, Docker has a default list of capabilities that are kept. The following table lists the Linux capability options which can be added or dropped.

| Capability Key | Capability Description |
| -------------- | ---------------------- |
| SETPCAP | Modify process capabilities. |
| SYS_MODULE| Load and unload kernel modules. |
| SYS_RAWIO | Perform I/O port operations (iopl(2) and ioperm(2)). |
| SYS_PACCT | Use acct(2), switch process accounting on or off. |
| SYS_ADMIN | Perform a range of system administration operations. |
| SYS_NICE | Raise process nice value (nice(2), setpriority(2)) and change the nice value for arbitrary processes. |
| SYS_RESOURCE | Override resource Limits. |
| SYS_TIME | Set system clock (settimeofday(2), stime(2), adjtimex(2)); set real-time (hardware) clock. |
| SYS_TTY_CONFIG | Use vhangup(2); employ various privileged ioctl(2) operations on virtual terminals. |
| MKNOD | Create special files using mknod(2). |
| AUDIT_WRITE | Write records to kernel auditing log. |
| AUDIT_CONTROL | Enable and disable kernel auditing; change auditing filter rules; retrieve auditing status and filtering rules. |
| MAC_OVERRIDE | Allow MAC configuration or state changes. Implemented for the Smack LSM. |
| MAC_ADMIN | Override Mandatory Access Control (MAC). Implemented for the Smack Linux Security Module (LSM). |
| NET_ADMIN | Perform various network-related operations. |
| SYSLOG | Perform privileged syslog(2) operations.  |
| CHOWN | Make arbitrary changes to file UIDs and GIDs (see chown(2)). |
| NET_RAW | Use RAW and PACKET sockets. |
| DAC_OVERRIDE | Bypass file read, write, and execute permission checks. |
| FOWNER | Bypass permission checks on operations that normally require the file system UID of the process to match the UID of the file. |
| DAC_READ_SEARCH | Bypass file read permission checks and directory read and execute permission checks. |
| FSETID | Don't clear set-user-ID and set-group-ID permission bits when a file is modified. |
| KILL | Bypass permission checks for sending signals. |
| SETGID | Make arbitrary manipulations of process GIDs and supplementary GID list. |
| SETUID | Make arbitrary manipulations of process UIDs. |
| LINUX_IMMUTABLE | Set the FS_APPEND_FL and FS_IMMUTABLE_FL i-node flags. |
| NET_BIND_SERVICE  | Bind a socket to internet domain privileged ports (port numbers less than 1024). |
| NET_BROADCAST |  Make socket broadcasts, and listen to multicasts. |
| IPC_LOCK | Lock memory (mlock(2), mlockall(2), mmap(2), shmctl(2)). |
| IPC_OWNER | Bypass permission checks for operations on System V IPC objects. |
| SYS_CHROOT | Use chroot(2), change root directory. |
| SYS_PTRACE | Trace arbitrary processes using ptrace(2). |
| SYS_BOOT | Use reboot(2) and kexec_load(2), reboot and load a new kernel for later execution. |
| LEASE | Establish leases on arbitrary files (see fcntl(2)). |
| SETFCAP | Set file capabilities.|
| WAKE_ALARM | Trigger something that will wake up the system. |
| BLOCK_SUSPEND | Employ features that can block system suspend. |

Further reference information is available on the [capabilities(7) - Linux man page](http://linux.die.net/man/7/capabilities)


> Set this value only to troubleshoot an application. 

In production this value MUST be set to an empty dict ```{}```


## desktop.allowPrivilegeEscalation

The ```desktop.allowPrivilegeEscalation``` option allow a user to run a sudo command. The execve system call can grant a newly-started program privileges that its parent did not have, such as the setuid or setgid Linux flags.

The default value is ```False``` 
You should only set ```desktop.allowPrivilegeEscalation``` to run ```sudo``` command.

In production this value MUST be set to ```False```

## desktop.desktopsecurityopt

The ```desktop.desktopsecurityopt``` option allow to set the ```security_opt``` default value for a docker application container. ```security_opt``` is the docker parameter.

* To run without the default seccomp profile ```seccomp=unconfined```
* To disable sudo command add ```no-new-privileges``` to the list. For example: ```[ 'no-new-privileges', 'seccomp=unconfined' ]```

Docker's default seccomp profile is a whitelist which specifies the calls that
are allowed. The table below lists the significant (but not all) syscalls that
are effectively blocked because they are not on the whitelist. The table includes
the reason each syscall is blocked rather than white-listed.

| Syscall             | Description                                                                                                                           |
|---------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| `acct`              | Accounting syscall which could let containers disable their own resource limits or process accounting. Also gated by `CAP_SYS_PACCT`. |
| `add_key`           | Prevent containers from using the kernel keyring, which is not namespaced.                                   |
| `bpf`               | Deny loading potentially persistent bpf programs into kernel, already gated by `CAP_SYS_ADMIN`.              |
| `clock_adjtime`     | Time/date is not namespaced. Also gated by `CAP_SYS_TIME`.                                                   |
| `clock_settime`     | Time/date is not namespaced. Also gated by `CAP_SYS_TIME`.                                                   |
| `clone`             | Deny cloning new namespaces. Also gated by `CAP_SYS_ADMIN` for CLONE_* flags, except `CLONE_USERNS`.         |
| `create_module`     | Deny manipulation and functions on kernel modules. Obsolete. Also gated by `CAP_SYS_MODULE`.                 |
| `delete_module`     | Deny manipulation and functions on kernel modules. Also gated by `CAP_SYS_MODULE`.                           |
| `finit_module`      | Deny manipulation and functions on kernel modules. Also gated by `CAP_SYS_MODULE`.                           |
| `get_kernel_syms`   | Deny retrieval of exported kernel and module symbols. Obsolete.                                              |
| `get_mempolicy`     | Syscall that modifies kernel memory and NUMA settings. Already gated by `CAP_SYS_NICE`.                      |
| `init_module`       | Deny manipulation and functions on kernel modules. Also gated by `CAP_SYS_MODULE`.                           |
| `ioperm`            | Prevent containers from modifying kernel I/O privilege levels. Already gated by `CAP_SYS_RAWIO`.             |
| `iopl`              | Prevent containers from modifying kernel I/O privilege levels. Already gated by `CAP_SYS_RAWIO`.             |
| `kcmp`              | Restrict process inspection capabilities, already blocked by dropping `CAP_SYS_PTRACE`.                          |
| `kexec_file_load`   | Sister syscall of `kexec_load` that does the same thing, slightly different arguments. Also gated by `CAP_SYS_BOOT`. |
| `kexec_load`        | Deny loading a new kernel for later execution. Also gated by `CAP_SYS_BOOT`.                                 |
| `keyctl`            | Prevent containers from using the kernel keyring, which is not namespaced.                                   |
| `lookup_dcookie`    | Tracing/profiling syscall, which could leak a lot of information on the host. Also gated by `CAP_SYS_ADMIN`. |
| `mbind`             | Syscall that modifies kernel memory and NUMA settings. Already gated by `CAP_SYS_NICE`.                      |
| `mount`             | Deny mounting, already gated by `CAP_SYS_ADMIN`.                                                             |
| `move_pages`        | Syscall that modifies kernel memory and NUMA settings.                                                       |
| `name_to_handle_at` | Sister syscall to `open_by_handle_at`. Already gated by `CAP_DAC_READ_SEARCH`.                                      |
| `nfsservctl`        | Deny interaction with the kernel nfs daemon. Obsolete since Linux 3.1.                                       |
| `open_by_handle_at` | Cause of an old container breakout. Also gated by `CAP_DAC_READ_SEARCH`.                                     |
| `perf_event_open`   | Tracing/profiling syscall, which could leak a lot of information on the host.                                |
| `personality`       | Prevent container from enabling BSD emulation. Not inherently dangerous, but poorly tested, potential for a lot of kernel vulns. |
| `pivot_root`        | Deny `pivot_root`, should be privileged operation.                                                           |
| `process_vm_readv`  | Restrict process inspection capabilities, already blocked by dropping `CAP_SYS_PTRACE`.                          |
| `process_vm_writev` | Restrict process inspection capabilities, already blocked by dropping `CAP_SYS_PTRACE`.                          |
| `ptrace`            | Tracing/profiling syscall. Blocked in Linux kernel versions before 4.8 to avoid seccomp bypass. Tracing/profiling arbitrary processes is already blocked by dropping `CAP_SYS_PTRACE`, because it could leak a lot of information on the host. |
| `query_module`      | Deny manipulation and functions on kernel modules. Obsolete.                                                  |
| `quotactl`          | Quota syscall which could let containers disable their own resource limits or process accounting. Also gated by `CAP_SYS_ADMIN`. |
| `reboot`            | Don't let containers reboot the host. Also gated by `CAP_SYS_BOOT`.                                           |
| `request_key`       | Prevent containers from using the kernel keyring, which is not namespaced.                                    |
| `set_mempolicy`     | Syscall that modifies kernel memory and NUMA settings. Already gated by `CAP_SYS_NICE`.                       |
| `setns`             | Deny associating a thread with a namespace. Also gated by `CAP_SYS_ADMIN`.                                    |
| `settimeofday`      | Time/date is not namespaced. Also gated by `CAP_SYS_TIME`.         |
| `stime`             | Time/date is not namespaced. Also gated by `CAP_SYS_TIME`.         |
| `swapon`            | Deny start/stop swapping to file/device. Also gated by `CAP_SYS_ADMIN`.                                       |
| `swapoff`           | Deny start/stop swapping to file/device. Also gated by `CAP_SYS_ADMIN`.                                       |
| `sysfs`             | Obsolete syscall.                                                                                             |
| `_sysctl`           | Obsolete, replaced by /proc/sys.                                                                              |
| `umount`            | Should be a privileged operation. Also gated by `CAP_SYS_ADMIN`.                                              |
| `umount2`           | Should be a privileged operation. Also gated by `CAP_SYS_ADMIN`.                                              |
| `unshare`           | Deny cloning new namespaces for processes. Also gated by `CAP_SYS_ADMIN`, with the exception of `unshare --user`. |
| `uselib`            | Older syscall related to shared libraries, unused for a long time.                                            |
| `userfaultfd`       | Userspace page fault handling, largely needed for process migration.                                          |
| `ustat`             | Obsolete syscall.                                                                                             |
| `vm86`              | In kernel x86 real mode virtual machine. Also gated by `CAP_SYS_ADMIN`.                                       |
| `vm86old`           | In kernel x86 real mode virtual machine. Also gated by `CAP_SYS_ADMIN`.                                       |


Read [security_opt](https://docs.docker.com/engine/security/seccomp/) from the docker website.


## desktop.defaultbackgroundcolors 

The ```desktop.defaultbackgroundcolors``` allow you to change the default background color.

The default value is a list of string ```[ '#6EC6F0', '#333333',  '#666666', '#CD3C14', '#4BB4E6', '#50BE87', '#A885D8', '#FFB4E6' ]```

The ```desktop.defaultbackgroundcolors``` length can contain up to 8 entries. To see the color 


Open the url http://localhost, in your web browser, to start a simple abcdesktop.io container. 

```
http://localhost
```

You should see the abcdesktop.io home page.

Press the ```Connect with Anonymous access, have look```

At the right top corner, click on the menu and choose ```Settings```, then click on ```Screen Colors```

You should see the default background colors, for example :
![defaultbackgroundcolors](img/newbackgroundcolors.png)


## desktop.imagePullSecret


The ```desktop.imagePullSecret``` is the name of the secret used by Kubernetes to access to the private registry.
The type of ```desktop.imagePullSecret``` is a string. This option is only available in Kubernetes mode, and anly used if you need to store the abcdesktop docker image on a private registry. 

* Example to build a registry Kubernetes secret named abcdesktopregistrysecret with the docker hub.

```
kubectl create secret docker-registry abcdesktopregistrysecret --docker-server=https://index.docker.io/v1/ --docker-username=XXXXXXX --docker-password=YYYYYYYU
```

* Example to build a registry Kubernetes secret named abcdesktopregistrysecret with your own privateregistry

```
kubectl create secret docker-registry abcdesktopregistrysecret --docker-server=registry.mydomain.local:443 --docker-username=XXXXXXX --docker-password=YYYYYYYU
```


## desktop.image

The ```desktop.image``` is the name of the X11 server container
The default value is ```abcdesktopio:oc.user.18.04```

## desktop.printerimage

The ```desktop.printerimage``` is the name of the  printer container
The default value is ```abcdesktopio:oc.cupds.18.04```

## desktop.useprintercontainer

The ```desktop.useprintercontainer``` is boolean, to use printer ```cupsd``` service as an separated container.
This value is only available in kubernetes mode.  The default value is ```False```.

## desktop.soundimage

The ```desktop.soundimage``` is the name of the sound container image
The default value is ```abcdesktopio:oc.pulseaudio.18.04```

## desktop.usesoundcontainer

The ```desktop.usesoundcontainer``` is boolean, to use pulseaudio service as an separated container.
This value is only available in kubernetes mode. The default value is ```False```.

## desktop.useinitcontainer

The ```desktop.useinitcontainer``` is boolean, to use init container.
The code call change mode for the user's home directory. The default value is ```False```.

```
chown balloon_uid:balloon_gid homedirectory
```

The initcontainerimage is a busybox shell, run to make sure that the home directory belongs to user [balloon](balloon.md). Pulseaudio check that [balloon](balloon.md) is the owner of his home directory.
Set this value to ```True``` if you read the error message :
```
pulseaudio not working : Home directory not accessible: Permission denied
```

> ```/home/balloon``` must belong to ```balloon``` default user and ```balloon``` default group.


## desktop.initcontainerimage

The ```desktop.initcontainerimage``` is the name of the init container image.
The default value is ```abcdesktopio:oc.busybox```


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
		'CUPS_SERVER': 'localhost:631' 
}
``` 

> Add ```'CUPS_SERVER: 'localhost:631'```  only if ```desktop.useprintercontainer``` is True.
> Add ```'PULSE_SERVER: 'localhost:631'``` only if ```desktop.usesoundcontainer``` is True.

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

```desktop.groupid``` describes the ```gid``` of the user created inside the oc.user container.
	The type of desktop.userid is integer. The default value is 4096.

If you change this value, you have to rebuild your own oc.user file
The script oc.user in Dockerfile oc.user :

```
RUN groupadd --gid 4096 $BUSER
```

Read the dedicated page on [balloon](balloon.md) to gaet more information about user balloon, uid, and gid.

## desktop.userhomedirectory 

```desktop.userhomedirectory``` describes the ```homedirectory``` of the user created inside the oc.user container.
	The type of desktop.userhomedirectory is string. The default value is ```/home/balloon```.

If you change this value, you have to rebuild your own oc.user file
The script oc.user in Dockerfile oc.user :

```
ENV BUSER balloon
RUN groupadd --gid 4096 $BUSER
RUN useradd --create-home --shell /bin/bash --uid 4096 -g $BUSER --groups lpadmin,sudo $BUSER
```

Read the dedicated page on [balloon](balloon.md) to gaet more information about user balloon, uid, and gid.


## desktop.uselocaltime

The ```desktop.uselocaltime``` is boolean, to use host value of ```/etc/localtime```.
The default value is ```False```.
If ```desktop.uselocaltime``` is True, this add a volume mapping from host file  ```/etc/localtime``` to container file ```/etc/localtime```.



# Experimental features

## desktop.desktopuseinternalfqdn

WARNING ```desktop.desktopuseinternalfqdn``` is an **experimental feature**, keep this value to False in production

```desktop.desktopuseinternalfqdn``` describes the content of the payload data in the JWT Desktop Token.
The default value is ```False```. 

Nginx front end act as a reverse proxy. This reverse proxy use the FQDN of the user's pod to route http request.
If this value is set to ```False``` the payload data in the JWT Desktop Token contains the **IP Address of the user Pod**.
If this value is set to ```True``` the payload data in the JWT Desktop Token contains the **FQDN of the user Pod**.

If you CAN NOT add ```endpoint_pod_names``` in the coredns configuration, you MUST set desktop.desktopuseinternalfqdn to ```False```.
This choice is less secure.

To set ```desktop.desktopuseinternalfqdn``` to ```True``` value, you have to update the ```coredns``` ConfigMap.

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


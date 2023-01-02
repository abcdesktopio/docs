# host_config resource description

`host_config` resource description allows to change the running context for docker application.
`host_config` is a dictionary and uses the same format in `applist.json` file and `od.config` file.

The same `host_config` format is reused in a multiple configuration files. `host_config` is present in `applist.json` file to build application image, and in `od.config` to set default running values in desktop and in application.


For example you can set low cpu and memory values to an application like the great X11 xeyes.

```json
{ 	
	"mem_limit":  "32M", 
	"shm_size":   "OM", 
	"cpu_period":  50000, 
	"cpu_quota":   50000, 
	"pid_mode":   false, 
	"network_mode": "none" 
}
```

## host_config entries


| Key name       | Type         | Description                                 |
|----------------|--------------|---------------------------------------------|
|	`auto_remove`	|	bool	     |	enable auto removal of the container on daemon side when the container’s process exits. |
|	`cpu_period`	|	int	        |	The length of a CPU period in microseconds. |
|	`cpu_quota`	|	int	 |	Microseconds of CPU time that the container can get in a CPU period.|
|	`cpu_shares`	|	int	 |	CPU shares relative weight.|
|	`cpuset_cpus`	|	str	|	CPUs in which to allow execution 0 3 0 1 .|
|	`cpuset_mems`	|	str	|	Memory nodes	MEMs in which to allow execution 0 3 0 1. Only effective on NUMA systems. |
|	`device_cgroup_rules`	|	list	|	A list of cgroup rules to apply to the container. |
|	`device_read_bps`	   |	bytes per second | Limit read rate from a device in the form of: [{“Path”: “device_path” “Rate”: rate}] |
|	`device_read_iops`    |	IO per second |  Limit read rate from a device. |
|	`device_write_bps` 	|	bytes per second | Limit write rate from a device. |
|	`device_write_iops` |	IO per second	|	 Limit write rate from a device. |
|	`devices`	|	list	|	Expose host devices to the container as a list of strings in the form <path_on_host>:<path_in_container>:<cgroup_permissions>. For example /dev/sda:/dev/xvda:rwm allows the container to have read write access to the host’s /dev/sda via a node named /dev/xvda inside the container. |
|	`device_requests`	|	list	|	Expose host resources such as GPUs to the container as a list of docker.types.DeviceRequest instances.|
|	`ipc_mode`	|	str	|	Set the IPC mode for the container.|
|	`mem_limit`	|	float or str	|	Memory limit. Accepts float values which represent the memory limit of the created container in bytes or a string with a units identification char 100000b 1000k 128m 1g. |
|	`mem_reservation`	|	float or str	|	Memory soft limit|
|	`mem_swappiness`	|	int	 |	Tune a container s memory swappiness behavior. Accepts number between 0 and 100. |
|	`memswap_limit`	 |	str or int	|	Maximum amount of memory + swap a container is allowed to consume. |
|	`oom_kill_disable`	|	bool	|	Whether to disable OOM killer. |
|	`oom_score_adj`	|	int	|	An integer value containing the score given to the container in order to tune OOM killer preferences. |
|	`shm_size`	|	str or int	|	Size of /dev/shm e.g. 1G. |
|	`cap_add`	|	list of str	|	Add kernel capabilities.  `{ 'add': [ 'SYS_ADMIN', 'SYS_PTRACE' ]} `for example to permit the call ptrace: `SYS_PTRACE`, trace arbitrary processes using ptrace, and `SYS_ADMIN`, perform a range of system administration operations. Read the docker run command informations [https://docs.docker.com/engine/reference/run/](https://docs.docker.com/engine/reference/run/) chapter Runtime privilege and Linux capabilities |
|	`cap_drop`	|	list of str	|	Drop kernel capabilities. |
|	`dns`	 |	list	|	Set custom DNS servers. |
|	`dns_opt`	|	list	|	Additional options to be added to the container’s resolv.conf file |
|	`dns_search`	|	list	|	DNS search domains. |
|	`extra_hosts`	|	dict	|	Additional hostnames to resolve inside the container as a mapping of hostname to IP address. |
|	`group_add`	|	list	|	List of additional group names and/or IDs that the container process will run as. |
|	`isolation`	|	str	|	Isolation technology to use. Default: None. |
|	`pid_mode`	|	str	 or bool |	If set to hostuse the host PID namespace inside the container. If set to host, use the host PID namespace inside the container.|
|	`pids_limit`	|	int	|	Tune a container’s pids limit. Set -1 for unlimited. |
|	`privileged`	|	bool	|	Give extended privileges to this container. |
|	`security_opt`	|	list	|	A list of string values to customize labels for MLS systems such as SELinux. |
|	`storage_opt`	|	dict	|	Storage driver options per container as a key value mapping. |
|	`sysctls`	|	dict	|	Kernel parameters to set in the container. |
|	`ulimits`	|	list	|	Ulimits to set inside the container as a list of docker.types.Ulimit instances. |
|	`userns_mode`	|	str	|	Sets the user namespace mode for the container when user namespace remapping option is enabled. Supported values are: host	 |
|	`uts_mode`	|	str 	|	Sets the UTS namespace mode for the container. Supported values are: host |
|	`runtime`	|	str	 |	Runtime to use with this container. |
|	`network_mode`	|	str	|	One of: bridge Create a new network stack for the container on the bridge network. none No networking for this container. container:<name id> Reuse another container’s network stack. host Use the host network stack. This mode is incompatible with port_bindings.|

 

## Main host_config entries descriptions

### `auto_remove`

The `auto_remove ` is use to remove or not remove an abcdesktop container application or desktop.

> For example, when an application container is exited, 
> do we need to remove the container, by running the ```docker rm``` command ?

By default the auto_remove is `True`. But if you need to keep your application container to post-mortem debugging or to get some value, set this value to `False`. Set this value to `False` only to troubleshoot an application. 

In production this value MUST be set to `True`

### `cpu_period`  `cpu_quota`

`cpu_period` Specify the CPU CFS scheduler period, which is used alongside --cpu-quota. Defaults to 100000 microseconds (100 milliseconds). Most users do not change this from the default. 

`cpu-quota` impose a CPU CFS quota on the container. The number of microseconds per --cpu-period that the container is limited to before throttled. As such acting as the effective ceiling. 


### `privileged`

The `privileged` option runs a user container in `privileged` mode. When the operator executes docker run privileged, docker will enable access to all devices on the host as well as set some configuration in AppArmor or SELinux to allow the container nearly all the same access to the host as processes running outside containers on the host.allow a user to run a sudo command. The default value is `False`. You should only set privilege to True for troobleshooting.
In production this value MUST be set to False.



### `ipc_mode`
The `ipc_mode` value is a string, the default value is `'shareable'`.
This option permits user's container to share the ipc namespace with application
This option is used by pulseaudio service by default. 

| value	  | description         					 |
|-----------|------------------------|
|`''`          	| Use daemon default. |
|`'none'`     | Own private IPC namespace. |
|`'private'`  | Own private IPC namespace. |
|`'shareable'` | Own private IPC namespace, with a possibility to share it with other containers. |
|`'host'`      | Use the host system IPC namespace. |

If not specified, daemon default is used, which can either be "private" or "shareable", depending on the daemon version and configuration.
IPC (POSIX/SysV IPC) namespace provides separation of named shared memory segments, semaphores and message queues.
Shared memory segments are used to accelerate inter-process communication at memory speed, rather than through pipes or through the network stack.
Shared memory is commonly used by databases and custom-built. 
If these types of applications are broken into multiple containers, you might need to share the IPC mechanisms of the containers, using shareable mode for the main (i.e. donor) container, and container:<donor-name-or-ID> for other containers.

## `security_opt`

The `securityopt` option allow to set the `security_opt` default value for a docker application container. `security_opt` is the docker parameter.

* To run without the default seccomp profile `seccomp=unconfined`
* To disable sudo command add `no-new-privileges` to the list. For example: `[ 'no-new-privileges', 'seccomp=unconfined' ]`

Docker's default seccomp profile is a whitelist which specifies the calls that are allowed. The table below lists the significant (but not all) syscalls that are effectively blocked because they are not on the whitelist. The table includes the reason each syscall is blocked rather than white-listed.

| Syscall             | Description                                                                                                  |
|---------------------|--------------------------------------------------------------------------------------------------------------|
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
| `kcmp`              | Restrict process inspection capabilities, already blocked by dropping `CAP_SYS_PTRACE`.                      |
| `kexec_file_load`   | Sister syscall of `kexec_load` that does the same thing, slightly different arguments. Also gated by `CAP_SYS_BOOT`. |
| `kexec_load`        | Deny loading a new kernel for later execution. Also gated by `CAP_SYS_BOOT`.                                 |
| `keyctl`            | Prevent containers from using the kernel keyring, which is not namespaced.                                   |
| `lookup_dcookie`    | Tracing/profiling syscall, which could leak a lot of information on the host. Also gated by `CAP_SYS_ADMIN`. |
| `mbind`             | Syscall that modifies kernel memory and NUMA settings. Already gated by `CAP_SYS_NICE`.                      |
| `mount`             | Deny mounting, already gated by `CAP_SYS_ADMIN`.                                                             |
| `move_pages`        | Syscall that modifies kernel memory and NUMA settings.                                                       |
| `name_to_handle_at` | Sister syscall to `open_by_handle_at`. Already gated by `CAP_DAC_READ_SEARCH`.                               |
| `nfsservctl`        | Deny interaction with the kernel nfs daemon. Obsolete since Linux 3.1.                                       |
| `open_by_handle_at` | Cause of an old container breakout. Also gated by `CAP_DAC_READ_SEARCH`.                                     |
| `perf_event_open`   | Tracing/profiling syscall, which could leak a lot of information on the host.                                |
| `personality`       | Prevent container from enabling BSD emulation. Not inherently dangerous, but poorly tested, potential for a lot of kernel vulns. |
| `pivot_root`        | Deny `pivot_root`, should be privileged operation.                                                           |
| `process_vm_readv`  | Restrict process inspection capabilities, already blocked by dropping `CAP_SYS_PTRACE`.                      |
| `process_vm_writev` | Restrict process inspection capabilities, already blocked by dropping `CAP_SYS_PTRACE`.                      |
| `ptrace`            | Tracing/profiling syscall. Blocked in Linux kernel versions before 4.8 to avoid seccomp bypass. Tracing/profiling arbitrary processes is already blocked by dropping `CAP_SYS_PTRACE`, because it could leak a lot of information on the host.                   |
| `query_module`      | Deny manipulation and functions on kernel modules. Obsolete.                                                 |
| `quotactl`          | Quota syscall which could let containers disable their own resource limits or process accounting. Also gated by `CAP_SYS_ADMIN`. |
| `reboot`            | Don't let containers reboot the host. Also gated by `CAP_SYS_BOOT`.                                          |
| `request_key`       | Prevent containers from using the kernel keyring, which is not namespaced.                                   |
| `set_mempolicy`     | Syscall that modifies kernel memory and NUMA settings. Already gated by `CAP_SYS_NICE`.                      |
| `setns`             | Deny associating a thread with a namespace. Also gated by `CAP_SYS_ADMIN`.                                   |
| `settimeofday`      | Time/date is not namespaced. Also gated by `CAP_SYS_TIME`.                                                   |
| `stime`             | Time/date is not namespaced. Also gated by `CAP_SYS_TIME`.                                                   |
| `swapon`            | Deny start/stop swapping to file/device. Also gated by `CAP_SYS_ADMIN`.                                      |
| `swapoff`           | Deny start/stop swapping to file/device. Also gated by `CAP_SYS_ADMIN`.                                      |
| `sysfs`             | Obsolete syscall.                                                                                            |
| `_sysctl`           | Obsolete, replaced by /proc/sys.                                                                             |
| `umount`            | Should be a privileged operation. Also gated by `CAP_SYS_ADMIN`.                                             |
| `umount2`           | Should be a privileged operation. Also gated by `CAP_SYS_ADMIN`.                                             |
| `unshare`           | Deny cloning new namespaces for processes. Also gated by `CAP_SYS_ADMIN`, with the exception of `unshare --user`. |
| `uselib`            | Older syscall related to shared libraries, unused for a long time.                                            |
| `userfaultfd`       | Userspace page fault handling, largely needed for process migration.                                          |
| `ustat`             | Obsolete syscall.                                                                                             |
| `vm86`              | In kernel x86 real mode virtual machine. Also gated by `CAP_SYS_ADMIN`.                                       |
| `vm86old`           | In kernel x86 real mode virtual machine. Also gated by `CAP_SYS_ADMIN`.                                       |


Read [security_opt](https://docs.docker.com/engine/security/seccomp/) from the docker website.



## capabilities `cap_add` `cap_drop`


This value is added to the oc.user docker container, or as securityContext attribut in kubernetes mode :

```
securityContext:
      capabilities:
        desktop.capabilities
```

For example 

```json 
	{ 
		'add': [ "SYS_ADMIN", "SYS_PTRACE" ]
	}
```

Permit a container  to call ptrace:

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






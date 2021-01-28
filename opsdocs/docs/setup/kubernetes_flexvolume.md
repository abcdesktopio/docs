
# CIFS Flexvolume Plugin for Kubernetes

Driver for [CIFS](https://en.wikipedia.org/wiki/Server_Message_Block) (SMB, Samba, Windows Share) network filesystems as [Kubernetes volumes](https://kubernetes.io/docs/concepts/storage/volumes/).

abcdesktop team is not the authors of the CIFS Flexvolume Plugin for kubernetes. This file is an update from the original source file [https://raw.githubusercontent.com/fstab/cifs/](https://raw.githubusercontent.com/fstab/cifs/master/README.md). The original source code is [https://github.com/fstab/cifs](https://raw.githubusercontent.com/fstab/cifs/master/README.md)
The author is [Fabian Stäber](https://github.com/fstab).
The update is part for abcdesktop.io

This article is just an update from [Fabian Stäber](https://github.com/fstab) work.

## Background 

Docker containers running in Kubernetes have an ephemeral file system: Once a container is terminated, all files are gone. In order to store persistent data in Kubernetes, you need to mount a [Persistent Volume](https://kubernetes.io/docs/concepts/storage/volumes/) into your container. Kubernetes has built-in support for network filesystems found in the most common cloud providers, like [Amazon's EBS](https://aws.amazon.com/ebs), [Microsoft's Azure disk](https://azure.microsoft.com/en-us/services/storage/unmanaged-disks/), etc. However, some cloud hosting services, like the [Hetzner cloud](https://hetzner.cloud), provide network storage using the CIFS (SMB, Samba, Windows Share) protocol, which is not natively supported in Kubernetes.

Fortunately, Kubernetes provides [Flexvolume](https://github.com/kubernetes/community/blob/master/contributors/devel/flexvolume.md), which is a plugin mechanism enabling users to write their own drivers. There are a few flexvolume drivers for CIFS out there, but for different reasons none of them seemed to work for me. So [Fabian Stäber](https://github.com/fstab) wrote this driver.

## Installing

The flexvolume plugin is a single shell script named [cifs](https://github.com/abcdesktopio/cifs). This shell script must be available on the Kubernetes master and on each of the Kubernetes nodes. By default, Kubernetes searches for third party volume plugins in ```/usr/libexec/kubernetes/kubelet-plugins/volume/exec/```. 

The plugin directory can be configured with the kubelet's ```--volume-plugin-dir``` parameter, run ```ps aux | grep kubelet``` to learn the location of the plugin directory on your system (see [#1][9]). The `cifs` script must be located in a subdirectory named `fstab~cifs/`. The directory name `abcdesktop~cifs/` will be [mapped](https://github.com/kubernetes/community/blob/master/contributors/devel/flexvolume.md#prerequisites) to the Flexvolume driver name `abcdesktop/cifs`.

On the Kubernetes master and on each Kubernetes node run the following commands:


```bash
VOLUME_PLUGIN_DIR="/usr/libexec/kubernetes/kubelet-plugins/volume/exec"
mkdir -p "$VOLUME_PLUGIN_DIR/abcdesktop~cifs"
cd "$VOLUME_PLUGIN_DIR/abcdesktop~cifs"
curl -L -O https://raw.githubusercontent.com/abcdesktop/cifs/main/cifs
chmod 755 cifs
```

The `cifs` script requires a few executables to be available on each host system:

* `mount.cifs`, on Ubuntu this is in the [cifs-utils](https://packages.ubuntu.com/bionic/cifs-utils) package.
* `jq`, on Ubuntu this is in the [jq](https://packages.ubuntu.com/bionic/jq) package.
* `mountpoint`, on Ubuntu this is in the [util-linux](https://packages.ubuntu.com/bionic/util-linux) package.
* `base64`, on Ubuntu this is in the [coreutils](https://packages.ubuntu.com/bionic/coreutils) package.

 
```bash
apt-get install cifs-utils jq util-linux coreutils

```

To check if the installation was successful, run the following command:

```bash
VOLUME_PLUGIN_DIR="/usr/libexec/kubernetes/kubelet-plugins/volume/exec"
$VOLUME_PLUGIN_DIR/abcdestkop~cifs/cifs init

```

It should output a JSON string containing `"status": "Success"`. This command is also run by Kubernetes itself when the cifs plugin is detected on the file system.




## Update your od.config file

In this example, we use a Microsoft Active Directory as a LDAP Server.
 
Add a rules to add ```TAG``` to the authentification provider



 
```

# Add an explicit authmanagers
authmanagers: {	
	'explicit': {
	    'show_domains': True,
	    'default_domain': 'AD',
	    'providers': {
	      'AD': { 
	        'config_ref': 'adconfig', 
	        'enabled': True
	       }
	    }
	}
}


# add the configuration reference for adconfig
adconfig : { 'AD': {   'default'       : True, 
                       'ldap_timeout'  : 15,
                       'ldap_protocol' : 'ldap',
                       'ldap_basedn'   : 'DC=ad,DC=domain,DC=local',
                       'ldap_fqdn'     : '_ldap._tcp.ad.domain.local',
                       'domain'        : 'AD',
                       'domain_fqdn'   : 'AD.DOMAIN.LOCAL',
                       'servers'       : [ '192.168.7.12' ],
                       'kerberos_realm': 'AD.DOMAIN.LOCAL' }
     }
}


 
```
 

## Testing


If everything is fine, start a new login in abcdesktop to see if it worked:


```bash
kubectl exec -ti busybox /bin/sh

```

Inside the container, you should see the CIFS share mounted to `/home/ballloon/U`.






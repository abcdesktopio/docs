# desktop.policies


The `desktop.policies` configuration defines rules for attaching additional `volumes` and `network` interfaces to user pods. Each rule matches a label value.

If a user is assigned the label `'hello'`, then `volumes['hello']` and `network['hello']` are applied to that user's pod.

- `volumes` defines additional volumes to be mounted in the pod
  - for example, mounting an NFS share for all members of a group
  
- `network` defines additional network interfaces and command hooks for a pod
  - Add a new network interface to a pod
  - Run commands to update DNS entries for a pod (on creation or deletion)

## volumes

`volumes` is a dictionary of label-keyed lists. Each entry describes the `mountPath` to be mounted inside the pod and the volume `type`.

Supported volume types are `nfs`, `hostPath`, `pvc`, and `cifs`.

```json
desktop.policies: { 
  'rules': { 
    'volumes': 
      { 'shipcrew': [ 
         { 'type': 'hostPath', 
           'name': 'mntmyproject', 
           'path': '/mnt/sharedhost',
           'mountPath': '/mnt/testmyproject'
         } 
        ] } } }
```

> If the user is assigned the `shipcrew` label, the mount point `/mnt/testmyproject` is added as a `hostPath` volume mapped to `/mnt/sharedhost` in the pod.

### volume type `nfs`

```json
desktop.policies: { 
  'rules': { 
    'volumes': {
		'nfsisostore': [ 
		 {	'type': 'nfs', 
			'name': 'isostore', 
			'server': '192.168.7.112',
			'path': '/volume1/isostore',
			'mountPath': '/mnt/iso'
		 } ]
    } } } 
```

> If the user is assigned the `nfsisostore` label, the mount point `/mnt/iso` is added to the pod as an NFS mount targeting `192.168.7.112:/volume1/isostore`.

Requirements

- `type`:`nfs` 
- `name` (string) is the name of the volume 
- `mountPath` (string) is the mountPath of the volume
- `server` (string) is the NFS server hostname or IP address
- `path` (string) is the NFS export path on the server


Options

- `readOnly` (boolean) whether the mount should be read-only


### volume type `hostPath`


```json
desktop.policies: { 
  'rules': { 
    'volumes': {
		'shipcrew': [ 
		 { 
		    'type': 'hostPath', 
		    'name': 'mntmyproject', 
		    'path': '/mnt/sharedhost',
		    'mountPath': '/mnt/testmyproject'
		 } ] 
	 } } } 
```

Requirements

- `type`:`hostPath` 
- `name` (string) is the name of the volume 
- `mountPath` (string) is the mountPath of the volume
- `path` (string) is the absolute path on the host node


> If the user is assigned the `shipcrew` label, the mount point `/mnt/testmyproject` is added to the pod as a `hostPath` volume mapped to `/mnt/sharedhost`.

### volume type `pvc`

```json
desktop.policies: { 
  'rules': { 
    'volumes': {
		'nfspvc': [ {
		    'type': 'pvc', 
		    'name': 'pvcstore', 
		    'claimName': 'pvc-store',
		    'mountPath': '/mnt/newpvcstore' 
		 } ]
	 } } }
```

Requirements

- `type`:`pvc` 
- `name` (string) is the name of the volume 
- `mountPath` (string) is the mountPath of the volume
- `claimName` (string) is the PersistentVolumeClaim name

> If the user is assigned the `nfspvc` label, the mount point `/mnt/newpvcstore` is added to the pod using the PVC named `pvc-store`.



## network


```
desktop.policies: { 
  'rules': { 
     'network': { 
      'shipcrew':  { 
        'webhook': { 
          'create':  'curl "http://{{ livedns_fqdn }}:8080/update?secret={{ livedns_secret }}&domain=desktop.yourdomain.net&hostname={{ name }}&addr={{ net2 }}"',
          'destroy': 'curl "http://{{ livedns_fqdn }}:8080/update?secret={{ livedns_secret }}&domain=desktop.yourdomain.net&hostname={{ name }}&addr={{ net2 }}"'
        },
        'annotations' : { 
          'k8s.v1.cni.cncf.io/networks': '[ {"name":"macvlan-conf-7"} ]' 
        }
    }          
```


> If the user is assigned the `shipcrew` label:

- The webhook `create` command is executed when the pod is created.
- The webhook `destroy` command is executed when the pod is deleted.
- The `annotations` dictionary is merged into the pod's metadata annotations.
 
For all fields, template entries in the form `{{ VAR }}` are replaced with the corresponding runtime value.



- desktop.webhookdict is a dictionary with key/value for `webhook` configuration

```
desktop.webhookdict: {  
  'fw_ip': '1.2.3.4', 
  'api_key': 'CAFECAFE', 
  'livedns_secret': 'ThisISMyDesktop',
  'livedns_fqdn': 'ns01desktop.yourdomain.net' }
```

The desktop interfaces are generated during the provisioning process

``` 
{ 
 'eth0': {'mac': '56:c7:eb:dc:c0:b8', 'ips': '10.244.0.239'  }, 
 'net1': {'mac': '2a:94:43:e0:f4:46', 'ips': '192.168.9.137' }, 
 'net2': {'mac': '1e:50:5f:b7:85:f6', 'ips': '194.3.2.1'     }
}
```

> Only the `ips` field replace the value of `eth0` or `net1` or `net2`.
> The number of interface is not limited.

For example, the command line 

```
curl "http://{{ livedns_fqdn }}:8080/update?secret={{ livedns_secret }}&domain=desktop.yourdomain.net&hostname={{ name }}&addr={{ net2 }}"
```

becomes

```
curl "http://ns01desktop.yourdomain.net:8080/update?secret=ThisISMyDesktop&domain=desktop.yourdomain.net&hostname=pod_fry3241&addr=194.3.2.1"
```


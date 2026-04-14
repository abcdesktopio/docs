# desktop.policies


`desktop.policies` defines some rules to add `volumes` and `network`.
Each rules matchs the labels value.

If a user gets the label `'hello'`, then `volumes['hello']`  and `network['hello']` are applied.

- `volumes` are defined to build additional volumes
> - like mount a nfs shared point for each member of a group
  
- `network` is defined to add networks and run command line
> - add a new network interface for a pod
> - run some commands to update dns entries for a pod ( on create, on delete )

## volumes

`volumes` is a dictionnay of list of matching labels. 
Each volume describes the `mountPath` to be mounted inside the pod, and a dedicated `type`.

The type of a volume can be `nfs`, `hostPath`, `pvc` or `cifs`

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

> if the user gets `shipcrew` as label, the add the mount point '/mnt/testmyproject' as a hostPath to '/mnt/sharedhost' in the pod

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

> if the user gets `nfsisostore` as label, the add the mount point '/mnt/iso' in the pod as a nfs mount to `192.168.7.112:/volume1/isostore`

Requirements

- `type`:`nfs` 
- `name` (string) is the name of the volume 
- `mountPath` (string) is the mountPath of the volume
- `server` (string) is the nfs server
- `path` (string) is the export 


Option

- `readOnly` (boolean) if the mount should be in ReadOnly 


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
- `path` (string) is the export nfs value


> if the user gets `shipcrew` as label, the add the mount point '/mnt/testmyproject' as a hostPath to '/mnt/sharedhost' in the pod

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
- `claimName ` (string) is the pvc claim

> if the user gets `nfspvc` as label, the add the mount point '/mnt/newpvcstore' as a pvc named 'pvc-store'



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


> if the user gets `shipcrew` as labels

- execute the bash command line on create pods
- execute the bash command line on delete pods 
- add the 'annotations' : `{ 'k8s.v1.cni.cncf.io/networks': '[ {"name":"macvlan-conf-7"} ]' }` tp the pod 
 
For the all fileds, the entries `{{ VAR }}` is replaced by the value of `VAL`.



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


# desktop options in od.config

The od.config contains options to describe how the oc.user and applications containers have to be created. 

## desktop.options

All desktop options are defined in od.config file.
Desktop options start with the prefix `desktop.`, then add the name of the option.

| Option name                           | Type           | Sample                             |
|---------------------------------------|----------------|------------------------------------|
| `desktop.defaultbackgroundcolors`     | list           | ['#6EC6F0', '#CD3C14', '#4BB4E6' ] |
| `desktop.homedirectorytype`           | string         | 'hostPath'                         |
| `desktop.remotehomedirectorytype`     | list           | []                                 |
| `desktop.persistentvolumespec`        | string         | None                               |
| `desktop.persistentvolumeclaimspec`   | string         | None                               |
| `desktop.homedirectorytype`           | string         | 'hostPath'                         |
| `desktop.envlocal`                    | dictionary     | `{ 'X11LISTEN':'tcp'}`             |
| `desktop.nodeselector`                | dictionary     | `{}`                               |
| `desktop.username`                    | string         | 'balloon'                          |
| `desktop.userid`                      | integer        | 4096                               |
| `desktop.groupid`                     | integer        | 4096                               |
| `desktop.userhomedirectory`           | string         | `'/home/balloon'`                  |
| `desktop.useinternalfqdn`             | boolean        | False                              |
| `desktop.uselocaltime`                | boolean        | False                              |
| `desktop.policies`                    | dictionary     | `{ 'rules':{}, 'max_app_counter':5 }`  |
| `desktop.webhookdict`                 | dictionary     | `{}`                               |


## desktop.homedirectory

This option describes how to create the home directory for the user. The value can be defined as :

* `'None'`: no dedicated volume is created, the oc.user container use an `emptyDir': { 'medium': 'Memory'}`. All user data will be removed at logout.
* `'hostPath'`: set a dedicated 'hostPath' volume, the user's container and applications share this volume. User home data are persistent.
* `'persistentVolumeClaim'`: set a dedicated 'persistentVolumeClaim' volume, the user's container and applications share this volume. User home data are persistent.

To get more information about user's home directory volume, read the [volumes](../volumes) chapter

## desktop.remotehomedirectorytype

desktop.remotehomedirectorytype is a list of string. Each string describe if the remount access to a directory is allowed.
example [ 'cifs', 'webdav' ]

For each entry in the desktop.remotehomedirectorytype list, abcdesktop.io try to mount the remote file system using data from the implicit auth provider.

If `desktop.remotehomedirectorytype` contains 'cifs' and if the authentification provider get `homeDrive` and `homeDirectory` attributs then abcdesktop request the kubernetes abcdesktop/CIFS Driver to mount the remote filesystem.
The user find a mount point named `homeDrive` value, and mounted to `homeDirectory`.

## desktop.defaultbackgroundcolors

The `desktop.defaultbackgroundcolors` allow you to change the default background color.

The default value is a list of string `[ '#6EC6F0', '#333333',  '#666666', '#CD3C14', '#4BB4E6', '#50BE87', '#A885D8', '#FFB4E6' ]`

The `desktop.defaultbackgroundcolors` length can contain up to 8 entries. To see the color 


Open the url http://localhost:30443, in your web browser, to start a simple abcdesktop.io container. 

``` url
http://localhost:30443
```

You should see the abcdesktop.io home page.

Press the `Connect with Anonymous access, have look`

At the right top corner, click on the menu and choose ```Settings```, then click on ```Screen Colors```

You should see the default background colors, for example :
![defaultbackgroundcolors](img/newbackgroundcolors.png)

## desktop.envlocal

`desktop.envlocal` is a dictionary. `desktop.envlocal` contains a (key,value) added as environment variables to oc.user.


The default value is :

```json
{ 
  'X11LISTEN': 'tcp'
}
```

### Reserved variables


| Variable      | Values        | Description                                           |
|---------------|---------------|-------------------------------------------------------|
| `X11LISTEN`   | `tcp`         | permit X11 to listen on tcp port, default is `udp`    |
| `ABCDESKTOP_RUN_DIR`   | `/var/run/desktop`  | directory to write pid services   |
| `ABCDESKTOP_LOG_DIR`   | `/var/log/desktop`  | directory to write log files services   |
| `DISABLE_REMOTEIP_FILTERING` | `disabled`    | disabled remote ip filtering inside pod user, default is `disabled`, change to `enabled` to remove core ip filtering |
| `SET_DEFAULT_WALLPAPER` | `myfile.jpeg`    | name of file to set the user wallpaper, this file must exist in `~/.wallpapers` |
| `SET_DEFAULT_COLOR ` | `#6EC6F0`    | Value of default colour saved in file `~/.store/currentColor`      | 
| `SENDCUTTEXT` | `enabled` | Send clipboard changes to user. Set value to `disabled` to disable clipboard changes to user web browser. This value is overwrite by label `ABCDESKTOP_LABEL_sendcuttext` if exist `SENDCUTTEXT=${ABCDESKTOP_LABEL_sendcuttext:-$SENDCUTTEXT}`. The default value is `enabled` | 
| `ACCEPTCUTTEXT` | `enabled` | Accept clipboard updates from user. Set value to `disabled` to disable clipboard changes to user web browser.  This value is overwrite by label `ABCDESKTOP_LABEL_acceptcuttext` if exist `ACCEPTCUTTEXT=${ABCDESKTOP_LABEL_acceptcuttext:-$ACCEPTCUTTEXT}`. The default value is `enabled` | 




## desktop.nodeselector

`desktop.nodeselector` is a dictionary. This option permits to assign user pods to nodes.

It specifies a map of key-value pairs. For the pod to be eligible to run on a node, the node must have each of the indicated key-value pairs as labels (it can have additional labels as well). 
The most common usage is one key-value pair. 

The value must be a string, by example 'true', and matches the labels node value.  

``` json
desktop.nodeselector:  { 'abcdesktopworker': 'true' }
```

To set a label `abcdesktopworker=true` to a node 

```bash
kubectl label node $YOUR_NODE abcdesktopworker=true
```

The commands returns

```
node/nodesample01 labeled
```

To list all labels on all nodes 

```bash
kubectl -n abcdesktop get nodes --template '{{range .items}}{{.metadata.labels}}{{"\n"}}{{end}}'
```

The commands returns

```json
map[beta.kubernetes.io/arch:amd64 beta.kubernetes.io/os:linux kubernetes.io/arch:amd64 kubernetes.io/hostname:abc3cp01 kubernetes.io/os:linux node-role.kubernetes.io/control-plane: node.kubernetes.io/exclude-from-external-load-balancers:]
map[abcdesktopworker:true beta.kubernetes.io/arch:amd64 beta.kubernetes.io/os:linux kubernetes.io/arch:amd64 kubernetes.io/hostname:abc3ws01 kubernetes.io/os:linux node-role.kubernetes.io/worker:worker]
map[abcdesktopworker:true beta.kubernetes.io/arch:amd64 beta.kubernetes.io/os:linux kubernetes.io/arch:amd64 kubernetes.io/hostname:abc3ws02 kubernetes.io/os:linux node-role.kubernetes.io/worker:worker]
map[abcdesktopworker:true beta.kubernetes.io/arch:amd64 beta.kubernetes.io/os:linux kubernetes.io/arch:amd64 kubernetes.io/hostname:abc3ws03 kubernetes.io/os:linux node-role.kubernetes.io/worker:worker]
```

`desktop.nodeselector` is used as selector by pyos to create user's pods and to pull container's images.


## desktop.username

```desktop.username``` is the name of the default username inside the user's pod.
If you define a LDAP auth with Posix ObjectClass support, this value is overwrite by the LDAP entry
The type of desktop.username is string. The default value is 'balloon'.

## desktop.userid

```desktop.userid``` describes the ```uid Number``` of the default user id number inside the user's pod.
If you define a LDAP auth with Posix ObjectClass support, this value is overwrite by the LDAP entry
The type of desktop.userid is integer. The default value is 4096.


## desktop.groupid

```desktop.groupid ``` describes the ```gid Number``` of the default group id number inside the user's pod.
If you define a LDAP auth with Posix ObjectClass support, this value is overwrite by the LDAP entry
The type of desktop.userid is integer. The default value is 4096.

## desktop.userhomedirectory

`desktop.userhomedirectory` describes the `homedirectory` of the user created inside the user's pod.
If you define a LDAP auth with Posix ObjectClass support, this value is overwrite by the LDAP entrycontainer. The type of `desktop.userhomedirectory` is string. The default value is `/home/balloon`.


## desktop.uselocaltime

The `desktop.uselocaltime` is boolean, to use host value of `/etc/localtime`.
The default value is `False`.
If `desktop.uselocaltime` is True, this add a volume mapping from host file  `/etc/localtime` to container file `/etc/localtime`.

## desktop.policies

`desktop.policies` has a dictionary format.

| Entry       | Description | 
|-------------|------------------------------|
| `max_app_counter` | limit applications counter, without checking the docker container status |
| `rules`      |	rules dictionary `'rules': { 'volumes': { 'domainuser':  { 'type': 'cifs', 'name': 'homedirectory', 'volumename': 'homedir' } }` |
| `acl`	 | allow or denied desktop creation |

Example

``` json
desktop.policies: { 
  'rules': { 
    'volumes': { 
      'domainuser':   { 'type': 'cifs', 'name': 'homedirectory', 'volumename': 'homedir' },
      'Mygroupteam':  { 'type': 'cifs', 'name': 'toto', 'unc': '//192.168.7.101/team', 'volumename': 'team' } 
	  } 
  },
  'acls' : {},
  'max_app_counter' : 4  
}
```

## desktop.webhookdict

desktop.webhookdict is a dictionary to add key/value to the command `create` and `destroy` in rules objects.

## Experimental features

### desktop.desktopuseinternalfqdn

WARNING `desktop.desktopuseinternalfqdn` is an **experimental feature**, keep this value to False in production

`desktop.desktopuseinternalfqdn` describes the content of the payload data in the JWT Desktop Token.
The default value is `False`. 

Nginx front end act as a reverse proxy. This reverse proxy use the FQDN of the user's pod to route http request.
If this value is set to `False` the payload data in the JWT Desktop Token contains the **IP Address of the user Pod**.
If this value is set to `True` the payload data in the JWT Desktop Token contains the **FQDN of the user Pod**.

If you CAN NOT add `endpoint_pod_names` in the coredns configuration, you MUST set `desktop.desktopuseinternalfqdn` to `False`.
This choice is less secure.

To set `desktop.desktopuseinternalfqdn` to `True` value, you have to update the `coredns` ConfigMap.

``` yaml
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

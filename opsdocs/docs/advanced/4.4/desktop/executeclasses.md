# executeclasses 

The `executeclasses` configuration defines resource profiles for desktop pods and application containers. It allows you to control resource allocation either by defining static rules or by letting users select from a predefined set of profiles. The `executeclasses` value is a dictionary in which each entry describes a distinct resource profile.


## `executeclasses` dictionary

```
executeclasses : {
  'default':{
    'nodeSelector':None,
    'description': 'default: up to 4 CPU cores and 8Gi',
    'runtimeClassName': None,
    'resources':{
      'requests':{'memory':"576Mi",'cpu':"220m"},       
      'limits':  {'memory':"8Gi",'cpu':"4000m"}
    }
  },
  'bronze':{
    'nodeSelector':None,
    'runtimeClassName': None,
    'description': 'bronze: up to 2 CPU cores and 8Gi',
    'resources':{
      'requests':{'memory':"576Mi",'cpu':"220m"},
      'limits':  {'memory':"8Gi",'cpu':"2000m"}
    }
  },
  'silver':{
    'nodeSelector': None,
    'description': 'silver: 4 CPU cores and 32Gi RAM',
    'runtimeClassName': None,
    'resources':{
      'requests':{'memory':"2Gi",'cpu':"2000m"},       
      'limits':{'memory':"32Gi",'cpu':"4000m"} 
    }
  },
  'gold':{
    # give a gpu to graphical container
    'containers' : { 'graphical': { 'resources': { 'limits': { 'nvidia.com/gpu':'1' } } } },
    'nodeSelector':{'nvidia.com/gpu': 'true'},
    'description': 'gold: 4 CPU cores, 32Gi RAM and 1 GPU',
    'runtimeClassName': 'nvidia',
    'resources':{
      'requests':{'memory':"2Gi",'cpu':"4000m"},       
      'limits':  {'memory':"32Gi",'cpu':"4000m"}
    }
  },
  'platinum':{
    # give a gpu to graphical container
    'containers' : { 'graphical': { 'resources': { 'limits': { 'nvidia.com/gpu':'1' } } } },
    # nodeselector optional 
    'nodeSelector':{'nvidia.com/gpu': 'true'},
    # this appears only on web interface 
    'description': 'platinum: 8 CPU cores, 128G RAM and 1 GPU',
    'runtimeClassName': 'nvidia',
    'resources':{
      'requests':{'memory':"4Gi",'cpu':"4000m"},       
      'limits':{'memory':"128Gi",'cpu':"8000m"} 
    }
  }}
```
  
The `'default'` entry is mandatory and must always be present.



| key                | type    | Description  | Values | 
|--------------------|---------|--------------|--------|
| containers         | dict    | Merge additional per-container configuration (e.g., resource limits) | `{ 'graphical': { 'resources': { 'limits': { 'nvidia.com/gpu':'1' } } } }` |
| nodeSelector       | dict    | Merge additional node selector constraints | `{'nvidia.com/gpu': 'true'}` |
| description        | string  | Display text shown on the login page | `'platinum: 8 CPU cores, 128G RAM and 1 GPU'` |
| runtimeClassName   | string  | (Optional) Name of the Kubernetes runtime class | `nvidia` |
| resources          | dict    | Pod resource requests and limits | `{ 'requests': {'memory':"4Gi",'cpu':"4000m"}, 'limits':{'memory':"128Gi",'cpu':"8000m"} }` |



## Define the `executeclassname` value

The `executeclassname` variable is an entry key in the `executeclasses` dictionary. It determines the `resources`, `nodeSelector`, and `runtimeClassName` applied to a user's pod. The `executeclassname` value is resolved during the authentication process.

A user can choose the `executeclassname` value from a predefined list, or it can be assigned automatically via rules. If `executeclassname` is not set, it defaults to the string `'default'`, and the corresponding entry `executeclasses['default']` is used.


### Set `executeclassname` by rules

Update your `od.config` file to add a new rule. The `label` of the rule must be `executeclassname`, and the `load` value sets the `executeclassname`.

```
	'rule-executeclass': {
            'conditions' : [ { 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',   'expected' : True  } ],
            'expected' : True,
            'label':'executeclassname',
            'load': 'silver'
    },
```

If the user is a member of the group `cn=ship_crew,ou=people,dc=planetexpress,dc=com`, the label `executeclassname` is set to the value `silver`. A complete example of the `ldapconfig` is shown below.

```
ldapconfig : {
    'planet': {
            'default'       : True,
            'ldap_timeout'  : 15,
            'ldap_protocol' : 'ldap',
            'ldap_basedn'   : 'ou=people,dc=planetexpress,dc=com',
            'servers'       : [ 'openldap' ],
            'serviceaccount': { 'login': 'cn=admin,dc=planetexpress,dc=com', 'password': 'GoodNewsEveryone' },
            'policies': {
                    'acls': None,
                    'rules' : {
                            'rule-dummy' : {
                              'conditions' : [ {'boolean':True, 'expected':True } ],
                                                            'expected' : True,
                                                            'label':'labeltrue'
                            },
                            'rule-ship': {
                                    'conditions' : [ { 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',   'expected' : True  } ],
                                    'expected' : True,
                                    'label':'shipcrew'
                            },
                            'rule-executeclass': {
                                    'conditions' : [ { 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',   'expected' : True  } ],
                                    'expected' : True,
                                    'label':'executeclassname',
                                    'load': 'silver'
                            },
                            'rule-staff': {
                                    'conditions' : [ { 'memberOf': 'cn=admin_staff,ou=people,dc=planetexpress,dc=com', 'expected' : True  } ],
                                    'expected' : True,
                                    'label': 'adminstaff'
                            }
                    }
            } } }
```

- Save the updated `od.config` file and reload the abcdesktop configuration.

```

```

Navigate to the abcdesktop service URL and sign in as a user who is a member of `ship_crew`. `Philip J. Fry` is a member of `ship_crew`.

![login rules sylver](img/login-rules-userinfo-silver.png)

> The pod is created with the requested resources.

![login pod sylver](img/login-rules-pod-silver.png)

- Get the pod description.

```
NAMESPACE=abcdesktop
kubectl get pods -l type=x11server -n $NAMESPACE
```

The expected stdout output is:

```
NAME             READY   STATUS    RESTARTS   AGE
fry-f7c42        4/4     Running   0          7s
```

Inspect the user pod named `fry-f7c42`; replace `POD_NAME` with your actual pod name.

```
NAMESPACE=abcdesktop
POD_NAME=fry-f7c42
kubectl describe pods $POD_NAME -n $NAMESPACE
```

A label `executeclassname` is applied to the user's pod:

```
Labels:           abcdesktop/role=desktop
                  access_provider=planet
                  access_providertype=ldap
                  access_userid=fry
                  access_username=philip-j.-fry
                  executeclassname=silver
                  ...
```

The resource limits and requests are derived from the `silver` execute class.

```
Resources:
  Limits:
    cpu:     4
    memory:  32Gi
  Requests:
    cpu:     2
    memory:  2Gi
```

- Read the execute class information from the web user interface.

The dialog box `settings`:`user information` displays the user's labels.

![login resources sylver](img/login-resource-userinfo-silver.png)

The current user has selected `silver`.



- Open a webshell to read the environment variables.

![login resources sylver](img/login-resources-silver-env.png)

Inside the pod, the environment variable `ABCDESKTOP_EXECUTE_CLASSNAME` is set to the value `silver`.

```
echo $ABCDESKTOP EXECUTE_CLASSNAME
silver
```

Inside the pod, the environment variable `ABCDESKTOP_EXECUTE_CLASS` is set to the selected JSON configuration object.

```
echo $ABCDESKTOP_EXECUTE_CLASS
{"nodeSelector": {}, "description": "silver: 4 CPU cores and 32Gi RAM", "runtimeClassName": null, "resources": {"requests": {"memory": "2Gi", "cpu": "2000m"}, "limits": {"memory": "32Gi", "cpu": "4000m"}}}
```



### Allow users to choose the `executeclassname`

To allow users to choose the `executeclassname`, configure the `desktop.features_permissions` option in your abcdesktop config file. `desktop.features_permissions` is a list of strings.


```
# features_permissions
# read executeclasses and permit a user to set a dedicated class name as desktop features
# 'read' features_permissions is exposed to the frontend
# 'submit' features_permissions can be set to create a desktop
# 
desktop.features_permissions : [ 'read', 'submit' ]
```

- To display the available execute classes on the login page, add `read` to the list.
- To allow users to select a class when creating a desktop, add `submit` to the list.


Enabling both options modifies the abcdesktop login page to display the `description` of each `executeclasses` entry, allowing users to make a selection before launching their desktop.

In this case `desktop.features_permissions : [ 'read', 'submit' ]`

![login resources](img/login-resources.png)

The user can choose an entry from the available `executeclasses` values.

![login resources sylver](img/login-resources-silver.png)

The `executeclassname` is set with the user's selected entry.

![login resources sylver](img/login-resources-silver.png)

The current user has selected `silver`.


> The pod is created with the requested resources.

![login pod sylver](img/login-rules-pod-silver.png)

- List the labels of the user's pod.

A label `executeclassname` is applied to the user's pod:

```
Labels:           abcdesktop/role=desktop
                  access_provider=planet
                  access_providertype=ldap
                  access_userid=fry
                  access_username=philip-j.-fry
                  executeclassname=silver
                  ...
```

The resource limits and requests are derived from the `silver` execute class.

```
Resources:
  Limits:
    cpu:     4
    memory:  32Gi
  Requests:
    cpu:     2
    memory:  2Gi
```
                 
The dialog box `settings`:`user information` displays the user's labels.

![login resources sylver](img/login-resource-userinfo-silver.png)

The current user has selected `silver`.

- Open a webshell to read the environment variables.

![login resources sylver](img/login-resources-silver-env.png)

Inside the pod, the environment variable `ABCDESKTOP_EXECUTE_CLASSNAME` is set to the value `silver`.

```
echo $ABCDESKTOP EXECUTE_CLASSNAME
silver
```

Inside the pod, the environment variable `ABCDESKTOP_EXECUTE_CLASS` is set to the selected JSON configuration object.

```
echo $ABCDESKTOP_EXECUTE_CLASS
{"nodeSelector": {}, "description": "silver: 4 CPU cores and 32Gi RAM", "runtimeClassName": null, "resources": {"requests": {"memory": "2Gi", "cpu": "2000m"}, "limits": {"memory": "32Gi", "cpu": "4000m"}}}
```


You can adjust pod resources either by defining authentication rules that automatically assign an execute class, or by configuring `desktop.features_permissions` to allow users to select from the profiles defined in `executeclasses`.







 

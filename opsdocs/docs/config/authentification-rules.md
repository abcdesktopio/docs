# Authentification rules configuration

All auth providers support rules configuration

A rule take some parameters and set label to the auth user.
All labels are stored inside the JWT Auth token.
The labels are use to define a container execution context.
For example to set a dedicated network for firefox application ( read the how-to ) 


## The rule object

A rule is a dictionary object with :

* a name (the entry of the rules)
* one or more conditions
* and expected boolean value True or False
* a label to set if the conditions are equal to the expected boolean value


Example :

To test if the user source IP address is equal to ```8.8.8.1/32```

```json 
'rule-home': { 
	'conditions' : [   { 'network': '8.8.8.1/32', 'expected' : True } ],
                         'expected' : True,
                         'label': 'homeipsource' }
```



                                    
### The conditions object

```conditions``` is a list of condition. All condition are always tested, as a logical ```AND```.
The result must be equal to the ```expected``` value.

####Examples:

####Example A:
To test if the user source IP address is in the subnet to ```80.0.0.0/8``` ```AND``` is ```memberOf``` ldap group DN 'cn=ship_crew,ou=people,dc=planetexpress,dc=com' 


```json 
 'rule-sample': { 'conditions':  [ 
 	{ 'network': '80.0.0.0/8', 'expected' : True },
 	{ 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',  'expected' : True } ], 
 	'expected' : True,
	'label': 'shipcrewandnet80'
}
```
Add the labels 'shipcrewandnet80', if the 'expected' value is ```True```

####Example B:
To test if the user source IP address is ```NOT``` in the subnet to ```80.0.0.0/8``` ```AND``` is  ```NOT``` a ```memberOf``` ldap group DN 'cn=ship_crew,ou=people,dc=planetexpress,dc=com' 


```json 
 'rule-sample': { 'conditions':  [ 
 	{ 'network': '80.0.0.0/8', 'expected' : True },
 	{ 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',  'expected' : True } ], 
 	'expected' : False,
	'label': 'noshipcrewandnet80'
}
```

Add the labels 'noshipcrewandnonet80', if the 'expected' value is ```False```



####Example C:
To test if the user source IP address is in the subnet to ```80.0.0.0/8``` ```AND``` is  ```NOT``` a ```memberOf``` ldap group DN 'cn=ship_crew,ou=people,dc=planetexpress,dc=com' 


```json 
 'rule-sample': { 'conditions':  [ 
 	{ 'network': '80.0.0.0/8', 'expected' : True },
 	{ 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',  'expected' : False } ], 
 	'expected' : True,
	'label': 'noshipcrewandnet80'
}
```

Add the labels 'noshipcrewandnet80', if the 'expected' value is ```True```



####Example D:
To test if the user source IP address is ```NOT``` in the subnet to ```80.0.0.0/8``` ```AND``` is   a ```memberOf``` ldap group DN 'cn=ship_crew,ou=people,dc=planetexpress,dc=com' 


```json 
 'rule-sample': { 'conditions':  [ 
 	{ 'network': '80.0.0.0/8', 'expected' : False },
 	{ 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',  'expected' : True } ], 
 	'expected' : True,
	'label': 'shipcrewandnonet80'
}
```

Add the labels 'shipcrewandnonet80', if the 'expected' value is ```True```



### The condition value


| name           | description                 | example          |
|----------------|-----------------------------|------------------|
| boolean        | always true or false        | 'boolean' : 'true' |
| httpheader     | test a HTTP header value    | 'httpheader': { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36' }  |
| memberOf       | test if the LDAP user object is member of group      | 'memberOf': [ 'cn=ship_crew,ou=people,dc=planetexpress,dc=com']  |
| network        | test if the client user IP Address is in a network subnet      | 'network': [ '1.2.3.4/24'] |
| primarygroupid | test if the LDAP user object has a attibute primaryGroupID and is equal to value    | 'primarygroupid': '513' |



#### condition boolean

This condition is a dummy condition; Only use to force a label or to disable a test.

```
'boolean': boolean
```

The commun usage is 

```json
'rule-dummy': { 'conditions':  [  { 'boolean': True, 'expected' : True  } ],
				   'expected' : True,
	             'label': 'dummy'
}
```

or alway False


```json
'rule-dummy': { 'conditions':  [  { 'boolean': True, 'expected' : True  } ],
				   'expected' : False,
	             'label': 'dummy'
}
```

 
#### condition httpheader 


This condition is test if a HTTP Header value is equal to a string. 

```
'httpheader': dict
```

example : if the 'User-Agent' is equal to 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36' then add the label 'chromemaxosx112'

```json 

 'rule-httpheader': { 
 		'conditions' : [ 
 			{ 	'httpheader': { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36' }, 
 				'expected' : True  } ],
 		'expected' : True,
 		'label': 'chromemaxosx112' }
 		
```


#### condition network

This condition is test if the client source ip address is in a subnet. IPv4 and IPv6 are supported.

```
'network': string
```


example

To test if the user source IP address is equal to ```8.8.8.1/32```

```json 
'rule-home': { 
	'conditions' : [   { 'network': '8.8.8.1/32', 'expected' : True } ],
                         'expected' : True,
                         'label': 'homeipsource' }
```

To test if the user source IP address is in the subnet ```10.0.0.0/8```

```json 
'rule-localnet': { 
	'conditions' : [   { 'network': '10.0.0.0/8', 'expected' : True } ],
                         'expected' : True,
                         'label': 'localnet' }
```


To test if the user source IP address is NOT in the subnet ```192.168.0.0/24```

```json 
'rule-localnet': { 
	'conditions' : [   { 'network': '192.168.0.0/24', 'expected' : False } ],
                         'expected' : True,
                         'label': 'no192168net' }
```

same as 

```json 
'rule-localnet': { 
	'conditions' : [   { 'network': '192.168.0.0/24', 'expected' : True } ],
                         'expected' : False,
                         'label': 'no192168net' }
```


#### condition memberof

This condition test if the user is a member of a LDAP Distinguished Name. 

```
'memberOf': string
```


```json 
 'rule-sample': { 'conditions':  [ 
  	{ 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',  'expected' : True } ], 
 	'expected' : True,
	'label': 'shipcrewgrp'
}
```



#### condition primarygroupid

This test is only used with Microsoft Active Directory.
primarygroupid test if the user attibute primaryGroupID is equal to a string.

```
'primarygroupid': string
```

To check is a user is memberof a ```DOMAIN\USER``` the primary group id is ```513```

```json 
'rule-domainuser': { 	'conditions':  [ { 'primarygroupid': '513', 'expected' : True } ],
 							'expected' : True,
 							'label': 'domainuser'
}
```

However, if the user needed to be seen as a ```Domain Admin for POSIX```, the ```PrimaryGroupID``` is ```512```, the RID for that group. 


```json 
'rule-posixdomainadmin': { 	'conditions':  [ { 'primarygroupid': '519', 'expected' : True } ],
 							'expected' : True,
 							'label': 'posixdomainadmin'
}
```

The ```Enterprise Admins group```, ```519```, is also used to grant this level in POSIX.

```json 
'rule-enterpriseadmin': { 	'conditions':  [ { 'primarygroupid': '519', 'expected' : True } ],
 							'expected' : True,
 							'label': 'enterpriseadmin'
}
```
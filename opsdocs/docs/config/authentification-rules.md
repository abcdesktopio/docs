# Authentification rules configuration

All auth providers support rules configuration

A rule take some parameters and set label to the auth user.
All labels are stored inside the JWT Auth token.
The labels are use to define a container execution context.
For example to set a dedicated network for firefox application ( read the how-to ) 


## The rule object

A rule is a dictionary object with :

* a name
* one or more conditions
* and expected boolean value True oo False
* a label to set if the conditions are equal to the expected boolean value


Example :

To test is the user source IP address is equal to ```8.8.8.1/32```

```json 
'rule-home': { 
	'conditions' : [   { 'network': '8.8.8.1/32', 'expected' : True } ],
                         'expected' : True,
                         'label': 'maisonalex' }
```

                                    
### The condition object

 
```json 

 'rule-httpheader': { 'conditions' : [ { 'httpheader': { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36
 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36' }, 'expected' : True  } ],
                                                              'expected' : True,
                                                              'label': 'dummyuseragent' },
```

## rules conditions

| condition      | description                 | example          |
|----------------|-----------------------------|------------------|
| boolean        | always true or false        | 'boolean' : 'true' |
| httpHeader     | test a HTTP header value    | 'httpheader': { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36' }  |
| memberOf       | test if the LDAP user object is member of group      | 'memberOf': [ 'cn=ship_crew,ou=people,dc=planetexpress,dc=com']  |
| network        | test if the client user IP Address is in a network subnet      | 'network': [ '1.2.3.4/24'] |
| primarygroupid | test if the LDAP user object has a attibute primaryGroupID and is equal to value    | 'primarygroupid': '513' |



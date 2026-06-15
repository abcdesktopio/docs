# Authentication Rules Configuration

All authentication providers support rules configuration.

A rule takes parameters and sets labels on the user's pod and on the user's JWT token.

- All labels are stored inside the JWT user token.
- All labels are applied to the user's pods.

Labels are used to define a container execution context for subsequent operations, such as:

- Allowing an application only to members of a specific group
- Applying network policies


## The Rule Object

A rule is a dictionary object with:

* A name (the key of the rule entry)
* One or more conditions
* An expected boolean result of `True` or `False`
* A label to apply when the conditions evaluate to the expected boolean value


**Example:**

To test whether the user's source IP address equals `192.168.2.3/32`:

```json 
'rule-home': { 
	'conditions' : [   { 'network': '192.168.2.3/32', 'expected' : True } ],
                         'expected' : True,
                         'label': 'allowipsource' }
```

If the source IP address equals `192.168.2.3`, the pod receives the label `allowipsource`.

                                    
### The Conditions Object

The `conditions` field is a list of individual condition objects. All conditions are always evaluated, functioning as a logical `AND` operator. The combined result must equal the `expected` value.

#### Examples

#### Example: (`True` AND `True`) expected `True`

To test whether the user's source IP address is in the subnet `80.0.0.0/8` **and** the user is a `memberOf` the LDAP group DN `cn=ship_crew,ou=people,dc=planetexpress,dc=com`:


```json 
 'rule-sample': {
  'conditions':  [ 
 	{ 'network': '80.0.0.0/8', 'expected' : True },
 	{ 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',  'expected' : True }
  ], 
  'expected' : True,
  'label': 'shipcrewandnet80' }
```

This rule applies the label `shipcrewandnet80` when the `expected` value is `True`.

#### Example: (`True` AND `True`) expected `False`

To test whether the user's source IP address is **NOT** in the subnet `80.0.0.0/8` **AND** the user is **NOT** a `memberOf` the LDAP group DN `cn=ship_crew,ou=people,dc=planetexpress,dc=com`:


```json 
 'rule-sample': {
   'conditions':  [ 
      { 'network': '80.0.0.0/8', 'expected' : True },
 	  { 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',  'expected' : True }
   ], 
   'expected' : False,
   'label': 'noshipcrewandnet80' }
```

Applies the label `noshipcrewandnonet80` when the `expected` value is `False`.


#### Example: (`True` AND `False`) expected `True`

To test whether the user's source IP address is in the subnet `80.0.0.0/8` **AND** the user is **NOT** a `memberOf` the LDAP group DN `cn=ship_crew,ou=people,dc=planetexpress,dc=com`:


```json 
'rule-sample': {
   'conditions':  [ 
 	 { 'network': '80.0.0.0/8', 'expected' : True },
 	 { 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',  'expected' : False }
   ], 
   'expected' : True,
   'label': 'noshipcrewandnet80' }
```

Applies the label `noshipcrewandnet80` when the `expected` value is `True`.


#### Example: (`False` AND `True`) expected `True`

To test whether the user's source IP address is **NOT** in the subnet `80.0.0.0/8` **AND** the user is a `memberOf` the LDAP group DN `cn=ship_crew,ou=people,dc=planetexpress,dc=com`:


```json 
'rule-sample': {
  'conditions':  [ 
 	{ 'network': '80.0.0.0/8', 'expected' : False },
 	{ 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',  'expected' : True }
  ], 
  'expected' : True,
  'label': 'shipcrewandnonet80' }
```

Applies the label `shipcrewandnonet80` when the `expected` value is `True`.




### Condition Value Reference


| Name              | Description                 | Example          |
|-------------------|-----------------------------|------------------|
| `boolean`         | Always evaluates to true or false | `'boolean' : 'true'` |
| `existhttpheader` | Tests whether an HTTP header exists | |
| `httpheader`      | Tests whether an HTTP header value equals a given string | `'httpheader': { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36' }`  |
|  `memberOf`       | Tests whether the LDAP user object is a member of a group | `'memberOf': [ 'cn=ship_crew,ou=people,dc=planetexpress,dc=com']`  |
| `network`         | Tests whether the client IP address falls within a network subnet | `'network': [ '1.2.3.4/24']` |
| `network-x-forwarded-for` | Reads the `X-Forwarded-For` HTTP attribute, then tests whether the value falls within a network subnet | |
| `network-x-real-ip` | Reads the `X-Real-IP` HTTP attribute, then tests whether the value falls within a network subnet | |
| `attribut`        | Tests whether an HTTP header value equals a given string | `'httpheader': { 'User-Agent': 'Mozilla/5.0`
| `primarygroupid`  | Tests whether the LDAP user object has a `primaryGroupID` attribute equal to a specified value | `'primarygroupid': '513'` |
| `asnumber`        | Tests whether the source IP address belongs to a given BGP AS number | `'asnumber': [ '3215', '12807']` |
| `geolocation`     | Tests whether the user is geolocated in a specific region. Geolocation data comes from the web browser and can be spoofed | `'geolocation': {'accuracy': 14.884, 'latitude': 48.8555131, 'longitude': 2.3752174 }` |


#### Condition: `boolean`

This is a trivial condition used to unconditionally force a label or to disable a test entirely.

```
'boolean': boolean
```

A common usage pattern is to always evaluate to `True`:

```json
'rule-dummy': {
  'conditions':  [  { 'boolean': True, 'expected' : True  } ],
  'expected' : True,
  'label': 'dummy' }
```

Or to always evaluate to `False`:


```json
'rule-dummy': {
   'conditions':  [  { 'boolean': True, 'expected' : True  } ],
   'expected': False,
   'label': 'dummy' }
```

 
#### Condition: `httpheader`

This condition tests whether an HTTP header value equals a specific string.

```
'httpheader': dict
```

Example: if the `User-Agent` header equals `Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36`, apply the label `chromemaxosx112`:

```json
'rule-httpheader': { 
  'conditions' : [ { 'httpheader': { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36' }, 'expected' : True  } ],
  'expected' : True,
  'label': 'chromemaxosx112' }
```


#### Condition: `network`

This condition tests whether the client's source IP address falls within a given subnet. Both IPv4 and IPv6 are supported.

```
'network': string or list of string, each string must be a subnet ipv4 or ipv6
```

To determine the source IP address, the service reads the following headers in order:

- `X-Forwarded-For` HTTP header
- `X-Real-IP` HTTP header
- `remoteip` — the raw socket IP source

**Examples:**

To test whether the user's source IP address equals `8.8.8.1/32`:

```json 
'rule-home': { 
	'conditions': [   { 'network': '8.8.8.1/32', 'expected' : True } ],
    'expected': True,
    'label': 'homeipsource' }
```

To test whether the user's source IP address is in the subnet `10.0.0.0/8`:

```json 
'rule-localnet': { 
	'conditions': [ { 'network': '10.0.0.0/8', 'expected' : True } ],
    'expected': True,
    'label': 'localnet' }
```


To test whether the user's source IP address is NOT in the subnet `192.168.0.0/24`:

```json 
'rule-localnet': { 
  'conditions': [ { 'network': '192.168.0.0/24', 'expected' : False } ],
  'expected': True,
  'label': 'no192168net' }
```

Which is equivalent to:

```json 
'rule-localnet': { 
	'conditions' : [   { 'network': [ '192.168.0.0/24'] , 'expected' : True } ],
    'expected' : False,
    'label': 'no192168net' }
```


##### IPv4 and IPv6 Subnet Support

To cover private IP address ranges defined in [RFC 1918](https://tools.ietf.org/html/rfc1918) and [RFC 3927](https://tools.ietf.org/html/rfc3927), define separate rules for each subnet. Both IPv4 and IPv6 addresses are supported. Multiple rules can assign the same label, such as `privatenetwork`.

```json
'policies': {
	'acl' : {},
	'rules'	: { 
		  'rule-privatenetwork-10': { 	'conditions': [ { 'network': '10.0.0.0/8', 'expected' : True } ], 
		  								'expected': True, 
		  								'label': 'privatenetwork' },
		  'rule-privatenetwork-172': {	'conditions': [ { 'network': '172.16.0.0/12', 'expected' : True } ], 
		  								'expected': True, 
		  								'label': 'privatenetwork' },
		  'rule-privatenetwork-192': {	'conditions': [ { 'network': '192.168.0.0/16',     'expected' : True } ], 
		  								'expected': True, 
		  								'label': 'privatenetwork' },
		  'rule-privatenetwork-169': {	'conditions': [ { 'network': '169.254.0.0/16',     'expected' : True } ], 
		  								'expected': True, 
		  								'label': 'privatenetwork' },
		  'rule-privatenetwork-fe80':{	'conditions': [ { 'network': 'fe80::/10',     'expected' : True } ], 
		  								'expected': True, 
		  								'label': 'privatenetwork' } } }
```

> Multiple rules can set the same label.

The above rules can be simplified into a single rule using a list of subnets:

```json
'policies': {
  'acl' : {},
    'rules'	: { 
      'rule-privatenetwork': {
        'conditions': [ { 'network': [ '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', '169.254.0.0/16', 'fe80::/10' ], 'expected' : True } ],
        'expected': True, 
		'label': 'privatenetwork' } } }
```

 	
#### Condition: `memberof`

This condition tests whether the user is a member of an LDAP Distinguished Name.

```json
'memberOf': string
```

```json 
'rule-sample': {
  'conditions':  [ { 'memberOf': 'cn=ship_crew,ou=people,dc=planetexpress,dc=com',  'expected' : True } ], 
  'expected' : True,
  'label': 'shipcrewgrp'
}
```



#### Condition: `primarygroupid`

This condition is used exclusively with Microsoft Active Directory. It tests whether the user's `primaryGroupID` attribute equals a specified string value.

```json
'primarygroupid': string
```

To verify that a user is a member of the `DOMAIN\Domain Users` group, the primary group ID is `513`:

```json 
'rule-domainuser': {
  'conditions':  [ { 'primarygroupid': '513', 'expected' : True } ],
  'expected' : True,
  'label': 'domainuser'
}
```

If the user must be identified as a `Domain Admin for POSIX`, the `PrimaryGroupID` is `512`, which is the RID for that group:


```json 
'rule-posixdomainadmin': {
  'conditions':  [ { 'primarygroupid': '512', 'expected' : True } ],
  'expected' : True,
  'label': 'posixdomainadmin'
}
```

The `Enterprise Admins` group uses the ID `519` and is also used to grant this level of access in POSIX environments:

```json 
'rule-enterpriseadmin': {
  'conditions': [ { 'primarygroupid': '519', 'expected' : True } ],
  'expected': True,
  'label': 'enterpriseadmin'
}
```

#### Condition: `asnumber`

BGP public AS numbers are globally unique identifiers assigned by IANA for Internet routing, ranging from 1 to 64495 (16-bit) and extended to 32-bit for greater availability. Public AS numbers must be unique on the Internet, and BGP uses the AS number as its loop-prevention mechanism.

```
'rule-asnumber' : {
  'conditions' : [ {'asnumber': [ '3215' ] , 'expected':True } ],
  'expected' : True,
  'label':'orangenetwork'
}
```

If the source IP address belongs to AS number `3215`, the label `orangenetwork` is applied. You can build filters for your own AS number to allow or deny access.

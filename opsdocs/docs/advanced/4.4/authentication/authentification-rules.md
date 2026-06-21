---
title: Authentication Rules & Labels Configuration | abcdesktop.io
description: Configure rule-based authentication in abcdesktop.io: define conditions on HTTP headers, LDAP attributes, network CIDR ranges, and geolocation to apply labels to user JWT tokens.
keywords: authentication rules, labels, JWT, LDAP, HTTP header, CIDR, geolocation, access control, abcdesktop, Kubernetes, security
tags:
  - authentication
  - security
  - rules
---

# Authentication Rules Configuration

All authentication providers support rule-based configuration. Rules evaluate one or more conditions against request attributes and, when the conditions produce the expected boolean result, apply a label to the user's pod and JWT token.

- All labels are stored inside the JWT user token.
- All labels are applied to the user's pods.

Labels define the container execution context used for subsequent operations, including:

- Restricting an application to members of a specific group
- Enforcing network policies


## The Rule Object

A rule is a dictionary object that consists of:

* A name (the dictionary key of the rule entry)
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

The `conditions` field is a list of individual condition objects. All conditions are evaluated unconditionally and combined using a logical `AND` operation. The aggregated result must equal the rule's `expected` value for the associated label to be applied.

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
| `boolean`         | Always evaluates to `True` or `False` regardless of request attributes | `'boolean' : 'true'` |
| `existhttpheader` | Tests whether a specified HTTP header is present in the request | |
| `httpheader`      | Tests whether an HTTP header value equals a given string | `'httpheader': { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36' }`  |
|  `memberOf`       | Tests whether the authenticated LDAP user object is a member of a specified group | `'memberOf': [ 'cn=ship_crew,ou=people,dc=planetexpress,dc=com']`  |
| `network`         | Tests whether the client IP address falls within a specified network subnet | `'network': [ '1.2.3.4/24']` |
| `network-x-forwarded-for` | Reads the `X-Forwarded-For` HTTP header value and tests whether it falls within a specified network subnet | |
| `network-x-real-ip` | Reads the `X-Real-IP` HTTP header value and tests whether it falls within a specified network subnet | |
| `attribut`        | Tests whether an LDAP user attribute value equals a given string | `'httpheader': { 'User-Agent': 'Mozilla/5.0`
| `primarygroupid`  | Tests whether the LDAP user object has a `primaryGroupID` attribute equal to a specified value | `'primarygroupid': '513'` |
| `asnumber`        | Tests whether the source IP address belongs to a given BGP AS number | `'asnumber': [ '3215', '12807']` |
| `geolocation`     | Tests whether the user is geolocated in a specific region. Geolocation data is provided by the web browser and may be spoofed | `'geolocation': {'accuracy': 14.884, 'latitude': 48.8555131, 'longitude': 2.3752174 }` |


#### Condition: `boolean`

This condition unconditionally forces a label or disables a test entirely, regardless of any request attributes.

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

BGP public AS numbers are globally unique identifiers assigned by IANA for Internet routing. 16-bit AS numbers range from 1 to 64495, while 32-bit AS numbers extend this space for greater availability. BGP uses the AS number as its primary loop-prevention mechanism, and all public AS numbers must be globally unique on the Internet.

```
'rule-asnumber' : {
  'conditions' : [ {'asnumber': [ '3215' ] , 'expected':True } ],
  'expected' : True,
  'label':'orangenetwork'
}
```

If the source IP address belongs to AS number `3215`, the label `orangenetwork` is applied. You can build filters based on your own AS number to selectively allow or deny access.

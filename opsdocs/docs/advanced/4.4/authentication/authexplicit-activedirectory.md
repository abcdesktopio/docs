---
title: Explicit Authentication with Active Directory | abcdesktop.io
description: Configure abcdesktop.io explicit authentication against Microsoft Active Directory: LDAP bind, UPN, service account credentials, and subnet discovery via AD Sites and Services.
keywords: Active Directory, LDAP, explicit authentication, AD, Windows domain, UPN, service account, abcdesktop, Kubernetes
tags:
  - authentication
  - Active Directory
  - LDAP
---

# Authentication `explicit` for Microsoft Active Directory Services


## authmanagers `explicit` Object

The `explicit` authentication configuration is defined as a dictionary object that contains one or more named provider entries, each corresponding to a Windows domain.


For example:

```
'explicit': {
    'show_domains': True,
    'default_domain': 'AD',
    'providers': {
      'AD': { 
        'config_ref': 'adconfig', 
        'enabled': True
       }
}
```


| Variable name      | Type   | Description   |
|--------------------|--------- |-------------|
|  `show_domains`   | boolean   | Controls whether the domain name is listed in the API `getclientdata` response. The default value is `False`. |
|  `default_domain` | string | The default domain name prefix applied when the user's login format does not include a domain prefix (e.g., `DOMAIN\USER`). If the user logs in as `USER`, the login is prefixed as `default_domain\USER`. | 
|  `providers`      | dictionary | `{ 'AD': {  'config_ref': 'adconfig',  'enabled': True  }}`
|



### Providers Configuration

The `provider` authentication configuration is defined as a dictionary object that must include a key name. The key name must match the [`USERDOMAIN`](https://en.wikipedia.org/wiki/Windows_domain) value and must correspond exactly to the key used in the `config_ref` dictionary.



Providers:

The provider is formatted as a dictionary:

 ```
 { 'AD': {  
 			'config_ref': 'adconfig',  
 			'enabled': True  
 		}
 }
 ```
 
| Variable name      | Type   | Description   |
|--------------------|--------- |-------------|
| config_ref         | string   | For increased readability, the `USERDOMAIN` configuration is defined in a dedicated dictionary using the key-value pair `'config_ref': 'adconfig'`, where the key is `config_ref` and the value is the name of the dictionary variable. |
| enable             | boolean  | Enables or disables the domain entry. |


In this example, the Microsoft Active Directory environment variables are configured as follows:

| Variable name        | Value for example                                    |
|----------------------|------------------------------------------------------|
|  ```USERDOMAIN ```   | ```AD```                                             |
|  ```USERDNSDOMAIN ```| ```AD.DOMAIN.LOCAL```                                |



The `adconfig` is a dictionary. For example:

```
adconfig : { 
  'AD': {   
  	   'default': True,
       'reduce_roles_for_jwt': 'cn',
       'ldap_timeout': 5,
       'ldap_connect_timeout': 2,
       'ldap_basedn': 'DC=ad,DC=domain,DC=local',
       'ldap_fqdn': '_ldap._tcp.ad.domain.local',
       'domain': 'AD',
       'domain_fqdn': 'AD.DOMAIN.LOCAL',
       'kerberos_realm': 'AD.DOMAIN.LOCAL',
       'auth_type': 'NTLM',
       'krb5_conf': '/etc/krb5.conf',
       'users_ou': 'DC=ad,DC=domain,DC=local',
       'auth_protocol' : { 'ntlm': False, 'cntlm': False, 'kerberos' : True, 'ldif': False },
       'servers': [ 'ldaps://srv1.domain.local', 'ldaps://srv2.domain.local','ldaps://srv3.domain.local' ]
       # 'serviceaccount': { 'login': 'SVCACCOUNT', 'password': 'SVCACCOUNTPASSWORD' } 
} }

```


Replace each variable value with settings specific to your Active Directory environment.


| Variable name        | Type		       | Description                        | Example  |
|----------------------|----------------|------------------------------------|----------|
|  `default`       | boolean        | Use this domain as the default domain  | True     |
|  `ldap_basedn`   | string         | LDAP Base Distinguished Name       | `DC=ad,DC=domain,DC=local` |
|  `ldap_fqdn`     | string         | LDAP SRV record for the domain     | `_ldap._tcp.ad.domain.local` |
|  `domain_fqdn`   | string         | Domain fully qualified domain name (FQDN) | `AD.DOMAIN.LOCAL` |
|  `servers`       | list of string | List of Active Directory server addresses | `[ '192.168.1.12', '192.168.1.13' ]` |
|  `kerberos_realm`| string         | Kerberos realm name (must be in UPPER CASE) | `AD.DOMAIN.LOCAL` |
| `reduce_roles_for_jwt`| string or None | Defines the role representation in the user's JWT | `'cn'`, `'raw'` or `None` |
| `servers `| list | List of LDAP server URIs  | `[ 'ldaps://srv1.domain.local', 'ldap://192.168.1.2'] ` |



## Service Account


```
  'serviceaccount': { 'login': 'SVCACCOUNT', 'password': 'SVCACCOUNTPASSWORD' }
```

`serviceaccount` is an optional credential configuration. When provided, it allows `pyos` to query the Active Directory service and retrieve subnet and site location information from the sites container at `'CN=Subnets,CN=Sites,CN=Configuration,' + BASE_DN` (for example, `CN=Subnets,CN=Sites,CN=Configuration,DC=example,DC=com`).

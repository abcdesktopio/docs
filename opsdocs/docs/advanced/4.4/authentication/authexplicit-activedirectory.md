
# Authentification `explicit` for Microsoft Active Directory services


## authmanagers `explicit` object

The `explicit` authentification configuration is defined as a dictionnary object and contains an `explicit` provider. 


For example :

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
|  `show_domains`   | boolean   | Permit the domain name to be listed in API getclientdata, the default value is False |
|  `default_domain` | string | Default domain name prefix if the user format does not containthe domain prefix like DOMAIN\USER. If the user login value is USER, the login is prefixed with the  default_domain\USER | 
|  `providers`      | dictionnary | `{ 'AD': {  'config_ref': 'adconfig',  'enabled': True  }}`
|



### providers configuration

The `provider` authentification configuration is defined as a dictionnary object and must contain a key name.
The key name must be set as the [`USERDOMAIN`](https://en.wikipedia.org/wiki/Windows_domain) and defined in the `config_ref` with the exact same value.



Providers :

The provider is formated as a dictionnary 

 ```
 { 'AD': {  
 			'config_ref': 'adconfig',  
 			'enabled': True  
 		}
 }
 ```
 
| Variable name      | Type   | Description   |
|--------------------|--------- |-------------|
| config_ref         | string   |  For increased legibility, the `USERDOMAIN` configuration is defined in a dedicated dictionnary used the key:value `'config_ref': 'adconfig'`, where `key` is `config_ref` and `value` is the dictionnay variable name.           |
| enable             | boolean  | enable or disable the domain entry            |


If this example, the Microsoft Active Directory value are set to :

| Variable name        | Value for example                                    |
|----------------------|------------------------------------------------------|
|  ```USERDOMAIN ```   | ```AD```                                             |
|  ```USERDNSDOMAIN ```| ```AD.DOMAIN.LOCAL```                                |



The adconfig is a dictionnary. For example :

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


For Active Directory authmanagers, replace the variable name with your own value.


| Variable name        | Type		       | Description                        | Example  |
|----------------------|----------------|------------------------------------|----------|
|  `default`       | boolean        | Use this domain as default domain  | True     |
|  `ldap_basedn`   | string         | LDAP Base Distinguished Names      | `DC=ad,DC=domain,DC=local` |
|  `ldap_fqdn`     | string         | _ldap._tcp.Domain_Name             | `_ldap._tcp.ad.domain.local` |
|  `domain_fqdn`   | string         | domain FQDN (also know as Domain_Name)    | `AD.DOMAIN.LOCAL` |
|  `servers`       | list of string | list of the Active Director servers       | `[ '192.168.1.12', '192.168.1.13' ]` |
|  `kerberos_realm`| string         | Replace kerberos_realm wih your kerberos realm (in UPPER CASE) | `AD.DOMAIN.LOCAL` |
| `reduce_roles_for_jwt`| string or None | define the role in user's JWT | `'cn'`, `'raw'` or `None` |
| `servers `| list | list of servers  | `[ 'ldaps://srv1.domain.local', 'ldap://192.168.1.2'] ` |



## Service Account


```
  'serviceaccount': { 'login': 'SVCACCOUNT', 'password': 'SVCACCOUNTPASSWORD' }
```

`serviceaccount`is optionnal, it allow ro run query to the Active Directory service to read the subnet and location from the sites in `'CN=Subnets,CN=Sites,CN=Configuration,' + BASE_DN` , (for example CN=Subnets,CN=Sites,CN=Configuration,DC=example,DC=com)


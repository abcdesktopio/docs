
# Authentification ```explicit``` for Microsoft Active Directory services


## authmanagers ```explicit``` object

The ```explicit``` authentification configuration is defined as a dictionnary object and contains an ```explicit``` provider. 


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
|  ```show_domains```   | boolean   | Permit the domain name to be listed in API getclientdata, the default value is False |
|  ```default_domain``` | string | Default domain name prefix if the user format does not containthe domain prefix like DOMAIN\USER. If the user login value is USER, the login is prefixed with the  default_domain\USER | 
|  ```providers```      | dictionnary | ```{ 'AD': {  'config_ref': 'adconfig',  'enabled': True  }}```
|



### providers configuration

The ```provider``` authentification configuration is defined as a dictionnary object and must contain a key name.
The key name must be set as the [```USERDOMAIN```](https://en.wikipedia.org/wiki/Windows_domain) and defined in the ```config_ref``` with the exact same value.



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
| config_ref         | string   |  For increased legibility, the ```USERDOMAIN``` configuration is defined in a dedicated dictionnary used the key:value ```'config_ref': 'adconfig'```, where ```key``` is ```config_ref``` and ```value``` is the dictionnay variable name.           |
| enable             | boolean  | enable or disable the domain entry            |


The adconfig is a dictionnary. For example :

```
adconfig : { 'AD': {   'default'       : True, 
                       'ldap_timeout'  : 15,
                       'ldap_protocol' : 'ldap',
                       'ldap_basedn'   : 'DC=ad,DC=domain,DC=local',
                       'ldap_fqdn'     : '_ldap._tcp.ad.domain.local',
                       'domain'        : 'AD',
                       'domain_fqdn': 'AD.DOMAIN.LOCAL',
                       'servers'	: [ '192.168.7.12' ],
          				'kerberos_realm': 'AD.DOMAIN.LOCAL',
          				'query_dcs'	: True,
          				'wins_servers'  : [ '192.168.1.12' ],
          				'serviceaccount': { 'login': 'SVCACCOUNT', 'password': 'SVCACCOUNTPASSWORD' }
     }
}
```

If this example, the Microsoft Active Directory value are set to :

| Variable name        | Value for example                                    |
|----------------------|------------------------------------------------------|
|  ```USERDOMAIN ```   | ```AD```                                             |
|  ```USERDNSDOMAIN ```| ```AD.DOMAIN.LOCAL```                                |



For Active Directory authmanagers, replace the variable name with your own value.


| Variable name        | Type		       | Description                        | Example  |
|----------------------|----------------|------------------------------------|----------|
|  ```default```       | boolean        | Use this domain as default domain  | True     |
|  ```ldap_basedn```   | string         | LDAP Base Distinguished Names      | ```DC=ad,DC=domain,DC=local``` |
|  ```ldap_fqdn```     | string         | _ldap._tcp.Domain_Name             | ```_ldap._tcp.ad.domain.local``` |
|  ```domain_fqdn```   | string         | domain FQDN (also know as Domain_Name)    | ```AD.DOMAIN.LOCAL``` |
|  ```servers```       | list of string | list of the Active Director servers       | ```[ '192.168.1.12', '192.168.1.13' ]``` |
|  ```kerberos_realm```| string         | Replace kerberos_realm wih your kerberos realm (in UPPER CASE) | ```AD.DOMAIN.LOCAL``` |







The ```explicit``` authentification is support ```LDAP``` and ```LDAPS``` bind.


The Microsoft Active Directory value are set to :

| Variable name      | Value                                           |
|--------------------|------------------------------------------------------|
|  ```USERDOMAIN ```   | ```AD```  |
|  ```USERDNSDOMAIN ```| ```AD.DOMAIN.LOCAL``` |


For Active Directory authmanagers, replace the variable name with your own value.


| Variable name      | Description | Example |
|--------------------|-------------|------|
|  ```ldap_basedn``` | Replace ldap_basedn with your LDAP Base Distinguished Names  | ```DC=ad,DC=domain,DC=local``` |
|  ```ldap_fqdn```   | Replace ldap_fqdn with the _ldap._tcp fqdn  | ```_ldap._tcp.ad.domain.local``` |
|  ```domain_fqdn``` | Replace domain_fqdn with domain FQDN value | ```AD.DOMAIN.LOCAL``` |
|  ```servers```     | Replace servers with list of the Active Director servers | ```[ '192.168.1.12', '192.168.1.13' ]``` |
|  ```kerberos_realm```| Replace kerberos_realm wih your kerberos realm (in UPPER CASE) | ```AD.DOMAIN.LOCAL``` |

## Service Account

The service account is use when od.py starts. It runs query to the Active Directory service to read the subnet and location from the sites in 'CN=Subnets,CN=Sites,CN=Configuration,' + BASE_DN , (for example CN=Subnets,CN=Sites,CN=Configuration,DC=example,DC=com)


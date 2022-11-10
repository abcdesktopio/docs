
# Authentification `metaexplicit` for Microsoft Active Directory services with trust relationships 

## authmanagers `metaexplicit` object

The `metaexplicit` authentification manager contains only one provider.
The provider must be defined as `metadirectory`.

``` json
'metaexplicit': {
    'providers': {
      'metadirectory': { 
        'config_ref': 'coporateconfig', 
        'enabled': True
       }
}
```

| Variable name      | Type        | Description   |
|--------------------|------------ |-------------|
|  `providers`   | dictionary | `{ 'metadirectory': {  'config_ref': 'coporateconfig',  'enabled': True  }}` |

### `metadirectory` provider configuration

The `metadirectory` provider is defined as a dictionnary object and must contain key name.
The key name must be set as the name of a dictionaryin the `config_ref`.

A `metadirectory` provider must contain a ldap attribut to describe the original DOMAIN and sAMaccountName.
The ldap attribut is defined as `join_key_ldapattribut`.

```
coporateconfig : { 'metadirectory': {  
                    'domain'        : 'CORPORATE',
                    'ldap_basedn'   : 'DC=foo,DC=corporate,DC=local',
                    'ldap_fqdn'     : '_ldap._tcp.foo.corporate.local',
                    'servers'       : [ 'ldap://192.168.9.11', 'ldap://192.168.7.12', 'ldap://192.168.7.13' ],
                    # join_key_ldapattribut must be defined for a metadirectory provider
                    'join_key_ldapattribut' : 'description',
                    'auth_type'  : 'KERBEROS',
                    'domain_fqdn': 'foo.corporate.local',
                    'kerberos_realm': 'FOO.CORPORATE.LOCAL',
                    # serviceaccount must be defined for a metadirectory provider
                    'serviceaccount': { 'login': 'svcaccount', 'password':'superpass' }
                 } } 
```

Pyos binds the metadirectory ldap server with serviceaccount credentials
Pyos read the ldap attribut `description` value to get the user's trusted domain.

For example :
``` ldif
description: AD\john
```

Then pyos look for provider `AD` configuration and process authentification on domain `AD`

The `metadirectory` accounts can be disabled. 
The ldap attribut `userAccountControl` is not read on metaDirectory provider. The account can have the bit `UF_ACCOUNT_DISABLE` set or not.

A service account must defined for a `metadirectory` provider. The service account is used to bind the metadirectory.

### Complete example with a `metadirectory` provider and active directory user domain

The user's domain mane is AD.
The meta domain name is CORPORATE.
The meta domain use a dedicated attribut `join_key_ldapattribut`

``` json
authmanagers: {
  #
  # define the meta explicit manager
  # This is the trusted external forest for the followed domain
  #
  'metaexplicit': {
    'providers': {
      # define the metadirectory provider
      # only one metadirectory provider is supported 
      'metadirectory': { 
        'config_ref': 'coporateconfig', 
        'enabled': True } 
    }
  },

  #        
  # define the Active Directory provider for each DOMAIN
  # define two domains in two disctinct forest with a trust relationship 
  # 
  'explicit': { 
    # define an Active Directory provider AD 
    'AD': {  'config_ref': 'adconfig', 'enabled': True },
    # define an Active Directory provider ANOTHER
    'ANOTHER': { 'config_ref': 'anotherconfig', 'enabled': True }  
  }
} # end of authmanagers

# In this example ldap attribut's description contains AD\myuser or ANOTHER\myuser 
coporateconfig : { 'metadirectory': {  
                    'domain'        : 'CORPORATE',
                    'ldap_basedn'   : 'DC=foo,DC=corporate,DC=local',
                    'ldap_fqdn'     : '_ldap._tcp.foo.corporate.local',
                    'servers'       : [ 'ldap://192.168.9.11', 'ldap://192.168.7.12', 'ldap://192.168.7.13' ],
                    # join_key_ldapattribut must be defined for a metadirectory provider
                    'join_key_ldapattribut' : 'description',
                    'auth_type'  : 'KERBEROS',
                    'domain_fqdn': 'foo.corporate.local',
                    'kerberos_realm': 'FOO.CORPORATE.LOCAL',
                    # serviceaccount must be defined for a metadirectory provider
                    'serviceaccount': { 'login': 'svcaccount', 'password':'superpass' }
                 } }


# 
# define the first DOMAIN AD
# The adconfig ref for domain AD
#
adconfig : { 'AD': {  'ldap_basedn'   : 'DC=ad,DC=domain,DC=local',
                      'ldap_fqdn'     : '_ldap._tcp.ad.domain.local',
                      'domain'        : 'AD',
                      'auth_type'     : 'NTLM',
                      'domain_fqdn'   : 'AD.DOMAIN.LOCAL',
                      'servers'       : [ 'ldap://192.168.7.12' ] } }

#
# define the second DOMAIN ANOTHER
# The anotherconfig ref for domain ANOTHER
#
anotherconfig : { 'ANOTHER': {
                      'ldap_basedn'   : 'DC=another,DC=super,DC=local',
                      'ldap_fqdn'     : '_ldap._tcp.another.super.local',
                      'domain'        : 'ANOTHER',
                      'auth_type'     : 'KERBEROS',
                      'domain_fqdn'   : 'ANOTHER.SUPER.LOCAL',
                      'servers'       : [ 'ldap://192.168.10.12' ],
                      'kerberos_realm': 'AD.SUPER.LOCAL' } }
```

### `metadirectory`support

`metadirectory` support the foreign security principal (FSP) to query security principal in the trusted external forest. These objects are created in the foreign security principals container of the domain.
`metadirectory` support `isMemberOf` on foreign security principal. 

The user's `SID` of domain  'AD' or 'ANOTHER' is NOT read.
A new ldap bind is done using the trusted domain on metadirectory provider and not unsing the service account.

The ldap query is build :
( "search_base={q.basedn}, search_scope={q.scope}, search_filter={filter}" )

To get more information about foreign security principal (FSP), read :

- [Foreign Security Principals Container](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/5aa09c90-c5db-4e97-98d0-b7cdd6bc1bfe)

- [Active Directory: Foreign Security Principals and Special Identities](https://social.technet.microsoft.com/wiki/contents/articles/51367.active-directory-foreign-security-principals-and-special-identities.aspx)


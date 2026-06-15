# Authentication `metaexplicit` for Microsoft Active Directory with Trust Relationships

## authmanagers `metaexplicit` Object

The `metaexplicit` authentication manager contains exactly one provider.
The provider must be defined with the name `metadirectory`.

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

### `metadirectory` Provider Configuration

The `metadirectory` provider is defined as a dictionary object and must contain a key name.
The key name must match the name of the dictionary referenced by `config_ref`.

A `metadirectory` provider requires an LDAP attribute to identify the original domain and `sAMAccountName`.
This LDAP attribute is specified using `join_key_ldapattribut`.

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

Pyos binds to the metadirectory LDAP server using the service account credentials, then reads the LDAP attribute `description` to determine the user's trusted domain.

For example:
``` ldif
description: AD\john
```

Pyos then looks up the `AD` provider configuration and performs authentication against the `AD` domain.

Accounts in the `metadirectory` can be in any state.
The LDAP attribute `userAccountControl` is not read for metadirectory providers. The `UF_ACCOUNT_DISABLE` bit is not evaluated.

A service account must be defined for every `metadirectory` provider. The service account is used to bind to the metadirectory.

### Complete Example with a `metadirectory` Provider and Active Directory User Domains

In this example:
- The user's domain name is `AD`.
- The meta domain name is `CORPORATE`.
- The meta domain uses a dedicated attribute specified by `join_key_ldapattribut`.

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

### `metadirectory` Support

The `metadirectory` provider supports Foreign Security Principals (FSPs) to query security principals in trusted external forests. These objects are created in the Foreign Security Principals container of the domain.
The `metadirectory` provider supports `isMemberOf` lookups on foreign security principals.

The user's SID from the `AD` or `ANOTHER` domain is NOT read directly.
A new LDAP bind is performed against the trusted domain on the metadirectory provider rather than using the service account.

The LDAP query is constructed as:
```
( "search_base={q.basedn}, search_scope={q.scope}, search_filter={filter}" )
```

For more information about Foreign Security Principals, refer to:

- [Foreign Security Principals Container](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/5aa09c90-c5db-4e97-98d0-b7cdd6bc1bfe)

- [Active Directory: Foreign Security Principals and Special Identities](https://social.technet.microsoft.com/wiki/contents/articles/51367.active-directory-foreign-security-principals-and-special-identities.aspx)

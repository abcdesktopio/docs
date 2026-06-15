# Authentication Overview

## Configuration File

The authentication configuration is set in the `od.config` file. This chapter requires you to update the `od.config` configuration file.
The update procedure differs depending on whether you are running in Docker mode or Kubernetes mode.

Read the
[Update your configuration file and apply the new configuration file](../configure/updateconfiguration.md) section to learn how to apply changes to the `od.config` file in a Kubernetes cluster.

## The authmanagers Dictionary

The `authmanagers` object is defined as a dictionary:

```
authmanagers: {
  'external': {},
  'explicit': {},
  'implicit': {}}
```

The `od.config` file defines four types of entries in the `authmanagers` object:

* `external`: Used for OpenID Connect (OAuth 2.0) authentication
* `explicit`: Used for directory service authentication with `LDAP`, `LDAPS`, and `Microsoft Active Directory`
* `metaexplicit`: Used for `Microsoft Active Directory` trusted relationships, with support for FSP (Foreign Security Principals)
* `implicit`: Used for anonymous authentication and SSL client certificate authentication

## Related authmanagers

| authmanagers type  | Description  |
|--------------------|--------------|
|  [`external`](authexternal.md)| For OpenID Connect OAuth 2.0 authentication |
|  [`metaexplicit`](authexplicit.md) | For Microsoft Active Directory trusted relationships, with support for Foreign Security Principals and Special Identities |
|  [`explicit`](authexplicit.md) | For LDAP, LDAPS, Active Directory, and Kerberos authentication |
|  [`implicit`](authimplicit.md) | For anonymous authentication, always-allow authentication, and SSL client certificate authentication |

## Hands-on

### Requirements

You should have read:

* [Update your configuration file and apply the new configuration file](../configure/updateconfiguration.md) — to learn how to apply changes to the `od.config` file in a Kubernetes cluster.

### Changing the authmanagers Configuration

Edit your `od.config` pyos configuration file and set the `authmanagers` dictionary with empty values for `implicit`, `explicit`, and `external`:

```
authmanagers: {
  'external': {},
  'explicit': {},
  'implicit': {}}
```

??? warning "json dictionary"
    ```
        If you define a dictionary, you must close the `}` on the same last line as the previous one. A simple quick example for authmanagers dictionary.
        authmanagers: {
          'external': {},
          'explicit': {},
          'implicit': {}}
    ```

To apply changes, replace the `abcdesktop-config` ConfigMap by running the `kubectl replace` command, then restart the `pyos` deployment:

```
kubectl create -n abcdesktop configmap abcdesktop-config --from-file=od.config  -o yaml --dry-run | kubectl replace -n abcdesktop -f -
kubectl rollout restart deployment pyos-od -n abcdesktop
```


Open your web browser and navigate to `http://localhost:30443`:

![authmanangers no provider](img/auth-no-provider.png)

The web home page displays only the abcdesktop.io title with no authentication providers available.

You can now configure authentication providers for your users.

## authmanagers `implicit`

`implicit` is the simplest configuration mode and is used for anonymous (always-allow) authentication.


![auth-overview-implicit](img/auth-overview-implicit.png)

Read the [authmanagers implicit](authimplicit.md) section.


## authmanagers `explicit`

`explicit` is configured to use a directory service such as LDAP.

![auth-overview-explicit](img/auth-overview-explicit.png)

Read the [authmanagers explicit](authexplicit.md) section.

## authmanagers `metaexplicit`

The `metaexplicit` authentication manager provides security across [multiple domains or forests through domain and forest trust relationships](https://learn.microsoft.com/en-us/entra/identity/domain-services/concepts-forest-trust). It reads the domain of the current user from another domain or forest, then performs the authentication process against the user's home domain.

`metaexplicit` supports Microsoft Active Directory trusted relationships, including Foreign Security Principals and Special Identities.


![auth-overview-explicit](img/auth-overview-explicit.png)

Read the [authmanagers meta explicit](authmetaexplicit.md) section.

## authmanagers `external`

`external` uses external OAuth 2.0 authentication services, such as [Google OAuth 2.0](https://developers.google.com/identity/protocols/oauth2), [GitHub OAuth 2.0](https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps), and others.

![auth-overview-external](img/auth-overview-external.png)

Read the [authmanagers external](authexternal.md) section.


## authmanagers Sample Configuration
        
After reading the [authmanagers implicit](authimplicit.md), [authmanagers explicit](authexplicit.md), and [authmanagers external](authexternal.md) sections, you will know how to define providers for each type.

You can combine all provider types into a single `authmanagers` dictionary:

- `external`
- `explicit`
- `implicit` 

For example, an abcdesktop login page with `external`, `explicit`, and `implicit` providers:

![allproviders](img/auth-overview-allproviders.png)

This page is generated from the following `authmanagers` configuration:

```json
authmanagers: {
  'external': {
    'providers': {
      'google': { 
        'icon': 'img/auth/google_icon.svg',
        'displayname': 'Google', 
        'textcolor': '#000000',
        'backgroundcolor': '#FFFFFF',
        'enabled': True,
        'client_id': 'xxxx', 
        'client_secret': 'xxxx',
        'userinfo_auth': True,
        'scope': [ 'https://www.googleapis.com/auth/userinfo.email',  'openid' ],
        'userinfo_url': 'https://www.googleapis.com/oauth2/v1/userinfo',
        'redirect_uri_prefix' : 'https://www.mydomain.com/API/auth/oauth',
        'redirect_uri_querystring': 'manager=external&provider=google',
        'authorization_base_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'policies': {  'acl': { 'permit': [ 'all' ] } }
     },
     'github': {
        'icon': 'img/auth/github_icon.svg',
        'textcolor': '#000000',
        'backgroundcolor': '#FFFFFF',
        'displayname': 'Github',
        'enabled': True,
        'basic_auth': True,
        'userinfo_auth': True,
        'scope' : [ 'read:user' ], 
        'client_id': 'xxxx',
        'client_secret': 'xxxx',
        'redirect_uri_prefix' : 'https://www.mydomain.com/API/auth/oauth',
        'redirect_uri_querystring': 'manager=external&provider=github',
        'authorization_base_url': 'https://github.com/login/oauth/authorize',
        'token_url': 'https://github.com/login/oauth/access_token',
        'userinfo_url': 'https://api.github.com/user',
        'policies': { 'acl' : { 'permit': [ 'all' ] } }
     }
    }
  },
  'explicit': {
    'show_domains': True,
    'default_domain': 'AD',
    'providers': {
      'AD': { 
        'config_ref': 'adconfig', 
        'enabled': True
       }
    }
  },
  'implicit': {
    'providers': {
      'anonymous': {
        'displayname': 'Guest',
        'textcolor': '#000000',
        'icon': 'img/auth/anonymous_icon.svg',
        'backgroundcolor': '#FFFFFF',
        'caption': 'Have a look !',
        'userid': 'anonymous',
        'username': 'Anonymous'
      } } } }


adconfig : { 
  'AD': { 
      'default' : True, 
      'ldap_timeout': 15,
      'ldap_basedn': 'DC=ad,DC=domain,DC=local',
      'ldap_fqdn': '_ldap._tcp.ad.domain.local',
      'domain': 'AD',
      'auth_type': 'KERBEROS',
      'domain_fqdn': 'AD.DOMAIN.LOCAL',
      'krb5_conf': '/etc/krb5.conf',
      'servers'    :  [ 'ldap://192.168.7.12' ],
      'kerberos_realm': 'AD.DOMAIN.LOCAL',
      'serviceaccount': { 'login': 'svcaccount', 'password':'account' },
      'auth_protocol' : { 
            'ntlm': True, 
            'cntlm': False, 
            'kerberos': True, 
            'citrix': False, 
            'localaccount': True },
      'query_dcs' : False } }
```

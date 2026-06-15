# Authentication `external`

## Requirements

To use the `external` authentication provider with OAuth 2.0, you need an FQDN and a secured website with HTTPS.

## Library

abcdesktop uses the [requests_oauthlib](https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html) Python module.

Requests-OAuthlib uses the Python Requests and OAuthlib libraries for building OAuth 2.0 clients.


## authmanagers `external`

The `external` authentication provider uses OAuth 2.0 authentication.

The `external` authentication configuration is defined as a dictionary object and contains a list of `external` providers.

Sample provider entry using the Google OAuth 2.0 authentication service:

```json
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
        'redirect_uri_prefix' : 'https://hostname.domain.local/API/auth/oauth',
        'redirect_uri_querystring': 'manager=external&provider=google',
        'authorization_base_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'policies': { 
          'acl': { 'permit': [ 'all' ] } 
        }
      }
  }}
```

- The values of `client_id` and `client_secret` have been set to the placeholder value `'xxxx'`.
- The `redirect_uri_prefix` contains the FQDN `hostname.domain.local`. Replace this with your own server's FQDN.


This configuration generates the following login area on the web front end:

![externalarea_description.png](img/externalarea_description.png)


Parameter reference:


| Variable name        | Type		    | Description                        | Sample  |
|----------------------|----------------|------------------------------------|----------|
|  `displayname`       | string         | Display name shown on the web front end | `Google`  |
|  `icon`              | string         | Path to the icon file. Must be in `svg` format. | `'img/auth/google_icon.svg'` |
|  `textcolor`         | string         | Text color for the front-end login page | `'#000000'` |
|  `backgroundcolor`   | string         | Background color for the front-end login page | `'#FFFFFF'` |
|  `enabled`   	       | boolean        | Enables or disables the provider   | `True`     |
|  `client_id`         | string         | OAuth 2.0 client ID                | `XXX-YYY.apps.googleusercontent.com` |
|  `client_secret`     | string         | OAuth 2.0 client secret            | `XXX` |
|  `scope`             | list of string | OAuth 2.0 scopes to request        | `[ 'https://www.googleapis.com/auth/userinfo.email',  'openid' ]` |
|  `userinfo_auth`     | boolean        | Enables the OAuth `userinfo` request. The default value is `True`. | `True` |
|  `userinfo_url`      | string         | URL of the userinfo endpoint       | `'https://www.googleapis.com/oauth2/v1/userinfo'` |
|  `redirect_uri_prefix`       | string | Base URL for the redirect URI      | `'https://hostname.domain.local/API/auth/oauth'` |
|  `redirect_uri_querystring`  | string | Query string appended to the redirect URI | `'manager=external&provider=google'` |
|  `authorization_base_url`    | string | OAuth 2.0 authorization endpoint   | `'https://accounts.google.com/o/oauth2/v2/auth'` |
|  `token_url`  			   | string | OAuth 2.0 token endpoint           | `'https://oauth2.googleapis.com/token'` |
| `userinfomap`                | dictionary | Remaps keys in the userinfo JSON response to new key names | `{ '*': '*', 'picture': 'picture.data.url' } ` |
| `policies`           | dict | Access control policies. The default value is `{}`. | `{ 'acl' : { 'permit': [ 'all' ] } }` |


- The complete redirect URL is constructed by concatenating `redirect_uri_prefix` and `redirect_uri_querystring`.
- The `userinfomap` overwrites the values for all fields listed in `[ 'userid', 'name' ]` and also the fields used to build the POSIX account: `[ 'cn', 'uid', 'gid', 'uidNumber', 'gidNumber', 'homeDirectory', 'loginShell', 'description', 'groups', 'gecos']`.


## Reading Groups and Setting Roles from userinfo

If `userinfo_auth` is `True`, abcdesktop attempts to read the JSON content from the `userinfo_url` endpoint. If the returned JSON dictionary contains a `groups` key whose value is a list of strings, the roles for the current user are set from that list. All roles are applied as label tags on the user's pod.

```python
     if isinstance( userinfo.get('groups'), list ):
            for role in userinfo.get('groups'):
                if isinstance(role, str):
                    roles.append(role)
```

For example, if the userinfo endpoint returns the following JSON:

```json
{ 
    "id": "34567345623452",
    "email": "mail@yourdomain.com",
    "verified_email": true,
    "picture": "https://lh3.googleusercontent.com/x-/xxxxxxxxxxxx",
    "hd": "yourdomain.com",
    "groups": [ "admins", "developers" ]
}
```

The user pod receives the following labels:

```
kubectl describe pods user-746b8   -n abcdesktop
```

The labels include `admins` and `developers`:

```
Labels:           abcdesktop/role=desktop
                  admins=true
                  developers=true
                  ...
```



## Orange OAuth

Orange's OAuth is supported for authentication. This API is based on OpenID Connect, which combines end-user authentication with OAuth 2.0 authorization.

### Orange Application
Create your Orange Application and set credentials for the Orange authentication API:

```json
 'orange': {       
        'displayname': 'Orange', 
        'icon': 'img/auth/orange_icon.svg',
        'textcolor': '#000000',
        'backgroundcolor': '#FFFFFF',
        'enabled': True,
        'basic_auth': True,
        'userinfo_auth': True,
        'scope' : [ 'openid', 'form_filling' ],
        'client_id': 'xxxx',
        'client_secret': 'xxxx',
        'redirect_uri_prefix' : 'https://hostname.domain.local/API/auth/oauth',
        'redirect_uri_querystring': 'manager=external&provider=orange',
        'authorization_base_url': 'https://api.orange.com/openidconnect/fr/v1/authorize',
        'token_url': 'https://api.orange.com/openidconnect/fr/v1/token', 
        'userinfo_url': 'https://api.orange.com/formfilling/fr/v1/userinfo',
        'policies': { 'acl'  : { 'permit': [ 'all' ] } }
      },
```


## Facebook OAuth
Facebook's OAuth is supported for authentication.

### Facebook Application
Create your Facebook Application credentials and set them for the Facebook authentication API:

```json
'facebook': { 
        'displayname': 'Facebook', 
        'icon': 'img/auth/facebook_icon.svg',
        'textcolor': '#000000',
        'backgroundcolor': '#FFFFFF',
        'enabled': True,
        'userinfo_auth': True,
        'client_id': 'xxxx', 
        'client_secret': 'xxxx', 
        'redirect_uri_prefix' : 'https://ocv4.pepins.net/API/auth/oauth',
        'redirect_uri_querystring': 'manager=external&provider=facebook',
        'authorization_base_url': 'https://www.facebook.com/dialog/oauth',
        'userinfo_url': 'https://graph.facebook.com/v2.6/me?fields=picture.width(400),name',
        'token_url': 'https://graph.facebook.com/v2.3/oauth/access_token',
        'userinfomap': {
            '*': '*',
            'picture': 'picture.data.url'
        },
        'policies': { 'acl'  : { 'permit': [ 'all' ] } }
      }
```

The `userinfomap` renames keys in the userinfo JSON document. In this example, it maps the key `picture` to the new key name `picture.data.url`.


## Google OAuth
Google's OAuth is supported for authentication. The `client_id` is the Google OAuth client ID, and `client_secret` is the OAuth client secret.


### Google Application
Create your Google credentials and configure the Google authentication API:

```json
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
        'redirect_uri_prefix' : 'https://hostname.domain.local/API/auth/oauth',
        'redirect_uri_querystring': 'manager=external&provider=google',
        'authorization_base_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'policies': { 
          'acl': { 'permit': [ 'all' ] } 
        }
      }    
```

## Github OAuth

GitHub's OAuth implementation supports the standard authorization code grant type and the OAuth 2.0 Device Authorization Grant for applications that do not have access to a web browser.

### Github OAuth

Enable other users to authorize your OAuth App. Create your GitHub credentials at [authorizing-oauth-apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps) and configure the GitHub authentication API:

```json
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
        'redirect_uri_prefix' : 'https://hostname.domain.local/API/auth/oauth',
        'redirect_uri_querystring': 'manager=external&provider=github',
        'authorization_base_url': 'https://github.com/login/oauth/authorize',
        'token_url': 'https://github.com/login/oauth/access_token',
        'userinfo_url': 'https://api.github.com/user',
        'policies': { 'acl' : { 'permit': [ 'all' ] } },
        'userinfomap': {  'uidNumber': 'id' }
      }
```

## LinkedIn OAuth

LinkedIn's OAuth is supported for authentication.

### LinkedIn Application
Create your LinkedIn Application and set credentials for the LinkedIn authentication API:

```json
 'linkedin': {
            'displayname': 'LinkedIn',
            'textcolor': 'white',
            'backgroundcolor': '#527edb',
            'icon': 'img/auth/linkedin.svg',
            'enabled': True,
            'userinfo_auth': True,
            'include_client_id': True,
            'scope': ['openid', 'profile', 'email'],
            'client_id': 'xxxx',
            'client_secret': 'xxxx',
            'redirect_uri_prefix': 'https://hostname.domain.local/API/auth/oauth',
            'redirect_uri_querystring': 'manager=external&provider=linkedin',
            'authorization_base_url': 'https://www.linkedin.com/oauth/v2/authorization',
            'token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
            'userinfo_url': 'https://api.linkedin.com/v2/userinfo'
            'policies': { 'acl'  : { 'permit': [ 'all' ] } }
          }
```

## Discord OAuth

Discord's OAuth is supported for authentication.

### Discord Application
Create your Discord Application and set credentials for the Discord authentication API:

```json
 'discord': {
            'displayname': 'Discord',
            'textcolor': 'white',
            'backgroundcolor': '#6e17e7',
            'icon': 'img/auth/discord.svg',
            'enabled': True,
            'userinfo_auth': True,
            'scope': ['identify'],
            'client_id': 'xxxx',
            'client_secret': 'xxxx',
            'redirect_uri_prefix': 'https://hostname.domain.local/API/auth/oauth',
            'redirect_uri_querystring': 'manager=external&provider=discord',
            'authorization_base_url': 'https://discord.com/oauth2/authorize',
            'token_url': 'https://discord.com/api/oauth2/token',
            'userinfo_url': 'https://discord.com/api/users/@me'
            'policies': { 'acl'  : { 'permit': [ 'all' ] } }
        }
```

## Keycloak OAuth

Keycloak's OAuth implementation supports the standard authorization code grant type and the OAuth 2.0 Device Authorization Grant for applications that do not have access to a web browser.

### Keycloak OAuth

Enable other users to authorize your OAuth App. Create your Keycloak credentials and configure the Keycloak authentication API:

```json
'keycloak': {
      'displayname': 'ABC Keycloak',
      'icon': 'img/auth/keycloak_icon.svg',
      'textcolor': '#000000',
      'backgroundcolor': '#FFFFFF',
      'enabled': True,
      'basic_auth': True,
      'userinfo_auth': True,
      'scope' : [ 'openid', 'roles', 'profile' ],
      'client_id': 'abcdesktop',
      'client_secret': 'xxxx',
      'redirect_uri_prefix' : 'https://hostname.domain.local/API/auth/oauth',
      'redirect_uri_querystring': 'manager=external&provider=keycloak',
      'authorization_base_url': 'https://auth.domain.local/realms/abc/protocol/openid-connect/auth',
      'token_url': 'https://auth.domain.local/realms/abc/protocol/openid-connect/token',
      'userinfo_url': 'https://auth.domain.local/realms/abc/protocol/openid-connect/userinfo',
      'revoke_url': 'https://auth.domain.local/realms/abc/protocol/openid-connect/revoke',
      'policies': { 'acl'  : { 'permit': [ 'all' ] } }
    }
```

You have successfully reviewed how the external OAuth 2.0 authentication configuration works.

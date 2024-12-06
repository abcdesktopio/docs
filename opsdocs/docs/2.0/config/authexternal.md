
# Authentification `external`

## Requirements

To use `external` Authentification OAuth 1.0 and or OAuth 2.0, you need an internet FQDN and a secured web site with https.

## Library

abcdesktop uses [requests_oauthlib](https://requests-oauthlib.readthedocs.io/en/latest/oauth2_workflow.html) python module. Requests-OAuthlib uses the Python Requests and OAuthlib libraries for building OAuth1 and OAuth2 clients.


## authmanagers `external`:

`external` authentification use OAuth 2.0 authenticaton.

The `external` authentification configuration is defined as a dictionary object and contains a list of `external` provider. 

Sample providers entry using the Google OAuth 2.0 authentification service. 

```json
'external': {
    'providers': {
    'google': { 
        'displayname': 'Google', 
        'enabled': True,
        'client_id': 'XXX-YYY.apps.googleusercontent.com', 
        'client_secret': 'XXX',
        'userinfo_auth': True,
        'scope': [ 'https://www.googleapis.com/auth/userinfo.email',  'openid' ],
        'userinfo_url': 'https://www.googleapis.com/oauth2/v1/userinfo',
        'redirect_uri_prefix' : 'https://host.domain.local/API/auth/oauth',
        'redirect_uri_querystring': 'manager=external&provider=google',
        'authorization_base_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token'
    }
}
```

The variable values `client_id` and `client_secret` have been set to obfuscate value 'XXX'. The FQDN is refered to the public server FQDN. 


| Variable name        | Type		       | Description                        | Sample  |
|----------------------|----------------|------------------------------------|----------|
|  `displayname`       | string         | Display Name show in Web front     | `Google`  |
|  `enabled`   	      | boolean        | LDAP Base Distinguished Names      | `True`     |
|  `client_id`        | string         | client id                          | `XXX-YYY.apps.googleusercontent.com` |
|  `client_secret` | string         | client secret                      | `XXX` |
|  `scope`         | list of string         | scope                              | `[ 'https://www.googleapis.com/auth/userinfo.email',  'openid' ]` |
|  `userinfo_url`    | string         | dialog URL                         | `https://www.googleapis.com/oauth2/v1/userinfo' |
|  `redirect_uri_prefix`      | string         | redirect URL               | `https://hostname.domain.local/API/auth/oauth` |
|  `redirect_uri_querystring`  | string | URL query string | `manager=external&provider=google` |
|  `authorization_base_url`    | string | callback URL   | `https://accounts.google.com/o/oauth2/v2/auth` |
|  `token_url`  					 | string | token URL | `https://oauth2.googleapis.com/token` |


The complete redirect url concats the two values `redirect_uri_prefix` and `redirect_uri_querystring`.

## Orange OAuth 2.0 

Orange's OAuth is supported for authentication. This API is based on OpenID Connect, which combines end-user authentication with OAuth2 authorisation. 

### Orange Application
Create your Orange Application here [https://developer.orange.com/apis](https://developer.orange.com/apis) and set credentials for Orange Authentification API in the section 

```json
'orange': {       
        'displayname': 'Orange', 
        'enabled': True,
        'basic_auth': True,
        'userinfo_auth': True,
        'scope' : [ 'openid', 'form_filling' ],
        'client_id': 'XXX',
        'client_secret': 'YYY',
        'redirect_uri_prefix' : 'https://hostname.domain.local/API/auth/oauth',
        'redirect_uri_querystring': 'manager=external&provider=orange',
        'authorization_base_url': 'https://api.orange.com/openidconnect/fr/v1/authorize',
        'token_url': 'https://api.orange.com/openidconnect/fr/v1/token', 
        'userinfo_url': 'https://api.orange.com/formfilling/fr/v1/userinfo',
      }
```


## Facebook OAuth 2.0
Facebook's OAuth is supported for authentication. 

### Facebook Application
Create your Facebook Application credentials here : [https://developers.facebook.com/apps/](https://developers.facebook.com/apps/) and set the credentials for Facebook Authentification API  

```json
'facebook': { 
        'displayname': 'Facebook', 
        'enabled': True,
        'userinfo_auth': True,
        'client_id': 'XXX', 
        'client_secret': 'YYY', 
        'redirect_uri_prefix' : 'https://hostname.domain.local/API/auth/oauth',
        'redirect_uri_querystring': 'manager=external&provider=facebook',
        'authorization_base_url': 'https://www.facebook.com/dialog/oauth',
        'userinfo_url': 'https://graph.facebook.com/v2.6/me?fields=picture.width(400),name',
        'token_url': 'https://graph.facebook.com/v2.3/oauth/access_token',
        'userinfomap': {
            '*': '*',
            'picture': 'picture.data.url'
        }
```

## Google OAuth 2.0
Google's OAuth is supported for authentication. The client_id is the google's OAuth client ID, and the client_secret is the OAuth client secret. 


### Google Application
Create your Google credentials here : [https://console.developers.google.com/apis/](https://console.developers.google.com/apis/) and set the correct credentials for Google Authentification API in the section [gauth]

```json
'google': { 
        'displayname': 'Google', 
        'enabled': True,
        'client_id': 'XXX-YYY.apps.googleusercontent.com', 
        'client_secret': 'XXX',
        'userinfo_auth': True,
        'scope': [ 'https://www.googleapis.com/auth/userinfo.email',  'openid' ],
        'userinfo_url': 'https://www.googleapis.com/oauth2/v1/userinfo',
        'redirect_uri_prefix' : 'https://host.domain.local/API/auth/oauth',
        'redirect_uri_querystring': 'manager=external&provider=google',
        'authorization_base_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token'
    }
```


Great, you have check how the implicit Authentification configuration works.



# Authentification ```external```

## Requirements

To use ```external``` Authentification Auth 2.0, you need an Internet FQDN and a secured web site with https.
 

## authmanagers ```external```:

```external``` authentification use OAuth 2.0 authenticaiton.

The ```external ``` authentification configuration is defined as a dictionnary object and contains a list of ```external ``` provider. 

Sample providers entry using the Google OAuth 2.0 authentification service. 

```
'external': {
    'providers': {
      'google': { 
        'displayname': 'Google', 
        'enabled': True,
        'client_id': 'YYYYYY', 
        'client_secret': 'XXXXXX',
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'dialog_url': 'https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={callback_url}&response_type=code&scope={scope}',
        'auth_url': 'https://oauth2.googleapis.com/token?code={code}&grant_type=authorization_code&redirect_uri={callback_url}&scope={scope}&client_id={client_id}&client_secret={client_secret}',
        'userinfo_url': 'https://openidconnect.googleapis.com/v1/userinfo?access_token={access_token}',
        'callback_url': 'https://FQDN/API/auth/oauth?manager={manager.name}&provider={name}'
      }
    }
```

The variable values ```client_id``` and ```client_secret``` have been set to obfuscate value 'XXXXXX', and 'YYYYYY'. The FQDN refere to the public FQDN service. 




| Variable name        | Type		       | Description                        | Sample  |
|----------------------|----------------|------------------------------------|----------|
|  ```displayname ```  | string         | Display Name show in Web front     | ```Facebook```  |
|  ```enabled```   	   | boolean        | LDAP Base Distinguished Names      | ```True```     |
|  ```client_id```     | string         | client id                          | ```799057940444306``` |
|  ```client_secret``` | string         | client secret                      | ```354aa49ea1ff2e1515aaa6aa40fa899a``` |
|  ```scope```         | string         | scope                              | ```https://www.googleapis.com/auth/userinfo.email``` |
|  ```dialog_url```    | string         | dialog URL                         | ```https://www.facebook.com/dialog/oauth?client_id={client_id}&redirect_uri={callback_url}&response_type=code``` |
|  ```auth_url```      | string         | authentification URL               | ```https://graph.facebook.com/v2.3/oauth/access_token?code={code}&redirect_uri={callback_url}&client_id={client_id}&client_secret={client_secret}``` |
|  ```userinfo_url```  | string         | userinfo URL                       | ```https://graph.facebook.com/v2.6/me?access_token={access_token}&fields=picture.width(400),name``` |
|  ```callback_url```  | string         | callback URL                       | ```https://host.domain.tldn/API/auth/oauth?manager={manager.name}&provider={name}``` |
|  ```userinfomap```  (optional)  | dictionnary    | userinfomap dictionnary to get user information | ``` { '*': '*', 'picture': 'picture.data.url' } ``` |



## Orange OAuth 2.0 

Orange's OAuth is supported for authentication. This API is based on OpenID Connect, which combines end-user authentication with OAuth2 authorisation. 

### Orange Application
Create your Orange Application here [https://developer.orange.com/apis](https://developer.orange.com/apis) and set credentials for Orange Authentification API in the section 

```
 'orange': {       
        'displayname': 'Orange', 
        'enabled': True,
        'basic_auth': True,
        'userinfo_auth': True,
        'client_id': 'XXXXXX', 
        'client_secret': 'YYYYYY',
        'dialog_url': 'https://api.orange.com/oauth/v2/authorize?client_id={client_id}&redirect_uri={callback_url}&scope=openid+profile+offline_access&response_type=code&prompt=login+consent&state={cal
lback_url}',
        'auth_url': 'https://api.orange.com/openidconnect/fr/v1/token?code={code}&redirect_uri={callback_url}&grant_type=authorization_code', 
        'userinfo_url': 'https://api.orange.com/openidconnect/v1/userinfo',
        'callback_url': 'https://FQDN/API/auth/oauth?manager={manager.name}&provider={name}'
      }
```


## Facebook OAuth 2.0
Facebook's OAuth is supported for authentication. 

### Facebook Application
Create your Facebook Application credentials here : [https://developers.facebook.com/apps/](https://developers.facebook.com/apps/) and set the credentials for Facebook Authentification API  

```
 'facebook': { 
        'displayname': 'Facebook', 
        'enabled': True,
        'client_id': 'XXXXXX', 
        'client_secret': 'YYYYYY', 
        'dialog_url': 'https://www.facebook.com/dialog/oauth?client_id={client_id}&redirect_uri={callback_url}&response_type=code',
        'auth_url': 'https://graph.facebook.com/v2.3/oauth/access_token?code={code}&redirect_uri={callback_url}&client_id={client_id}&client_secret={client_secret}',
        'userinfo_url': 'https://graph.facebook.com/v2.6/me?access_token={access_token}&fields=picture.width(400),name',
        'callback_url': 'https://FQDN/API/auth/oauth?manager={manager.name}&provider={name}',
        'userinfomap': {
            '*': '*',
            'picture': 'picture.data.url'
        }
      }
```

## Google OAuth 2.0
Google's OAuth is supported for authentication. The client_id is the google's OAuth client ID, and the client_secret is the OAuth client secret. 


### Google Application
Create your Google credentials here : [https://console.developers.google.com/apis/](https://console.developers.google.com/apis/) and set the correct credentials for Google Authentification API in the section [gauth]

```
'external': {
    'providers': {
      'google': { 
        'displayname': 'Google', 
        'enabled': True,
        'client_id': 'YYYYYY', 
        'client_secret': 'XXXXXX',
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        'dialog_url': 'https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={callback_url}&response_type=code&scope={scope}',
        'auth_url': 'https://oauth2.googleapis.com/token?code={code}&grant_type=authorization_code&redirect_uri={callback_url}&scope={scope}&client_id={client_id}&client_secret={client_secret}',
        'userinfo_url': 'https://openidconnect.googleapis.com/v1/userinfo?access_token={access_token}',
        'callback_url': 'https://FQDN/API/auth/oauth?manager={manager.name}&provider={name}'
      }
    }
```


Great, you have check how the implicit Authentification configuration works.


---
title: Logmein SSL Mutual Authentication | abcdesktop.io
description: Configure the abcdesktop.io logmein provider for SSL mutual TLS (mTLS) certificate-based authentication forwarded via a reverse proxy.
keywords: logmein, mTLS, mutual TLS, SSL client certificate, reverse proxy, authentication, abcdesktop, Kubernetes, security
tags:
  - authentication
  - mTLS
  - security
---

# logmein Authentication


`logmein` redirects users to an HTTPS website to perform mutual SSL (mTLS) authentication.

``` mermaid
---
config:
  mirrorActors: false
  look: handDrawn
title: implicit with mutual authentication
---
sequenceDiagram
  actor user as user
  participant secure as secure
  participant pyos as pyos
  user ->> pyos: implicit auth
  pyos ->> user: go to secure for that
  user ->> secure: hello 
  secure ->> user: who comes there ?
  Note left of user: I have my certificat
  user ->> secure: certificat
  secure ->> secure: certificat check
  secure ->> pyos: user with certificat wants to login 
  pyos ->> pyos: security check
  Note right of pyos: Where the http request comes from ?
  Note right of pyos: What is this certificat ?
  pyos ->> user: user JWT
  user ->> pyos: create desktop ( user JWT )
  pyos ->> user: desktop JWT
```

In the typical flow, the user is redirected to an HTTPS service and authenticated using their X.509 certificate. The certificate is then forwarded via an HTTP header to `pyos`, which performs security checks and issues a user JWT to the client.


 
- `logmein` is an `implicit` provider.

The user is redirected to `dialog_url`. For example, `https://secure.your_domain.com/protectedbyssl`.
The implicit provider configuration looks like this:

```
'implicit': {
  'providers'   : {
    'sslclient' : {
      'displayname': 'Logmein protected by SSL',
      'icon': 'img/auth/sslclient_icon.svg',
      'textcolor': '#000000',
      'backgroundcolor': '#FFFFFF',
      'enabled': True,
      'dialog_url' : 'https://secure.your_domain.com/protectedbyssl',
      'auth_protocol' : { 'localaccount': True }
    } 
  }
}
``` 

Mutual SSL authentication is performed at `dialog_url`: `https://secure.your_domain.com/protectedbyssl`. If the SSL client certificate is successfully verified, the user is proxy-passed from `https://secure.your_domain.com/protectedbyssl` to `$my_node/API/auth/logmein?provider=sslclient`.

```
location /protectedbyssl {
   if ($ssl_client_verify != SUCCESS) {return 403 $ssl_client_verify;}
   proxy_set_header AbcdesktopUserCert $ssl_client_escaped_cert;
   proxy_pass $my_node/API/auth/logmein?provider=sslclient;
}
```

> The server requests the client's certificate in a `CertificateRequest` message, enabling mutual TLS authentication.

### `logmein` Endpoint Configuration

The `API/auth/logmein` endpoint performs security checks to verify that the request originates from an authorized network defined in `network_list`. When configured, it also validates the required HTTP header name and its value. It reads the X.509 certificate to extract the user ID and then performs implicit authentication for that user.

```
auth.logmein : {  
	'enable' : True,
	'network_list' : ['0.0.0.0/0'],
	'permit_querystring' : False,
	'http_attribut' : 'ABCDESKTOPUSERCERT' }
```   


| Variable name       | Type     | Description   |
|---------------------|----------|-------------|
| `enable `           | boolean  | Enables or disables the logmein feature. The default value is `False`. |
| `network_list`      | list     | List of subnets authorized to query the `logmein` endpoint. | 
| `permit_querystring`| boolean  | Allows passing the `userid` as a query string parameter. The default value is `False`. |
| `oid_list`          | list     | List of OID strings used to read the user ID from the X.509 certificate. The default values are `[ cryptography.x509.oid.NameOID.USER_ID, cryptography.x509.oid.NameOID.COMMON_NAME ]`. |
| `http_attribut`     | string   | (Optional) Name of the HTTP header. If set, the value of this header must be a PEM-encoded X.509 certificate. | 


The `oid_list` entries are resolved from OID dotted-string notation to `ObjectIdentifier` objects. For example, `[ cryptography.x509.oid.NameOID.USER_ID, cryptography.x509.oid.NameOID.COMMON_NAME ]` becomes `[ '0.9.2342.19200300.100.1.1', '2.5.4.3' ]`.




## nginx Configuration with Mutual Authentication

- nginx reverse proxy sample:

```
server {
	listen   443;
	server_name secure.your_domain.com;
	
	root /usr/share/nginx/www;
	index index.html index.htm;
	
	resolver a.b.c.d; # if need
	ssl on;
	ssl_certificate /etc/letsencrypt/live/secure.your_domain.com/fullchain.pem;
	ssl_certificate_key /etc/letsencrypt/live/secure.your_domain.com/privkey.pem;

	# where should you go ?
	# to your abcdesktop web site to call /API/auth/logmein endpoint
	set $my_node  http://abcdesktop_url:30443;

	# client certificate
	ssl_client_certificate /etc/nginx/ca/ca-cert.pem;
	# make verification optional, so we can display a 403 message to those
	# who fail authentication
	# ssl_verify_client optional;
	ssl_verify_depth 2;
	ssl_verify_client on;

	location /protectedbyssl {
	   if ($ssl_client_verify != SUCCESS) {return 403 $ssl_client_verify;}
	   proxy_set_header AbcdesktopUserCert $ssl_client_escaped_cert;
	   proxy_pass $my_node/API/auth/logmein?provider=sslclient;
	}
```


## od.config file


```
auth.logmein : {  
	'enable' : True,
	'network_list' : ['0.0.0.0/0'], 
	'permit_querystring' : False,
	'http_attribut' : 'ABCDESKTOPUSERCERT' }

authmanagers: {
  'implicit': {
     'providers'   : {
	     'sslclient' : {
	          'displayname': 'Logmein protected by SSL',
	          'icon': 'img/auth/sslclient_icon.svg',
	          'textcolor': '#000000',
	          'backgroundcolor': '#FFFFFF',
	          'enabled': True,
	          'dialog_url' : 'https://secure.your_domain.com/protectedbyssl',
	          'auth_protocol' : { 'localaccount': True }
	     } } } }
```



# abcdesktop configuration


## configuration file

The abcdesktop configuration is embedded inside a kubernetes `configmap`


```bash
NAMESPACE=abcdesktop
kubectl -n $NAMESPACE get configmap abcdesktop-config
```

The `abcdesktop-config` configmap contains a file `od.config`. To read the `od.config` content

```bash
kubectl -n abcdesktop get configmap abcdesktop-config -o jsonpath='{.data.od\.config}' > od.config
```

This file has the [cherrypy file format](https://docs.cherrypy.dev/en/stable/config.html).

When the pyos process starts, it reads the `od.config` file.

If something is wrong, the pyos process hangs. The command line `kubectl logs -l name=pyos-od  -n abcdesktop` writes the pyos log to stdout.


## [global]

The section describe the `[global]` values define in `od.config` file.


### `default_host_url`

The default host url is the public host url of the service. Change this with your own URL or set the external URL service if you use a reverse proxy


```
# DEFAULT HOST URL 
# public host url of the service
# change this with your URL or
# set the external URL service if you use a reverse proxy
# default_host_url : 'https://abcdesktop.domain.com'
default_host_url : 'https://abcdesktop.domain.com'
# END OF DEFAULT HOST URL
```

### Geolocation `server.geolocation_ipaddr`


`server.geolocation_ipaddr` is used by geoip to locate the external ip of the service. Change this value to help geoip to locate your service


```
#
# EXTERNAL IP ADDRESS SECTION
# THIS IS NOT THE BINDING IP ADDR
# server.geolocation_ipaddr is only used to locate the external ip of the service
# server.geolocation_ipaddr is used by geoip and Active Directory site subnet queries
# the default value is a dummy value '127.0.0.1'
# change this value to help geoip to locate your service or for Active Directory site and subnet query 
server.geolocation_ipaddr: '127.0.0.1'
# END OF EXTERNAL IP ADDRESS SECTION
```

### `trusted_proxy_cidr`

`trusted_proxy_cidr` is a list of subnet IPv4 or IPv6.
The default value is an empty list `[]`

If the list is not empty, read all ip addresses in the `X-Forwarded-For` http header. At least one ip address of the `X-Forwarded-For` must match in the `trusted_proxy_cidr` list, else a http 401 error is returned. 

`trusted_proxy_cidr` list prevents reverse proxy spoofing.

```
trusted_proxy_cidr : [ '10.0.0.0/8', '192.168.1.0/24' ]
```



## `server.thread_pool`

`server.thread_pool` defines the number of worker threads to start up in the pool, the default value is `server.thread_pool: 10` 

```
# the default server.thread_pool is 10
# increase this value to add more cherrypy threads
# server.thread_pool: 16
# END OF THREAD_POOL
```

## `OAUTHLIB`

- `OAUTHLIB_INSECURE_TRANSPORT`

OAuthLib will raise an InsecureTransportError if you attempt to use OAuth2 over HTTP, rather than HTTPS. Setting this environment variable will prevent this error from being raised. This is mostly useful for local testing, or automated tests.

```
OAUTHLIB_INSECURE_TRANSPORT: True
```

- `OAUTHLIB_RELAX_TOKEN_SCOPE` needs to request user authorization from a Microsoft Work account.

```
# fix request user authorization from a Microsoft Work account
OAUTHLIB_RELAX_TOKEN_SCOPE: True
```


## K8S timeout

- PVC timeout
- Create pod and ephemeral container timeout

``` 
# default time out to bound a persistentVolumeClaim
K8S_BOUND_PVC_TIMEOUT_SECONDS: 60
K8S_BOUND_PVC_MAX_EVENT: 5

# default time out to create a pod
K8S_CREATE_POD_TIMEOUT_SECONDS: 360
K8S_CREATE_EPHEMERALCONTAINER_TIMEOUT_SECONDS: 5
```


## JWT and RSA keys


Define the RSA keys to sign and encrypt payload.

There are two kinds of `JWT`:

- `jwt_token_user` User JWT is signed. So we need to define a (private, public) RSA keys for signing. 
- `jwt_token_desktop` Desktop JWT is encrypted AND signed. So we need to define a (private, public) RSA keys for signing, and a (private, public) RSA keys to encrypt data.


```
# JWT SECTION
# JWT Token for /API URL
# exp : time in seconds, None for unlimited
jwt_token_user : {
  'exp': 360,
  'jwtuserprivatekeyfile': '/config.usersigning/abcdesktop_jwt_user_signing_private_key.pem',
  'jwtuserpublickeyfile' : '/config.usersigning/abcdesktop_jwt_user_signing_public_key.pem' }
#
# JWT RSA SIGNING ANS PAYLOAD KEYS
#
jwt_token_desktop : {
  'exp': 420,
  'jwtdesktopprivatekeyfile':     '/config.signing/abcdesktop_jwt_desktop_signing_private_key.pem',
  'jwtdesktoppublickeyfile' :     '/config.signing/abcdesktop_jwt_desktop_signing_public_key.pem',
  'payloaddesktoppublickeyfile' : '/config.payload/abcdesktop_jwt_desktop_payload_public_key.pem' }
# END OF JWT SECTION #
```


* The JWT payload is encrypted with the abcdesktop jwt desktop payload private by pyos
* The JWT payload is decrypted with the abcdesktop jwt desktop payload public keys by nginx.

> Use the payload private key as the encryption key, and keep the payload public key private as well.
> Do not publish the payload public key. This key must remain private — this is a deliberate security design choice, not a mistake.

* The JSON Web Tokens payload is signed with the abcdesktop jwt desktop signing private keys
* The JSON Web Tokens payload is verified with the abcdesktop jwt desktop signing public keys.

* The JSON Web Tokens user is signed with the abcdesktop jwt user signing private keys by pyos.
* The JSON Web Tokens user is verified with the abcdesktop jwt user signing public keys by pyos

> As multiple pods of pyos can run simultaneously, the same private and public keys value are stored into kubernetes secret.

The abcdesktop JWT desktop payload public key is read by the route container. When exporting the public key, the `RSAPublicKey_out` option must be used to produce the `RSAPublicKey` format. The `RSAPublicKey` format ensures compatibility between the `python 3.x jwt module` and the `lua jwt lib`.


The following commands will let you create all necessary keys :

```
openssl genrsa -out abcdesktop_jwt_desktop_payload_private_key.pem 1024
openssl rsa -in abcdesktop_jwt_desktop_payload_private_key.pem -outform PEM -pubout -out  _abcdesktop_jwt_desktop_payload_public_key.pem
openssl rsa -pubin -in _abcdesktop_jwt_desktop_payload_public_key.pem -RSAPublicKey_out -out abcdesktop_jwt_desktop_payload_public_key.pem
openssl genrsa -out abcdesktop_jwt_desktop_signing_private_key.pem 1024
openssl rsa -in abcdesktop_jwt_desktop_signing_private_key.pem -outform PEM -pubout -out abcdesktop_jwt_desktop_signing_public_key.pem
openssl genrsa -out abcdesktop_jwt_user_signing_private_key.pem 1024
openssl rsa -in abcdesktop_jwt_user_signing_private_key.pem -outform PEM -pubout -out abcdesktop_jwt_user_signing_public_key.pem
```
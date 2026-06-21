---
title: Configuration File Overview | abcdesktop.io
description: Reference for the abcdesktop.io od.config global configuration parameters: host URL, trusted proxy CIDR, JWT/RSA key pairs, thread pool, Kubernetes timeouts, and OAuth settings.
keywords: od.config, configuration, JWT, RSA, trusted proxy, CIDR, ConfigMap, Kubernetes, abcdesktop, thread pool, OAuth
tags:
  - configuration
---


# abcdesktop configuration


## Configuration File

The abcdesktop configuration is stored inside a Kubernetes `ConfigMap`.


```bash
NAMESPACE=abcdesktop
kubectl -n $NAMESPACE get configmap abcdesktop-config
```

The `abcdesktop-config` ConfigMap contains a file named `od.config`. To read the `od.config` content:

```bash
kubectl -n abcdesktop get configmap abcdesktop-config -o jsonpath='{.data.od\.config}' > od.config
```

This file uses the [CherryPy configuration file format](https://docs.cherrypy.dev/en/stable/config.html).

When the `pyos` process starts, it reads the `od.config` file. If the file contains a syntax error, the `pyos` process fails to start. Inspect the `pyos` logs with `kubectl logs -l name=pyos-od -n abcdesktop`.


## [global]

This section describes the `[global]` values defined in the `od.config` file.


### `default_host_url`

The default host URL is the publicly accessible URL of the abcdesktop service. Set this to your own domain name, or to the external URL of a reverse proxy if one is deployed in front of the service.


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


`server.geolocation_ipaddr` is used by the GeoIP subsystem to determine the external IP address of the service. Update this value with your service's actual external IP address to enable accurate geolocation and Active Directory site and subnet queries.


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

`trusted_proxy_cidr` is a list of IPv4 or IPv6 CIDR subnets.
The default value is an empty list (`[]`).

When this list is not empty, the service reads all IP addresses from the `X-Forwarded-For` HTTP header. At least one IP address in the `X-Forwarded-For` header must match an entry in the `trusted_proxy_cidr` list; otherwise, the service returns an HTTP 401 error.

The `trusted_proxy_cidr` list prevents reverse proxy IP spoofing attacks.

```
trusted_proxy_cidr : [ '10.0.0.0/8', '192.168.1.0/24' ]
```



## `server.thread_pool`

`server.thread_pool` defines the number of worker threads in the CherryPy thread pool. The default value is `10`.

```
# the default server.thread_pool is 10
# increase this value to add more cherrypy threads
# server.thread_pool: 16
# END OF THREAD_POOL
```

## `OAUTHLIB`

- `OAUTHLIB_INSECURE_TRANSPORT`

OAuthLib raises an `InsecureTransportError` when OAuth2 is used over HTTP instead of HTTPS. Setting this environment variable suppresses that error. Enable this option only for local development or automated testing environments.

```
OAUTHLIB_INSECURE_TRANSPORT: True
```

- `OAUTHLIB_RELAX_TOKEN_SCOPE` is required when requesting user authorization from a Microsoft Work or organizational account.

```
# fix request user authorization from a Microsoft Work account
OAUTHLIB_RELAX_TOKEN_SCOPE: True
```


## Kubernetes Timeouts

- PVC creation timeout
- Pod and ephemeral container creation timeout

``` 
# default time out to bound a persistentVolumeClaim
K8S_BOUND_PVC_TIMEOUT_SECONDS: 60
K8S_BOUND_PVC_MAX_EVENT: 5

# default time out to create a pod
K8S_CREATE_POD_TIMEOUT_SECONDS: 360
K8S_CREATE_EPHEMERALCONTAINER_TIMEOUT_SECONDS: 5
```


## JWT and RSA Keys


RSA key pairs are used to sign and encrypt JWT payloads within abcdesktop.

Two types of JWT tokens are used by abcdesktop:

- `jwt_token_user`: The user JWT is signed only. A (private, public) RSA key pair is required for signing.
- `jwt_token_desktop`: The desktop JWT is both signed and encrypted. It requires a (private, public) RSA key pair for signing and a separate (private, public) RSA key pair for payload encryption.


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


* The JWT payload is encrypted by `pyos` using the abcdesktop JWT desktop payload private key.
* The JWT payload is decrypted by `nginx` using the abcdesktop JWT desktop payload public key.

> Use the payload private key as the encryption key, and keep the payload public key private as well.
> Do not publish the payload public key. This key must remain private — this is a deliberate security design choice, not a mistake.

* The JWT payload is signed using the abcdesktop JWT desktop signing private key.
* The JWT payload is verified using the abcdesktop JWT desktop signing public key.

* The user JWT is signed by `pyos` using the abcdesktop JWT user signing private key.
* The user JWT is verified by `pyos` using the abcdesktop JWT user signing public key.

> Because multiple `pyos` pods may run simultaneously, the same private and public key values are stored in a Kubernetes Secret.

The abcdesktop JWT desktop payload public key is read by the route container. When exporting the public key, you must use the `RSAPublicKey_out` option to produce the `RSAPublicKey` format, which ensures compatibility between the Python 3.x JWT module and the Lua JWT library.


Use the following commands to generate all required key pairs:

```
openssl genrsa -out abcdesktop_jwt_desktop_payload_private_key.pem 1024
openssl rsa -in abcdesktop_jwt_desktop_payload_private_key.pem -outform PEM -pubout -out  _abcdesktop_jwt_desktop_payload_public_key.pem
openssl rsa -pubin -in _abcdesktop_jwt_desktop_payload_public_key.pem -RSAPublicKey_out -out abcdesktop_jwt_desktop_payload_public_key.pem
openssl genrsa -out abcdesktop_jwt_desktop_signing_private_key.pem 1024
openssl rsa -in abcdesktop_jwt_desktop_signing_private_key.pem -outform PEM -pubout -out abcdesktop_jwt_desktop_signing_public_key.pem
openssl genrsa -out abcdesktop_jwt_user_signing_private_key.pem 1024
openssl rsa -in abcdesktop_jwt_user_signing_private_key.pem -outform PEM -pubout -out abcdesktop_jwt_user_signing_public_key.pem
```
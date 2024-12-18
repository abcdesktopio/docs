
# Controllers 

## Controllers
abcdesktop is based on the Model View Controller (usually known as MVC). This MVC is used for developing user interfaces which divides the related program logic into three interconnected elements. This is done to separate internal representations of information from the ways information is presented to and accepted from the user.

List of all abcdesktop's controllers and the description : 

| Controller               |  Description   |
|--------------------------|--------------- |
|`AccountingController`   	| accounting data json format |
|`AuthController`			| authenticate user  |
|`ComposerController` 		| CRUD main services (like createDesktop, createApplication)|
|`CoreController`			| get configuration and user message info |
|`ManagerController` 		| manage service (like add an application)  |
|`UserController`			| retrieve user information |


## Access Permission

The `controllers` configuration is a dictionary, and is defined in the pyos's `od.config` file. 

```json
controllers : { 
	'AccountingController': { 
		'apikey': [ 'fPCdPNcCafec4lXm3M' ],
		'permitip': [ '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', 'fd00::/8', '169.254.0.0/16', '127.0.0.0/8' ] 
	},
	'ManagerController': { 
		'apikey': [ 'fQDbvjCafec4l', 'KzH23EZjCZSfsd9'],
		'permitip': [ '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', 'fd00::/8', '169.254.0.0/16', '127.0.0.0/8' ] 
	},
	'AuthController' : 		{ 'permitip': None },
	'ComposerController' : 	{ 'permitip': None },
	'CoreController' : 		{ 'permitip': None },
	'UserController' : 		{ 'permitip': None }
} 
```

By default, `AccountingController` and `ManagerController` access are protected by ip source filters.
The configuration permits private networks defined in [rfc1918](https://tools.ietf.org/html/rfc1918) and [rfc4193](https://tools.ietf.org/html/rfc4193). Get more information about the [private network](https://en.wikipedia.org/wiki/Private_network).

By default, others controllers access is enabled, without any restriction.

### Access control filter 

The access control filter configuration is defined in a json dictionary.
Each dictionary entry use the `controller` name and with entries `permitip` and/or `apikey`.

- The `permitip` is a list of subnet, for example `[ '10.0.0.0/8', '172.16.0.0/12' ]`. If `permitip` is not set or if the `controller` is not defined, filtering features is disabled.
- The `apikey` is a list of string, for example `[ 'fPCdPSSj8gZri1Ncmg', 'Z9pXCa2y6ccDeBBeeUc4' ]`.
If `apikey`  is not set or the ```controller``` not defined, filtering features is disabled. The http header value is `X-API-Key`

If the source ip address is denied, the response is a HTTP status is 403 `code 403 Forbidden`
	
```json
{"status": 403, "status_message": "403 Forbidden", "message": "Request forbidden -- authorization will not help"} 
```


## Curl http requests sample

### Curl http request with `X-API-Key`

Add the http header `X-API-Key: fQDbvjCafec4l` to the curl command to list images

```bash
curl -X GET -H 'X-API-Key: fQDbvjCafec4l' -H 'Content-Type: text/javascript' http://localhost:30443/API/manager/images
```

The command returns

```json
{}
```

Add the http header `X-API-Key: fQDbvjCafec4l` to the curl command to add new application

```bash
curl -X POST -H 'X-API-Key: fQDbvjCafec4l'  -H 'Content-Type: text/javascript' http://localhost:30443/API/manager/image -d@xeyes.d.3.0.json
```

The command returns

```json
[
 {	"cmd": ["/composer/appli-docker-entrypoint.sh"], 
 	"path": "/usr/bin/xeyes", 
 	"sha_id": "sha256:4ed2e110042b80f1634d8f3ae66b793914db813f53cd88811285448602d7540e", 
 	"id": "abcdesktopio/xeyes.d:3.0", 
 	"rules": {}, 
 	"acl": {"permit": ["all"]}, 
 	"launch": "xeyes.XEyes", 
 	"name": "xeyes", 
 	"icon": "circle_xfce4-eyes.svg", 
 	"keyword": "xeyes,eyes", 
 	"uniquerunkey": null, 
 	"cat": "utilities", 
 	"args": null, 
 	"execmode": null, 
 	"showinview": null, 
 	"displayname": "xeyes", 
 	"home": null, 
 	"desktopfile": null, 
 	"executeclassname": null, 
 	"executablefilename": "xeyes", 
 	"usedefaultapplication": false, 
 	"mimetype": [], 
 	"fileextensions": [], 
 	"legacyfileextensions": [], 
 	"secrets_requirement": null, 
 	"image_pull_policy": "IfNotPresent", 
 	"image_pull_secrets": null, 
 	"containerengine": "ephemeral_container", 
 	"securitycontext": {}
 }
]
```

### Curl http request forbidden

```bash
curl -X DELETE -H 'Content-Type: text/javascript' http://localhost:30443/API/manager/images
```

The command returns

```json
{"status": 403, "message": "Request forbidden -- authorization will not help"}
```
 

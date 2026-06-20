# Controllers

## Overview

abcdesktop.io is built on the Model-View-Controller (MVC) design pattern. MVC decouples the internal representation of data from how that data is presented to and accepted from the user, enabling a clean separation of concerns across the `pyos` control plane.

## Controller Reference

The following table lists all `pyos` controllers and their responsibilities:

| Controller | Description |
|---|---|
| `AccountingController` | Exposes per-user accounting and session metrics in JSON format |
| `AuthController` | Handles all user authentication flows |
| `ComposerController` | Manages CRUD operations for core services — e.g., `createDesktop`, `createApplication` |
| `CoreController` | Returns system configuration data and user-facing messages |
| `ManagerController` | Provides management operations (e.g., adding or removing application images); used exclusively by the console service |
| `UserController` | Returns authenticated user profile information |

## Access Control Configuration

Controller access is configured in the `controllers` dictionary in the `od.config` file. Access can be restricted by source IP address (`permitip`) and/or API key (`apikey`).

```json
controllers : { 
	'AccountingController': { 
		'apikey': [ 'fPCdPNcCafec4lXm3M' ],
		'permitip': [ '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', 'fd00::/8', '169.254.0.0/16', '127.0.0.0/8' ] 
	},
	'ManagerController': { 
	   'database_acl': [ 'get', 'put', 'delete' ],
		'apikey': [ 'fQDbvjCafec4l', 'KzH23EZjCZSfsd9'],
		'permitip': [ '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16', 'fd00::/8', '169.254.0.0/16', '127.0.0.0/8' ] 
	},
	'AuthController' : 		{ 'permitip': None },
	'ComposerController' : { 'requestsallowed' : { 'getdesktopdescription': True } },
	'CoreController' : 		{ 'permitip': None },
	'UserController' : 		{ 'permitip': None }
} 
```

By default, `AccountingController` and `ManagerController` are restricted to source IP addresses from RFC 1918 private ranges ([RFC 1918](https://tools.ietf.org/html/rfc1918)) and the IPv6 Unique Local Address range ([RFC 4193](https://tools.ietf.org/html/rfc4193)). All other controllers are accessible without restriction by default.

### Access Control Filter Options

| Filter | Type | Description |
|---|---|---|
| `permitip` | list of CIDR strings | Restricts access to requests originating from the listed subnets. Set to `None` to disable IP filtering. Example: `['10.0.0.0/8', '172.16.0.0/12']` |
| `apikey` | list of strings | Restricts access to requests presenting a valid API key in the `X-API-Key` HTTP header. Set to `None` to disable API key filtering. Example: `['fPCdPSSj8gZri1Ncmg']` |

When a request is denied due to an IP source filter violation, the HTTP response is:

```json
{"status": 403, "status_message": "403 Forbidden", "message": "Request forbidden -- authorization will not help"} 
```

## curl Request Examples

### Request with `X-API-Key` Header

List all registered application images:

```bash
curl -X GET -H 'X-API-Key: fQDbvjCafec4l' -H 'Content-Type: text/javascript' http://localhost:30443/API/manager/images
```

Expected response:

```json
{}
```

Register a new application image:

```bash
curl -X POST -H 'X-API-Key: fQDbvjCafec4l'  -H 'Content-Type: text/javascript' http://localhost:30443/API/manager/image -d@xeyes.d.{{ abcdesktop.latest_release }}.json
```

Expected response:

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
 	"displayname": "xeyes"
 }
]
```

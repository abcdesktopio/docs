---
title: Spawner service v1.0.0
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
highlight_theme: darkula
headingLevel: 2

---

<!-- Generator: Widdershins v4.0.1 -->

<h1 id="spawner-service">Spawner service v1.0.0</h1>

> Scroll down for code samples, example requests and responses. Select a language for code samples from the tabs above or the mobile navigation menu.

A sample API

Base URLs:

* <a href="/">/</a>

<h1 id="spawner-service-default">Default</h1>

## get__version

`GET /version`

Get User container version

> Example responses

> 200 Response

```json
{
  "date": null,
  "commit": "string",
  "version": "string"
}
```

<h3 id="get__version-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<h3 id="get__version-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» date|Date|false|none|none|
|» commit|string|false|none|none|
|» version|string|false|none|none|

Status Code **404**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer|false|none|none|
|» data|string|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## post__launch

`POST /launch`

Used to run builtin application process

> Body parameter

```json
{
  "command": "string",
  "args": [
    "string"
  ]
}
```

<h3 id="post__launch-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|false|none|
|» command|body|string|true|none|
|» args|body|[string]|false|none|

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": {}
}
```

<h3 id="post__launch-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[launch](#schemalaunch)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## post__setAudioQuality

`POST /setAudioQuality`

Set the audio quality

> Body parameter

```json
{
  "sink": "string"
}
```

<h3 id="post__setaudioquality-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|false|none|
|» sink|body|string|true|none|

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": {}
}
```

<h3 id="post__setaudioquality-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[processResult](#schemaprocessresult)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## post__playAudioSample

`POST /playAudioSample`

Play a sample audio

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": {}
}
```

<h3 id="post__playaudiosample-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[processResult](#schemaprocessresult)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## put__configurePulse

`PUT /configurePulse`

Configure pulse audio for Janus

> Body parameter

```json
{
  "destinationIp": "string",
  "port": "string"
}
```

<h3 id="put__configurepulse-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|false|none|
|» destinationIp|body|string|true|none|
|» port|body|string|true|none|

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": "string"
}
```

<h3 id="put__configurepulse-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Success](#schemasuccess)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## post__broadcastwindowslist

`POST /broadcastwindowslist`

Emit a broadcast with window list as data

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": "string"
}
```

<h3 id="post__broadcastwindowslist-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Success](#schemasuccess)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## post__clipboardsync

`POST /clipboardsync`

Synchronize X11 and gtk clipboard

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": "string"
}
```

<h3 id="post__clipboardsync-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Success](#schemasuccess)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## post__setDesktop

`POST /setDesktop`

Store a data as json file in desktop

> Body parameter

```json
{
  "key": "string",
  "value": "string"
}
```

<h3 id="post__setdesktop-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|false|none|
|» key|body|string|true|none|
|» value|body|string|true|none|

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": "string"
}
```

<h3 id="post__setdesktop-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Success](#schemasuccess)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## get__getDesktop

`GET /getDesktop`

Get a data stored as json file

<h3 id="get__getdesktop-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|key|query|string|true|none|

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": {}
}
```

<h3 id="get__getdesktop-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<h3 id="get__getdesktop-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer|false|none|none|
|» data|object|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## get__getmimeforfile

`GET /getmimeforfile`

Get a mime for a given filename

<h3 id="get__getmimeforfile-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|filename|query|string|true|none|

> Example responses

> 200 Response

```json
{
  "data": {}
}
```

<h3 id="get__getmimeforfile-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[MIME](#schemamime)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## get__filesearch

`GET /filesearch`

Used for list files by dock

<h3 id="get__filesearch-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|maxfile|query|integer|false|none|
|keywords|query|string|true|none|

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": [
    {
      "file": "string",
      "mime": "string"
    }
  ]
}
```

<h3 id="get__filesearch-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<h3 id="get__filesearch-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer|false|none|none|
|» data|[object]|false|none|none|
|»» file|string|false|none|none|
|»» mime|string|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## post__generateDesktopFiles

`POST /generateDesktopFiles`

Build desktop files to run containerized applications

> Body parameter

```json
{
  "list": [
    {
      "mimetype": "string",
      "path": "string",
      "executablefilename": "string",
      "icon": "string",
      "name": "string",
      "launch": "string"
    }
  ]
}
```

<h3 id="post__generatedesktopfiles-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|false|none|
|» list|body|[object]|true|none|
|»» mimetype|body|string|false|none|
|»» path|body|string|false|none|
|»» executablefilename|body|string|false|none|
|»» icon|body|string|false|none|
|»» name|body|string|false|none|
|»» launch|body|string|false|none|

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": "string"
}
```

<h3 id="post__generatedesktopfiles-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Success](#schemasuccess)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## get__getappforfile

`GET /getappforfile`

Allow to get the app necessary

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": [
    {
      "command": "string",
      "args": "string"
    }
  ]
}
```

<h3 id="get__getappforfile-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[AppForFile](#schemaappforfile)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## get__about

`GET /about`

Get system informations

> Example responses

> 200 Response

```json
{
  "hostname": "string",
  "ipaddr": "string",
  "plateform": "string",
  "arch": "string",
  "release": "string",
  "cpu": "string",
  "clientipaddr": "string",
  "country": "string",
  "language": "string",
  "build": "string",
  "POD_NAMESPACE": "string",
  "POD_NAME": "string",
  "NODE_NAME": "string",
  "POD_IP": "string",
  "KUBERNETES_SERVICE_HOST": "string"
}
```

<h3 id="get__about-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<h3 id="get__about-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» hostname|string|false|none|none|
|» ipaddr|string|false|none|none|
|» plateform|string|false|none|none|
|» arch|string|false|none|none|
|» release|string|false|none|none|
|» cpu|string|false|none|none|
|» clientipaddr|string|false|none|none|
|» country|string|false|none|none|
|» language|string|false|none|none|
|» build|string|false|none|none|
|» POD_NAMESPACE|string|false|none|none|
|» POD_NAME|string|false|none|none|
|» NODE_NAME|string|false|none|none|
|» POD_IP|string|false|none|none|
|» KUBERNETES_SERVICE_HOST|string|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## get__getSettings

`GET /getSettings`

Get configuration for settings window

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": [
    {
      "tab": "string",
      "enabled": true
    }
  ]
}
```

<h3 id="get__getsettings-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<h3 id="get__getsettings-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer|false|none|none|
|» data|[any]|false|none|none|
|»» tab|string|false|none|none|
|»» enabled|boolean|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## post__setBackgroundColor

`POST /setBackgroundColor`

Change the background color

> Body parameter

```json
{
  "color": "string"
}
```

<h3 id="post__setbackgroundcolor-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|false|none|
|» color|body|string|true|none|

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": "string"
}
```

<h3 id="post__setbackgroundcolor-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Success](#schemasuccess)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## post__setBackgroundImage

`POST /setBackgroundImage`

Set the background image

> Body parameter

```json
{
  "imgName": "string"
}
```

<h3 id="post__setbackgroundimage-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|false|none|
|» imgName|body|string|true|none|

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": {
    "color": "string",
    "subData": {
      "code": 0,
      "data": "string"
    }
  }
}
```

<h3 id="post__setbackgroundimage-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<h3 id="post__setbackgroundimage-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer|false|none|none|
|» data|object|false|none|none|
|»» color|string|false|none|none|
|»» subData|[Success](#schemasuccess)|false|none|All operations completed with success|
|»»» code|integer|false|none|none|
|»»» data|string|false|none|none|

Status Code **404**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer|false|none|none|
|» data|string|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## post__setDefaultImage

`POST /setDefaultImage`

Set the default image as background

> Example responses

> 200 Response

<h3 id="post__setdefaultimage-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|404|[Not Found](https://tools.ietf.org/html/rfc7231#section-6.5.4)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<h3 id="post__setdefaultimage-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer|false|none|none|
|» data|string|false|none|none|

Status Code **404**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer|false|none|none|
|» data|string|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## get__getwindowslist

`GET /getwindowslist`

Get window list

> Example responses

> 200 Response

<h3 id="get__getwindowslist-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<h3 id="get__getwindowslist-responseschema">Response Schema</h3>

Status Code **200**

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|» code|integer|false|none|none|
|» data|[any]|false|none|none|
|»» id|integer|false|none|none|
|»» pid|integer|false|none|none|
|»» wm_class|string|false|none|none|
|»» title|string|false|none|none|
|»» machine_name|string|false|none|none|

<aside class="success">
This operation does not require authentication
</aside>

## post__activatewindows

`POST /activatewindows`

Activate windows

> Body parameter

```json
{
  "windowsid": [
    0
  ]
}
```

<h3 id="post__activatewindows-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|false|none|
|» windowsid|body|[integer]|true|none|

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": "string"
}
```

<h3 id="post__activatewindows-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Success](#schemasuccess)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## post__closewindows

`POST /closewindows`

Close windows

> Body parameter

```json
{
  "windowsid": [
    0
  ]
}
```

<h3 id="post__closewindows-parameters">Parameters</h3>

|Name|In|Type|Required|Description|
|---|---|---|---|---|
|body|body|object|false|none|
|» windowsid|body|[integer]|true|none|

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": "string"
}
```

<h3 id="post__closewindows-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Success](#schemasuccess)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

## post__placeAllWindows

`POST /placeAllWindows`

Place and resize all windows

> Example responses

> 200 Response

```json
{
  "code": 0,
  "data": "string"
}
```

<h3 id="post__placeallwindows-responses">Responses</h3>

|Status|Meaning|Description|Schema|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[Success](#schemasuccess)|
|500|[Internal Server Error](https://tools.ietf.org/html/rfc7231#section-6.6.1)|none|[InternalError](#schemainternalerror)|

<aside class="success">
This operation does not require authentication
</aside>

# Schemas

<h2 id="tocS_InternalError">InternalError</h2>
<!-- backwards compatibility -->
<a id="schemainternalerror"></a>
<a id="schema_InternalError"></a>
<a id="tocSinternalerror"></a>
<a id="tocsinternalerror"></a>

```json
{
  "code": 0,
  "data": "string"
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|code|integer|false|none|none|
|data|string|false|none|none|

<h2 id="tocS_Success">Success</h2>
<!-- backwards compatibility -->
<a id="schemasuccess"></a>
<a id="schema_Success"></a>
<a id="tocSsuccess"></a>
<a id="tocssuccess"></a>

```json
{
  "code": 0,
  "data": "string"
}

```

All operations completed with success

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|code|integer|false|none|none|
|data|string|false|none|none|

<h2 id="tocS_processResult">processResult</h2>
<!-- backwards compatibility -->
<a id="schemaprocessresult"></a>
<a id="schema_processResult"></a>
<a id="tocSprocessresult"></a>
<a id="tocsprocessresult"></a>

```json
{
  "code": 0,
  "data": {}
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|code|integer|false|none|none|
|data|object|false|none|none|

<h2 id="tocS_launch">launch</h2>
<!-- backwards compatibility -->
<a id="schemalaunch"></a>
<a id="schema_launch"></a>
<a id="tocSlaunch"></a>
<a id="tocslaunch"></a>

```json
{
  "code": 0,
  "data": {}
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|code|integer|false|none|none|
|data|object|false|none|none|

<h2 id="tocS_MIME">MIME</h2>
<!-- backwards compatibility -->
<a id="schemamime"></a>
<a id="schema_MIME"></a>
<a id="tocSmime"></a>
<a id="tocsmime"></a>

```json
{
  "data": {}
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|data|object|false|none|none|

<h2 id="tocS_AppForFile">AppForFile</h2>
<!-- backwards compatibility -->
<a id="schemaappforfile"></a>
<a id="schema_AppForFile"></a>
<a id="tocSappforfile"></a>
<a id="tocsappforfile"></a>

```json
{
  "code": 0,
  "data": [
    {
      "command": "string",
      "args": "string"
    }
  ]
}

```

### Properties

|Name|Type|Required|Restrictions|Description|
|---|---|---|---|---|
|code|integer|false|none|none|
|data|[object]|false|none|none|
|» command|string|false|none|none|
|» args|string|false|none|none|


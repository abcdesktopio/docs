---
title: Welcome Information & JavaScript Injection | abcdesktop.io
description: Configure the abcdesktop.io welcomeinfo parameter to display custom messages and inject JavaScript — including Google Tag Manager — on the login page.
keywords: welcome, welcomeinfo, login page, JavaScript, Google Tag Manager, GTM, message, abcdesktop, customization
tags:
  - config
  - configuration
  - customization
---

# Welcome

## welcomeinfo

### Description

`welcomeinfo` allows you to display informational messages on the login page.

```json
welcomeinfo: { 'welcome': [] }
```


`welcomeinfo.welcome` is a list of dictionaries, each supporting the following fields:

- `notbefore`: date time
- `notafter`: date time
- `script` (optional) `{ 'async': boolean, 'src': uri }` or `{ 'data' : 'javascript code' } `
- `title` and `information` (optional)

### Example

```json
# welcomeinfo
# Show a welcome message to the login page
welcomeinfo: {
  'welcome': [
   { 'notbefore': '01 Dec 2023 00:00:00 GMT',
      'notafter':  '01 Dec 2026 00:12:00 GMT',
       'title': 'maintenance mode sample A',
       'information': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    },
    { 'notbefore': '03 Dec 2023 22:12:00 GMT',
      'notafter':  '04 Dec 2026 00:12:00 GMT',
      'title': 'maintenance mode sample B',
      'information': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
    } ] }
```


The login page displays the configured messages:

![welcome info sample](img/welcomeinfosample.png)


### Script

`welcomeinfo` can also load JavaScript source code from an external URI or from an inline string. The JavaScript code is injected directly into the abcdesktop login page.

#### `data`

```json
welcomeinfo: {
  'welcome': [
    {
      'notbefore': '01 Dec 2023 00:00:00 GMT',
      'notafter':  '01 Dec 2026 00:12:00 GMT',
      'script': {
        'data': 'console.log(\'hello from welcomeinfo \');'
      }
    },
    { 'notbefore': '01 Dec 2023 00:00:00 GMT',
      'notafter':  '01 Dec 2026 00:12:00 GMT',
       'title': 'maintenance mode sample A',
       'information': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    },
    { 'notbefore': '03 Dec 2023 22:12:00 GMT',
      'notafter':  '04 Dec 2026 00:12:00 GMT',
      'title': 'maintenance mode sample B',
      'information': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
    } ] }
```


In the browser's developer console, you can observe the following output:

![welcomeinfo console log](img/welcomeinfolog.png)

#### `src` and `async`

The `script` field also supports `src` and `async` properties for loading an external URI either synchronously or asynchronously.

The following example loads the Google Tag Manager script from `https://www.googletagmanager.com/gtag/js?id=G-VS25TGNTRZ` with `async` set to `False`, and then executes the following inline JavaScript:

```json
      window.dataLayer = window.dataLayer || [];\
      function gtag(){dataLayer.push(arguments);}\
      gtag(\'js\', new Date());\
      gtag(\'config\', \'G-VS25TGNTRZ\');
```

The following is a complete example that embeds Google Tag Manager:

```json
welcomeinfo: {
  'welcome': [
    { 'notbefore': '04 Dec 2023 00:12:00 GMT',
      'notafter':  '08 Dec 2026 00:12:00 GMT',
      'script' : {
        'async': False,
        'src': 'https://www.googletagmanager.com/gtag/js?id=G-VS25TGNTRZ'
      }
    },
    {
      'notbefore': '01 Dec 2023 00:00:00 GMT',
      'notafter':  '01 Dec 2026 00:12:00 GMT',
      'script': {
        'data': '\
          window.dataLayer = window.dataLayer || [];\
          function gtag(){dataLayer.push(arguments);}\
          gtag(\'js\', new Date());\
          gtag(\'config\', \'G-VS25TGNTRZ\');'
      }
    },
    { 'notbefore': '01 Dec 2023 00:00:00 GMT',
      'notafter':  '01 Dec 2026 00:12:00 GMT',
       'title': 'maintenance mode',
       'information': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    },
    { 'notbefore': '03 Dec 2023 22:12:00 GMT',
      'notafter':  '04 Dec 2026 00:12:00 GMT',
      'title': 'maintenance mode',
      'information': 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
    } ] }
```
In the browser's network panel, you can observe the HTTP fetch request sent to `google-analytics.com`.

![google analytics](img/welcomeinfogoogle.png)

You have now configured `welcomeinfo` messages to display maintenance notifications and optionally inject JavaScript source code into the abcdesktop login page.

---
title: Disable Outbound Firefox Connections | abcdesktop.io
description: Configure Firefox policies to disable telemetry, Normandy, and other background network connections in an abcdesktop.io Remote Browser Isolation deployment.
keywords: Firefox, disable connections, policies, telemetry, Normandy, RBI, remote browser isolation, abcdesktop, privacy
tags:
  - FAQ
  - Firefox
  - RBI
  - security
  - privacy
- firefox
---

# How to Disable Mozilla Firefox Automatic Connections at Startup

## Usage of policies.json

You can specify Firefox policies in a file called `policies.json`. You may need to create this file, as it is not present by default.

Path to `policies.json` depending on your OS (you may need to create intermediate directories):

* Windows: `C:\Program Files\Mozilla Firefox\distribution\policies.json`
* Linux: `/usr/lib/firefox/distribution/policies.json`
* macOS: `/Applications/Firefox.app/Contents/Resources/distribution/policies.json`

You can find all policy templates for your Firefox version on the Mozilla GitHub page: [https://github.com/mozilla/policy-templates/releases](https://github.com/mozilla/policy-templates/releases)

## Usage of autoconfig.js and firefox.cfg

Some preferences cannot be set through the `policies.json` file — for example, disabling Normandy — due to Firefox restrictions. These can instead be configured by creating a JavaScript file called `autoconfig.js` and a configuration file called `firefox.cfg`.

`autoconfig.js` is responsible for loading and executing `firefox.cfg` at startup.

### autoconfig.js

```JS
// Setup config file
pref("general.config.filename", "firefox.cfg");
pref("general.config.obscure_value", 0);
```

Path to `autoconfig.js` depending on your OS (you may need to create intermediate directories):

* Windows: `C:\Program Files\Mozilla Firefox\defaults\pref\autoconfig.js`
* Linux: `/usr/lib/firefox/defaults/pref/autoconfig.js`
* macOS: `/Applications/Firefox.app/Contents/Resources/defaults/pref/autoconfig.js`

Locked preferences are specified in the `firefox.cfg` file. Path to `firefox.cfg` depending on your OS:

* Windows: `C:\Program Files\Mozilla Firefox\firefox.cfg`
* Linux: `/usr/lib/firefox/firefox.cfg`
* macOS: `/Applications/Firefox.app/Contents/Resources/firefox.cfg`

## Usage of proxy.pac file

Despite all efforts to disable automatic connections via `policies.json` and `firefox.cfg`, a small number of connections may remain that cannot be disabled through policy settings alone. To work around this behavior, create a file named `proxy.pac` that blocks access to the remaining URLs by redirecting them to an unreachable proxy.

Save `proxy.pac` to your machine and note the file path.

Once saved, add the following line to the `Proxy` policy inside your `policies.json` file:
`"AutoConfigURL": "file:///path/to/your/proxy.pac"`

## Disable Startup Connections

### policies.json

| URL                            | Parameter(s) to set |
| ------------------------------ | ---------------- |
| `https://location.services.mozilla.com` | `"browser.region.network.url": ""` |
| `https://contile.services.mozilla.com`<br>`https://tiles-cdn.prod.ads.prod.webservices.mozgcp.net` | `"browser.topsites.contile.enabled": false`<br>`"browser.topsites.contile.endpoint": ""` |
| `https://spocs.getpocket.com` | `"browser.newtabpage.activity-stream.discoverystream.enabled": false` |
| `https://push.services.mozilla.com` | `"dom.push.connection.enabled": false` |
| `https://accounts.firefox.com` | `"browser.startup.homepage_override.mstone": "ignore"`<br>(also disables the news page) |
| `https://shavar.services.mozilla.com` | `"browser.safebrowsing.provider.mozilla.gethashURL": ""`<br>`"browser.safebrowsing.provider.mozilla.updateURL": ""` |
| `https://tracking-protection.cdn.mozilla.net` | `"browser.safebrowsing.downloads.remote.enabled": false` |
| `http://detectportal.firefox.com` | `"network.captive-portal-service.enabled": false`<br>`"network.connectivity-service.enabled": false` |
| `https://incoming.telemetry.mozilla.org`<br>`https://www.mozilla.org` | Set `"DisableTelemetry"` policy to `true` |

### firefox.cfg

| URL                            | Parameter(s) to set |
| ------------------------------ | ------------------------- |
| `https://normandy.cdn.mozilla.net`<br>`https://classify-client.services.mozilla.com` | `lockPref("app.normandy.enabled", false)`<br>`lockPref("app.normandy.api_url", "")` |

### Example of policies.json file

```JSON
"policies": {
    "DisableTelemetry": true,
    "Preferences": {
        "browser.region.network.url": "",
        "browser.topsites.contile.endpoint": "",
        "browser.newtabpage.activity-stream.discoverystream.enabled": false,
        "browser.startup.homepage_override.mstone": "ignore",
        "browser.safebrowsing.provider.mozilla.gethashURL": "",
        "browser.safebrowsing.provider.mozilla.updateURL": "",
        "browser.safebrowsing.downloads.remote.enabled": false,
        "dom.push.connection.enabled": false,
        "network.captive-portal-service.enabled": false,
        "network.connectivity-service.enabled": false
    },
    "Proxy": {
        "Mode": "autoConfig",
        "AutoConfigURL": "file:///path/to/your/proxy.pac"
    }
}
```

### Example of firefox.cfg file

```
// Disable Normandy service
lockPref("app.normandy.enabled", false);
lockPref("app.normandy.api_url", "");
```

### Example of proxy.pac file

```
// File PAC
//
function FindProxyForURL(url, host)
{
  // just define hostname and unreachable port
  var var_blackhole = "127.0.0.1:12345"; // could be any other UNUSED port than 12345

  //URL deny definition - Blackhole for blocked URL

  if ( host == "firefox.settings.services.mozilla.com"
    || host == "content-signature-2.cdn.mozilla.net"
    || host == "firefox-settings-attachments.cdn.mozilla.net"
  ) {
    return "PROXY " + var_blackhole;
  }

  return  "DIRECT; ";
}
```
## Sources

- [How to stop Firefox from making automatic connections](https://support.mozilla.org/en-US/kb/how-stop-firefox-making-automatic-connections)
- [nikitastupin/stop-firefox-automatic-connections](https://github.com/nikitastupin/stop-firefox-automatic-connections)
- [Silencing Firefox's Chattiness for Web App Testing](https://www.secureideas.com/blog/2018/10/silencing-firefoxs-chattiness-for-web-app-testing.html)
- [Customizing Firefox Using AutoConfig](https://support.mozilla.org/en-US/kb/customizing-firefox-using-autoconfig)
- [Firefox Reddit](https://www.reddit.com/r/firefox/)
- [Mozilla support forums](https://support.mozilla.org/en-US/questions/)

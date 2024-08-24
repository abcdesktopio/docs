# How to disable Mozilla Firefox automatic connections at startup 

## Usage of policies.json

You can specifiy firefox policies in a file called `policies.json`, you may have to create it as it is noy present by default.

Path to `policies.json` depending on your OS (you may have to create directories of the paths):

Windows : `C:\Program Files\Mozilla Firefox\distribution\policies.json`  
Linux : `/usr/lib/firefox/distribution/policies.json`  
MacOS : `/Applications/Firefox.app/Contents/Resources/distribution/policies.json`

You can find all the policies templates, according to your firefox version, on the mozilla github page : https://github.com/mozilla/policy-templates/releases 

## Usage of autoconfig.js and firefox.cfg 

Some preferences cannot be set through the `policies.json` file, such as disable normandy, because of firefox restrictions. But we can bypass it by creating a JS file called `autoconfig.js` and a config file called `firefox.cfg`. 

`autoconfig.js` is used to load and execute `firefox.cfg`.  

### autoconfig.js

```JS
// Setup config file
pref("general.config.filename", "firefox.cfg");
pref("general.config.obscure_value", 0);
```

Path to `autoconfig.js` depending on your OS (you may have to create directories of the paths):  

Windows : `C:\Program Files\Mozilla Firefox\defaults\pref\autoconfig.js`  
Linux : `/usr/lib/firefox/defaults/pref/autoconfig.js`  
MacOS : `/Applications/Firefox.app/Contents/Resources/defaults/pref/autoconfig.js`

The locked preferences are specified in the `firefox.cfg` file.  
Path to `firefox.cfg` depending on your OS (you may have to create directories of the paths):  

Windows : `C:\Program Files\Mozilla Firefox\firefox.cfg`  
Linux : `/usr/lib/firefox/firefox.cfg`  
MacOS : `/Applications/Firefox.app/Contents/Resources/firefox.cfg`

## Usage of proxy.pac file

Despite all the efforts to disable automatic connections via `policies.json` and `firefox.cfg` files, there where still a few connections that seems to be not possible to disable.  
To bypass this phenomena, we will create a file named `proxy.pac` that will block access to the remaining URLs by redirecting them to an unreachable proxy. 

Save `proxy.pac` on your machine and keep in mind the path to your file. 

Once done, you should add the following line to the `Proxy` policy inside your `policies.json` file :  
`"AutoConfigURL": "file:///path/to/your/proxy.pac"`

## Disable startup connections

### policies.json

| URL                            | Parameter(s) to set |
| ------------------------------ | ---------------- |
| `https://location.services.mozilla.com` | `"browser.region.network.url": ""` |
| `https://contile.services.mozilla.com`<br>`https://tiles-cdn.prod.ads.prod.webservices.mozgcp.net` | `"browser.topsites.contile.enabled": false`<br>`"browser.topsites.contile.endpoint": ""` |
| `https://spocs.getpocket.com` | `"browser.newtabpage.activity-stream.discoverystream.enabled": false` |
| `https://push.services.mozilla.com` | `"dom.push.connection.enabled": false` |
| `https://accounts.firefox.com` | `"browser.startup.homepage_override.mstone": "ignore"`<br>(also disable news page) |
| `https://shavar.services.mozilla.com` | `"browser.safebrowsing.provider.mozilla.gethashURL": ""`<br>`"browser.safebrowsing.provider.mozilla.updateURL": ""` |
| `https://tracking-protection.cdn.mozilla.net` | `"browser.safebrowsing.downloads.remote.enabled": false` |
| `http://detectportal.firefox.com` | `"network.captive-portal-service.enabled": false`<br>`"network.connectivity-service.enabled": false` |
| `https://incoming.telemetry.mozilla.org`<br>`https://www.mozilla.org` | Set `"DisableTelemetry"` policy to true |

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

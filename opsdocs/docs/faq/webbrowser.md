---
tags:
  - faq
  - browser
---

# FAQ Web Browser


## How to change the default language ?

abcdesktop reads the your web browser language and starts application and desktop this user's choose.
The default installed languages are `English`, `French`, 'German`, and `Romanian`. If you need other languages support you have to rebuild the container image with your language.

## Which web browser is supported ?

abcdesktop.io uses many modern web technologies. However these are the minimum versions we are currently aware of:

* Chrome 49, 
* Firefox 58, 
* Safari 11, 
* Opera 36,  
* Microsoft Edge (based on Chromium)


## How to do a `copy and paste` ?

To fully use `copy and paste` features, from your local device to your abcdesktop (and vice versa), choose `Chrome`, `Chromium` or  `Microsoft Edge Chromium`. The `copy and paste` feature is also supported on Firefox with a [dedicated abcdesktop extension](firefox-extension.md).

| Web browser      | Clipboard sync                 |
|------------------|-------------------------------------|
|  Chrome     | Yes, built in support |
|  Chromium     | Yes, built in support  |
|  Microsoft Edge Chromium     | Yes, built in support  |
|  Firefox       | Yes, install the [dedicated abcdesktop extension](/common/firefox-extension)| 
|  Safari       | No, the clipboard access is not allowed by the user agent or the platform in the current context, possibly because the user denied permission|

> Make sure to use `https` protocol to allow read and write api calls to your clipboard
 

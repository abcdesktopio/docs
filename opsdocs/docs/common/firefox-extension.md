

# Mozilla Firefox clipboard extension

## Install the Firefox Extension

### Download the Mozilla Firefox clipboard extension for abcdesktop

1. Download the Firefox clipboard extension [abcdesktop_clipboard_helper.xpi](https://www.abcdesktop.io/abcdesktop_clipboard_helper-1.0.3-fx.xpi) and press the `Continue to Installation` button.
![Download and continue](img/allow-install-add-on.png)

2. Choose `Add` in response to the prompt `Add abcdesktop Clipboard Helper?`
![confirm to add ons](img/add-install-firefox-about-add-ons.png)

3. Press `OKay, Got it` to confirm the `abcdesktop Clipboard Helper` installation
![OKay confirm install add ons](img/ok-add-install-firefox-about-add-ons.png)




## Use fully qualified domain name filter

The Firefox clipboard extension is active **only when the URL hostname contains the string `desktop`**.

The URL must match `*://*desktop*/*"` to activate the clipboard extension.

* `https://demo.abcdesktop.io` matches; the Firefox clipboard extension is active.
* `https://desktop.domain.io` matches; the Firefox clipboard extension is active.
* `https://abcdesktop.mydomain.local` matches; the Firefox clipboard extension is active.
* `https://demo.domain.com` does not match; the Firefox clipboard extension is not active.


## Run the Firefox clipboard extension for abcdesktop

> The Firefox clipboard extension syncs **only text data**; binary data such as images is not yet supported.

* The Firefox clipboard extension syncs clipboard data selected within your abcdesktop desktop session to your local desktop environment.

* The Firefox clipboard extension syncs your local desktop environment clipboard to your abcdesktop desktop clipboard.

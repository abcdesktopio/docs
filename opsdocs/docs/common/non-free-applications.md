# Install non-free applications


## Install and build `Citrix Receiver` for abcdesktop

`Citrix Workspace App` or `Citrix Receiver` does not exist in official debian repository. You need to download the `deb package` from the www.citrix.com website manually.


* Clone the abcdesktopio/oc.apps repository
```
git clone https://github.com/abcdesktopio/oc.apps.git
```

* Download the Citrix Receiver for Linux .deb package. Go to [https://www.citrix.com/downloads/citrix-receiver/linux/receiver-for-linux-latest.html](https://www.citrix.com/downloads/citrix-receiver/linux/receiver-for-linux-latest.html)

* Copy the downloaded file `icaclient_13.10.0.20_amd64.deb` for example as **icaclient_amd64.deb** to your local oc.apps directory
```
cd oc.apps
cp ~/Download/icaclient_13.10.0.20_amd64.deb icaclient_amd64.deb 
```
* Run docker build command

```
docker build  --build-arg TAG=dev -t abcdesktopio/citrix.d:dev -f 
```

```
Sending build context to Docker daemon  29.13MB
Step 1/28 : ARG TAG=dev
Step 2/28 : FROM abcdesktopio/oc.template.gtk.18.04:$TAG
 ---> c66ccd2edc52
Step 3/28 : COPY icaclient_amd64.deb /tmp/icaclient_amd64.deb
 ---> Using cache
 ---> de6a2bcaa7c0
Step 4/28 : RUN apt-get install  --no-install-recommends --yes /tmp/icaclient_amd64.deb && apt-get clean && rm /tmp/icaclient_amd64.deb
 ---> Using cache
 ---> 87e1ce530e44
Step 5/28 : ENV BUSER balloon
 ---> Using cache
 ---> e4f474a17688
Step 6/28 : LABEL oc.icon="icaclient.svg"
 ---> Using cache
 ---> c6b12ecd898c
Step 7/28 : LABEL oc.icondata="PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2NCIgaGVpZ2h0PSI2NCIgdmVyc2lvbj0iMSI+CiA8cmVjdCBzdHlsZT0ib3BhY2l0eTouMiIgd2lkdGg9IjU2IiBoZWlnaHQ9IjU2IiB4PSItNTkiIHk9Ii02MCIgcng9IjI4IiByeT0iMjgiIHRyYW5zZm9ybT0ibWF0cml4KDAsLTEsLTEsMCwwLDApIi8+CiA8cmVjdCBzdHlsZT0iZmlsbDojNGY0ZjRmIiB3aWR0aD0iNTYiIGhlaWdodD0iNTYiIHg9Ii01OCIgeT0iLTYwIiByeD0iMjgiIHJ5PSIyOCIgdHJhbnNmb3JtPSJtYXRyaXgoMCwtMSwtMSwwLDAsMCkiLz4KIDxwYXRoIHN0eWxlPSJvcGFjaXR5Oi4yIiBkPSJtMzIgMTFhMiAyIDAgMCAwIC0wLjE5MTQgMC4wMTE3MmMtMTAuOTMzMjI0IDAuMTA0NTM5LTE5LjgwODYgOS4wMzA5Ny0xOS44MDg2IDE5Ljk4ODI4IDAgMTEuMDIyMDA2IDguOTc3OTk0IDIwIDIwIDIwIDEwLjk1NDY3OCAwIDE5Ljg3OTUyNC04Ljg3MTE4IDE5Ljk4ODI4Mi0xOS44MDA3ODJhMiAyIDAgMCAwIDAuMDExNzE4IC0wLjE5OTIxOCAyIDIgMCAwIDAgLTIgLTIgMiAyIDAgMCAwIC0yIDJjMCA4Ljg2MDI0Ni03LjEzOTc1NCAxNi0xNiAxNnMtMTYtNy4xMzk3NTQtMTYtMTYgNy4xMzk3NTQtMTYgMTYtMTZhMiAyIDAgMCAwIDIgLTIgMiAyIDAgMCAwIC0yIC0yem0wIDhhMiAyIDAgMCAwIC0wLjE5MTQgMC4wMDc4Yy02LjUxNTM3NCAwLjEwNDEyNi0xMS44MDg2IDUuNDUzMDUyLTExLjgwODYgMTEuOTkyMiAwIDYuNjAzNzI4IDUuMzk2MjcyIDEyIDEyIDEyIDYuNTM2NDUyIDAgMTEuODc5ODgtNS4yODkxMTIgMTEuOTg4MjgyLTExLjgwMDc4MmEyIDIgMCAwIDAgMC4wMTE3MTggLTAuMTk5MjE4IDIgMiAwIDAgMCAtMiAtMiAyIDIgMCAwIDAgLTIgMmMwIDQuNDQxOTY4LTMuNTU4MDMyIDgtOCA4cy04LTMuNTU4MDMyLTgtOCAzLjU1ODAzMi04IDgtOGEyIDIgMCAwIDAgMiAtMiAyIDIgMCAwIDAgLTIgLTJ6bTAgOGE0IDQgMCAwIDAgLTQgNCA0IDQgMCAwIDAgNCA0IDQgNCAwIDAgMCA0IC00IDQgNCAwIDAgMCAtNCAtNHoiLz4KIDxwYXRoIHN0eWxlPSJmaWxsOiNmZmZmZmYiIGQ9Im0zMiAxMGEyIDIgMCAwIDAgLTAuMTkxNCAwLjAxMTcyYy0xMC45MzMyMjQgMC4xMDQ1MzktMTkuODA4NiA5LjAzMDk3LTE5LjgwODYgMTkuOTg4MjggMCAxMS4wMjIwMDYgOC45Nzc5OTQgMjAgMjAgMjAgMTAuOTU0Njc4IDAgMTkuODc5NTI0LTguODcxMTggMTkuOTg4MjgyLTE5LjgwMDc4MmEyIDIgMCAwIDAgMC4wMTE3MTggLTAuMTk5MjE4IDIgMiAwIDAgMCAtMiAtMiAyIDIgMCAwIDAgLTIgMmMwIDguODYwMjQ2LTcuMTM5NzU0IDE2LTE2IDE2cy0xNi03LjEzOTc1NC0xNi0xNiA3LjEzOTc1NC0xNiAxNi0xNmEyIDIgMCAwIDAgMiAtMiAyIDIgMCAwIDAgLTIgLTJ6bTAgOGEyIDIgMCAwIDAgLTAuMTkxNCAwLjAwNzhjLTYuNTE1Mzc0IDAuMTA0MTI2LTExLjgwODYgNS40NTMwNTItMTEuODA4NiAxMS45OTIyIDAgNi42MDM3MjggNS4zOTYyNzIgMTIgMTIgMTIgNi41MzY0NTIgMCAxMS44Nzk4OC01LjI4OTExMiAxMS45ODgyODItMTEuODAwNzgyYTIgMiAwIDAgMCAwLjAxMTcxOCAtMC4xOTkyMTggMiAyIDAgMCAwIC0yIC0yIDIgMiAwIDAgMCAtMiAyYzAgNC40NDE5NjgtMy41NTgwMzIgOC04IDhzLTgtMy41NTgwMzItOC04IDMuNTU4MDMyLTggOC04YTIgMiAwIDAgMCAyIC0yIDIgMiAwIDAgMCAtMiAtMnptMCA4YTQgNCAwIDAgMCAtNCA0IDQgNCAwIDAgMCA0IDQgNCA0IDAgMCAwIDQgLTQgNCA0IDAgMCAwIC00IC00eiIvPgogPHBhdGggc3R5bGU9Im9wYWNpdHk6LjE7ZmlsbDojZmZmZmZmIiBkPSJtMzIgMmMtMTUuNTEyIDAtMjggMTIuNDg4LTI4IDI4IDAgMC4xMTM0NSAwLjAxMTI4MDUgMC4yMjQxMTMgMC4wMTc1NzgxIDAuMzM1OTM4IDAuMzUxNTQzMi0xNS4yMDE3NTcgMTIuNjkzMTQ5OS0yNy4zMzU5MzggMjcuOTgyNDIxOS0yNy4zMzU5MzhzMjcuNjMwODc5IDEyLjEzNDE4MSAyNy45ODI0MjIgMjcuMzM1OTM4YzAuMDA2Mjk4LTAuMTExODI1IDAuMDE3NTc4LTAuMjIyNDg4IDAuMDE3NTc4LTAuMzM1OTM4IDAtMTUuNTEyLTEyLjQ4OC0yOC0yOC0yOHoiLz4KPC9zdmc+Cg=="
 ---> Using cache
 ---> cb5821f26574
Step 8/28 : LABEL oc.keyword="ica,citrix,icaclient,"
 ---> Using cache
 ---> 841fc5293542
Step 9/28 : LABEL oc.cat="office"
 ---> Using cache
 ---> b02b64fab112
Step 10/28 : LABEL oc.desktopfile="wfica.desktop"
 ---> Using cache
 ---> d8929c453992
Step 11/28 : LABEL oc.launch="Wfica.Wfica"
 ---> Using cache
 ---> 3c0001542ee6
Step 12/28 : LABEL oc.template="abcdesktopio/oc.template.gtk.18.04"
 ---> Using cache
 ---> c48014944a74
Step 13/28 : ENV ARGS="-icaroot /opt/Citrix/ICAClient"
 ---> Using cache
 ---> d242eb681417
Step 14/28 : LABEL oc.name="citrix"
 ---> Using cache
 ---> fee77a4b23d6
Step 15/28 : LABEL oc.displayname="citrix-client"
 ---> Using cache
 ---> 1fb6f9642a9f
Step 16/28 : LABEL oc.path="/opt/Citrix/ICAClient/wfica"
 ---> Using cache
 ---> 0cba59460d1a
Step 17/28 : LABEL oc.type=app
 ---> Using cache
 ---> a14be19dc259
Step 18/28 : LABEL oc.showinview="dock"
 ---> Using cache
 ---> 9ee26ab86b1d
Step 19/28 : LABEL oc.mimetype="application/x-ica;"
 ---> Using cache
 ---> 5536706365ef
Step 20/28 : RUN  if [ -d /usr/share/icons ];   then cd /usr/share/icons;    /composer/safelinks.sh; fi
 ---> Using cache
 ---> 49a06d7adf22
Step 21/28 : RUN  if [ -d /usr/share/pixmaps ]; then cd /usr/share/pixmaps;  /composer/safelinks.sh; fi
 ---> Using cache
 ---> 5090828ce15e
Step 22/28 : WORKDIR /home/balloon
 ---> Using cache
 ---> ac6821413e1f
Step 23/28 : USER balloon
 ---> Using cache
 ---> 7cbea5e541e8
Step 24/28 : ENV APPNAME "citrix"
 ---> Using cache
 ---> a6662e5e1ea4
Step 25/28 : ENV APPBIN "/opt/Citrix/ICAClient/wfica"
 ---> Using cache
 ---> 475f164cc974
Step 26/28 : LABEL oc.args="-icaroot /opt/Citrix/ICAClient"
 ---> Using cache
 ---> b085c5a7c97d
Step 27/28 : ENV APP "/opt/Citrix/ICAClient/wfica"
 ---> Using cache
 ---> 534994e86953
Step 28/28 : LABEL oc.usedefaultapplication=true
 ---> Using cache
 ---> 5cd6ea7a4228
Successfully built 5cd6ea7a4228
Successfully tagged abcdesktopio/citrix.d:dev
```

* The new ica citrix docker image `abcdesktopio/citrix.d:dev` is ready to run


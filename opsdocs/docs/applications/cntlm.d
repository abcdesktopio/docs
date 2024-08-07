# Dynamic DockerFile application file for abcdesktopio generated by abcdesktopio/oc.apps/make.js
# DO NOT EDIT THIS FILE BY HAND -- YOUR CHANGES WILL BE OVERWRITTEN
ARG TAG=dev
FROM abcdesktopio/oc.template.ubuntu.minimal.22.04:$TAG
USER root
COPY cntlm/cntlm.mustache  cntlm/init.cntlm.sh /composer/
COPY composer/init.d/init.gnome-terminal /composer/init.d/
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y  --no-install-recommends ruby-mustache gnome-terminal dbus-x11 cntlm net-tools vim curl wget && apt-get clean
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
LABEL oc.icon="cntlm.svg"
LABEL oc.icondata="PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pg0KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDE4LjAuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPg0KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4NCjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCINCgkgdmlld0JveD0iMCAwIDQ3MC4xMDcgNDcwLjEwNyIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgNDcwLjEwNyA0NzAuMTA3OyIgeG1sOnNwYWNlPSJwcmVzZXJ2ZSI+DQo8Zz4NCgk8cGF0aCBkPSJNNDIzLjQ4OSwxNjkuNzg1YzQuMzY0LTEyLjMzOCw2Ljg2My0yNS41NTUsNi44NjMtMzkuMzkxYzAtNjUuMzE2LTUyLjk1Ni0xMTguMjcyLTExOC4yNzItMTE4LjI3Mg0KCQljLTQ0LjQ0NSwwLTgzLjEyOSwyNC41NTMtMTAzLjMzMiw2MC43OTljLTE1LjM5LTkuNjc1LTMzLjU2LTE1LjM2LTUzLjA4LTE1LjM2Yy01NS4yMzksMC0xMDAuMDEsNDQuNzczLTEwMC4wMSwxMDAuMDAyDQoJCWMwLDMuODI4LDAuMjY0LDcuNTkzLDAuNjg0LDExLjMxM2gtMC42ODRDMjQuOTI1LDE2OC44NzUsMCwxOTMuNzkyLDAsMjI0LjUzM2MwLDMwLjc0LDI0LjkyNSw1NS42NTgsNTUuNjU4LDU1LjY1OGgyMC4yMDQNCgkJYy0yLjQwOC0zLjg2Ni0zLjc0Mi04LjI5OS0zLjc0Mi0xMi45NTljMC02LjU2MSwyLjU0Ni0xMi43NDIsNy4yMDUtMTcuNDE2bDE0LjA4NS0xNC4wN2w4LjMyNS04LjMyMw0KCQljNC42NDMtNC42MzUsMTAuODIzLTcuMTgzLDE3LjM5Mi03LjE4M2M2LjU2OSwwLDEyLjc2NSwyLjU1NiwxNy40MjQsNy4yMTNsMC4wNDYsMC4wNDh2LTAuMDdjMC0xMy41OCwxMS4wNDItMjQuNjMxLDI0LjYzMS0yNC42MzENCgkJaDMxLjYzM2MxMy41NzIsMCwyNC42MTUsMTEuMDUsMjQuNjE1LDI0LjYzMXYwLjA4NGwwLjA2Mi0wLjA2MmMxMS4wNjQtMTEuMDY0LDI2Ljk3Mi03Ljg5LDM0Ljg0OC0wLjAxNGwxMC4zMjcsMTAuMzI3DQoJCWwxMi4wMzUsMTIuMDM1YzQuNjU5LDQuNjUxLDcuMjIxLDEwLjgzOSw3LjIyMSwxNy40MjRjMCw0LjY3NS0xLjM1LDkuMTE1LTMuNzU4LDEyLjk2N2gzMy40MDQNCgkJYzIzLjAzLTM2LjA1Miw5MS40NjktNTIuNTA0LDExMC41MjMtNi42ODVjMC43NzYsMS44NjQsMC45MzIsMy44MzYsMS4xOCw1Ljc5M2MyNi40OTMtNC4yNzEsNDYuNzktMjcuMDYxLDQ2Ljc5LTU0Ljc2NQ0KCQlDNDcwLjEwNywxOTYuODkyLDQ0OS45MDQsMTc0LjEyNSw0MjMuNDg5LDE2OS43ODV6Ii8+DQoJPHBhdGggZD0iTTE0Ni4xOTUsMzcyLjExYy0xNS4yODItMTAuMDcxLTI1LjQwNy0yNy4zMzEtMjUuNDA3LTQ2Ljk1M2MwLTMxLjAyLDI1LjIzNS01Ni4yNTUsNTYuMjQ3LTU2LjI1NQ0KCQljMzEuMDI4LDAsNTYuMjYzLDI1LjIzNSw1Ni4yNjMsNTYuMjU1YzAsMy44MDQtMC40MDQsNy41MjMtMS4xMTgsMTEuMTE5bDUxLjMyNC0yMS40di01LjU0M2MwLTQuODIzLTMuOTEzLTguNzM3LTguNzI3LTguNzM3DQoJCWgtMTcuOTM2Yy0xLjU1NC01LjA1NC0zLjYwNC05Ljg5OS02LjA0MS0xNC40OTZsMTIuNzAzLTEyLjcwM2MxLjY0Ni0xLjYzOCwyLjU2Mi0zLjg1OSwyLjU2Mi02LjE3Mw0KCQljMC0yLjMxNC0wLjkxNi00LjUzNC0yLjU2Mi02LjE4MWwtMjIuMzYyLTIyLjM2MmMtMS43MS0xLjcwOC0zLjk0NS0yLjU1Ni02LjE4MS0yLjU1NmMtMi4yMzYsMC00LjQ1NywwLjg0OC02LjE2NSwyLjU1Ng0KCQlsLTEyLjcxOSwxMi43MTFjLTQuNTk3LTIuNDM4LTkuNDI3LTQuNDgtMTQuNTA0LTYuMDI1VjIyNy40M2MwLTQuODIzLTMuODk4LTguNzI5LTguNzEzLTguNzI5aC0zMS42MzMNCgkJYy00LjgxNSwwLTguNzI5LDMuOTA2LTguNzI5LDguNzI5djE3LjkzNmMtNS4wNjIsMS41NDYtOS45MDcsMy41ODgtMTQuNTA0LDYuMDI1bC0xMi42ODctMTIuNjk1DQoJCWMtMS43MDgtMS43MS0zLjk0NS0yLjU1Ni02LjE4MS0yLjU1NmMtMi4yMzYsMC00LjQ3MiwwLjg0Ni02LjE4MSwyLjU0OGwtMjIuMzc4LDIyLjM3Yy0xLjYzLDEuNjM4LTIuNTQ2LDMuODU5LTIuNTQ2LDYuMTczDQoJCWMwLDIuMzIyLDAuOTE2LDQuNTQyLDIuNTQ2LDYuMTgxbDEyLjcwMywxMi42OTVjLTIuNDM4LDQuNTk3LTQuNDcyLDkuNDM1LTYuMDI1LDE0LjQ4OEg3OS4zMDljLTQuODEzLDAtOC43MjcsMy45MTQtOC43MjcsOC43MzcNCgkJdjMxLjY0MWMwLDQuODE0LDMuOTE0LDguNzI3LDguNzI3LDguNzI3SDk3LjIzYzEuNTY4LDUuMDU1LDMuNjAyLDkuOTAxLDYuMDQsMTQuNDk4bC0xMi43MDMsMTIuNzAzDQoJCWMtMy40MDEsMy40LTMuNDAxLDguOTM3LDAsMTIuMzQ1bDcuNTE3LDcuNTA5YzQuMzMyLTQuNjksOS42MjctOC42MDMsMTUuOTAyLTExLjIyMUwxNDYuMTk1LDM3Mi4xMXoiLz4NCgk8cGF0aCBkPSJNMTc3LjAzNSwyODQuODA0Yy0yMi4yNTMsMC00MC4zNDUsMTguMS00MC4zNDUsNDAuMzUzYzAsMTguNDM0LDEyLjQ4NiwzMy44NTQsMjkuMzk3LDM4LjY2bDQ2LjA5Mi0xOS4yMQ0KCQljMy4yMTQtNS43OTEsNS4yMTctMTIuMzYxLDUuMjE3LTE5LjQ1QzIxNy4zOTcsMzAyLjkwNCwxOTkuMjg5LDI4NC44MDQsMTc3LjAzNSwyODQuODA0eiIvPg0KCTxwYXRoIGQ9Ik00MjUuMzA1LDMzMi41NzJjLTAuODIyLDAtMS42NjIsMC4xNjItMi40NywwLjQ5NmwtMzIuOTg0LDEzLjczNmMtMS40MjgsMC41OTgtMi45MDQsMC44NzgtNC4zNjQsMC44NzgNCgkJYy00LjQ0MiwwLTguNjY1LTIuNjMzLTEwLjQ4My03LjAwNWwtMTAuMDYzLTI0LjEyNGMtMS4xNDgtMi43ODgtMS4xOC01LjkwOS0wLjAxNi04LjY5N2MxLjEzNC0yLjc5NiwzLjM0LTUuMDA5LDYuMTE5LTYuMTY1DQoJCWwzMi45ODQtMTMuNzQ0YzMuMjYyLTEuMzU4LDQuNzgzLTUuMDc4LDMuNDMyLTguMzE1Yy01LjY1Mi0xMy41OC0yMC4yNS0yMC43NjMtMzQuMTAyLTE3LjU2NGwtMTYuMzY4LDMuNzM1DQoJCWMtMTUuNTc2LDMuNTU2LTI4LjY1MSwxNC4wNDYtMzUuNTE2LDI4LjQ1N0wzMDguNCwzMjEuNzMyTDEyMC4xMDQsNDAwLjIxYy0xNS4zMTIsNi4zODMtMjIuNTQ4LDIzLjk1My0xNi4xNjYsMzkuMjgxDQoJCWM2LjMyMSwxNS4xNSwyMy44MDcsMjIuNjExLDM5LjI4OSwxNi4xNzRsMTg4LjMxLTc4LjQ3MWwyOC42ODMsMTAuMDQ5YzUuNjIzLDEuOTcyLDExLjQ2MSwyLjk0MiwxNy4yNywyLjk0Mg0KCQljOS43ODMsMCwxOS40OS0yLjc0OCwyNy45NTMtOC4xMTNsMTQuMTk0LTguOTk5YzEyLjIzNy03Ljc2NSwxNy4wOTgtMjMuMjAxLDExLjUyMy0zNi41OA0KCQlDNDMwLjE1LDMzNC4wNDgsNDI3Ljc5LDMzMi41NzIsNDI1LjMwNSwzMzIuNTcyeiIvPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPC9zdmc+DQo="
LABEL oc.keyword="cntlm,cntlm,proxy,ntlm"
LABEL oc.cat="development"
LABEL oc.launch="gnome-terminal-server.cntlm"
LABEL oc.template="abcdesktopio/oc.template.ubuntu.minimal.22.04"
ENV ARGS="--class cntlm -- bash -c '/usr/sbin/cntlm -f -v; exec bash'"
LABEL oc.name="cntlm"
LABEL oc.displayname="cntlm"
LABEL oc.path="/usr/bin/gnome-terminal"
LABEL oc.type=app
LABEL oc.acl="{\"permit\":[\"all\"]}"
LABEL oc.host_config="{\"network_mode\":\"container\"}"
RUN  if [ -d /usr/share/icons ]   && [ -x /composer/safelinks.sh ] && [ -d /usr/share/icons   ];  then cd /usr/share/icons;    /composer/safelinks.sh; fi 
RUN  if [ -d /usr/share/pixmaps ] && [ -x /composer/safelinks.sh ] && [ -d /usr/share/pixmaps ];  then cd /usr/share/pixmaps;  /composer/safelinks.sh; fi 
ENV APPNAME "cntlm"
ENV APPBIN "/usr/bin/gnome-terminal"
LABEL oc.args="--class cntlm -- bash -c '/usr/sbin/cntlm -f -v; exec bash'"
ENV APP "/usr/bin/gnome-terminal"
RUN chown balloon:root /etc/cntlm.conf
RUN chmod 755 /composer/cntlm.mustache
USER root
RUN mkdir -p /var/secrets/abcdesktop/localaccount && cp /etc/passwd /etc/group /etc/shadow /var/secrets/abcdesktop/localaccount
RUN rm -f /etc/passwd && ln -s /var/secrets/abcdesktop/localaccount/passwd /etc/passwd
RUN rm -f /etc/group && ln -s /var/secrets/abcdesktop/localaccount/group  /etc/group
RUN rm -f /etc/shadow && ln -s /var/secrets/abcdesktop/localaccount/shadow /etc/shadow
RUN rm -f /etc/gshadow && ln -s /var/secrets/abcdesktop/localaccount/gshadow /etc/gshadow
USER balloon
CMD [ "/composer/appli-docker-entrypoint.sh" ]

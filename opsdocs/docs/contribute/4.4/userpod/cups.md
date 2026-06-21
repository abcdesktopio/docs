---
title: Virtual Printer (CUPS) Container | abcdesktop.io
description: Developer reference for the abcdesktop.io virtual printer container: CUPS configuration, Node.js PDF download service, and Dockerfile structure.
keywords: CUPS, virtual printer, PDF, Node.js, abcdesktop, contribute, user pod
tags:
  - contribute
  - CUPS
  - printer
  - user pod
---

# Dockerfile and Runtime Architecture Specification

## 1. Scope and Intent

This document is the normative specification of the container image produced by the Dockerfile in this repository.

Image purpose:
- Provide a CUPS-based printing runtime for abcdesktop.
- Bundle and run two Node.js services used by the printing workflow.
- Run all runtime processes under a Supervisor process manager.

Design style:
- Single-stage image.
- The runtime uses a multi-service process supervision model rather than a single-process container design.
- Configuration-heavy image where repository-provided `/etc` content defines runtime behavior.

## 2. Base Image and Global Build Inputs

### 2.1 Base image

- Base image: node:20

Implications:
- Node.js runtime is available for printer-service and file-service.
- Debian/apt package management is available.

### 2.2 Build argument contract

- ARG BRANCH={{ abcdesktop.latest_release }}
- ENV BRANCH=$BRANCH

Meaning:
- BRANCH selects which branch is cloned for external service repositories.
- If BRANCH is not provided, branch 4.4 is used.

Example build:

```bash
docker build --build-arg BRANCH={{ abcdesktop.latest_release }} -t oc.cupsd:{{ abcdesktop.latest_release }} .
```

## 3. External Source Dependencies (Build-Time)

The Dockerfile clones source code at build time from:

- https://github.com/abcdesktopio/file-service.git into /composer/node/file-service
- https://github.com/abcdesktopio/printer-service.git into /composer/node/printer-service

Branch selection:
- Both repositories are cloned with -b $BRANCH.

Reproducibility note:
- Because both repositories are cloned using a branch name rather than a pinned commit or tag, the resulting images may vary over time even when the same Dockerfile and BRANCH value are used. Pin to specific commits or tags for reproducible production builds.

## 4. Dependency Installation Behavior

### 4.1 Node dependencies

For each cloned Node.js service:
- The working directory is set to the service directory.
- `npm install --save-prod` is executed to install production dependencies only.

Behavioral implications:
- Production dependencies are installed.
- The exact dependency graph may change over time unless the lockfiles in the cloned repositories are stable and honored.

### 4.2 System dependencies

The image installs two groups of apt packages.

Font and rendering group:
- fonts-recommended
- xfonts-base
- xfonts-encodings
- xfonts-utils
- xfonts-100dpi
- xfonts-75dpi
- libfontconfig
- libfreetype6
- fonts-freefont-ttf
- fonts-croscore
- fonts-dejavu-core
- fonts-horai-umefont
- fonts-noto
- fonts-opendyslexic
- fonts-roboto
- fonts-roboto-hinted
- fonts-sil-mondulkiri
- fonts-unfonts-core
- fonts-wqy-microhei

Printing and supervision group:
- supervisor
- smbclient
- cups-pdf
- cups

Cleanup behavior:
- apt cache is cleaned after install.
- /var/lib/apt/lists is removed to reduce layer size.

## 5. Files Injected from Repository

### 5.1 Entrypoint

- docker-entrypoint.sh is copied to /docker-entrypoint.sh

### 5.2 Configuration tree override

The entire local `etc` directory is copied into `/etc` in the image.

This includes at minimum:
- `/etc/supervisord.conf`
- `/etc/supervisor/conf.d/*.conf`
- `/etc/cups/*`

Operational meaning:
- Container runtime behavior is strongly governed by repository configuration files.
- Upstream defaults from the base image may be overridden by this repository's content.

## 6. Build-Time Filesystem and Permissions

Directories explicitly created:
- /var/log/desktop
- /var/run/desktop
- /composer/run

Additional metadata file:
- /etc/build.date (contains output of date captured at build time)

Ownership adjustments:
- chown -R lp:root /etc/cups/ppd /etc/cups/printers.conf

Group membership change:
- root is added to lpadmin group.

## 7. Runtime Entrypoint Contract

Default command:

```bash
/docker-entrypoint.sh
```

Entrypoint runtime sequence:

1. Export KUBERNETES_SERVICE_HOST.
2. Compute CONTAINER_IP_ADDR as:
  - POD_IP when provided, otherwise
  - output of hostname -i.
3. Rewrite /etc/cups/cupsd.conf:
  - replace localhost:631 with ${CONTAINER_IP_ADDR}:631.
4. Normalize DISABLE_REMOTEIP_FILTERING:
  - default is disabled when empty.
  - only literal enabled is preserved.
5. Export file-service restrictions:
  - ACCEPTFILE=false
  - ACCEPTLISTFILE=false
  - ACCEPTDELETEFILE=false
6. Start supervisor in foreground:
  - /usr/bin/supervisord --pidfile /var/run/desktop/supervisord.pid --nodaemon --configuration /etc/supervisord.conf

Runtime side effect:
- `cupsd.conf` is mutated at container startup, so the CUPS listening address is determined at runtime rather than build time.

## 8. Supervisor Process Topology

Supervisor master config:
- /etc/supervisord.conf

Included program configs:
- /etc/supervisor/conf.d/cupsd.conf
- /etc/supervisor/conf.d/printer-service.conf
- /etc/supervisor/conf.d/printerfile-service.conf

### 8.1 Process: cupsd

- Command: /usr/sbin/cupsd -c /etc/cups/cupsd.conf -f
- User: root
- Autostart: true
- Autorestart: true
- Start priority: 10

### 8.2 Process: printer-service

- Command: node /composer/node/printer-service/printer-service.js
- User: nobody
- Autostart: true
- Autorestart: true
- Start priority: 90
- Environment:
  - WATCHDIR=/var/spool/cups-pdf/ANONYMOUS
  - CONTAINER_IP_ADDR from entrypoint export
  - DISABLE_REMOTEIP_FILTERING from entrypoint export
  - BROADCAST_SERVICE_TCP_PORT=29784

### 8.3 Process: printerfile-service

- Command: node /composer/node/file-service/file-service.js
- User: nobody
- Autostart: true
- Autorestart: true
- Start priority: 10
- Environment:
  - HOME=/var/spool/cups-pdf/ANONYMOUS
  - LOGNAME=nobody
  - DISABLE_REMOTEIP_FILTERING from entrypoint export
  - CONTAINER_IP_ADDR from entrypoint export
  - FILE_SERVICE_TCP_PORT=29782

## 9. CUPS and CUPS-PDF Runtime Specification

### 9.1 cupsd listening behavior

Configured initially in /etc/cups/cupsd.conf:
- Listen localhost:631
- Listen /tmp/.cups.sock

After entrypoint rewrite:
- Listen <CONTAINER_IP_ADDR>:631
- Listen /tmp/.cups.sock

### 9.2 Access control model

From /etc/cups/cupsd.conf and /etc/cups/cups-files.conf:
- SystemGroup is lpadmin.
- Administrative operations require authenticated @SYSTEM users.
- Root and admin locations allow local/network-permitted access according to config rules.

### 9.3 PDF output contract

From /etc/cups/cups-pdf.conf:
- Out /var/spool/cups-pdf/ANONYMOUS
- AnonDirName /var/spool/cups-pdf/ANONYMOUS
- AnonUser nobody
- Grp lpadmin

Service integration contract:
- printer-service watches /var/spool/cups-pdf/ANONYMOUS.
- printerfile-service uses same path as HOME.

## 10. Network Interface Specification

Dockerfile exposed ports:
- 631/tcp: CUPS endpoint
- 29782/tcp: printerfile-service endpoint

Not exposed by Dockerfile but used internally by service config:
- 29784/tcp: printer-service broadcast service port variable

## 11. Environment Variable Matrix

### 11.1 Build-time

- BRANCH: selects Git branch for cloned service repos.

### 11.2 Runtime input variables

- POD_IP: preferred container IP source.
- KUBERNETES_SERVICE_HOST: exported if present.
- DISABLE_REMOTEIP_FILTERING: accepted values effectively enabled or disabled.

### 11.3 Runtime computed/exported variables

- CONTAINER_IP_ADDR: computed from POD_IP or hostname -i.
- DISABLE_REMOTEIP_FILTERING: normalized by entrypoint.
- ACCEPTFILE=false
- ACCEPTLISTFILE=false
- ACCEPTDELETEFILE=false

### 11.4 Service-level variables via supervisor

- WATCHDIR=/var/spool/cups-pdf/ANONYMOUS
- BROADCAST_SERVICE_TCP_PORT=29784
- FILE_SERVICE_TCP_PORT=29782
- HOME=/var/spool/cups-pdf/ANONYMOUS
- LOGNAME=nobody

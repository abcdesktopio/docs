## Purpose

This Dockerfile builds the `oc.cupsd` container image used by abcdesktop.io to provide a CUPS-based printer subsystem. The image combines:

* the CUPS scheduler and PDF printing support
* a Node.js printer service
* a Node.js file service dedicated to printer-related file downloads
* the configuration files required to run those services under `supervisord`

The container is designed to run as a long-lived service container, not as a one-shot build artifact.

## Image Identity

* Base image: `node:20`
* Image type: single-stage Linux container
* Primary runtime process: `/usr/bin/supervisord`
* Container user at runtime: `root`

## Build Inputs

### Build argument

* `BRANCH` Default: `4.4`

The `BRANCH` argument is exported to `ENV BRANCH` and is used to select the Git branch cloned from the upstream repositories.

### External source repositories

At build time, the image clones the following repositories from GitHub:

* `https://github.com/abcdesktopio/file-service.git`
* `https://github.com/abcdesktopio/printer-service.git`

Both are cloned using the branch named by `BRANCH`.

## Build Process

The image is assembled in the following order:

1. Start from `node:20`.
2. Set the `BRANCH` build argument and export it as an environment variable.
3. Create `/composer/node/file-service` and clone the file service repository into it.
4. Create `/composer/node/printer-service` and clone the printer service repository into it.
5. Install production dependencies for the file service with `npm install --save-prod`.
6. Install production dependencies for the printer service with `npm install --save-prod`.
7. Install font packages and font libraries needed for print rendering.
8. Install CUPS, CUPS-PDF, `smbclient`, and `supervisor`.
9. Copy `docker-entrypoint.sh` into the image root as `/docker-entrypoint.sh`.
10. Add the `root` user to the `lpadmin` group.
11. Record the build timestamp in `/etc/build.date`.
12. Create runtime directories under `/var/log/desktop`, `/var/run/desktop`, and `/composer/run`.
13. Copy the `etc/` directory into `/etc`, replacing the container's runtime configuration.
14. Change ownership of `/etc/cups/ppd` and `/etc/cups/printers.conf` to `lp:root`.
15. Run the container as `root`.
16. Launch `/docker-entrypoint.sh` by default.
17. Expose TCP ports `631` and `29782`.

## Installed System Packages

### Font and rendering packages

The Dockerfile explicitly installs the following font-related packages:

* `fonts-recommended`
* `xfonts-base`
* `xfonts-encodings`
* `xfonts-utils`
* `xfonts-100dpi`
* `xfonts-75dpi`
* `libfontconfig`
* `libfreetype6`
* `fonts-freefont-ttf`
* `fonts-croscore`
* `fonts-dejavu-core`
* `fonts-horai-umefont`
* `fonts-noto`
* `fonts-opendyslexic`
* `fonts-roboto`
* `fonts-roboto-hinted`
* `fonts-sil-mondulkiri`
* `fonts-unfonts-core`
* `fonts-wqy-microhei`

These packages provide broad font coverage for generated and printed documents.

### Printing and process supervision packages

The Dockerfile installs:

* `supervisor`
* `smbclient`
* `cups-pdf`
* `cups`

These packages provide the CUPS scheduler, PDF backend, SMB printer access, and process supervision.

## Files Added or Overridden in the Image

### `/docker-entrypoint.sh`

The entrypoint script is copied from the repository root. It is the first process started by Docker and is responsible for environment preparation before starting `supervisord`.

### `/etc`

The entire repository `etc/` directory is copied into `/etc` inside the image. This is a broad override of container configuration and includes:

* `/etc/supervisord.conf`
* `/etc/supervisor/conf.d/*.conf`
* `/etc/cups/*`

### `/etc/build.date`

Contains the build timestamp generated at image build time.

## Runtime Contract

### Entrypoint Behavior

The entrypoint performs the following runtime actions:

1. Exports `KUBERNETES_SERVICE_HOST` if it exists in the environment.
2. Determines the container IP address using `POD_IP` if present, otherwise `hostname -i`.
3. Rewrites `/etc/cups/cupsd.conf`, replacing `localhost:631` with `<container-ip>:631`.
4. Normalizes the `DISABLE_REMOTEIP_FILTERING` environment variable.
5. Forces the following environment variables for the printer-related services:
   * `ACCEPTFILE=false`
   * `ACCEPTLISTFILE=false`
   * `ACCEPTDELETEFILE=false`
6. Starts `supervisord` in the foreground using `/etc/supervisord.conf`.

### Supervisord-managed services

The container starts the following supervised programs:

* `cupsd` from `/etc/supervisor/conf.d/cupsd.conf`
* `printer-service` from `/etc/supervisor/conf.d/printer-service.conf`
* `printerfile-service` from `/etc/supervisor/conf.d/printerfile-service.conf`

#### `cupsd`

* Command: `/usr/sbin/cupsd -c /etc/cups/cupsd.conf -f`
* User: `root`
* Autostart: yes
* Restart: yes

#### `printer-service`

* Command: `node /composer/node/printer-service/printer-service.js`
* User: `nobody`
* Environment:
  * `WATCHDIR=/var/spool/cups-pdf/ANONYMOUS`
  * `CONTAINER_IP_ADDR` inherited from the entrypoint
  * `DISABLE_REMOTEIP_FILTERING` inherited from the entrypoint
  * `BROADCAST_SERVICE_TCP_PORT=29784`
* Autostart: yes
* Restart: yes

#### `printerfile-service`

* Command: `node /composer/node/file-service/file-service.js`
* User: `nobody`
* Environment:
  * `HOME=/var/spool/cups-pdf/ANONYMOUS`
  * `LOGNAME=nobody`
  * `DISABLE_REMOTEIP_FILTERING` inherited from the entrypoint
  * `CONTAINER_IP_ADDR` inherited from the entrypoint
  * `FILE_SERVICE_TCP_PORT=29782`
* Autostart: yes
* Restart: yes

## CUPS Configuration Contract

### Listen addresses

The shipped `cupsd.conf` initially listens on:

* `localhost:631`
* `/tmp/.cups.sock`

At runtime, the entrypoint rewrites `localhost:631` to `<container-ip>:631` so CUPS binds to the detected container IP address instead of loopback.

### Access model

The CUPS configuration is set up to:

* allow local-network access to the root and admin locations
* require authentication for sensitive administrative operations
* use the `lpadmin` group as the `@SYSTEM` group in `cups-files.conf`

### CUPS-PDF output path

`cups-pdf.conf` configures anonymous PDF output to:

* `/var/spool/cups-pdf/ANONYMOUS`

This path is also used by the Node services as their watch/output directory.

## Port Specification

The image exposes the following ports:

* `631/tcp` - CUPS scheduler and HTTP administrative interface
* `29782/tcp` - printer file service

The supervisor configuration also references `29784/tcp` for broadcast service coordination, but that port is not declared in `EXPOSE`.

## Filesystem Specification

### Created directories

The Dockerfile creates these directories during build:

* `/var/log/desktop`
* `/var/run/desktop`
* `/composer/run`

### Important persistent or runtime paths

* `/var/log/desktop` - supervisord logs and container-level logs
* `/var/run/desktop` - PID files and socket files for supervisor-managed processes
* `/var/log/cups` - CUPS logs, as configured in `cups-files.conf`
* `/var/spool/cups-pdf/ANONYMOUS` - PDF output directory used by CUPS-PDF and Node services
* `/etc/cups` - scheduler configuration and printer definitions

### Ownership and permissions

The image sets the ownership of these files to `lp:root`:

* `/etc/cups/ppd`
* `/etc/cups/printers.conf`

This aligns the CUPS printer data with the system service account expected by the container.

## Environment Variables

### Build-time and inherited variables

* `BRANCH` - selects the Git branch for upstream service clones
* `KUBERNETES_SERVICE_HOST` - re-exported by the entrypoint if present
* `POD_IP` - preferred source for the container IP address

### Runtime service variables

* `CONTAINER_IP_ADDR` - computed by the entrypoint and consumed by CUPS and the Node services
* `DISABLE_REMOTEIP_FILTERING` - normalizes remote IP filtering behavior for the printer services
* `ACCEPTFILE=false` - disables file upload acceptance in the printer-related file service context
* `ACCEPTLISTFILE=false` - disables list-file acceptance
* `ACCEPTDELETEFILE=false` - disables delete-file acceptance
* `WATCHDIR=/var/spool/cups-pdf/ANONYMOUS` - printer-service watch directory
* `BROADCAST_SERVICE_TCP_PORT=29784` - printer-service broadcast port
* `FILE_SERVICE_TCP_PORT=29782` - printerfile-service TCP port


## Functional Summary

At runtime, the image provides:

* a CUPS scheduler reachable on port `631`
* a printer file service on port `29782`
* a printer service that uses the CUPS-PDF output directory as its watch path
* runtime CUPS configuration derived from the container IP and repository-provided config files

## Specification Checklist

An implementation conforming to this Dockerfile must:

* build from `node:20`
* accept `BRANCH` with a default of `4.0`
* clone `file-service` and `printer-service` from `abcdesktopio`
* install production dependencies for both Node services
* install the declared font and printing packages
* copy the repository `etc/` tree to `/etc`
* copy `docker-entrypoint.sh` to `/docker-entrypoint.sh`
* create the runtime directories listed above
* run `supervisord` as PID 1 via the entrypoint
* expose ports `631` and `29782`
* start `cupsd`, `printer-service`, and `printerfile-service` under supervisord

## Relevant Repository Files

* [Dockerfile](Dockerfile)
* [docker-entrypoint.sh](docker-entrypoint.sh)
* [README.md](README.md)
* [etc/supervisord.conf](etc/supervisord.conf)
* [etc/supervisor/conf.d/cupsd.conf](etc/supervisor/conf.d/cupsd.conf)
* [etc/supervisor/conf.d/printer-service.conf](etc/supervisor/conf.d/printer-service.conf)
* [etc/supervisor/conf.d/printerfile-service.conf](etc/supervisor/conf.d/printerfile-service.conf)
* [etc/cups/cupsd.conf](etc/cups/cupsd.conf)
* [etc/cups/cups-files.conf](etc/cups/cups-files.conf)
* [etc/cups/cups-pdf.conf](etc/cups/cups-pdf.conf)

=======
# Dockerfile and Runtime Architecture Specification

## 1. Scope and Intent

This document is the normative specification of the container image produced by this repository Dockerfile.

Image purpose:
- Provide a CUPS-based printing runtime for abcdesktop.
- Bundle and run two Node.js services used by the printing workflow.
- Run all runtime processes under supervisor.

Design style:
- Single-stage image.
- Runtime is process-supervised multi-service (not a one-process image).
- Configuration-heavy image where repository-provided /etc content defines behavior.

## 2. Base Image and Global Build Inputs

### 2.1 Base image

- Base image: node:20

Implications:
- Node.js runtime is available for printer-service and file-service.
- Debian/apt package management is available.

### 2.2 Build argument contract

- ARG BRANCH=4.4
- ENV BRANCH=$BRANCH

Meaning:
- BRANCH selects which branch is cloned for external service repositories.
- If BRANCH is not provided, branch 4.4 is used.

Example build:

```bash
docker build --build-arg BRANCH=4.4 -t oc.cupsd:4.4 .
```

## 3. External Source Dependencies (Build-Time)

The Dockerfile clones source code at build time from:

- https://github.com/abcdesktopio/file-service.git into /composer/node/file-service
- https://github.com/abcdesktopio/printer-service.git into /composer/node/printer-service

Branch selection:
- Both repositories are cloned with -b $BRANCH.

Reproducibility note:
- Because clones are branch-based (not commit-pinned), resulting images can vary over time for the same Dockerfile and BRANCH value.

## 4. Dependency Installation Behavior

### 4.1 Node dependencies

For each cloned Node service:
- Working directory is set to service directory.
- npm install --save-prod is executed.

Behavioral implications:
- Production dependencies are installed.
- Exact dependency graph may change over time unless lockfiles in cloned repos are stable and honored.

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

- Entire local etc directory is copied into /etc in the image.

This includes at minimum:
- /etc/supervisord.conf
- /etc/supervisor/conf.d/*.conf
- /etc/cups/*

Operational meaning:
- Container runtime behavior is strongly defined by repository config files.
- Upstream defaults from the base image may be overridden by this repository content.

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
- cupsd.conf is mutated at container startup, so CUPS listen address is runtime-dependent.

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

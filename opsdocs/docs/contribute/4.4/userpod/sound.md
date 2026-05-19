# Dockerfile and Runtime Architecture Specification

## Scope

This specification documents the container architecture, build behavior, runtime process topology, and media relay contracts for this repository.

Primary configuration artifacts:

- `Dockerfile`
- `docker-entrypoint.sh`
- `etc/supervisord.conf`
- `etc/supervisor/conf.d/pulseaudio.conf`
- `etc/supervisor/conf.d/ffmpeg.speaker.conf`
- `etc/supervisor/conf.d/websocket-relay.speaker.conf`
- `etc/supervisor/conf.d/websocket-relay.microphone.conf`
- `composer/ffmpeg.speaker.sh`

Primary sound artifacts:

- `composer/node/websocket-relay.microphone/websocket-relay.js`
- `composer/node/websocket-relay.speaker/websocket-relay.js`


## 1. System Purpose

The image provides a containerized audio stack that:

1. Runs PulseAudio in-container.
2. Captures speaker output and re-encodes it with FFmpeg.
3. Streams media data through FIFO files in `/container`.
4. Exposes websocket relay services via Node.js processes.
5. Uses Supervisor to keep processes alive and coordinate startup.


## 2. Dockerfile Build Specification

### 2.1 Base Image

- Base image: `ubuntu` (floating tag).

### 2.2 Identity and Runtime User

Configured environment variables:

- `PULSEUID=102`
- `PULSEGID=104`
- `PULSELOGNAME=pulse`
- `PULSEUSER=pulse`
- `PULSEGROUP=pulse`

Provisioning:

- Creates group `pulse` with GID 104.
- Creates user `pulse` with UID 102.
- Adds user to `sudo` group.
- Final runtime user is `pulse`.

### 2.3 Noninteractive Package Installation

Debconf settings:

- `DEBCONF_FRONTEND=noninteractive`
- `TERM=linux`

Installed apt packages:

- `ca-certificates`
- `pulseaudio`
- `pulseaudio-utils`
- `supervisor`
- `libnss-extrausers`
- `ffmpeg`
- `gnupg`
- `curl`

### 2.4 Node.js Installation

- `NODE_MAJOR=20`
- Installs NodeSource apt key and repository.
- Installs `nodejs`.
- Upgrades npm globally (`npm install -g npm`).

### 2.5 Application and Configuration Copy

- Copies repository `etc` directory to `/etc`.
- Copies repository `composer` directory to `/composer`.
- Copies `etc/nsswitch.conf` explicitly to `/etc/nsswitch.conf`.

### 2.6 Node Dependency Installation

- Runs `npm install --omit=dev && npm audit fix` in:
  - `/composer/node/websocket-relay.speaker`
  - `/composer/node/websocket-relay.microphone`

### 2.7 Runtime Filesystem Setup

Creates and/or adjusts:

- `/var/run/dbus`
- `/var/log/desktop`
- `/var/run/desktop`
- `/var/run/local`
- `/var/log/local`
- `/var/lib/dbus/machine-id`
- `/etc/pulse/abcdesktopcookie`
- `/container`


### 2.8 Runtime Defaults and Entrypoint

- `ENV PULSE_SERVER=/tmp/.pulse.sock`
- Writes build timestamp to `/etc/build.date`.
- Copies `docker-entrypoint.sh` to `/docker-entrypoint.sh`.
- Uses `USER pulse`.
- Runs `CMD ["/docker-entrypoint.sh"]`.
- Exposes ports: `29788` and `29789`.



## 3. Runtime Behavior Specification

### 3.1 Entrypoint (`docker-entrypoint.sh`)

Startup flow:

1. Sets defaults for:
   - `ABCDESKTOP_LOG_DIR` (default `/var/log/desktop`)
   - `ABCDESKTOP_RUN_DIR` (default `/var/run/desktop`)
2. Logs `id`, environment, and selected directory listings for diagnostics.
3. Computes container IP from `POD_IP` or `hostname -i`.
4. Sets `LC_ALL=C`.
5. Rebuilds `/etc/pulse/abcdesktopcookie` from `PULSEAUDIO_COOKIE` when set.
6. Sets `WEBRELAY_INTERNAL_TCP_PORT=29780`.
7. Creates FIFO `/container/speaker`.
8. Starts Supervisor in foreground using `/etc/supervisord.conf`.

### 3.2 Supervisor Topology

From `/etc/supervisord.conf` and include rules:

- Includes `/etc/supervisor/conf.d/*.conf`.

Configured programs:

1. `pulseaudio`
   - command: `/composer/pulseaudio.sh`
   - autostart: true
2. `websocket-relay.speaker`
   - command: `node /composer/node/websocket-relay.speaker/websocket-relay /container/speaker 29788`
   - autostart: true
3. `websocket-relay.microphone`
   - command: `node /composer/node/websocket-relay.microphone/websocket-relay /container/microphone 29789`
   - autostart: true
4. `ffmpeg.speaker`
   - command: `/composer/ffmpeg.speaker.sh`
   - autostart: false


## 4. FFmpeg Speaker Script Specification

File: `composer/ffmpeg.speaker.sh`

Purpose:

- Capture PulseAudio monitor source `speaker.monitor`.
- Encode to MPEG-TS + MP2 audio.
- Write stream to FIFO `/container/speaker`.

Inputs:

- `POD_IP` (optional)
- `PULSE_SERVER` (default `/tmp/.pulse.sock`)
- `WEBRELAY_INTERNAL_TCP_PORT` (default `29780`)

Behavior:

1. Resolves `CONTAINER_IP_ADDR`, `PULSE_SERVER`, `WEBRELAY_INTERNAL_TCP_PORT`.
2. If PulseAudio socket is not ready, waits briefly.
3. Executes ffmpeg pipeline:
   - input: `-f pulse -i speaker.monitor`
   - output format: `-f mpegts`
   - audio codec: `-codec:a mp2`
   - bitrate: `-b:a 128k`
   - channels: `-ac 1`
   - output: `> /container/speaker`

Output contract:

- Continuous MPEG-TS audio stream into FIFO `/container/speaker`.
- Intended consumer: speaker websocket relay process.


## 5. Microphone Relay JavaScript Specification

### 5.1 Active Source File

File:
- `composer/node/websocket-relay.microphone/websocket-relay.js`

Role:

- Websocket ingest endpoint for microphone data.
- Receives websocket binary/audio payloads and writes them into FIFO.

Key behavior:

1. Parses args:
   - FIFO path (default `/container/microphone`)
   - websocket port (default `8082`)
2. Binds websocket server on:
   - host: `CONTAINER_IP_ADDR` or `0.0.0.0`
   - configured port
3. On first client connection:
   - opens FIFO write stream (`fs.createWriteStream(FIFO_FILENAME)`)
4. On each websocket message:
   - writes payload to FIFO if stream is active
5. On last disconnect:
   - closes FIFO stream and clears handle


## 6. Speaker Relay JavaScript Reference

File:

- `composer/node/websocket-relay.speaker/websocket-relay.js`

Role:

- Broadcasts speaker media from FIFO to connected websocket clients.

Behavior summary:

1. Opens FIFO read stream (`/container/speaker` by default).
2. Broadcasts each data chunk to all open websocket clients.
3. Uses Supervisor RPC client to start `ffmpeg.speaker` on first websocket connection.
4. Attempts to stop process name `ffmpeg` on last disconnection.


## 7. Interface Contracts

### 7.1 Environment Variables

Runtime variables used by scripts:

- `PULSEAUDIO_COOKIE`
- `POD_IP`
- `ABCDESKTOP_LOG_DIR`
- `ABCDESKTOP_RUN_DIR`
- `PULSE_SERVER`
- `CONTAINER_IP_ADDR`
- `WEBRELAY_INTERNAL_TCP_PORT`

### 7.2 Network Contracts

- Speaker websocket service: `29788/tcp`
- Microphone websocket service: `29789/tcp`

### 7.3 Local IPC Contracts

- FIFO speaker stream: `/container/speaker`
- FIFO microphone stream: `/container/microphone`
=======
## 1. System Purpose

The image implements a PulseAudio streaming sidecar with two websocket services:

1. Speaker relay: reads encoded audio from a FIFO and broadcasts to websocket clients.
2. Microphone relay: receives websocket payloads and writes to a FIFO consumed by PulseAudio module-pipe-source.
3. Supervisor manages lifecycle of PulseAudio and relay processes.

---

## 2. Build Specification

### 2.1 Base Image and Reproducibility

- Base image: ubuntu:24.04.
- This is pinned by tag, but not by digest.

### 2.2 Identity Model

Configured variables:
- PULSEUID=102
- PULSEGID=104
- PULSELOGNAME=pulse
- PULSEUSER=pulse
- PULSEGROUP=pulse

Provisioning:

1. Creates group pulse with GID 104.
2. Creates user pulse with UID 102.
3. User supplementary groups are set via --groups 104.
4. Runtime user is pulse.

### 2.3 OS Package Layer

Debconf noninteractive mode is configured and these packages are installed:

- ca-certificates
- pulseaudio
- pulseaudio-utils
- supervisor
- libnss-extrausers
- ffmpeg
- gnupg
- curl

### 2.4 Node.js Layer

- NODE_MAJOR=20.
- NodeSource repository is configured.
- nodejs package is installed.
- npm is globally upgraded.

### 2.5 Source and Config Copy

Build copies:
1. etc -> /etc
2. composer -> /composer
3. etc/nsswitch.conf -> /etc/nsswitch.conf

### 2.6 Node Dependency Installation

Dependency strategy now uses lockfiles and npm ci:

1. /composer/node/websocket-relay.speaker: npm ci --omit=dev
2. /composer/node/websocket-relay.microphone: npm ci --omit=dev

Required lockfiles are present in both relay directories.

### 2.7 Runtime Filesystem Preparation

Dockerfile prepares these paths:

- /var/run/dbus
- /var/log/desktop
- /var/run/desktop
- /var/run/local
- /var/log/local
- /var/lib/dbus/machine-id
- /etc/pulse/abcdesktopcookie
- /container

Current mode setup uses 666 for directories and selected files.

### 2.8 Entrypoint and Port Contract

- ENV PULSE_SERVER=/tmp/.pulse.sock
- CMD /docker-entrypoint.sh
- USER pulse
- EXPOSE 29788 29789

---

## 3. Runtime Topology and Control Plane

### 3.1 Entrypoint Behavior

At startup, docker-entrypoint.sh:

1. Sets ABCDESKTOP_LOG_DIR and ABCDESKTOP_RUN_DIR defaults.
2. Logs id, environment, home listing, and /etc/pulse listing.
3. Resolves CONTAINER_IP_ADDR from POD_IP or hostname -i.
4. Rewrites /etc/pulse/abcdesktopcookie from PULSEAUDIO_COOKIE if provided.
5. Exports WEBRELAY_INTERNAL_TCP_PORT=29780.
6. Creates FIFO /container/speaker.
7. Starts supervisord in foreground with /etc/supervisord.conf.

### 3.2 Supervisor Programs

From include pattern /etc/supervisor/conf.d/*.conf:

1. pulseaudio
   - command: /composer/pulseaudio.sh
   - autostart: true
2. websocket-relay.speaker
   - command: node /composer/node/websocket-relay.speaker/websocket-relay.js /container/speaker 29788
   - autostart: true
3. websocket-relay.microphone
   - command: node /composer/node/websocket-relay.microphone/websocket-relay.js /container/microphone 29789
   - autostart: true
4. ffmpeg.speaker
   - command: /composer/ffmpeg.speaker.sh
   - autostart: false

---

## 4. Dataflow Specification

### 4.1 Speaker Data Path

1. ffmpeg.speaker.sh captures PulseAudio source speaker.monitor.
2. ffmpeg outputs MPEG-TS/MP2 stream redirected into /container/speaker.
3. websocket-relay.speaker reads /container/speaker.
4. websocket server on 29788 broadcasts chunks to all connected clients.

Control behavior:

1. On first client, relay requests Supervisor startProcess("ffmpeg.speaker").
2. On last client disconnect, relay requests stopProcess("ffmpeg").

### 4.2 Microphone Data Path

1. websocket-relay.microphone listens on 29789.
2. On first client, it opens a write stream to /container/microphone.
3. Incoming websocket messages are written to /container/microphone.
4. PulseAudio module-pipe-source (configured in PulseAudio config) consumes FIFO data as virtual microphone source.

---

## 5. Script-Level Specification

### 5.1 composer/pulseaudio.sh

- Executes pulseaudio with module-native-protocol-tcp.
- listen address uses CONTAINER_IP_ADDR.
- auth-cookie uses /etc/pulse/abcdesktopcookie.

### 5.2 composer/ffmpeg.speaker.sh

Purpose:

1. Read audio from speaker.monitor.
2. Encode audio as MP2 inside MPEG-TS.
3. Stream to /container/speaker FIFO.

Important runtime inputs:

- PULSE_SERVER (default /tmp/.pulse.sock)
- POD_IP optional (for CONTAINER_IP_ADDR)
- WEBRELAY_INTERNAL_TCP_PORT metadata variable

FFmpeg main characteristics:

- sample rate 44100
- mono channel
- bitrate 128k
- mpegts output

### 5.3 Speaker Relay Node Service

File: composer/node/websocket-relay.speaker/websocket-relay.js

Behavior:

1. Creates websocket server on configured host:port.
2. Opens read stream from FIFO.
3. Broadcasts FIFO chunks to connected clients.
4. Starts ffmpeg.speaker on first client.
5. Requests stop of process named ffmpeg when count returns to zero.

### 5.4 Microphone Relay Node Service

File: composer/node/websocket-relay.microphone/websocket-relay.js

Behavior:

1. Creates websocket server on configured host:port.
2. On first connection opens write stream to FIFO.
3. Writes websocket payloads to FIFO.
4. Closes FIFO stream when last client disconnects.
5. Includes documentation note for PulseAudio module-pipe-source contract.

---

## 6. Interface Contracts

### 6.1 Runtime Environment Variables

Used variables:

- PULSEAUDIO_COOKIE
- POD_IP
- ABCDESKTOP_LOG_DIR
- ABCDESKTOP_RUN_DIR
- CONTAINER_IP_ADDR
- WEBRELAY_INTERNAL_TCP_PORT
- PULSE_SERVER

### 6.2 Network Interface

- 29788/tcp: speaker websocket relay
- 29789/tcp: microphone websocket relay

### 6.3 Filesystem and IPC Interface

- /container/speaker: FIFO producer/consumer path for speaker stream
- /container/microphone: FIFO ingestion path for microphone stream
- /var/run/desktop/supervisor.sock: Supervisor RPC socket

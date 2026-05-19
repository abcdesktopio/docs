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
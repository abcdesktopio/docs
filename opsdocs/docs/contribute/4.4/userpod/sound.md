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

The image implements a PulseAudio streaming sidecar with two WebSocket relay services:

1. **Speaker relay**: reads encoded audio from a FIFO and broadcasts the stream to connected WebSocket clients.
2. **Microphone relay**: receives WebSocket payloads from the browser and writes them to a FIFO consumed by a PulseAudio `module-pipe-source`.
3. **Supervisor** manages the lifecycle of the PulseAudio daemon and both relay processes.

---

## 2. Build Specification

### 2.1 Base Image and Reproducibility

- Base image: `ubuntu:24.04`.
- The image is pinned by tag but not by digest. For fully reproducible builds, pin to a specific image digest.

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

Dependency installation uses lockfiles and `npm ci` for reproducible builds:

1. `/composer/node/websocket-relay.speaker`: `npm ci --omit=dev`
2. `/composer/node/websocket-relay.microphone`: `npm ci --omit=dev`

Required lockfiles must be present in both relay directories.

### 2.7 Runtime Filesystem Preparation

The Dockerfile creates these paths at build time:

- `/var/run/dbus`
- `/var/log/desktop`
- `/var/run/desktop`
- `/var/run/local`
- `/var/log/local`
- `/var/lib/dbus/machine-id`
- `/etc/pulse/abcdesktopcookie`
- `/container`

Directory permissions are set to mode `666` for directories and selected files that require broad write access across process users.

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

1. `ffmpeg.speaker.sh` captures audio from the `speaker.monitor` PulseAudio source.
2. `ffmpeg` encodes the audio as an MPEG-TS/MP2 stream and redirects the output to `/container/speaker`.
3. `websocket-relay.speaker` reads from `/container/speaker`.
4. The WebSocket server on port `29788` broadcasts audio chunks to all connected clients.

Control behavior:

1. On the first client connection, the relay requests Supervisor to start the `ffmpeg.speaker` process.
2. When the last client disconnects, the relay requests Supervisor to stop the `ffmpeg` process.

### 4.2 Microphone Data Path

1. `websocket-relay.microphone` listens on port `29789`.
2. On the first client connection, it opens a write stream to `/container/microphone`.
3. Incoming WebSocket messages are written to `/container/microphone`.
4. The PulseAudio `module-pipe-source` (configured in the PulseAudio configuration) consumes the FIFO data as a virtual microphone source.

---

## 5. Script-Level Specification

### 5.1 composer/pulseaudio.sh

- Executes pulseaudio with module-native-protocol-tcp.
- listen address uses CONTAINER_IP_ADDR.
- auth-cookie uses /etc/pulse/abcdesktopcookie.

### 5.2 composer/ffmpeg.speaker.sh

Purpose:

1. Read audio from `speaker.monitor`.
2. Encode the audio as MP2 inside an MPEG-TS container.
3. Stream the encoded output to the `/container/speaker` FIFO.

Important runtime inputs:

- `PULSE_SERVER` (default: `/tmp/.pulse.sock`)
- `POD_IP` (optional, used to derive `CONTAINER_IP_ADDR`)
- `WEBRELAY_INTERNAL_TCP_PORT` metadata variable

FFmpeg stream characteristics:

- Sample rate: 44100 Hz
- Channels: mono
- Bitrate: 128 kbps
- Container format: MPEG-TS

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

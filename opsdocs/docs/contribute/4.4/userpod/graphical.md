# Specification for the `graphical` service from Dockerfile.ubuntu

## 1. Purpose and Scope

The file [Dockerfile.ubuntu](https://github.com/abcdesktopio/oc.user/blob/4.4/Dockerfile.ubuntu) builds an Ubuntu-based remote desktop runtime image for the abcdesktop ecosystem, including:

- Node.js services (under /composer/node),
- VNC server and WebSocket bridge components,
- audio, printing, and X11 session utilities,
- optional hardening behavior (TARGET_MODE=hardening).

The build uses a two-stage (multi-stage) architecture:

1. ubuntu_node_modules_builder: prepares Node dependencies and composer assets.
2. final stage: assembles the OS, desktop stack, themes, and runtime components.


## 2. Build Interface (Input Contract)

### 2.1 Global build arguments

Declared before the first FROM:

- TARGETPLATFORM
- BUILDPLATFORM
- TAG
- BASE_IMAGE (default: ubuntu)
- BASE_IMAGE_RELEASE (default: 24.04)

### 2.2 Builder-stage arguments

- TARGET_MODE
- TARGET_PRUNE

Exported as environment variables:

- ENV TARGET_MODE=$TARGET_MODE
- ENV TARGET_PRUNE=$TARGET_PRUNE
- ENV NODE_MAJOR=20

### 2.3 Final-stage argument

- TARGET_MODE

Exported as environment variables:

- TARGET_MODE
- NODE_MAJOR=20


## 3. Detailed Specification of Stage 1: ubuntu_node_modules_builder

### 3.1 Base and shell

- Base image: ${BASE_IMAGE}:${BASE_IMAGE_RELEASE}
- Shell: bash (SHELL ["/bin/bash", "-c"])

### 3.2 Toolchain and native prerequisites

Installs build dependencies:

- gcc, g++, make
- libx11-dev, libxmu-dev, libimlib2-dev
- ca-certificates, git, curl, gnupg, dpkg

Purpose: allow compilation of native Node modules (via node-gyp).

### 3.3 Node.js installation

- Adds NodeSource repository for NODE_MAJOR=20.
- Installs nodejs.
- Updates npm globally.
- Installs node-gyp globally.

### 3.4 Composer source import

- COPY composer /composer

The builder then works in /composer/node subdirectories.

### 3.5 Node dependency installation by service

Processed services:

- /composer/node/wait-port
- /composer/node/broadcast-service
- /composer/node/ocrun (repository cloned from run-service)
- /composer/node/ocdownload
- /composer/node/occall
- /composer/node/spawner-service/lib_spawner/colorflow (repository cloned)
- /composer/node/spawner-service
- /composer/node/xterm.js (except in hardening mode)

TARGET_PRUNE behavior:

- empty: generally performs full npm install,
- defined: generally uses npm install --omit=dev.

Implementation note: the condition in the ocrun block is inverted versus other blocks.

### 3.6 ocrun variants generation

The build creates two script variants:

- ocrun.builtin.js (builtin mode)
- ocrun.frontendjs.js (frontendjs mode)

This is done by copying then patching DEFAULT_EXECMODE with sed.

### 3.7 Builder output

Main artifact: enriched /composer tree.

- includes installed Node dependencies,
- includes composer/version.json.



## 4. Detailed Specification of Stage 2 (Final Image)

### 4.1 System initialization

- COPY etc /etc
- apt-get upgrade -y
- base packages: ca-certificates, curl, gnupg, net-tools, bash
- locales setup: locales, language-pack-en, language-pack-fr, language-pack-de, then locale-gen

### 4.2 TigerVNC installation

- TIGERVNC_RELEASE=1.16.0
- Builds dynamic .deb URL using:
  - Ubuntu release (DISTRIB_RELEASE),
  - architecture (dpkg --print-architecture).
- Downloads and installs through apt-get install /tmp/tigervncserver.deb.

### 4.3 Core runtime packages

Installs base runtime services:

- supervision and utilities: supervisor, websockify, desktop-file-utils, xdg-user-dirs
- auth/session: xauth, dbus-x11
- audio/printing: pulseaudio-utils, pavumeter, cups-client
- X11/desktop: x11-utils, x11-apps, xdg-utils, kwin-x11
- infra/security related: krb5-user, libnss-extrausers

### 4.4 Builder artifact import

- COPY --from=ubuntu_node_modules_builder /composer /composer

### 4.5 KDE Plasma and hardening mode

Installs Plasma packages:

- plasma-desktop, plasma-workspace, plasma-workspace-data,
- systemsettings, KDE QML modules.

In hardening mode:

- targeted removal based on dpkg -L libkf5su5 piped to /composer/rmfol.sh
- targeted removal based on dpkg -L sudo piped to /composer/rmfol.sh

### 4.6 Notifications, fonts, and themes

- notifications: libnotificationmanager1, libnotify-bin, libnotify4
- fonts: adds fonts/Selawik.tar, installs fontconfig, fonts-noto, xfonts-base, refreshes cache
- local themes: copies usr/share/themes/Windows-10 and usr/share/aurorae
- remote themes: clones and installs Win11-icon-theme and Win11OS-kde
- wallpaper copy into /composer/wallpapers
- installs Breeze GTK integration

### 4.7 Node.js runtime in final image

Node.js is installed again in the final image (NodeSource, NODE_MAJOR=20).

### 4.8 Runtime resources and application hardening

- adds ALSA sounds (usr/share/sounds/alsa)
- creates /var/log/desktop and /var/run/desktop
- removes xterm supervisor config in hardening mode
- writes build date to /etc/build.date
- in non-hardening mode installs qterminal and vim-gtk3
- removes mimeinfo.cache

### 4.9 Execution contract

- GPU environment variables:
  - NVIDIA_VISIBLE_DEVICES=all
  - NVIDIA_DRIVER_CAPABILITIES=all
- default command:
  - CMD [ "/composer/docker-entrypoint.sh" ]

### 4.10 Network contract

Exposed ports:

- 6081
- 29781
- 29784
- 29786




## 5. Runtime Contract

At runtime, the image assumes:

- startup through /composer/docker-entrypoint.sh,
- service orchestration via Supervisor (config copied from etc),
- writable log/run directories,
- environment compatible with remote desktop operation (VNC/WebSocket/X11).

Hardening-mode behavior:

- no xterm.conf Supervisor entry,
- targeted removal of selected admin/elevation-related file trees,
- no qterminal/vim installation.


## 6. External Dependencies and Supply Chain

The build relies on external sources outside the repository:

- NodeSource repository,
- GitHub repositories cloned during build,
- TigerVNC .deb downloaded from GitHub.

Impact:

- partial reproducibility,
- sensitivity to network/service availability,
- need for pinning and checksum strategy for strict production requirements.



## 7. Security and Compliance Analysis

### Positive aspects

- hardening mode is available,
- frequent apt index cleanup (rm -rf /var/lib/apt/lists/*),
- builder/runtime separation through multi-stage design.

### Identified risks

1. Non-deterministic build behavior
   - git clone without pinned commit/tag,
   - npm audit fix during image build.

2. Supply-chain integrity not fully verified
   - downloaded .deb not validated with explicit checksum,
   - git clones not signature-verified.



## 8. Build Performance and Image Footprint

Observations:

- many separate apt-get update/install blocks,
- heavy desktop packages,
- partial duplication of Node logic (builder and runtime).

Consequences:

- longer build time,
- large final image,
- cache usage can be improved.



## 9. Architecture Recommendations (Expert Level)

### 9.1 Reproducibility

- pin external git dependencies (tag + commit),
- enforce deterministic npm installation from lockfiles,
- move npm audit fix out of Docker build into CI SCA pipeline.

### 9.2 Security

- verify downloaded .deb integrity (SHA256/signature),
- restrict NVIDIA_DRIVER_CAPABILITIES to required capabilities only.

### 9.3 Dockerfile quality

- fix potentially fragile line-continuation formatting (backslash + trailing spaces),
- normalize TARGET_PRUNE logic across all service blocks,
- merge suitable apt installation steps to reduce layers.

### 9.4 Runtime robustness

- explicitly document dependencies of /composer/docker-entrypoint.sh,
- add HEALTHCHECK for critical service/port availability,
- evaluate non-root runtime where compatible with the graphics stack.




## 10. Example Build Commands

```bash
docker build -f Dockerfile.ubuntu -t oc-user:ubuntu .
```

Hardening mode:

```bash
docker build \
  -f Dockerfile.ubuntu \
  --build-arg TARGET_MODE=hardening \
  --build-arg TARGET_PRUNE=1 \
  -t oc-user:ubuntu-hardening \
  .
```




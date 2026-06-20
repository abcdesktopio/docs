# desktop.pod

abcdesktop represents each user's desktop environment as a Kubernetes pod — a cohesive group of containers that collectively deliver the full desktop experience. This multi-container pod architecture is a foundational design principle of abcdesktop: each container encapsulates a single, dedicated service, allowing individual services to be independently enabled, disabled, or replaced without affecting other components.

For example:

- The `printer` container hosts the CUPS print service. It runs inside the user pod and can be enabled or disabled independently of other services.
- The `graphical` container hosts the X11 display server and VNC service, which is the core component responsible for rendering the user's desktop.


## Containers in the user pod

| Container | Description |
|---|---|
| `init` | Executes initialization commands at pod startup, such as setting ownership and permissions on the user's home directory |
| `graphical` | Provides the graphical desktop session via X11 and VNC |
| `printer` | Runs the CUPS print service (`cupsd`), enabling virtual printing to PDF |
| `sound` | Provides audio input and output via PulseAudio |
| `filer` | Provides file transfer capabilities, allowing users to upload and download files to and from their home directory |

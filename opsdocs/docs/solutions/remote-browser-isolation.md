---
title: "Remote Browser Isolation Open Source: Kubernetes-Native RBI with abcdesktop.io"
description: "Looking for an open source Remote Browser Isolation solution? abcdesktop.io delivers RBI natively on Kubernetes — every browser runs in an isolated container, streaming only pixels to the endpoint. Free, self-hosted, no vendor lock-in."
keywords: remote browser isolation open source, open source RBI, remote browser isolation Kubernetes, browser isolation self-hosted, web isolation open source, clientless browser isolation, RBI solution open source, remote browser isolation free, Kubernetes browser isolation, secure browsing Kubernetes
tags:
  - solutions
  - security
  - RBI
---

# Remote Browser Isolation Open Source: RBI on Kubernetes with abcdesktop.io

**Remote Browser Isolation (RBI)** is a security architecture that moves web browsing off the user's endpoint and into an isolated server-side environment. The user's device receives only a rendered pixel stream, no web content, no JavaScript, no active code ever executes locally.

Most commercial RBI solutions are delivered as cloud SaaS with per-seat pricing in the hundreds of dollars per user per year. **abcdesktop.io** implements Remote Browser Isolation as a core architectural paradigm, running entirely on your own Kubernetes cluster, at zero licensing cost.

[:material-rocket-launch-outline: **Try abcdesktop.io — Live Demo**](https://demo.gcp.abcdesktop.com){ .md-button .md-button--primary }

---

## What is Remote Browser Isolation?

Traditional security models attempt to block malicious web content before it reaches the browser. Remote Browser Isolation takes the opposite approach: **let the browser execute everything, but run that browser on a remote server**.

```
Without RBI                         With RBI (abcdesktop.io)
─────────────────────               ─────────────────────────────────
User device                         User device
  └── Browser (local)                 └── Pixel stream only (WebSocket)
       └── Web content                      │
            ├── JavaScript    ←── NEVER     ▼
            ├── Malware            Server-side container (Kubernetes pod)
            └── Exploits             └── Browser (isolated)
                                          └── Web content executes here
                                               ├── JavaScript ✅ (contained)
                                               ├── Malware ✅ (discarded at logout)
                                               └── Exploits ✅ (pod-level isolation)
```

Even if a site delivers a zero-day exploit, it executes inside the ephemeral container. The container is discarded at session end, leaving no persistent compromise on the user's device or the cluster node.

---

## Why open source RBI matters

Commercial RBI vendors (Menlo Security, Zscaler, Symantec) route your users' browsing through their own cloud infrastructure. This creates three structural concerns:

1. **Data sovereignty** : all web traffic passes through a third-party cloud. Regulated industries (defense, finance, healthcare, public sector) may have strict requirements about traffic routing.
2. **Vendor dependency** : pricing, availability, and feature roadmap are controlled by the vendor. A pricing change or service discontinuation directly impacts your security posture.
3. **Cost at scale** : per-seat SaaS pricing makes RBI prohibitively expensive for large user populations or for organizations with variable headcounts.

**Open source RBI on Kubernetes** (abcdesktop.io) eliminates all three:

- Traffic stays within your own infrastructure
- No external dependency, as the platform runs on your Kubernetes cluster
- No per-seat cost : scale to any number of users at infrastructure cost only

---

## How abcdesktop.io implements Remote Browser Isolation

### Architecture

abcdesktop.io provisions one Kubernetes pod per user session. Inside that pod:

- The web browser (Chromium, Firefox, or any installed browser) runs as a **containerized process**
- The pod streams a rendered display to the user's browser via an **encrypted WebSocket (noVNC)**
- The user's endpoint device acts as a pure display terminal, no content is transferred, only pixels

```
User device (any OS, any browser)
    │
    │  HTTPS / WSS — pixels only
    ▼
abcdesktop.io router (nginx ingress)
    │
    ▼
User pod (Kubernetes pod — ephemeral)
  ├── Chromium / Firefox (browser process)
  │     └── Executes web content here
  ├── X11 display server
  ├── noVNC WebSocket encoder
  └── NetworkPolicy: egress restricted to approved destinations
```

### Ephemeral isolation — discarded at logout

Every user pod is created fresh at login and destroyed at logout (or after the session timeout enforced by the garbage collector). There is no persistent state on the container filesystem between sessions. Malware that executes inside the pod cannot survive a session end.

### NetworkPolicy enforcement

Kubernetes NetworkPolicies restrict outbound traffic from user pods. In the default configuration, egress from the user pod to the internal cluster network is blocked. The browser pod can reach the internet but cannot reach internal services. This prevents lateral movement in the event of a browser compromise.

---

## RBI use cases with abcdesktop.io

| Use case | How abcdesktop.io addresses it |
|---|---|
| **Secure web browsing** | Browser runs in isolated pod -> endpoint receives only pixels |
| **BYOD environments** | No software installed on user device, any HTML5 browser is sufficient |
| **Contractor / third-party access** | Isolated session with no access to internal network resources |
| **High-risk web research** (OSINT, threat intelligence) | Pod discarded after session; no persistent artefacts |
| **Regulated industry compliance** | Traffic stays on-premises -> full audit log via Kubernetes logging |
| **Air-gapped or sovereign cloud** | Runs fully on-premises with no external SaaS dependency |

---

## Remote Application Isolation (RAI) — beyond the browser

abcdesktop.io extends the isolation model beyond web browsing to **all applications**. Each application launched within a user session runs as its own **ephemeral container** inside the user pod:

- Applications are isolated from each other at the container boundary
- An application compromise cannot access another application's memory or filesystem
- Applications are discarded at session end, leaving no artefacts

This is **Remote Application Isolation (RAI)** is a superset of RBI that applies the same containment model to office suites, email clients, PDF readers, and any other application delivered through the platform.

---

## Comparison: open source RBI vs. commercial RBI

| | abcdesktop.io (open source) | Commercial RBI (SaaS) |
|---|---|---|
| **Cost** | Infrastructure only -> no per-seat fee | $5–$25 / user / month typically |
| **Data routing** | Your own infrastructure | Vendor cloud |
| **Deployment** | Self-hosted on Kubernetes | Vendor-managed SaaS |
| **Source code** | Open source (Apache 2.0) | Closed source |
| **Customization** | Full control | Limited to vendor options |
| **Air-gap / sovereign** | ✅ Fully supported | ❌ Not possible |
| **Application isolation** | ✅ RAI included | ⚠️ Browser-only for most vendors |

---

## Get started with open source RBI

<div class="grid cards" markdown>

-   :material-script-text-play-outline: **Quick install — script**

    ---

    Deploy abcdesktop.io on Kubernetes in minutes and get Remote Browser Isolation running immediately.

    [:octicons-arrow-right-24: Install with script](../install/4.4/script.md)

-   :material-kubernetes: **Production install — Helm**

    ---

    Helm-based deployment with full values customization for production environments.

    [:octicons-arrow-right-24: Install with Helm](../install/4.4/helm.md)

-   :material-rocket-launch-outline: **Live demo**

    ---

    Try Remote Browser Isolation in your browser — no installation, no sign-up.

    [:octicons-arrow-right-24: demo.gcp.abcdesktop.com](https://demo.gcp.abcdesktop.com)

</div>

---

## Frequently asked questions about open source RBI

??? question "What is the difference between Remote Browser Isolation and a VPN?"
    A VPN encrypts the network connection between the user's device and the corporate network but does not prevent malicious web content from executing on the endpoint. With Remote Browser Isolation, web content never reaches the endpoint — it executes on the server and only a pixel stream is delivered. RBI and VPN are complementary, not interchangeable.

??? question "Does abcdesktop.io RBI work with any web browser on the client side?"
    Yes. The user accesses abcdesktop.io from any HTML5-capable browser — Chrome, Firefox, Safari, Edge — on any operating system. No browser extension or plugin is required. The client-side browser is only a display terminal for the pixel stream.

??? question "How is the abcdesktop.io RBI session terminated?"
    Sessions are terminated by the user (logout) or automatically by the garbage collector after a configurable inactivity timeout (default: 15 minutes in the demo). At termination, the Kubernetes pod is deleted — all ephemeral container state is lost. PersistentVolumeClaims (user home directories) are retained if configured.

??? question "Can abcdesktop.io RBI enforce egress filtering for user pods?"
    Yes. Kubernetes NetworkPolicies are applied to user pods by default. Egress rules can be configured to restrict which external destinations the browser pod can reach, implementing domain allowlisting at the network layer. See the [network policy documentation](../advanced/4.4/networkpolicy/netpol.md).

??? question "Is abcdesktop.io suitable as a Menlo Security or Zscaler alternative?"
    For organizations that need data sovereignty, air-gap capability, or want to eliminate per-seat SaaS costs, abcdesktop.io is a viable self-hosted alternative for the core RBI use case. The primary difference is operational model: abcdesktop.io requires a Kubernetes cluster and operational expertise, whereas commercial SaaS vendors abstract that infrastructure layer.

??? question "What authentication methods does abcdesktop.io support for RBI sessions?"
    abcdesktop.io supports OAuth2/OIDC (Google, GitHub, Microsoft, Keycloak), LDAP/LDAPS, Active Directory, anonymous authentication, and SSL mutual authentication. This makes it integrable with existing enterprise identity providers without additional federation infrastructure.
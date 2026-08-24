---
title: "Self-Hosted VDI: Run Your Own Virtual Desktop Infrastructure with abcdesktop.io"
description: "Looking for a self-hosted VDI solution? abcdesktop.io is a free, open source virtual desktop platform that runs entirely on your own Kubernetes cluster — no SaaS, no vendor cloud, full data sovereignty."
keywords: self-hosted VDI, self hosted VDI, on-premise VDI, self-hosted DaaS, on-premises virtual desktop, self-hosted virtual desktop infrastructure, open source self-hosted VDI, VDI on-premises Kubernetes, private VDI, sovereign VDI, self-managed VDI, air-gap VDI
tags:
  - solutions
  - self-hosted
  - VDI
faq_schema:
  - q: "What infrastructure do I need to self-host abcdesktop.io?"
    a: "A Kubernetes cluster with at least one node and 4 GB of available RAM. For production, a multi-node cluster with persistent storage (NFS or CSI-compatible) and a load balancer or ingress controller is recommended. abcdesktop.io runs on bare metal, VMs, or any cloud Kubernetes service."
  - q: "Can I self-host abcdesktop.io without internet access?"
    a: "Yes. After the initial image pull, abcdesktop.io runs fully offline with no licensing callbacks, telemetry endpoints, or external API calls at runtime. Container images can be mirrored to a private registry for fully air-gapped environments."
  - q: "How many concurrent users can a self-hosted abcdesktop.io deployment support?"
    a: "There is no software-imposed session cap. Capacity depends on infrastructure: each user session consumes roughly 500 MB to 2 GB of RAM. Adding Kubernetes nodes scales capacity linearly."
  - q: "Can I use abcdesktop.io as a self-hosted alternative to Azure Virtual Desktop?"
    a: "Yes. abcdesktop.io provides browser-accessible virtual desktops with application isolation, without dependency on Microsoft Azure. The key difference: AVD offers tighter Microsoft 365 integration; abcdesktop.io delivers Linux desktops and applications on your own infrastructure."
---

# Self-Hosted VDI: Your Own Virtual Desktop Infrastructure, No Vendor Cloud Required

**Self-hosted VDI** means running your virtual desktop infrastructure on your own servers, not routing user sessions through a vendor's cloud. Every desktop session, every application, and every byte of user data stays within your own infrastructure perimeter.

abcdesktop.io is a free, open source VDI platform built for Kubernetes. It deploys entirely on your own cluster, with no external dependency on a vendor control plane, no telemetry, and no per-seat licensing.

[:material-rocket-launch-outline: **Try abcdesktop.io — Live Demo**](https://demo.gcp.abcdesktop.com){ .md-button .md-button--primary }

---

## Why self-host your VDI?

Organizations choose self-hosted VDI for four main reasons:

### 1. Data sovereignty and compliance

In cloud-delivered VDI, desktop sessions are processed on the vendor's infrastructure. For organizations subject to **GDPR, HIPAA, FedRAMP, NIS2, or sector-specific regulations**, routing user sessions and application data through a third-party cloud may be non-compliant by default.

With abcdesktop.io, every session runs on your Kubernetes cluster, on-premises, in your private cloud, or in a government/sovereign cloud region. No data leaves your perimeter.

### 2. Total cost of ownership

Cloud VDI and SaaS DaaS platforms charge per user per month: **Azure Virtual Desktop, Citrix DaaS, VMware Horizon Cloud** all carry per-seat fees that compound at scale. Self-hosting shifts the cost structure to infrastructure only, hardware or IaaS compute, without per-user licensing.

| Model | Cost structure |
|---|---|
| SaaS / cloud VDI | Per-seat monthly fee + infrastructure |
| Self-hosted VDI (abcdesktop.io) | Infrastructure only — zero licensing fee |

### 3. No vendor lock-in

SaaS VDI platforms tie your desktop delivery to the vendor's roadmap, pricing changes, and service continuity. A vendor discontinuing a tier or changing pricing forces a migration under time pressure. abcdesktop.io is fully open source so you own the platform, the data, and the migration path.

### 4. Air-gap and offline capability

Some environments, for example defense, industrial control, classified networks cannot route traffic to the public internet at all. Cloud VDI is structurally incompatible with these requirements. abcdesktop.io runs fully offline after initial deployment, with no check-in or licensing callbacks.

---

## How abcdesktop.io implements self-hosted VDI

abcdesktop.io deploys as a set of Kubernetes workloads on your existing cluster. There are no external SaaS components.

### Deployment model

```
Your infrastructure (on-premises / private cloud / sovereign IaaS)
  └── Kubernetes cluster
        ├── abcdesktop.io control plane (pyos, router, console)
        ├── MongoDB (session state)
        └── User pods (one per active session)
              ├── Desktop environment (X11)
              ├── Application containers (ephemeral)
              ├── PulseAudio / CUPS
              └── noVNC → WebSocket → user browser
```

Everything above runs inside your cluster. User browsers connect via HTTPS/WSS to your ingress. No outbound call to a vendor API is required at runtime.

### Authentication — integrate with your existing identity

Self-hosted VDI means your identity provider stays in-house too. abcdesktop.io supports:

- **LDAP / LDAPS** — connect to any RFC 4511-compliant directory
- **Active Directory** — including Kerberos and NTLM authentication
- **OAuth2 / OIDC** — Keycloak, Authentik, Microsoft Entra ID, Google Workspace
- **SSL mutual authentication** — client certificate-based login for high-assurance environments
- **Anonymous** — for kiosk or evaluation deployments

### Storage — keep user data on your infrastructure

Home directories and persistent user data are stored on your own storage backend:

- **NFS** — any NFS-compatible storage array or server
- **HostPath** — local node storage for single-node or development clusters
- **Any CSI-compatible storage class** — Rook/Ceph, Longhorn, Portworx, NetApp Trident, and others

---

## Supported self-hosting environments

| Environment | Supported |
|---|---|
| On-premises bare metal | ✅ |
| On-premises VM cluster (VMware, Proxmox) | ✅ |
| Kind / MiniKube (evaluation) | ✅ |
| Private cloud (OpenStack, Nutanix) | ✅ |
| Sovereign / government IaaS | ✅ |
| Amazon EKS (self-managed region) | ✅ |
| Microsoft AKS | ✅ |
| Google GKE | ✅ |
| Air-gapped / offline cluster | ✅ |

---

## Self-hosted VDI use cases

| Use case | Why self-hosted |
|---|---|
| **Public sector / government** | Data sovereignty; cannot use foreign cloud infrastructure |
| **Financial services** | Regulatory compliance (DORA, GDPR); audit trail ownership |
| **Healthcare** | HIPAA / HDS compliance; patient data stays on-premises |
| **Defense / classified** | Air-gap requirement; no internet-routable traffic |
| **Education / universities** | Large user populations; cost at scale makes SaaS prohibitive |
| **Industrial / OT environments** | Network segmentation; offline operation during connectivity loss |
| **MSPs / IT service providers** | Multi-tenant deployment on own infrastructure, resold to clients |

---

## Self-hosted VDI vs. cloud VDI comparison

| | abcdesktop.io (self-hosted) | Azure Virtual Desktop | Citrix DaaS | VMware Horizon Cloud |
|---|---|---|---|---|
| **Licensing cost** | Free (infrastructure only) | Per-user/month | Per-user/month | Per-user/month |
| **Data location** | Your infrastructure | Microsoft cloud | Citrix cloud | VMware cloud |
| **Air-gap support** | ✅ | ❌ | ❌ | ❌ |
| **Source code** | Open source | Closed | Closed | Closed |
| **Kubernetes-native** | ✅ | ❌ | ❌ | ❌ |
| **Vendor dependency** | None | Microsoft | Citrix | Broadcom |

---

## Get started with self-hosted VDI

<div class="grid cards" markdown>

-   :material-script-text-play-outline: **Install with script**

    ---

    Single-command deployment on any Kubernetes cluster. Evaluation-ready in minutes.

    [:octicons-arrow-right-24: Install with script](../install/4.4/script.md)

-   :material-kubernetes: **Install with Helm**

    ---

    Production-grade deployment via Helm chart. Full values customization for your environment.

    [:octicons-arrow-right-24: Install with Helm](../install/4.4/helm.md)

-   :material-cloud-outline: **Cloud provider guides**

    ---

    Step-by-step guides for AWS, Azure, GCP, OVHcloud, and DigitalOcean.

    [:octicons-arrow-right-24: Cloud provider guides](../index.md#quick-online-preview-release-44)

</div>

---

## Frequently asked questions about self-hosted VDI

??? question "What infrastructure do I need to self-host abcdesktop.io?"
    A Kubernetes cluster with at least one node and 4 GB of available RAM. For production deployments, a multi-node cluster with persistent storage (NFS or CSI-compatible) and a load balancer or ingress controller is recommended. abcdesktop.io runs on bare metal, VMs, or any cloud Kubernetes service.

??? question "Can I self-host abcdesktop.io without internet access?"
    Yes. After the initial image pull from Docker Hub (or your own private registry), abcdesktop.io runs fully offline. There are no licensing callbacks, telemetry endpoints, or external API calls required at runtime. Container images can be mirrored to a private registry for fully air-gapped environments.

??? question "How many concurrent users can a self-hosted abcdesktop.io deployment support?"
    Capacity depends entirely on your infrastructure. Each user session is a Kubernetes pod consuming roughly 500 MB–2 GB of RAM depending on active applications. The Kubernetes scheduler distributes pods across nodes; adding nodes scales capacity linearly. There is no software-imposed session cap.

??? question "Is self-hosted VDI harder to operate than SaaS VDI?"
    Self-hosted VDI requires Kubernetes operational skills: cluster maintenance, monitoring, storage management, and network configuration. If your organization already operates Kubernetes, the additional operational burden is low — abcdesktop.io is a standard set of Kubernetes workloads. If you are new to Kubernetes, the SaaS operational convenience of cloud VDI comes at the cost of data sovereignty and per-seat pricing.

??? question "How do I handle high availability in a self-hosted VDI deployment?"
    abcdesktop.io control plane components (router, pyos, MongoDB) support replicated deployment for HA. User pods are inherently isolated per-session; a node failure affects only the sessions running on that node. With a properly configured Kubernetes cluster (pod disruption budgets, anti-affinity rules, and multi-zone node groups), abcdesktop.io supports production-grade availability.

??? question "Can I use abcdesktop.io as a self-hosted alternative to Azure Virtual Desktop?"
    Yes, for organizations whose primary motivation for AVD is remote desktop delivery to internal users. abcdesktop.io provides the same core capability — browser-accessible virtual desktops with application isolation — without the dependency on Microsoft Azure. The key trade-off: AVD provides tighter integration with Microsoft 365 and Windows applications; abcdesktop.io delivers Linux desktops and Linux-native applications.
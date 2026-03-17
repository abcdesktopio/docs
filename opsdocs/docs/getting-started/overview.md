---
hide:
  - navigation   # masque le sidebar gauche
  - toc          # masque la table des matières droite
wizard_overview: true  
---
<style>
/* masque uniquement le premier H1 du contenu de la page */
.md-typeset > h1:first-of-type { display: none; } 
</style>

Choose your profile to follow the right path.

<div class="gs-diagram">

```mermaid
flowchart BT
    subgraph Platform["Platform"]
        K8S[("<span style='color:white'>☸ Kubernetes<br/>Cluster</span>")]:::infra
        REG[("<span style='color:white'>📦 Container<br/>Registry</span>")]:::infra
    end

    subgraph Actors["Who does what ?"]
        USR["<span style='color:white'>👤 User<br/>Uses the desktop</span>"]:::user
        DEV["<span style='color:white'>💻 Developer<br/>Builds & packages apps</span>"]:::dev
        ADM["<span style='color:white'>🖥️ Admin<br/>Installs & operates</span>"]:::admin
    end

    classDef admin fill:#2196f3,stroke:#0d47a1,stroke-width:1px # blue   500/900
    classDef dev   fill:#4caf50,stroke:#1b5e20,stroke-width:1px # green  500/900
    classDef user  fill:#9c27b0,stroke:#4a148c,stroke-width:1px # purple 500/900
    classDef infra fill:#9e9e9e,stroke:#212121,stroke-width:1px # grey   500/900

    ADM -->|"deploys"| K8S
    DEV -->|"publishes images"| REG
    REG -->|"pulled by"| K8S
    K8S -->|"runs sessions for"| USR
```

</div>

=== ":material-account: User"

    You use abcdesktop to access your applications from a browser.

    **Estimated time: ~xx min**

    | Step | Page | Time |
    |------|------|------|
    | 1 | [Overview](user/step1.md) | 2 min |
    | 2 | [...](user/step2.md) | 3 min |
    | 3 | [...](user/step3.md) | 5 min |

    [:material-arrow-right: Start here](user/step1.md){ .md-button .md-button--primary }

=== ":material-laptop: Developer"

    You build and package applications for abcdesktop.

    **Estimated time: ~xx min**

    | Step | Page | Time |
    |------|------|------|
    | 1 | [Overview](user/step1.md) | 2 min |
    | 2 | [...](user/step2.md) | 3 min |
    | 3 | [...](user/step3.md) | 5 min |

    [:material-arrow-right: Start here](developer/step1.md){ .md-button .md-button--primary }

=== ":material-server: Admin"

    You install, configure and operate abcdesktop for your organization.

    **Estimated time: ~xx min**

    | Step | Page | Time |
    |------|------|------|
    | 1 | [Prerequisites](admin/step1.md) | 5 min |
    | 2 | [Installation](admin/step2.md) | 10 min |
    | 3 | [Uninstall](admin/step3.md) | 5 min |

    [:material-arrow-right: Start here](admin/step1.md){ .md-button .md-button--primary }

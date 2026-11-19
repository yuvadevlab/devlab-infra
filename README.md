# Infrastructure Control Plane (`devlab-infra`)

Central infrastructure repository, service fleet catalog, and cloud topology authority for the **Yuva DevLab Ecosystem**.

---

## 1. Overview

`devlab-infra` is the central infrastructure repository, service fleet catalog, and cloud topology authority for the **Yuva DevLab Ecosystem**. 

It codifies:
- **Service Catalog**: Authoritative registry of all deployable HTTP APIs, WebSocket servers, and Cloud Run Jobs across the ecosystem.
- **Port Registry**: Strict port allocation preventing collisions during local development and multi-container environments.
- **Secret Management**: Google Secret Manager (GSM) definitions and IAM bindings.
- **Ingress & Routing**: Custom domain mappings, health check paths, and load balancer rules.

---

## 2. The 3-Tier Ecosystem Architecture

```
┌─────────────────────────┐          ┌─────────────────────────┐          ┌─────────────────────────┐
│      devlab-infra       │          │         .github         │          │    Application Repos    │
│  (Cloud Infrastructure) │          │  (CI/CD Pipeline Engine)│          │  (fin-ai, knowledge-ai) │
│                         │          │                         │          │                         │
│ • Service Catalog       ├─────────►│ • Reusable Docker Build ├─────────►│ • Product Code         │
│ • Secret Manager (GSM)  │          │ • Reusable Cloud Run    │          │ • Multi-stage Dockerfile│
│ • Port Allocation Table │          │ • Quality Gate Linter   │          │ • Lightweight Workflows │
└─────────────────────────┘          └─────────────────────────┘          └─────────────────────────┘
```

---

## 3. Directory Layout

```
devlab-infra/
├── catalog/
│   ├── services.yaml          # Master Service Registry (all 20+ services, compute limits, archetypes)
│   └── routes.yaml            # Public domains & ingress mapping
├── gcp/
│   ├── secret-manager/
│   │   └── secrets-catalog.yaml # GSM catalog (zero plain-text secrets in git)
│   └── scripts/
│       └── provision-secrets.sh # Shell automation to provision GSM secrets
├── docs/
│   ├── ARCHITECTURE.md        # Architectural guide for Cloud Run & scaling
│   ├── PORT_ALLOCATION.md     # Authoritative port registry
│   └── RUNBOOK.md             # Rollback & emergency operations runbook
└── README.md
```

---

## 4. Compute Archetypes

Every service in the fleet is categorized into one of three compute patterns in [catalog/services.yaml](file:///Users/yuvarajpattabi/Yuva/yuva-devlab/repos/devlab-infra/catalog/services.yaml):

| Archetype | Compute Engine | Behavior | Examples |
| :--- | :--- | :--- | :--- |
| **`http-api`** | Cloud Run Service | Scales 0 ↔ N instances, concurrency 80, CPU throttled | `devlab-portal-api`, `finai-api`, `knowledge-ai-api` |
| **`websocket-server`** | Cloud Run Service | No CPU throttling, session affinity, 3600s timeout | `orchestr-ai-intelligence`, `knowledge-ai-realtime` |
| **`background-job`** | Cloud Run Job | Runs batch/cron to completion, exits, \$0 when idle | `knowledge-ai-crawler`, `quant-ai-engine` |

---

## 5. Operations & Runbooks

- **Instant Rollback**: See [docs/RUNBOOK.md](file:///Users/yuvarajpattabi/Yuva/yuva-devlab/repos/devlab-infra/docs/RUNBOOK.md) for 2-second Cloud Run traffic shifting.
- **Port Allocation**: Consult [docs/PORT_ALLOCATION.md](file:///Users/yuvarajpattabi/Yuva/yuva-devlab/repos/devlab-infra/docs/PORT_ALLOCATION.md) before spinning up new services.
- **Adding a Service**: Follow the onboarding checklist in [docs/RUNBOOK.md](file:///Users/yuvarajpattabi/Yuva/yuva-devlab/repos/devlab-infra/docs/RUNBOOK.md).

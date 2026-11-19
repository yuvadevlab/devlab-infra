# Infrastructure & Deployment Architecture

Global infrastructure, deployment pipelines, and scaling topology for the Yuva DevLab ecosystem.

---

## 1. Architectural Philosophy

Yuva DevLab follows a **3-Tier Separation of Concerns**:

```
[Tier 1: devlab-infra]         [Tier 2: .github]             [Tier 3: App Repos]
Cloud State & Catalog         CI/CD Pipeline Engine         Product Source Code
├── Service Catalog           ├── reusable-docker-build     ├── fin-ai
├── Google Secret Manager     ├── reusable-deploy-cloudrun  ├── devlab-portal
└── Port Registry             └── reusable-deploy-job       └── knowledge-ai
```

1. **`devlab-infra` (The Cloud State)**:
   - Owns the declarative service catalog, port allocations, and Google Secret Manager (GSM) integration.
   - It answers: *"What services exist and what are their resource allocations?"*

2. **`.github` (The CI/CD Engine)**:
   - Owns the reusable workflows (BuildKit, GHA caching, WIF auth, Cloud Run deploy).
   - It answers: *"How does code move safely from a Git commit to a running container?"*

3. **Application Repositories (The Code)**:
   - Own product features, tests, and Dockerfiles.
   - They contain **zero imperative deployment scripts**, only lightweight declarative workflow calls.

---

## 2. Compute Archetypes

Every service in the ecosystem maps to one of three compute archetypes:

### Archetype 1: Stateless HTTP APIs (`http-api`)
- **Examples**: `devlab-portal-api`, `finai-api`, `knowledge-ai-api`
- **Platform**: Google Cloud Run Service
- **Characteristics**:
  - Scales 0 ↔ N instances based on request concurrency (default: 80).
  - CPU is throttled when not processing requests to minimize cost.
  - `--cpu-boost` is enabled for 2x CPU during cold boot.
  - Production (`main`) runs with `min-instances: 1` for zero cold starts.

### Archetype 2: Realtime Streaming & WebSockets (`websocket-server`)
- **Examples**: `orchestr-ai-intelligence`, `knowledge-ai-realtime`
- **Platform**: Google Cloud Run Service (Long-lived mode)
- **Characteristics**:
  - `--cpu-throttling` is disabled (CPU is always allocated).
  - `--session-affinity` is enabled so sequential SSE/WebSocket connections stay pinned.
  - Request timeout is extended up to 3600 seconds.

### Archetype 3: Batch Crawlers, Scrapers & Jobs (`background-job`)
- **Examples**: `knowledge-ai-crawler`, `quant-ai-engine`, database migrations
- **Platform**: Google Cloud Run Jobs (NOT Services)
- **Characteristics**:
  - Run to completion and terminate immediately.
  - Incur \$0 cost when idle.
  - Triggered on a cadence via Cloud Scheduler (e.g. `0 */3 * * *`).

---

## 3. Secret Management via Google Secret Manager (GSM)

Raw database strings and cryptographic seeds are **never** committed to Git, passed via plain-text environment variables, or stored redundantly across 20 GitHub repositories.

1. Secrets are stored centrally in **Google Secret Manager**.
2. Cloud Run instances are granted `roles/secretmanager.secretAccessor`.
3. Workflows mount secrets by reference:
   `--set-secrets=DATABASE_URL=finai-db-url:latest`
4. Rotating a secret in GSM updates running containers without triggering a code rebuild.

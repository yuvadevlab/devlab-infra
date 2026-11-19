# Ecosystem Port Allocation Registry

Canonical port registry for all local development servers, container bindings, and microservices across `/Users/yuvarajpattabi/Yuva/yuva-devlab/repos/*`.

---

## 1. Port Allocation Strategy

To avoid collision during parallel local development and when running multi-container Docker environments:
- **`3000 – 3099`**: Web Frontend Applications (Next.js / Vite / Remix)
- **`4000 – 4099`**: Core Backend APIs (Node.js / Express / Fastify / NestJS)
- **`8080 – 8099`**: Python AI Engines, Scrapers, Crawlers & FastAPI Microservices
- **`9000 – 9099`**: Native Go Agents, Telemetry Collectors & Metrics Endpoints

---

## 2. Authoritative Allocation Table

| Port | Service Name | Repository | Runtime | Archetype |
| :--- | :--- | :--- | :--- | :--- |
| **`3000`** | `devlab-portal-web` | `devlab-portal` | Node 24 | Web Frontend |
| **`3001`** | `finai-web` | `fin-ai` | Node 24 | Web Frontend |
| **`3002`** | `orchestr-ai-web` | `orchestr-ai` | Node 22 | Web Frontend |
| **`3003`** | `devlab-logs-web` | `devlab-logs` | Node 22 | Web Frontend |
| **`3004`** | `vital-ai-web` | `vital-ai` | Node 24 | Web Frontend |
| **`3006`** | `incident-ai-web` | `incident-ai` | Node 22 | Web Frontend |
| **`3007`** | `quant-ai-web` | `quant-ai` | Node 22 | Web Frontend |
| **`3008`** | `knowledge-ai-web` | `knowledg-ai` | Node 24 | Web Frontend |
| **`4000`** | `devlab-portal-api` | `devlab-portal` | Node 24 | HTTP API |
| **`4001`** | `finai-api` | `fin-ai` | Node 24 | HTTP API |
| **`4002`** | `orchestr-ai-api` | `orchestr-ai` | Node 22 | HTTP API |
| **`4003`** | `devlab-logs-api` | `devlab-logs` | Node 22 | HTTP API |
| **`4004`** | `vital-ai-api` | `vital-ai` | Python 3.12 | HTTP API |
| **`4006`** | `incident-ai-api` | `incident-ai` | Node 22 | HTTP API |
| **`4007`** | `quant-ai-api` | `quant-ai` | Node 22 | HTTP API |
| **`4008`** | `knowledge-ai-api` | `knowledg-ai` | Node 24 | HTTP API |
| **`4009`** | `knowledge-ai-realtime` | `knowledg-ai` | Node 24 | WebSocket Server |
| **`8082`** | `orchestr-ai-intelligence` | `orchestr-ai` | Python 3.12 | WebSocket / Agent |
| **`8083`** | `orchestr-ai-crawler` | `orchestr-ai` | Python 3.12 | Background Job |
| **`8085`** | `devlab-guard-service` | `devlab-guard` | Python 3.12 | Security Daemon |
| **`8087`** | `quant-ai-engine` | `quant-ai` | Python 3.12 | Background Job |
| **`8088`** | `knowledge-ai-crawler` | `knowledg-ai` | Python 3.12 | Background Job |
| **`8089`** | `knowledge-ai-scraper` | `knowledg-ai` | Python 3.12 | Background Job |
| **`9003`** | `devlab-logs-collector` | `devlab-logs` | Go 1.23 | Log Collector Agent |

---

## 3. Invariant Rule
Before creating any new service or modifying local development server configuration, check this file to claim an unallocated port number in the corresponding range.

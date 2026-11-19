# Operations & Deployment Runbook

Standard operating procedures for deployments, rollbacks, and incident mitigation across the ecosystem.

---

## 1. Instant 2-Second Rollback in Cloud Run

Because every container is tagged with an immutable Git commit SHA (`:${GITHUB_SHA}`), rolling back a problematic release does **not** require rebuilding code.

### Option A: Shift Traffic via CLI (Instant)
```bash
# List previous revisions
gcloud run revisions list --service=finai-api --region=asia-southeast1

# Route 100% of user traffic back to the previous healthy revision
gcloud run services update-traffic finai-api \
  --region=asia-southeast1 \
  --to-revisions=PREVIOUS_REVISION_NAME=100
```

### Option B: Deploy Previous Image Tag
```bash
# Deploy a known good Git SHA image
gcloud run deploy finai-api \
  --image=asia-southeast1-docker.pkg.dev/project-cbe181a6-46e7-4c7c-8e8/cloud-run-source-deploy/finai-api:<GOOD_COMMIT_SHA> \
  --region=asia-southeast1
```

---

## 2. Onboarding a New Service

When adding a new service (e.g. in `knowledge-ai` or `quant-ai`):

1. **Claim a Port**:
   - Open [PORT_ALLOCATION.md](file:///Users/yuvarajpattabi/Yuva/yuva-devlab/repos/devlab-infra/docs/PORT_ALLOCATION.md) and claim an unallocated port number in the proper range.
2. **Register in Catalog**:
   - Add the service specification to [catalog/services.yaml](file:///Users/yuvarajpattabi/Yuva/yuva-devlab/repos/devlab-infra/catalog/services.yaml) with its archetype, compute limits, and required secrets.
3. **Provision Secrets in GSM**:
   - Add required database or third-party API keys to [gcp/secret-manager/secrets-catalog.yaml](file:///Users/yuvarajpattabi/Yuva/yuva-devlab/repos/devlab-infra/gcp/secret-manager/secrets-catalog.yaml) and create them in Google Secret Manager.
4. **Wire the Workflow**:
   - In the application repository, create `.github/workflows/deploy.yml` calling `yuvadevlab/.github/.github/workflows/reusable-deploy-cloudrun.yml@main`.

---

## 3. Rotating Secrets in Google Secret Manager

1. Open Google Secret Manager in the GCP Console (or use `gcloud`):
   ```bash
   echo -n "new-super-secret-database-url" | gcloud secrets versions add finai-db-url --data-file=-
   ```
2. Cloud Run services referencing `finai-db-url:latest` will automatically pick up the new secret version on next container startup.
3. To trigger an immediate rolling restart of all active instances without rebuilding the image:
   ```bash
   gcloud run services update finai-api --region=asia-southeast1
   ```

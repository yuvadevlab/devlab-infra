#!/usr/bin/env bash
# ==============================================================================
# Google Secret Manager Provisioner
# Declarative secret provisioning script for Google Cloud Secret Manager.
# ==============================================================================

set -euo pipefail

PROJECT_ID="${GCP_PROJECT:-project-cbe181a6-46e7-4c7c-8e8}"
REGION="asia-southeast1"

echo "=== Initializing Google Secret Manager in $PROJECT_ID ==="

# Enable Secret Manager API if not active
gcloud services enable secretmanager.googleapis.com --project="$PROJECT_ID" --quiet

SECRETS=(
  "gemini-api-key:Google AI Studio / Gemini API Master Key"
  "devlab-portal-db-url:Production Postgres Database URL for Portal"
  "devlab-portal-session-secret:Session HMAC signing key for Portal Auth"
  "finai-db-url:Neon Postgres Database URL for FinAI"
  "orchestrai-db-url:Postgres Database URL for OrchestrAI Coordinator"
  "orchestrai-redis-url:Redis URL for OrchestrAI PubSub and Queue"
  "knowledgeai-db-url:Postgres/Vector Database URL for KnowledgeAI"
)

for entry in "${SECRETS[@]}"; do
  SECRET_NAME="${entry%%:*}"
  SECRET_DESC="${entry#*:}"

  if gcloud secrets describe "$SECRET_NAME" --project="$PROJECT_ID" >/dev/null 2>&1; then
    echo "✓ Secret '$SECRET_NAME' already exists."
  else
    echo "Creating secret '$SECRET_NAME'..."
    gcloud secrets create "$SECRET_NAME" \
      --project="$PROJECT_ID" \
      --replication-policy="automatic" \
      --labels="managed-by=devlab-infra" \
      --quiet
    echo "✓ Created secret '$SECRET_NAME'."
  fi
done

echo "=== Google Secret Manager Provisioning Completed ==="

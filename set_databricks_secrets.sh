#!/usr/bin/env bash
set -euo pipefail

# Check that required vars are set
for var in AZURE_STORAGE_ACCOUNT_NAME AZURE_STORAGE_ACCOUNT_KEY AZURE_CONTAINER_NAME; do
  if [[ -z "${!var:-}" ]]; then
    echo "Error: \$${var} is not set." >&2
    exit 1
  fi
done

SCOPE="streaming"

echo "Creating/updating secrets in Databricks scope '$SCOPE'..."

databricks secrets put \
  --scope "$SCOPE" \
  --key AZURE_STORAGE_ACCOUNT_NAME \
  --string-value "$AZURE_STORAGE_ACCOUNT_NAME"

databricks secrets put \
  --scope "$SCOPE" \
  --key AZURE_STORAGE_ACCOUNT_KEY \
  --string-value "$AZURE_STORAGE_ACCOUNT_KEY"

databricks secrets put \
  --scope "$SCOPE" \
  --key AZURE_CONTAINER_NAME \
  --string-value "$AZURE_CONTAINER_NAME"

echo "Done. Current keys in scope '$SCOPE':"
databricks secrets list --scope "$SCOPE"

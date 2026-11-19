#!/usr/bin/env python3
"""
Infrastructure Catalog Validator
Validates schema conformance, port uniqueness (zero collisions), and cross-catalog integrity.
"""

import sys
from pathlib import Path
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SERVICES_FILE = REPO_ROOT / "catalog" / "services.yaml"
ROUTES_FILE = REPO_ROOT / "catalog" / "routes.yaml"
SECRETS_FILE = REPO_ROOT / "gcp" / "secret-manager" / "secrets-catalog.yaml"

VALID_ARCHETYPES = {"http-api", "websocket-server", "background-job", "web-frontend"}


def load_yaml(path: Path):
    if not path.is_file():
        print(f"❌ Error: Required file not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_catalog():
    errors = []
    warnings = []

    print("🔍 [1/3] Validating Services Catalog...")
    services_data = load_yaml(SERVICES_FILE)
    services = services_data.get("services", [])
    if not services:
        errors.append("No services declared in catalog/services.yaml")

    service_ids = set()
    ports_map = {}

    for s in services:
        sid = s.get("id")
        if not sid:
            errors.append(f"Service missing 'id': {s}")
            continue

        if sid in service_ids:
            errors.append(f"Duplicate service ID detected: '{sid}'")
        service_ids.add(sid)

        archetype = s.get("archetype")
        if archetype not in VALID_ARCHETYPES:
            errors.append(f"Service '{sid}' has invalid archetype: '{archetype}' (allowed: {VALID_ARCHETYPES})")

        port = s.get("port")
        if port is None:
            errors.append(f"Service '{sid}' is missing required 'port' declaration")
        else:
            if not isinstance(port, int) or port < 1024 or port > 65535:
                errors.append(f"Service '{sid}' port {port} is invalid (must be int 1024-65535)")
            elif port in ports_map:
                prev_id = ports_map[port]
                errors.append(f"💥 Port collision detected! Port {port} is assigned to both '{prev_id}' and '{sid}'")
            else:
                ports_map[port] = sid

    print(f"   ✓ Verified {len(services)} services across {len(ports_map)} unique allocated ports.")

    print("🔍 [2/3] Validating Secret Manager Catalog...")
    secrets_data = load_yaml(SECRETS_FILE)
    catalog_secrets = {sec.get("name"): sec for sec in secrets_data.get("secrets", [])}

    # Verify secret references in services
    for s in services:
        sid = s.get("id")
        for secret_ref in s.get("secrets", []):
            sname = secret_ref.get("secret_name")
            if sname not in catalog_secrets:
                errors.append(
                    f"Service '{sid}' references secret '{sname}' not found in secrets-catalog.yaml"
                )

    print(f"   ✓ Verified {len(catalog_secrets)} secrets and references.")

    print("🔍 [3/3] Validating Ingress & Routes Topology...")
    routes_data = load_yaml(ROUTES_FILE)
    routes = routes_data.get("routing", {})

    for env_name in ("production", "development"):
        env_routes = routes.get(env_name, {})
        for api_id, cfg in env_routes.get("apis", {}).items():
            if api_id not in service_ids:
                warnings.append(
                    f"Route '{env_name}.apis.{api_id}' targets service ID not in services.yaml"
                )
            if not cfg.get("cloud_run_url"):
                errors.append(f"Route '{env_name}.apis.{api_id}' missing 'cloud_run_url'")

    print("   ✓ Verified routing maps.")

    print("\n" + "=" * 60)
    if warnings:
        print(f"⚠️  {len(warnings)} Warnings:")
        for w in warnings:
            print(f"   - {w}")

    if errors:
        print(f"\n❌ Validation FAILED with {len(errors)} errors:")
        for e in errors:
            print(f"   - {e}")
        sys.exit(1)

    print("🎉 All validation checks PASSED! Catalog, Ports, and GSM definitions are consistent.")
    print("=" * 60)


if __name__ == "__main__":
    validate_catalog()

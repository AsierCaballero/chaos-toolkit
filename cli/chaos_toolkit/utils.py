"""Utility helpers for chaos-toolkit."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


def validate_k8s_name(name: str) -> bool:
    """Validate a Kubernetes resource name (RFC 1123)."""
    return bool(re.match(r"^[a-z0-9]([a-z0-9\-]{0,61}[a-z0-9])?$", name))


def check_kubectl() -> bool:
    """Check if kubectl is available on the PATH."""
    try:
        subprocess.run(["kubectl", "version", "--client"], capture_output=True, check=False)
        return True
    except FileNotFoundError:
        return False


def find_manifests(path: str | Path) -> list[Path]:
    """Find all YAML manifests in a directory tree."""
    base = Path(path).expanduser()
    if base.is_file() and base.suffix in (".yaml", ".yml"):
        return [base]
    return sorted(base.rglob("*.yaml")) + sorted(base.rglob("*.yml"))


def merge_dicts(base: dict, override: dict) -> dict:
    """Deep merge two dictionaries."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

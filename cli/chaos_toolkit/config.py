"""Configuration loader for chaos-toolkit."""

import os
from pathlib import Path

import yaml

DEFAULT_CONFIG = {
    "namespace": "default",
    "litmus_endpoint": "",
    "poll_interval": 5,
    "timeout": 300,
}


def load_config(path: str = "~/.chaos/config.yaml") -> dict:
    """Load configuration from a YAML file, merging with defaults."""
    config = DEFAULT_CONFIG.copy()
    config_path = Path(path).expanduser()
    if config_path.exists():
        with open(config_path) as f:
            user_config = yaml.safe_load(f) or {}
        config.update(user_config)
    env_overrides = {
        "namespace": os.getenv("CHAOS_NAMESPACE"),
        "litmus_endpoint": os.getenv("LITMUS_ENDPOINT"),
    }
    for key, value in env_overrides.items():
        if value is not None:
            config[key] = value
    return config

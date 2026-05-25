"""Tests for chaos_toolkit.config module."""

import os
import tempfile
from pathlib import Path

import pytest
import yaml

from chaos_toolkit.config import load_config


def test_load_config_defaults():
    config = load_config("/nonexistent/path/config.yaml")
    assert config["namespace"] == "default"
    assert config["poll_interval"] == 5


def test_load_config_from_file():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump({"namespace": "chaos-ns", "poll_interval": 10}, f)
        f.flush()
        config = load_config(f.name)
        assert config["namespace"] == "chaos-ns"
        assert config["poll_interval"] == 10
        assert config["timeout"] == 300


def test_load_config_env_override():
    os.environ["CHAOS_NAMESPACE"] = "env-ns"
    config = load_config("/nonexistent/path/config.yaml")
    assert config["namespace"] == "env-ns"
    del os.environ["CHAOS_NAMESPACE"]


def test_load_config_file_overrides_defaults():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump({"namespace": "file-ns"}, f)
        config = load_config(f.name)
        assert config["namespace"] == "file-ns"
        assert config["poll_interval"] == 5

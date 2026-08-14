"""Tests for chaos_toolkit.experiments module."""

import yaml

from chaos_toolkit.experiments import TEMPLATES, Experiment


class TestExperiment:
    def test_create_pod_delete_experiment(self):
        exp = Experiment(
            name="test-pod-delete",
            kind="pod-delete",
            target="nginx",
            duration=30,
            namespace="default",
        )
        engine = exp.to_chaos_engine()
        assert engine["apiVersion"] == "litmuschaos.io/v1alpha1"
        assert engine["kind"] == "ChaosEngine"
        assert engine["metadata"]["name"] == "test-pod-delete"
        assert engine["spec"]["engineState"] == "active"
        assert len(engine["spec"]["experiments"]) == 1

    def test_experiment_with_params(self):
        exp = Experiment(
            name="cpu-stress",
            kind="cpu-hog",
            target="app-container",
            params={"CPU_CORES": "2", "CPU_LOAD": "80"},
        )
        engine = exp.to_chaos_engine()
        env = engine["spec"]["experiments"][0]["spec"]["components"]["env"]
        env_map = {e["name"]: e["value"] for e in env}
        assert env_map["CPU_CORES"] == "2"
        assert env_map["CPU_LOAD"] == "80"

    def test_experiment_renders_as_valid_yaml(self):
        exp = Experiment(name="valid-exp", kind="pod-delete", target="target")
        engine = exp.to_chaos_engine()
        yaml_str = yaml.dump(engine, default_flow_style=False)
        parsed = yaml.safe_load(yaml_str)
        assert parsed["metadata"]["name"] == "valid-exp"


class TestTemplates:
    def test_templates_defined(self):
        assert "pod-delete" in TEMPLATES
        assert "cpu-hog" in TEMPLATES
        assert "network-latency" in TEMPLATES

    def test_template_structure(self):
        for tpl in TEMPLATES.values():
            assert "kind" in tpl
            assert "description" in tpl
            assert "default_params" in tpl
            assert isinstance(tpl["default_params"], dict)

    def test_pod_delete_defaults(self):
        tpl = TEMPLATES["pod-delete"]
        assert tpl["default_params"]["TOTAL_CHAOS_DURATION"] == "60"
        assert tpl["default_params"]["FORCE"] == "true"

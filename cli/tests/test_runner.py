"""Tests for chaos_toolkit.runner module."""

from unittest.mock import patch, MagicMock
import yaml

from chaos_toolkit.runner import run_experiment, K8sClient


class TestRunExperiment:
    def test_run_experiment_parses_manifest(self, tmp_path):
        manifest = {
            "apiVersion": "litmuschaos.io/v1alpha1",
            "kind": "ChaosEngine",
            "metadata": {"name": "test-exp"},
            "spec": {
                "engineState": "active",
                "chaosServiceAccount": "litmus-admin",
                "experiments": [{"name": "pod-delete", "spec": {"components": {"env": []}}}],
            },
        }
        m = tmp_path / "manifest.yaml"
        m.write_text(yaml.dump(manifest))

        with patch.object(K8sClient, "apply_manifest") as mock_apply:
            mock_apply.return_value = {"metadata": {"name": "test-exp"}}
            with patch.object(K8sClient, "get_experiment") as mock_get:
                mock_get.return_value = {
                    "name": "test-exp",
                    "kind": "ChaosEngine",
                    "status": "Completed",
                    "verdict": "Pass",
                }
                result = run_experiment(str(m), "default", 30, True)

        assert result["success"] is True
        assert result["verdict"] == "Pass"

    def test_run_experiment_injects_duration(self, tmp_path):
        manifest = {
            "apiVersion": "litmuschaos.io/v1alpha1",
            "kind": "ChaosEngine",
            "metadata": {"name": "test-exp"},
            "spec": {
                "experiments": [{"name": "pod-delete", "spec": {"components": {"env": []}}}],
            },
        }
        m = tmp_path / "manifest.yaml"
        m.write_text(yaml.dump(manifest))

        def check_manifest(body):
            env = body["spec"]["experiments"][0]["spec"]["components"]["env"]
            assert any(e["name"] == "TOTAL_CHAOS_DURATION" and e["value"] == "120" for e in env)
            return {"metadata": {"name": "test-exp"}}

        with patch.object(K8sClient, "apply_manifest", side_effect=check_manifest):
            with patch.object(K8sClient, "get_experiment") as mock_get:
                mock_get.return_value = {"status": "Completed", "experiments": [{"verdict": "Pass"}]}
                result = run_experiment(str(m), "default", 120)

        assert result["success"] is True

    def test_run_experiment_api_error(self, tmp_path):
        manifest = {
            "apiVersion": "litmuschaos.io/v1alpha1",
            "kind": "ChaosEngine",
            "metadata": {"name": "test-exp"},
            "spec": {"experiments": [{"name": "pod-delete"}]},
        }
        m = tmp_path / "manifest.yaml"
        m.write_text(yaml.dump(manifest))

        from kubernetes.client.rest import ApiException
        exc = ApiException(status=403, reason="Forbidden")

        with patch.object(K8sClient, "apply_manifest", side_effect=exc):
            result = run_experiment(str(m), "default")

        assert result["success"] is False
        assert "403" in result["error"]

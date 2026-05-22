"""Kubernetes runner for chaos experiments."""

import logging
import time
from typing import Any

import yaml
from kubernetes import config
from kubernetes.client import CustomObjectsApi, CoreV1Api
from kubernetes.client.rest import ApiException

logger = logging.getLogger(__name__)


class K8sClient:
    def __init__(self, namespace: str = "default"):
        self.namespace = namespace
        self._custom_api = None
        self._core_api = None
        self._setup()

    def _setup(self):
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()
        self._custom_api = CustomObjectsApi()
        self._core_api = CoreV1Api()

    def apply_manifest(self, manifest: dict) -> dict:
        return self._custom_api.create_namespaced_custom_object(
            group="litmuschaos.io",
            version="v1alpha1",
            namespace=self.namespace,
            plural="chaosengines",
            body=manifest,
        )

    def get_experiments(self) -> list[dict[str, str]]:
        try:
            engines = self._custom_api.list_namespaced_custom_object(
                group="litmuschaos.io",
                version="v1alpha1",
                namespace=self.namespace,
                plural="chaosengines",
            )
        except ApiException as e:
            if e.status == 404:
                return []
            raise

        results = []
        for item in engines.get("items", []):
            results.append({
                "name": item["metadata"]["name"],
                "kind": "ChaosEngine",
                "status": item.get("status", {}).get("engineStatus", "Unknown"),
                "age": self._age(item["metadata"].get("creationTimestamp", "")),
            })
        return results

    def get_experiment(self, name: str) -> dict | None:
        try:
            engine = self._custom_api.get_namespaced_custom_object(
                group="litmuschaos.io",
                version="v1alpha1",
                namespace=self.namespace,
                plural="chaosengines",
                name=name,
            )
        except ApiException as e:
            if e.status == 404:
                return None
            raise

        status = engine.get("status", {})
        exp_result = (status.get("experiments") or [{}])[0]
        return {
            "name": engine["metadata"]["name"],
            "kind": "ChaosEngine",
            "status": status.get("engineStatus", "Unknown"),
            "verdict": exp_result.get("verdict", "N/A"),
            "started": engine["metadata"].get("creationTimestamp", "N/A"),
            "duration": exp_result.get("lastUpdatedAt", "N/A"),
        }

    def get_experiment_logs(self, name: str) -> str:
        pods = self._core_api.list_namespaced_pod(
            self.namespace, label_selector=f"chaosengine={name}"
        )
        if not pods.items:
            return "No experiment pods found."

        lines = []
        for pod in pods.items:
            try:
                log = self._core_api.read_namespaced_pod_log(
                    pod.metadata.name, self.namespace
                )
                lines.append(f"--- {pod.metadata.name} ---\n{log}")
            except ApiException:
                lines.append(f"--- {pod.metadata.name} ---\n(unable to retrieve logs)")
        return "\n".join(lines)

    def delete_experiment(self, name: str) -> bool:
        try:
            self._custom_api.delete_namespaced_custom_object(
                group="litmuschaos.io",
                version="v1alpha1",
                namespace=self.namespace,
                plural="chaosengines",
                name=name,
            )
            return True
        except ApiException:
            return False

    def _age(self, timestamp: str) -> str:
        if not timestamp:
            return "N/A"
        try:
            from datetime import datetime, timezone
            created = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            delta = datetime.now(timezone.utc) - created
            total_minutes = int(delta.total_seconds() // 60)
            if total_minutes < 60:
                return f"{total_minutes}m"
            hours = total_minutes // 60
            if hours < 24:
                return f"{hours}h"
            return f"{hours // 24}d"
        except (ValueError, TypeError):
            return "N/A"


def run_experiment(
    manifest_path: str,
    namespace: str,
    duration: int = 60,
    wait: bool = True,
    poll_interval: int = 5,
    timeout: int = 300,
) -> dict[str, Any]:
    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)

    manifest.setdefault("spec", {})
    manifest["spec"].setdefault("engineState", "active")

    for exp in manifest.get("spec", {}).get("experiments", []):
        env = exp.setdefault("spec", {}).setdefault("components", {}).setdefault("env", [])
        if not any(e.get("name") == "TOTAL_CHAOS_DURATION" for e in env):
            env.append({"name": "TOTAL_CHAOS_DURATION", "value": str(duration)})

    client = K8sClient(namespace)
    try:
        result = client.apply_manifest(manifest)
    except ApiException as e:
        logger.error("Failed to apply ChaosEngine: %s", e)
        return {"success": False, "error": f"API error: {e.status} {e.reason}"}

    name = result["metadata"]["name"]

    if not wait:
        return {"success": True, "name": name, "verdict": "Running"}

    elapsed = 0
    while elapsed < timeout:
        status = client.get_experiment(name)
        if status and status["status"] == "Completed":
            return {"success": True, "name": name, "verdict": status.get("verdict", "Pass")}
        time.sleep(poll_interval)
        elapsed += poll_interval

    return {"success": True, "name": name, "verdict": "Timeout"}


def list_experiments(namespace: str) -> list[dict]:
    return K8sClient(namespace).get_experiments()


def get_experiment_status(name: str, namespace: str) -> dict | None:
    return K8sClient(namespace).get_experiment(name)


def get_experiment_logs(name: str, namespace: str) -> str:
    return K8sClient(namespace).get_experiment_logs(name)


def describe_experiment(name: str, namespace: str) -> str | None:
    client = K8sClient(namespace)
    try:
        engine = client._custom_api.get_namespaced_custom_object(
            group="litmuschaos.io",
            version="v1alpha1",
            namespace=namespace,
            plural="chaosengines",
            name=name,
        )
    except ApiException:
        return None
    return yaml.dump(engine, default_flow_style=False)

def poll_experiment(name, namespace, timeout=300, interval=5):
    """Poll experiment status until completion or timeout."""
    import time
    client = K8sClient(namespace)
    elapsed = 0
    while elapsed < timeout:
        status = client.get_experiment(name)
        if status and status["status"] == "Completed":
            return status
        time.sleep(interval)
        elapsed += interval
    return {"status": "Timeout"}

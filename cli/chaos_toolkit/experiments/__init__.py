"""Experiment base class and template registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Experiment:
    """Represents a chaos experiment configuration."""
    name: str
    kind: str
    target: str
    duration: int = 60
    namespace: str = "default"
    labels: dict[str, str] = field(default_factory=dict)
    params: dict[str, str] = field(default_factory=dict)

    def to_chaos_engine(self) -> dict[str, Any]:
        """Render into a Litmus ChaosEngine CRD manifest."""
        return {
            "apiVersion": "litmuschaos.io/v1alpha1",
            "kind": "ChaosEngine",
            "metadata": {
                "name": self.name,
                "namespace": self.namespace,
                "labels": self.labels,
            },
            "spec": {
                "engineState": "active",
                "chaosServiceAccount": f"{self.name}-sa",
                "experiments": [
                    {
                        "name": self.kind,
                        "spec": {
                            "components": {
                                "env": [
                                    {"name": "TOTAL_CHAOS_DURATION", "value": str(self.duration)},
                                    {"name": "CHAOS_INTERVAL", "value": "10"},
                                    {"name": "TARGET_CONTAINER", "value": self.target},
                                ]
                                + [{"name": k, "value": v} for k, v in self.params.items()]
                            }
                        },
                    }
                ],
            },
        }


TEMPLATES: dict[str, dict[str, Any]] = {
    "pod-delete": {
        "kind": "pod-delete",
        "description": "Randomly deletes a pod to test deployment resilience",
        "default_params": {
            "TOTAL_CHAOS_DURATION": "60",
            "CHAOS_INTERVAL": "10",
            "FORCE": "true",
        },
    },
    "cpu-hog": {
        "kind": "cpu-hog",
        "description": "Consumes CPU resources on a target container",
        "default_params": {
            "TOTAL_CHAOS_DURATION": "60",
            "CPU_CORES": "1",
            "CPU_LOAD": "100",
        },
    },
    "network-latency": {
        "kind": "network-latency",
        "description": "Injects network latency into a target pod",
        "default_params": {
            "TOTAL_CHAOS_DURATION": "60",
            "NETWORK_LATENCY": "2000",
            "JITTER": "500",
        },
    },
    "pod-memory-hog": {
        "kind": "pod-memory-hog",
        "description": "Consumes memory on a target container",
        "default_params": {
            "TOTAL_CHAOS_DURATION": "60",
            "MEMORY_CONSUMPTION": "500",
            "MEMORY_PERCENTAGE": "80",
        },
    },
    "node-drain": {
        "kind": "node-drain",
        "description": "Drains a node to test workload rescheduling",
        "default_params": {
            "TOTAL_CHAOS_DURATION": "120",
            "DRAIN_TIMEOUT": "60",
        },
    },
}

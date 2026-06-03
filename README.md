# Chaos Toolkit

A lightweight chaos engineering platform built on LitmusChaos to inject faults (pod kill, CPU stress, network latency) into Kubernetes environments. Includes a CLI for experiment management and a real-time dashboard.

## Features

- **CLI tool** — trigger, list, and monitor chaos experiments from your terminal
- **Kubernetes-native** — leverages LitmusChaos CRDs (ChaosEngine, ChaosExperiment)
- **Pre-built experiments** — pod-delete, CPU hog, network latency, and more
- **Real-time dashboard** — Vue-based UI to visualize experiment history and cluster health
- **Pluggable** — write custom experiments using the ChaosExperiment CRD

## Quick start

```bash
pip install chaos-toolkit
chaos run k8s/experiments/pod-delete.yaml --namespace default
```

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   CLI       │────▶│  API Server  │────▶│  Dashboard  │
│  (Python)   │     │  (Litmus)    │     │   (Vue.js)  │
└─────────────┘     └──────────────┘     └─────────────┘
                          │
                    ┌─────┴──────┐
                    │  Chaos     │
                    │  Operator  │
                    └─────┬──────┘
                          │
              ┌───────────┴───────────┐
              │   Target Namespace    │
              │   (experiments run)   │
              └───────────────────────┘
```

## Badges

[![CI](https://github.com/AsierCaballero/chaos-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/AsierCaballero/chaos-toolkit/actions/workflows/ci.yml)


## Example usage

```bash
chaos templates
chaos run k8s/experiments/pod-delete.yaml
chaos status pod-delete-sample
```


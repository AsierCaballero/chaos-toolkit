# Architecture

## Overview

Chaos Toolkit is composed of three main components:

```
┌─────────────────────────────────────────────────────┐
│                   CLI (Python)                       │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────┐  │
│  │  Runner   │  │  Reporter  │  │  Experiment DSL  │  │
│  └────┬─────┘  └─────┬─────┘  └────────┬─────────┘  │
│       │              │                  │            │
└───────┼──────────────┼──────────────────┼────────────┘
        │              │                  │
┌───────┼──────────────┼──────────────────┼────────────┐
│       │     Kubernetes API              │            │
│  ┌────┴─────────────────────────────────┴────────┐   │
│  │              LitmusChaos Operator              │   │
│  │  ┌──────────┐  ┌──────────┐  ┌─────────────┐  │   │
│  │  │ ChaosEng │  │ ChaosExp │  │ ChaosResult  │  │   │
│  │  │  ines    │  │ eriments │  │             │  │   │
│  │  └──────────┘  └──────────┘  └─────────────┘  │   │
│  └────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────┐
│              Dashboard (Vue.js)                       │
│  ┌──────────┐  ┌───────────┐  ┌──────────────────┐   │
│  │  Views    │  │  Pinia    │  │  Chart.js        │   │
│  │          │  │  Store    │  │  Visualizations  │   │
│  └──────────┘  └───────────┘  └──────────────────┘   │
└──────────────────────────────────────────────────────┘
```

## Components

### CLI (Python)
- **Runner** — applies ChaosEngine CRDs to the cluster via the Kubernetes API
- **Reporter** — exports experiment results in table, JSON, SARIF, or HTML formats
- **Experiment DSL** — programmatic experiment creation with Python dataclasses

### Chaos Operator (LitmusChaos)
- **ChaosEngine** — CRD that defines which experiment to run and how
- **ChaosExperiment** — CRD containing the actual fault injection logic
- **ChaosResult** — CRD that stores the experiment verdict

### Dashboard (Vue.js)
- Single-page application with real-time experiment monitoring
- Chart.js integration for result visualization
- Pinia store for state management

## Experiment Lifecycle

1. User submits a ChaosEngine manifest (via CLI or kubectl)
2. LitmusChaos Operator detects the new ChaosEngine resource
3. Operator spawns a runner pod that executes the fault
4. Results are recorded in a ChaosResult CRD
5. CLI polls for completion and returns the verdict

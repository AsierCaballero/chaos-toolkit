# Getting Started with Chaos Toolkit

## Prerequisites

- Kubernetes cluster (v1.23+)
- Helm (v3+)
- kubectl configured

## Installation

### 1. Install LitmusChaos

```bash
helm repo add litmus https://litmuschaos.github.io/litmus-helm/
helm install chaos litmus/litmus --namespace litmus --create-namespace
```

Verify the operator is running:

```bash
kubectl get pods -n litmus
```

### 2. Install Chaos Toolkit CLI

```bash
pip install chaos-toolkit
```

Or from source:

```bash
git clone https://github.com/AsierCaballero/chaos-toolkit.git
cd chaos-toolkit
pip install -e cli/
```

### 3. Configure RBAC

```bash
kubectl apply -f k8s/rbac.yaml
```

## Running Your First Experiment

```bash
# List available templates
chaos templates

# Run a pod-delete experiment
chaos run k8s/experiments/pod-delete.yaml -n default

# Check experiment status
chaos status pod-delete-sample
```

## Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

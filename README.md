# Repo Orchestrator

YAML-driven GitHub repository control plane.

This tool manages the lifecycle of a structured set of repositories using:

- Declarative configuration
- Blueprint-based inheritance
- Explicit lifecycle state tracking
- Safe reconciliation logic
- Guardrails for governance and protection

It behaves like a lightweight infrastructure-as-code system for GitHub repositories.

---

# Architecture Overview

This system separates:

| Concern | File |
|----------|------|
| Desired State | `config/repo-groups.yaml` |
| Operational State | `config/repo-state.yaml` |
| Execution Engine | `orchestrator.py` |

Execution model:

```
repo-groups.yaml  → Desired State
repo-state.yaml   → Lifecycle State
orchestrator.py   → Reconciliation Engine
```

Flow:

1. Load desired configuration
2. Validate blueprint references
3. Load lifecycle state
4. Compare desired vs actual (GitHub + filesystem)
5. Determine required actions
6. Apply changes (if instructed)
7. Update lifecycle state

---

# Directory Structure

```
repo-orchestrator/
├── config/
│   ├── repo-groups.yaml
│   └── repo-state.yaml
│
├── orchestrator.py
├── pyproject.toml
├── uv.lock
├── LICENSE
└── README.md
```

Managed repositories live under:

```
/Users/<user>/Desktop/git/managed-repos
```

The orchestrator **will not modify repositories outside this directory.**

---

# Configuration

## repo-groups.yaml (Desired State)

Defines:

- Base path
- Blueprints
- Projects
- Repository definitions

Blueprints define behavior once and are reused per repository.

Example:

```yaml
showcase-protected:
  visibility: public
  license: none
  gitignore: Python
```

Repositories reference a blueprint:

```yaml
- name: ml-usecases-in-healthcare
  blueprint: showcase-protected
  description: "Applied ML experimentation in healthcare."
```

All repositories must reference a valid blueprint.

---

## repo-state.yaml (Operational State)

Tracks runtime metadata:

```yaml
repos:

  ml-usecases-in-healthcare:
    status: CREATED
    locked: false
    last_applied: 2026-02-28
```

Fields:

- `status` → lifecycle state
- `locked` → prevents reconciliation
- `last_applied` → audit timestamp

This file is committed for auditability.

---

# Running the Tool

All commands are executed using `uv`.

## Basic Usage

### Plan

Shows what actions would be taken without modifying anything:

```
uv run python orchestrator.py plan
```

### Apply

Creates missing repositories and clones them locally:

```
uv run python orchestrator.py apply
```

---

## Optional Arguments

### Limit to a Specific Project

```
uv run python orchestrator.py plan --project ml-series
```

```
uv run python orchestrator.py apply --project ml-series
```

This restricts reconciliation to a single project block in `repo-groups.yaml`.

---

# Locked Repositories

If a repository is marked:

```yaml
locked: true
```

The orchestrator will:

- Skip apply operations
- Skip pull operations
- Skip reconciliation
- Still display it during plan

This prevents unnecessary checks and modifications.

Future support may include a `--force` override flag.

---

# Safety Guarantees

- Only operates within configured base path
- Fails if blueprint reference is invalid
- Does not mutate desired configuration
- Lifecycle state tracked explicitly
- Designed to avoid destructive operations
- Clear separation between desired config and runtime state

---

# Blueprint Strategy

Blueprints encode repository intent:

### showcase-protected
- Public visibility
- No license (copyright retained)
- Portfolio exposure
- No reuse rights granted

### open-learning
- Public
- MIT licensed
- Open experimentation

### incubation-private
- Private
- Protected IP
- Monetization incubation

### research-sandbox
- Public research repos
- Academic experimentation

Blueprints allow governance without repetition.

---

# Environment Management

This project uses `uv` for dependency and environment management.

Run:

```
uv run python orchestrator.py plan
```

No manual virtual environment activation required.

Dependencies are defined in:

```
pyproject.toml
```

Locked via:

```
uv.lock
```

---

# Future Enhancements

Planned capabilities:

- Drift detection
- Metadata reconciliation
- Override flags (`--force`)
- Repo archival
- Multi-environment support
- Agent-driven orchestration
- Copilot task automation
- CI integration

---

# Design Goals

This tool is built to:

- Scale a multi-domain ML portfolio
- Protect business-applied implementations
- Separate academic learning from monetizable systems
- Enable structured GitHub governance
- Provide deterministic lifecycle control
- Support automation and AI-driven operations

---

# Author

Richard Urena  
Lead Software Engineer | ML & Analytics Practitioner  
Georgia Tech OMSCS – Machine Learning & Analytics  

---

# License

Copyright (c) 2026 Richard Urena

This repository is licensed under the MIT License.

The license applies only to this orchestration framework.

Managed repositories created by this tool may use different licensing strategies as defined by their respective blueprints.

See LICENSE file for full terms.
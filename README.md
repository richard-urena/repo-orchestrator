# Repo Orchestrator

YAML-driven GitHub repository control plane.

This tool manages the lifecycle of a structured set of repositories using:

- Declarative configuration
- Blueprint-based inheritance
- Explicit lifecycle state tracking
- Safe reconciliation logic
- Guardrails for governance and protection

It is designed to scale domain portfolios (e.g., applied ML business use cases) while preserving architectural boundaries between public showcase, protected implementation, and private incubation.

---

# Core Philosophy

This tool separates **desired state**, **operational state**, and **execution logic**.

| Concern | File |
|----------|------|
| Desired State | `config/repo-groups.yaml` |
| Operational State | `config/repo-state.yaml` |
| Execution Engine | `orchestrator.py` |

It behaves like a lightweight infrastructure-as-code system for GitHub repositories.

The configuration defines what should exist.  
The state file tracks what currently exists.  
The orchestrator reconciles the two.

---

# What This Tool Does

- Creates repositories if they do not exist
- Applies blueprint-based settings (visibility, license, gitignore, etc.)
- Clones repositories into a managed directory
- Tracks lifecycle state (`CREATED`, `READY`, etc.)
- Enforces `locked` repositories
- Prevents touching unmanaged repositories
- Fails fast on invalid blueprint references
- Designed for future automation via Copilot or agent systems

---

# Directory Structure

```
repo-orchestrator/
├── config/
│   ├── repo-groups.yaml   # Desired configuration (manual edits)
│   └── repo-state.yaml    # Lifecycle state (system-managed, committed)
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

Only this directory is touched by the orchestrator.

---

# Configuration Model

## 1. repo-groups.yaml (Declarative Desired State)

Defines:

- Base path
- Blueprints
- Projects
- Repository definitions
- Blueprint references

Blueprints define repository behavior once and are reused per repository.

Example blueprint:

```yaml
showcase-protected:
  visibility: public
  license: none
  gitignore: Python
  has_issues: false
  has_wiki: false
```

Repositories reference them:

```yaml
- name: ml-usecases-in-healthcare
  blueprint: showcase-protected
  description: "Applied ML experimentation in healthcare."
```

This prevents duplication and enforces governance consistency.

---

## 2. repo-state.yaml (Operational State)

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
- `locked` → prevents modification or reconciliation
- `last_applied` → audit timestamp

This file is committed for auditability and traceability.

The orchestrator updates this file intentionally and predictably.

---

# Blueprint Strategy

Blueprints encode repository intent and legal posture.

### showcase-protected
- Public visibility
- No license (copyright retained)
- Portfolio exposure
- No reuse rights granted

### open-learning
- Public
- MIT licensed
- Open experimentation allowed

### incubation-private
- Private
- Protected IP
- Monetization incubation

### research-sandbox
- Public research repositories
- Academic-aligned experiments
- Flexible experimentation

This structure separates:
- Public portfolio work
- Protected business implementations
- Private incubation
- Academic experimentation

---

# Commands

All commands are executed via `uv`.

## Plan

Shows reconciliation actions without applying changes:

```
uv run python orchestrator.py plan
```

## Apply

Creates missing repositories and clones locally:

```
uv run python orchestrator.py apply
```

Respects:

- Locked repositories
- Base path enforcement
- Blueprint validation
- State tracking

---

# Safety Guarantees

- Will not modify repositories outside `managed-repos`
- Fails if blueprint reference is invalid
- Does not mutate desired configuration
- Uses explicit lifecycle tracking
- Designed to avoid destructive operations
- Separation between desired config and runtime state

---

# Architecture Overview

This system follows a simplified reconciliation model:

```
repo-groups.yaml  → Desired State
repo-state.yaml   → Observed / Lifecycle State
orchestrator.py   → Reconciliation Engine
```

Execution flow:

1. Load desired configuration
2. Validate blueprint references
3. Load lifecycle state
4. Compare desired vs actual (GitHub + filesystem)
5. Determine required actions
6. Apply changes (if instructed)
7. Update lifecycle state file

Future architecture extensions may include:

- Drift detection
- Metadata reconciliation
- Selective project execution
- Override flags (`--force`)
- Repo archival
- Automated PR scaffolding
- Agent-driven orchestration
- Copilot task delegation
- Multi-environment support

---

# Design Goals

This tool is built to:

- Scale a multi-domain ML portfolio
- Protect business-applied implementations
- Separate academic learning from monetizable systems
- Enable structured GitHub governance
- Provide deterministic repo lifecycle control
- Serve as foundation for automation and AI-driven orchestration

It is intentionally lightweight, explicit, and extensible.

---

# Author

Richard Urena  
Lead Software Engineer | ML & Analytics Practitioner  
Georgia Tech OMSCS – Machine Learning & Analytics  

---

# License

Copyright (c) 2026 Richard Urena

This repository and its contents are licensed under the MIT License.

The license applies to the orchestration framework and tooling contained in this repository only.

Managed repositories created by this tool may use different licensing strategies as defined by their respective blueprints.

See the LICENSE file for full terms.

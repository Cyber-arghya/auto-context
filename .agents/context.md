# auto-context — Executive Context Hub

> **Last Updated:** 2026-11-03 | **Stack:** Python (CLI Tool)  
> **Directory:** `C:/Users/worka/Desktop/test/auto-context` | **Model:** Hub & Satellite

---

<!-- AUTO-CONTEXT:DISCOVERY:START -->
## 1. Network & Configuration Vault

> 🔒 **Security Boundary:** All private secrets and environment variables belong exclusively in `.env` (protected by `.gitignore`). Never commit live credentials to version control.

| Service / Key | Port / Setting | Source / Mode |
| :--- | :--- | :--- |
| **Network Ports** | `None` | CLI / Library (No local server ports detected) |
| **Runtime Secrets** | `.env` | Protected by .gitignore |

## 2. Satellites & On-Demand Dispatch Directory

* **Primary Stack:** Python 3.12 (Typer, Rich, Hatchling)
* **Satellites Root:** [`.agents/`](file://C:/Users/worka/Desktop/test/auto-context/.agents/)

> 🧭 **Progressive Disclosure Rule:** Do NOT bulk-read satellite files. Inspect the specific satellite file ONLY when your active task matches its trigger condition:

| Domain / Intent | When to Read (Task Triggers) | Target Satellite File |
| :--- | :--- | :--- |
| **Architecture Traps & Invariants** | Before modifying architecture, ports, state, or build pipelines | [`gotchas.md`](file://C:/Users/worka/Desktop/test/auto-context/.agents/context/gotchas.md) |
| **Command Routes & Endpoints** | When modifying, adding, or removing CLI subcommands or routes | [`routes.md`](file://C:/Users/worka/Desktop/test/auto-context/.agents/context/routes.md) |
| **Project Roadmap & ADR** | When aligning features with long-term goals or architectural decisions | [`project-goal.md`](file://C:/Users/worka/Desktop/test/auto-context/.agents/project-goal.md) |

## 3. Operations Runbook

| Action | Command |
| :--- | :--- |
| Run CLI (Local Development) | `uv run init-context` |
| Run Test Suite | `python tests/run_tests.py` |
| Update Global Plugin Assets | `uv run init-context update` |
<!-- AUTO-CONTEXT:DISCOVERY:END -->

---

## 4. Active Invariants & Critical Gotchas

> ⚠️ Consult [`.agents/context/gotchas.md`](file://C:/Users/worka/Desktop/test/auto-context/.agents/context/gotchas.md) before modifying database models, port bindings, or build pipelines.

1. **Precision Targeting:** Do NOT read full component bodies; use Grep / Symbol targeting.
2. **Secret Safety:** Never commit plaintext credentials or private tokens.
3. **Single Source of Truth:** All canonical rules and skills live in `src/auto_context/templates/`.

---

## 5. Skills & Progressive Disclosure Routing

| Skill | Triggers | Location |
| :--- | :--- | :--- |
| **`docker-ops`** | `docker`, `compose` | [SKILL.md](file://C:/Users/worka/Desktop/test/auto-context/src/auto_context/templates/skills/docker-ops/SKILL.md) |
| **`git-workflow`** | `git`, `commit`, `rebase` | [SKILL.md](file://C:/Users/worka/Desktop/test/auto-context/src/auto_context/templates/skills/git-workflow/SKILL.md) |
| **`server-diagnostics`** | `health`, `ram`, `port` | [SKILL.md](file://C:/Users/worka/Desktop/test/auto-context/src/auto_context/templates/skills/server-diagnostics/SKILL.md) |
| **`feature-verification`** | `test`, `verify`, `check` | [SKILL.md](file://C:/Users/worka/Desktop/test/auto-context/src/auto_context/templates/skills/feature-verification/SKILL.md) |

# {{PROJECT_NAME}} — Executive Context Hub

> **Last Updated:** {{DATE_NOW}} | **Stack:** {{STACK}} ({{FRAMEWORK}})  
> **Directory:** `{{PROJECT_DIR}}` | **Model:** Hub & Satellite

---

<!-- AUTO-CONTEXT:DISCOVERY:START -->
## 1. Network & Configuration Vault

> 🔒 **Security Boundary:** All private secrets and environment variables belong exclusively in `.env` (protected by `.gitignore`). Never commit live credentials to version control.

| Service / Key | Port / Setting | Source / Mode |
| :--- | :--- | :--- |
| **Network Ports** | `None detected` | Runtime / Discovered |
| **Runtime Secrets** | `.env` | Protected by .gitignore |

## 2. Stack & Adaptive Satellites

* **Primary Stack:** {{STACK}} ({{FRAMEWORK}})
* **Project Goals & ADR:** [`.agents/project-goal.md`](file://{{PROJECT_DIR}}/.agents/project-goal.md) — North Star, roadmap & architecture decisions
* **Satellites Directory:** [`.agents/context/`](file://{{PROJECT_DIR}}/.agents/context/)
  - **Critical Gotchas:** [`gotchas.md`](file://{{PROJECT_DIR}}/.agents/context/gotchas.md) — Architecture invariants & traps
  - **Adaptive Satellites:** Maintained on-demand as project scales (`routes.md` for APIs/pages, `schema.md` for database models)

## 3. Operations Runbook

| Action | Command |
| :--- | :--- |
<!-- AUTO-CONTEXT:DISCOVERY:END -->

---

## 4. Active Invariants & Critical Gotchas

> ⚠️ Consult [`.agents/context/gotchas.md`](file://{{PROJECT_DIR}}/.agents/context/gotchas.md) before modifying database models, port bindings, or build pipelines.

1. **Precision Targeting:** Do NOT read full component bodies; use Grep / Symbol targeting.
2. **Secret Safety:** Never commit plaintext credentials or private tokens.

---

## 5. Skills & Progressive Disclosure Routing

| Skill | Triggers | Location |
| :--- | :--- | :--- |
| **`docker-ops`** | `docker`, `compose` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/docker-ops/SKILL.md) |
| **`git-workflow`** | `git`, `commit`, `rebase` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/git-workflow/SKILL.md) |
| **`server-diagnostics`** | `health`, `ram`, `port` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/server-diagnostics/SKILL.md) |
| **`feature-verification`** | `test`, `verify`, `check` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/feature-verification/SKILL.md) |

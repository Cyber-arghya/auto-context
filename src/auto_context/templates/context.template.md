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

## 2. Operations Runbook

| Action | Command |
| :--- | :--- |
<!-- AUTO-CONTEXT:DISCOVERY:END -->

---

## 3. Active Architecture Invariants

> ⚡ **System Constraints:** Non-obvious rules, traps, and invariants specific to this codebase that cannot be inferred from code alone.

1. **Precision Targeting:** Do NOT bulk-read entire files; use targeted Grep / Symbol navigation.
2. **Secret Safety:** Never commit plaintext credentials or private tokens.
3. **Verified Executable Runbooks:** Only record 100% executable commands parsed from manifests or verified tools.

---

## 4. Stack-Adaptive Satellites & Domain Maps (On-Demand)

> 🧭 Satellites reside in [`.agents/context/`](file://{{PROJECT_DIR}}/.agents/context/) and are created/inspected **only when the corresponding domain exists** (Zero Ghost Files):

| Domain | Satellite File | Condition / When Needed |
| :--- | :--- | :--- |
| **Project North Star & ADR** | [`project-goal.md`](file://{{PROJECT_DIR}}/.agents/project-goal.md) | Scope verification, milestone alignment, or architectural decisions |
| **API Endpoints & UI Views** | `routes.md` | Web/API projects only (when creating or modifying endpoints/pages) |
| **Database Schemas & Models** | `schema.md` | Database/ORM projects only (when altering tables or migrations) |

---

## 5. Skills & Progressive Disclosure Routing

| Skill | Triggers | Location |
| :--- | :--- | :--- |
| **`docker-ops`** | `docker`, `compose` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/docker-ops/SKILL.md) |
| **`git-workflow`** | `git`, `commit`, `rebase` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/git-workflow/SKILL.md) |
| **`server-diagnostics`** | `health`, `ram`, `port` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/server-diagnostics/SKILL.md) |
| **`feature-verification`** | `test`, `verify`, `check` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/feature-verification/SKILL.md) |

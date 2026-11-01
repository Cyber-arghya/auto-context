# {{PROJECT_NAME}} — Executive Context Hub

> **Last Updated:** {{DATE_NOW}} | **Stack:** {{STACK}} ({{FRAMEWORK}})  
> **Directory:** `{{PROJECT_DIR}}` | **Model:** Hub & Satellite (< 400 Tokens)

---

<!-- AUTO-CONTEXT:DISCOVERY:START -->
## 1. Network & Configuration Vault

> 🔒 **Sandbox Isolation:** Mock dev accounts and local ports live in [`context.local.md`](file://{{PROJECT_DIR}}/context.local.md). Production secrets belong exclusively in `.env`.

| Service / Key | Port / Setting | Source / Mode |
| :--- | :--- | :--- |
| **App Server** | `3000` (Default) | Development |
| **Test Fixtures** | `context.local.md` | Mock accounts (chmod 600) |
| **Runtime Secrets** | `.env` | Protected by .gitignore |

## 2. Stack & Adaptive Satellites

* **Primary Stack:** {{STACK}} ({{FRAMEWORK}})
* **Satellites Directory:** [`.agents/context/`](file://{{PROJECT_DIR}}/.agents/context/)
  - **Critical Gotchas:** [`gotchas.md`](file://{{PROJECT_DIR}}/.agents/context/gotchas.md) — Architecture invariants & traps
  - **Routes & Endpoints:** [`routes.md`](file://{{PROJECT_DIR}}/.agents/context/routes.md) — Discovered API & page map
  - **Database Schemas:** [`schema.md`](file://{{PROJECT_DIR}}/.agents/context/schema.md) — Discovered models & ORM entities

## 3. Operations Runbook

| Action | Command |
| :--- | :--- |
| **Rescan & Sync Runbook** | `init-context scan` |
<!-- AUTO-CONTEXT:DISCOVERY:END -->

---

## 4. Active Invariants & Critical Gotchas

> ⚠️ Consult [`.agents/context/gotchas.md`](file://{{PROJECT_DIR}}/.agents/context/gotchas.md) before modifying database models, port bindings, or build pipelines.

1. **Token Conservation:** Do NOT read full component bodies; use Grep / Symbol targeting.
2. **Secret Safety:** Never commit plaintext credentials or test keys.

---

## 5. Skills & Progressive Disclosure Routing

| Skill | Triggers | Location |
| :--- | :--- | :--- |
| **`docker-ops`** | `docker`, `compose` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/docker-ops/SKILL.md) |
| **`git-workflow`** | `git`, `commit`, `rebase` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/git-workflow/SKILL.md) |
| **`server-diagnostics`** | `health`, `ram`, `port` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/server-diagnostics/SKILL.md) |
| **`browser-testing`** | `browser`, `playwright` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/browser-testing/SKILL.md) |

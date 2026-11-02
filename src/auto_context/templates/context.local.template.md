# ⚠️ LOCAL SANDBOX & DUMMY TEST FIXTURES ONLY
# ==============================================================================
# SECURITY GUARDRAIL:
# DO NOT STORE REAL PRODUCTION SECRETS, PAYMENT KEYS, OR LIVE PASSWORDS HERE.
# This file is strictly for mock logins, seed users, localhost ports, and dev test data.
# Real secrets MUST stay in .env (protected by system environment variables).
#
# GIT STATUS: STRICTLY GIT-IGNORED (*.local.md, context.local.md)
# FILE PERMISSIONS: chmod 600
# ==============================================================================

> **Project:** `{{PROJECT_NAME}}`  
> **Purpose:** Local mock credentials & test logins for AI browser testing and dev automation.  
> **Notice to AI Assistant:** Check this file before asking user for test login credentials. Never commit this file to Git.

---

## 1. Project Directory & Environment Paths

| Environment | Absolute Filesystem Directory | Host / Container Context |
| :--- | :--- | :--- |
| **Local Workspace** | `{{PROJECT_DIR}}` | Local Host OS Working Directory |
| **Remote Server Root** | `/var/www/{{PROJECT_NAME}}` | Production / Staging Server Directory |
| **Container Workdir** | `/app` | Docker / Containerized Workload |

---

## 2. Local Dev Endpoints & Test Ports

| Service | Local URL / Port | Status / Description |
| :--- | :--- | :--- |
| **Frontend Web** | `http://localhost:3000` | Dev server |
| **Backend API** | `http://localhost:8000` | Local API endpoint |
| **Local Mock DB** | `localhost:5432` / `database.db` | Non-production dev database |

---

## 3. Seed Accounts & Dummy Test Logins (Browser Automation)

Use these mock accounts when performing automated UI testing, Playwright / Puppeteer workflows, or manual verification.

| Role | Username / Email | Mock Password | Notes / Permissions |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin@test.local` | `adminpass123` | Full admin privileges |
| **Standard User** | `user@test.local` | `userpass123` | Default user permissions |
| **Guest / Demo** | `guest@test.local` | `guestpass123` | Read-only access |

---

## 4. Local Mock Tokens & Test Headers

```http
Authorization: Bearer dev-mock-token-12345
X-Test-Bypass: true
```

---

## 5. Local Test Notes & Scratch Data
<!-- AI and developer can jot temporary test notes, cookie values, or scratch session tokens here -->
- Test session initialized: {{DATE_NOW}}


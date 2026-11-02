---
name: security-boundaries
description: Enforces zero plaintext secrets in Git, strict .env protection, and isolated mock data in context.local.md.
trigger: always_on
---

# Rule: Security Boundaries & Secret Safety

## Objective
Prevent credential leakage, indirect prompt injection, and unauthorized network exposure across all code, configuration files, and git commits.

## Guidelines & Constraints
1. **Zero Hardcoded Secrets:**
   - API keys, tokens, database passwords, and private keys must NEVER be hardcoded into source code, committed configs, or git history.
   - All runtime secrets must be loaded via `.env` or system environment variables.
2. **Local Sandbox Test Data Isolation (`context.local.md`):**
   - Only dummy/mock credentials (e.g. `admin@test.local`) belong in `context.local.md`.
   - Real production credentials or live payment keys are strictly prohibited in markdown files.
   - `context.local.md` must remain strictly git-ignored (`chmod 600`).
3. **Public Exposure Boundaries:**
   - Raw database and internal service ports must bind to `127.0.0.1` unless encapsulated by secure tunneling.
4. **Local & Server Directory Path Isolation (`context.local.md`):**
   - Every project's absolute local workspace directory (e.g. `C:\Users\...` or `/home/...`) and target remote server/container deployment path (e.g. `/var/www/...` or `/app`) MUST be documented inside `context.local.md`.
   - Never commit machine-specific local filesystem paths into public git repositories or public documentation.
   - The AI assistant must always inspect `context.local.md` (Section 1) to resolve working directories, server paths, and remote deployment targets before executing operations.

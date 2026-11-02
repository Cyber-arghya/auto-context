---
name: security-boundaries
description: Enforces zero plaintext secrets in Git, strict .env protection, and secure network isolation.
trigger: always_on
---

# Rule: Security Boundaries & Secret Safety

## Objective
Prevent credential leakage, indirect prompt injection, and unauthorized network exposure across all code, configuration files, and git commits.

## Guidelines & Constraints
1. **Zero Hardcoded Secrets:**
   - API keys, tokens, database passwords, and private keys must NEVER be hardcoded into source code, committed configs, or git history.
   - All runtime secrets must be loaded via `.env` or system environment variables.
2. **Environment & Test Isolation:**
   - Dedicated test credentials and mock tokens must be loaded via `.env.test` or environment test fixtures.
   - Real production credentials or live payment keys are strictly prohibited in test fixtures and markdown documentation.
3. **Public Exposure Boundaries:**
   - Raw database and internal service ports must bind to `127.0.0.1` (localhost) unless encapsulated by secure tunneling.
4. **Machine Path & Sensitive Data Privacy:**
   - Never commit machine-specific absolute filesystem paths or private network hostnames into public git repositories or public documentation.

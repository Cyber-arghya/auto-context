---
name: readme-docs-sync
description: Mandates immediate documentation synchronization in README.md whenever features, commands, or workflows are added or updated in auto-context or any Git repository.
trigger: always_on
---

# Rule: Mandatory README & Documentation Synchronization

## Objective
Ensure that all features, subcommands, options, and architectural workflows in `auto-context` or any active Git repository are comprehensively, accurately, and immediately documented in `README.md` with proper executable commands and instructions.

## Guidelines & Constraints
1. **Zero Undocumented Features:**
   - Whenever a new feature, CLI command, option, flag, or architectural capability is added or modified, `README.md` MUST be updated before committing or releasing.
   - Both the English reference documentation and the Bengali guide (বাংলা নির্দেশিকা) must be updated.
2. **Clear & Executable Instructions:**
   - Every command documented must be 100% executable and tested.
   - Include clear syntax examples (`init-context update`, `init-context promote`, `init-context memory`, etc.), options tables, and expected output.
3. **Safety & Non-Breaking Boundaries:**
   - Explicitly document data protection guarantees (e.g. `context.md`, `.env`, and user custom rules are never overwritten or broken).
4. **Release Version Alignment:**
   - When bumping package versions (`pyproject.toml`, tags), update release badges and installation commands in `README.md`.

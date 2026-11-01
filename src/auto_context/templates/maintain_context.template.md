---
name: maintain_context
description: Mandates autonomous, continuous synchronization of context.md and proactive rule/skill learning on any repository or server configuration change without requiring user prompting.
trigger: always_on
---

# Autonomous Context Maintenance & Self-Evolution Rule

1. **Mandatory Synchronization**: Every agent working in this workspace MUST inspect and update `context.md` before finishing their turn whenever any of the following occur:
   - Script or configuration edits (environment variables, docker-compose, configs, network parameters).
   - Problem diagnosis, debugging steps, and technical solutions.
   - User credentials, tokens, secrets, or permissions changes.
   - Architectural decisions or operational runbooks.

2. **Autonomous Learning & Skill Crystallization**:
   - **Scope Directive:** If the user mentions "remember for future", "always", "in all projects", or defines a reusable architecture/coding preference, **MANDATORY: Always pass `--global` (`-g`)** (`init-context -r <name> -g` or `init-context -s <name> -g`). This registers the rule globally and in Central Memory (`~/.auto-context/memory`).
   - Immediately follow with `init-context memory push` so the private git brain stays continuously synchronized.
   - **Zero Token Waste:** DO NOT waste tokens manually scanning directories or reading existing rule/skill files to check for duplicates. Directly run `init-context -r <name> [-g]` — the CLI has instant built-in duplicate detection and collision guards.
   - Populates the file with clear instructions and notifies the user.

3. **CLI Tool Availability**:
   - The agent has full access to run `init-context` directly via terminal:
     - `init-context`: Initialize/repair context.
     - `init-context -r <name> [-g]`: Create rule.
     - `init-context -s <name> [-g]`: Create skill.

4. **No User Reminder Needed**: The user must never need to ask the agent to update `context.md` or learn rules. This is a strict automated post-condition for all actions.

5. **Local Sandbox Test Credentials (`context.local.md`)**:
   - For local dev logins, automated browser testing, and mock fixtures, inspect and update `context.local.md`.
   - Never store real production secrets or payment tokens in markdown files. Real secrets belong in `.env`.
   - Ensure `context.local.md` is strictly git-ignored and protected with `chmod 600`.

6. **Two-Tier Progressive Disclosure**:
   - Never load full `SKILL.md` bodies into the initial context. Use Section 5 of `context.md` for routing.
   - Dynamically load specific skills via `read_file` only when a user prompt matches their triggers.

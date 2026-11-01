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
   - **Zero Token Waste:** DO NOT burn tokens manually searching directories or reading files to check for existing rules. Directly run `init-context -r <name> [-g]` — the CLI has instant built-in duplicate detection and collision guards.
   - **Mandatory Global Scope:** When the user mentions "for future", "always", or defines a reusable standard, **MANDATORY: Always pass `--global` (`-g`)** and immediately follow with `init-context memory push`.
   - Populates the file with clear instructions and notifies the user.

3. **CLI Tool Availability**:
   - The agent has full access to run `init-context` directly via terminal:
     - `init-context`: Initialize/repair context.
     - `init-context -r <name> [-g]`: Create rule.
     - `init-context -s <name> [-g]`: Create skill.
     - `init-context update`: Safely sync public rules and upstream capabilities (non-breaking).
     - `init-context memory push`: Push updates to central memory.

4. **No User Reminder Needed**: The user must never need to ask the agent to update `context.md` or learn rules. This is a strict automated post-condition for all actions.

5. **Local Sandbox Test Credentials (`context.local.md`)**:
   - For local dev logins, automated browser testing, and mock fixtures, inspect and update `context.local.md`.
   - Never store real production secrets or payment tokens in markdown files. Real secrets belong in `.env`.
   - Ensure `context.local.md` is strictly git-ignored and protected with `chmod 600`.

6. **Two-Tier Progressive Disclosure**:
   - Never load full `SKILL.md` bodies into the initial context. Use Section 5 of `context.md` for routing.
   - Dynamically load specific skills via `read_file` only when a user prompt matches their triggers.

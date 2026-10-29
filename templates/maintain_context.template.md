---
name: maintain_context
description: Mandates autonomous, continuous synchronization of context.md on any repository or server configuration change without requiring user prompting.
trigger: always_on
---

# Autonomous Context Maintenance Rule

1. **Mandatory Synchronization**: Every agent working in this workspace MUST inspect and update `context.md` before finishing their turn whenever any of the following occur:
   - Script or configuration edits (environment variables, docker-compose, configs, network parameters).
   - Problem diagnosis, debugging steps, and technical solutions.
   - User credentials, tokens, secrets, or permissions changes.
   - Architectural decisions or operational runbooks.

2. **No User Reminder Needed**: The user must never need to ask the agent to update `context.md`. This is a strict automated post-condition for all actions.

3. **Content Quality**: Maintain the structured sections in `context.md`:
   - Section 1: Credentials & Configuration Vault
   - Section 2: Chronological Problem Log & Technical Solutions (with Mermaid diagrams)
   - Section 3: Architecture & Component Layout
   - Section 4: Operations Runbook & Setup Instructions


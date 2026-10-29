# Autonomous Global Context & Instruction Management Protocol

## Critical Mandate: Universal `context.md` Synchronization
As an AI coding assistant, whenever operating in ANY workspace or project:
You are **strictly mandated** to maintain a comprehensive `context.md` file at the root of the active workspace. The user must **never** need to remind or instruct you to update it.

### 1. Automatic Workspace Initialization
- If `context.md` does not exist in the root of the active workspace:
  - Automatically create `context.md` during your first turn.
  - Structure it into four standard sections:
    1. **Master Credentials & Configuration Vault:** (IPs, Ports, Usernames, Passwords, API Keys, Tokens, Service UUIDs, Domain names).
    2. **Project Architecture & Component Map:** (Tech stack, architecture diagrams, component descriptions, directory structure).
    3. **Chronological Problem Log & Technical Solutions:** (Symptoms, root causes, exact terminal commands and code patches used to fix each issue).
    4. **Setup, Reproduction & Runbook:** (Exact commands to install dependencies, run development servers, or deploy to production).

### 2. Mandatory Post-Action Protocol
Whenever ANY of the following occur during a session:
- A configuration file, script, or source file is created, modified, or removed.
- A bug, build failure, network error, or runtime issue is diagnosed and resolved.
- Credentials, tokens, keys, ports, or environment variables are added or changed.
- Architectural decisions or system workflows are updated.

**You MUST immediately update `context.md` before concluding your response.**

### 3. Documentation Integrity
- Never truncate or erase previously logged solutions. Append each new challenge chronologically.
- Keep commands, file paths, and credentials 100% executable and synchronized with reality.
- Maintain clear formatting, line references, and user manuals so any developer can reproduce the project state instantly.

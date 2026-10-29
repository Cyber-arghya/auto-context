---
name: auto-context
description: Scaffolds or updates a comprehensive context.md file and project agent rules (GEMINI.md, AGENTS.md, .agents/rules/) in the active workspace.
---

# Auto Context Scaffolding Skill

When invoked, this skill automatically sets up or audits the context tracking infrastructure of any project.

## Workflow

1. **Workspace Inspection:**
   - Detect project root and primary language/framework (Node.js, Python, Go, Rust, Java, Bash, Docker, etc.).
   - Scan for existing configuration files (`.env.example`, `config.*`, `docker-compose.yml`, `package.json`, etc.).

2. **Scaffold `context.md`:**
   - If `context.md` does not exist, create it with standard template sections:
     - Section 1: Master Credentials & Configuration Vault
     - Section 2: Chronological Problem Log & Technical Solutions (with Mermaid diagrams)
     - Section 3: Architecture & Tech Stack Map
     - Section 4: Operational Setup & Runbook
   - If `context.md` exists, review it and synchronize any missing items.

3. **Scaffold Rules (`GEMINI.md`, `AGENTS.md`, `.agents/rules/`):**
   - Ensure local rule files exist so all subagents and IDE sessions unconditionally enforce real-time `context.md` maintenance.

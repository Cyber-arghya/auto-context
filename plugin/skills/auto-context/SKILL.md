---
name: auto-context
description: Scaffolds or updates a comprehensive context.md file, manages project agent rules, and provides tools for learning and codifying new skills and rules with init-context.
---

# Auto Context Skill

Use this skill when initializing context for a project, scaffolding new agent rules, or learning and crystallizing custom skills.

## Critical Agent Mandates

- **Zero Token Waste:** DO NOT burn tokens manually searching directories or reading files to check for existing rules. Directly run `init-context -r <name> [-g]` — the CLI has instant built-in duplicate detection and collision guards.
- **Mandatory Global Scope:** When the user mentions "for future", "always", or defines a reusable standard, MANDATORY: Always pass `--global` (`-g`) and immediately follow with `init-context memory push`.

## Capabilities & Workflows

1. **Scaffold or Repair Project Context:**
   Run `init-context` in any workspace directory to generate:
   - `context.md` (5-tier single source of truth)
   - `GEMINI.md` and `AGENTS.md` (Standing rules)
   - `.agents/rules/maintain_context.md` (Always-on rule)

2. **Codify a New Rule (Constraints, Styles, Security):**
   ```bash
   init-context -r <rule-name> [--global]
   ```
   * Creates `.agents/rules/<rule-name>.md` (or globally in plugin and Central Memory with `-g`).
   * Built-in collision guard prevents overwrites automatically.
   * Populate with guidelines, constraints, and prohibited patterns.

3. **Codify a New Skill (Workflows, Runbooks, Multi-Step Tasks):**
   ```bash
   init-context -s <skill-name> [--global]
   ```
   * Creates `.agents/skills/<skill-name>/SKILL.md` (or globally with `-g`).
   * Populate with when-to-activate triggers, step-by-step procedure, and verification steps.

4. **Manage MCP Tooling & Runtimes (uvx / npx):**
   ```bash
   init-context mcp add <name> [--runtime uvx|npx] [--args <args>]
   init-context mcp list
   init-context mcp remove <name>
   ```
   * Automatically aligns stdio tools to `uvx` (Python) or `npx` (Node) based on project markers.
   * Tokens and secrets reference `${VAR_NAME}` from `.env` and are protected from Git.

5. **Local Sandbox Test Fixtures (`context.local.md`):**
   * Automatically generated with `chmod 600` and protected by `.gitignore`.
   * Holds mock logins, seed users (`admin@test.local`), and local dev ports for browser testing.
   * Real production secrets are strictly prohibited (they reside in `.env`).

6. **Central Memory Brain & Disaster Recovery:**
   ```bash
   init-context memory init [repo-name]   # Creates strictly private GitHub brain
   init-context memory push               # Zero-bypass secret audit & push to GitHub
   init-context memory pull [repo-url]    # Pull and synchronize brain to new machine
   init-context memory status             # Inspect central brain status
   ```
   * Enforces `--private` flag during remote creation.
   * Scans every file for tokens, keys, and `.env` before pushing (hard-blocks with Exit 1 on secret detection).

7. **Granular Skill Sharing & Safe Import:**
   ```bash
   init-context share <name>              # Share skill or rule via GitHub Gist
   init-context import <url> [--as <name>] # Import external skill with Collision Guard
   ```
   * Collision Guard protects against accidental overwrites with `[O]verwrite / [R]ename / [C]ancel`.

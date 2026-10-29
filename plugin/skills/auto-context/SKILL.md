---
name: auto-context
description: Scaffolds or updates a comprehensive context.md file, manages project agent rules, and provides tools for learning and codifying new skills and rules with init-context.
---

# Auto Context Skill

Use this skill when initializing context for a project, scaffolding new agent rules, or learning and crystallizing custom skills.

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
   * Creates `.agents/rules/<rule-name>.md` with YAML frontmatter.
   * Populate with guidelines, constraints, and prohibited patterns.

3. **Codify a New Skill (Workflows, Runbooks, Multi-Step Tasks):**
   ```bash
   init-context -s <skill-name> [--global]
   ```
   * Creates `.agents/skills/<skill-name>/SKILL.md` with YAML frontmatter.
   * Populate with when-to-activate triggers, step-by-step procedure, and verification steps.

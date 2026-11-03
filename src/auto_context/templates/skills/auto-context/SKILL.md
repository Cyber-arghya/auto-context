---
name: auto-context
description: Scaffolds or updates a comprehensive context.md file, manages project agent rules, promotes rules/skills, and manages Central Memory and MCP servers with init-context.
---

# Auto Context Skill

Use this skill when initializing project context, creating or appending rules and skills, managing MCP tools, promoting local conventions to global scope, or synchronizing with Central Memory.

## Critical Agent Mandates

- **Zero Token Waste:** DO NOT burn tokens manually searching directories or reading files to check for existing rules. Directly run `init-context -r <name> [-g]` — the CLI has instant built-in duplicate detection and collision guards via `registry.json`.
- **Mandatory Global Scope:** When the user mentions "for future", "always", or defines a reusable standard across projects, **MANDATORY: Always pass `--global` (`-g`)** and immediately follow with `init-context memory push`.
- **Zero-Bypass Secret Audit:** Never attempt to bypass secret scanning or force-push uncommitted credentials to Central Memory.

---

## Capabilities & Workflows

### 1. Scaffold or Repair Project Context
Scaffolds the complete `.agents/` context hub, standing rules, starter domain rules, and built-in skills.
```bash
# Initialize active workspace
init-context

# Initialize a specific target directory
init-context /path/to/project

# Explicit subcommand syntax
init-context init [DIR] [--force]
```
* Generates: `.agents/context.md`, `.agents/project-goal.md`, `AGENTS.md`, `GEMINI.md`, `.agents/rules/`, and `.agents/skills/`.
* Automatically registers Zero-Footprint patterns in `.gitignore` and global excludes.

---

### 2. Rule Management (`rule`)
Scaffolds a new domain rule or appends guidelines to an existing domain with built-in duplicate detection.
```bash
# Create local project rule (.agents/rules/api-standards.md)
init-context rule api-standards
init-context -r api-standards

# Append guideline to an existing rule without manual editing
init-context rule code-standards --append --guideline "Always use early returns"
init-context -r code-standards -a --guideline "Enforce static typing"

# Create global rule across all projects (~/.gemini/config/plugins/auto-context/rules/)
init-context rule security-policies --global
init-context -r security-policies -g

# Overwrite existing rule
init-context rule api-standards --force
```

---

### 3. Skill Management (`skill`)
Scaffolds a new operational skill directory with frontmatter triggers, description, and procedure runbook.
```bash
# Create local project skill (.agents/skills/deploy-k8s/SKILL.md)
init-context skill deploy-k8s
init-context -s deploy-k8s

# Create global skill across all projects
init-context skill cloudflare-worker --global
init-context -s cloudflare-worker -g

# Overwrite existing skill
init-context skill deploy-k8s --force
```

---

### 4. Rule & Skill Promotion (`promote`)
Promotes a local workspace rule or skill to machine-wide Global Plugin scope and pushes it to Central Memory in one automated step.
```bash
# Promote local rule to global scope
init-context promote api-standards

# Promote local skill to global scope
init-context promote deploy-k8s
```

---

### 5. Central Memory Brain (`memory`)
Manage private central memory repository (dotfiles for AI agents) across multiple machines with automated secret audits.
```bash
# 1. Initialize private GitHub memory repository
init-context memory init
init-context memory init --repo-name my-agent-brain --private

# 2. Push workspace rules & skills (runs automated Zero-Bypass secret audit before push)
init-context memory push
init-context memory push --message "feat: add payment gateway rules"

# 3. Pull central brain on a new machine
init-context memory pull
init-context memory pull --url git@github.com:username/my-agent-brain.git

# 4. Inspect memory status & sync health
init-context memory status

# 5. Switch or configure remote repository
init-context memory remote
init-context memory remote git@github.com:username/new-memory-brain.git

# 6. Reset local memory cache (safely preserving remote URL)
init-context memory reset
init-context memory reset --force
```

---

### 6. MCP (Model Context Protocol) Registry (`mcp`)
Manage native MCP server configurations for Antigravity and Gemini CLI without committing plaintext secrets.
```bash
# 1. Add pre-configured presets (references ${ENV_VARS} safely)
init-context mcp add sqlite --args "data.db"
init-context mcp add postgres
init-context mcp add github
init-context mcp add brave
init-context mcp add duckdb
init-context mcp add time
init-context mcp add git

# Customize secret environment variable name
init-context mcp add github --env-var MY_GITHUB_PAT

# 2. Add custom command or remote HTTP MCP tool
init-context mcp add my-tool --command "python" --args "server.py"
init-context mcp add remote-tool --url "https://mcp.example.com/sse"

# 3. Choose runner explicitly (uvx vs npx)
init-context mcp add fetch --runtime uvx
init-context mcp add puppeteer --runtime npx

# 4. List registered MCP servers
init-context mcp list
init-context mcp list --global

# 5. Remove an MCP tool
init-context mcp remove sqlite
init-context mcp remove github --global
```

---

### 7. Granular Sharing & Import (`share` / `import`)
Share isolated rules or skills with teammates via GitHub Gist and import them safely with Collision Guard.
```bash
# 1. Share a rule or skill as a private GitHub Gist
init-context share docker-ops
init-context share code-standards

# Share as public Gist
init-context share docker-ops --public

# 2. Import rule or skill from Gist / URL
init-context import https://gist.github.com/user/gist_id

# Import into machine-wide global plugin scope
init-context import <gist-url> --global

# Import with a custom local name
init-context import <gist-url> --as custom-docker-skill
```

---

### 8. Upstream Rule & Capability Updates (`update`)
Safely sync public rules and upstream capabilities without overwriting your custom rules.
```bash
init-context update
```

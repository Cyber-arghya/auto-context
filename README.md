<div align="center">

# 🧠 Auto-Context

**Autonomous Context & Instruction Management Protocol for AI Coding Assistants**

[![PyPI - Version](https://img.shields.io/pypi/v/auto-context-cli.svg?color=blue)](https://pypi.org/project/auto-context-cli/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/auto-context-cli.svg)](https://pypi.org/project/auto-context-cli/)
[![GitHub Release](https://img.shields.io/github/v/release/Cyber-arghya/auto-context?color=green)](https://github.com/Cyber-arghya/auto-context/releases/tag/v1.5.0)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux%20WSL2-success.svg)](#-quick-install)
[![AI Supported](https://img.shields.io/badge/AI%20Supported-Antigravity%20%7C%20Cursor%20%7C%20Claude%20Code%20%7C%20Copilot%20%7C%20Windsurf-orange.svg)](#-supported-ai-assistants)

*Never lose context, forgotten architecture decisions, or unlogged invariants again.*

[What It Does](#-what-is-auto-context) • [How It Works](#️-how-auto-context-works) • [Quick Install](#-quick-install) • [Core Philosophy](#-core-philosophy) • [Command Runbook](#-complete-cli-command-runbook) • [Project Layout](#-generated-project-layout) • [Architecture](#-repository-architecture)

</div>

---

## 📖 What is Auto-Context?

**Auto-Context** is an autonomous context orchestration, instruction management, and persistent memory protocol designed for modern AI coding assistants (Antigravity, Cursor, Claude Code, Copilot, Windsurf).

It transforms how AI agents interact with your codebase by replacing raw, token-burning context dumps with an intelligent, self-guiding **360° End-to-End Execution Pipeline**.

### 🛑 The Problems It Solves:

* **Context Window Pollution & Token Burn:** Dumping entire directories, database schemas, and 500 lines of error logs into monolithic context files burns 10,000+ tokens on *every single prompt*, degrading AI reasoning and triggering premature context compaction.
* **Context Drift & AI Amnesia:** When opening a new chat session or switching agents, the AI forgets architectural invariants, local port bindings, and coding conventions unless repeatedly reminded.
* **Lack of Execution Discipline:** Unassisted AI assistants frequently jump straight into writing code without verifying project scope, hallucinate completion without running automated tests, or repeat previously resolved bugs.

---

## ⚙️ How Auto-Context Works

Auto-Context establishes a deterministic, multi-phase execution loop that every AI assistant executes automatically from the very first turn:

```text
┌────────────────────────────────────────────────────────┐
│ Phase 0: Scope & Gatekeeper (.agents/project-goal.md)   │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ Phase 1: Constitutional Guardrails (.agents/rules/)    │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ Phase 2: Macro Context (.agents/context.md)            │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ Phase 3: Targeted Discovery (.agents/context/*.md)     │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ Phase 4: Implementation (.agents/skills/)              │◄──────┐
└──────────────────────────┬─────────────────────────────┘       │
                           ▼                                     │ (Test Failed:
┌────────────────────────────────────────────────────────┐       │  Self-Correct)
│ Phase 5: Verification & Sync Gate                      │       │
│          • Automated Tests (Exit Code 0)               ├───────┘
│          • Sync Invariants & README (Pass)             │
└────────────────────────────────────────────────────────┘
```

### The 6-Phase Autonomous Execution Pipeline

1. **Phase 0: Scope & Gatekeeper (`.agents/project-goal.md`)**
   - **Autonomous Synthesis:** On first run, the AI automatically inspects your repository and populates the project goal, core purpose, active milestones, and anti-goals (what *not* to build).
   - **Context Pruning:** If the project is a CLI, library, or script, it automatically prunes non-existent network ports and DB tables from `context.md`.
   - **The Brutal Truth Filter:** The AI actively challenges inefficient, over-complicated, or out-of-scope requests before writing code.

2. **Phase 1: Constitutional Guardrails (`.agents/rules/*.md`)**
   - **Continuous Compliance:** Standing, non-negotiable boundaries enforced on every turn (zero hardcoded secrets, early returns, clean git commits, documentation parity).
   - **Dynamic Discovery:** Any rule created via `init-context rule` or synced from Central Memory is instantly recognized and enforced without manual config.

3. **Phase 2: Macro Context Hub (`.agents/context.md`)**
   - **Strict Token Budget (< 80 lines / ~400 tokens):** Serves as an executive routing index containing the project archetype, active runtime toolchain, verified runbook commands (build, lint, test), and failure invariants.

4. **Phase 3: Targeted Discovery & Precision Reads**
   - **Zero Bulk Reading:** Prohibits dumping 50+ files into context. Follows the precision formula:
     $$\text{Precision Context} = \text{Macro Route Map} + \text{Grep / Symbol Search} + \text{Targeted Range Read (\#L30-L70)}$$
   - Specialised satellites (`routes.md`, `schema.md`) are loaded strictly on-demand when relevant.

5. **Phase 4: Dynamic Skills Execution (`.agents/skills/*/SKILL.md`)**
   - **On-Demand Procedural Runbooks:** Reusable operational workflows (Docker ops, Git releases, Browser automation, Server diagnostics) that activate only when their declared triggers match the task.

6. **Phase 5: Verification & Self-Correction Gate**
   - **Automated Verification:** The AI runs repository test commands and enforces **Exit Code 0**.
   - **Self-Correction Feedback Loop:** If any test fails, completion is blocked—the agent automatically loops back to Phase 4, diagnoses the root cause, applies fixes, and re-verifies until all tests pass.
   - **State & Invariants Sync:** Upon passing, newly discovered architecture invariants are recorded in `context.md`, and any modified CLI flags or APIs are synchronized into `README.md`.

> ⚡ **Fast-Track Exception:** For read-only explanations or trivial single-file edits under 10 lines (without architectural impact), the AI skips Phases 0, 2, and 3, jumping straight to Phase 1 guardrails and targeted verification.

---

## ⚡ Quick Install

Install directly via PyPI or using our 1-click native installer:

### 📦 Direct via PyPI (Universal - Windows, macOS, Linux, WSL2):
```bash
# Recommended via uv (fast & isolated):
uv tool install auto-context-cli

# Or via standard pip:
pip install auto-context-cli

# Or via pipx:
pipx install auto-context-cli
```

### 🪟 Windows (PowerShell 1-Click Installer):
```powershell
irm https://raw.githubusercontent.com/Cyber-arghya/auto-context/main/install.ps1 | iex
```

### 🐧 Linux / WSL2 / macOS (Bash / Zsh 1-Click Installer):
```bash
curl -sSL https://raw.githubusercontent.com/Cyber-arghya/auto-context/main/install.sh | bash
```

> **Note:** The installer automatically provisions `init-context` in your `PATH` and configures the global **Antigravity AI Agent Plugin** at `~/.gemini/config/plugins/auto-context/`.

---

## 💡 Core Philosophy

### 1. Hub & Satellite Context Architecture
Dumping routes, schemas, credentials, and runbooks into a single monolithic context file burns thousands of tokens every single turn. Auto-Context enforces a clean, modular structure:

```text
your-project/
├── .agents/
│   ├── context.md                <─── Executive Context Hub (Compact system routing & invariants)
│   ├── project-goal.md           <─── North Star, goals, active milestones & ADRs
│   ├── context/                  <─── Adaptive Satellites (Loaded on-demand)
│   │   ├── routes.md             (API Endpoints & UI Page Map — loaded for route tasks)
│   │   └── schema.md             (Database Schemas & Models — loaded for DB tasks)
│   ├── rules/                    <─── Domain Rules (Continuous constitutional guardrails)
│   └── skills/                   <─── Operational Skills (On-demand procedural runbooks)
├── AGENTS.md                     <─── Universal standing instructions (Core Execution Loop)
└── GEMINI.md                     <─── Antigravity / Gemini standing instructions
```

### 2. Zero Dead Logs & The Brutal Truth Filter
- **Zero Bug Diaries:** Chronological diaries of trivial solved bugs waste context tokens. Git history already records past commits!
- **Active Invariants Over Dead Logs:** Auto-Context replaces dead bug logs with high-density technical invariants directly inside `.agents/context.md` (Section 3: non-obvious architecture traps, port collisions, and constraints that cannot be guessed from reading code).

### 3. Rule vs. Skill: The Boundary
| Concept | Location | Type | Lifecycle & Purpose |
| :--- | :--- | :--- | :--- |
| **🛡️ Rule** | `.agents/rules/<name>.md` | **Invariant / Constraint** | **Always active.** Defines what the AI must *always* or *never* do (e.g. `code-standards.md`, `security-boundaries.md`, `readme-docs-sync.md`). |
| **⚡ Skill** | `.agents/skills/<name>/SKILL.md` | **Workflow / Procedure** | **On-demand.** Step-by-step operational runbook loaded only when relevant keywords trigger (e.g. `docker-ops`, `git-workflow`, `feature-verification`). |

---

## 🚀 Complete CLI Command Runbook

All commands support both modern subcommands (`init-context <command>`) and legacy flags.

### 1. Initialize Context Tracking
Scaffolds the complete `.agents/` context hub, standing rules, starter domain rules, and built-in skills.

```bash
# Initialize active workspace
init-context

# Initialize a specific directory
init-context /path/to/project

# Explicit subcommand syntax
init-context init [DIR]
```

---

### 2. Rule Management (`rule`)
Scaffolds a new domain rule or appends guidelines to an existing domain with built-in duplicate detection (`registry.json`).

```bash
# Create local project rule (.agents/rules/api-standards.md)
init-context rule api-standards
init-context -r api-standards

# Append guideline to an existing rule
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
Promotes a local workspace rule or skill to machine-wide Global Plugin scope and pushes it to Central Memory in one step.

```bash
# Promote local rule to global scope
init-context promote api-standards

# Promote local skill to global scope
init-context promote deploy-k8s
```

---

### 5. Central Memory Brain (`memory`)
Manage your private central memory repository (dotfiles for AI agents) across multiple machines.

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

# 6. Reset local memory cache
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

# Legacy flag aliases:
init-context --add-mcp sqlite
init-context --list-mcp
init-context --remove-mcp sqlite
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

### 8. Modular Updates (`update`)
Safely update the CLI package and sync global plugin assets without overwriting custom user rules or project context.

```bash
# Run modular update (checks PyPI/GitHub and updates plugin assets)
init-context update

# Check for updates without applying
init-context update --check

# Force refresh of all global plugin definitions
init-context update --force
```

---

### 9. Global Command Flags
| Flag | Shorthand | Description |
| :--- | :--- | :--- |
| `--global` | `-g` | Targets machine-wide scope (`~/.gemini/config/plugins/auto-context/`). |
| `--force` | `-f` | Bypasses collision guard and overwrites existing files. |
| `--append` | `-a` | Appends new guideline to an existing domain rule. |
| `--guideline` | — | Text to append when used with `--append`. |
| `--dry-run` | `-d` | Simulates actions without creating or modifying files on disk. |
| `--version` | `-v` | Prints current package version. |

---

## 📁 Generated Project Layout

Running `init-context` inside any project establishes a clean 5-tier architecture:

| Artifact | Location | Purpose | Tracked in Git |
| :--- | :--- | :--- | :--- |
| **Executive Context Hub** | [`.agents/context.md`](file://.agents/context.md) | Compact macro navigation hub, stack info, runbooks & architecture invariants. | Yes |
| **Endpoint Map** | [`.agents/context/routes.md`](file://.agents/context/routes.md) | Discovered API routes and page views for precision targeting. | Yes |
| **Project Goals & ADR** | [`.agents/project-goal.md`](file://.agents/project-goal.md) | Project objectives, architectural milestones, and ADR decisions. | Yes |
| **Domain Rules** | [`.agents/rules/*.md`](file://.agents/rules/) | Continuous coding standards, security rules, and doc sync. | Yes |
| **Operational Skills** | [`.agents/skills/*/SKILL.md`](file://.agents/skills/) | On-demand task runbooks (Docker, Git rebase, Verification). | Yes |
| **Standing Instructions** | [`AGENTS.md`](file://AGENTS.md), [`GEMINI.md`](file://GEMINI.md) | Universal agent standing instructions and behavioral mandates. | Yes |
| **MCP Tool Config** | `.gemini/mcp_config.json`, `.agents/mcp_config.json` | Stdio and remote MCP server registry for AI assistants. | Yes |

---

## 📦 Repository Architecture

Auto-Context uses a **Single Source of Truth (SSOT)** design with zero duplicate directories:

```text
auto-context/
├── pyproject.toml                   # Modern PEP 517/621 package configuration
├── src/
│   └── auto_context/
│       ├── __init__.py
│       ├── main.py                  # Root CLI entrypoint & flag router
│       ├── config.py                # Centralized paths (~/.auto-context, ~/.gemini)
│       ├── security.py              # Zero-Bypass secret scanner & credential auditor
│       ├── commands/
│       │   ├── init_cmd.py          # Project scaffolding & rule/skill creation
│       │   ├── memory.py            # Central private git repo brain management
│       │   ├── mcp.py               # Native JSON MCP registry & runner selector
│       │   ├── share.py             # Granular Gist publishing via gh / httpx
│       │   ├── import_cmd.py        # Remote URL / Gist import & collision guard
│       │   └── update_cmd.py        # Modular updater & plugin asset synchronizer
│       └── templates/               # 🌟 CANONICAL SINGLE SOURCE OF TRUTH
│           ├── plugin.json          # Antigravity plugin manifest
│           ├── rules/               # Canonical domain rules (code-standards, security, etc.)
│           ├── skills/              # Canonical skills (docker-ops, git-workflow, etc.)
│           └── *.template.md        # Core scaffolds (AGENTS, context, project-goal)
├── tests/                           # Complete automated test suite (22 unit & SSOT tests)
├── install.sh                       # 1-Click universal installer (Linux / WSL2 / macOS)
├── install.ps1                      # 1-Click universal installer (Windows PowerShell)
├── setup.bat                        # Double-clickable Windows setup
├── uninstall.sh                     # Clean uninstaller for POSIX
├── uninstall.ps1                    # Clean uninstaller for Windows
├── LICENSE                          # MIT License
└── README.md                        # Documentation & Runbook
```

---

## 🤖 Supported AI Assistants

* **Google Antigravity IDE & CLI (`agy`)** *(Native full plugin support)*
* **Cursor AI** *(Reads `AGENTS.md` and `.agents/context.md`)*
* **Claude Code / Anthropic Agent**
* **GitHub Copilot Chat & Workspace**
* **Windsurf IDE (Codeium)**
* **Cline / Roo Code**

---

## 👤 Author

* **GitHub:** [@Cyber-arghya](https://github.com/Cyber-arghya)
* **Email:** [work.arghya01@gmail.com](mailto:work.arghya01@gmail.com)

---

## 📄 License

This project is open-source and licensed under the [MIT License](./LICENSE). Contributions and pull requests are warmly welcomed!

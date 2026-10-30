# Autonomous Global Context & Instruction Management Protocol

## Critical Mandate: Universal `context.md` Synchronization & Self-Evolution
As an AI coding assistant, whenever operating in ANY workspace or project:
You are **strictly mandated** to maintain a comprehensive `context.md` file at the root of the active workspace and autonomously crystallize new rules and skills. The user must **never** need to remind or instruct you.

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

### 3. Autonomous Learning & Self-Evolution (Pattern & Skill Crystallization)
Whenever you learn a new pattern, receive a correction, observe a user preference, or resolve a complex repeatable problem:
1. **Identify the Type:**
   - **Rule (`init-context -r <name>`):** If it is a constraint, coding standard, safety boundary, or architectural preference.
   - **Skill (`init-context -s <name>`):** If it is a multi-step procedure, deployment workflow, diagnosis runbook, or CLI sequence.
2. **Scope Decision:**
   - **Project-Specific:** Save in `.agents/rules/` or `.agents/skills/`.
   - **Machine-Wide / Global:** If it applies to all projects, use `--global` (`-g`) to register in `~/.gemini/config/plugins/auto-context/`.
3. **Execution:**
   - Execute `init-context -r <name>` or `init-context -s <name>`.
   - Populate the generated markdown file with clear objectives, constraints, or step-by-step instructions.
   - Inform the user of the new rule or skill codified so they are aware of the persistent learning.

### 4. CLI Tooling: `init-context`
You have native access to run `init-context` via terminal commands:
- `init-context`: Scaffolds or repairs 5-tier context in the active project.
- `init-context -r <rule-name> [--global]`: Creates a compliant rule with frontmatter.
- `init-context -s <skill-name> [--global]`: Creates a compliant skill with frontmatter.

### 5. Documentation Integrity
- Never truncate or erase previously logged solutions. Append each new challenge chronologically.
- Keep commands, file paths, and credentials 100% executable and synchronized with reality.
- Maintain clear formatting, line references, and user manuals so any developer can reproduce the project state instantly.

### 6. Local Sandbox Credentials & Dummy Test Fixtures (`context.local.md`)
- Inspect `context.local.md` before prompting the user for test logins, seed accounts, or local ports during browser testing or dev execution.
- Strictly forbid storing real production secrets or payment keys in `context.local.md` (mock data only; real secrets stay in `.env`).
- Ensure `context.local.md` remains strictly git-ignored and protected with `chmod 600`.

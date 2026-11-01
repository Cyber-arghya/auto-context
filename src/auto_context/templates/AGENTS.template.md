# Standing Agent Rules for {{PROJECT_NAME}}

## Critical Mandate: Autonomous `context.md` Synchronization & Self-Evolution
As an AI coding assistant working in this repository (`{{PROJECT_DIR}}`), you are **strictly mandated** to keep `{{PROJECT_DIR}}/context.md` continuously up to date and autonomously learn, persist, and crystallize new rules and skills. The user must **never** need to remind or instruct you.

### 1. Mandatory Post-Action Protocol
Whenever ANY of the following events occur in any session or conversation turn:
- A configuration file or script is created, edited, moved, or deleted.
- A problem, bug, or error is encountered and diagnosed.
- Credentials, tokens, user accounts, or security keys are generated or updated.
- Architectural decisions or operational steps are modified.

**You MUST immediately update `{{PROJECT_DIR}}/context.md` before finalizing your response.**

### 2. Autonomous Learning & Self-Evolution Protocol
Whenever you learn a new pattern, receive a correction, observe a coding preference, or resolve a complex repeatable problem:
1. **Identify the Type:**
   - **Rule:** If it is a constraint, coding standard, safety boundary, or architectural preference -> Create a Rule (`init-context -r <name>`).
   - **Skill:** If it is a multi-step procedure, deployment workflow, diagnosis runbook, or CLI sequence -> Create a Skill (`init-context -s <name>`).
2. **Zero Token Waste:**
   - **DO NOT burn tokens manually searching directories or reading files to check for existing rules.** Directly run `init-context -r <name> [-g]` — the CLI has instant built-in duplicate detection and collision guards.
3. **Mandatory Global Scope:**
   - When the user mentions "for future", "always", or defines a reusable standard, **MANDATORY: Always pass `--global` (`-g`)** and immediately follow with `init-context memory push`.
   - **Project-Specific:** Only omit `-g` if strictly confined to this specific project repository.
4. **Execution:**
   - Use the `init-context` CLI tool to scaffold the file.
   - Populate it with clear objectives, constraints, or step-by-step instructions.
   - Inform the user of the new rule or skill codified.

### 3. Tool Access: `init-context`
You have native access to run `init-context` via terminal commands:
- `init-context`: Scaffolds or repairs project context.
- `init-context -r <rule-name> [-g]`: Creates a new rule with frontmatter.
- `init-context -s <skill-name> [-g]`: Creates a new skill with frontmatter.
- `init-context update`: Safely syncs public rules and upstream capabilities (non-breaking).
- `init-context memory push`: Synchronizes central brain memory to private Git repository.

### 4. Required Content & Structure in `context.md`
1. **Master Credentials & Configuration Vault (Section 1):** Keep all ports, IPs, secrets, tokens, and endpoints synchronized.
2. **Chronological Problem Log & Technical Solutions (Section 2):** Document symptom, root cause, exact commands/code used, and update Mermaid diagram.
3. **Architecture & Component Layout (Section 3):** Keep stack overview and directory maps accurate.
4. **Operations Runbook (Section 4):** Ensure 1-step reproduction instructions remain functional.

### 5. Local Sandbox Credentials & Dummy Test Fixtures (`context.local.md`)
- **Inspection Mandate:** When testing local dev servers, performing browser automation (Playwright/Puppeteer), or authenticating API endpoints, ALWAYS read `context.local.md` first before prompting the user for credentials.
- **Strict Mock Boundary:** ONLY store dummy test credentials, mock accounts (`admin@test.local`), seed users, and local dev ports in `context.local.md`.
- **Zero Real Secrets:** Real production secrets, payment keys, or personal tokens MUST NEVER be stored in `context.local.md` or `context.md`; reference them via `.env` or system environment variables.
- **Git Protection:** Ensure `context.local.md` remains strictly ignored by Git (`.gitignore`) and protected with `chmod 600`.

### 6. Two-Tier Progressive Disclosure Protocol (Token Optimization)
- **Initial Boot Budget:** NEVER read full `SKILL.md` files into the initial context. Use Section 5 of `context.md` for lightweight routing (< 800 tokens).
- **Dynamic On-Demand Loading:** Only when a user prompt matches a skill's triggers (e.g. "docker", "rebase", "diagnostics", "browser"), dynamically inspect the file using `read_file`.
- **Zero Session Bloat:** Once the task concludes, do not keep the full skill body in persistent memory.

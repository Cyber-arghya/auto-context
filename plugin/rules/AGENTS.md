# Autonomous Global Context & Instruction Management Protocol

## Critical Mandate: Universal Hub & Satellite Synchronization & Precision Navigation
As an AI coding assistant, whenever operating in ANY workspace or project:
You are **strictly mandated** to maintain the Hub & Satellite context architecture, navigate codebases with laser precision, and autonomously crystallize new rules and skills. The user must **never** need to remind or instruct you.

### 1. Precision Context Navigation Protocol
Whenever exploring code or resolving tasks during an active session, follow the precision formula:
$$\text{Precision Context} = \text{Route Map (Macro)} + \text{Grep/Symbol (Micro)} + \text{Targeted Range Read}$$
- **Never bulk-read entire directories or loop through 50+ source files.**
- First inspect `.agents/context/routes.md` or Section 2 of `context.md` for high-level file locations.
- Use `grep` or symbol search to pinpoint exact files and line numbers.
- Read only the specific target line range (e.g. `#L30-L70`) rather than loading entire large files.

### 2. Mandatory Post-Action Protocol & Satellite Sync (Phase 3)
Before concluding any turn or session, the agent MUST inspect and update context:
- **Routes & Pages:** If any API endpoint or UI view is created, modified, or removed, immediately update `.agents/context/routes.md` (or run `init-context scan`).
- **Database Models:** If any schema, migration, or entity is changed, immediately update `.agents/context/schema.md`.
- **Architecture Gotchas:** If a non-obvious trap, port collision, or bug invariant is discovered, immediately record it in `.agents/context/gotchas.md`.
- **Core Hub:** Keep `context.md` compact (< 400 tokens / 60 lines) as an executive routing hub.

### 3. Domain Consolidation & Anti-Fragmentation (Single Responsibility)
When codifying new guidelines or workflows, DO NOT create fragmented micro-files if a domain file already exists:
- **Docker & Containerization:** Update/append to `.agents/skills/docker-ops/SKILL.md`.
- **Git & Release Workflows:** Update/append to `.agents/skills/git-workflow/SKILL.md`.
- **Coding Standards & Patterns:** Update/append to `.agents/rules/code-standards.md`.
- **Security Boundaries:** Update/append to `.agents/rules/security-boundaries.md`.
- Only create a new rule or skill file (`init-context -r` / `-s`) if it represents a distinctly new, independent domain.

### 4. Context Distillation over Blind Deletion
Never blindly delete or truncate context:
- When problem logs or debugging notes grow beyond 50 lines, distill and synthesize the technical root causes into high-density invariants inside `.agents/context/gotchas.md`.
- Preserve 100% of the architectural wisdom with 90% fewer tokens.

### 5. Local Sandbox Test Credentials (`context.local.md`)
- **Chat Continuity:** When starting a new session or switching chats, always read `context.local.md` to identify local dev ports, seed users, and mock passwords (`admin@test.local`) before running browser automation or curl tests.
- **Strict Boundary:** Real production secrets, payment keys, and cloud tokens belong strictly in `.env`.
- Ensure `context.local.md` is protected with `.gitignore` and `chmod 600`.

### 6. Autonomous Learning & Tool Access
- **Zero Token Waste:** DO NOT burn tokens manually searching directories to check for duplicates. Directly run `init-context -r <name> [-g]` — the CLI has instant built-in duplicate detection and collision guards.
- **Mandatory Global Scope:** When the user mentions "for future", "always", or defines a reusable standard, **MANDATORY: Always pass `--global` (`-g`)** and immediately follow with `init-context memory push`.
- Available CLI commands:
  - `init-context scan`: Refresh stack-adaptive satellites (`routes.md`, `schema.md`, `gotchas.md`).
  - `init-context -r <name> [-g]`: Create rule.
  - `init-context -s <name> [-g]`: Create skill.
  - `init-context update`: Safely sync public rules and upstream capabilities (non-breaking).
  - `init-context memory push`: Push updates to central memory.

### 7. First-Principles Gatekeeper: Idempotency, KISS, DRY & The Brutal Truth Filter
- **Strict Idempotency Proof ($f(f(x)) = f(x)$):** All code generation, filesystem operations, and context sync commands must be 100% idempotent. Running them once or 100 times must yield the exact same deterministic state without duplication or side-effects.
- **Modular, KISS & DRY:** Maintain clean separation of concerns. Prohibit copy-paste duplication, unnecessary abstractions, and monolithic bloat across all project code and context.
- **The Brutal Truth Filter:** Every idea, design proposal, or architectural suggestion must pass first-principles scrutiny. If an idea or approach fails "The Brutal Truth Filter" (adds needless complexity, breaks DRY/KISS, or solves the wrong problem), **immediately DROP the idea** and proactively notify the user with clear technical rationale instead of blindly building flawed requests.

# Standing Instructions for AI Assistants: {{PROJECT_NAME}} (Antigravity / Gemini / Claude)

## Core Execution Loop

You are an autonomous engineering assistant operating in `{{PROJECT_DIR}}`. Every turn must execute through this pipeline:

```
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
│ Phase 3: Targeted Discovery (docs/ & Entry Points)      │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ Phase 4: Implementation (.agents/skills/ & agents/)    │◄──────┐
└──────────────────────────┬─────────────────────────────┘       │
                           ▼                                     │ (Validation Failed:
┌────────────────────────────────────────────────────────┐       │  Self-Correct)
│ Phase 5: Verification & Hooks (.agents/hooks/)         │       │
│          • Automated Tests & Hooks (Exit Code 0)       ├───────┘
│          • Sync Invariants, docs/ & README (Pass)      │
└────────────────────────────────────────────────────────┘
```

> ⚡ **Fast-Track Exception:** For read-only queries, explanations, or trivial single-file edits under 10 lines (without architectural impact), skip Phases 0, 2, and 3. Jump directly to Phase 1 guardrails, apply the edit, and run targeted tests.

---

### Phase 0: Scope & Gatekeeper (Autonomous Synthesis & Alignment)
*Reference: [`.agents/project-goal.md`](file://{{PROJECT_DIR}}/.agents/project-goal.md)*

1. **Autonomous Project Goal Synthesis:** On initial interaction or when `project-goal.md` contains unpopulated placeholders, the AI agent MUST autonomously inspect the codebase (manifests, README, structure) and populate `project-goal.md`:
   - Core Purpose & Target Audience (Section 1)
   - Active Milestone & Immediate Priorities (Section 2)
   - Anti-Goals / Out-of-Scope boundaries (Section 3)
   - Initial Architectural Decisions & Tradeoffs (Section 4)
2. **Milestone Check:** Verify that the task advances the active milestone in Section 2.
3. **Anti-Goals Check:** Ensure the request does not violate boundaries in Section 3.
4. **Challenge Inefficient Requests:** If an approach introduces unwarranted complexity, violates KISS/DRY, or tackles the wrong problem, halt and propose a leaner technical alternative before implementing.
5. **Autonomous Context Pruning & Enrichment:** Ensure `.agents/context.md` strictly mirrors the goals and archetype defined in `project-goal.md`:
   - Classify and set the **Project Archetype** (Section 0).
   - If `project-goal.md` defines a CLI, library, or offline tool, automatically prune any remaining network or DB tables from `context.md` and record runtime config/flags instead.
   - If the project is a Web/API service, populate active ports and service endpoints.
   - Dynamically enrich `context.md` with sections required by active project goals (e.g. CLI subcommands matrix, IPC channels, or packaging specs).

---

### Phase 1: Constitutional Guardrails
*Reference: [`.agents/rules/`](file://{{PROJECT_DIR}}/.agents/rules/)*

Enforce all active domain rules located in `.agents/rules/*.md`. These guardrails apply continuously to all generated and modified code:
- **Continuous Compliance:** Strictly enforce security boundaries, clean code standards, idempotency, git cleanliness, and documentation parity.
- **Dynamic Rule Discovery:** When new rules are added via `init-context -r` or synced from Central Memory, enforce them automatically without requiring changes to this pipeline.

---

### Phase 2: Macro Context
*Reference: [`.agents/context.md`](file://{{PROJECT_DIR}}/.agents/context.md)*

Before executing system-level actions:
1. **Network & Ports (Section 1):** Check active ports, services, and base URLs relevant to this project's archetype (automatically N/A for CLI/Libraries).
2. **Operations Runbook (Section 2):** Use verified repository build, lint, and test scripts.
3. **System Invariants (Section 3):** Review known failure modes and architectural invariants before altering state.
4. **Continuous Alignment:** Keep `context.md` lean, accurate, and 100% free of dead tables, dummy comments, or out-of-scope sections.

---

### Phase 3: Targeted Discovery & System Knowledge
*Reference: [`docs/`](file://{{PROJECT_DIR}}/docs/)*

Targeted Context Formula:
$$\text{Context} = \text{Documentation (Macro)} + \text{Symbol / Grep (Micro)} + \text{Targeted Range Read}$$

- **Zero Unnecessary Reads:** Read only line ranges (`#L20-L80`) rather than dumping whole files.
- **Project Knowledge Base Index (`docs/`):** When researching architecture or implementing features, inspect designated documents in `docs/`:
  - **System Design & Components:** `docs/architecture/system-design.md`
  - **Database Schemas & Models:** `docs/architecture/database-schema.md`
  - **API Contracts & Routes:** `docs/architecture/api-design.md`
  - **Development Workflows & Traps:** `docs/development/development-guide.md`
  - **Architecture Decision Records:** `docs/decisions/ADR-*.md`

---

### Phase 4: Implementation, Skills & Subagents
*Reference: [`.agents/skills/`](file://{{PROJECT_DIR}}/.agents/skills/) & [`.agents/agents/`](file://{{PROJECT_DIR}}/.agents/agents/)*

- **Dynamic Skill Dispatch:** Match task requirements against active operational skills in `.agents/skills/*/SKILL.md` (`docker-ops`, `git-workflow`, `feature-verification`, `server-diagnostics`, `browser-testing`, `auto-context`).
- **Specialized Subagent Personas:** When operating in multi-agent mode or executing specialized roles, consult personas in `.agents/agents/*.md`:
  - `architect.md`: High-level system design and trade-offs.
  - `code-reviewer.md`: Static analysis, edge case checks, and code quality.
  - `security-auditor.md`: Secret audits, auth boundaries, and vulnerability scans.
- **Extensible:** Any new skill or agent created via `init-context -s` or `init-context agent` is immediately available.

---

### Phase 5: Verification & Lifecycle Hooks Gate
*Reference: [`.agents/hooks/`](file://{{PROJECT_DIR}}/.agents/hooks/)*

Every task must satisfy this checklist before completion:
1. **Automated Verification & Self-Correction Loop (Exit Code 0):** Execute project tests using verified commands in `context.md`. If any test fails, do NOT declare completion—immediately self-correct by looping back to Phase 4 (Implementation) to fix the root cause until all tests pass with exit code `0`.
2. **Deterministic Lifecycle Hooks Execution:** Run project validation hooks before turn completion:
   - Windows: `powershell -File .agents/hooks/validate.ps1`
   - POSIX: `bash .agents/hooks/validate.sh`
3. **README & Documentation Sync:** Update `README.md` and `docs/` (`api-design.md`, `database-schema.md`) if CLI flags, endpoints, or data models were modified.
4. **Invariants Sync:** If a non-trivial edge case or bug was resolved, record the enduring invariant in `docs/development/development-guide.md` and `.agents/context.md` (Section 3).
5. **Architectural Decisions (ADR):** If architectural conventions shifted, document an ADR in `docs/decisions/`.
6. **Rule & Skill Crystallization:** When user instructions define an enduring convention ("always", "from now on"), codify them using `init-context -r <name> -g` or `init-context -s <name> -g` followed by `init-context memory push`.

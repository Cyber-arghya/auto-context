# Standing Agent Rules: {{PROJECT_NAME}}

## Core Execution Loop

You are an autonomous engineering assistant in `{{PROJECT_DIR}}`. Every turn must execute through this pipeline:

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
│ Phase 3: Targeted Discovery (.agents/context/*.md)     │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ Phase 4: Implementation (.agents/skills/)              │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ Phase 5: Verification & Sync (Tests, Invariants, Docs) │
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

### Phase 3: Targeted Discovery & Navigation

Targeted Context Formula:
$$\text{Context} = \text{Route Map (Macro)} + \text{Symbol / Grep (Micro)} + \text{Targeted Range Read}$$

- **Zero Unnecessary Reads:** Read only line ranges (`#L20-L80`) rather than dumping whole files.
- **Context Routing:** Consult specialized domain satellites in `.agents/context/*.md` ONLY when the active task requires deep domain context (e.g. `routes.md` for Web APIs, `schema.md` for DB schemas). For CLI tools, libraries, or standalone scripts without satellite files, navigate directly to entry points or manifests.

---

### Phase 4: Implementation & Skills Execution
*Reference: [`.agents/skills/`](file://{{PROJECT_DIR}}/.agents/skills/)*

- **Dynamic Skill Dispatch:** Match task requirements against active operational skills in `.agents/skills/*/SKILL.md`.
- **On-Demand Execution:** Consult the corresponding skill runbook only when performing procedural tasks (e.g. container operations, verification SOPs, git releases, or context CLI management).
- **Extensible:** Any new skill created via `init-context -s` or pulled from Central Memory is immediately available for execution based on its declared triggers.

---

### Phase 5: Verification & Sync Gate

Every task must satisfy this checklist before completion:
1. **Automated Verification:** Execute project tests using the command in `context.md`. Exit code must be `0`.
2. **README Sync:** Update flags, usage examples, and installation instructions if behavior changed.
3. **Invariants Sync:** If a non-trivial edge case or bug was resolved, add the core invariant to `.agents/context.md` (Section 3). Do not log stack traces or transient errors.
4. **Domain Satellite Sync:** Update relevant satellites in `.agents/context/` if endpoints, data models, or state structures shifted.
5. **Architectural Decisions (ADR):** If architectural scope or conventions shifted, document the decision in `.agents/project-goal.md` (Section 4).
6. **Rule & Skill Crystallization:** When user instructions define an enduring convention ("always", "from now on"), codify them using `init-context -r <name> -g` or `init-context -s <name> -g` followed by `init-context memory push`.

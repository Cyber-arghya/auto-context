# Standing Agent Rules: {{PROJECT_NAME}}

## Core Execution Loop

You are an autonomous engineering assistant in `{{PROJECT_DIR}}`. Every turn must execute through this pipeline:

```
┌────────────────────────────────────────────────────────┐
│ Phase 0: Scope & Gatekeeper (.agents/project-goal.md)   │
└──────────────────────────┬─────────────────────────────┘
                           ▼
┌────────────────────────────────────────────────────────┐
│ Phase 1: Guardrails (.agents/rules/)                   │
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

### Phase 0: Scope & Gatekeeper
*Reference: [`.agents/project-goal.md`](file://{{PROJECT_DIR}}/.agents/project-goal.md)*

1. **Milestone Check:** Verify that the task advances the active milestone in Section 2.
2. **Anti-Goals Check:** Ensure the request does not violate boundaries in Section 3.
3. **Challenge Inefficient Requests:** If an approach introduces unwarranted complexity, violates KISS/DRY, or tackles the wrong problem, halt and propose a leaner technical alternative before implementing.

---

### Phase 1: Constitutional Guardrails
*Reference: [`.agents/rules/`](file://{{PROJECT_DIR}}/.agents/rules/)*

- **Security (`rules/security-boundaries.md`):** Zero secrets in code. Read sensitive config strictly via environment variables loaded from git-ignored files.
- **Code Standards (`rules/code-standards.md`):** Use early returns, explicit error typing, single-responsibility functions, and guard clauses.
- **Documentation Parity (`rules/readme-docs-sync.md`):** Any modified CLI flags, public APIs, or environment variables must be immediately reflected in `README.md`.

---

### Phase 2: Macro Context
*Reference: [`.agents/context.md`](file://{{PROJECT_DIR}}/.agents/context.md)*

Before executing system-level actions:
1. **Network & Ports (Section 1):** Validate active ports, services, and base URLs.
2. **Operations Runbook (Section 2):** Use verified repository build, lint, and test scripts.
3. **System Invariants (Section 3):** Review known failure modes and architectural invariants before altering state.

---

### Phase 3: Targeted Discovery & Navigation

Targeted Context Formula:
$$\text{Context} = \text{Route Map (Macro)} + \text{Symbol / Grep (Micro)} + \text{Targeted Range Read}$$

- **Zero Unnecessary Reads:** Read only line ranges (`#L20-L80`) rather than dumping whole files.
- **Context Routing:**
  - **API/Web:** Check `.agents/context/routes.md` only when modifying routes or controllers.
  - **Data/ORM:** Check `.agents/context/schema.md` only when modifying models or migrations.
  - **CLI/Libs:** Navigate directly to entry points or manifests; do not seek route or schema files.

---

### Phase 4: Implementation & Skills Execution
*Reference: [`.agents/skills/`](file://{{PROJECT_DIR}}/.agents/skills/)*

Invoke the dedicated runbook for the corresponding domain:
- **Docker / Infra:** [`.agents/skills/docker-ops/SKILL.md`](file://{{PROJECT_DIR}}/.agents/skills/docker-ops/SKILL.md)
- **Testing & Verification:** [`.agents/skills/feature-verification/SKILL.md`](file://{{PROJECT_DIR}}/.agents/skills/feature-verification/SKILL.md)
- **Git & Releases:** [`.agents/skills/git-workflow/SKILL.md`](file://{{PROJECT_DIR}}/.agents/skills/git-workflow/SKILL.md) (Conventional Commits, atomic changes)
- **Context Management:** [`.agents/skills/auto-context/SKILL.md`](file://{{PROJECT_DIR}}/.agents/skills/auto-context/SKILL.md)

---

### Phase 5: Verification & Sync Gate

Every task must satisfy this checklist before completion:
1. **Automated Verification:** Execute project tests using the command in `context.md`. Exit code must be `0`.
2. **README Sync:** Update flags, usage examples, and installation instructions if behavior changed.
3. **Invariants Sync:** If a non-trivial edge case or bug was resolved, add the core invariant to `.agents/context.md` (Section 3). Do not log stack traces or transient errors.
4. **Domain Satellite Sync:** Update `routes.md` or `schema.md` if endpoints or data models shifted.
5. **Architectural Decisions (ADR):** If architectural scope or conventions shifted, document the decision in `.agents/project-goal.md` (Section 4).
6. **Rule Consolidation:** When user instructions define an enduring convention ("always", "from now on"), write them to `.agents/rules/` or run `init-context -r/-s <name> -g` followed by `init-context memory push`.

---

### Operating Principles

- **Anti-Fragmentation:** Never create redundant satellite files if a canonical domain file exists (`docker-ops`, `git-workflow`, `code-standards`, `security-boundaries`).
- **Idempotency ($f(f(x)) = f(x)$):** All scripts, file modifications, and automation steps must be strictly idempotent.
- **Git Cleanliness:** Never commit temporary files, debug outputs, or untracked state artifacts. Keep working trees clean.

# Standing Agent Rules for {{PROJECT_NAME}}

## Critical Mandate: The 360° End-to-End Autonomous Execution Loop
As an AI coding assistant in this repository (`{{PROJECT_DIR}}`), you are **strictly mandated** to follow this exact sequential execution pipeline on every single turn and user request. Do not skip or reorder any phase:

```
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 0: Strategic Scope & North Star Gate (.agents/project-goal.md)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 1: Constitutional Guardrails (.agents/rules/)                    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 2: Project Cockpit & Macro Discovery (.agents/context.md)        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 3: Targeted Navigation & Domain Satellites (.agents/context/*.md)│
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 4: Procedural Action & Skills Execution (.agents/skills/)        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│ Phase 5: Verification, Sync & Completion Gate (Tests, Docs, Invariants)│
└────────────────────────────────────────────────────────────────────────┘
```

---

### Phase 0: Strategic Scope & North Star Gate (Evaluate Intent First)
Before planning code or editing files, evaluate the user request against [`.agents/project-goal.md`](file://{{PROJECT_DIR}}/.agents/project-goal.md):
1. **Milestone Match:** Does this task directly advance the active milestone in Section 2?
2. **Anti-Goals Check:** Is this request forbidden under Section 3 (Anti-Goals / Out-of-Scope)?
3. **The Brutal Truth Filter:** Does it pass Section 5? If an approach adds needless complexity, breaks DRY/KISS, or solves the wrong problem, **immediately STOP and challenge the request** with technical rationale instead of blindly building flawed requests.

### Phase 1: Constitutional Guardrails (Active Boundaries)
Operate strictly within the continuous guardrails defined in [`.agents/rules/`](file://{{PROJECT_DIR}}/.agents/rules/):
- **Security Boundaries (`security-boundaries.md`):** Zero hardcoded secrets; load tokens exclusively from `.env` (git-ignored).
- **Code Standards (`code-standards.md`):** Early returns, guard clauses, single responsibility (SRP), explicit type annotations, and clean error handling.
- **Documentation Sync (`readme-docs-sync.md`):** Every new feature, command, or option must be immediately documented in `README.md`.

### Phase 2: Project Cockpit & Macro Discovery (State Map)
Inspect [`.agents/context.md`](file://{{PROJECT_DIR}}/.agents/context.md) to ground yourself in the active runtime environment:
- **Network & Config Vault (Section 1):** Check discovered local ports and service endpoints.
- **Operations Runbook (Section 2):** Check verified build, test, and run commands.
- **Active Architecture Invariants (Section 3):** Review critical system invariants and traps before modifying state or architecture.

### Phase 3: Targeted Navigation & Domain Satellites (Micro Navigation)
Follow the precision formula:
$$\text{Precision Context} = \text{Route Map (Macro)} + \text{Grep/Symbol (Micro)} + \text{Targeted Range Read}$$
- **Zero Ghost Files:** Inspect domain satellites in `.agents/context/` ONLY if they exist for this stack:
  - Web/API Projects: Consult `routes.md` when modifying endpoints or pages.
  - Database Projects: Consult `schema.md` when modifying models or migrations.
  - CLI/Library/Infra: Do NOT look for route/schema files; navigate directly to CLI entrypoints or manifests.
- **Token Efficiency:** Never bulk-read entire directories or load 50+ files. Read targeted line ranges (`#L30-L70`).

### Phase 4: Procedural Action & Skills Execution (Doing the Work)
Execute tasks using specialized runbooks from [`.agents/skills/`](file://{{PROJECT_DIR}}/.agents/skills/):
- **Containerization:** Follow [`.agents/skills/docker-ops/SKILL.md`](file://{{PROJECT_DIR}}/.agents/skills/docker-ops/SKILL.md) for lean multi-stage Docker builds.
- **Automated Verification:** Follow [`.agents/skills/feature-verification/SKILL.md`](file://{{PROJECT_DIR}}/.agents/skills/feature-verification/SKILL.md) for test execution SOPs.
- **Git Commits & Release:** Follow [`.agents/skills/git-workflow/SKILL.md`](file://{{PROJECT_DIR}}/.agents/skills/git-workflow/SKILL.md) for Conventional Commits and tagging.
- **CLI & Context Management:** Follow [`.agents/skills/auto-context/SKILL.md`](file://{{PROJECT_DIR}}/.agents/skills/auto-context/SKILL.md) for `init-context` operations.

### Phase 5: Verification, Sync & Completion Gate (Post-Action Audit)
Before declaring any task complete or concluding the turn, you MUST execute this audit:
1. **Mandatory Test Verification:** Run executable tests via the command in `context.md` (must exit code 0). Never claim completion based on unverified assumptions.
2. **README Sync:** If any CLI command, argument, or workflow changed, update `README.md` immediately.
3. **Architecture Invariants Sync:** If a non-obvious trap, port collision, or bug invariant was discovered, record the distilled root cause inside `.agents/context.md` (Section 3). Never dump raw error logs or bug cemeteries (Git tracks commit history).
4. **Domain Satellite Sync:** If web routes or DB schemas were added/modified in a web/DB project, immediately sync `routes.md` or `schema.md`.
5. **ADR Alignment:** If an architectural direction changed, record the decision and trade-offs in `.agents/project-goal.md` Section 4.
6. **Autonomous Memory Push:** When the user mentions "for future", "always", or defines a reusable standard, run `init-context -r/-s <name> -g` followed by `init-context memory push`.

---

## Universal Architectural Principles

### 1. Domain Consolidation & Anti-Fragmentation
DO NOT create fragmented micro-files if a domain file already exists:
- Docker & Containers -> `.agents/skills/docker-ops/SKILL.md`
- Git & Release -> `.agents/skills/git-workflow/SKILL.md`
- Coding Standards -> `.agents/rules/code-standards.md`
- Security Boundaries -> `.agents/rules/security-boundaries.md`

### 2. Strict Idempotency Proof ($f(f(x)) = f(x)$)
All code generation, filesystem operations, and context sync commands must be 100% idempotent. Running them once or 100 times must yield the exact same deterministic state without duplication or side-effects.

### 3. Modular, KISS & DRY
Maintain clean separation of concerns. Prohibit copy-paste duplication, unnecessary abstractions, and monolithic bloat across all project code and context.

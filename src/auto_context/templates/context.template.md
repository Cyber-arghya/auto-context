# Project Cockpit & Macro Context: {{PROJECT_NAME}}

> **Last Updated:** {{DATE_NOW}} | **Stack:** {{STACK}} ({{FRAMEWORK}})  
> **Directory:** `{{PROJECT_DIR}}` | **Model:** Hub & Stack-Adaptive Satellites
>
> 🧭 **Agent Instruction:** Check the **Project Archetype** below first. Only inspect and enforce sections marked relevant for this archetype. Do not hallucinate or scan for non-existent network ports or databases in CLI/Library projects.

---

## Section 0: Project Archetype & Metadata

- **Project Archetype:** `[ Web / Fullstack | Backend API | CLI / Automation | Library / SDK | Desktop / Mobile | Infra / DevOps ]`
- **Primary Runtime / Toolchain:** {{STACK}} ({{FRAMEWORK}})
- **Entry Points:**
  - Main Runtime: `src/` (e.g. `cli.py`, `main.py`, `index.ts`, `lib.rs`, `main.go`)
  - Manifest / Config: `pyproject.toml` (or `package.json`, `Cargo.toml`, `go.mod`)

---

## Section 1: Network & Config Vault (Conditional)

<!-- 
RULE: 
- For Web / API / Microservices: Fill the table below.
- For CLI / Library / Standalone Scripts: Mark table as "N/A" and list configuration flags/paths only.
-->

### Service Endpoints (Web / API / Service Archetype Only)
| Service / Dependency | Host / Base URL | Default Port | Config Key | Health Check / Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **Primary App** | `localhost` | `3000` | `PORT=3000` | `http://localhost:3000/api/health` |
| **Database** | `127.0.0.1` | `5432` | `DATABASE_URL` | PostgreSQL 16 (via Docker) |
| **Cache / Queue** | `127.0.0.1` | `6379` | `REDIS_URL` | Redis 7.x |
<!-- If CLI or Library, replace table above with: "N/A - Standalone execution, no network listeners." -->

### Runtime Configuration & Local Paths
- **Config Storage:** `.env` (derived from `.env.example`) or `~/.config/{{PROJECT_NAME}}/config.json`
- **Key Flags / Envs:**
  - `DEBUG` / `LOG_LEVEL`: Controls verbosity (`info`, `debug`, `trace`).
  - `CACHE_DIR`: Local disk cache or temporary build directory.

---

## Section 2: Operations Runbook (Standardized Commands)

Use only these verified commands for build, test, lint, and run execution.

### 1. Installation & Environment
```bash
# Clean dependency install
<package-manager> install
# Example: npm ci | pnpm install --frozen-lockfile | uv sync | cargo build
```

### 2. Linting & Type Integrity
```bash
# Read-only audit (Must exit code 0)
<lint-command> && <typecheck-command>
# Example: npm run lint && npm run typecheck | ruff check . && mypy . | cargo clippy

# Automatic formatting and safe fixes
<format-command>
# Example: npm run format:fix | ruff format . | cargo fmt
```

### 3. Test Suites & Verification Gate
```bash
# Fast unit tests (in-memory / mock only)
<test-unit-command>
# Example: npm run test:unit | pytest tests/unit -q | cargo test --lib

# Targeted single test run (use during development)
<test-single-command> <path-to-file>
# Example: pnpm test tests/auth.test.ts | pytest tests/unit/test_cli.py -k "test_arg"

# Full regression / integration suite (Mandatory before task completion)
<test-all-command>
# Example: npm run test | pytest | cargo test
```

### 4. Build, Run & Dev
```bash
# Local development execution
<dev-command>
# Example: npm run dev | python -m my_pkg | cargo run

# Production compile / bundle build
<build-command>
# Example: npm run build | uv build | cargo build --release
```

---

## Section 3: Active Architecture Invariants & Traps

Record enduring system rules, operational boundaries, and distilled bug root causes. Never log transient stack traces or historical bug cemeteries.

### Architecture Invariants
1. **Boundary Validation:** Every external input (CLI arguments, HTTP request payloads, env variables) must be validated at the boundary using schema validation (e.g. Zod, Pydantic, Clap) before passing to core logic.
2. **Side-Effect Isolation:** Pure functions for core logic; isolate filesystem mutations, network I/O, or OS calls to dedicated adapter layers.
3. **Strict Idempotency:** Any file-generation, database migration, or state synchronization task must produce identical output if re-run ($f(f(x)) = f(x)$).

### Known Traps & Gotchas
- **Trap:** Cross-Platform File Paths & Permissions
  - **Context:** POSIX vs. Windows path separators or missing executable permissions (`chmod +x`).
  - **Rule:** Always use language-native path modules (`path.join()`, `pathlib.Path`) and never hardcode `/` or `\\`.
- **Trap:** Unhandled Process Exits / Dangling Locks
  - **Context:** Interrupting a script mid-run leaves lock files or temporary files intact.
  - **Rule:** Register clean-up handlers for SIGINT / SIGTERM to unlink temp directories and close connection pools.
- **Trap:** Resource Leak on Async Failure
  - **Context:** Crashing inside an async stream or file reader leaves file descriptors open.
  - **Rule:** Always wrap file and network resource usage in scoped cleanup constructs (`try...finally`, `with` statement, or using disposable patterns).

---

## Section 4: Stack-Adaptive Satellites & Domain Maps (On-Demand)

> 🧭 Satellites reside in [`.agents/context/`](file://{{PROJECT_DIR}}/.agents/context/) and are created/inspected **only when the corresponding domain exists** (Zero Ghost Files):

| Domain | Satellite File | Condition / When Needed |
| :--- | :--- | :--- |
| **Project North Star & ADR** | [`project-goal.md`](file://{{PROJECT_DIR}}/.agents/project-goal.md) | Scope verification, milestone alignment, or architectural decisions |
| **API Endpoints & UI Views** | `routes.md` | Web/API projects only (when creating or modifying endpoints/pages) |
| **Database Schemas & Models** | `schema.md` | Database/ORM projects only (when altering tables or migrations) |

---

## Section 5: Skills & Progressive Disclosure Routing

| Skill | Triggers | Location |
| :--- | :--- | :--- |
| **`docker-ops`** | `docker`, `compose` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/docker-ops/SKILL.md) |
| **`git-workflow`** | `git`, `commit`, `rebase` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/git-workflow/SKILL.md) |
| **`server-diagnostics`** | `health`, `ram`, `port` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/server-diagnostics/SKILL.md) |
| **`feature-verification`** | `test`, `verify`, `check` | [SKILL.md](file://{{PROJECT_DIR}}/.agents/skills/feature-verification/SKILL.md) |

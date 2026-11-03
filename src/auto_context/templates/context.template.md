# Project Cockpit & Macro Context: {{PROJECT_NAME}}

> **Last Updated:** {{DATE_NOW}} | **Stack:** {{STACK}} ({{FRAMEWORK}})  
> **Directory:** `{{PROJECT_DIR}}` | **Model:** Hub & Stack-Adaptive Satellites
>
> 🧭 **Agent Instruction:** On initial interaction or when unpopulated, classify the **Project Archetype** below and populate this cockpit strictly aligned with `.agents/project-goal.md`. Prune any non-applicable sections (e.g. ports for CLI/Library) and enrich with project-specific runtime configuration.

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
RULE FOR AI AGENT:
- For Web / API / Services: Record active host, ports, and healthcheck endpoints below.
- For CLI / Library / Standalone Scripts: Replace the table with: "N/A - Standalone execution (no background network listeners)." and list config paths/flags only.
-->

### Service Endpoints
| Service / Dependency | Host / Base URL | Default Port | Config Key | Health Check / Protocol |
| :--- | :--- | :--- | :--- | :--- |
| **Primary App** | `localhost` | `3000` | `PORT=3000` | `http://localhost:3000/api/health` |

### Runtime Configuration & Local Paths
- **Config Storage:** `.env` (derived from `.env.example`) or `~/.config/{{PROJECT_NAME}}/config.json`
- **Key Flags / Envs:**
  - `DEBUG` / `LOG_LEVEL`: Controls verbosity (`info`, `debug`, `trace`).
  - `CACHE_DIR`: Local disk cache or temporary build directory.

---

## Section 2: Operations Runbook (Standardized Commands)

Use only verified commands for build, test, lint, and run execution.

### 1. Installation & Environment
```bash
<package-manager> install
```

### 2. Linting & Type Integrity
```bash
<lint-command> && <typecheck-command>
```

### 3. Test Suites & Verification Gate
```bash
# Fast unit tests (in-memory / mock only)
<test-unit-command>

# Targeted single test run (use during development)
<test-single-command> <path-to-file>

# Full regression / integration suite (Mandatory before task completion)
<test-all-command>
```

### 4. Build, Run & Dev
```bash
<dev-command>
<build-command>
```

---

## Section 3: Project Architecture Invariants & Traps

> ⚡ **Codebase Constraints:** Non-obvious traps, OS/toolchain quirks, port allocations, or environmental invariants discovered *in this specific project* that cannot be inferred from code alone.
> (Record enduring constraints here as distilled invariants. Do NOT dump transient error stack traces or solved bug diaries).

1. **Verified Executable Runbooks:** Only record 100% executable commands in Section 2 parsed from manifests or verified CLI tools.
2. **Secret Safety:** Never commit plaintext credentials or private tokens into version control.
<!-- Add project-specific invariants below as discovered -->

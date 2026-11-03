# Project Cockpit & Macro Context: {{PROJECT_NAME}}

> **Last Updated:** {{DATE_NOW}} | **Stack:** {{STACK}} ({{FRAMEWORK}})  
> **Directory:** `{{PROJECT_DIR}}` | **Model:** Hub & Stack-Adaptive Satellites
>
> 🧭 **Agent Instruction:** Check the **Project Archetype** below first. Only inspect and enforce sections marked relevant for this archetype. Do not hallucinate or scan for non-existent network ports or databases in CLI/Library projects.

---

## Section 0: Project Archetype & Metadata

- **Project Archetype:** {{ARCHETYPE}}
- **Primary Runtime / Toolchain:** {{STACK}} ({{FRAMEWORK}})
- **Entry Points:**
  - Main Runtime: `src/` (e.g. `cli.py`, `main.py`, `index.ts`, `lib.rs`, `main.go`)
  - Manifest / Config: `pyproject.toml` (or `package.json`, `Cargo.toml`, `go.mod`)

---

{{SECTION_1_CONTENT}}

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

## Section 3: Project Architecture Invariants & Traps

> ⚡ **Codebase Constraints:** Non-obvious traps, OS/toolchain quirks, port allocations, or environmental invariants discovered *in this specific project* that cannot be inferred from code alone.
> (Record enduring constraints here as distilled invariants. Do NOT dump transient error stack traces or solved bug diaries).

1. **Verified Executable Runbooks:** Only record 100% executable commands in Section 2 parsed from manifests or verified CLI tools.
2. **Secret Safety:** Never commit plaintext credentials or private tokens into version control.
<!-- Add project-specific invariants below as they are discovered (e.g. "Windows sandbox requires BypassSandbox for pnpm", "DB timezone must be UTC") -->

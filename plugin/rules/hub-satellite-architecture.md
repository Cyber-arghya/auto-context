---
name: hub-satellite-architecture
description: Enforces the Hub & Satellite modular context pattern, strict idempotency, token budget ceilings, and the Brutal Truth Filter across all projects.
trigger: always_on
---

# Rule: Hub & Satellite Modular Architecture & Idempotency Proof

## Objective
Prevent monolithic context file bloat, eliminate token waste, ensure 100% idempotent execution, and enforce high-value institutional knowledge retention across all coding tasks.

## Guidelines & Constraints

1. **Hub & Satellite Pattern (Strict Token Budget):**
   - Primary `context.md` serves solely as an **Executive Hub** and MUST NOT exceed **80 lines / ~400 tokens**.
   - Detailed domain specifics must be separated into stack-adaptive satellite files inside `.agents/context/` (e.g. `routes.md`, `schema.md`, `gotchas.md`).
   - Satellites are dynamically loaded on-demand via progressive disclosure, preserving conversation context window budgets.

2. **Strict Idempotency Proof ($f(f(x)) = f(x)$):**
   - Running context generation or sync commands 1 time or 100 times must produce the exact same deterministic result without duplicating blocks.
   - Use anchored block delimiters (`<!-- AUTO-CONTEXT:<TAG>:START --> ... <!-- AUTO-CONTEXT:<TAG>:END -->`).
   - Re-running replaces block contents rather than appending.
   - User-written notes, secrets, and manual entries outside anchored zones must remain 100% untouched.
   - Check content hashes before disk writes to avoid unnecessary I/O.

3. **The Brutal Truth Filter (Zero Dead Logs):**
   - If an idea, log entry, or feature fails first-principles scrutiny, drop it immediately and inform the user.
   - Prohibit chronological bug cemeteries (`history.md` dumps of trivial solved bugs).
   - In their place, maintain **`gotchas.md`**: high-impact institutional knowledge, non-obvious architecture traps, port collisions, and edge-case invariants.

4. **KISS & DRY Heuristics:**
   - Prefer language-agnostic filesystem convention heuristics (directories, manifests) over heavy language AST parsers that crash on in-flight syntax errors.
   - All scanners must degrade gracefully with zero unhandled exceptions.


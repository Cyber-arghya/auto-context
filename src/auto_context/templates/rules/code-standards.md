---
name: code-standards
description: Enforces clean code principles, DRY architecture, early return patterns, defensive error handling, and mandatory feature verification.
trigger: always_on
---

# Rule: Code Quality & Architecture Standards

## Objective
Maintain readable, maintainable, modular, and type-safe codebases with clear error handling, idempotency, git cleanliness, and verified feature delivery.

## Guidelines & Constraints
1. **Defensive Coding & Early Return:**
   - Prefer guard clauses and early returns to reduce nested indentation.
   - Always validate inputs and handle edge cases at the beginning of functions.
2. **Clean Code & Self-Documenting Logic:**
   - Keep functions focused on a single responsibility (SRP).
   - Write descriptive variable and function names; avoid cryptic abbreviations.
   - Preserve existing comments and docstrings.
3. **Structured Error Handling:**
   - Never suppress exceptions with empty `catch` or `except` blocks.
   - Log actionable error messages that include relevant context (e.g. invalid inputs, resource identifiers).
4. **Git Hygiene & Semantic Commits:**
   - Write semantic commit messages (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).
   - Never commit temporary files, debug outputs, or untracked state artifacts. Keep working trees clean.
5. **Static Type Annotations & Null Safety:**
   - Enforce explicit type annotations for public functions, parameters, and return types.
   - Prohibit unchecked null / undefined dereferencing.
6. **Named Constants Over Magic Values:**
   - Replace literal strings and magic numbers with descriptive, uppercase module-level constants.
7. **Immutable Data Structures & Strict Idempotency:**
   - Prefer immutable data patterns over shared mutable state.
   - All file-generation, database migration, or state synchronization tasks must produce identical output if re-run ($f(f(x)) = f(x)$).
8. **Anti-Fragmentation & DRY Architecture:**
   - Never create fragmented micro-files when a canonical domain rule or skill already exists. Update existing domain files instead of scattering logic.
9. **Mandatory Feature Verification & Test Reporting:**
   - Every new feature, behavior modification, or bug fix must be verified with executable tests or automated scripts before concluding the turn.
   - Never declare completion based on unverified assumptions; run tests and confirm zero errors (exit code 0).
   - Conclude each feature with a structured Verification Report detailing: (a) Feature scope, (b) Executed test commands, (c) Concrete output/proof, and (d) Edge cases validated.

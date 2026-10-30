---
name: code-standards
description: Enforces clean code principles, DRY architecture, early return patterns, and defensive error handling.
trigger: always_on
---

# Rule: Code Quality & Architecture Standards

## Objective
Maintain readable, maintainable, modular, and type-safe codebases with clear error handling.

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
4. **Conventional Git Commits:**
   - Write semantic commit messages (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`).

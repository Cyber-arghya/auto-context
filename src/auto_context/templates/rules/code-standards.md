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
5. **Static Type Annotations & Null Safety:**
   - Enforce explicit type annotations for public functions, parameters, and return types.
   - Prohibit unchecked null / undefined dereferencing.
6. **Named Constants Over Magic Values:**
   - Replace literal strings and magic numbers with descriptive, uppercase module-level constants.
7. **Immutable Data Structures**

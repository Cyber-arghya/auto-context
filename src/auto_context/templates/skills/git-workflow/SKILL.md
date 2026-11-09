---
name: git-workflow
version: 1.1.0
description: Conventional commit standards, branch management, safe rebasing, pre-commit quality gates, and merge conflict resolution.
triggers: ["git", "commit", "branch", "pr", "pull-request", "merge", "conflict", "rebase", "hook", "pre-commit"]
---

# Skill: Git Workflow & Release Management

## Overview
Standard procedures for feature branching, atomic conventional commits, pre-commit quality gates, interactive rebasing, merge conflict resolution, and safe remote synchronization.

## When to Activate
- When staging, committing, or pushing code changes to remote repositories.
- When creating pull requests, managing feature branches, or tagging releases.
- When resolving git merge or rebase conflicts.

## Workflows & Procedures

### 1. Conventional Commit Specification
Always format commit messages using structured semantic prefixes:
* `feat:` A new user-facing feature or CLI command.
* `fix:` A bug fix or error correction.
* `docs:` Documentation changes only (e.g. `README.md`, `context.md`).
* `refactor:` Code restructuring that neither fixes a bug nor adds a feature.
* `chore:` Build process, tooling, or dependency updates.
* `test:` Adding or updating automated tests.

**Format:**
```
<type>(<optional scope>): <short summary in imperative mood>

[optional body explaining motivation and technical approach]

[optional footer(s), e.g. Closes #123]
```

### 2. Branching & PR Hygiene
* Keep `main` / `master` production-ready and protected.
* Create short-lived feature branches: `git checkout -b feat/feature-name`
* Before opening a PR or pushing:
  ```bash
  git fetch origin
  git rebase origin/main
  ```

### 3. Safe Merge Conflict Resolution Runbook
1. **Identify conflicted files:** `git status` (look for `both modified:`)
2. **Inspect conflicts:** Look for conflict markers `<<<<<<< HEAD`, `=======`, `>>>>>>>`
3. **Decide resolution strategy:**
   - If keeping current branch's changes: `git checkout --ours <file>`
   - If adopting incoming commit's changes: `git checkout --theirs <file>`
   - If merging manually: edit file to remove conflict markers and test.
4. **Complete rebase:**
   ```bash
   git add <resolved-files>
   GIT_EDITOR=true git rebase --continue
   ```
5. **Never force-push without lease:** Use `git push --force-with-lease` instead of raw `--force`.

### 4. Automated Release Tagging Protocol
Upon completion of a major architectural update, new feature, or breaking change, once verified stable and confirmed by user:
1. **Manifest & Version Bump:** Increment semantic version in `pyproject.toml` (and package entrypoints like `main.py`).
2. **Docs Alignment:** Update release badges, URLs, and installation snippets in `README.md`.
3. **Release Commit:** Commit with message: `chore(release): bump version to vX.Y.Z with <summary>`.
4. **Annotated Tag:** Create tag: `git tag -a vX.Y.Z -m "Release vX.Y.Z: <summary>"`.
5. **Remote Push:** Push both main and tag: `git push origin main && git push origin vX.Y.Z`.
6. **Dual-Sync Pipeline:** Execute `init-context memory push` to update Central Memory & private repo.

### 5. Zero-Footprint Git Protection & Autonomous Central Memory Sync Protocol
`auto-context` operates strictly as a local development helper without leaving git footprint in client or application repositories.

1. **Zero-Footprint Ignore Enforcement:**
   - The following artifacts must NEVER be tracked or committed to user application repositories:
     ```gitignore
     .agents/
     .gemini/
     context.md
     context.local.md
     *.local.md
     AGENTS.md
     AGENTS.md.bak
     GEMINI.md
     GEMINI.md.bak
     .auto-context/
     auto-context/
     ```
   - Automatically ensured machine-wide in `~/.gitignore_global` and project `.gitignore`.

2. **Autonomous Central Memory Sync Invariant:**
   - Whenever any new rule/skill is codified, or existing domain files are modified:
     - Follow Domain Consolidation (all guidelines for the same domain reside in that domain's single consolidated file, validated against `registry.json`).
     - The AI assistant **MUST autonomously run `init-context memory push`** immediately upon concluding the task.
     - The user must **NEVER** be required to manually run push commands.

### 6. Pre-Commit Quality Gate & Git Hook Protocol

To prevent broken code, unformatted files, or failing CI/CD pipelines from reaching remote branches, all repositories must enforce a deterministic pre-commit verification chain.

#### 1. Mandatory Local Quality Gate Chain
Before committing or creating a pull request, run the complete verification chain:
```bash
# 1. Static analysis & linting (fast failure)
uv run ruff check src/ tests/

# 2. Static type checking
uv run mypy src/ --ignore-missing-imports

# 3. Unit & integration test suite
uv run python tests/run_tests.py
```
To automatically fix formatting or safe linter issues:
```bash
uv run ruff check --fix src/ tests/
```

#### 2. Git Hooks Architecture & Remote Isolation Invariant
* **Why `.git/hooks/` is NEVER pushed to GitHub:**
  By core Git architecture and security design, Git strictly excludes the `.git/` metadata directory from commits and remote tracking. This is a fundamental security barrier preventing cloned repositories from automatically executing untrusted scripts on a developer's host machine.
* **Local Hook Installation:**
  To automate verification on every `git commit`, configure `.git/hooks/pre-commit`:
  ```bash
  #!/bin/sh
  set -e

  echo "🔍 Running Ruff linter..."
  uv run ruff check src/ tests/

  echo "🔎 Running Mypy type checker..."
  uv run mypy src/ --ignore-missing-imports

  echo "🧪 Running Test Suite..."
  uv run python tests/run_tests.py

  echo "✅ All pre-commit quality checks passed!"
  ```
  Ensure the hook has executable permissions (`chmod +x .git/hooks/pre-commit` on Unix/macOS or created directly on Windows).
* **Cross-Team Hook Versioning (`core.hooksPath`):**
  When hooks must be version-controlled in GitHub across team members:
  1. Store repository hooks in a versioned folder (e.g., `.agents/hooks/` or `.githooks/`).
  2. Configure git to read hooks from that folder:
     ```bash
     git config core.hooksPath .agents/hooks
     # or
     git config core.hooksPath .githooks
     ```
* **Emergency Bypass:**
  In verified emergency rollbacks or documentation-only quick commits where verification is inapplicable, bypass the hook using:
  ```bash
  git commit -m "docs: emergency hotfix" --no-verify
  ```


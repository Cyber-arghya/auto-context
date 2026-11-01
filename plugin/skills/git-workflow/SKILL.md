---
name: git-workflow
version: 1.0.0
description: Conventional commit standards, branch management, safe rebasing, and merge conflict resolution.
triggers: ["git", "commit", "branch", "pr", "pull-request", "merge", "conflict", "rebase"]
---

# Skill: Git Workflow & Release Management

## Overview
Standard procedures for feature branching, atomic conventional commits, interactive rebasing, merge conflict resolution, and safe remote synchronization.

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

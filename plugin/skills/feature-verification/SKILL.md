---
name: feature-verification
version: 1.0.0
description: Standard operational procedure for verifying new features, executing automated test suites, and generating verifiable completion reports.
triggers: ["verify", "test-feature", "verification", "report", "qa", "feature-test"]
---

# Skill: Feature Verification & Test Reporting

## Overview
Protocol for executing rigorous verification cycles before concluding any feature development, refactoring, or bug fix. Ensures zero unverified claims and standardizes the Verification Report format.

## When to Activate
- Immediately after writing, modifying, or refactoring feature code.
- Prior to declaring any coding task complete or committing changes.
- When validating bug fixes to prove regression elimination.

## Workflows & Procedures

### 1. Test Selection & Execution Matrix
1. **Existing Test Suite:** Check project test manifests (`pytest`, `npm test`, `cargo test`, `go test`). Run existing tests to ensure no regressions.
2. **Feature-Specific Verification:** Write or execute an isolated test case, CLI verification command, or scratch test script covering the new feature's core path and edge cases.
3. **Capture Exit Codes & Output:** Never rely on exit code suppression; verify exit code is explicitly 0 and output matches expected behavior.

### 2. Mandatory Verification Report Format
Conclude every feature implementation turn with a structured report using this format:

```markdown
### 📋 Feature Verification Report

#### 1. Scope of Implementation
- **Feature / Fix:** <Short description of what was built or fixed>
- **Impacted Files:** <Links to modified source files>

#### 2. Executed Test Commands & Output
- **Command:** `<command executed>`
- **Exit Code:** `0 (Success)`
- **Summary Output:**
  ```text
  <paste actual output / test summary>
  ```

#### 3. Edge Cases & Boundary Conditions Validated
- [x] Input validation / defensive guards
- [x] Null / undefined / empty input handling
- [x] Regression check against existing test suite
```

#!/usr/bin/env bash
# Auto-Context Lifecycle Hook: validate.sh
# Deterministic verification gate (secrets, lint, tests).
# Stack: {{STACK}} ({{FRAMEWORK}})
set -euo pipefail

echo "🛡️  [validate.sh] Running validation gate for {{PROJECT_NAME}}..."

# Step 1: Secret Safety Audit
echo "  [1/3] Auditing codebase for secrets..."
if command -v init-context >/dev/null 2>&1; then
    init-context audit .
fi

# Step 2: Static Analysis & Linter
echo "  [2/3] Checking code quality and types..."
if command -v ruff >/dev/null 2>&1; then
    ruff check .
elif [ -f "package.json" ] && grep -q '"lint"' package.json; then
    npm run lint
elif [ -f "Cargo.toml" ] && command -v cargo >/dev/null 2>&1; then
    cargo check
fi

# Step 3: Automated Test Execution
echo "  [3/3] Executing automated tests..."
if [ -f "tests/run_tests.py" ]; then
    python tests/run_tests.py
elif command -v pytest >/dev/null 2>&1 && [ -d "tests" ]; then
    pytest
elif [ -f "package.json" ] && grep -q '"test"' package.json; then
    npm test
elif [ -f "Cargo.toml" ] && command -v cargo >/dev/null 2>&1; then
    cargo test
elif [ -f "go.mod" ] && command -v go >/dev/null 2>&1; then
    go test ./...
fi

echo "✅ [validate.sh] Validation gate passed (Exit code: 0)!"
exit 0

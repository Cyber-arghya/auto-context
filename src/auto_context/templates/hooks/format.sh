#!/usr/bin/env bash
# Auto-Context Lifecycle Hook: format.sh
# Formats project codebase deterministically.
# Stack: {{STACK}} ({{FRAMEWORK}})
set -euo pipefail

echo "🎨 [format.sh] Formatting codebase for {{PROJECT_NAME}}..."

# 1. Python formatting (ruff / black)
if command -v ruff >/dev/null 2>&1; then
    echo "  -> Running ruff format..."
    ruff format .
elif command -v black >/dev/null 2>&1; then
    echo "  -> Running black..."
    black .
fi

# 2. JavaScript / TypeScript formatting (prettier / npm)
if [ -f "package.json" ]; then
    if command -v prettier >/dev/null 2>&1; then
        echo "  -> Running prettier..."
        prettier --write --ignore-unknown .
    elif grep -q '"format"' package.json; then
        echo "  -> Running npm run format..."
        npm run format
    fi
fi

# 3. Rust formatting
if [ -f "Cargo.toml" ] && command -v cargo >/dev/null 2>&1; then
    echo "  -> Running cargo fmt..."
    cargo fmt
fi

# 4. Go formatting
if [ -f "go.mod" ] && command -v gofmt >/dev/null 2>&1; then
    echo "  -> Running gofmt..."
    gofmt -w .
fi

echo "✨ [format.sh] Code formatting completed successfully!"
exit 0

<#
.SYNOPSIS
Auto-Context Lifecycle Hook: validate.ps1
Deterministic verification gate (secrets, lint, tests) for Windows.
Stack: {{STACK}} ({{FRAMEWORK}})
#>
$ErrorActionPreference = "Stop"

Write-Host "🛡️  [validate.ps1] Running validation gate for {{PROJECT_NAME}}..." -ForegroundColor Cyan

# Step 1: Secret Safety Audit
Write-Host "  [1/3] Auditing codebase for secrets..." -ForegroundColor Gray
if (Get-Command init-context -ErrorAction SilentlyContinue) {
    & init-context audit .
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Secret audit violation detected. Aborting."
        exit 1
    }
}

# Step 2: Static Analysis & Linter
Write-Host "  [2/3] Checking code quality and types..." -ForegroundColor Gray
if (Get-Command ruff -ErrorAction SilentlyContinue) {
    & ruff check .
    if ($LASTEXITCODE -ne 0) { exit 1 }
} elseif (Test-Path "package.json") {
    $pkg = Get-Content "package.json" -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($pkg.scripts.lint) {
        & npm run lint
        if ($LASTEXITCODE -ne 0) { exit 1 }
    }
} elseif ((Test-Path "Cargo.toml") -and (Get-Command cargo -ErrorAction SilentlyContinue)) {
    & cargo check
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

# Step 3: Automated Test Execution
Write-Host "  [3/3] Executing automated tests..." -ForegroundColor Gray
if (Test-Path "tests\run_tests.py") {
    & python tests\run_tests.py
    if ($LASTEXITCODE -ne 0) { exit 1 }
} elseif ((Get-Command pytest -ErrorAction SilentlyContinue) -and (Test-Path "tests")) {
    & pytest
    if ($LASTEXITCODE -ne 0) { exit 1 }
} elseif (Test-Path "package.json") {
    $pkg = Get-Content "package.json" -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($pkg.scripts.test) {
        & npm test
        if ($LASTEXITCODE -ne 0) { exit 1 }
    }
} elseif ((Test-Path "Cargo.toml") -and (Get-Command cargo -ErrorAction SilentlyContinue)) {
    & cargo test
    if ($LASTEXITCODE -ne 0) { exit 1 }
} elseif ((Test-Path "go.mod") -and (Get-Command go -ErrorAction SilentlyContinue)) {
    & go test ./...
    if ($LASTEXITCODE -ne 0) { exit 1 }
}

Write-Host "✅ [validate.ps1] Validation gate passed (Exit code: 0)!" -ForegroundColor Green
exit 0

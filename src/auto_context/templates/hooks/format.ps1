<#
.SYNOPSIS
Auto-Context Lifecycle Hook: format.ps1
Formats project codebase deterministically on Windows.
Stack: {{STACK}} ({{FRAMEWORK}})
#>
$ErrorActionPreference = "Stop"

Write-Host "🎨 [format.ps1] Formatting codebase for {{PROJECT_NAME}}..." -ForegroundColor Cyan

# 1. Python formatting
if (Get-Command ruff -ErrorAction SilentlyContinue) {
    Write-Host "  -> Running ruff format..." -ForegroundColor Gray
    & ruff format .
} elseif (Get-Command black -ErrorAction SilentlyContinue) {
    Write-Host "  -> Running black..." -ForegroundColor Gray
    & black .
}

# 2. JavaScript / TypeScript formatting
if (Test-Path "package.json") {
    if (Get-Command prettier -ErrorAction SilentlyContinue) {
        Write-Host "  -> Running prettier..." -ForegroundColor Gray
        & prettier --write --ignore-unknown .
    } else {
        $pkg = Get-Content "package.json" -Raw | ConvertFrom-Json -ErrorAction SilentlyContinue
        if ($pkg.scripts.format) {
            Write-Host "  -> Running npm run format..." -ForegroundColor Gray
            & npm run format
        }
    }
}

# 3. Rust formatting
if ((Test-Path "Cargo.toml") -and (Get-Command cargo -ErrorAction SilentlyContinue)) {
    Write-Host "  -> Running cargo fmt..." -ForegroundColor Gray
    & cargo fmt
}

# 4. Go formatting
if ((Test-Path "go.mod") -and (Get-Command gofmt -ErrorAction SilentlyContinue)) {
    Write-Host "  -> Running gofmt..." -ForegroundColor Gray
    & gofmt -w .
}

Write-Host "✨ [format.ps1] Code formatting completed successfully!" -ForegroundColor Green
exit 0

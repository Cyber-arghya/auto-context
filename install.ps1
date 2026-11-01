# ==============================================================================
# Script: install.ps1
# Repository: https://github.com/Cyber-arghya/auto-context
# Author: Arghya Biswas (@Cyber-arghya)
# Description: 1-Click installer for Windows PowerShell and pwsh
# Usage: irm https://raw.githubusercontent.com/Cyber-arghya/auto-context/main/install.ps1 | iex
# ==============================================================================
[CmdletBinding()]
param()

$RepoRaw = "https://raw.githubusercontent.com/Cyber-arghya/auto-context/main"
$PackageName = "auto-context-cli"
$Version = "1.0.3"

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "⚡ Auto-Context: 1-Click Installer (Windows)" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Determine Local vs Remote
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path -ErrorAction SilentlyContinue
$IsLocal = $ScriptDir -and (Test-Path (Join-Path $ScriptDir "pyproject.toml"))

# 2. Check / Install uv package runner
if (-not (Get-Command "uv" -ErrorAction SilentlyContinue)) {
    Write-Host "  [*] Astral uv not found. Installing uv package manager..." -ForegroundColor Yellow
    try {
        irm https://astral.sh/uv/install.ps1 | iex
        $env:Path = "$HOME\.local\bin;$HOME\.cargo\bin;$HOME\AppData\Roaming\uv\bin;$env:Path"
    } catch {
        Write-Host "  [!] Could not auto-install uv. Trying pipx / python fallback..." -ForegroundColor Yellow
    }
}

# 3. Install auto-context CLI
$Installed = $false
if (Get-Command "uv" -ErrorAction SilentlyContinue) {
    Write-Host "  [*] Installing auto-context via uv tool..." -ForegroundColor Cyan
    if ($IsLocal) {
        uv tool install $ScriptDir --force
    } else {
        uv tool install $PackageName --force
    }
    if ($LASTEXITCODE -eq 0) { $Installed = $true }
}

if (-not $Installed -and (Get-Command "pipx" -ErrorAction SilentlyContinue)) {
    Write-Host "  [*] Installing auto-context via pipx..." -ForegroundColor Cyan
    if ($IsLocal) {
        pipx install $ScriptDir --force
    } else {
        pipx install $PackageName --force
    }
    if ($LASTEXITCODE -eq 0) { $Installed = $true }
}

if (-not $Installed -and (Get-Command "python" -ErrorAction SilentlyContinue)) {
    Write-Host "  [*] Installing auto-context via pip..." -ForegroundColor Cyan
    if ($IsLocal) {
        python -m pip install $ScriptDir --quiet
    } else {
        python -m pip install $PackageName --quiet
    }
    if ($LASTEXITCODE -eq 0) { $Installed = $true }
}

if (-not $Installed) {
    Write-Host "`n[✗] Installation failed. Run manually via pip or uv:" -ForegroundColor Red
    Write-Host "    pip install $PackageName" -ForegroundColor Yellow
    exit 1
}

Write-Host "  [✓] CLI 'init-context' installed successfully!" -ForegroundColor Green

# 4. Install Global Antigravity / Gemini Plugin
$WinPluginDir = Join-Path $HOME ".gemini\config\plugins\auto-context"
$WinRulesDir = Join-Path $WinPluginDir "rules"
$WinSkillsDir = Join-Path $WinPluginDir "skills\auto-context"

New-Item -ItemType Directory -Path $WinRulesDir -Force | Out-Null
New-Item -ItemType Directory -Path $WinSkillsDir -Force | Out-Null

if ($IsLocal -and (Test-Path (Join-Path $ScriptDir "plugin"))) {
    Copy-Item -Path (Join-Path $ScriptDir "plugin\*") -Destination $WinPluginDir -Recurse -Force
} else {
    try {
        Invoke-RestMethod -Uri "$RepoRaw/plugin/plugin.json" -OutFile (Join-Path $WinPluginDir "plugin.json") -ErrorAction SilentlyContinue
        Invoke-RestMethod -Uri "$RepoRaw/plugin/rules/AGENTS.md" -OutFile (Join-Path $WinRulesDir "AGENTS.md") -ErrorAction SilentlyContinue
        Invoke-RestMethod -Uri "$RepoRaw/plugin/skills/auto-context/SKILL.md" -OutFile (Join-Path $WinSkillsDir "SKILL.md") -ErrorAction SilentlyContinue
    } catch {}
}
Write-Host "  [✓] Configured Global AI Agent Plugin in: $WinPluginDir" -ForegroundColor Green

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "🎉 Installation Complete!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "To initialize autonomous context tracking in any project, run:"
Write-Host "  cd C:\path\to\your-project" -ForegroundColor Yellow
Write-Host "  init-context" -ForegroundColor Green
Write-Host ""

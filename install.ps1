# ==============================================================================
# Script: install.ps1
# Repository: https://github.com/Cyber-arghya/auto-context
# Author: Arghya Biswas (@Cyber-arghya)
# Description: 1-Line installer for Windows PowerShell and pwsh
# Usage: irm https://raw.githubusercontent.com/Cyber-arghya/auto-context/main/install.ps1 | iex
# ==============================================================================
[CmdletBinding()]
param()

$RepoRaw = "https://raw.githubusercontent.com/Cyber-arghya/auto-context/main"
$Version = "1.0.0"

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "⚡ Auto-Context: 1-Click Installer (Windows PowerShell / pwsh)" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Target Directory
$InstallDir = Join-Path $HOME ".local\bin"
if (-not (Test-Path $InstallDir)) {
    New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
}

$Ps1Target = Join-Path $InstallDir "init-context.ps1"
$CmdTarget = Join-Path $InstallDir "init-context.cmd"

# 2. Local vs Remote download
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path -ErrorAction SilentlyContinue
if ($ScriptDir -and (Test-Path (Join-Path $ScriptDir "bin\init-context.ps1"))) {
    Write-Host "  [*] Installing from local repository files..." -ForegroundColor Yellow
    Copy-Item (Join-Path $ScriptDir "bin\init-context.ps1") $Ps1Target -Force
    Copy-Item (Join-Path $ScriptDir "bin\init-context.cmd") $CmdTarget -Force
    $PluginSource = Join-Path $ScriptDir "plugin"
} else {
    Write-Host "  [*] Downloading latest init-context CLI from GitHub..." -ForegroundColor Yellow
    Invoke-RestMethod -Uri "$RepoRaw/bin/init-context.ps1" -OutFile $Ps1Target
    Invoke-RestMethod -Uri "$RepoRaw/bin/init-context.cmd" -OutFile $CmdTarget
    $PluginSource = $null
}

Write-Host "  [✓] CLI scripts installed in: $InstallDir" -ForegroundColor Green

# 3. Add to User PATH
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($UserPath -notlike "*$InstallDir*") {
    $NewUserPath = "$UserPath;$InstallDir"
    [Environment]::SetEnvironmentVariable("Path", $NewUserPath, "User")
    Write-Host "  [✓] Added $InstallDir to User PATH." -ForegroundColor Green
}
$env:Path = "$env:Path;$InstallDir"

# 4. Configure PowerShell Profile Function
if ($PROFILE) {
    $ProfileDir = Split-Path -Parent $PROFILE
    if (-not (Test-Path $ProfileDir)) {
        New-Item -ItemType Directory -Path $ProfileDir -Force | Out-Null
    }
    if (-not (Test-Path $PROFILE)) {
        New-Item -ItemType File -Path $PROFILE -Force | Out-Null
    }
    $ProfileContent = Get-Content -Path $PROFILE -Raw -ErrorAction SilentlyContinue
    $FunctionBlock = @"

# Auto-Context CLI wrapper
function init-context {
    & "$Ps1Target" @args
}
"@
    if ($ProfileContent -notmatch "function init-context") {
        Add-Content -Path $PROFILE -Value $FunctionBlock
        Write-Host "  [✓] Registered 'init-context' in PowerShell profile: $PROFILE" -ForegroundColor Green
    }
}

# 5. Global Antigravity Plugin Setup (Windows)
$WinPluginDir = Join-Path $HOME ".gemini\config\plugins\auto-context"
$WinRulesDir = Join-Path $WinPluginDir "rules"
$WinSkillsDir = Join-Path $WinPluginDir "skills\auto-context"

New-Item -ItemType Directory -Path $WinRulesDir -Force | Out-Null
New-Item -ItemType Directory -Path $WinSkillsDir -Force | Out-Null

if ($PluginSource -and (Test-Path $PluginSource)) {
    Copy-Item -Path "$PluginSource\*" -Destination $WinPluginDir -Recurse -Force
} else {
    try {
        Invoke-RestMethod -Uri "$RepoRaw/plugin/plugin.json" -OutFile (Join-Path $WinPluginDir "plugin.json") -ErrorAction SilentlyContinue
        Invoke-RestMethod -Uri "$RepoRaw/plugin/rules/AGENTS.md" -OutFile (Join-Path $WinRulesDir "AGENTS.md") -ErrorAction SilentlyContinue
        Invoke-RestMethod -Uri "$RepoRaw/plugin/skills/auto-context/SKILL.md" -OutFile (Join-Path $WinSkillsDir "SKILL.md") -ErrorAction SilentlyContinue
    } catch {
        # Optional network ignore
    }
}
Write-Host "  [✓] Installed Global AI Agent Plugin in: $WinPluginDir" -ForegroundColor Green

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "🎉 Installation Complete!" -ForegroundColor Green
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "To initialize autonomous context tracking in any project, simply run:"
Write-Host "  cd C:\path\to\your-project" -ForegroundColor Yellow
Write-Host "  init-context" -ForegroundColor Green
Write-Host ""

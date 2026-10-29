# ==============================================================================
# Script: uninstall.ps1
# Repository: https://github.com/Cyber-arghya/auto-context
# Author: Arghya Biswas (@Cyber-arghya)
# ==============================================================================
[CmdletBinding()]
param()

Write-Host ">>> Uninstalling Auto-Context..." -ForegroundColor Yellow

$InstallDir = Join-Path $HOME ".local\bin"
Remove-Item (Join-Path $InstallDir "init-context.ps1") -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $InstallDir "init-context.cmd") -Force -ErrorAction SilentlyContinue
Write-Host "  [✓] Removed CLI scripts from $InstallDir" -ForegroundColor Green

$WinPluginDir = Join-Path $HOME ".gemini\config\plugins\auto-context"
Remove-Item $WinPluginDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  [✓] Removed global plugin directory" -ForegroundColor Green

Write-Host "Auto-Context uninstalled successfully." -ForegroundColor Green


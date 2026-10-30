# ==============================================================================
# Script: uninstall.ps1
# Repository: https://github.com/Cyber-arghya/auto-context
# Author: Arghya Biswas (@Cyber-arghya)
# ==============================================================================
[CmdletBinding()]
param()

Write-Host ">>> Uninstalling Auto-Context..." -ForegroundColor Yellow

if (Get-Command "uv" -ErrorAction SilentlyContinue) {
    uv tool uninstall auto-context 2>$null
}
if (Get-Command "pipx" -ErrorAction SilentlyContinue) {
    pipx uninstall auto-context 2>$null
}

$WinPluginDir = Join-Path $HOME ".gemini\config\plugins\auto-context"
Remove-Item $WinPluginDir -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  [✓] Removed global plugin directory" -ForegroundColor Green

Write-Host "Auto-Context uninstalled successfully." -ForegroundColor Green

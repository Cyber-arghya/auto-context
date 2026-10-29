@echo off
setlocal
echo =====================================================================
echo   Auto-Context Offline Windows Installer
echo =====================================================================
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
echo.
pause


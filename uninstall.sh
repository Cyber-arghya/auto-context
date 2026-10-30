#!/usr/bin/env bash
# ==============================================================================
# Script: uninstall.sh
# Repository: https://github.com/Cyber-arghya/auto-context
# Author: Arghya Biswas (@Cyber-arghya)
# ==============================================================================
set -euo pipefail

echo ">>> Uninstalling Auto-Context..."

if command -v uv &>/dev/null; then
    uv tool uninstall auto-context 2>/dev/null || true
fi
if command -v pipx &>/dev/null; then
    pipx uninstall auto-context 2>/dev/null || true
fi

PLUGIN_DIR="$HOME/.gemini/config/plugins/auto-context"
rm -rf "$PLUGIN_DIR"
echo "  [✓] Removed global plugin directory"

echo "Auto-Context uninstalled successfully."

#!/usr/bin/env bash
# ==============================================================================
# Script: uninstall.sh
# Repository: https://github.com/Cyber-arghya/auto-context
# Author: Arghya Biswas (@Cyber-arghya)
# ==============================================================================
set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "\n${YELLOW}>>> Uninstalling Auto-Context...${NC}"

# Remove binary
rm -f "$HOME/.local/bin/init-context" "/usr/local/bin/init-context" 2>/dev/null || true
echo -e "  ${GREEN}[✓] Removed CLI binary.${NC}"

# Remove plugin
rm -rf "$HOME/.gemini/config/plugins/auto-context" 2>/dev/null || true
echo -e "  ${GREEN}[✓] Removed global plugin directory.${NC}"

echo -e "\n${GREEN}Auto-Context uninstalled successfully.${NC}\n"


#!/usr/bin/env bash
# ==============================================================================
# Script: install.sh
# Repository: https://github.com/Cyber-arghya/auto-context
# Author: Arghya Biswas (@Cyber-arghya)
# Description: 1-Line installer for Linux, WSL2, and macOS
# Usage: curl -sSL https://raw.githubusercontent.com/Cyber-arghya/auto-context/main/install.sh | bash
# ==============================================================================
set -euo pipefail

REPO_RAW="https://raw.githubusercontent.com/Cyber-arghya/auto-context/main"
VERSION="1.0.0"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "\n${CYAN}=====================================================================${NC}"
echo -e "${BOLD}${GREEN}⚡ Auto-Context: 1-Click Installer (Linux / WSL2 / macOS)${NC}"
echo -e "${CYAN}=====================================================================${NC}\n"

# 1. Determine install location
if [ "$EUID" -eq 0 ]; then
    INSTALL_DIR="/usr/local/bin"
else
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
fi

CLI_BIN="$INSTALL_DIR/init-context"

# 2. Check if running from cloned repository or remote
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "")"
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/bin/init-context" ]; then
    echo -e "  ${YELLOW}[*] Installing from local repository files...${NC}"
    cp -f "$SCRIPT_DIR/bin/init-context" "$CLI_BIN"
    PLUGIN_SOURCE="$SCRIPT_DIR/plugin"
else
    echo -e "  ${YELLOW}[*] Downloading latest init-context CLI from GitHub...${NC}"
    curl -sSL "$REPO_RAW/bin/init-context" -o "$CLI_BIN"
    PLUGIN_SOURCE=""
fi

chmod +x "$CLI_BIN"
echo -e "  ${GREEN}[✓] CLI installed successfully at:${NC} $CLI_BIN"

# 3. Ensure PATH is configured
SHELL_RC=""
case "${SHELL:-/bin/bash}" in
    */zsh)  SHELL_RC="$HOME/.zshrc" ;;
    */bash) SHELL_RC="$HOME/.bashrc" ;;
    *)      SHELL_RC="$HOME/.profile" ;;
esac

if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    if [ -f "$SHELL_RC" ] && ! grep -q "$INSTALL_DIR" "$SHELL_RC"; then
        echo -e "\n# Added by auto-context installer" >> "$SHELL_RC"
        echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$SHELL_RC"
        echo -e "  ${GREEN}[✓] Added $INSTALL_DIR to PATH in:${NC} $SHELL_RC"
    fi
fi

# 4. Install Global Antigravity / Gemini Plugin
PLUGIN_DIR="$HOME/.gemini/config/plugins/auto-context"
mkdir -p "$PLUGIN_DIR/rules" "$PLUGIN_DIR/skills/auto-context"

if [ -n "$PLUGIN_SOURCE" ] && [ -d "$PLUGIN_SOURCE" ]; then
    cp -rf "$PLUGIN_SOURCE"/* "$PLUGIN_DIR/" 2>/dev/null || true
else
    curl -sSL "$REPO_RAW/plugin/plugin.json" -o "$PLUGIN_DIR/plugin.json" 2>/dev/null || true
    curl -sSL "$REPO_RAW/plugin/rules/AGENTS.md" -o "$PLUGIN_DIR/rules/AGENTS.md" 2>/dev/null || true
    curl -sSL "$REPO_RAW/plugin/skills/auto-context/SKILL.md" -o "$PLUGIN_DIR/skills/auto-context/SKILL.md" 2>/dev/null || true
fi
echo -e "  ${GREEN}[✓] Installed Global AI Agent Plugin in:${NC} $PLUGIN_DIR"

echo -e "\n${CYAN}=====================================================================${NC}"
echo -e "${BOLD}${GREEN}🎉 Installation Complete!${NC}"
echo -e "${CYAN}=====================================================================${NC}"
echo -e "To initialize autonomous context tracking in any project, simply run:"
echo -e "  ${YELLOW}cd /path/to/any/project${NC}"
echo -e "  ${GREEN}init-context${NC}\n"

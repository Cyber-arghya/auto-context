#!/usr/bin/env bash
# ==============================================================================
# Script: install.sh
# Repository: https://github.com/Cyber-arghya/auto-context
# Author: Arghya Biswas (@Cyber-arghya)
# Description: 1-Click installer for Linux, WSL2, and macOS
# Usage: curl -sSL https://raw.githubusercontent.com/Cyber-arghya/auto-context/main/install.sh | bash
# ==============================================================================
set -euo pipefail

REPO_RAW="https://raw.githubusercontent.com/Cyber-arghya/auto-context/main"
PACKAGE_NAME="auto-context-cli"
VERSION="1.0.1"

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "\n${CYAN}=====================================================================${NC}"
echo -e "${BOLD}${GREEN}⚡ Auto-Context: 1-Click Installer (Linux / WSL2 / macOS)${NC}"
echo -e "${CYAN}=====================================================================${NC}\n"

# 1. Determine Local vs Remote
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || echo "")"
IS_LOCAL=false
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/pyproject.toml" ]; then
    IS_LOCAL=true
fi

# 2. Check / Install uv package manager
if ! command -v uv &>/dev/null; then
    echo -e "  ${YELLOW}[*] Astral uv not found. Installing uv package manager...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh || true
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

# 3. Install auto-context CLI
INSTALLED=false
if command -v uv &>/dev/null; then
    echo -e "  ${CYAN}[*] Installing auto-context via uv tool...${NC}"
    if [ "$IS_LOCAL" = true ]; then
        uv tool install "$SCRIPT_DIR" --force
    else
        uv tool install "$PACKAGE_NAME" --force
    fi
    INSTALLED=true
elif command -v pipx &>/dev/null; then
    echo -e "  ${CYAN}[*] Installing auto-context via pipx...${NC}"
    if [ "$IS_LOCAL" = true ]; then
        pipx install "$SCRIPT_DIR" --force
    else
        pipx install "$PACKAGE_NAME" --force
    fi
    INSTALLED=true
elif command -v python3 &>/dev/null; then
    echo -e "  ${CYAN}[*] Installing auto-context via pip...${NC}"
    if [ "$IS_LOCAL" = true ]; then
        python3 -m pip install "$SCRIPT_DIR" --quiet
    else
        python3 -m pip install "$PACKAGE_NAME" --quiet
    fi
    INSTALLED=true
fi

if [ "$INSTALLED" = false ]; then
    echo -e "\n${RED}[✗] Installation failed. Run manually via pip or uv:${NC}"
    echo -e "    ${YELLOW}pip install $PACKAGE_NAME${NC}"
    exit 1
fi

echo -e "  ${GREEN}[✓] CLI 'init-context' installed successfully!${NC}"

# 4. Install Global Antigravity / Gemini Plugin
PLUGIN_DIR="$HOME/.gemini/config/plugins/auto-context"
mkdir -p "$PLUGIN_DIR/rules" "$PLUGIN_DIR/skills/auto-context"

if [ "$IS_LOCAL" = true ] && [ -d "$SCRIPT_DIR/plugin" ]; then
    cp -rf "$SCRIPT_DIR/plugin"/* "$PLUGIN_DIR/" 2>/dev/null || true
else
    curl -sSL "$REPO_RAW/plugin/plugin.json" -o "$PLUGIN_DIR/plugin.json" 2>/dev/null || true
    curl -sSL "$REPO_RAW/plugin/rules/AGENTS.md" -o "$PLUGIN_DIR/rules/AGENTS.md" 2>/dev/null || true
    curl -sSL "$REPO_RAW/plugin/skills/auto-context/SKILL.md" -o "$PLUGIN_DIR/skills/auto-context/SKILL.md" 2>/dev/null || true
fi
echo -e "  ${GREEN}[✓] Configured Global AI Agent Plugin in:${NC} $PLUGIN_DIR"

# 5. Ensure PATH contains ~/.local/bin
SHELL_RC=""
case "${SHELL:-/bin/bash}" in
    */zsh)  SHELL_RC="$HOME/.zshrc" ;;
    */bash) SHELL_RC="$HOME/.bashrc" ;;
    *)      SHELL_RC="$HOME/.profile" ;;
esac

INSTALL_DIR="$HOME/.local/bin"
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]] && [ -f "$SHELL_RC" ]; then
    if ! grep -q "$INSTALL_DIR" "$SHELL_RC"; then
        echo -e "\n# Added by auto-context installer" >> "$SHELL_RC"
        echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$SHELL_RC"
        echo -e "  ${GREEN}[✓] Added $INSTALL_DIR to PATH in:${NC} $SHELL_RC"
    fi
fi

echo -e "\n${CYAN}=====================================================================${NC}"
echo -e "${BOLD}${GREEN}🎉 Installation Complete!${NC}"
echo -e "${CYAN}=====================================================================${NC}"
echo -e "To initialize autonomous context tracking in any project, run:"
echo -e "  ${YELLOW}cd /path/to/any/project${NC}"
echo -e "  ${GREEN}init-context${NC}\n"

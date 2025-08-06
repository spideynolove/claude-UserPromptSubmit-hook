#!/bin/bash

# Install script for claude-UserPromptSubmit-hook with BMad integration
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR=$(pwd)
CLAUDE_DIR="$PROJECT_DIR/.claude"

echo "Claude Code UserPromptSubmit Hook Installer"
echo "==========================================="

# Create .claude directory structure
mkdir -p "$CLAUDE_DIR/hooks/UserPromptSubmit"
mkdir -p "$CLAUDE_DIR/commands"

# Function to copy hook files
copy_hooks() {
    echo "Copying hook files..."
    cp "$SCRIPT_DIR/hooks/UserPromptSubmit/ultimate-prompt-hook.py" "$CLAUDE_DIR/hooks/UserPromptSubmit/"
    cp "$SCRIPT_DIR/hooks/UserPromptSubmit/ultimate-prompt-hook-enhanced.py" "$CLAUDE_DIR/hooks/UserPromptSubmit/"
    chmod +x "$CLAUDE_DIR/hooks/UserPromptSubmit/"*.py
}

# Function to install settings
install_settings() {
    local version=$1
    if [ "$version" = "enhanced" ]; then
        cp "$SCRIPT_DIR/settings-enhanced.json" "$CLAUDE_DIR/settings.json"
        echo "Installed enhanced settings (includes BMad integration)"
    else
        cp "$SCRIPT_DIR/settings.json" "$CLAUDE_DIR/settings.json" 
        echo "Installed standard settings"
    fi
}

# Function to setup BMad Method
setup_bmad() {
    echo "Setting up BMad Method integration..."
    
    # Install BMad Method if not present
    if [ ! -d "bmad-core" ]; then
        echo "Installing BMad Method..."
        npx bmad-method install
    else
        echo "BMad Method already installed"
    fi

    # Install Ultrathink command
    if [ ! -f "$CLAUDE_DIR/commands/ultrathink.md" ]; then
        echo "Installing Ultrathink command..."
        curl -s -o "$CLAUDE_DIR/commands/ultrathink.md" https://claudecodecommands.directory/api/download/ultrathink
    else
        echo "Ultrathink command already installed"
    fi

    # Setup MCP servers
    echo "Setting up MCP servers..."
    
    # Check if claude command exists
    if command -v claude &> /dev/null; then
        # Add Serena
        if ! claude mcp list | grep -q "serena"; then
            claude mcp add serena -- uvx --from git+https://github.com/oraios/serena \
                serena start-mcp-server --context ide-assistant --project "$PROJECT_DIR"
        fi
        
        # Add Context7
        if ! claude mcp list | grep -q "context7"; then
            claude mcp add --transport http context7 https://mcp.context7.com/mcp
        fi
        
        echo "MCP servers configured"
    else
        echo "Claude Code not found - MCP servers need to be configured manually"
        echo "Run these commands after installing Claude Code:"
        echo "  claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server --context ide-assistant --project \$(pwd)"
        echo "  claude mcp add --transport http context7 https://mcp.context7.com/mcp"
    fi
}

# Interactive installation
echo ""
echo "Choose installation type:"
echo "1) Standard - Original hook functionality"
echo "2) Enhanced - Includes BMad Method integration and anti-wrapper rules"
echo "3) BMad Full Setup - Enhanced version + BMad Method + MCP servers"

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        copy_hooks
        install_settings "standard"
        echo ""
        echo "✅ Standard installation complete!"
        echo ""
        echo "Available flags: -u, -p, -e, -test, -review, -hh (show all)"
        echo "Start with: 'Show me available flags -hh'"
        ;;
    2)
        copy_hooks
        install_settings "enhanced"
        echo ""
        echo "✅ Enhanced installation complete!"
        echo ""
        echo "Enhanced features:"
        echo "  - Anti-wrapper rule enforcement"
        echo "  - BMad context detection (-bmad flag)"
        echo "  - Enhanced engineering standards"
        echo ""
        echo "Available flags: -u, -p, -e, -bmad, -bmad-story, -hh (show all)"
        echo "Start with: 'Show me available flags -hh'"
        ;;
    3)
        copy_hooks
        install_settings "enhanced"
        setup_bmad
        echo ""
        echo "✅ Full BMad setup complete!"
        echo ""
        echo "Installed:"
        echo "  ✓ Enhanced hook with BMad integration"
        echo "  ✓ BMad Method framework"
        echo "  ✓ Ultrathink command"
        echo "  ✓ MCP servers (Serena, Context7)"
        echo ""
        echo "BMad agents: @analyst, @architect, @dev, @pm, @po, @qa, @sm, @ux-expert"
        echo "Hook flags: -u, -p, -e, -bmad, -bmad-story, -bmad-review, -hh"
        echo ""
        echo "Start with: 'Begin BMad workflow for new project -bmad -u -p'"
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "Hook installed to: $CLAUDE_DIR/hooks/UserPromptSubmit/"
echo "Settings: $CLAUDE_DIR/settings.json"
echo ""
echo "Test with: 'Hello -hh' to see all available flags"
# Enhanced Version Features

## What's New in Enhanced Version

The enhanced version includes all original functionality plus:

### 🎯 BMad Method Integration
- **BMad context detection**: Automatically detects BMad Method installation
- **BMad-specific flags**: `-bmad`, `-bmad-story`, `-bmad-review`
- **Technical preferences loading**: Reads from `bmad-core/data/technical-preferences.md`
- **Project structure awareness**: Detects stories, architecture docs, PRD

### 🛡️ Anti-Wrapper Rule Enforcement
Critical development rule automatically enforced:
```
Don't write or generate any wrapper or replacement code for existing third-party packages.
Use the official API of the specified package directly, as documented.
```

### 📋 Enhanced Flags

#### BMad Method Flags
- `-bmad` - Load BMad Method context and patterns
- `-bmad-story` - BMad story implementation mode with acceptance criteria focus
- `-bmad-review` - BMad QA review mode with systematic checklist

#### Enhanced Standard Flags
- `-e`, `-eng`, `-standards` - Now includes anti-wrapper rule enforcement
- `-ng`, `-no_guess` - Enhanced with anti-wrapper rule reminder

## Installation Options

### Quick Install
```bash
git clone https://github.com/spideynolove/claude-UserPromptSubmit-hook
cd claude-UserPromptSubmit-hook
chmod +x install.sh

# Install in current directory
./install.sh

# Or install in specific project directory
./install.sh /path/to/your/project
```

### Manual Setup
1. **Standard Version**: Use `settings.json` + `ultimate-prompt-hook.py`
2. **Enhanced Version**: Use `settings-enhanced.json` + `ultimate-prompt-hook-enhanced.py`

### BMad Method Integration
Choose option 3 in installer for full setup including:
- BMad Method framework (`npx bmad-method install`)
- Ultrathink command
- MCP servers (Serena, Context7)

## Usage Examples

### BMad Workflow
```bash
# Start new BMad project
"Begin BMad greenfield workflow -bmad -u -p"

# Implement BMad story
"Implement story 1.2 with full testing -bmad-story -test"

# Review BMad implementation
"Review current story implementation -bmad-review -u"
```

### Anti-Wrapper Enforcement
The enhanced version automatically reminds AI to:
- Use official APIs directly
- Avoid creating wrapper abstractions
- Preserve existing architecture patterns
- Ask for clarification when uncertain

## File Structure
```
├── hooks/UserPromptSubmit/
│   ├── ultimate-prompt-hook.py          # Original version
│   └── ultimate-prompt-hook-enhanced.py # Enhanced with BMad integration
├── settings.json                        # Standard configuration
├── settings-enhanced.json               # Enhanced configuration
└── install.sh                          # Interactive installer
```

## Compatibility
- **Original hook**: Fully preserved, all existing functionality works
- **Enhanced version**: Extends original with BMad integration
- **Fallback support**: Enhanced version works even without BMad Method installed
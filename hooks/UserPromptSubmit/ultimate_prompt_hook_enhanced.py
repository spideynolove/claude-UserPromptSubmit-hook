#!/usr/bin/env python3
"""
Ultimate UserPromptSubmit Hook for Claude Code - Enhanced Version
Based on veteranbv/claude-UserPromptSubmit-hook with BMad Method integration

Enhanced features:
- BMad Method context detection and integration
- Anti-wrapper rule enforcement
- Additional BMad-specific flags
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

# Import base functionality from original hook
# This allows using the original hook as a base while adding enhancements
try:
    import importlib.util
    import sys
    
    # Try to load the original hook module
    hook_path = Path(__file__).parent / "ultimate-prompt-hook.py"
    if hook_path.exists():
        spec = importlib.util.spec_from_file_location("ultimate_prompt_hook", hook_path)
        ultimate_prompt_hook = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ultimate_prompt_hook)
        
        # Import classes and functions
        BaseFlagHandlers = ultimate_prompt_hook.FlagHandlers
        ContextInjectors = ultimate_prompt_hook.ContextInjectors
        PromptEnhancer = ultimate_prompt_hook.PromptEnhancer
        parse_flags = ultimate_prompt_hook.parse_flags
        should_apply_defaults = ultimate_prompt_hook.should_apply_defaults
        write_log = ultimate_prompt_hook.write_log
        ENABLE_LOGGING = ultimate_prompt_hook.ENABLE_LOGGING
        LOG_DIR = ultimate_prompt_hook.LOG_DIR
        ENGINEER_NAME = ultimate_prompt_hook.ENGINEER_NAME
        
        USE_BASE_HANDLERS = True
    else:
        raise ImportError("Original hook file not found")
        
except (ImportError, AttributeError):
    # Fallback if original hook is not available
    USE_BASE_HANDLERS = False
    # Use configurations from original
    ENABLE_LOGGING = True
    LOG_DIR = Path.home() / ".claude" / "logs"
    ENGINEER_NAME = os.environ.get("USER", "Engineer")

# Enhanced configurations
ANTI_WRAPPER_RULE = """

CRITICAL DEVELOPMENT RULE:
Don't write or generate any wrapper or replacement code for existing third-party packages.

Use the official API of the specified package directly, as documented.

A successful solution must:
• Solve only the exact problem specified
• Use the provided third-party package without modification or abstraction
• Require minimal integration effort with the existing system
• Preserve existing architecture and patterns
• Include concise explanations of the API calls used and why

Don't write or change any code until you're at least 95% confident in what needs to be done. If anything is unclear, ask for more information.
"""

# Enhanced Flag Handlers (extends base handlers)
class EnhancedFlagHandlers:
    """Enhanced flag handlers with BMad integration"""
    
    @staticmethod
    def engineering_standards() -> str:
        """Enhanced engineering standards with anti-wrapper rule"""
        base_standards = """
Follow the project's principal engineering standards. No shortcuts, stubs, or hardcoded values. We build it right the first time: clean, robust, and production ready. No halfway measures.

Keep it tight. Use the simplest solution that meets the need with high quality. Do not overengineer. Do not create new files, layers, or abstractions unless they are clearly necessary. Every line of code should earn its place. Simplicity is earned through understanding, not guesswork.

Make it clean. Make it count.

If you encounter uncertainty, lack context, or are not confident in the solution, stop. Do not guess or make things up. It is not only okay, it is expected, to ask for clarification or help. Excellence includes knowing when to pause.
"""
        return base_standards + ANTI_WRAPPER_RULE

    @staticmethod
    def no_guess() -> str:
        """Enhanced no guess mode with anti-wrapper rule"""
        return f"\n\nDo not guess or make assumptions. If something is unclear or you lack necessary context, stop and ask for clarification. It's better to ask than to implement incorrectly.{ANTI_WRAPPER_RULE}"

    @staticmethod
    def bmad() -> str:
        """BMad Method specific context"""
        bmad_context = ""
        
        # Check if BMad is installed
        if Path("bmad-core").exists():
            bmad_context += "\n\n[BMad Method Active]"
            
            # Load technical preferences if available
            tech_prefs = Path("bmad-core/data/technical-preferences.md")
            if tech_prefs.exists():
                bmad_context += "\nReference technical preferences from bmad-core/data/technical-preferences.md"
            
            # Check current stories
            stories_dir = Path("docs/stories")
            if stories_dir.exists():
                stories = list(stories_dir.glob("*.md"))
                if stories:
                    bmad_context += f"\nActive stories available in docs/stories/ ({len(stories)} stories)"
            
            # Check for architecture docs
            arch_docs = Path("docs/architecture")
            if arch_docs.exists():
                bmad_context += "\nArchitecture documentation available in docs/architecture/"
            
            # Check for PRD
            prd_file = Path("docs/prd.md")
            if prd_file.exists():
                bmad_context += "\nPRD available in docs/prd.md"
            
            bmad_context += "\nApply BMad workflow patterns and engineering standards."
        else:
            bmad_context += "\n\n[BMad Method Not Detected - Install with: npx bmad-method install]"
        
        return bmad_context

    @staticmethod
    def bmad_story() -> str:
        """BMad story implementation context"""
        return "\n\nBMad Story Mode: Reference story file for context and acceptance criteria. Implement with tests and update story with implementation notes. Use engineering standards and verify against existing codebase patterns."

    @staticmethod
    def bmad_review() -> str:
        """BMad review mode"""
        return "\n\nBMad Review Mode: Apply BMad QA checklist. Review against acceptance criteria, check architectural alignment, suggest improvements. Use systematic review approach."

    @staticmethod
    def help() -> str:
        """Enhanced help with BMad flags"""
        base_help = """
The user has just asked for help understanding the UserPromptSubmit hooks. Please display the following help message:
Here are all available UserPromptSubmit hook flags:

🧠 THINKING MODES
- -u, -ultrathink    Maximum thinking budget (31,999 tokens) for complex problems
- -th, -think_hard   Enhanced thinking for challenging tasks
- -t, -think         Step-by-step thinking for standard problems

🏗️ QUALITY & STANDARDS
- -e, -eng, -standards    Apply engineering standards (no shortcuts, production-ready)
- -clean                  Follow clean code principles (SOLID, DRY, meaningful names)

💻 DEVELOPMENT MODES
- -p, -plan          Create detailed plan before implementation
- -v, -verbose       Include verbose explanations and detailed comments
- -s, -sec, -security    Focus on security best practices
- -test              Include comprehensive unit tests
- -doc               Provide detailed documentation with examples
- -perf              Optimize for performance with benchmarks
- -review            Critical code review mode
- -refactor          Refactor for clarity and maintainability
- -debug             Systematic debugging approach
- -api               API design best practices

🔧 OTHER OPTIONS
- -ng, -no_guess     Never guess; ask for clarification instead
- -ctx, -context     Include project context (package managers, tools)
- -hh, -hhelp        Show this help message

🎯 BMAD METHOD FLAGS (Enhanced Version)
- -bmad              BMad Method context and patterns
- -bmad-story        BMad story implementation mode
- -bmad-review       BMad review and QA mode

💡 COMMON COMBINATIONS
Complex problem:     -u -p        (ultrathink + plan)
Production feature:  -e -test -doc (standards + tests + docs)
Code review:        -review -u    (review + deep thinking)
BMad workflow:      -bmad -u -p   (BMad context + ultrathink + plan)
BMad story impl:    -bmad-story -e -test (BMad story + standards + tests)

Note: Engineering standards include anti-wrapper rule enforcement. BMad flags only available in enhanced version."""
        
        return base_help

def get_enhanced_flag_handler(flag: str) -> Optional[Callable[[], str]]:
    """Get enhanced flag handler, fallback to base handlers"""
    enhanced_mapping = {
        # Enhanced versions
        "e": EnhancedFlagHandlers.engineering_standards,
        "eng": EnhancedFlagHandlers.engineering_standards,
        "standards": EnhancedFlagHandlers.engineering_standards,
        "no_guess": EnhancedFlagHandlers.no_guess,
        "ng": EnhancedFlagHandlers.no_guess,
        # BMad specific
        "bmad": EnhancedFlagHandlers.bmad,
        "bmad_story": EnhancedFlagHandlers.bmad_story,
        "bmad_review": EnhancedFlagHandlers.bmad_review,
        # Enhanced help
        "hh": EnhancedFlagHandlers.help,
        "hhelp": EnhancedFlagHandlers.help,
    }
    
    # Check enhanced handlers first
    if flag.lower() in enhanced_mapping:
        return enhanced_mapping[flag.lower()]
    
    # Fall back to base handlers if available
    if USE_BASE_HANDLERS:
        base_mapping = {
            "u": BaseFlagHandlers.ultrathink,
            "ultrathink": BaseFlagHandlers.ultrathink,
            "th": BaseFlagHandlers.think_hard,
            "think_hard": BaseFlagHandlers.think_hard,
            "t": BaseFlagHandlers.think,
            "think": BaseFlagHandlers.think,
            "clean": BaseFlagHandlers.clean,
            "p": BaseFlagHandlers.plan,
            "plan": BaseFlagHandlers.plan,
            "v": BaseFlagHandlers.verbose,
            "verbose": BaseFlagHandlers.verbose,
            "s": BaseFlagHandlers.security,
            "sec": BaseFlagHandlers.security,
            "security": BaseFlagHandlers.security,
            "test": BaseFlagHandlers.test,
            "doc": BaseFlagHandlers.doc,
            "perf": BaseFlagHandlers.perf,
            "review": BaseFlagHandlers.review,
            "refactor": BaseFlagHandlers.refactor,
            "debug": BaseFlagHandlers.debug,
            "api": BaseFlagHandlers.api,
            "ctx": BaseFlagHandlers.context,
            "context": BaseFlagHandlers.context,
        }
        return base_mapping.get(flag.lower())
    
    return None

# Fallback implementations if base handlers not available
if not USE_BASE_HANDLERS:
    class PromptEnhancer:
        def __init__(self) -> None:
            self.contexts: List[str] = []
            self.log_data: Dict[str, Any] = {
                "timestamp": datetime.now().isoformat(),
                "formatted_date": datetime.now().strftime("%B {}, %Y").format(datetime.now().day),
            }

        def add_context(self, context: str) -> None:
            if context and context.strip():
                self.contexts.append(context.strip())

        def log_event(self, key: str, value: Any) -> None:
            self.log_data[key] = value

    def parse_flags(prompt: str) -> Tuple[str, List[str]]:
        flags_pattern = r"((?:^|\s+)-[a-zA-Z_]+)+$"
        match = re.search(flags_pattern, prompt)
        if match:
            flags_str = match.group(0)
            clean_prompt = prompt[: match.start()].rstrip()
            flags = re.findall(r"-([a-zA-Z_]+)", flags_str)
            return clean_prompt, flags
        return prompt, []

    def should_apply_defaults(prompt: str, flags: List[str]) -> bool:
        skip_patterns = [
            r"^(ls|dir|pwd|cd|cat|grep|find|which|what|where|who|when|how much|how many)\b",
            r"^(show|list|display|get|fetch)\s+(me\s+)?(the\s+)?",
            r"^\?", r"^(hi|hello|hey|thanks|thank you|bye)",
        ]
        prompt_lower = prompt.lower()
        for pattern in skip_patterns:
            if re.match(pattern, prompt_lower):
                return False
        return True

    def write_log(enhancer: PromptEnhancer) -> None:
        if not ENABLE_LOGGING:
            return
        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            log_file = LOG_DIR / "prompt_hooks.jsonl"
            with open(log_file, "a") as f:
                json.dump(enhancer.log_data, f)
                f.write("\n")
        except (IOError, OSError, PermissionError):
            pass

def main() -> None:
    try:
        input_data = json.load(sys.stdin)
        prompt: str = input_data.get("prompt", "")
        session_id: str = input_data.get("session_id", "unknown")

        enhancer = PromptEnhancer()
        enhancer.log_event("original_prompt", prompt)
        enhancer.log_event("session_id", session_id)
        enhancer.log_event("hook_version", "enhanced")

        clean_prompt, flags = parse_flags(prompt)
        enhancer.log_event("flags", flags)
        enhancer.log_event("clean_prompt", clean_prompt)

        if clean_prompt.strip() == "" and ("hh" in flags or "hhelp" in flags):
            clean_prompt = "Show available hook flags"
            enhancer.log_event("help_request", True)

        # Add current date context
        current_date = f"\n[Current Date: {datetime.now().strftime('%B %d, %Y')}]"
        enhancer.add_context(current_date)

        # Add git branch if available
        try:
            branch = subprocess.check_output(
                ["git", "branch", "--show-current"], stderr=subprocess.DEVNULL
            ).decode().strip()
            if branch:
                enhancer.add_context(f"\n[Git Branch: {branch}]")
        except (subprocess.CalledProcessError, FileNotFoundError, OSError):
            pass

        # Apply default engineering standards
        if "hh" not in flags and "hhelp" not in flags:
            if (should_apply_defaults(clean_prompt, flags) 
                and "e" not in flags and "eng" not in flags):
                enhancer.add_context(EnhancedFlagHandlers.engineering_standards())
                enhancer.log_event("auto_applied_enhanced_standards", True)

        # Process explicit flags
        applied_flags: List[str] = []
        for flag in flags:
            handler = get_enhanced_flag_handler(flag)
            if handler:
                enhancer.add_context(handler())
                applied_flags.append(flag)

        enhancer.log_event("applied_flags", applied_flags)

        # Output combined context
        if enhancer.contexts:
            output: str = "\n".join(enhancer.contexts)
            print(output)
            enhancer.log_event("injected_context", output)

        write_log(enhancer)
        sys.exit(0)

    except Exception as e:
        print(f"[Enhanced Hook Error: {str(e)}]", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
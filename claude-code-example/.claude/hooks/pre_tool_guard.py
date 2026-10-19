"""PreToolUse hook: runs BEFORE Claude's tool call and can block it.

Exam concept: a CLAUDE.md rule like "never touch .env" is guidance Claude usually follows.
A hook is code that runs every time, so it ENFORCES the rule deterministically.

Claude Code sends the pending call as JSON on stdin, e.g.
  {"tool_name": "Bash", "tool_input": {"command": "cat .env"}, ...}
Printing a "deny" decision blocks the call, and the reason is shown to Claude so it can adjust.
"""
import json
import re
import sys

BLOCKED_COMMANDS = [
    (r"\brm\s+-[a-z]*r[a-z]*f|\brm\s+-[a-z]*f[a-z]*r", "recursive force-delete (rm -rf) is not allowed"),
    (r"git\s+push\s+.*(--force|-f\b)", "force-push is not allowed"),
]
SECRET_FILE = re.compile(r"(?<![\w.])\.env\b|credentials", re.IGNORECASE)
REAL_LOOKING_KEY = re.compile(r"\bAKIA(?![A-Z0-9]{9}EXAMPLE\b)[A-Z0-9]{16}\b")


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main() -> None:
    event = json.load(sys.stdin)
    tool = event.get("tool_name", "")
    tool_input = event.get("tool_input", {})

    if tool == "Bash":
        command = tool_input.get("command", "")
        for pattern, reason in BLOCKED_COMMANDS:
            if re.search(pattern, command):
                deny(f"Blocked by project hook: {reason}.")
        if SECRET_FILE.search(command):
            deny("Blocked by project hook: commands may not read or touch secret files (.env, credentials).")

    if tool in ("Read", "Edit", "Write"):
        if SECRET_FILE.search(tool_input.get("file_path", "")):
            deny("Blocked by project hook: secret files (.env, credentials) are off limits.")

    if tool in ("Edit", "Write"):
        new_text = tool_input.get("content", "") + tool_input.get("new_string", "")
        if REAL_LOOKING_KEY.search(new_text):
            deny("Blocked by project hook: that looks like a real AWS access key. "
                 "Use the documented example key AKIAIOSFODNN7EXAMPLE instead.")

    sys.exit(0)  # no output + exit 0 = allow the call to go ahead normally


if __name__ == "__main__":
    main()

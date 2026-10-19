"""PostToolUse hook: runs AFTER Claude edits a file.

Exam concept: post-tool hooks give Claude automatic feedback. Here, every time a Python file
is edited the test suite runs. If it fails, a "block" decision sends the failure output back
to Claude, which then fixes the code before moving on. Every edit is also written to an
audit log, something a prompt alone can never guarantee.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path(__file__).resolve().parents[2]))
AUDIT_LOG = PROJECT_DIR / ".claude" / "hooks" / "audit.log"


def main() -> None:
    event = json.load(sys.stdin)
    file_path = event.get("tool_input", {}).get("file_path", "")

    with AUDIT_LOG.open("a") as log:
        log.write(f"{datetime.now(timezone.utc).isoformat()} {event.get('tool_name')} {file_path}\n")

    if not file_path.endswith(".py"):
        sys.exit(0)

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "-q"],
        cwd=PROJECT_DIR, capture_output=True, text=True, timeout=60,
    )
    if result.returncode != 0:
        print(json.dumps({
            "decision": "block",
            "reason": f"Tests failed after editing {file_path}. Fix them before continuing:\n"
                      + result.stderr[-2000:],
        }))
    sys.exit(0)


if __name__ == "__main__":
    main()

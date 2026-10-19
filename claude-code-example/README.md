# Claude Code example: memory, prompts, skills, tools and hooks

A small Claude Code project for practicing the **Claude Certified Architect: Foundations** concepts.
The code is a tiny AWS ARN helper library (`arn_utils.py`), the same topic as `../dataset.json`.
Everything around it is Claude Code configuration, and each file is commented with the exam concept it shows.

## Try it

```bash
cd claude-code-example
pip install -r requirements.txt     # only needed for the MCP tool
claude                              # accept the "trust this folder" prompt the first time
```

| Type this in Claude Code | What it shows |
|---|---|
| `/memory` | CLAUDE.md, the imported `docs/arn-format.md`, and the path-scoped rule got loaded |
| `how do I run the tests?` | Claude answers from **memory** without searching |
| `/add-function return the account ID from an ARN` | **Custom prompt** (slash command) with `$ARGUMENTS` |
| `inventory the ARNs in docs/arn-format.md` | **Skill** triggers from its description and runs its script |
| `what region is arn:aws:sqs:eu-west-2:123456789012:q in?` | **MCP tool** `lookup_arn` gets called |
| `lookup_arn on "nope"` | Structured tool error (`errorCategory`, `isRetryable`) |
| `run cat .env` | **PreToolUse hook** blocks it |
| `add a test that uses the key AKIA1234567890ABCDEF` | **PreToolUse hook** blocks a real-looking key |
| `make extract_region return "" for global ARNs` | **PostToolUse hook** runs the tests and sends the failure back to Claude |
| `/hooks` | Lists the hooks Claude Code loaded |

## What each piece is

```
claude-code-example/
├── CLAUDE.md                     MEMORY: project conventions, loaded every session
├── docs/arn-format.md            MEMORY: pulled in by "@docs/arn-format.md" in CLAUDE.md
├── .claude/
│   ├── rules/tests.md            MEMORY: path-scoped, loads only for test_*.py
│   ├── commands/add-function.md  PROMPT: reusable slash command /add-function
│   ├── skills/arn-report/
│   │   ├── SKILL.md              SKILL: name + description always in context, body on demand
│   │   └── scripts/scan.py       SKILL: deterministic script the skill runs
│   ├── hooks/
│   │   ├── pre_tool_guard.py     PRE-TOOL HOOK: deny rm -rf, force-push, .env, real AWS keys
│   │   └── post_tool_check.py    POST-TOOL HOOK: run tests after edits, audit log
│   └── settings.json             wires up the hooks, permissions and MCP server approval
├── .mcp.json                     TOOL: registers the MCP server with Claude Code
├── mcp_server/server.py          TOOL: lookup_arn and check_access_key_id
├── arn_utils.py                  the code Claude works on
└── test_arn_utils.py             its tests
```

### 1. Memory (`CLAUDE.md`)
Instructions Claude should always follow go in memory, not in every prompt.
- **Hierarchy:** `~/.claude/CLAUDE.md` (you, everywhere), `./CLAUDE.md` (team, checked in), `CLAUDE.local.md` (you, this project).
- **`@path` imports** keep CLAUDE.md short and split context into files.
- **`.claude/rules/*.md` with `paths:`** loads a rule only when matching files are touched, so it costs no context the rest of the time.

### 2. Prompt (`.claude/commands/add-function.md`)
A checked-in prompt template the whole team runs as `/add-function ...`.
It uses the prompt-engineering habits from the course: XML tags (`<task>`, `<steps>`, `<output_format>`),
explicit numbered steps, and a required output format. `allowed-tools` limits what it can do.

### 3. Skill (`.claude/skills/arn-report/`)
A skill is a folder of instructions + scripts that Claude loads **only when needed** (progressive disclosure).
- The `description` decides when it triggers, so it states *what* it does and *when* to use it.
- The script does the exact work (no re-deriving regexes each time); `SKILL.md` fixes the output format.
- Prompt vs skill: a slash command runs when **you** type it; a skill runs when **Claude** decides the request matches.

### 4. Tool (`mcp_server/server.py` + `.mcp.json`)
A custom tool exposed over MCP. Claude sees it as `mcp__arn-tools__lookup_arn`.
- The **docstring is the tool description**: what it does, what it returns, and when to use something else instead.
- **Structured errors** (`isError`, `errorCategory`, `isRetryable`) let Claude tell "fix the input" apart from "retry later".
- `.mcp.json` is the project-scoped, checked-in config; `~/.claude.json` holds personal servers.

### 5. Hooks (`.claude/settings.json` + `.claude/hooks/`)
Hooks are **your code**, run by Claude Code on every matching tool call. That makes them deterministic,
unlike a CLAUDE.md rule, which Claude follows *most* of the time.

| | PreToolUse | PostToolUse |
|---|---|---|
| Runs | before the tool | after the tool succeeds |
| Can | **block** the call (`permissionDecision: "deny"`) | **give feedback** (`decision: "block"` + `reason`); the tool already ran |
| Here | blocks `rm -rf`, force-push, `.env`, real-looking AWS keys | runs the tests after any `.py` edit, writes `audit.log` |
| `matcher` | `Bash\|Read\|Edit\|Write` | `Edit\|Write` |

Both scripts read the tool call as JSON on stdin (`tool_name`, `tool_input`, and `tool_response` for post).
Test one by hand:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"cat .env"}}' | python3 .claude/hooks/pre_tool_guard.py
```

**Rule of thumb for the exam:** if something *must* happen every time (security, compliance, formatting, tests),
use a hook. If it is guidance or style, use memory or a prompt.

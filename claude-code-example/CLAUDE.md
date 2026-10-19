# Project memory: AWS ARN helpers

<!--
  MEMORY (exam concept): CLAUDE.md is loaded into context automatically at the start of
  every session launched in this folder. Hierarchy, most general to most specific:
    ~/.claude/CLAUDE.md   user memory      (just you, every project)
    ./CLAUDE.md           project memory   (checked in, shared with the team)  <- this file
    ./CLAUDE.local.md     local memory     (just you, this project, git-ignored)
    .claude/rules/*.md    modular rules, optionally scoped to file paths with `paths:`
  Put conventions here, not in every prompt. Type `/memory` in Claude Code to see what loaded.
-->

## What this project is
A tiny Python library (`arn_utils.py`) for parsing AWS ARNs and validating access key IDs.

## Commands
- Run tests: `python3 -m unittest -v`
- No third-party packages in `arn_utils.py`; the standard library only.

## Conventions
- Every public function has a one-line docstring and a unit test in `test_arn_utils.py`.
- Invalid input raises `ValueError` with the bad value in the message; never return `False` for "bad ARN".
- Never put a real AWS key in code. In tests use AWS's documented example key `AKIAIOSFODNN7EXAMPLE`.

## Extra context (imported with @, loaded only because it is referenced here)
@docs/arn-format.md

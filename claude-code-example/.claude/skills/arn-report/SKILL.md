---
name: arn-report
description: Finds every AWS ARN and access key ID in a file or pasted text and produces a report of their services, regions and accounts, flagging anything that looks like a real credential. Use when the user asks to audit, summarize or inventory ARNs or AWS keys, or pastes a block of config, IAM policy or logs containing ARNs.
allowed-tools: Read, Bash(python3 .claude/skills/arn-report/scripts/scan.py:*)
---
<!--
  SKILL (exam concept): only the `name` + `description` above sit in context all the time.
  Claude reads the body below only when a request matches the description (progressive
  disclosure), and runs the bundled script instead of re-deriving the logic each time.
  The description says WHAT it does and WHEN to use it; that is what triggers it.
-->
# ARN report

## Steps
1. Get the input. If it is a file, pass its path. If it is pasted text, save it to a temp file first.
2. Run the scanner (it prints JSON, do not parse ARNs yourself):
   `python3 .claude/skills/arn-report/scripts/scan.py <path>`
3. Write the report in exactly this format:

```
## ARN report for <source>
**N ARNs, M access key IDs**

| ARN | Service | Region | Account |
|-----|---------|--------|---------|

### Credentials
- <key> - EXAMPLE key (safe) | POSSIBLE REAL KEY - rotate it and remove from the file
```

## Rules
- A key ending in `EXAMPLE` is AWS's documentation key: mark it safe.
- Any other `AKIA...` key: mark it as a possible real key and show only its first 8 characters.
- Write `global` in the Region column when the region is empty.

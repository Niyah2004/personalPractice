---
description: Add a new helper to arn_utils.py with a docstring and tests
argument-hint: <what the function should do>
allowed-tools: Read, Edit, Bash(python3 -m unittest:*)
---
<!--
  CUSTOM PROMPT / SLASH COMMAND (exam concept): a reusable, checked-in prompt template.
  Run it as:  /add-function return the account ID from an ARN
  $ARGUMENTS is replaced with whatever you type after the command.
  `allowed-tools` limits what Claude may use without asking while running this prompt.
-->
<task>
Add a function to `arn_utils.py` that does the following: $ARGUMENTS
</task>

<steps>
1. Read `arn_utils.py` and reuse `parse_arn` instead of writing a new regex.
2. Add the function with a one-line docstring, following the conventions in CLAUDE.md.
3. Add a `<Function>Test` class to `test_arn_utils.py` with one valid and one invalid case.
4. Run `python3 -m unittest -v` and fix anything that fails.
</steps>

<output_format>
Finish with: the function signature, the test names you added, and the final test result line.
</output_format>

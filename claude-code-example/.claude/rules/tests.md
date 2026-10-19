---
paths:
  - "test_*.py"
---
<!--
  PATH-SCOPED MEMORY (exam concept): this rule only loads when Claude works on files
  matching `paths`, so it costs no context the rest of the time.
-->
# Test-file rules
- Use `unittest` (not pytest) so the suite runs with no installs.
- One `TestCase` class per function under test, named `<Function>Test`.
- Cover at least one valid input and one invalid input per function.

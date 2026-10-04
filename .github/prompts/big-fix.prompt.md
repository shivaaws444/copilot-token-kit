---
description: Fix a serious/complex bug - repro test first, root cause, full fix
agent: build
---
Use the major-bug-fix skill (and debug-failure for investigation).
Bug: ${input:bug:symptom, where (prod/test/local), frequency, impact}
Evidence: ${input:evidence:trimmed trace via ctx.py, logs, failing input, recent changes}
Start with a failing reproduction test. Do not change production code until it fails for the right reason.
If this will take more than one chat, create docs/work/bug-<slug>.md first.

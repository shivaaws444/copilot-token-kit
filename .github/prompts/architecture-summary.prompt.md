---
description: One-time - write docs/ARCHITECTURE.md from the repo map
agent: plan
---
Use the repo-map skill. Read docs/repo-map.md. Open source files only to clarify business purpose of a flow (max ~10 files).
Write docs/ARCHITECTURE.md (<= 150 lines) with:
- Purpose of the service in 3 lines
- Modules and their responsibility
- Main business flows (group related endpoints), each as 3-6 steps
- Data: key entities/tables and who writes them
- Integrations: outbound HTTP, messaging, AWS services, auth (ADFS/OAuth) as seen in code
- Cross-cutting: error handling, retries, transactions, security config
- Known gaps / things the map could not determine
This file is reused as context for later chats, so be dense and factual. No code blocks except one Mermaid flowchart.

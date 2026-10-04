---
description: Explain the end-to-end flow of one endpoint or listener
agent: build
---
Use the repo-map skill.
Entry point: ${input:entry:e.g. POST /api/v1/cards/{id}/activate or @KafkaListener card-events}
Start from docs/repo-map.md, then open only the classes in that flow.
Explain: request DTO and validation -> service steps -> DB tables read/written -> external calls -> events -> response DTO, status codes, and error paths.
End with a Mermaid sequenceDiagram (<= 15 lines).

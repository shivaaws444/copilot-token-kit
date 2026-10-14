# Knowledge base (continuous improvement loop)
Small, topic-split files so Copilot loads only what a task needs.
| File | Holds |
|---|---|
| domain-glossary.md | business terms (card acquisition, eligibility decisioning, co-brand, KYC, PCI scopes) |
| system-facts.md | services, topics/queues, data owners, SLAs, environments |
| lessons-learned.md | dated one-line lessons from bugs, incidents, reviews (inbox) |
Loop: after a bug/incident/review run `/learn` -> lesson appended -> monthly `/curate-knowledge` promotes repeated lessons into the right `.instructions.md` or skill and deletes them here.

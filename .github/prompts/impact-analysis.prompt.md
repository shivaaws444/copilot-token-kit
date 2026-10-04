---
description: What will a change affect?
agent: build
---
Use the repo-map skill.
Planned change: ${input:change:e.g. add field to Card entity, change FraudClient.check signature}
Using docs/repo-map.md (verify in code only where needed), list:
1. Entry points (endpoints/listeners/schedulers) affected
2. Classes to change (path + method)
3. DB tables / migrations needed
4. External contracts affected (APIs, topics, queues)
5. Tests to update or add, with the narrowest mvn command

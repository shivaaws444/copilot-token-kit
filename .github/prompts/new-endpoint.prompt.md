---
description: Add a REST endpoint following module patterns
agent: build
---
Use the spring-feature and token-budget skills.
Module: ${input:module:e.g. card-service}
Endpoint: ${input:endpoint:e.g. POST /cards/{id}/activate}
Behavior: ${input:behavior:what it should do, inputs, outputs, errors}
Copy patterns from the closest existing endpoint in this module (name it before coding).
Deliver: controller, service, DTOs, service unit test, @WebMvcTest. Hunks only.

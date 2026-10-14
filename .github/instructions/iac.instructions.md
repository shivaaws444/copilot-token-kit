---
applyTo: "**/*.{tf,yaml,yml}"
---
- Terraform: variables for env-specific values, least-privilege IAM, tags on all resources, no secrets in state/vars.
- Kubernetes: resource requests/limits, liveness/readiness probes, non-root securityContext, config via ConfigMap/Secret.
- Output a plan/diff summary; never suggest `apply`/`kubectl delete` without explicit ask.

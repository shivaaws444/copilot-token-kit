---
name: terraform-k8s
description: Change Terraform/CloudFormation or Kubernetes/EKS manifests/Helm (services, IAM, SQS, Lambda, deployments, probes, HPA). Use for any infra, IaC, k8s, EKS, or deployment config task.
---
# Terraform / Kubernetes
- Smallest diff in the existing module; no new modules/providers without asking.
- Terraform: `terraform fmt && terraform validate`, show expected `plan` resources (+/~/-). Flag any destroy.
- IAM: explicit actions/resources, no `*` unless justified.
- K8s: requests/limits, probes, PodDisruptionBudget for prod, non-root, image tag pinned (no `latest`).
- Never run apply/delete; the user does. Output diff + risk + rollback line.

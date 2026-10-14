---
name: aws-lambda-python
description: Write or fix AWS Lambda functions in Python (SQS/API Gateway/EventBridge triggers, boto3, DynamoDB). Use for any Lambda, boto3, or serverless Python task.
---
# AWS Lambda (Python)
- Handler: validate event -> pure logic function -> response. Clients created at module scope.
- SQS trigger: return `batchItemFailures`; never raise for the whole batch on one bad record.
- Config via env vars; secrets via Secrets Manager/SSM, cached.
- Least-privilege IAM listed with the change. Timeouts/memory justified.
- Tests: pytest, botocore Stubber or moto; test the pure function separately from the handler.
Done when: `pytest -q tests/<file>` passes. Output hunks + IAM/infra delta.

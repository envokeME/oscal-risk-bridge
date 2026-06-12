# Optional AWS Deployment Pattern

The project does not need AWS to run. The local CLI is the simplest demo path and is usually the best way to show the risk engineering concept.

If this becomes a cloud workflow, the lightweight AWS pattern is:

1. Upload OSCAL assessment-results JSON to an S3 input prefix.
2. Trigger a Lambda function when a new file lands.
3. Lambda downloads the assessment results, mapping file, and optional context questionnaire files.
4. Lambda runs `oscal_risk_bridge`.
5. Lambda writes CSV and JSON risk registers to an S3 output prefix.
6. EventBridge or SNS notifies reviewers that a new risk register is ready.

## Sample Environment Variables

```text
OUTPUT_BUCKET=oscal-risk-bridge-demo-output
OUTPUT_PREFIX=risk-registers/
MAPPING_KEY=config/risk-scenarios.json
QUESTIONS_KEY=config/risk-context-questions.json
CONTEXT_KEY=config/risk-context.answers.json
VALIDATE_OSCAL=true
```

## Notes

- The included Lambda handler is intentionally thin. The CLI remains the source of truth.
- Keep mapping files versioned. Risk scenario logic should be reviewable like code.
- In production, add full OSCAL schema validation, object tagging, encryption, IAM least privilege, and structured logs.

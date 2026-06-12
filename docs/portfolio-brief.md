# Portfolio Brief

## Project

OSCAL Risk Bridge translates OSCAL-formatted control assessment findings into NIST CSF-aligned risk scenarios and risk register outputs.

## Problem

Control assessments often produce technically accurate findings, but those findings do not automatically answer the risk question.

For example:

- `AC-2` failure: inactive privileged accounts remain enabled
- `IA-2` failure: MFA is not enforced for all administrative access

Individually, these are control failures. Together, they describe a more useful risk scenario: unauthorized privileged access.

## Approach

The project uses a local-first Python CLI to:

1. Parse OSCAL assessment-results JSON.
2. Optionally validate the OSCAL structure used by the demo.
3. Extract failed control findings.
4. Load risk context questionnaire answers.
5. Normalize control identifiers.
6. Map control failures to risk scenarios.
7. Align scenarios to NIST CSF 2.0 functions, categories, and outcomes.
8. Aggregate likelihood, impact, confidence, evidence, and response guidance.
9. Export CSV, JSON, Markdown, and HTML risk register outputs.

## Why It Matters

This project demonstrates practical risk engineering:

- Understanding control frameworks and OSCAL structure
- Applying NIST CSF as a risk communication layer
- Translating technical findings into risk language
- Designing explainable scoring with weighted control coverage, context adjustments, and confidence
- Building automation that supports, rather than replaces, risk judgment
- Producing artifacts that can be used by risk managers and leadership

## Technical Stack

- Python 3.10+
- Standard-library JSON, CSV, argparse, dataclasses
- Local CLI-first design
- Optional AWS Lambda/S3 deployment pattern
- GitHub Actions test workflow
- Static HTML report generation
- OSCAL structure validation guardrail
- Data-driven risk context questionnaire
- AI-ready embedded report data for future model review

## Employer-Relevant Signal

The project is intentionally small, but it shows an end-to-end workflow:

```text
OSCAL assessment data -> context questionnaire -> CSF-aligned scenario aggregation -> risk register output
```

That workflow is relevant to GRC engineering, security automation, cloud risk management, audit readiness, and cyber risk reporting roles.

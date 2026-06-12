# OSCAL Risk Bridge

OSCAL Risk Bridge is a small risk engineering project that translates control assessment findings into risk scenarios and risk register outputs.

Most GRC automation stops at control status: passed, failed, open, or not satisfied. This project explores the next layer up:

- What risk does a failed control actually create?
- How do multiple failed controls aggregate into a scenario leadership can understand?
- How can OSCAL-formatted technical findings become a usable risk register?

The project is intentionally local-first. You can run the full demo without AWS, cloud credentials, or paid services. The `aws/` folder includes a reference pattern for deploying the same flow with S3, Lambda, and EventBridge later.

## Flow

```text
OSCAL assessment results
        |
        v
Control finding parser
        |
        v
Risk scenario mapping
        |
        v
Scenario aggregation and scoring
        |
        v
CSV / JSON risk register
```

## Quick Start

Requires Python 3.10 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m oscal_risk_bridge `
  --findings examples/oscal-assessment-results.json `
  --mapping mappings/risk-scenarios.json `
  --out demo-output/risk-register.csv `
  --json-out demo-output/risk-register.json
```

Or run directly from source without installing:

```powershell
$env:PYTHONPATH="src"
python -m oscal_risk_bridge --findings examples/oscal-assessment-results.json --mapping mappings/risk-scenarios.json --out demo-output/risk-register.csv --json-out demo-output/risk-register.json
```

## Example Output

The CSV risk register includes:

- Scenario ID and title
- Business-readable risk statement
- Aggregated likelihood, impact, and rating
- Mapped failed controls
- Evidence from the originating OSCAL findings
- Suggested owner and response

Example risk statement:

> Unauthorized access risk increases because account lifecycle controls and MFA enforcement have failed, making it more likely that orphaned or weakly protected accounts remain active.

## Project Structure

```text
src/oscal_risk_bridge/     Python package and CLI
examples/                  Sample OSCAL assessment-results input
mappings/                  Control-to-risk-scenario mapping file
docs/                      Architecture notes and LinkedIn follow-up draft
aws/                       Optional AWS deployment notes and sample config
tests/                     Unit tests
demo-output/               Generated locally by the demo command
```

## Design Notes

The scoring model is deliberately simple and transparent:

1. Parse failed or open OSCAL findings.
2. Normalize control IDs such as `AC-2`, `IA-2`, or `SC-7`.
3. Match failed controls to mapped risk scenarios.
4. Aggregate evidence by scenario.
5. Adjust likelihood based on mapped control weight and finding severity.
6. Export a risk register that can be reviewed by risk managers.

This is not a replacement for FAIR, NIST 800-30, or enterprise risk methodology. It is a bridge between control assessment evidence and risk identification.

## AWS Pattern

The AWS version can be built with:

- S3 bucket for OSCAL assessment-results uploads
- Lambda function running this package
- S3 output prefix for generated risk registers
- EventBridge notification when new risk registers are created

The included AWS files are intentionally examples, not account-specific infrastructure.

## Roadmap

- Add support for richer OSCAL assessment-results fields
- Add scenario confidence scoring
- Add risk treatment recommendations
- Add GitHub Actions test workflow
- Add optional API endpoint for uploading findings

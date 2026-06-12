# OSCAL Risk Bridge

[![tests](https://github.com/envokeME/oscal-risk-bridge/actions/workflows/tests.yml/badge.svg)](https://github.com/envokeME/oscal-risk-bridge/actions/workflows/tests.yml)

OSCAL Risk Bridge is a Python GRC engineering prototype that translates OSCAL-formatted control findings into NIST CSF-aligned risk scenarios and risk register outputs.

The goal is to bridge a common gap in GRC automation: control assessment tools can tell us which controls failed, but risk managers still have to explain what those failures mean in operational, governance, and leadership terms.

## Why This Project Exists

Most automation in GRC focuses on evidence collection, control status, and compliance reporting. This project explores the layer above that:

- What risk does a failed control actually create?
- How do multiple failed controls combine into a meaningful risk scenario?
- How can technical assessment findings become language a risk owner can act on?

This is not intended to replace OSCAL, FAIR, NIST 800-30, or an enterprise risk methodology. It is a small bridge between control assessment results and risk identification.

## What It Does

```mermaid
flowchart LR
    A["OSCAL assessment-results JSON"] --> B["Parse failed findings"]
    B --> C["Normalize control IDs"]
    C --> D["Map controls to risk scenarios"]
    D --> E["Align to NIST CSF 2.0 outcomes"]
    E --> F["Aggregate likelihood and impact"]
    F --> G["Export risk register"]
```

Given sample OSCAL assessment findings such as failed `AC-2`, `IA-2`, `AU-6`, `SC-7`, and `CM-6` controls, the tool produces risk register entries like:

| Scenario | NIST CSF 2.0 Alignment | Rating | Why it matters |
| --- | --- | --- | --- |
| Unauthorized privileged access | PROTECT / PR.AA | Critical | Account lifecycle and MFA failures create a plausible path for misuse of privileged accounts. |
| External attack surface exposure | IDENTIFY + PROTECT / ID.RA, PR.PS | Critical | Boundary protection gaps and configuration drift increase exposure to production systems. |
| Delayed detection of suspicious activity | DETECT / DE.CM | Moderate | Inconsistent audit review reduces confidence that suspicious activity will be escalated in time. |

## Demo

Run the local demo:

```powershell
git clone https://github.com/envokeME/oscal-risk-bridge.git
cd oscal-risk-bridge

py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -e .

oscal-risk-bridge `
  --findings examples/oscal-assessment-results.json `
  --mapping mappings/risk-scenarios.json `
  --out demo-output/risk-register.csv `
  --json-out demo-output/risk-register.json `
  --markdown-out demo-output/risk-register.md `
  --html-out demo-output/risk-register.html
```

Expected result:

```text
Parsed 5 OSCAL findings.
Generated 3 risk register entries.
Wrote CSV: demo-output\risk-register.csv
Wrote JSON: demo-output\risk-register.json
Wrote Markdown: demo-output\risk-register.md
Wrote HTML: demo-output\risk-register.html
```

If `py` is not available, use `python` instead.

## Outputs

The tool exports the same risk register in three formats:

- CSV for spreadsheet review
- JSON for downstream automation
- Markdown for GitHub, documentation, and executive-readable summaries
- HTML for a polished BattleRisk-themed risk register

Each output includes:

- Source control findings
- Mapped risk scenario
- NIST CSF 2.0 function/category/outcomes
- Likelihood, impact, score, and rating
- Evidence and recommended response
- AI analysis placeholder with embedded structured risk data

Sample outputs:

- [Sample CSV risk register](examples/risk-register.sample.csv)
- [Sample JSON risk register](examples/risk-register.sample.json)
- [Sample Markdown risk report](examples/risk-register.sample.md)
- [Sample HTML risk report](examples/risk-register.sample.html)
- [NIST CSF alignment notes](docs/nist-csf-alignment.md)

## Project Structure

```text
src/oscal_risk_bridge/     Python package and CLI
examples/                  Sample OSCAL input and generated outputs
mappings/                  Control-to-risk-scenario mapping data
docs/                      Architecture notes and portfolio narrative
aws/                       Optional S3/Lambda deployment pattern
tests/                     Unit tests
```

## Design Choices

The project keeps the subjective risk translation layer in data instead of hiding it in code.

`mappings/risk-scenarios.json` defines:

- Scenario title and risk domain
- NIST CSF 2.0 function, category, and outcome references
- Business-readable risk statement template
- Owner and response recommendation
- Control mappings and weights
- Base likelihood and impact

The scoring model is intentionally simple and explainable:

1. Parse failed or open OSCAL findings.
2. Normalize control IDs such as `AC-2`, `IA-2`, or `SC-7`.
3. Match failed controls to mapped risk scenarios.
4. Aggregate evidence by scenario.
5. Align scenarios to NIST CSF 2.0 functions, categories, and outcomes.
6. Adjust likelihood and impact based on control weight and severity.
7. Export a risk register a human risk owner can review.

## UI or CLI?

This project intentionally starts as a CLI plus report generator. That is the right shape for a GRC engineering artifact because it is automatable, testable, and easy to wire into CI, AWS Lambda, or scheduled assessment workflows.

The generated HTML report provides the presentation layer without requiring a web app server. It includes a BattleRisk-style layout and an AI analysis placeholder with embedded structured JSON for a future model review workflow. A full UI can come later as a separate dashboard layer.

## AWS Pattern

The project runs locally without AWS. The optional AWS pattern is:

```text
S3 upload -> Lambda -> OSCAL Risk Bridge -> S3 risk register outputs
```

See [aws/README.md](aws/README.md) for the deployment concept.

## Tests

```powershell
py -m unittest discover -s tests -p "test_*.py"
```

## Roadmap

- Support more OSCAL assessment-results fields
- Add scenario confidence scoring
- Add richer risk treatment recommendations
- Add optional API endpoint for uploading findings
- Add an HTML dashboard for browsing generated risk scenarios

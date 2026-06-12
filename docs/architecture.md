# Architecture

OSCAL Risk Bridge is built around a small set of explicit transformations.

## 1. Parse Assessment Findings

`oscal.py` reads an OSCAL assessment-results JSON document and extracts findings from:

```text
assessment-results.results[].findings[]
```

Each finding is normalized into a `ControlFinding` object with:

- Control ID
- Finding title
- Status
- Severity
- Description
- Source identifier

The parser is intentionally forgiving so demo data and early assessment exports can still be processed while the project evolves.

## 2. Map Controls to Risk Scenarios

`mappings/risk-scenarios.json` defines the bridge between control language, NIST CSF 2.0 outcomes, and risk language.

Each scenario has:

- Business-readable title
- Domain
- NIST CSF 2.0 function, category, outcomes, and alignment rationale
- Base likelihood and impact
- Owner and response recommendation
- Control mappings with weights and rationale

This keeps the most subjective part of the project in version-controlled data instead of burying it inside Python code.

## 3. Aggregate Scenario Evidence

`engine.py` groups failed findings by normalized control ID, matches them to mapped scenarios, carries forward NIST CSF alignment metadata, and computes weighted exposure.

Severity affects the calculation:

```text
critical = 2.0
high     = 1.5
moderate = 1.0
low      = 0.5
```

The model is simple by design. It is meant to produce explainable first-pass risk register entries, not a black-box risk score.

## 4. Export Risk Register

`exporters.py` writes the resulting risk register as CSV, JSON, Markdown, and HTML.

CSV is useful for spreadsheet review. JSON is useful for downstream workflow automation, dashboards, or API integration. Markdown is useful for GitHub and documentation. HTML is useful for a polished browser-readable risk register that can be shared or screenshotted.

The exports include CSF function, category, outcomes, and rationale so reviewers can trace a risk register row back to a recognizable cybersecurity risk management language.

## Local vs AWS

The local CLI is the source of truth:

```text
python -m oscal_risk_bridge --findings examples/oscal-assessment-results.json --mapping mappings/risk-scenarios.json --out demo-output/risk-register.csv --json-out demo-output/risk-register.json --markdown-out demo-output/risk-register.md --html-out demo-output/risk-register.html
```

The optional AWS pattern uses the same package from Lambda:

```text
S3 upload -> Lambda -> risk register CSV/JSON -> S3 output prefix
```

That means the project can be demonstrated without cloud dependencies, then moved into AWS when a real workflow needs it.

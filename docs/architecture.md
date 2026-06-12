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

`mappings/risk-scenarios.json` defines the bridge between control language and risk language.

Each scenario has:

- Business-readable title
- Domain
- Base likelihood and impact
- Owner and response recommendation
- Control mappings with weights and rationale

This keeps the most subjective part of the project in version-controlled data instead of burying it inside Python code.

## 3. Aggregate Scenario Evidence

`engine.py` groups failed findings by normalized control ID, matches them to mapped scenarios, and computes weighted exposure.

Severity affects the calculation:

```text
critical = 2.0
high     = 1.5
moderate = 1.0
low      = 0.5
```

The model is simple by design. It is meant to produce explainable first-pass risk register entries, not a black-box risk score.

## 4. Export Risk Register

`exporters.py` writes the resulting risk register as CSV and JSON.

CSV is useful for risk teams and leadership review. JSON is useful for downstream workflow automation, dashboards, or API integration.

## Local vs AWS

The local CLI is the source of truth:

```text
python -m oscal_risk_bridge --findings examples/oscal-assessment-results.json --mapping mappings/risk-scenarios.json --out demo-output/risk-register.csv --json-out demo-output/risk-register.json
```

The optional AWS pattern uses the same package from Lambda:

```text
S3 upload -> Lambda -> risk register CSV/JSON -> S3 output prefix
```

That means the project can be demonstrated without cloud dependencies, then moved into AWS when a real workflow needs it.


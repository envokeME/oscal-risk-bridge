# Inputs and Outputs

OSCAL Risk Bridge is designed around explicit, reviewable data files.

## Inputs

| Input | File | Purpose |
| --- | --- | --- |
| OSCAL assessment results | `examples/oscal-assessment-results.json` | Source control findings and objective status data. |
| Risk scenario mapping | `mappings/risk-scenarios.json` | Maps failed controls to risk scenarios, NIST CSF alignment, response owners, and scoring weights. |
| Risk context questions | `mappings/risk-context-questions.json` | Defines 10 business context questions that refine likelihood, impact, and confidence. |
| Risk context answers | `examples/risk-context.answers.json` | Captures assessor or risk owner answers using a 1-5 scale. |

The questionnaire is intentionally separate from the OSCAL file. OSCAL remains the control assessment input, while the questionnaire captures business context such as asset criticality, data sensitivity, exposure, compensating controls, remediation timing, and confidence in the finding data.

## Outputs

| Output | File | Audience |
| --- | --- | --- |
| CSV | `examples/risk-register.sample.csv` | Spreadsheet review, risk register import, and governance workflows. |
| JSON | `examples/risk-register.sample.json` | Automation, API integration, dashboards, and future AI review. |
| Markdown | `examples/risk-register.sample.md` | GitHub review, documentation, and executive-readable summaries. |
| HTML | `examples/risk-register.sample.html` | Static, polished report for presentation and screenshots. |

Each output includes the mapped scenario, NIST CSF 2.0 alignment, risk statement, likelihood, impact, score, rating, control coverage, weighted exposure, confidence, evidence, context adjustments, aggregation notes, owner, and recommended response.

## Example Command

```powershell
oscal-risk-bridge `
  --validate-oscal `
  --findings examples/oscal-assessment-results.json `
  --mapping mappings/risk-scenarios.json `
  --questions mappings/risk-context-questions.json `
  --context examples/risk-context.answers.json `
  --out demo-output/risk-register.csv `
  --json-out demo-output/risk-register.json `
  --markdown-out demo-output/risk-register.md `
  --html-out demo-output/risk-register.html
```

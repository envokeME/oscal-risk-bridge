# Demo Walkthrough

This walkthrough uses the included sample OSCAL assessment-results file, risk scenario mapping, and risk context questionnaire answers.

## Input

The demo OSCAL input contains five `not-satisfied` control findings:

| Control | Finding | Severity |
| --- | --- | --- |
| AC-2 | Inactive privileged accounts remain enabled | High |
| IA-2 | MFA not enforced for all administrative access | High |
| AU-6 | Security log review is inconsistent | Moderate |
| SC-7 | Inbound network exposure exceeds approved baseline | Critical |
| CM-6 | Configuration standard drift | Moderate |

## Mapping

The mapping file connects control failures to risk scenarios:

| Scenario | Mapped Controls | NIST CSF 2.0 Alignment |
| --- | --- | --- |
| Unauthorized privileged access | AC-2, IA-2, AC-6 | PROTECT / PR.AA |
| Delayed detection of suspicious activity | AU-6, SI-4, IR-5 | DETECT / DE.CM |
| External attack surface exposure | SC-7, CM-6, RA-5 | IDENTIFY + PROTECT / ID.RA, PR.PS |

## Context Questions

The demo also includes a 10-question risk context input. The answers refine likelihood, impact, and confidence using business context such as:

- Asset criticality
- Data sensitivity
- Internet exposure
- Privileged access scope
- Known exploitability
- Compensating controls
- Detection coverage
- Remediation timeline
- Business dependency
- Owner confidence

## Command

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

## Result

The tool generates three risk register entries:

| Scenario | Rating | Score |
| --- | --- | ---: |
| Unauthorized privileged access | Critical | 25 |
| External attack surface exposure | Critical | 25 |
| Delayed detection of suspicious activity | High | 16 |

## Example Risk Statement

> Unauthorized access risk increases because AC-2, IA-2 control failures indicate weaknesses in account lifecycle and authentication enforcement. This creates a plausible path for misuse of orphaned or weakly protected privileged accounts.

## Interpretation

The value of the project is not the score by itself. The value is the traceable path from evidence to risk language:

```text
OSCAL finding -> failed control -> mapped scenario -> NIST CSF alignment -> risk register entry
```

The output also shows weighted control coverage, confidence, context adjustments, and aggregation notes so a reviewer can see why the scenario scored the way it did.

This gives risk teams a starting point for review, prioritization, and treatment planning.

## Presentation Output

For LinkedIn or portfolio review, open the HTML report:

```powershell
start demo-output/risk-register.html
```

The HTML output is static and self-contained, so it can be attached, screenshot, or hosted without running a backend service. It uses neutral report styling, a small maintainer logo, and an optional analysis placeholder with embedded structured JSON for future model review.

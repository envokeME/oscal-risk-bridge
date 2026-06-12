# Demo Walkthrough

This walkthrough uses the included sample OSCAL assessment-results file.

## Input

The demo input contains five failed or open control findings:

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

## Command

```powershell
oscal-risk-bridge `
  --findings examples/oscal-assessment-results.json `
  --mapping mappings/risk-scenarios.json `
  --out demo-output/risk-register.csv `
  --json-out demo-output/risk-register.json `
  --markdown-out demo-output/risk-register.md
```

## Result

The tool generates three risk register entries:

| Scenario | Rating | Score |
| --- | --- | ---: |
| Unauthorized privileged access | Critical | 25 |
| External attack surface exposure | Critical | 25 |
| Delayed detection of suspicious activity | Moderate | 9 |

## Example Risk Statement

> Unauthorized access risk increases because AC-2, IA-2 control failures indicate weaknesses in account lifecycle and authentication enforcement. This creates a plausible path for misuse of orphaned or weakly protected privileged accounts.

## Interpretation

The value of the project is not the score by itself. The value is the traceable path from evidence to risk language:

```text
OSCAL finding -> failed control -> mapped scenario -> NIST CSF alignment -> risk register entry
```

This gives risk teams a starting point for review, prioritization, and treatment planning.

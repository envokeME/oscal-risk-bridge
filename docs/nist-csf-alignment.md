# NIST CSF 2.0 Alignment

This project uses NIST CSF 2.0 as the risk communication layer above individual control findings.

The intent is not to claim formal compliance with NIST CSF. The intent is to show how technical findings can be grouped into risk scenarios that map to recognizable CSF functions, categories, and outcomes.

Official NIST CSF 2.0 resources:

- https://www.nist.gov/cyberframework
- https://doi.org/10.6028/NIST.CSWP.29

## Alignment Model

```text
OSCAL finding
  -> failed control
  -> mapped risk scenario
  -> NIST CSF function/category/outcomes
  -> risk register entry
```

## Scenario Mapping

| Scenario | Failed Controls | NIST CSF 2.0 Function | Category | Outcomes |
| --- | --- | --- | --- | --- |
| Unauthorized privileged access | AC-2, IA-2 | PROTECT | PR.AA - Identity Management, Authentication, and Access Control | PR.AA-01, PR.AA-03, PR.AA-05 |
| Delayed detection of suspicious activity | AU-6 | DETECT | DE.CM - Continuous Monitoring | DE.CM-01, DE.CM-03, DE.CM-09 |
| External attack surface exposure | SC-7, CM-6 | IDENTIFY / PROTECT | ID.RA - Risk Assessment; PR.PS - Platform Security | ID.RA-01, ID.RA-05, PR.PS-01 |

## Why CSF Works Here

OSCAL and control frameworks are strong at representing assessment evidence. NIST CSF is strong at communicating cybersecurity risk outcomes across technical, risk, and leadership audiences.

This project uses both:

- OSCAL-style input for finding structure
- Control mappings for technical traceability
- NIST CSF 2.0 for risk communication
- Risk register exports for review and decision-making

## Example

Two findings may appear separately in an assessment:

```text
AC-2: Inactive privileged accounts remain enabled
IA-2: MFA not enforced for all administrative access
```

The risk scenario mapping aggregates them into:

```text
Unauthorized privileged access
NIST CSF 2.0: PROTECT / PR.AA
```

This is the GRC engineering bridge: the tool preserves the control-level evidence while translating it into a risk scenario that a control owner, risk manager, or executive can understand.

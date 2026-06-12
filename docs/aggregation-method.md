# Aggregation Method

The scoring model is intentionally explainable. It is not a statistical loss model and does not replace enterprise risk methodology. Its purpose is to create a first-pass risk register from control evidence.

## 1. Failed Finding Selection

The parser reads OSCAL `assessment-results.results[].findings[]` and keeps findings whose status indicates the objective is not satisfied.

## 2. Control-to-Scenario Mapping

Each risk scenario contains mapped controls and weights. A higher weight means the failed control is more important to that scenario.

Example:

```json
{
  "control_id": "SC-7",
  "weight": 4,
  "rationale": "Boundary protection failures can expose services or administrative access paths."
}
```

## 3. Severity-Adjusted Exposure

Each matched control contributes:

```text
control weight x severity multiplier
```

Current severity multipliers:

| Severity | Multiplier |
| --- | ---: |
| Critical | 2.0 |
| High | 1.5 |
| Moderate / Medium | 1.0 |
| Low | 0.5 |
| Informational | 0.25 |

## 4. Weighted Control Coverage

Control coverage is calculated as:

```text
matched mapped control weight / total mapped control weight
```

This helps separate a scenario where one minor mapped control failed from a scenario where the major drivers failed.

## 5. Questionnaire Context

The risk context questionnaire adds business information that control findings do not usually contain. Each answer uses a 1-5 scale:

```text
1 = low / limited
3 = normal
5 = high / extensive
```

Questions can adjust likelihood, impact, or confidence. They can apply globally or only to specific scenarios.

Likelihood and impact questionnaire influence is capped at +/-1 per dimension. This keeps the scoring anchored in the control evidence while still allowing business context to matter.

## 6. Confidence

Confidence is calculated from:

- Weighted control coverage
- Number of supporting findings
- Number of context answers applied
- Explicit confidence adjustment from the questionnaire

Confidence is not a truth score. It is a signal for reviewers: high confidence means the scenario is well supported by mapped control evidence and contextual answers; lower confidence means the scenario may need more review before being used for leadership reporting.

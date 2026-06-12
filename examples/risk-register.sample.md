# Risk Register Report

Generated from OSCAL assessment findings using OSCAL Risk Bridge.

## Executive Summary

| Scenario | CSF Function | CSF Category | Rating | Score | Confidence | Coverage | Owner |
| --- | --- | --- | --- | ---: | ---: | ---: | --- |
| Unauthorized privileged access | PROTECT | PR.AA - Identity Management, Authentication, and Access Control | Critical | 25 | 88% | 75% | Identity Platform Owner |
| External attack surface exposure | IDENTIFY / PROTECT | ID.RA - Risk Assessment; PR.PS - Platform Security | Critical | 25 | 88% | 75% | Cloud Infrastructure |
| Delayed detection of suspicious activity | DETECT | DE.CM - Continuous Monitoring | High | 16 | 73% | 38% | Security Operations |

## RSK-001: Unauthorized privileged access

**Rating:** Critical  
**Likelihood:** 5/5  
**Impact:** 5/5  
**Confidence:** 88%  
**Control Coverage:** 75%  
**Owner:** Identity Platform Owner

### NIST CSF 2.0 Alignment

- Function: PROTECT
- Category: PR.AA - Identity Management, Authentication, and Access Control
- Outcomes: PR.AA-01, PR.AA-03, PR.AA-05
- Rationale: The scenario maps to NIST CSF 2.0 PROTECT because the failed controls indicate weaknesses in identity management, authentication, and access enforcement.

### Risk Statement

Unauthorized access risk increases because AC-2, IA-2 control failures indicate weaknesses in account lifecycle and authentication enforcement. This creates a plausible path for misuse of orphaned or weakly protected privileged accounts.

### Failed Controls

AC-2, IA-2

### Evidence

- AC-2 | high | Inactive privileged accounts remain enabled: The assessment identified privileged accounts with no login activity for more than 90 days that were still enabled.
- IA-2 | high | MFA not enforced for all administrative access: Administrative console access is allowed for a subset of users without phishing-resistant MFA.

### Aggregation Notes

- Matched 2 of 3 mapped controls (75% weighted control coverage).
- Used 2 failed finding(s) with severity-adjusted weighted exposure of 9.00.
- Applied 9 risk context questionnaire adjustment(s).
- Questionnaire influence is capped at +/-1 per likelihood/impact dimension (applied likelihood +1.00, impact +1.00).

### Context Adjustments

- asset_criticality: +0.5 impact (answer 4/5) - Higher asset criticality increases business impact if the risk scenario occurs. Notes: Production identity, logging, and cloud infrastructure are in scope.
- data_sensitivity: +0.4 impact (answer 4/5) - Sensitive data increases the consequence of unauthorized access or exposure. Notes: Administrative paths can reach systems that process customer and operational data.
- privileged_access_scope: +0.4 impact (answer 4/5) - Broader privileged access increases blast radius after compromise. Notes: Inactive privileged accounts remained enabled.
- known_exploitability: +0.45 likelihood (answer 4/5) - Known exploitability increases the probability that a weakness becomes a loss event. Notes: Account takeover and exposed administrative services are common attacker paths.
- compensating_controls: +0.4 likelihood (answer 2/5) - Compensating controls can reduce likelihood even when a primary control has failed. Notes: Compensating control evidence was incomplete.
- detection_coverage: +0.35 likelihood (answer 2/5) - Better detection coverage reduces the chance that the risk remains active long enough to create material impact. Notes: Log reviews are inconsistent across production accounts.
- remediation_timeline: +0.3 likelihood (answer 4/5) - Longer remediation windows increase exposure duration. Notes: Remediation depends on owner review and change windows.
- business_dependency: +0.45 impact (answer 4/5) - Business process dependency increases operational impact. Notes: Affected services support production operations.
- owner_confidence: +0.5 confidence (answer 4/5) - Confidence improves when finding data is complete, reviewed, and understood by the owner. Notes: Findings were reviewed, but the sample assessment remains a demo dataset.

### Recommended Response

Disable inactive privileged accounts, enforce MFA for administrative access, and review exception handling.


## RSK-003: External attack surface exposure

**Rating:** Critical  
**Likelihood:** 5/5  
**Impact:** 5/5  
**Confidence:** 88%  
**Control Coverage:** 75%  
**Owner:** Cloud Infrastructure

### NIST CSF 2.0 Alignment

- Function: IDENTIFY / PROTECT
- Category: ID.RA - Risk Assessment; PR.PS - Platform Security
- Outcomes: ID.RA-01, ID.RA-05, PR.PS-01
- Rationale: The scenario maps to NIST CSF 2.0 IDENTIFY and PROTECT because exposed network paths and configuration drift affect risk assessment, prioritization, and secure platform configuration.

### Risk Statement

External attack surface risk increases because CM-6, SC-7 control failures suggest exposed network paths and configuration drift that could be used to reach production systems.

### Failed Controls

CM-6, SC-7

### Evidence

- SC-7 | critical | Inbound network exposure exceeds approved baseline: Security group rules permit inbound administrative access from ranges wider than the approved corporate network.
- CM-6 | moderate | Configuration standard drift: A subset of compute instances deviates from the approved hardening baseline.

### Aggregation Notes

- Matched 2 of 3 mapped controls (75% weighted control coverage).
- Used 2 failed finding(s) with severity-adjusted weighted exposure of 10.00.
- Applied 9 risk context questionnaire adjustment(s).
- Questionnaire influence is capped at +/-1 per likelihood/impact dimension (applied likelihood +1.00, impact +1.00).

### Context Adjustments

- asset_criticality: +0.5 impact (answer 4/5) - Higher asset criticality increases business impact if the risk scenario occurs. Notes: Production identity, logging, and cloud infrastructure are in scope.
- data_sensitivity: +0.4 impact (answer 4/5) - Sensitive data increases the consequence of unauthorized access or exposure. Notes: Administrative paths can reach systems that process customer and operational data.
- internet_exposure: +1.0 likelihood (answer 5/5) - External reachability increases opportunity for exploitation. Notes: Administrative ingress was broader than the approved corporate network.
- known_exploitability: +0.45 likelihood (answer 4/5) - Known exploitability increases the probability that a weakness becomes a loss event. Notes: Account takeover and exposed administrative services are common attacker paths.
- compensating_controls: +0.4 likelihood (answer 2/5) - Compensating controls can reduce likelihood even when a primary control has failed. Notes: Compensating control evidence was incomplete.
- detection_coverage: +0.35 likelihood (answer 2/5) - Better detection coverage reduces the chance that the risk remains active long enough to create material impact. Notes: Log reviews are inconsistent across production accounts.
- remediation_timeline: +0.3 likelihood (answer 4/5) - Longer remediation windows increase exposure duration. Notes: Remediation depends on owner review and change windows.
- business_dependency: +0.45 impact (answer 4/5) - Business process dependency increases operational impact. Notes: Affected services support production operations.
- owner_confidence: +0.5 confidence (answer 4/5) - Confidence improves when finding data is complete, reviewed, and understood by the owner. Notes: Findings were reviewed, but the sample assessment remains a demo dataset.

### Recommended Response

Restrict inbound administrative access, review security group exceptions, and remediate baseline drift.


## RSK-002: Delayed detection of suspicious activity

**Rating:** High  
**Likelihood:** 4/5  
**Impact:** 4/5  
**Confidence:** 73%  
**Control Coverage:** 38%  
**Owner:** Security Operations

### NIST CSF 2.0 Alignment

- Function: DETECT
- Category: DE.CM - Continuous Monitoring
- Outcomes: DE.CM-01, DE.CM-03, DE.CM-09
- Rationale: The scenario maps to NIST CSF 2.0 DETECT because audit review and monitoring gaps reduce timely discovery and analysis of suspicious activity.

### Risk Statement

Delayed detection risk increases because AU-6 control failures reduce confidence that suspicious activity will be reviewed and escalated in time to limit business impact.

### Failed Controls

AU-6

### Evidence

- AU-6 | moderate | Security log review is inconsistent: Audit logs are collected, but documented review cadence is inconsistent across production accounts.

### Aggregation Notes

- Matched 1 of 3 mapped controls (38% weighted control coverage).
- Used 1 failed finding(s) with severity-adjusted weighted exposure of 3.00.
- Applied 7 risk context questionnaire adjustment(s).
- Questionnaire influence is capped at +/-1 per likelihood/impact dimension (applied likelihood +1.00, impact +0.95).

### Context Adjustments

- asset_criticality: +0.5 impact (answer 4/5) - Higher asset criticality increases business impact if the risk scenario occurs. Notes: Production identity, logging, and cloud infrastructure are in scope.
- known_exploitability: +0.45 likelihood (answer 4/5) - Known exploitability increases the probability that a weakness becomes a loss event. Notes: Account takeover and exposed administrative services are common attacker paths.
- compensating_controls: +0.4 likelihood (answer 2/5) - Compensating controls can reduce likelihood even when a primary control has failed. Notes: Compensating control evidence was incomplete.
- detection_coverage: +0.35 likelihood (answer 2/5) - Better detection coverage reduces the chance that the risk remains active long enough to create material impact. Notes: Log reviews are inconsistent across production accounts.
- remediation_timeline: +0.3 likelihood (answer 4/5) - Longer remediation windows increase exposure duration. Notes: Remediation depends on owner review and change windows.
- business_dependency: +0.45 impact (answer 4/5) - Business process dependency increases operational impact. Notes: Affected services support production operations.
- owner_confidence: +0.5 confidence (answer 4/5) - Confidence improves when finding data is complete, reviewed, and understood by the owner. Notes: Findings were reviewed, but the sample assessment remains a demo dataset.

### Recommended Response

Define log review cadence, automate alert routing, and track review evidence for high-value systems.

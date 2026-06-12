# Risk Register Report

Generated from OSCAL assessment findings using OSCAL Risk Bridge.

## Executive Summary

| Scenario | CSF Function | CSF Category | Rating | Score | Owner |
| --- | --- | --- | --- | ---: | --- |
| Unauthorized privileged access | PROTECT | PR.AA - Identity Management, Authentication, and Access Control | Critical | 25 | Identity Platform Owner |
| External attack surface exposure | IDENTIFY / PROTECT | ID.RA - Risk Assessment; PR.PS - Platform Security | Critical | 25 | Cloud Infrastructure |
| Delayed detection of suspicious activity | DETECT | DE.CM - Continuous Monitoring | Moderate | 9 | Security Operations |

## RSK-001: Unauthorized privileged access

**Rating:** Critical  
**Likelihood:** 5/5  
**Impact:** 5/5  
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

### Recommended Response

Disable inactive privileged accounts, enforce MFA for administrative access, and review exception handling.


## RSK-003: External attack surface exposure

**Rating:** Critical  
**Likelihood:** 5/5  
**Impact:** 5/5  
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

### Recommended Response

Restrict inbound administrative access, review security group exceptions, and remediate baseline drift.


## RSK-002: Delayed detection of suspicious activity

**Rating:** Moderate  
**Likelihood:** 3/5  
**Impact:** 3/5  
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

### Recommended Response

Define log review cadence, automate alert routing, and track review evidence for high-value systems.

from __future__ import annotations

import math

from .models import ControlFinding, RiskRegisterEntry, RiskScenario


SEVERITY_MULTIPLIERS = {
    "critical": 2.0,
    "high": 1.5,
    "moderate": 1.0,
    "medium": 1.0,
    "low": 0.5,
    "informational": 0.25,
}


def build_risk_register(
    findings: list[ControlFinding],
    scenarios: list[RiskScenario],
) -> list[RiskRegisterEntry]:
    failed_findings = [finding for finding in findings if finding.is_failed]
    findings_by_control: dict[str, list[ControlFinding]] = {}

    for finding in failed_findings:
        findings_by_control.setdefault(finding.normalized_control_id, []).append(finding)

    entries = [
        entry
        for scenario in scenarios
        if (entry := _build_entry_for_scenario(scenario, findings_by_control)) is not None
    ]
    return sorted(entries, key=lambda item: item.score, reverse=True)


def _build_entry_for_scenario(
    scenario: RiskScenario,
    findings_by_control: dict[str, list[ControlFinding]],
) -> RiskRegisterEntry | None:
    matched_findings: list[ControlFinding] = []
    matched_controls: list[str] = []
    rationale: list[str] = []
    weighted_exposure = 0.0

    for mapping in scenario.mappings:
        control_findings = findings_by_control.get(mapping.normalized_control_id, [])
        if not control_findings:
            continue

        matched_controls.append(mapping.control_id.upper())
        rationale.append(f"{mapping.control_id.upper()}: {mapping.rationale}")
        matched_findings.extend(control_findings)

        severity_multiplier = max(
            _severity_multiplier(finding.severity) for finding in control_findings
        )
        weighted_exposure += mapping.weight * severity_multiplier

    if not matched_findings:
        return None

    likelihood = _bounded_score(
        scenario.likelihood_base + math.ceil(weighted_exposure / 4)
    )
    impact = _bounded_score(
        scenario.impact_base + _impact_adjustment(matched_findings)
    )
    score = likelihood * impact

    controls_text = ", ".join(sorted(set(matched_controls)))
    risk_statement = scenario.statement_template.format(
        summary=scenario.summary,
        controls=controls_text,
        finding_count=len(matched_findings),
    )

    return RiskRegisterEntry(
        scenario_id=scenario.scenario_id,
        title=scenario.title,
        domain=scenario.domain,
        csf_function=scenario.csf_function,
        csf_category=scenario.csf_category,
        csf_outcomes=list(scenario.csf_outcomes),
        csf_rationale=scenario.csf_rationale,
        risk_statement=risk_statement,
        owner=scenario.owner,
        response=scenario.response,
        likelihood=likelihood,
        impact=impact,
        score=score,
        rating=_rating(score),
        failed_controls=sorted(set(matched_controls)),
        evidence=_evidence_lines(matched_findings),
        rationale=rationale,
    )


def _severity_multiplier(severity: str) -> float:
    return SEVERITY_MULTIPLIERS.get(severity.strip().lower(), 1.0)


def _impact_adjustment(findings: list[ControlFinding]) -> int:
    severities = {finding.severity.strip().lower() for finding in findings}
    if "critical" in severities:
        return 2
    if "high" in severities:
        return 1
    return 0


def _bounded_score(value: int) -> int:
    return max(1, min(5, value))


def _rating(score: int) -> str:
    if score >= 20:
        return "Critical"
    if score >= 12:
        return "High"
    if score >= 6:
        return "Moderate"
    return "Low"


def _evidence_lines(findings: list[ControlFinding]) -> list[str]:
    lines: list[str] = []

    for finding in findings:
        lines.append(
            f"{finding.control_id.upper()} | {finding.severity} | {finding.title}: "
            f"{finding.description}"
        )

    return lines

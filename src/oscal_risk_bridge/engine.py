from __future__ import annotations

import math

from .context import get_context_adjustments
from .models import (
    ControlFinding,
    RiskContext,
    RiskContextAdjustment,
    RiskRegisterEntry,
    RiskScenario,
)


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
    context: RiskContext | None = None,
) -> list[RiskRegisterEntry]:
    context = context or RiskContext()
    failed_findings = [finding for finding in findings if finding.is_failed]
    findings_by_control: dict[str, list[ControlFinding]] = {}

    for finding in failed_findings:
        findings_by_control.setdefault(finding.normalized_control_id, []).append(finding)

    entries = [
        entry
        for scenario in scenarios
        if (entry := _build_entry_for_scenario(scenario, findings_by_control, context)) is not None
    ]
    return sorted(entries, key=lambda item: item.score, reverse=True)


def _build_entry_for_scenario(
    scenario: RiskScenario,
    findings_by_control: dict[str, list[ControlFinding]],
    context: RiskContext,
) -> RiskRegisterEntry | None:
    matched_findings: list[ControlFinding] = []
    matched_controls: list[str] = []
    rationale: list[str] = []
    matched_control_weight = 0.0
    total_control_weight = sum(mapping.weight for mapping in scenario.mappings)
    weighted_exposure = 0.0

    for mapping in scenario.mappings:
        control_findings = findings_by_control.get(mapping.normalized_control_id, [])
        if not control_findings:
            continue

        matched_controls.append(mapping.control_id.upper())
        rationale.append(f"{mapping.control_id.upper()}: {mapping.rationale}")
        matched_findings.extend(control_findings)
        matched_control_weight += mapping.weight

        severity_multiplier = max(
            _severity_multiplier(finding.severity) for finding in control_findings
        )
        weighted_exposure += mapping.weight * severity_multiplier

    if not matched_findings:
        return None

    context_adjustments = get_context_adjustments(context, scenario.scenario_id)
    likelihood_adjustment = _bounded_adjustment(
        sum(
            adjustment.delta
            for adjustment in context_adjustments
            if adjustment.dimension == "likelihood"
        )
    )
    impact_adjustment = _bounded_adjustment(
        sum(
            adjustment.delta
            for adjustment in context_adjustments
            if adjustment.dimension == "impact"
        )
    )

    likelihood = _bounded_score(
        _round_score(
            scenario.likelihood_base
            + min(2, math.ceil(weighted_exposure / 4))
            + likelihood_adjustment
        )
    )
    impact = _bounded_score(
        _round_score(
            scenario.impact_base + _impact_adjustment(matched_findings) + impact_adjustment
        )
    )
    score = likelihood * impact
    control_coverage = (
        matched_control_weight / total_control_weight if total_control_weight else 1.0
    )

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
        control_coverage=round(control_coverage, 2),
        weighted_exposure=round(weighted_exposure, 2),
        confidence=_confidence(
            control_coverage=control_coverage,
            evidence_count=len(matched_findings),
            context_adjustments=context_adjustments,
        ),
        context_adjustments=_context_lines(context_adjustments),
        aggregation_notes=_aggregation_notes(
            scenario=scenario,
            matched_controls=matched_controls,
            matched_findings=matched_findings,
            control_coverage=control_coverage,
            weighted_exposure=weighted_exposure,
            context_adjustments=context_adjustments,
            likelihood_adjustment=likelihood_adjustment,
            impact_adjustment=impact_adjustment,
        ),
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


def _round_score(value: float) -> int:
    return math.floor(value + 0.5)


def _bounded_adjustment(value: float) -> float:
    return max(-1.0, min(1.0, value))


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


def _confidence(
    control_coverage: float,
    evidence_count: int,
    context_adjustments: list[RiskContextAdjustment],
) -> int:
    evidence_points = min(15, evidence_count * 4)
    context_points = min(10, len(context_adjustments) * 2)
    confidence_delta = sum(
        adjustment.delta * 5
        for adjustment in context_adjustments
        if adjustment.dimension == "confidence"
    )
    confidence = (
        45
        + (control_coverage * 30)
        + evidence_points
        + context_points
        + confidence_delta
    )
    return int(max(25, min(95, round(confidence))))


def _context_lines(adjustments: list[RiskContextAdjustment]) -> list[str]:
    lines: list[str] = []

    for adjustment in adjustments:
        sign = "+" if adjustment.delta > 0 else ""
        line = (
            f"{adjustment.question_id}: {sign}{adjustment.delta} {adjustment.dimension} "
            f"(answer {adjustment.value}/5) - {adjustment.rationale}"
        )
        if adjustment.notes:
            line = f"{line} Notes: {adjustment.notes}"
        lines.append(line)

    return lines


def _aggregation_notes(
    scenario: RiskScenario,
    matched_controls: list[str],
    matched_findings: list[ControlFinding],
    control_coverage: float,
    weighted_exposure: float,
    context_adjustments: list[RiskContextAdjustment],
    likelihood_adjustment: float,
    impact_adjustment: float,
) -> list[str]:
    mapped_count = len(scenario.mappings)
    matched_count = len(set(matched_controls))
    notes = [
        (
            f"Matched {matched_count} of {mapped_count} mapped controls "
            f"({control_coverage:.0%} weighted control coverage)."
        ),
        (
            f"Used {len(matched_findings)} failed finding(s) with severity-adjusted "
            f"weighted exposure of {weighted_exposure:.2f}."
        ),
    ]

    if context_adjustments:
        notes.append(
            f"Applied {len(context_adjustments)} risk context questionnaire adjustment(s)."
        )
        notes.append(
            "Questionnaire influence is capped at +/-1 per likelihood/impact dimension "
            f"(applied likelihood {likelihood_adjustment:+.2f}, impact {impact_adjustment:+.2f})."
        )
    else:
        notes.append("No risk context questionnaire adjustments were applied.")

    return notes

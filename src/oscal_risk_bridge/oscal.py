from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import ControlFinding


def load_oscal_findings(path: Path) -> list[ControlFinding]:
    with path.open("r", encoding="utf-8") as file:
        document = json.load(file)

    findings = list(_iter_findings(document))
    return [_to_control_finding(item) for item in findings]


def _iter_findings(document: dict[str, Any]) -> list[dict[str, Any]]:
    if "findings" in document:
        return list(document.get("findings") or [])

    assessment_results = document.get("assessment-results", {})
    results = assessment_results.get("results", [])
    extracted: list[dict[str, Any]] = []

    for result in results:
        extracted.extend(result.get("findings", []) or [])

    return extracted


def _to_control_finding(item: dict[str, Any]) -> ControlFinding:
    target = item.get("target", {}) or {}
    properties = _props_to_dict(item.get("props", []) or [])

    control_id = (
        target.get("target-id")
        or item.get("control_id")
        or item.get("control-id")
        or properties.get("control-id")
        or "unknown"
    )

    status = (
        item.get("status", {}).get("state")
        if isinstance(item.get("status"), dict)
        else item.get("status")
    ) or properties.get("status") or "unknown"

    severity = (
        properties.get("severity")
        or properties.get("risk-severity")
        or item.get("severity")
        or "moderate"
    )

    description = _first_text(
        item.get("description"),
        item.get("remarks"),
        target.get("description"),
        "No finding description provided.",
    )

    title = _first_text(item.get("title"), target.get("title"), f"{control_id} finding")
    source_id = item.get("uuid") or item.get("id") or f"{control_id}:{title}"
    remarks = _first_text(item.get("remarks"), properties.get("remarks"), "")

    return ControlFinding(
        control_id=str(control_id),
        title=str(title),
        status=str(status),
        severity=str(severity),
        description=str(description),
        source_id=str(source_id),
        remarks=str(remarks),
    )


def _props_to_dict(props: list[dict[str, Any]]) -> dict[str, str]:
    values: dict[str, str] = {}

    for prop in props:
        name = prop.get("name")
        value = prop.get("value")
        if name and value is not None:
            values[str(name)] = str(value)

    return values


def _first_text(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


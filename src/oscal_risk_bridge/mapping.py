from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import ControlMapping, RiskScenario


def load_risk_scenarios(path: Path) -> list[RiskScenario]:
    with path.open("r", encoding="utf-8") as file:
        document = json.load(file)

    scenarios = document.get("scenarios", [])
    return [_to_scenario(item) for item in scenarios]


def _to_scenario(item: dict[str, Any]) -> RiskScenario:
    mappings = tuple(
        ControlMapping(
            control_id=str(mapping["control_id"]),
            weight=float(mapping.get("weight", 1.0)),
            rationale=str(mapping.get("rationale", "")),
        )
        for mapping in item.get("control_mappings", [])
    )

    return RiskScenario(
        scenario_id=str(item["id"]),
        title=str(item["title"]),
        domain=str(item.get("domain", "Enterprise Risk")),
        csf_function=str(item.get("csf_function", "GV")),
        csf_category=str(item.get("csf_category", "GV.RM")),
        csf_outcomes=tuple(str(outcome) for outcome in item.get("csf_outcomes", [])),
        csf_rationale=str(item.get("csf_rationale", "")),
        summary=str(item.get("summary", "")),
        owner=str(item.get("owner", "Risk Management")),
        response=str(item.get("response", "Review control failures and define treatment plan.")),
        likelihood_base=int(item.get("likelihood_base", 2)),
        impact_base=int(item.get("impact_base", 3)),
        mappings=mappings,
        statement_template=str(item.get("statement_template", "{summary}")),
    )

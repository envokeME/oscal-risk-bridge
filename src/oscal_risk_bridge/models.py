from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ControlFinding:
    control_id: str
    title: str
    status: str
    severity: str
    description: str
    source_id: str
    remarks: str = ""

    @property
    def normalized_control_id(self) -> str:
        return normalize_control_id(self.control_id)

    @property
    def is_failed(self) -> bool:
        return self.status.strip().lower() in {
            "fail",
            "failed",
            "finding",
            "not-satisfied",
            "not satisfied",
            "open",
            "partially-satisfied",
            "partially satisfied",
            "unsatisfied",
        }


@dataclass(frozen=True)
class ControlMapping:
    control_id: str
    weight: float
    rationale: str

    @property
    def normalized_control_id(self) -> str:
        return normalize_control_id(self.control_id)


@dataclass(frozen=True)
class RiskScenario:
    scenario_id: str
    title: str
    domain: str
    summary: str
    owner: str
    response: str
    likelihood_base: int
    impact_base: int
    mappings: tuple[ControlMapping, ...]
    statement_template: str


@dataclass
class RiskRegisterEntry:
    scenario_id: str
    title: str
    domain: str
    risk_statement: str
    owner: str
    response: str
    likelihood: int
    impact: int
    score: int
    rating: str
    failed_controls: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    rationale: list[str] = field(default_factory=list)


def normalize_control_id(control_id: str) -> str:
    return control_id.strip().lower().replace("_", "-")


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
    csf_function: str
    csf_category: str
    csf_outcomes: tuple[str, ...]
    csf_rationale: str
    summary: str
    owner: str
    response: str
    likelihood_base: int
    impact_base: int
    mappings: tuple[ControlMapping, ...]
    statement_template: str


@dataclass(frozen=True)
class RiskContextQuestion:
    question_id: str
    prompt: str
    dimension: str
    direction: str
    weight: float
    applies_to: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class RiskContextAnswer:
    question_id: str
    value: int
    notes: str = ""


@dataclass(frozen=True)
class RiskContextAdjustment:
    question_id: str
    prompt: str
    dimension: str
    delta: float
    value: int
    rationale: str
    notes: str = ""


@dataclass(frozen=True)
class RiskContext:
    questions: tuple[RiskContextQuestion, ...] = ()
    answers: tuple[RiskContextAnswer, ...] = ()


@dataclass
class RiskRegisterEntry:
    scenario_id: str
    title: str
    domain: str
    csf_function: str
    csf_category: str
    csf_outcomes: list[str]
    csf_rationale: str
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
    control_coverage: float = 0.0
    weighted_exposure: float = 0.0
    confidence: int = 0
    context_adjustments: list[str] = field(default_factory=list)
    aggregation_notes: list[str] = field(default_factory=list)


def normalize_control_id(control_id: str) -> str:
    return control_id.strip().lower().replace("_", "-")

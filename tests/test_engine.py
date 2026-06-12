import unittest

from oscal_risk_bridge.engine import build_risk_register
from oscal_risk_bridge.models import (
    ControlFinding,
    ControlMapping,
    RiskContext,
    RiskContextAnswer,
    RiskContextQuestion,
    RiskScenario,
)


class EngineTests(unittest.TestCase):
    def test_build_risk_register_aggregates_failed_controls(self):
        findings = [
            ControlFinding(
                control_id="AC-2",
                title="Inactive account",
                status="not-satisfied",
                severity="high",
                description="Privileged inactive account remains enabled.",
                source_id="finding-1",
            ),
            ControlFinding(
                control_id="IA-2",
                title="MFA gap",
                status="open",
                severity="high",
                description="MFA is not enforced.",
                source_id="finding-2",
            ),
            ControlFinding(
                control_id="AU-6",
                title="Passing finding",
                status="satisfied",
                severity="low",
                description="Should not appear.",
                source_id="finding-3",
            ),
        ]
        scenarios = [
            RiskScenario(
                scenario_id="RSK-001",
                title="Unauthorized privileged access",
                domain="Identity",
                csf_function="PROTECT",
                csf_category="PR.AA",
                csf_outcomes=("PR.AA-01", "PR.AA-03"),
                csf_rationale="Access control failures map to CSF identity outcomes.",
                summary="Access risk increases.",
                owner="IAM",
                response="Fix IAM controls.",
                likelihood_base=3,
                impact_base=4,
                mappings=(
                    ControlMapping("AC-2", 3, "Account lifecycle issue."),
                    ControlMapping("IA-2", 3, "Authentication issue."),
                ),
                statement_template="{summary} Failed controls: {controls}.",
            )
        ]

        register = build_risk_register(findings, scenarios)

        self.assertEqual(len(register), 1)
        self.assertEqual(register[0].scenario_id, "RSK-001")
        self.assertEqual(register[0].rating, "Critical")
        self.assertEqual(register[0].csf_function, "PROTECT")
        self.assertEqual(register[0].csf_outcomes, ["PR.AA-01", "PR.AA-03"])
        self.assertEqual(register[0].failed_controls, ["AC-2", "IA-2"])
        self.assertEqual(len(register[0].evidence), 2)
        self.assertEqual(register[0].control_coverage, 1.0)
        self.assertGreater(register[0].confidence, 0)
        self.assertTrue(register[0].aggregation_notes)

    def test_build_risk_register_applies_context_adjustments(self):
        findings = [
            ControlFinding(
                control_id="SC-7",
                title="Broad ingress",
                status="not-satisfied",
                severity="critical",
                description="Administrative ingress is broader than approved.",
                source_id="finding-1",
            )
        ]
        scenarios = [
            RiskScenario(
                scenario_id="RSK-003",
                title="External attack surface exposure",
                domain="Infrastructure",
                csf_function="IDENTIFY / PROTECT",
                csf_category="ID.RA; PR.PS",
                csf_outcomes=("ID.RA-01",),
                csf_rationale="Exposure maps to risk assessment and platform security.",
                summary="Exposure risk increases.",
                owner="Cloud Infrastructure",
                response="Restrict ingress.",
                likelihood_base=2,
                impact_base=3,
                mappings=(ControlMapping("SC-7", 4, "Boundary control issue."),),
                statement_template="{summary} Failed controls: {controls}.",
            )
        ]
        context = RiskContext(
            questions=(
                RiskContextQuestion(
                    question_id="internet_exposure",
                    prompt="Is it internet reachable?",
                    dimension="likelihood",
                    direction="increase",
                    weight=1.0,
                    applies_to=("RSK-003",),
                    rationale="Internet exposure increases exploitation opportunity.",
                ),
            ),
            answers=(RiskContextAnswer("internet_exposure", 5, "Public path exists."),),
        )

        register = build_risk_register(findings, scenarios, context=context)

        self.assertEqual(register[0].likelihood, 5)
        self.assertIn("internet_exposure", register[0].context_adjustments[0])


if __name__ == "__main__":
    unittest.main()

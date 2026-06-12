import unittest

from oscal_risk_bridge.engine import build_risk_register
from oscal_risk_bridge.models import ControlFinding, ControlMapping, RiskScenario


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


if __name__ == "__main__":
    unittest.main()

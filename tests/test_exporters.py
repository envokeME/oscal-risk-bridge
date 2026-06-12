import tempfile
import unittest
from pathlib import Path

from oscal_risk_bridge.exporters import write_html, write_markdown
from oscal_risk_bridge.models import RiskRegisterEntry


class ExporterTests(unittest.TestCase):
    def test_write_markdown_creates_executive_summary(self):
        entry = RiskRegisterEntry(
            scenario_id="RSK-001",
            title="Unauthorized privileged access",
            domain="Identity and Access Risk",
            csf_function="PROTECT",
            csf_category="PR.AA",
            csf_outcomes=["PR.AA-01", "PR.AA-03"],
            csf_rationale="Access control failures map to CSF identity outcomes.",
            risk_statement="Unauthorized access risk increases.",
            owner="Identity Platform Owner",
            response="Review and remediate privileged access.",
            likelihood=4,
            impact=5,
            score=20,
            rating="Critical",
            failed_controls=["AC-2", "IA-2"],
            evidence=["AC-2 | high | Inactive account remains enabled."],
            rationale=["AC-2: Account lifecycle issue."],
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "risk-register.md"
            write_markdown([entry], path)
            output = path.read_text(encoding="utf-8")

        self.assertIn("# Risk Register Report", output)
        self.assertIn("| Unauthorized privileged access |", output)
        self.assertIn("## RSK-001: Unauthorized privileged access", output)
        self.assertIn("### NIST CSF 2.0 Alignment", output)
        self.assertIn("PR.AA-01, PR.AA-03", output)
        self.assertIn("AC-2, IA-2", output)

    def test_write_html_creates_presentable_report(self):
        entry = RiskRegisterEntry(
            scenario_id="RSK-001",
            title="Unauthorized privileged access",
            domain="Identity and Access Risk",
            csf_function="PROTECT",
            csf_category="PR.AA",
            csf_outcomes=["PR.AA-01", "PR.AA-03"],
            csf_rationale="Access control failures map to CSF identity outcomes.",
            risk_statement="Unauthorized access risk increases.",
            owner="Identity Platform Owner",
            response="Review and remediate privileged access.",
            likelihood=4,
            impact=5,
            score=20,
            rating="Critical",
            failed_controls=["AC-2", "IA-2"],
            evidence=["AC-2 | high | Inactive account remains enabled."],
            rationale=["AC-2: Account lifecycle issue."],
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "risk-register.html"
            write_html([entry], path)
            output = path.read_text(encoding="utf-8")

        self.assertIn("<!doctype html>", output)
        self.assertIn("NIST CSF-Aligned Risk Register", output)
        self.assertIn("Unauthorized privileged access", output)
        self.assertIn("PR.AA-01, PR.AA-03", output)
        self.assertIn("rating-critical", output)


if __name__ == "__main__":
    unittest.main()

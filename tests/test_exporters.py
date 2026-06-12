import tempfile
import unittest
from pathlib import Path

from oscal_risk_bridge.exporters import write_markdown
from oscal_risk_bridge.models import RiskRegisterEntry


class ExporterTests(unittest.TestCase):
    def test_write_markdown_creates_executive_summary(self):
        entry = RiskRegisterEntry(
            scenario_id="RSK-001",
            title="Unauthorized privileged access",
            domain="Identity and Access Risk",
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
        self.assertIn("AC-2, IA-2", output)


if __name__ == "__main__":
    unittest.main()

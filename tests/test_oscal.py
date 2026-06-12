import json
import tempfile
import unittest
from pathlib import Path

from oscal_risk_bridge.oscal import load_oscal_findings


class OscalTests(unittest.TestCase):
    def test_load_oscal_findings_from_assessment_results(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "assessment-results.json"
            path.write_text(
                json.dumps(
                    {
                        "assessment-results": {
                            "results": [
                                {
                                    "findings": [
                                        {
                                            "uuid": "finding-1",
                                            "title": "MFA is missing",
                                            "description": "Administrative MFA is missing.",
                                            "target": {"target-id": "IA-2"},
                                            "props": [{"name": "severity", "value": "high"}],
                                            "status": {"state": "not-satisfied"},
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ),
                encoding="utf-8",
            )

            findings = load_oscal_findings(path)

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].control_id, "IA-2")
        self.assertTrue(findings[0].is_failed)
        self.assertEqual(findings[0].severity, "high")


if __name__ == "__main__":
    unittest.main()

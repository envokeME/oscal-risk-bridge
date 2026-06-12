import unittest
from pathlib import Path

from oscal_risk_bridge.validation import has_errors, validate_assessment_results, validate_oscal_file


class ValidationTests(unittest.TestCase):
    def test_sample_oscal_assessment_results_passes_validator(self):
        repo_root = Path(__file__).resolve().parents[1]
        messages = validate_oscal_file(repo_root / "examples" / "oscal-assessment-results.json")

        self.assertFalse(has_errors(messages), messages)

    def test_invalid_uuid_is_reported(self):
        messages = validate_assessment_results(
            {
                "assessment-results": {
                    "uuid": "not-a-uuid",
                    "metadata": {
                        "title": "Invalid sample",
                        "last-modified": "2026-06-10T16:30:00-07:00",
                        "version": "0.1.0",
                        "oscal-version": "1.1.2",
                    },
                    "import-ap": {"href": "assessment-plan.demo.json"},
                    "results": [
                        {
                            "uuid": "8e44ec1e-7ca0-4b56-98c6-bdf452c732e1",
                            "title": "Assessment",
                            "description": "Assessment result.",
                            "start": "2026-06-10T09:00:00-07:00",
                            "reviewed-controls": {
                                "control-selections": [{"include-controls": [{"control-id": "AC-2"}]}]
                            },
                            "findings": [],
                        }
                    ],
                }
            }
        )

        self.assertTrue(has_errors(messages))
        self.assertIn("assessment-results.uuid", [message.path for message in messages])


if __name__ == "__main__":
    unittest.main()

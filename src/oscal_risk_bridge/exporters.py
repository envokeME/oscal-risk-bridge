from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

from .models import RiskRegisterEntry


CSV_FIELDS = [
    "scenario_id",
    "title",
    "domain",
    "csf_function",
    "csf_category",
    "csf_outcomes",
    "csf_rationale",
    "rating",
    "score",
    "likelihood",
    "impact",
    "owner",
    "response",
    "failed_controls",
    "risk_statement",
    "evidence",
    "rationale",
]


def write_csv(entries: list[RiskRegisterEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
        writer.writeheader()

        for entry in entries:
            row = asdict(entry)
            row["failed_controls"] = "; ".join(entry.failed_controls)
            row["csf_outcomes"] = "; ".join(entry.csf_outcomes)
            row["evidence"] = " || ".join(entry.evidence)
            row["rationale"] = " || ".join(entry.rationale)
            writer.writerow(row)


def write_json(entries: list[RiskRegisterEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump([asdict(entry) for entry in entries], file, indent=2)
        file.write("\n")


def write_markdown(entries: list[RiskRegisterEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Risk Register Report",
        "",
        "Generated from OSCAL assessment findings using OSCAL Risk Bridge.",
        "",
        "## Executive Summary",
        "",
        "| Scenario | CSF Function | CSF Category | Rating | Score | Owner |",
        "| --- | --- | --- | --- | ---: | --- |",
    ]

    for entry in entries:
        lines.append(
            "| "
            f"{_escape_table(entry.title)} | "
            f"{_escape_table(entry.csf_function)} | "
            f"{_escape_table(entry.csf_category)} | "
            f"{entry.rating} | "
            f"{entry.score} | "
            f"{_escape_table(entry.owner)} |"
        )

    for entry in entries:
        lines.extend(
            [
                "",
                f"## {entry.scenario_id}: {entry.title}",
                "",
                f"**Rating:** {entry.rating}  ",
                f"**Likelihood:** {entry.likelihood}/5  ",
                f"**Impact:** {entry.impact}/5  ",
                f"**Owner:** {entry.owner}",
                "",
                "### NIST CSF 2.0 Alignment",
                "",
                f"- Function: {entry.csf_function}",
                f"- Category: {entry.csf_category}",
                f"- Outcomes: {', '.join(entry.csf_outcomes)}",
                f"- Rationale: {entry.csf_rationale}",
                "",
                "### Risk Statement",
                "",
                entry.risk_statement,
                "",
                "### Failed Controls",
                "",
                ", ".join(entry.failed_controls),
                "",
                "### Evidence",
                "",
            ]
        )
        lines.extend(f"- {evidence}" for evidence in entry.evidence)
        lines.extend(["", "### Recommended Response", "", entry.response, ""])

    with path.open("w", encoding="utf-8") as file:
        file.write("\n".join(lines).rstrip())
        file.write("\n")


def _escape_table(value: str) -> str:
    return value.replace("|", "\\|")

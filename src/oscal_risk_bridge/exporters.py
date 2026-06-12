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
            row["evidence"] = " || ".join(entry.evidence)
            row["rationale"] = " || ".join(entry.rationale)
            writer.writerow(row)


def write_json(entries: list[RiskRegisterEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump([asdict(entry) for entry in entries], file, indent=2)
        file.write("\n")


from __future__ import annotations

import argparse
from pathlib import Path

from .engine import build_risk_register
from .exporters import write_csv, write_json
from .mapping import load_risk_scenarios
from .oscal import load_oscal_findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="oscal-risk-bridge",
        description="Translate OSCAL assessment findings into risk register outputs.",
    )
    parser.add_argument("--findings", required=True, type=Path, help="OSCAL JSON findings file")
    parser.add_argument("--mapping", required=True, type=Path, help="Risk scenario mapping JSON")
    parser.add_argument("--out", required=True, type=Path, help="CSV risk register output path")
    parser.add_argument("--json-out", type=Path, help="Optional JSON risk register output path")
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="Reserved for future use; currently only matched risk scenarios are exported.",
    )

    args = parser.parse_args(argv)

    findings = load_oscal_findings(args.findings)
    scenarios = load_risk_scenarios(args.mapping)
    entries = build_risk_register(findings, scenarios)

    write_csv(entries, args.out)
    if args.json_out:
        write_json(entries, args.json_out)

    print(f"Parsed {len(findings)} OSCAL findings.")
    print(f"Generated {len(entries)} risk register entries.")
    print(f"Wrote CSV: {args.out}")
    if args.json_out:
        print(f"Wrote JSON: {args.json_out}")

    return 0


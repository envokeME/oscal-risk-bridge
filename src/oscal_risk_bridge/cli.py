from __future__ import annotations

import argparse
from pathlib import Path

from .engine import build_risk_register
from .exporters import write_csv, write_html, write_json, write_markdown
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
    parser.add_argument("--markdown-out", type=Path, help="Optional Markdown risk report output path")
    parser.add_argument("--html-out", type=Path, help="Optional HTML risk report output path")
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
    if args.markdown_out:
        write_markdown(entries, args.markdown_out)
    if args.html_out:
        write_html(entries, args.html_out)

    print(f"Parsed {len(findings)} OSCAL findings.")
    print(f"Generated {len(entries)} risk register entries.")
    print(f"Wrote CSV: {args.out}")
    if args.json_out:
        print(f"Wrote JSON: {args.json_out}")
    if args.markdown_out:
        print(f"Wrote Markdown: {args.markdown_out}")
    if args.html_out:
        print(f"Wrote HTML: {args.html_out}")

    return 0

from __future__ import annotations

import csv
import html
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


def write_html(entries: list[RiskRegisterEntry], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    total = len(entries)
    critical = sum(1 for entry in entries if entry.rating == "Critical")
    high = sum(1 for entry in entries if entry.rating == "High")
    moderate = sum(1 for entry in entries if entry.rating == "Moderate")
    average_score = round(sum(entry.score for entry in entries) / total, 1) if total else 0

    report = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OSCAL Risk Bridge - Risk Register</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #17202a;
      --muted: #5e6a75;
      --line: #d8dee6;
      --surface: #ffffff;
      --soft: #f6f8fb;
      --navy: #12304a;
      --teal: #0f766e;
      --gold: #b7791f;
      --red: #b42318;
      --green: #2f855a;
      --blue: #2563eb;
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      background: #eef2f6;
      color: var(--ink);
      font-family: Arial, Helvetica, sans-serif;
      line-height: 1.5;
    }}

    .page {{
      max-width: 1180px;
      margin: 0 auto;
      background: var(--surface);
      min-height: 100vh;
    }}

    header {{
      background: var(--navy);
      color: #ffffff;
      padding: 34px 42px 30px;
      border-bottom: 6px solid var(--teal);
    }}

    .eyebrow {{
      margin: 0 0 8px;
      color: #b8d7d3;
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 0;
      text-transform: uppercase;
    }}

    h1 {{
      margin: 0;
      font-size: 34px;
      line-height: 1.15;
      letter-spacing: 0;
    }}

    .subtitle {{
      max-width: 850px;
      margin: 14px 0 0;
      color: #dce7ef;
      font-size: 16px;
    }}

    main {{
      padding: 28px 42px 46px;
    }}

    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 28px;
    }}

    .metric {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
      background: var(--soft);
      min-height: 112px;
    }}

    .metric-label {{
      color: var(--muted);
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
    }}

    .metric-value {{
      display: block;
      margin-top: 10px;
      font-size: 32px;
      font-weight: 800;
      color: var(--navy);
    }}

    .metric-note {{
      margin-top: 4px;
      color: var(--muted);
      font-size: 13px;
    }}

    section {{
      margin-top: 30px;
    }}

    h2 {{
      margin: 0 0 14px;
      color: var(--navy);
      font-size: 22px;
      letter-spacing: 0;
    }}

    .table-wrap {{
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      background: #ffffff;
    }}

    th {{
      background: #edf3f8;
      color: #203040;
      font-size: 13px;
      text-align: left;
      text-transform: uppercase;
      padding: 12px;
      border-bottom: 1px solid var(--line);
    }}

    td {{
      padding: 13px 12px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
      font-size: 14px;
    }}

    tr:last-child td {{
      border-bottom: 0;
    }}

    .scenario-grid {{
      display: grid;
      gap: 18px;
    }}

    .scenario {{
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
      background: #ffffff;
    }}

    .scenario-head {{
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 18px;
      padding: 18px 20px;
      background: #f8fafc;
      border-bottom: 1px solid var(--line);
    }}

    .scenario-title {{
      margin: 0;
      color: var(--navy);
      font-size: 20px;
    }}

    .scenario-domain {{
      margin: 5px 0 0;
      color: var(--muted);
      font-size: 14px;
    }}

    .scenario-body {{
      padding: 18px 20px 20px;
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 24px;
    }}

    .label {{
      margin: 0 0 6px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 800;
      text-transform: uppercase;
    }}

    .statement {{
      margin: 0 0 18px;
      font-size: 15px;
    }}

    .badge {{
      display: inline-block;
      border-radius: 999px;
      padding: 5px 10px;
      font-size: 12px;
      font-weight: 800;
      border: 1px solid transparent;
      white-space: nowrap;
    }}

    .rating-critical {{
      color: #ffffff;
      background: var(--red);
    }}

    .rating-high {{
      color: #ffffff;
      background: var(--gold);
    }}

    .rating-moderate {{
      color: #103b2b;
      background: #cfe9dd;
      border-color: #a8d8c2;
    }}

    .rating-low {{
      color: #12351f;
      background: #dcfce7;
      border-color: #bbf7d0;
    }}

    .control-list,
    .evidence-list {{
      margin: 0 0 18px;
      padding-left: 18px;
    }}

    .control-list li,
    .evidence-list li {{
      margin-bottom: 7px;
    }}

    .csf-panel {{
      border-left: 4px solid var(--teal);
      background: #f0fdfa;
      padding: 14px;
      border-radius: 6px;
    }}

    .csf-panel p {{
      margin: 0 0 9px;
      font-size: 14px;
    }}

    .score-box {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      margin-top: 14px;
    }}

    .score-item {{
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px;
      text-align: center;
      background: #ffffff;
    }}

    .score-item strong {{
      display: block;
      color: var(--navy);
      font-size: 20px;
    }}

    footer {{
      border-top: 1px solid var(--line);
      padding: 18px 42px 30px;
      color: var(--muted);
      font-size: 13px;
      background: #f8fafc;
    }}

    @media (max-width: 850px) {{
      header,
      main,
      footer {{
        padding-left: 20px;
        padding-right: 20px;
      }}

      .summary-grid,
      .scenario-body {{
        grid-template-columns: 1fr;
      }}

      .scenario-head {{
        grid-template-columns: 1fr;
      }}

      .table-wrap {{
        overflow-x: auto;
      }}

      table {{
        min-width: 760px;
      }}
    }}
  </style>
</head>
<body>
  <div class="page">
    <header>
      <p class="eyebrow">OSCAL Risk Bridge</p>
      <h1>NIST CSF-Aligned Risk Register</h1>
      <p class="subtitle">Control assessment findings translated into risk scenarios, CSF outcomes, evidence, ownership, and response guidance.</p>
    </header>
    <main>
      <div class="summary-grid">
        <div class="metric">
          <span class="metric-label">Risk Scenarios</span>
          <span class="metric-value">{total}</span>
          <div class="metric-note">Generated from matched control findings</div>
        </div>
        <div class="metric">
          <span class="metric-label">Critical</span>
          <span class="metric-value">{critical}</span>
          <div class="metric-note">Requires priority review</div>
        </div>
        <div class="metric">
          <span class="metric-label">High / Moderate</span>
          <span class="metric-value">{high + moderate}</span>
          <div class="metric-note">{high} high, {moderate} moderate</div>
        </div>
        <div class="metric">
          <span class="metric-label">Average Score</span>
          <span class="metric-value">{average_score}</span>
          <div class="metric-note">Likelihood x impact</div>
        </div>
      </div>

      <section>
        <h2>Executive Summary</h2>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Scenario</th>
                <th>CSF Function</th>
                <th>CSF Category</th>
                <th>Rating</th>
                <th>Score</th>
                <th>Owner</th>
              </tr>
            </thead>
            <tbody>
              {_summary_rows(entries)}
            </tbody>
          </table>
        </div>
      </section>

      <section>
        <h2>Risk Scenarios</h2>
        <div class="scenario-grid">
          {_scenario_cards(entries)}
        </div>
      </section>
    </main>
    <footer>
      Generated by OSCAL Risk Bridge. This report is a decision-support artifact, not a formal compliance attestation.
    </footer>
  </div>
</body>
</html>
"""

    with path.open("w", encoding="utf-8") as file:
        file.write(report)


def _summary_rows(entries: list[RiskRegisterEntry]) -> str:
    return "\n".join(
        f"""<tr>
                <td>{_h(entry.title)}</td>
                <td>{_h(entry.csf_function)}</td>
                <td>{_h(entry.csf_category)}</td>
                <td>{_rating_badge(entry.rating)}</td>
                <td>{entry.score}</td>
                <td>{_h(entry.owner)}</td>
              </tr>"""
        for entry in entries
    )


def _scenario_cards(entries: list[RiskRegisterEntry]) -> str:
    return "\n".join(_scenario_card(entry) for entry in entries)


def _scenario_card(entry: RiskRegisterEntry) -> str:
    controls = "\n".join(f"<li>{_h(control)}</li>" for control in entry.failed_controls)
    evidence = "\n".join(f"<li>{_h(item)}</li>" for item in entry.evidence)
    outcomes = ", ".join(_h(outcome) for outcome in entry.csf_outcomes)

    return f"""<article class="scenario">
            <div class="scenario-head">
              <div>
                <h3 class="scenario-title">{_h(entry.scenario_id)}: {_h(entry.title)}</h3>
                <p class="scenario-domain">{_h(entry.domain)}</p>
              </div>
              <div>{_rating_badge(entry.rating)}</div>
            </div>
            <div class="scenario-body">
              <div>
                <p class="label">Risk Statement</p>
                <p class="statement">{_h(entry.risk_statement)}</p>
                <p class="label">Failed Controls</p>
                <ul class="control-list">{controls}</ul>
                <p class="label">Evidence</p>
                <ul class="evidence-list">{evidence}</ul>
              </div>
              <div>
                <div class="csf-panel">
                  <p class="label">NIST CSF 2.0 Alignment</p>
                  <p><strong>Function:</strong> {_h(entry.csf_function)}</p>
                  <p><strong>Category:</strong> {_h(entry.csf_category)}</p>
                  <p><strong>Outcomes:</strong> {outcomes}</p>
                  <p><strong>Rationale:</strong> {_h(entry.csf_rationale)}</p>
                </div>
                <div class="score-box">
                  <div class="score-item"><span class="label">Likelihood</span><strong>{entry.likelihood}/5</strong></div>
                  <div class="score-item"><span class="label">Impact</span><strong>{entry.impact}/5</strong></div>
                  <div class="score-item"><span class="label">Score</span><strong>{entry.score}</strong></div>
                </div>
                <p class="label" style="margin-top: 18px;">Recommended Response</p>
                <p class="statement">{_h(entry.response)}</p>
              </div>
            </div>
          </article>"""


def _rating_badge(rating: str) -> str:
    css_class = f"rating-{rating.lower()}"
    return f'<span class="badge {css_class}">{_h(rating)}</span>'


def _h(value: str) -> str:
    return html.escape(str(value), quote=True)

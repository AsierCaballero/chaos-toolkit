"""Report and export utilities for chaos experiment results."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from tabulate import tabulate


def generate_report(experiments: list[dict], format: str = "table") -> str:
    """Generate a formatted report from experiment results."""
    if format == "json":
        return json.dumps(experiments, indent=2)

    headers = ["Name", "Kind", "Status", "Verdict", "Age"]
    rows = []
    for exp in experiments:
        rows.append([
            exp.get("name", "N/A"),
            exp.get("kind", "N/A"),
            exp.get("status", "N/A"),
            exp.get("verdict", "N/A"),
            exp.get("age", "N/A"),
        ])

    return tabulate(rows, headers=headers, tablefmt="grid")


def export_sarif(experiments: list[dict]) -> str:
    """Export experiment results in SARIF format for CI integration."""
    sarif_log = {
        "$schema": "https://sarif-json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "chaos-toolkit",
                        "version": "0.1.0",
                        "informationUri": "https://github.com/AsierCaballero/chaos-toolkit",
                    }
                },
                "results": [
                    {
                        "ruleId": exp.get("name", "unknown"),
                        "level": "error" if exp.get("verdict") == "Fail" else "note",
                        "message": {
                            "text": f"Experiment '{exp.get('name')}' verdict: {exp.get('verdict', 'N/A')}"
                        },
                    }
                    for exp in experiments
                ],
            }
        ],
    }
    return json.dumps(sarif_log, indent=2)


def export_html(experiments: list[dict]) -> str:
    """Export experiment results as a standalone HTML report."""
    rows = ""
    for exp in experiments:
        status_color = {
            "Pass": "green",
            "Fail": "red",
            "Running": "orange",
        }.get(exp.get("verdict", ""), "gray")
        rows += f"""
        <tr>
            <td>{exp.get('name', 'N/A')}</td>
            <td>{exp.get('kind', 'N/A')}</td>
            <td>{exp.get('status', 'N/A')}</td>
            <td style="color: {status_color}; font-weight: bold;">{exp.get('verdict', 'N/A')}</td>
            <td>{exp.get('age', 'N/A')}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Chaos Report</title>
<style>
  body {{ font-family: system-ui, sans-serif; padding: 2rem; }}
  h1 {{ color: #333; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ padding: 0.5rem; text-align: left; border-bottom: 1px solid #ddd; }}
  th {{ background: #f5f5f5; }}
</style>
</head>
<body>
<h1>Chaos Engineering Report</h1>
<p>Generated: {datetime.now(timezone.utc).isoformat()}</p>
<table>
<thead><tr><th>Name</th><th>Kind</th><th>Status</th><th>Verdict</th><th>Age</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</body>
</html>"""

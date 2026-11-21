"""JSON, CSV, and self-contained HTML report writers."""
import csv
import html
import json
from datetime import datetime, timezone
from pathlib import Path


def write_report(result: dict, analysis: dict, fmt: str, output_dir: str = "reports") -> str:
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = folder / f"royal-inspector-{stamp}.{fmt}"
    payload = {"generated_at": datetime.now(timezone.utc).isoformat(), "result": result, "analysis": analysis}
    if fmt == "json":
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    elif fmt == "csv":
        fields = ["host", "protocol", "port", "state", "service", "product", "version"]
        with path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(analysis.get("open_ports", []))
    elif fmt == "html":
        keys = ("host", "protocol", "port", "state", "service", "product", "version")
        rows = "".join("<tr>" + "".join(f"<td>{html.escape(str(item.get(k, '') or ''))}</td>" for k in keys) + "</tr>"
                       for item in analysis.get("open_ports", []))
        path.write_text(
            "<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>Royal Network Inspector Report</title><style>body{font:16px system-ui;max-width:1000px;margin:2rem auto;padding:0 1rem}"
            "table{border-collapse:collapse;width:100%}td,th{border:1px solid #bbb;padding:.5rem;text-align:left}</style>"
            "<h1>Royal Network Inspector</h1><p>Authorized-lab report. Heuristic hints are not a vulnerability assessment.</p>"
            f"<p>Hosts: {analysis.get('host_count',0)} | Open ports: {analysis.get('open_port_count',0)}</p>"
            "<table><thead><tr><th>Host</th><th>Protocol</th><th>Port</th><th>State</th><th>Service</th><th>Product</th><th>Version</th></tr></thead>"
            f"<tbody>{rows}</tbody></table></html>", encoding="utf-8")
    else:
        raise ValueError("Report format must be json, csv, or html.")
    return str(path)

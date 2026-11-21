"""Local-only scan history; do not publish real infrastructure inventory."""
import json
from datetime import datetime, timezone
from pathlib import Path


def record_history(target: str, mode: str, analysis: dict, history_file: str = "reports/history.json") -> None:
    path = Path(history_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        entries = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
        if not isinstance(entries, list):
            entries = []
    except (OSError, json.JSONDecodeError):
        entries = []
    entries.append({"timestamp": datetime.now(timezone.utc).isoformat(), "target": target, "mode": mode,
                    "host_count": analysis.get("host_count", 0), "open_port_count": analysis.get("open_port_count", 0)})
    path.write_text(json.dumps(entries[-200:], indent=2), encoding="utf-8")

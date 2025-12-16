import json
from pathlib import Path
from typing import List

from .models import Event



"""Parses log files and returns Event objects.

Looks only for folders like run_2024-...

Args:    log_file (str): Path to the log file.
Returns:    List[Event]: List of parsed Event objects.


"""

def list_runs(logs_dir: str = "logs") -> List[str]:
    base = Path(logs_dir)
    if not base.exists():
        return []

    runs = [
        p.name for p in base.iterdir()
        if p.is_dir() and p.name.startswith("run_")
    ]

    return sorted(runs)



def read_jsonl(path: Path) -> List[dict]:
    records = []

    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    records.append({
                        "raw": line,
                        "error": "invalid_json"
                    })
    except Exception as e:
        records.append({
            "raw": str(path),
            "error": str(e)
        })

    return records



def normalize_record(record: dict, source: str) -> Event:
    ts = (
        record.get("ts")
        or record.get("timestamp")
        or record.get("time")
        or "unknown"
    )

    action = (
        record.get("action")
        or record.get("event")
        or record.get("hook")
        or "unknown"
    )

    message = record.get("message") or action

    direction = record.get("direction")

    return Event(
        ts=str(ts),
        source=source,
        action=str(action),
        message=str(message),
        data=record,
        direction=direction
    )



def detect_scenario_name(run_dir: Path) -> str:
    scenario_log = run_dir / "scenario_log.jsonl"

    if not scenario_log.exists():
        return "baseline / unknown"

    with scenario_log.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
                if record.get("type") == "scenario_meta":
                    return record.get("scenario", "baseline / unknown")
            except Exception:
                continue

    return "baseline / unknown"


def load_events(run_path: str):
    run_dir = Path(run_path)
    events: List[Event] = []
    
    scenario_name = detect_scenario_name(run_dir)

    if not run_dir.exists():
        return events, scenario_name

    # Priority: scenario_log.jsonl
    scenario_log = run_dir / "scenario_log.jsonl"
    if scenario_log.exists():
        records = read_jsonl(scenario_log)
        for r in records:
            events.append(normalize_record(r, source="scenario"))

    # Other jsonl files
    for file in run_dir.glob("*.jsonl"):
        if file.name == "scenario_log.jsonl":
            continue

        records = read_jsonl(file)
        for r in records:
            events.append(normalize_record(r, source=file.stem))

    # Optional: plain text logs
    for file in run_dir.glob("*.log"):
        try:
            with file.open("r", encoding="utf-8") as f:
                for line in f:
                    events.append(Event(
                        ts="unknown",
                        source=file.stem,
                        action="log",
                        message=line.strip(),
                        data={"raw": line.strip()}
                    ))
        except Exception:
            pass

    # Sort by timestamp to ensure correct order
    events.sort(key=lambda e: e.ts)

    return events, scenario_name



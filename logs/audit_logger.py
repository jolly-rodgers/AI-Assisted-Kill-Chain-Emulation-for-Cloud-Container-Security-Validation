import json
from pathlib import Path
from datetime import datetime

AUDIT_LOG = Path("logs/audit_log.jsonl")

def log_event(event: dict):
    event["timestamp"] = datetime.utcnow().isoformat() + "Z"
    with AUDIT_LOG.open("a") as f:
        f.write(json.dumps(event) + "\n")

import json
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path("memory/technique_memory.json")

def load_memory():
    if not MEMORY_FILE.exists():
        return {"runs": []}
    return json.loads(MEMORY_FILE.read_text())

def record_run(target, technique, result, confidence, risk):
    memory = load_memory()
    memory["runs"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "target": target,
        "technique": technique,
        "result": result,
        "confidence": confidence,
        "risk": risk
    })
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))

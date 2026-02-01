#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# --- FORCE PROJECT ROOT INTO PYTHONPATH ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
# ----------------------------------------

import json
import argparse
import subprocess
import uuid
from datetime import datetime

from memory.memory_store import record_run

# Optional audit logger (safe import)
try:
    from logs.audit_logger import log_event
    AUDIT_AVAILABLE = True
except Exception:
    AUDIT_AVAILABLE = False

# Pin Docker API version for lab daemon compatibility
os.environ.setdefault("DOCKER_API_VERSION", "1.43")

RECON_FILE = Path("ai-recon/examples/exposed_docker.json")
TECHNIQUES_FILE = Path("execution/techniques.yaml")

# -------------------------
# Utility loaders
# -------------------------
def load_json(path):
    return json.loads(path.read_text())

def load_yaml(path):
    import yaml
    return yaml.safe_load(path.read_text())

def run_cmd(cmd, dry_run):
    if dry_run:
        print(f"[DRY-RUN] {cmd}")
        return True
    print(f"[EXEC] {cmd}")
    return subprocess.run(cmd, shell=True).returncode == 0

# -------------------------
# Main execution
# -------------------------
def main():
    parser = argparse.ArgumentParser(description="Blackcart Kill-Chain Executor")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution only")
    parser.add_argument("--lab-live", action="store_true", help="Execute against lab targets")
    parser.add_argument("--audit", action="store_true", help="Enable audit logging")
    args = parser.parse_args()

    dry_run = not args.lab_live
    run_id = str(uuid.uuid4())

    recon = load_json(RECON_FILE)
    techniques = load_yaml(TECHNIQUES_FILE)

    goal = recon.get("goal", "Security validation")

    targets = [
        t for t in recon.get("results", [])
        if t.get("confidence", 0) >= 0.8
        and t.get("org") == "lab"
    ]

    print(f"[+] Eligible targets: {len(targets)}")

    for t in targets:
        target = f"tcp://{t['ip']}:{t['port']}"
        service = t.get("service", "docker")

        print(f"\n[+] LAB Target: {target}")

        ordered = sorted(
            techniques.items(),
            key=lambda x: x[1].get("escalation_level", 0)
        )

        for tech_id, meta in ordered:

            # --- SERVICE / TARGET GATING ---
            requires = meta.get("requires")
            if requires and requires != service:
                continue
            # --------------------------------

            if t["confidence"] < meta.get("confidence_min", 1.0):
                continue

            playbook = Path("execution/playbooks") / meta["playbook"]
            print(f"\n[>] Technique: {tech_id}")

            commands = load_yaml(playbook).get("commands", [])
            success = True

            for cmd in commands:
                rendered = cmd.replace("{{target}}", target)
                success = run_cmd(rendered, dry_run)
                if not success:
                    print("[!] Technique failed — stopping escalation")
                    break

            # -------------------------
            # Learning memory
            # -------------------------
            record_run(
                target=target,
                technique=tech_id,
                result="success" if success else "failure",
                confidence=meta.get("confidence_min", 0),
                risk=meta.get("risk", "UNKNOWN")
            )

            # -------------------------
            # Audit logging (optional)
            # -------------------------
            if args.audit and AUDIT_AVAILABLE:
                log_event({
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "run_id": run_id,
                    "mode": "lab",
                    "goal": goal,
                    "target": target,
                    "service": service,
                    "kill_chain_phase": meta.get("phase", "execution"),
                    "technique": tech_id,
                    "escalation_level": meta.get("escalation_level", 0),
                    "confidence_required": meta.get("confidence_min", 0),
                    "risk": meta.get("risk", "UNKNOWN"),
                    "action_type": "command_execution",
                    "result": "success" if success else "failure",
                    "dry_run": dry_run,
                    "safety_controls": {
                        "lab_only": meta.get("lab_only", True),
                        "read_only": not meta.get("destructive", False),
                        "destructive": meta.get("destructive", False)
                    }
                })

            if not success:
                break

    print("\n[✓] Execution complete.")

if __name__ == "__main__":
    main()


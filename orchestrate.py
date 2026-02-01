#!/usr/bin/env python3

import argparse
import subprocess
import sys
import json
from pathlib import Path

RECON_CMD = ["python3", "ai-recon/agent/recon_agent.py"]
EXEC_CMD = ["python3", "execution/run_blackcart.py"]
RECON_RESULTS = Path("ai-recon/examples/exposed_docker.json")

def run(cmd, allow_fail=False):
    print(f"\n[+] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0 and not allow_fail:
        print("[!] Step failed — stopping orchestration")
        sys.exit(result.returncode)

def inject_lab_target():
    if not RECON_RESULTS.exists():
        print("[!] Recon results file not found — skipping lab injection")
        return

    data = json.loads(RECON_RESULTS.read_text())

    lab_target = {
        "ip": "localhost",
        "port": 2375,
        "service": "docker",
        "exposure": "lab",
        "org": "lab",
        "country": "LAB",
        "risk_reason": "Local unauthenticated Docker API (lab)",
        "confidence": 1.0,
        "tags": ["docker", "lab", "unauthenticated"],
        "source": "lab"
    }

    results = data.get("results", [])

    # Avoid duplicate injection
    if not any(t.get("org") == "lab" for t in results):
        results.insert(0, lab_target)
        data["results"] = results
        RECON_RESULTS.write_text(json.dumps(data, indent=2))
        print("[+] LAB target injected into recon results")
    else:
        print("[+] LAB target already present")

def main():
    parser = argparse.ArgumentParser(description="Autonomous Red Team Orchestrator")
    parser.add_argument("--goal", required=True)
    parser.add_argument("--mode", choices=["lab"], default="lab")
    parser.add_argument("--auto-approve", action="store_true")
    args = parser.parse_args()

    print("\n=== PHASE 1: AI Recon ===")
    run(RECON_CMD + [args.goal], allow_fail=True)

    if args.mode == "lab":
        inject_lab_target()

    print("\n=== PHASE 2: Dry-Run Validation ===")
    run(EXEC_CMD + ["--dry-run"])

    if args.auto_approve:
        print("\n=== PHASE 3: LAB-LIVE EXECUTION (AUTHORIZED) ===")
        run(EXEC_CMD + ["--lab-live"])
    else:
        print("\n[!] Auto-approve not set — stopping after dry-run")

    print("\n[✓] Orchestration complete")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import json
import sys
from pathlib import Path

RECON_FILE = Path("ai-recon/examples/exposed_docker.json")
PLAYBOOK_FILE = Path("execution/playbooks/docker_lab_validate.yaml")

MIN_CONFIDENCE = 0.8

def load_recon():
    if not RECON_FILE.exists():
        print(f"[!] Recon file not found: {RECON_FILE}")
        sys.exit(1)
    return json.loads(RECON_FILE.read_text())

def main():
    data = load_recon()
    targets = data.get("results", [])

    print("\n[+] Blackcart Dry-Run Simulator")
    print("[+] Playbook:", PLAYBOOK_FILE.name)
    print("[+] Confidence threshold:", MIN_CONFIDENCE)

    eligible = [
        t for t in targets
        if float(t.get("confidence", 0)) >= MIN_CONFIDENCE
    ]

    print(f"\n[+] {len(eligible)} targets eligible for execution\n")

    for t in eligible:
        target = f"tcp://{t['ip']}:{t['port']}"
        print("=" * 60)
        print(f"Target: {target}")
        print(f"Org: {t.get('org')}")
        print(f"Country: {t.get('country')}")
        print(f"Confidence: {t.get('confidence')}")
        print("\nCommands that would execute:\n")

        print(f"docker -H {target} version")
        print(f"docker -H {target} ps")
        print(f"docker -H {target} run --rm alpine id")

    print("\n[+] Dry-run complete. No commands executed.")

if __name__ == "__main__":
    main()

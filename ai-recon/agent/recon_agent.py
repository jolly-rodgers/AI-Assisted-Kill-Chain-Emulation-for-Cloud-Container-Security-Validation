"""
recon_agent.py

Autonomous recon orchestrator.
No chat. No UI. One-shot execution.
"""

import sys
import json
from pathlib import Path
from statistics import mean

from ollama_runtime import OllamaRuntime
from shodan_client import ShodanMCPClient
from normalizer import normalize_docker_host


# -------------------------------
# Path resolution (CRITICAL)
# -------------------------------
# ai-recon/agent/recon_agent.py
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "examples"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -------------------------------
# Recon configuration
# -------------------------------
DOCKER_QUERIES = [
    'port:2375 "Docker API"',
    'port:2375 "Api-Version"',
    'port:2375 "Containers"',
    'port:2375 "GET /containers/json"',
]

CONFIDENCE_THRESHOLD = 0.75


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 recon_agent.py '<goal>'")
        sys.exit(1)

    goal = sys.argv[1]
    print(f"[+] Goal received: {goal}")

    # 1. Initialize runtime + intel client
    runtime = OllamaRuntime()
    shodan = ShodanMCPClient()

    # 2. AI planning (advisory only)
    plan = runtime.plan(goal)
    print(f"[+] AI plan: {plan}")

    # 3. Execute curated Docker recon queries
    raw_hosts = []

    for query in DOCKER_QUERIES:
        print(f"[+] Shodan query: {query}")
        try:
            result = shodan.search(query=query, limit=5)
            raw_hosts.extend(result.get("matches", []))
        except Exception as e:
            print(f"[!] Query failed: {e}")

    print(f"[+] Retrieved {len(raw_hosts)} raw hosts (pre-dedup)")

    # 4. De-duplicate by IP
    unique_hosts = {}
    for host in raw_hosts:
        ip = host.get("ip_str")
        if ip and ip not in unique_hosts:
            unique_hosts[ip] = host

    deduped_hosts = list(unique_hosts.values())
    print(f"[+] {len(deduped_hosts)} unique hosts after dedup")

    # 5. Normalize results
    targets = []

    for host in deduped_hosts:
        try:
            target = normalize_docker_host(host)

            # Absolute safety: confidence must be numeric
            target["confidence"] = round(
                min(float(target.get("confidence", 0.0)), 1.0),
                2
            )

            targets.append(target)
        except Exception:
            continue

    print(f"[+] Normalized {len(targets)} targets")

    # 6. Confidence gating
    if targets:
        avg_confidence = mean(t["confidence"] for t in targets)
    else:
        avg_confidence = 0.0

    print(f"[+] Average confidence: {avg_confidence:.2f}")

    if avg_confidence >= CONFIDENCE_THRESHOLD:
        decision = {
            "decision": "stop",
            "reason": "Sufficient high-confidence unauthenticated Docker APIs identified"
        }
    else:
        decision = runtime.reflect(targets)
        if not decision.get("reason"):
            decision["reason"] = "Decision based on confidence and exposure signals"

    print(f"[+] AI decision: {decision}")

    # 7. Save artifact (DETERMINISTIC LOCATION)
    output = {
        "goal": goal,
        "plan": plan,
        "decision": decision,
        "results": targets
    }

    out_file = OUTPUT_DIR / "exposed_docker.json"
    out_file.write_text(json.dumps(output, indent=2))
    print(f"[+] Results written to {out_file}")


if __name__ == "__main__":
    main()
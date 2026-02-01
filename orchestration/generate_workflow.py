"""
generate_workflow.py

Transforms recon artifacts into Blackdagger workflows.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RECON_FILE = BASE_DIR / "ai-recon" / "examples" / "exposed_docker.json"
WORKFLOW_DIR = BASE_DIR / "orchestration" / "workflows"
TEMPLATE_FILE = WORKFLOW_DIR / "docker_validate.yaml"
OUTPUT_FILE = WORKFLOW_DIR / "docker_validate.generated.yaml"


def load_targets():
    if not RECON_FILE.exists():
        raise FileNotFoundError(f"Recon file not found: {RECON_FILE}")

    data = json.loads(RECON_FILE.read_text())
    return data.get("results", [])


def generate_workflow(targets):
    template = TEMPLATE_FILE.read_text()

    target_blocks = []
    for t in targets:
        block = f"""
targets:
  - ip: {t['ip']}
    port: {t['port']}
    protocol: http
"""
        target_blocks.append(block)

    return template + "\n".join(target_blocks)


def main():
    WORKFLOW_DIR.mkdir(parents=True, exist_ok=True)

    targets = load_targets()
    print(f"[+] Loaded {len(targets)} recon targets")

    workflow = generate_workflow(targets)
    OUTPUT_FILE.write_text(workflow)

    print(f"[+] Generated Blackdagger workflow:")
    print(f"    {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
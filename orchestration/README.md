# Phase 2 – Orchestration (Blackdagger)

This phase consumes normalized recon artifacts produced by Phase 1
and converts them into deterministic, auditable execution workflows.

## Responsibilities
- Read recon artifacts (JSON)
- Apply confidence and service filters
- Generate Blackdagger DAG workflows
- NO recon
- NO exploitation
- NO AI decision-making

## Input
- ../ai-recon/examples/exposed_docker.json

## Output
- workflows/*.yaml (Blackdagger DAGs)

## Design Principles
- Artifact-driven (not API-driven)
- Deterministic and re-runnable
- Safe-by-default (read-only validation)
- Execution deferred to Phase 3 (Blackcart)

Phase 2 answers:
"Given trusted targets, what actions should be orchestrated and in what order?"

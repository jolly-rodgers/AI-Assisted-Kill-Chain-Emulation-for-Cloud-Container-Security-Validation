# 🧠 AI-Assisted Kill-Chain Emulation for Cloud & Container Security

## Executive Summary

This project demonstrates how a modern attacker could move from **exposed cloud or container attack surfaces** to **host-level impact** if security controls or detections fail.

It is a **defensive, lab-only system** designed to help security teams **validate controls, uncover detection gaps, and generate actionable evidence** before issues reach production.

The system emulates **attacker behavior**, not malware.  
There is **no persistence, no destructive payloads, and no live exploitation**.

Its purpose is to help organizations answer one question:

> *If an attacker tried this today, would we block it — and if not, would we know?*

---

## ⚠️ Scope & Safety

**Authorized / Lab Environments Only**

- No real malware
- No data destruction
- No uncontrolled lateral movement
- No persistence mechanisms

All techniques are **behavior-accurate but defender-safe**, designed for:
- Pre-production validation
- Purple team exercises
- Detection engineering
- Control verification

---

## 🎯 What This Project Demonstrates

This system shows how **real attackers operate across cloud and container environments**, and how modern defenses should respond.

It demonstrates the ability to:

- Discover exposed cloud and container attack surfaces
- Autonomously select escalation techniques using AI
- Execute a controlled kill-chain end-to-end
- Record forensic-quality audit evidence
- Validate security controls *before* production

---

## 🧩 Control Validation vs Detection Gaps

This project explicitly separates **security controls** from **security detections**.

### Controls Successfully Enforced

In hardened environments, the system confirms that:

- Privileged container execution is blocked
- Host filesystem mounts are prevented
- Cloud metadata access is restricted when protections are enabled

These outcomes demonstrate **effective preventative controls**.

---

### Detection Gaps Identified

The project also highlights where **detections lag behind behavior**, including:

- Reconnaissance activity generating logs but no alerts
- Docker API exposure producing telemetry without correlation
- Container escape indicators lacking severity classification

These are not failures of technology — they are **signal-to-noise and prioritization problems** commonly seen in real SOCs.

---

### Recommended Improvements

Based on observed gaps, recommended improvements include:

- Alerting on Docker API enumeration attempts
- Correlating container runtime events with host namespace changes
- Flagging repeated failed escalation attempts as early intrusion signals

The goal is not exploitation — it is **continuous validation that controls and detections work together**.

---

## 🧭 Simulated Kill-Chain Coverage

| Kill Chain Phase | Emulated | Real Malware |
|----------------|----------|--------------|
| Reconnaissance | ✅ | ❌ |
| Initial Access | ✅ | ❌ |
| Execution | ✅ | ❌ |
| Privilege Escalation | ✅ | ❌ |
| Container Escape | ✅ | ❌ |
| Command & Control (Behavioral) | ✅ | ❌ |
| Persistence (Attempted) | ✅ | ❌ |
| Exfiltration (Simulated) | ✅ | ❌ |

✔ Behavior-accurate  
✔ Detection-focused  
✔ Defender-safe  

---

## 🧠 System Architecture

The system is built as a **controlled orchestration pipeline**:

- AI-driven technique selection
- Safety-checked execution paths
- Continuous audit and learning feedback
- Explicit stop conditions and confidence thresholds

📄 Detailed architecture: `docs/architecture.md`

---

## 🔬 Techniques Implemented

### Docker / Containers

- `docker_api_enumerate` — Unauthenticated Docker API discovery
- `docker_run_root` — Root-level container execution (lab only)
- `docker_mount_host_ro` — Read-only host filesystem escape simulation

### Kubernetes (Early Stage)

- `kubelet_readonly` — Unauthenticated kubelet endpoint access

### Cloud Metadata

- `cloud_metadata_enum` — Metadata service exposure detection

---

## 🧠 Learning & Audit Capabilities

Each execution records:

- Technique outcome (success / blocked)
- Confidence thresholds
- Risk classification
- Observable side effects
- Safety controls applied

Generated artifacts include:

- `memory/technique_memory.json`
- `logs/audit_log.jsonl`
- `docs/reports/Executive_Attack_Report.pdf`

These artifacts are designed for **SOC review, incident response, and audit evidence**.

---

## 🧪 End-to-End Demo Evidence

A single autonomous run is documented via screenshots:

| Phase | Evidence |
|-----|---------|
| AI Recon & Target Discovery | `docs/screenshots/01-ai-recon.png` |
| Dry-Run Validation | `docs/screenshots/02-dry-run.png` |
| Live Lab Execution | `docs/screenshots/03-lab-live-execution.png` |
| Container Escape Proof | `docs/screenshots/04-container-escape.png` |
| Learning Memory | `docs/screenshots/05-learning-memory.png` |
| Audit Logging | `docs/screenshots/06-audit-logging.png` |
| Full Kill-Chain | `docs/screenshots/07-end-to-end.png` |

---

## How This Would Be Used in Production

In a real organization, this system would be:

- Run in staging and pre-production environments
- Triggered during security validation or purple-team exercises
- Integrated with SIEM and alerting pipelines
- Used to continuously test assumptions about cloud and container security

This approach helps teams discover **unknown unknowns** before attackers do.

---

## 🚀 Running the Lab (Example)

```bash
python3 orchestrate.py \
  --goal "Find exposed Docker APIs" \
  --mode lab \
  --auto-approve

python3 execution/run_blackcart.py --dry-run

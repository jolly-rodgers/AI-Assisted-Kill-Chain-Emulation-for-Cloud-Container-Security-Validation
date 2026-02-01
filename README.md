# 🧠 AI-Assisted Kill-Chain Emulation for Cloud & Container Security

> **Autonomous, AI-driven red-team simulation used to validate cloud, container, and SOC detection controls — safely and defensively.**

⚠️ **Authorized / Lab Environments Only**  
This project emulates attacker *behavior*, not real malware or live exploitation.

---

## 🎯 What This Project Demonstrates

This system shows how **real attackers operate across cloud and container environments**, and how modern defenses should detect them.

It proves the ability to:
- Discover exposed cloud/container attack surfaces
- Autonomously select escalation techniques using AI
- Execute a controlled kill-chain end-to-end
- Generate forensic audit logs & learning feedback
- Validate security controls *before* production

**No real malware. No persistence. No data destruction.**

---

## 🧪 End-to-End Demo (Screenshots)

| Phase | Evidence |
|-----|---------|
| AI Recon & Target Discovery | `docs/screenshots/01-ai-recon.png` |
| Dry-Run Validation | `docs/screenshots/02-dry-run.png` |
| Live Lab Execution | `docs/screenshots/03-lab-live-execution.png` |
| Container Escape Proof | `docs/screenshots/04-container-escape.png` |
| Learning Memory | `docs/screenshots/05-learning-memory.png` |
| Audit Logging | `docs/screenshots/06-audit-logging.png` |
| Full Kill-Chain | `docs/screenshots/07-end-to-end.png` |

> These screenshots show a **single autonomous run**, from reconnaissance → execution → audit evidence.

---

## 🧭 Simulated Kill-Chain Coverage

| Kill Chain Phase | Emulated | Real Malware |
|-----------------|----------|--------------|
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

📄 Detailed architecture: `docs/architecture.md`

---

## 🔬 Techniques Implemented

### Docker / Containers
- `docker_api_enumerate` — Unauthenticated Docker API discovery
- `docker_run_root` — Root-level container execution
- `docker_mount_host_ro` — Read-only host filesystem escape

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
- Observable effects
- Safety controls applied

Artifacts:
- `memory/technique_memory.json`
- `logs/audit_log.jsonl`
- `docs/reports/Executive_Attack_Report.pdf`

---

## 🚀 How to Run (Lab)

```bash
python3 orchestrate.py \
  --goal "Find exposed Docker APIs" \
  --mode lab \
  --auto-approve

python3 execution/run_blackcart.py --dry-run

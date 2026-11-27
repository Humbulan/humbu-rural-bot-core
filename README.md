# Humbu Rural Bot Core

**Lightweight Automation, Telemetry & Government SaaS Engine for Edge & Termux Environments**

![Humbu Rural Bot Core Demo](assets/demo.gif)

`humbu-rural-bot-core` is the operational engine powering rural service delivery, hardware telemetry, and municipal SaaS workflows. Designed to run cleanly on low-overhead Linux nodes and Android Termux deployments without heavy cloud dependencies, it bridges field hardware, real-time monitoring, and auditable load verification.

## Quick Start

```bash
# 1. Install dependencies (use requirements.txt on standard Linux servers)
pip install -r requirements_light.txt

# 2. Launch the core orchestration stack and run system sanity checks
chmod +x start_humbu_system.sh && ./start_humbu_system.sh && python3 test_system.py

# 3. Generate a verifiable proof-of-load audit report
python3 generate_audit.py && cat Audit_Proof_of_Load.txt


## Key Capabilities

* **Termux & Edge Optimization:** Dual dependency profiles (`requirements.txt` for full servers, `requirements_light.txt` for mobile/Termux nodes) with unified service orchestration via `start_humbu_system.sh`.
* **Hardware & Telemetry Integration:** Direct interfacing with field sensors and local network hardware (`hardware/`, `monitoring/`) for continuous uptime and load tracking.
* **Auditable Load & Revenue Verification:** Automated proof-of-load generation (`generate_audit.py` → `Audit_Proof_of_Load.txt`) to validate throughput, service milestones, and billing metrics.
* **Modular API & Scripting Layer:** Clean separation between API endpoints (`api/`), operational automation (`scripts/`), environment configuration (`config/`), and persistent storage (`data/`).

---

## Repository Structure

```text
humbu-rural-bot-core/
├── api/                     # Core service endpoints and external integrations
├── config/                  # Environment and runtime configuration profiles
├── data/                    # Structured operational datasets and state records
├── hardware/                # Field device drivers and telemetry interfaces
├── monitoring/              # Health checks, alerts, and performance metrics
├── scripts/                 # Operational maintenance and automation helpers
├── generate_audit.py        # Generates verifiable proof-of-load reports
├── Audit_Proof_of_Load.txt  # Latest system throughput and audit verification output
├── start_humbu_system.sh    # Primary orchestration script for Termux/Linux startup
├── test_system.py           # Automated integration and system sanity checks
├── requirements.txt         # Standard Linux server dependencies
└── requirements_light.txt   # Minimal dependency footprint for Termux/mobile nodes

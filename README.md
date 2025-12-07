🔌 OCPP–CAN Security Lab
EV Charging Infrastructure Attack/Defense Simulation Environment

This repository provides a modular lab environment for simulating Electric Vehicle (EV) charging security scenarios, including:

OCPP (Open Charge Point Protocol) message flow

Mapping OCPP → CAN (EV internal bus)

CAN-Bus simulated via vcan0

Anomaly scenarios (attack scripts)

Defense mechanisms (future)

The project mirrors a real CP (Charge Point) ↔ CSMS (Central System) communication pipeline and extends it into EV-side CAN behavior.

📂 Project Structure

ocpp-can-lab/
│
├── infra/                  # Core infrastructure
│    ├── ocpp_client.py     # Charge Point emulator
│    ├── ocpp_server.py     # CSMS emulator
│    ├── mapping.py         # OCPP → CAN conversion logic
│    ├── can_smoke_test.py  # VCAN testing tool
│    ├── setup_vcan.sh      # VCAN initializer
│    └── __init__.py
│
├── scenarios/              # All anomaly scenarios (each in its own folder)
│    ├── _template/         # Scenario boilerplate
│    └── scenario_00_baseline/
│
├── docs/                   # Project documentation (optional)
│
├── .devcontainer/          # GitHub Codespaces configuration
├── .gitignore
└── README.md




🚀 Getting Started

1. Create virtual environment

python3 -m venv venv
source venv/bin/activate
pip install websockets python-can


2. Enable CAN simulation (Linux only)

sudo bash infra/setup_vcan.sh


3. Run CSMS

python -m infra.ocpp_server

4. Run Charge Point

python -m infra.ocpp_client


🧪 Baseline Scenario

scenarios/scenario_00_baseline/

contains the simplest simulation (no attacks), used to verify pipeline behavior.


🧩 Creating your own scenario

Each scenario lives in its own folder:

scenarios/scenario_XY_name/
   ├── simulate.py
   └── README.md

Team Members can override hook functions:

pre_ocpp()

post_ocpp()

pre_can()

post_can()

to modify, drop, or inject malicious traffic.


🔐 Future Work

Attack scripts for 12 anomaly scenarios

Defense algorithms (IDS, filtering, validation)

Integration with ML/RAG models

Data logging + security reporting



👥 Team Notes

Everyone create a scenario folder + branch

CP pipeline ensures consistent behavior

Devcontainer makes the lab usable on Windows/Mac

Testing is fully reproducible via vcan


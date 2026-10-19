# JalRakshak

**Predict the Failure. Protect the Water.**

JalRakshak is a prototype edge‑AI powered predictive‑maintenance and water‑infrastructure‑reliability system built around the Nordic Semiconductor **nRF54LM20 DK**. The solution demonstrates how a low‑power Bluetooth Mesh node can sense pump health, run on‑device AI inference, compute a water‑reliability score, and communicate with a web dashboard – all while supporting offline‑first operation.

---

## Table of Contents
- [Project Vision](#project-vision)
- [Core Features](#core-features)
- [Repository Structure](#repository-structure)
- [Quick Start (Demo)](#quick-start-demo)
- [Documentation](#documentation)
- [Hardware Architecture](#hardware-architecture)
- [Edge AI Pipeline](#edge-ai-pipeline)
- [Bluetooth Mesh / AquaMesh](#bluetooth-meshaquaMesh)
- [Simulation Engine](#simulation-engine)
- [Contributing](#contributing)
- [License](#license)

---

### Project Vision
JalRakshak translates **equipment degradation** into a **water‑reliability risk** and actionable maintenance decisions. It answers:
1. **What** is degrading?
2. **How severe** is the degradation?
3. **What impact** could it have on water availability?
4. **How urgent** is the maintenance?
5. **What** should the technician inspect?

---

### Core Features
- **Pump Health Monitoring** – vibration, current, temperature, flow, runtime (simulated & real‑sensor ready).
- **Edge AI / Predictive Maintenance** – baseline, feature extraction, health classification (HEALTHY / DEGRADING / CRITICAL).
- **Water Reliability Score** – composite 0‑100 metric (prototype).
- **Failure‑to‑Impact Prediction** – risk, estimated maintenance window, recommended actions.
- **Maintenance Priority Queue** – ranking with urgency levels.
- **Maintenance‑by‑Opportunity** – opportunistic inspection based on technician proximity.
- **Bluetooth / AquaMesh** – BLE Mesh node on nRF54LM20, data‑mule gateway, offline‑first sync.
- **Simulation Engine** – synthetic fault injection for demo without hardware.
- **Multi‑Asset Dashboard** – React + TypeScript UI showing all pumps, tanks, and network status.

---

### Repository Structure
```
JalRakshak/
│
├── README.md               # ← You are here
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
├── .env.example
├── BOM.md                  # Bill of Materials
├── ARCHITECTURE.md         # High‑level system diagram & description
├── DEMO.md                 # Step‑by‑step demo guide
├── ROADMAP.md
├── LIMITATIONS.md
│
├── docs/                   # Detailed design docs (Markdown)
│   ├── problem.md
│   ├── solution.md
│   ├── predictive-maintenance.md
│   ├── edge-ai.md
│   ├── bluetooth-mesh.md
│   ├── nrf54lm20.md
│   ├── hardware.md
│   ├── data-flow.md
│   ├── testing.md
│   └── competition.md
│
├── firmware/               # Nordic nRF Connect SDK project
│   ├── README.md
│   ├── CMakeLists.txt
│   ├── prj.conf
│   ├── boards/
│   └── src/
│       ├── main.c
│       ├── sensors/
│       ├── ai/
│       ├── bluetooth/
│       ├── telemetry/
│       ├── health/
│       └── storage/
│   └── include/
│
├── edge_ai/                # Python ML pipeline & TinyML model
│   ├── datasets/
│   ├── preprocessing/
│   ├── features/
│   ├── models/
│   ├── training/
│   ├── evaluation/
│   └── inference/
│   └── README.md
│
├── backend/                # FastAPI service
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── models/
│   │   └── schemas/
│   ├── tests/
│   └── requirements.txt
│   └── README.md
│
├── frontend/               # React dashboard
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── api/
│   ├── public/
│   ├── package.json
│   └── README.md
│
├── simulation/            # Fault‑injection engine
│   ├── scenarios/
│   ├── generators/
│   └── README.md
│
├── scripts/                # Utility scripts (setup, data generation, etc.)
│
└── assets/
    ├── diagrams/
    └── screenshots/
```

---

### Quick Start (Demo)
1. **Clone the repo**
   ```bash
   git clone <repo‑url> JalRakshak && cd JalRakshak
   ```
2. **Backend** – set up a virtual env and start FastAPI
   ```bash
   cd backend
   python -m venv .venv && .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```
3. **Frontend** – install and run the React UI
   ```bash
   cd ../frontend
   npm ci
   npm run dev   # Vite dev server at http://localhost:5173
   ```
4. **Simulation** – launch the demo simulation engine (Node or Python)
   ```bash
   cd ../simulation
   python -m generators.demo_engine
   ```
5. Open the dashboard; you will see a healthy pump. Use the **Simulation** tab to inject faults step‑by‑step (bearing degradation, overload, etc.). The UI will update health scores, water‑reliability, risk, and maintenance recommendations in real time.

---

### Documentation
- **ARCHITECTURE.md** – overall system block diagram, data flow, and hardware‑software mapping.
- **docs/** – in‑depth design docs (predictive‑maintenance, edge‑AI, Bluetooth Mesh, hardware, testing).
- **BOM.md** – list of required components for a real build (nRF54LM20 DK, sensor breakout boards, etc.).

---

### License
This prototype is released under the Apache‑2.0 License.

---

*All numbers, scores, and predictions are **prototype‑only** and not validated for production use.*

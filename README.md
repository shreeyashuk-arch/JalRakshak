# JalRakshak: Edge-AI Water Reliability & Predictive Maintenance

**Predict the Failure. Protect the Water.**

JalRakshak is an Edge-AI predictive maintenance and water infrastructure reliability system designed for the **Hackster.io "Sustain the System" competition sponsored by Nordic Semiconductor**. The project uses the **Nordic Semiconductor nRF54LM20 DK** as the primary embedded processing, edge-inference, and Bluetooth Mesh node.

---

## 1. What JalRakshak Does Differently

Standard IoT water monitoring merely triggers reactive sensor alarms:
```
Abnormal Vibration Detected  ──>  Alarm Buzzer / Generic Notification
```

**JalRakshak connects machine degradation to community water-access risk:**
```
Pump Vibration Starts Increasing
             ↓
Edge AI Detects Deviation from Healthy Baseline (nRF54LM20)
             ↓
Pump Health Score Decreases (e.g. 96% → 54%)
             ↓
Flow Efficiency Drops & Storage Tank Recovery Time Increases
             ↓
Water Reliability Score Decreases (e.g. 97 → 58.2/100)
             ↓
Potential Water Interruption is Predicted Before Failure
             ↓
Maintenance Priority Becomes HIGH PRIORITY
             ↓
Technician Receives Actionable Maintenance-by-Opportunity Recommendation:
"Inspect bearing/coupling and verify intake condition within 18–30 operating hours."
```

---

## 2. Implementation Boundaries

To ensure complete scientific and engineering honesty:

### Implemented Now in Repository:
- **Firmware Architecture (`firmware/`):** Full Nordic nRF Connect SDK / Zephyr RTOS project structure targeting the **nRF54LM20 DK** (`nrf54lm20dk/nrf54lm20a/cpuapp` and `nrf54lm20dk/nrf54lm20b/cpuapp`). Includes C implementations for sliding-window sensor management, TinyML feature extraction, pump health classification, AquaMesh Bluetooth Mesh layouts, and offline telemetry ring buffering.
- **Edge AI Pipeline (`edge_ai/`):** Reproducible synthetic dataset generator for 5 physical operating modes, 9-dimensional time-series feature extractor (RMS, Crest factor, variance, flow efficiency), trained baseline classification model, and evaluation reporting.
- **Backend Service (`backend/`):** FastAPI REST application with local SQLite persistence, seeded multi-asset fleet (pumps and tanks), failure-to-impact decision logic, and simulation endpoints.
- **Frontend Dashboard (`frontend/`):** React 18 + TypeScript + Tailwind CSS application featuring an overview dashboard, asset fleet rankings, failure-to-impact predictions, AquaMesh BLE status, and an interactive demo simulation panel.
- **Simulation Engine (`simulation/`):** Physical time-series fault generator supporting normal operation, bearing degradation, motor electrical overload, low flow/cavitation, and overheating.
- **Automated Tests:** Comprehensive unit test suites covering the backend API, reliability score formulation, Edge AI pipeline, and simulation fault modes.

### Hardware Dependent / Future Physical Steps:
- Physical sensor acquisition via I2C/SPI/SAADC from physical accelerometer (ADXL355), current sensor (SCT-013), temperature probe (DS18B20), and flow meter (YF-S201).
- Physical 2.4 GHz radio propagation and mesh provisioning across multiple physical nRF54LM20 DK boards.
- Long-term field validation on operating municipal or village borehole pumps.

---

## 3. Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+

### 1. Run the Backend
```bash
# From repository root:
python -m uvicorn backend.app.main:app --port 8000
```
Interactive API docs: `http://localhost:8000/docs`

### 2. Run the React Frontend
```bash
cd frontend
npm install
npm run dev
```
Open your browser at: `http://localhost:5173`

### 3. Run Automated Tests
```bash
# Run backend tests
python -m pytest backend/tests/test_backend.py

# Run Edge-AI pipeline tests
python -m pytest edge_ai/tests/test_edge_ai.py

# Run Simulation tests
python -m pytest simulation/tests/test_simulation.py
```

### 4. Retrain Edge-AI Model
```bash
python -m edge_ai.training.train_baseline
```

---

## 4. Hardware Architecture & BOM

See **[BOM.md](BOM.md)** for complete specifications. The primary controller is the **Nordic Semiconductor nRF54LM20 DK**, chosen for its dual-core ARM Cortex-M33 architecture, hardware FPU, dedicated Axon NPU target, and multiprotocol 2.4 GHz radio.

See **[docs/nrf54lm20.md](docs/nrf54lm20.md)** for in-depth embedded architecture and integration details.

---

## 5. Repository Structure
```
JalRakshak/
├── README.md               # Project overview and status
├── BOM.md                  # Bill of Materials (nRF54LM20 DK & sensors)
├── ARCHITECTURE.md         # End-to-end architecture & boundaries
├── DEMO.md                 # Step-by-step demo guide
│
├── firmware/               # Nordic nRF Connect SDK / Zephyr project
│   ├── CMakeLists.txt
│   ├── prj.conf
│   ├── README.md
│   ├── include/            # C headers (sensors, AI, health, AquaMesh)
│   └── src/                # Modular C implementations
│
├── edge_ai/                # Edge AI pipeline
│   ├── datasets/           # Synthetic dataset generator
│   ├── features/           # Time-series feature extraction
│   ├── models/             # Trained baseline classifier
│   ├── training/           # Model training script
│   ├── evaluation/         # Test evaluation metrics
│   └── inference/          # Offline inference engine
│
├── backend/                # FastAPI backend service
│   ├── app/                # Main application & SQLite database
│   ├── tests/              # Unit tests
│   └── requirements.txt
│
├── frontend/               # React + TypeScript + Tailwind dashboard
│   ├── src/                # UI components & pages
│   ├── package.json
│   └── vite.config.ts
│
├── simulation/             # Physical fault simulation engine
│   ├── generators/         # Time-series fault generator
│   └── tests/              # Simulation tests
│
└── docs/                   # Engineering documentation
    └── nrf54lm20.md        # Nordic nRF54LM20 DK technical documentation
```

---
*Disclaimer: JalRakshak is an experimental prototype research system. Numerical scores, maintenance windows, and simulated faults are prototype estimates and do not represent validated municipal field performance.*

# ARCHITECTURE.md

## System Overview

```
+----------------+      BLE Mesh (AquaMesh)      +-------------------+
| nRF54LM20 DK   |<----------------------------->| Technician Phone |
| (Sensor Node) |  <--- Offline‑First Sync --->  | (Gateway)        |
+----------------+                                 +-------------------+
        |                                                   |
        v                                                   v
+----------------+      FastAPI Backend (Python)      +-------------------+
| Sensors / AI  |-----------------------------------| React Dashboard   |
| (vibration,   |   REST/WS (JSON)                  | (TS + Vite)       |
|  current, ...) |                                   +-------------------+
+----------------+                                         |
        |                                                 |
        v                                                 v
   SQLite DB (local)                               +-------------------+
                                                   | Cloud (optional) |
                                                   +-------------------+
```

### Key Blocks
- **Embedded Firmware** – runs on the nRF54LM20 DK, collects sensor data, runs Edge‑AI inference, and publishes health messages over BLE Mesh.
- **Simulation Layer** – software model of the mesh and sensor streams for early demo without hardware.
- **Backend Service** – FastAPI server that ingests telemetry, stores it in SQLite, computes water‑reliability scores, and serves a REST API.
- **Frontend Dashboard** – React + TypeScript UI that visualises assets, health trends, and maintenance queues.
- **Edge‑AI Pipeline** – Python scripts that generate synthetic data, train a TinyML model, and export a `.tflite` for the device.

---

## Data Flow
1. **Sensors → Firmware** – raw samples are sampled at 100 Hz (vibration) or appropriate rates.
2. **Firmware → AI Engine** – windowed data → feature extraction → TensorFlow‑Lite inference → health classification.
3. **Firmware → Mesh** – health payload (health score, risk, timestamp) broadcast via BLE Mesh.
4. **Gateway Phone** – receives Mesh messages, buffers locally, forwards via HTTP to the backend when internet is available.
5. **Backend** – persists telemetry, recomputes water‑reliability, updates maintenance priority, pushes updates via WebSocket to the dashboard.
6. **Dashboard** – visualises real‑time and historical data; provides simulation controls.

---

## Extensibility
- Add new sensor types by extending `sensor_manager` in the firmware and updating the feature extraction scripts.
- Swap the TinyML model with a more accurate one trained on real data – just replace `model.tflite` and re‑flash.
- Replace SQLite with PostgreSQL for production; the FastAPI schemas are already Pydantic‑typed.

---

*All components are prototype‑ready and documented for easy migration to a production‑grade deployment.*

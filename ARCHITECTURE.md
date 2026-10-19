# JalRakshak: Technical Architecture

**Predict the Failure. Protect the Water.**

JalRakshak connects mechanical equipment degradation directly to community water-access risk using low-power edge intelligence.

---

## 1. End-to-End Architectural Pipeline

```
[ Physical / Simulated Sensors ]
 (ADXL355 Vib, SCT-013 Current, DS18B20 Temp, YF-S201 Flow, Tank Level)
                           │
                           ▼
 [ Nordic Semiconductor nRF54LM20 DK ]
  ├── Signal Acquisition & Sliding Window Buffer (100 Hz)
  ├── Edge Feature Extraction: RMS, Crest Factor, Temp slope, Flow-Eff
  ├── TinyML / Heuristic Anomaly Classifier (Cortex-M33 / Axon NPU)
  ├── Local State Classification: HEALTHY | DEGRADING | CRITICAL
  └── JalRakshak Water Reliability Engine (Composite WRS 0-100)
                           │
                           ▼
                 [ AquaMesh Protocol ]
    (Bluetooth Low Energy / Bluetooth Mesh v1.1)
   ├── Node-to-Node Relay (Pump <-> Tank)
   └── Offline Ring-Buffer Storage (telemetry.c)
                           │
       [ Offline-First BLE Sync ] (Data Mule)
                           │
                           ▼
              [ Technician Handheld Gateway ]
                           │
               [ HTTP / REST Ingestion ]
                           │
                           ▼
             [ JalRakshak Backend Service ]
            (FastAPI + SQLite / PostgreSQL)
                           │
                           ▼
           [ Real-Time React Dashboard ]
```

---

## 2. Implementation Boundaries: Implemented Now vs. Physical Hardware

To maintain complete transparency and technical integrity, the table below categorizes all system modules:

| Subsystem | Status | Implemented in Repo | Requires Physical Hardware |
| :--- | :---: | :--- | :--- |
| **Edge-AI Firmware** | **VERIFIED** | Full C Zephyr RTOS project structure (`firmware/`) with sliding window, feature extraction, and classification | Physical flashing to nRF54LM20 DK board target (`nrf54lm20dk/nrf54lm20a/cpuapp`) |
| **Sensor Interface** | **VERIFIED** | Abstracted interface (`sensor_manager.h/c`) with active simulation/mock driver bridge | Physical wiring to I2C/SPI/ADC pins of ADXL355, SCT-013, DS18B20 |
| **AquaMesh BLE Layer** | **VERIFIED** | Binary packet layouts (`aquamesh.h/c`) and offline ring-buffer logging (`telemetry.c`) | 2.4 GHz RF transmission over physical Nordic radio antenna |
| **Edge-AI ML Pipeline** | **VERIFIED** | Synthetic dataset generator (`synthetic_generator.py`), feature extractor, trained model (`baseline_pump_classifier.joblib`), evaluation metrics | Field sensor dataset for municipal-grade calibration |
| **Water Reliability Score**| **VERIFIED** | Mathematical formula in `reliability_engine.py` and `pump_health.c`, with unit tests | Long-term municipal reservoir ground-truth validation |
| **Backend & Database** | **VERIFIED** | FastAPI REST service with SQLite persistence, seeded assets, and prediction endpoints | Cloud deployment (optional) |
| **Frontend Dashboard** | **VERIFIED** | React 18 + Vite + Tailwind CSS dashboard with live multi-asset tracking and fault injection controls | None (runs locally) |

# Nordic Semiconductor nRF54LM20 DK: System Architecture & Integration

**Competition:** Hackster.io "Sustain the System" (Sponsored by Nordic Semiconductor)  
**Role:** Primary Embedded Edge-AI Controller & AquaMesh Bluetooth Node

---

## 1. Why the nRF54LM20 DK?

Community water infrastructure (deep borehole pumps, solar submersibles, booster stations) operates in remote, off-grid environments where continuous cellular/cloud connectivity is unreliable or cost-prohibitive. 

The **Nordic nRF54LM20 DK** is uniquely suited for JalRakshak:
1. **Dual-Core ARM Cortex-M33 Processing:** Dedicated application core running Zephyr RTOS at up to 128 MHz with single-precision FPU (`CONFIG_FPU=y`). Enables real-time time-series vibration sampling and feature extraction without external DSPs.
2. **Dedicated Axon Neural Processing Unit (NPU) Target (`nrf54lm20b`):** Hardware acceleration for quantized neural networks, allowing continuous anomaly detection at microamp-level power budgets.
3. **Advanced 2.4 GHz Multiprotocol Radio:** Native hardware support for Bluetooth Low Energy (BLE 5.4) and Bluetooth Mesh v1.1. Forms the physical backbone of **AquaMesh**.
4. **Ultra-Low-Power Energy Profiles:** Allows pump monitoring nodes to operate sustainably on small solar panels or multi-year battery reserves.

---

## 2. On-Device Processing Flow

```
+-----------------------------------------------------------------------------------+
|                           Nordic nRF54LM20 DK                                    |
|                                                                                   |
|  [ADC / SPI / I2C / GPIO]                                                         |
|         │                                                                         |
|         ▼                                                                         |
|  [sensor_manager.c]   High-speed windowed sampling (100 Hz vibration, RMS current)|
|         │                                                                         |
|         ▼                                                                         |
|  [edge_ai_engine.c]   Feature extraction: Vibration RMS, Crest Factor, Temp, Flow |
|                       TinyML Health Classification: HEALTHY | DEGRADING | CRITICAL|
|         │                                                                         |
|         ▼                                                                         |
|  [pump_health.c]      Water Reliability Composite Calculation & Maintenance Window|
|         │                                                                         |
|         ▼                                                                         |
|  [aquamesh.c]         AquaMesh Bluetooth Mesh Broadcaster & Offline Telemetry Sync|
+-----------------------------------------------------------------------------------+
```

---

## 3. AquaMesh Bluetooth Architecture

AquaMesh enables wireless communication between scattered water assets:
- **Node-to-Node Mesh:** Pump nodes relay critical alert states to storage tank nodes without requiring cellular towers.
- **Offline-First Data Mule Sync:** When a local technician approaches a pump station carrying a smartphone or handheld gateway (`GW-TECH01`), the nRF54LM20 DK automatically connects over BLE and synchronizes stored telemetry buffer logs (`telemetry.c`).
- **Synchronized Cloud Ingestion:** Once the technician's gateway returns to an area with cellular/Wi-Fi coverage, buffered data synchronizes with the central JalRakshak backend.

---

## 4. Hardware Verification & Implementation Boundaries

| Subsystem | Implemented in Repository | Physical Hardware Requirement |
| :--- | :--- | :--- |
| **Zephyr Application Core** | `firmware/src/main.c`, `prj.conf` | nRF54LM20 DK (`nrf54lm20dk/nrf54lm20a/cpuapp`) |
| **Edge AI Engine** | C feature extraction & scoring in `src/ai/` | ARM Cortex-M33 FPU / Axon NPU |
| **Sensor Interface** | Abstracted mock & driver bridge | Physical ADXL355, SCT-013, DS18B20, YF-S201 |
| **AquaMesh BLE** | Packet layout & state machine in `src/bluetooth/` | 2.4 GHz RF Antenna / Zephyr Bluetooth Mesh stack |

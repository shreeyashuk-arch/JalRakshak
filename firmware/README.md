# JalRakshak nRF54LM20 DK Firmware

**Target Hardware:** Nordic Semiconductor nRF54LM20 DK (`nrf54lm20dk/nrf54lm20a/cpuapp` or `nrf54lm20dk/nrf54lm20b/cpuapp`)  
**SDK Base:** Nordic nRF Connect SDK (Zephyr RTOS v3.1.1+)

---

## 1. What is Implemented Now vs. What Requires Hardware

| Component | Status in Repository | Description / Note |
| :--- | :--- | :--- |
| **Firmware Architecture** | **IMPLEMENTED** | Modular Zephyr/nRF structure (`sensors`, `ai`, `bluetooth`, `health`, `telemetry`, `storage`). |
| **Sensor Interface Abstraction** | **IMPLEMENTED** | `sensor_manager.h/c` with software simulated/mock acquisition pipeline for vibration, current, temperature, and flow. |
| **TinyML Feature Extraction** | **IMPLEMENTED** | Feature calculation in C (Vibration RMS, crest factor, motor current RMS, temperature slope). |
| **Health Decision Engine** | **IMPLEMENTED** | On-chip threshold & state assessment (`HEALTHY`, `DEGRADING`, `CRITICAL`) with maintenance priority weighting. |
| **AquaMesh BLE Architecture** | **IMPLEMENTED** | BLE Advertising & Bluetooth Mesh state structure and payload definitions (`aquamesh.h/c`). |
| **Physical I2C/SPI Sensor Drivers** | **HARDWARE DEPENDENT** | Requires physical ADXL355, SCT-013 ADC, DS18B20 1-Wire, and YF-S201 connected to nRF54LM20 DK pin headers. |
| **Physical BLE Mesh Radio Testing**| **HARDWARE DEPENDENT** | Requires flashing onto physical nRF54LM20 DK and provisioning onto a 2.4 GHz Bluetooth Mesh network. |

---

## 2. Directory Structure

```
firmware/
├── CMakeLists.txt          # Zephyr CMake build script
├── prj.conf                # Kconfig options (BT, BT_MESH, CBPRINTF, FPU, TINYML)
├── README.md               # Hardware documentation & build guide
├── include/
│   ├── sensor_manager.h    # Unified sensor abstraction layer
│   ├── edge_ai_engine.h    # TinyML feature extraction & inference runner
│   ├── pump_health.h       # Health score calculation & state machine
│   ├── aquamesh.h          # BLE Mesh packet layout & node communication
│   ├── telemetry.h         # Offline ring-buffer storage & synchronization
│   └── jalrakshak_config.h # Sampling rates, thresholds, and pin definitions
└── src/
    ├── main.c              # Application entry, RTOS thread orchestration
    ├── sensors/
    │   └── sensor_manager.c
    ├── ai/
    │   └── edge_ai_engine.c
    ├── health/
    │   └── pump_health.c
    ├── bluetooth/
    │   └── aquamesh.c
    └── telemetry/
        └── telemetry.c
```

---

## 3. How to Build (When Nordic SDK is Installed)

Prerequisites:
1. Install [Nordic nRF Connect SDK](https://www.nordicsemi.com/Products/Development-software/nRF-Connect-SDK) v3.1.1+.
2. Install `west` toolchain.

Building for the nRF54LM20 DK:
```bash
# From repository root:
cd firmware
west build -b nrf54lm20dk/nrf54lm20a/cpuapp
```

Flashing to the board:
```bash
west flash
```

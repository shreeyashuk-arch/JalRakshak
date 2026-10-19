# JalRakshak: Bill of Materials (BOM) & Hardware Specifications

**Competition:** Hackster.io "Sustain the System" (Sponsored by Nordic Semiconductor)  
**Project:** JalRakshak — Predict the Failure. Protect the Water.  
**Role:** Primary Edge-AI Controller, Sensing Abstraction & AquaMesh BLE Network

---

## 1. Primary Processing & Wireless Controller (Core Platform)

| Item | Component / Model | Quantity | Purpose / Role in Architecture | Status | Requirement |
| :---: | :--- | :---: | :--- | :---: | :---: |
| **1** | **Nordic Semiconductor nRF54LM20 DK** | 1 | **Central Edge-AI Controller & AquaMesh Node:** High-performance ARM Cortex-M33 application core with hardware FPU and dedicated Axon NPU target. *Note: The nRF54LM20 DK supports the nRF54LM20A and nRF54LM20B. JalRakshak targets the nRF54LM20B configuration (`nrf54lm20dk/nrf54lm20b/cpuapp`) for Edge AI development using its integrated Axon NPU.* Runs on-chip time-series signal windowing, feature extraction, TinyML health inference, and Bluetooth Mesh 2.4 GHz communications. | Planned / Application Platform | **Required** |

---

## 2. Sensor Instrumentation (Edge Vibration, Power & Fluid Dynamics)

| Item | Sensor / Module | Interface | Quantity | Target Parameter & Engineering Justification | Status | Requirement |
| :---: | :--- | :---: | :---: | :--- | :---: | :---: |
| **2** | **ADXL355 / LIS3DH 3-Axis Digital Accelerometer** | SPI / I2C | 1 | **High-Frequency Vibration & Bearing Shock:** Captures pump casing vibration signatures across 100 Hz – 1 kHz. Used for RMS, peak crest factor, and spectral band energy anomaly detection. | Prototype Planned | Required for physical sensing |
| **3** | **SCT-013-030 Non-Invasive AC Current Sensor (or INA219/INA226 for DC solar pumps)** | SAADC / I2C | 1 | **Motor Load & Irregularity Sensing:** Monitors active phase current, current harmonics, and uncharacteristic load surges indicative of impellor cavitation or motor winding distress. | Prototype Planned | Required for physical sensing |
| **4** | **DS18B20 Waterproof Digital Temp Sensor (or PT100/MAX31865)** | 1-Wire / SPI | 1 | **Bearing Housing & Motor Stator Temperature:** Tracks absolute operating temperature and $\Delta T / \Delta t$ thermal ramp-up rates during degradation phases. | Prototype Planned | Required for physical sensing |
| **5** | **YF-S201 / G1/2 Hall Effect Flow Sensor** | GPIO Pulse Counter | 1 | **Hydraulic Flow Rate:** Quantifies hydraulic discharge in L/min to calculate volumetric efficiency ($Q_{\text{actual}} / Q_{\text{nominal}}$) and identify head loss. | Prototype Planned | Required for physical sensing |
| **6** | **Ultrasonic / Hydrostatic Tank Level Sensor (JSN-SR04T)** | UART / GPIO Echo | 1 | **Storage Buffer & Recovery Rate:** Measures tank water level recovery slope ($dh/dt$) to correlate pump degradation with community water-access risk. | Prototype Planned | Optional / Secondary node |

---

## 3. Power Supply & Auxiliary Infrastructure

| Item | Component | Specification | Quantity | Role | Status | Requirement |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: |
| **7** | **LiFePO4 / Li-Ion Battery Pack with Solar BMS** | 3.7V - 5V Regulated (TP4056 or PMIC) | 1 | Off-grid power supply for rural community borewells. | Prototype Planned | Required for off-grid |
| **8** | **Industrial IP65/IP67 Enclosure** | Polycarbonate with cable glands | 1 | Weatherproof protection against pump manifold washdown. | Prototype Planned | Optional |
| **9** | **Signal Conditioning & Interface Shield** | Custom / Protoboard PCB | 1 | Passive RC filtering and terminal blocks for nRF54LM20 DK headers. | Prototype Planned | Optional |

---
*Note: JalRakshak is a prototype research project designed for low-power edge predictive maintenance in water infrastructure.*

# JalRakshak: Bill of Materials (BOM) & Hardware Specifications

**Competition Project:** Hackster.io "Sustain the System" (Sponsored by Nordic Semiconductor)  
**Project:** JalRakshak — Predict the Failure. Protect the Water.  
**Hardware Node Role:** Edge-AI Vibration, Current, Temperature & Flow Monitoring Node with AquaMesh BLE Connectivity.

---

## 1. Primary Processing & Wireless Controller (Core Requirement)

| Item | Component / Model | Quantity | Purpose / Role in Architecture | Status |
| :--- | :--- | :---: | :--- | :--- |
| **1** | **Nordic Semiconductor nRF54LM20 DK** | 1 | **Central Edge-AI Controller & AquaMesh Node:** High-performance dual-core ARM Cortex-M33, 2.4 GHz multiprotocol radio supporting Bluetooth Low Energy & Bluetooth Mesh. Runs local feature extraction, TinyML inference, composite water reliability scoring, and secure telemetry transmission. | **Selected / Primary Platform** |

---

## 2. Sensor Instrumentation (Edge Vibration, Power & Fluid Dynamics)

| Item | Sensor / Module | Interface | Quantity | Target Parameter & Engineering Justification |
| :--- | :--- | :---: | :---: | :--- |
| **2** | **ADXL355 / LIS3DH 3-Axis Digital Accelerometer** | SPI / I2C | 1 | **High-Frequency Vibration & Bearing Shock:** Captures pump casing vibration signatures across 100 Hz – 1 kHz. Used for RMS, peak crest factor, and spectral band energy anomaly detection. |
| **3** | **SCT-013-030 Non-Invasive AC Current Sensor (or INA219/INA226 for DC solar pumps)** | Analog ADC / I2C | 1 | **Motor Load & Irregularity Sensing:** Monitors active phase current, current harmonics, and uncharacteristic load surges indicative of impellor cavitation or motor winding distress. |
| **4** | **DS18B20 Waterproof Digital Temp Sensor (or PT100/MAX31865)** | 1-Wire / SPI | 1 | **Bearing Housing & Motor Stator Temperature:** Tracks absolute operating temperature and $\Delta T / \Delta t$ thermal ramp-up rates during degradation phases. |
| **5** | **YF-S201 / G1/2 Hall Effect Flow Sensor** | GPIO Pulse Counter / Timer | 1 | **Hydraulic Flow Rate:** Quantifies hydraulic discharge in L/min to calculate volumetric efficiency ($Q_{\text{actual}} / Q_{\text{nominal}}$) and identify head loss. |
| **6** | **Ultrasonic / Hydrostatic Tank Level Sensor (JSN-SR04T)** | UART / GPIO Echo | 1 | **Storage Buffer & Recovery Rate:** Measures tank water level recovery slope ($dh/dt$) to correlate pump degradation with community water-access risk. |

---

## 3. Power Supply & Auxiliary Infrastructure

| Item | Component | Specification | Quantity | Role |
| :--- | :--- | :--- | :---: | :--- |
| **7** | **LiFePO4 / Li-Ion Battery Pack with Solar Charging BMS** | 3.7V - 5V Regulated (TP4056 or Nordic PMIC) | 1 | Offline / remote off-grid operation for rural and community water points. |
| **8** | **Industrial Enclosure (IP65/IP67 rated)** | Polycarbonate with cable glands | 1 | Harsh outdoor environmental protection near pump manifolds. |
| **9** | **Signal Conditioning & Interface Shield** | Custom / Protoboard PCB | 1 | Level shifting, RC anti-aliasing filtering, and secure mechanical terminal block connections to nRF54LM20 DK GPIO headers. |

---

## 4. Connectivity & AquaMesh Architecture

The Nordic nRF54LM20 DK functions as an autonomous edge node:
1. **Local Sensing:** High-speed sampling via hardware timer interrupts, DMA, and on-board ADC/SPI.
2. **On-Device Inference:** Windowed feature extraction and quantized neural network/anomaly model.
3. **AquaMesh Network:** Broadcaster/Relay node broadcasting state to neighbouring pumps, tanks, and roaming technician handheld gateways (Offline-First sync).

---
*Note: JalRakshak is a prototype research project designed for low-power edge predictive maintenance in water infrastructure.*

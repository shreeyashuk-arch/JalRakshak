# Hardware Specifications & Pinout Interface

**Primary Development Platform:** Nordic Semiconductor nRF54LM20 DK  
**Target Configuration:** `nrf54lm20dk/nrf54lm20b/cpuapp`

---

## 1. Controller Specifications: Nordic nRF54LM20 DK

- **Application Processor:** Dual-core ARM Cortex-M33 running at up to 128 MHz with single-cycle DSP instructions and IEEE 754 single-precision FPU.
- **Dedicated Neural Processing Unit (NPU):** Axon NPU target for INT8 quantized TinyML inference (`nrf54lm20b`).
- **Memory:** High-density on-chip non-volatile memory and ultra-low-leakage RAM.
- **Radio Protocol Support:** Bluetooth Low Energy 5.4, Bluetooth Mesh v1.1, 2.4 GHz proprietary, Thread, and Matter.
- **Supply Voltage:** 1.8V to 3.6V (optimized for LiFePO4 batteries and solar energy harvesting).

---

## 2. Sensor Hardware Interface Mapping

| Sensor | Parameter | Protocol / Interface | nRF54LM20 DK Connector Header |
| :--- | :--- | :--- | :--- |
| **ADXL355 / LIS3DH** | 3-Axis High-G Vibration | High-Speed SPI (or I2C) | Arduino Shield Header / Dedicated SPI lines |
| **SCT-013-030** | AC Motor Current (RMS) | Analog SAADC (with DC bias offset) | Analog In (AIN0 / AIN1) |
| **DS18B20** | Casing & Stator Temp | 1-Wire Digital (Open-Drain) | Digital GPIO with 4.7k pull-up |
| **YF-S201** | Water Flow Rate (LPM) | Digital Pulse Counter | Hardware Counter / Timer capture GPIO |
| **JSN-SR04T** | Tank Water Level | UART / Echo Pulse | UART RX/TX or Timer capture |

---

## 3. Power Architecture & Off-Grid Deployment

For rural off-grid community borewells, the nRF54LM20 DK is paired with:
- **LiFePO4 3.2V Battery Pack (2000 mAh):** Extremely high thermal stability and multi-year cycle life.
- **5W / 6V Solar Panel with PMIC:** Keeps the battery topped up using daytime solar radiance.
- **Ultra-Low-Power Sleep Modes:** Zephyr power management (`CONFIG_PM=y`) places the Cortex-M33 into low-power retention between 100 Hz sampling windows, achieving an average power budget in the low tens of microamps.

# JalRakshak: Technical Development Roadmap

**Project:** JalRakshak — Predict the Failure. Protect the Water.  
**Hardware Platform:** Nordic Semiconductor nRF54LM20 DK  
**Contest:** Hackster.io "Sustain the System" (Nordic Semiconductor)

This roadmap outlines the path from the current working initial prototype to full physical bench testing and municipal pilot validation.

---

## Phase 1: Architecture, Simulation & Prototype Baseline (COMPLETED / CURRENT MILESTONE)
- [x] End-to-end repository structure, documentation, and boundary definitions.
- [x] Zephyr RTOS firmware project structure targeting `nrf54lm20dk/nrf54lm20b/cpuapp`.
- [x] Sensor manager abstraction with simulated multi-fault generation in C.
- [x] Edge-AI feature extraction engine (vibration RMS, crest factor, current RMS, thermal climb, flow efficiency).
- [x] Failure-to-impact decision logic and prototype composite *Water Reliability Score*.
- [x] AquaMesh Bluetooth Mesh payload protocol and offline telemetry ring-buffer.
- [x] Synthetic time-series dataset generator (2,000 samples) and baseline model training.
- [x] FastAPI REST backend with SQLite persistence and seeded multi-asset fleet.
- [x] React 18 + TypeScript + Tailwind CSS real-time dashboard with fault injection controls.
- [x] Comprehensive test suites (Backend, Simulation, Edge AI) passing 100%.

---

## Phase 2: Physical Hardware Integration & Sensor Bench Testing (UPCOMING)
- [ ] Receive physical **Nordic Semiconductor nRF54LM20 DK**.
- [ ] Connect ADXL355 3-axis accelerometer over SPI (`CONFIG_SPI=y`).
- [ ] Calibrate SCT-013 current sensor with nRF54LM20 Successive Approximation ADC (SAADC).
- [ ] Wire DS18B20 1-Wire temperature sensor to bearing housing mount.
- [ ] Integrate YF-S201 pulse flow sensor with Zephyr Counter hardware timer.
- [ ] Measure physical baseline vibration and electrical power consumption in idle/sensing states.

---

## Phase 3: Axon NPU Deployment & Quantized TinyML
- [ ] Convert trained model to TensorFlow Lite for Microcontrollers (TFLM) INT8 quantized format.
- [ ] Leverage the nRF54LM20B's integrated Axon NPU using the Nordic Edge AI toolchain.
- [ ] Profile inference latency (target: < 15 ms per 2-second audio/vibration window) and microamp power draw.

---

## Phase 4: AquaMesh Field Deployment & Gateway Testing
- [ ] Provision 3+ physical nRF54LM20 DK nodes onto an active Bluetooth Mesh v1.1 network.
- [ ] Validate relay hops from borehole pump station to community storage tank node.
- [ ] Build technician mobile app (React Native / Nordic nRF Connect Mobile SDK) for BLE data mule synchronization.
- [ ] Conduct field pilot testing at a community borehole pump site.

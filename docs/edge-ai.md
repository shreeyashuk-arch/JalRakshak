# JalRakshak Edge AI Architecture & Pipeline

**Target Hardware:** Nordic Semiconductor nRF54LM20 DK (`nrf54lm20dk/nrf54lm20b/cpuapp`)  
**Processing Core:** ARM Cortex-M33 with FPU & Axon Neural Processing Unit (NPU)

---

## 1. Edge AI Philosophy

Community water pumps operate in electrically noisy, remote environments. Streaming high-frequency raw vibration audio/acceleration over cellular or satellite is technically infeasible and power-prohibitive.

JalRakshak executes **all signal conditioning, windowing, feature extraction, and anomaly classification on-device** at the nRF54LM20 DK node. Only lightweight, structured telemetry messages (health percentage, state, and water reliability score) are transmitted across AquaMesh.

---

## 2. Feature Extraction Mathematics

For each 2-second time window (sampled at 100 Hz):

1. **Vibration RMS ($V_{\text{RMS}}$):**
   $$V_{\text{RMS}} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} v_i^2}$$
   Quantifies overall kinetic energy and unbalance in the pump rotating assembly.

2. **Vibration Crest Factor ($CF$):**
   $$CF = \frac{\max(|v_i|)}{V_{\text{RMS}}}$$
   Detects sharp, impulsive shock waves indicative of bearing race flaking or ball spalling.

3. **Current RMS ($I_{\text{RMS}}$):**
   Monitors effective electrical motor loading and phase imbalance.

4. **Thermal Rate of Change ($\Delta T / \Delta t$):**
   Identifies friction-induced heat ramp-up prior to critical bearing seizure.

5. **Flow Efficiency ($\eta_Q$):**
   $$\eta_Q = \frac{Q_{\text{actual}}}{Q_{\text{nominal}}}$$
   Correlates mechanical degradation directly to fluid delivery capacity.

---

## 3. Dataset & Model Training Summary

- **Dataset:** 2,000 synthetic windows generated using `edge_ai/datasets/synthetic_generator.py`.
- **Target States:**
  - `HEALTHY` (State 0)
  - `DEGRADING` (State 1)
  - `CRITICAL` (State 2)
- **Model:** Random Forest Classifier (20 estimators, max depth 6) exported to `edge_ai/models/baseline_pump_classifier.joblib`.
- **Reported Accuracy:** Measured on synthetic hold-out test set (see `edge_ai/evaluation/evaluation_metrics.json`).

> [!NOTE]
> *Scientific Honesty Rule:* This baseline model was trained and evaluated on synthetic physical signals. Field deployment will incorporate empirical vibration data gathered from physical nRF54LM20 DK testing.

# Solution Architecture: The JalRakshak Predictive Water Reliability Network

**System:** JalRakshak — Predict the Failure. Protect the Water.  
**Hardware Core:** Nordic Semiconductor nRF54LM20 DK

---

## 1. Solution Overview

JalRakshak transforms water infrastructure monitoring from **isolated threshold alarms** into an **Edge-AI powered predictive water reliability network**.

```
  Decentralized Asset
 (Borehole / Solar Pump)
          │
          ▼
 [ Nordic nRF54LM20 DK ] ──> Local On-Device Feature Extraction & TinyML
          │                  (Zero dependence on permanent cloud connection)
          │
          ▼
   [ AquaMesh BLE ] ───────> Local Peer-to-Peer Mesh (Pump ↔ Tank)
          │
          ▼
 [ Offline Data Mule ] ────> Service technician smartphone / handheld gateway
          │
          ▼
 [ Water Reliability ] ────> Translates machine degradation into water-access risk:
   Composite Engine          WRS (0-100), Failure Window, Maintenance-by-Opportunity
```

---

## 2. Key Pillars of the Solution

### Pillar 1: True Edge Autonomy on the nRF54LM20 DK
By running signal windowing, RMS calculation, spectral crest factor extraction, and state classification on the nRF54LM20's ARM Cortex-M33 application core (and targeting the Axon NPU), JalRakshak operates completely offline. No expensive cellular data plans or fragile satellite uplinks are required at each pump.

### Pillar 2: AquaMesh Local Wireless Network
Pumps and storage tanks coordinate directly over low-power Bluetooth Mesh v1.1. When a pump begins to degrade, downstream tanks receive early warning to conserve storage reserves.

### Pillar 3: Failure-to-Impact Predictive Engine
The system does not just output abstract raw millivolts or acceleration numbers. It computes an explainable metric:
- **What is degrading?** *(Bearing race defect detected)*
- **What is the community impact?** *(Tank recovery time delayed by +14 minutes)*
- **How urgent is the action?** *(Maintenance Window: 18–30 operating hours)*
- **What should be inspected?** *(Inspect bearing lubrication & verify intake condition)*

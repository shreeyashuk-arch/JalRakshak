# JalRakshak Simulation Engine

**Predict the Failure. Protect the Water.**

This module provides the physical time-series signal generation engine used for reproducible demonstration and algorithm verification before physical transducers are wired.

---

## 1. Simulated Fault Modes

| Mode | Simulated Physical Behavior | Key Sensor Signatures |
| :--- | :--- | :--- |
| `NORMAL` | Smooth motor rotation and steady pumping | Vibration ~1.0g RMS, Current ~4.2A, Temp ~42°C, Flow ~85 LPM |
| `BEARING_DEGRADATION` | Bearing race defect, ball spalling | High-frequency vibration spikes (+38%), temperature rise (+14°C), flow drop (-12%) |
| `OVERLOAD` | Mechanical binding, excessive head pressure | Electrical current surge (+3.2A), winding temperature ramp (+20°C) |
| `LOW_FLOW` / `CAVITATION` | Blocked intake screen, choked suction pipe | Severe volumetric flow collapse (-60%), cavitation fluid shock waves |
| `OVERHEATING` | Insufficient motor cooling or lubricant breakdown | Motor stator temperature ramp exceeding critical threshold (+28°C) |

---

## 2. Running Simulation Tests

```bash
python -m pytest simulation/tests/test_simulation.py -v
```

## 3. Interactive Execution

```bash
python -m simulation.generators.simulation_engine
```
Generates time-series samples and logs output values.

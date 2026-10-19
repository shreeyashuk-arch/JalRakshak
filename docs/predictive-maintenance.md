# Failure-to-Impact Predictive Maintenance & Water Reliability Formulation

**Tagline:** Predict the Failure. Protect the Water.  
**System:** JalRakshak Composite Reliability Engine

---

## 1. The Core Differentiator: Failure-to-Impact

Conventional predictive maintenance stops at equipment condition:
- *"Bearing vibration is high."*
- *"Current draw is anomalous."*

**JalRakshak connects equipment degradation directly to human water access:**
- *"Bearing vibration is +38% above baseline."*
- *"Flow efficiency has dropped to 88%."*
- *"Storage tank recovery time is delayed by +14 minutes."*
- *"Predicted Impact: Community reservoir buffer depletion within 18–30 operating hours."*
- *"Maintenance Priority: HIGH PRIORITY (Maintenance opportunity detected near Sector 1 route)."*

---

## 2. Mathematical Formulation: Water Reliability Score (WRS)

The **JalRakshak Water Reliability Score** is an experimental composite index ranging from **0 to 100**:

$$\text{WRS} = w_p \cdot H_{\text{pump}} + w_f \cdot (\eta_Q \cdot 100) + w_t \cdot (R_{\text{tank}} \cdot 100) + w_s \cdot (S_{\text{op}} \cdot 100)$$

Where:
- $H_{\text{pump}}$: Pump Health Score (0 – 100%), calculated from on-device vibration, current, and temperature anomaly scores.
- $\eta_Q$: Flow Delivery Efficiency relative to nominal rating ($\min(1.2, Q_{\text{actual}} / Q_{\text{nominal}})$).
- $R_{\text{tank}}$: Tank recovery rate factor (0.0 to 1.0, based on fill-rate slope).
- $S_{\text{op}}$: Electrical and thermal operating stability index (0.0 to 1.0).

### Weighting Coefficients:
$$\begin{aligned}
w_p &= 0.40 \quad (\text{Mechanical health of rotating assets}) \\
w_f &= 0.30 \quad (\text{Volumetric fluid delivery}) \\
w_t &= 0.20 \quad (\text{Downstream community storage reserve}) \\
w_s &= 0.10 \quad (\text{Electrical \& thermal stability}) \\
\sum w &= 1.00
\end{aligned}$$

---

## 3. Maintenance Ranking & Priority Rules

| WRS Range | Pump Health | Risk Level | Maintenance Priority | Estimated Maintenance Window | Action |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **85 – 100** | $\ge 80\%$ | **LOW** | **NORMAL** | 300 – 600 hours | Routine scheduled observation. |
| **70 – 84** | $\ge 65\%$ | **LOW** | **MONITOR** | 100 – 200 hours | Mild baseline drift. Maintain telemetry observation. |
| **55 – 69** | $\ge 50\%$ | **MEDIUM** | **INSPECT SOON** | 36 – 72 hours | Degradation active. Lubricate bearings, check couplings. |
| **35 – 54** | $\ge 30\%$ | **HIGH** | **HIGH PRIORITY**| 18 – 30 hours | Potential water outage. Overhaul pump bearing & intake. |
| **0 – 34** | $< 30\%$ | **CRITICAL**| **CRITICAL** | 2 – 8 hours | Immediate shutdown risk. Urgent technician deployment. |

---
*Disclaimer: This is a prototype composite metric developed for JalRakshak and is not an industry-standard reliability index.*

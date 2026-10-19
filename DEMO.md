# JalRakshak: Step-by-Step Demonstration Guide

**Project:** JalRakshak — Predict the Failure. Protect the Water.  
**Competition:** Hackster.io "Sustain the System" (Nordic Semiconductor)

This guide walks through reproducing the core predictive maintenance and failure-to-impact demo.

---

## 1. Quick Start Commands

### Terminal 1: Backend
```bash
# From repository root:
python -m uvicorn backend.app.main:app --port 8000
```
API Documentation will be live at: `http://localhost:8000/docs`

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 2. Walkthrough Scenario: Bearing Degradation Fault Injection

### Step 1: Baseline Healthy State
1. Open the dashboard at `http://localhost:5173`.
2. Notice the **Water Reliability Score**: ~96/100 (HEALTHY).
3. Monitored assets are running within normal baseline vibration (~1.0g RMS), temperature (~42°C), and nominal flow.

### Step 2: Injecting Bearing Degradation
1. Click on the **Demo Simulation** tab.
2. Select **Pump-03** (Centrifugal Booster Pump C).
3. Click the button: **"1. Bearing Degradation"**.
4. The simulation engine injects high-frequency vibration shock waves (+38%), temperature rise (+14°C), and flow efficiency loss into the live SQLite database.

### Step 3: Observing Edge-AI Detection
1. Switch to the **Impact Prediction** tab.
2. Observe the real-time calculations:
   - **Pump Health:** Drops from 96% down to **54%**.
   - **Observed Deviations:**
     - Vibration: +38% from nominal baseline
     - Current: +9% irregularity detected
     - Flow efficiency: -12% drop
     - Tank recovery time: +14 minutes delay
3. **Failure-to-Impact Prediction:**
   - **Water Reliability Score:** Decreases to **58.2/100**.
   - **System Risk:** Elevates to **HIGH**.
   - **Maintenance Priority:** Escalates to **HIGH PRIORITY**.
   - **Estimated Maintenance Window:** Calculated at **18–30 operating hours**.
   - **Recommended Action:** *"Inspect pump bearing/coupling and verify intake condition."*

### Step 4: Resetting the System
1. Go back to the **Demo Simulation** tab.
2. Click **"Reset Simulation to Healthy Baseline"**.
3. All telemetry curves and reliability scores immediately return to nominal state.

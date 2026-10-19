# JalRakshak Frontend Dashboard

**Predict the Failure. Protect the Water.**

This module implements the responsive operator and technician dashboard built with **React 18**, **TypeScript**, and **Tailwind CSS**.

---

## 1. Quick Start

### Installation
```bash
cd frontend
npm install
```

### Development Server
```bash
npm run dev
```
Open `http://localhost:5173` in your browser. Telemetry requests to `/api/*` are automatically proxied to the backend at `http://localhost:8000`.

### Production Build
```bash
npm run build
```
Builds optimized production assets to `frontend/dist/`.

---

## 2. Dashboard Sections

1. **Overview:** Top-level KPIs: composite Water Reliability Score, active assets count, assets at risk, and technician maintenance opportunities.
2. **Asset Fleet:** Multi-asset status table sortable by water-access risk.
3. **Failure-to-Impact Prediction:** Visual inspection of selected pump, observed sensor deviations, and algorithmic recommendations.
4. **AquaMesh BLE:** Network status, relay hop counts, signal strengths (RSSI), and synchronization status.
5. **Demo Simulation:** Single-click fault injection (*Bearing Degradation*, *Motor Overload*, *Blocked Intake*) and reset controls.

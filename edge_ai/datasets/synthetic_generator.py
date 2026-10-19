import os
import json
import numpy as np

def generate_synthetic_dataset(samples_per_class=400, sample_rate_hz=100, window_sec=2.0, random_seed=42):
    """
    Generates realistic, physically-grounded synthetic time-series data for pump monitoring.
    
    Fault modes simulated:
    1. HEALTHY: Baseline vibration (~1.0g RMS with motor rotation harmonics), nominal current (~4.2A), ~42C, 85 LPM flow.
    2. BEARING_DEGRADATION: Elevated vibration harmonics, high crest factor, temperature creep.
    3. OVERLOAD: Electrical motor current surge, resistive heating ramp, modest mechanical oscillation.
    4. LOW_FLOW: Severe drop in flow rate, cavitation transient pulses, tank depletion impact.
    5. OVERHEATING: Thermal drift towards critical threshold with viscosity breakdown.
    
    NOTE: These results are based on synthetic prototype data and do not represent field performance.
    """
    np.random.seed(random_seed)
    n_pts = int(sample_rate_hz * window_sec) # 200 points per window
    t = np.linspace(0, window_sec, n_pts)

    classes = ["HEALTHY", "BEARING_DEGRADATION", "OVERLOAD", "LOW_FLOW", "OVERHEATING"]
    labels_map = {"HEALTHY": 0, "BEARING_DEGRADATION": 1, "OVERLOAD": 2, "LOW_FLOW": 3, "OVERHEATING": 4}
    
    # State severity maps for 3-class target: 0=HEALTHY, 1=DEGRADING, 2=CRITICAL
    state_map = {
        "HEALTHY": 0,               # HEALTHY
        "BEARING_DEGRADATION": 1,   # DEGRADING
        "OVERLOAD": 1,              # DEGRADING
        "LOW_FLOW": 2,              # CRITICAL
        "OVERHEATING": 2            # CRITICAL
    }

    dataset = []

    for c in classes:
        for i in range(samples_per_class):
            noise = np.random.normal(0, 0.05, n_pts)
            
            if c == "HEALTHY":
                # 50 Hz line / 25 Hz rotational harmonic
                vib = 1.0 + 0.15 * np.sin(2 * np.pi * 25 * t) + noise
                current = 4.2 + 0.1 * np.sin(2 * np.pi * 50 * t) + np.random.normal(0, 0.04, n_pts)
                temp = 42.0 + np.random.normal(0, 0.5)
                flow = 85.0 + np.random.normal(0, 1.2)
                
            elif c == "BEARING_DEGRADATION":
                # High frequency shock impulses & 3x harmonics
                impulses = 0.6 * np.sin(2 * np.pi * 120 * t) * (np.random.rand(n_pts) > 0.85)
                vib = 1.45 + 0.4 * np.sin(2 * np.pi * 25 * t) + impulses + noise * 2.0
                current = 4.4 + 0.15 * np.sin(2 * np.pi * 50 * t) + np.random.normal(0, 0.05, n_pts)
                temp = 51.5 + np.random.normal(0, 0.8)
                flow = 79.0 + np.random.normal(0, 1.5)
                
            elif c == "OVERLOAD":
                vib = 1.25 + 0.25 * np.sin(2 * np.pi * 25 * t) + noise * 1.2
                current = 6.8 + 0.3 * np.sin(2 * np.pi * 50 * t) + np.random.normal(0, 0.1, n_pts)
                temp = 58.0 + np.random.normal(0, 1.0)
                flow = 82.0 + np.random.normal(0, 1.5)
                
            elif c == "LOW_FLOW":
                vib = 1.35 + 0.3 * np.sin(2 * np.pi * 15 * t) + noise * 1.5 # Fluid turbulence / cavitation
                current = 3.6 + np.random.normal(0, 0.08, n_pts) # Low hydraulic load
                temp = 44.0 + np.random.normal(0, 0.6)
                flow = 28.0 + np.random.normal(0, 2.5) # Choked intake
                
            elif c == "OVERHEATING":
                vib = 1.20 + noise
                current = 4.9 + np.random.normal(0, 0.1, n_pts)
                temp = 68.0 + np.random.normal(0, 1.5) # Severe thermal breakdown
                flow = 74.0 + np.random.normal(0, 1.8)

            record = {
                "class_name": c,
                "fault_label": labels_map[c],
                "health_state": state_map[c], # 0: Healthy, 1: Degrading, 2: Critical
                "vibration_series": vib.tolist(),
                "current_series": current.tolist(),
                "temp_mean": float(temp),
                "flow_mean": float(flow)
            }
            dataset.append(record)

    out_dir = os.path.join(os.path.dirname(__file__), "..", "datasets")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "synthetic_pump_dataset.json")
    with open(out_file, "w") as f:
        json.dump(dataset, f)
    
    print(f"[Dataset] Generated {len(dataset)} samples across {len(classes)} classes -> {out_file}")
    return out_file

if __name__ == "__main__":
    generate_synthetic_dataset()

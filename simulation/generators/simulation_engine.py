import time
import math
import json
import random

API_BASE_URL = "http://localhost:8000/api"

class SimulationEngine:
    """
    Simulation Engine generating time-series data for:
    - NORMAL
    - BEARING_DEGRADATION
    - OVERLOAD
    - LOW_FLOW
    - OVERHEATING
    
    Controls:
    - Fault type
    - Severity (0.0 to 1.0)
    - Noise level
    - Pump load
    
    DISCLAIMER: Prototype simulation. Does not represent exact physical behavior.
    """
    FAULT_MODES = ["NORMAL", "BEARING_DEGRADATION", "OVERLOAD", "LOW_FLOW", "OVERHEATING"]

    def __init__(self, target_asset="PUMP-03", base_flow=85.0, base_current=4.2, base_temp=42.0):
        self.target_asset = target_asset
        self.base_flow = base_flow
        self.base_current = base_current
        self.base_temp = base_temp
        self.current_fault = "NORMAL"
        self.severity = 0.0
        self.ticks = 0

    def set_fault(self, fault_name: str, severity: float = 0.65):
        if fault_name not in self.FAULT_MODES:
            raise ValueError(f"Unknown fault: {fault_name}")
        self.current_fault = fault_name
        self.severity = max(0.0, min(1.0, severity))
        print(f"[SimulationEngine] Set {self.target_asset} -> {self.current_fault} (severity={self.severity:.2f})")

    def generate_next_sample(self):
        self.ticks += 1
        t = self.ticks * 0.1
        noise = (random.random() - 0.5) * 0.05

        vib = 1.0 + 0.08 * math.sin(t) + noise
        current = self.base_current + 0.05 * math.sin(t * 1.5) + noise * 0.5
        temp = self.base_temp + (random.random() - 0.5) * 0.2
        flow = self.base_flow + (random.random() - 0.5) * 0.5

        if self.current_fault == "BEARING_DEGRADATION":
            vib += (0.65 * self.severity) + (0.2 * self.severity * math.sin(t * 5.0))
            temp += (14.0 * self.severity)
            flow -= (9.0 * self.severity)
        elif self.current_fault == "OVERLOAD":
            current += (3.2 * self.severity)
            temp += (20.0 * self.severity)
            vib += (0.25 * self.severity)
        elif self.current_fault == "LOW_FLOW":
            flow -= (55.0 * self.severity)
            vib += (0.35 * self.severity) # cavitation noise
            current -= (0.7 * self.severity)
        elif self.current_fault == "OVERHEATING":
            temp += (28.0 * self.severity)
            vib += (0.20 * self.severity)

        return {
            "timestamp_tick": self.ticks,
            "fault_mode": self.current_fault,
            "severity": self.severity,
            "vibration_rms": round(vib, 3),
            "motor_current": round(current, 2),
            "temperature": round(temp, 1),
            "flow_rate": round(max(0.0, flow), 1)
        }

if __name__ == "__main__":
    sim = SimulationEngine()
    print("Normal reading:", sim.generate_next_sample())
    sim.set_fault("BEARING_DEGRADATION", 0.70)
    print("Degraded reading:", sim.generate_next_sample())

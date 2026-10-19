import pytest
from simulation.generators.simulation_engine import SimulationEngine

def test_simulation_fault_modes():
    sim = SimulationEngine(target_asset="PUMP-03")
    
    # 1. Normal mode
    s_normal = sim.generate_next_sample()
    assert s_normal["fault_mode"] == "NORMAL"
    assert 0.8 < s_normal["vibration_rms"] < 1.2
    assert 80.0 < s_normal["flow_rate"] < 90.0

    # 2. Bearing degradation
    sim.set_fault("BEARING_DEGRADATION", severity=0.8)
    s_bearing = sim.generate_next_sample()
    assert s_bearing["vibration_rms"] > 1.3
    assert s_bearing["temperature"] > 45.0

    # 3. Overload
    sim.set_fault("OVERLOAD", severity=0.85)
    s_overload = sim.generate_next_sample()
    assert s_overload["motor_current"] > 5.5

    # 4. Low flow
    sim.set_fault("LOW_FLOW", severity=0.9)
    s_lowflow = sim.generate_next_sample()
    assert s_lowflow["flow_rate"] < 45.0

    # 5. Overheating
    sim.set_fault("OVERHEATING", severity=0.8)
    s_heat = sim.generate_next_sample()
    assert s_heat["temperature"] > 55.0

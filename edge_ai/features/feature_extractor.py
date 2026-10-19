import numpy as np

def extract_features_from_sample(vib_series, current_series, temp_val, flow_val):
    """
    Extracts time-series features suitable for lightweight Edge-AI inference:
    1. Vibration RMS
    2. Vibration Variance
    3. Vibration Peak (Max absolute value)
    4. Vibration Crest Factor (Peak / RMS)
    5. Current RMS
    6. Current Variance
    7. Temperature (Celsius)
    8. Flow Rate (LPM)
    9. Flow Efficiency (Ratio of nominal 85 LPM)
    """
    v_arr = np.array(vib_series, dtype=np.float32)
    c_arr = np.array(current_series, dtype=np.float32)

    vib_rms = float(np.sqrt(np.mean(v_arr ** 2)))
    vib_var = float(np.var(v_arr))
    vib_peak = float(np.max(np.abs(v_arr)))
    vib_crest = float(vib_peak / vib_rms) if vib_rms > 1e-4 else 1.0

    current_rms = float(np.sqrt(np.mean(c_arr ** 2)))
    current_var = float(np.var(c_arr))

    flow_eff = float(flow_val / 85.0)

    return [
        vib_rms,
        vib_var,
        vib_peak,
        vib_crest,
        current_rms,
        current_var,
        float(temp_val),
        float(flow_val),
        flow_eff
    ]

FEATURE_NAMES = [
    "vibration_rms",
    "vibration_var",
    "vibration_peak",
    "vibration_crest_factor",
    "current_rms",
    "current_var",
    "temperature",
    "flow_rate",
    "flow_efficiency"
]

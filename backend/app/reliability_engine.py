from typing import Dict, Any

def compute_water_reliability_score(pump_health: float, flow_efficiency: float, tank_recovery: float, stability: float = 1.0) -> Dict[str, Any]:
    """
    Computes the JalRakshak Water Reliability Score (0 - 100).
    
    Mathematical Formulation:
      WRS = w_p * Health + w_f * (Flow_Eff * 100) + w_t * (Tank_Rec * 100) + w_s * (Stability * 100)
    
    Weights:
      w_p = 0.40 (Pump health & mechanical condition)
      w_f = 0.30 (Flow efficiency relative to nominal output)
      w_t = 0.20 (Tank level recovery rate factor)
      w_s = 0.10 (Operating electrical & thermal stability)
      Sum = 1.00
      
    DISCLAIMER:
    "This is a prototype composite metric developed for JalRakshak and is not an industry-standard reliability index."
    """
    p_clamped = max(0.0, min(100.0, float(pump_health)))
    f_clamped = max(0.0, min(1.2, float(flow_efficiency)))
    t_clamped = max(0.0, min(1.0, float(tank_recovery)))
    s_clamped = max(0.0, min(1.0, float(stability)))

    raw_score = (
        (0.40 * p_clamped) +
        (0.30 * f_clamped * 100.0) +
        (0.20 * t_clamped * 100.0) +
        (0.10 * s_clamped * 100.0)
    )

    final_score = round(max(0.0, min(100.0, raw_score)), 1)

    # Determine Failure-to-Impact Risk
    if final_score >= 85.0 and p_clamped >= 80.0:
        risk_level = "LOW"
        maint_priority = "NORMAL"
        est_min_h, est_max_h = 300, 600
        urgency = "ROUTINE"
        rec = "Pump and water delivery within normal parameters. Continue standard routine monitoring."
    elif final_score >= 70.0 and p_clamped >= 65.0:
        risk_level = "LOW"
        maint_priority = "MONITOR"
        est_min_h, est_max_h = 100, 200
        urgency = "ADVISORY"
        rec = "Mild baseline vibration drift detected. Maintain telemetry observation."
    elif final_score >= 55.0 or p_clamped >= 50.0:
        risk_level = "MEDIUM"
        maint_priority = "INSPECT SOON"
        est_min_h, est_max_h = 36, 72
        urgency = "MODERATE"
        rec = "Degradation trend detected. Inspect bearing lubrication and verify pipe coupling tightness."
    elif final_score >= 35.0 or p_clamped >= 30.0:
        risk_level = "HIGH"
        maint_priority = "HIGH PRIORITY"
        est_min_h, est_max_h = 18, 30
        urgency = "HIGH"
        rec = "Potential reduction in water delivery reliability predicted. Inspect pump bearing/coupling and verify intake condition."
    else:
        risk_level = "CRITICAL"
        maint_priority = "CRITICAL"
        est_min_h, est_max_h = 2, 8
        urgency = "IMMEDIATE"
        rec = "CRITICAL: Imminent pump failure will cause immediate water outage. Deploy technician for urgent overhaul."

    return {
        "water_reliability_score": final_score,
        "pump_health": p_clamped,
        "flow_efficiency": round(f_clamped, 2),
        "tank_recovery": round(t_clamped, 2),
        "risk_level": risk_level,
        "maintenance_priority": maint_priority,
        "urgency": urgency,
        "recommended_action": rec,
        "estimated_maintenance_window": f"{est_min_h}–{est_max_h} operating hours",
        "est_window_min_hours": est_min_h,
        "est_window_max_hours": est_max_h,
        "disclaimer": "This is a prototype composite metric developed for JalRakshak and is not an industry-standard reliability index."
    }

#include "pump_health.h"
#include <stdio.h>
#include <string.h>

void pump_health_compute_impact(const ai_inference_result_t *ai_res, float current_tank_recovery, water_impact_assessment_t *out_assessment)
{
    if (!ai_res || !out_assessment) return;

    float p_health = ai_res->health_percentage;
    float flow_eff = ai_res->flow_efficiency;
    float tank_rec = (current_tank_recovery > 1.0f) ? 1.0f : (current_tank_recovery < 0.0f ? 0.0f : current_tank_recovery);

    out_assessment->pump_health_score = p_health;
    out_assessment->flow_efficiency = flow_eff;
    out_assessment->tank_recovery_factor = tank_rec;

    /*
     * JalRakshak Water Reliability Score Formulation:
     * Composite Prototype Index (0 - 100):
     * WRS = (0.45 * Pump_Health) + (0.30 * Flow_Efficiency * 100) + (0.25 * Tank_Recovery * 100)
     * NOTE: This is an experimental prototype metric.
     */
    float wrs = (0.45f * p_health) + (0.30f * flow_eff * 100.0f) + (0.25f * tank_rec * 100.0f);
    if (wrs > 100.0f) wrs = 100.0f;
    if (wrs < 0.0f) wrs = 0.0f;
    out_assessment->water_reliability_score = wrs;

    /* Determine Failure-to-Impact Severity and Priority */
    if (p_health >= 85.0f && wrs >= 85.0f) {
        out_assessment->priority = MAINT_PRIORITY_NORMAL;
        out_assessment->est_maint_window_hours_min = 250;
        out_assessment->est_maint_window_hours_max = 500;
        snprintf(out_assessment->recommendation, sizeof(out_assessment->recommendation),
                 "Normal operation. Routine scheduled inspection.");
    } else if (p_health >= 70.0f && wrs >= 75.0f) {
        out_assessment->priority = MAINT_PRIORITY_MONITOR;
        out_assessment->est_maint_window_hours_min = 100;
        out_assessment->est_maint_window_hours_max = 200;
        snprintf(out_assessment->recommendation, sizeof(out_assessment->recommendation),
                 "Mild vibration drift detected. Monitor telemetry trends.");
    } else if (p_health >= 55.0f || wrs >= 60.0f) {
        out_assessment->priority = MAINT_PRIORITY_INSPECT_SOON;
        out_assessment->est_maint_window_hours_min = 36;
        out_assessment->est_maint_window_hours_max = 72;
        snprintf(out_assessment->recommendation, sizeof(out_assessment->recommendation),
                 "Degradation trend active. Schedule bearing lubrication & coupling check.");
    } else if (p_health >= 40.0f || wrs >= 40.0f) {
        out_assessment->priority = MAINT_PRIORITY_HIGH_PRIORITY;
        out_assessment->est_maint_window_hours_min = 18;
        out_assessment->est_maint_window_hours_max = 30;
        snprintf(out_assessment->recommendation, sizeof(out_assessment->recommendation),
                 "High risk of water supply interruption. Inspect bearing/coupling & intake condition.");
    } else {
        out_assessment->priority = MAINT_PRIORITY_CRITICAL;
        out_assessment->est_maint_window_hours_min = 2;
        out_assessment->est_maint_window_hours_max = 8;
        snprintf(out_assessment->recommendation, sizeof(out_assessment->recommendation),
                 "CRITICAL: Immediate technician intervention required to avoid catastrophic pump seizure.");
    }
}

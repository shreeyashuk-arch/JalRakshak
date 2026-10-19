#include "edge_ai_engine.h"
#include <math.h>

int edge_ai_engine_init(void)
{
    /* On nRF54LM20B: Initialize Axon NPU or CMSIS-NN / TF-Lite Micro runtime */
    return 0;
}

int edge_ai_process_window(const sensor_reading_t *window, uint16_t sample_count, ai_inference_result_t *out_result)
{
    if (!window || sample_count == 0 || !out_result) return -1;

    float sum_vib_sq = 0.0f;
    float peak_vib = 0.0f;
    float sum_current = 0.0f;
    float sum_temp = 0.0f;
    float sum_flow = 0.0f;

    for (uint16_t i = 0; i < sample_count; i++) {
        float v_mag = sqrtf(window[i].vibration_x * window[i].vibration_x +
                            window[i].vibration_y * window[i].vibration_y +
                            window[i].vibration_z * window[i].vibration_z);
        sum_vib_sq += (v_mag * v_mag);
        if (v_mag > peak_vib) peak_vib = v_mag;

        sum_current += window[i].motor_current;
        sum_temp += window[i].temperature;
        sum_flow += window[i].flow_rate;
    }

    float rms_vib = sqrtf(sum_vib_sq / (float)sample_count);
    float crest_factor = (rms_vib > 0.001f) ? (peak_vib / rms_vib) : 1.0f;
    float mean_current = sum_current / (float)sample_count;
    float mean_temp = sum_temp / (float)sample_count;
    float mean_flow = sum_flow / (float)sample_count;
    float flow_eff = mean_flow / 85.0f; /* 85 LPM nominal */
    if (flow_eff > 1.2f) flow_eff = 1.2f;

    out_result->vibration_rms = rms_vib;
    out_result->vibration_crest_factor = crest_factor;
    out_result->current_rms = mean_current;
    out_result->temp_celsius = mean_temp;
    out_result->flow_efficiency = flow_eff;

    /* Embedded Decision Logic / Quantized Model Approximation */
    /* Baseline: rms_vib ~ 1.0g, temp ~ 42C, current ~ 4.2A */
    float vib_penalty = (rms_vib > 1.25f) ? ((rms_vib - 1.25f) * 60.0f) : 0.0f;
    float temp_penalty = (mean_temp > 48.0f) ? ((mean_temp - 48.0f) * 2.0f) : 0.0f;
    float current_penalty = (mean_current > 5.0f) ? ((mean_current - 5.0f) * 15.0f) : 0.0f;
    float flow_penalty = (flow_eff < 0.90f) ? ((0.90f - flow_eff) * 50.0f) : 0.0f;

    float total_penalty = vib_penalty + temp_penalty + current_penalty + flow_penalty;
    float health = 100.0f - total_penalty;
    if (health < 10.0f) health = 10.0f;
    if (health > 100.0f) health = 100.0f;

    out_result->health_percentage = health;
    out_result->anomaly_score = (100.0f - health) / 100.0f;

    if (health >= 85.0f) {
        out_result->predicted_state = HEALTH_STATE_HEALTHY;
    } else if (health >= 55.0f) {
        out_result->predicted_state = HEALTH_STATE_DEGRADING;
    } else {
        out_result->predicted_state = HEALTH_STATE_CRITICAL;
    }

    return 0;
}

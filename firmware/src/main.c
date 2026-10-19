#include <stdio.h>
#include <string.h>
#include "sensor_manager.h"
#include "edge_ai_engine.h"
#include "pump_health.h"
#include "aquamesh.h"
#include "telemetry.h"

#define WINDOW_SIZE 16

int main(void)
{
    printf("==================================================\n");
    printf("  JALRAKSHAK: Edge-AI Water Reliability System    \n");
    printf("  Target: Nordic Semiconductor nRF54LM20 DK       \n");
    printf("  Tagline: Predict the Failure. Protect the Water \n");
    printf("==================================================\n");

    /* Initialize subsystems */
    sensor_manager_init(true);
    edge_ai_engine_init();
    aquamesh_init();
    telemetry_init();

    printf("[System] Initialization complete. Sensor buffer online.\n");

    sensor_reading_t sample_window[WINDOW_SIZE];
    uint16_t sample_idx = 0;
    uint32_t iteration = 0;

    /* Main processing loop */
    while (iteration < 20) {
        sensor_reading_t current_sample;
        sensor_manager_read(&current_sample);
        sample_window[sample_idx++] = current_sample;

        if (sample_idx >= WINDOW_SIZE) {
            sample_idx = 0;
            ai_inference_result_t ai_result;
            edge_ai_process_window(sample_window, WINDOW_SIZE, &ai_result);

            water_impact_assessment_t assessment;
            pump_health_compute_impact(&ai_result, 0.85f, &assessment);

            aquamesh_telemetry_pkt_t pkt = {
                .protocol_version = 1,
                .node_id = 3,
                .node_type = NODE_TYPE_PUMP,
                .health_score = (uint8_t)assessment.pump_health_score,
                .reliability_score = (uint8_t)assessment.water_reliability_score,
                .risk_level = (assessment.priority >= MAINT_PRIORITY_HIGH_PRIORITY) ? 2 : 0,
                .maint_priority = (uint8_t)assessment.priority,
                .vib_rms_milli_g = (uint16_t)(ai_result.vibration_rms * 1000.0f),
                .current_rms_milli_a = (uint16_t)(ai_result.current_rms * 1000.0f),
                .temp_deci_c = (int16_t)(ai_result.temp_celsius * 10.0f),
                .flow_deci_lpm = (uint16_t)(ai_result.flow_efficiency * 850.0f),
                .seq_num = iteration
            };

            aquamesh_publish_telemetry(&pkt);
            telemetry_buffer_packet(&pkt);

            printf("[Edge-AI] Window %u: Health=%u%%, WaterReliability=%u/100, Priority=%d\n",
                   iteration, pkt.health_score, pkt.reliability_score, pkt.maint_priority);
        }
        iteration++;
    }

    printf("[System] Prototype loop demonstration finished successfully.\n");
    return 0;
}

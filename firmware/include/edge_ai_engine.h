#ifndef EDGE_AI_ENGINE_H_
#define EDGE_AI_ENGINE_H_

#include "sensor_manager.h"
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    HEALTH_STATE_HEALTHY = 0,
    HEALTH_STATE_DEGRADING = 1,
    HEALTH_STATE_CRITICAL = 2
} health_state_t;

typedef struct {
    float vibration_rms;
    float vibration_crest_factor;
    float current_rms;
    float temp_celsius;
    float flow_efficiency;  /* Normalized (1.0 = nominal) */
    
    health_state_t predicted_state;
    float anomaly_score;    /* 0.0 (normal) to 1.0 (abnormal) */
    float health_percentage;/* 100.0% down to 0.0% */
} ai_inference_result_t;

int edge_ai_engine_init(void);
int edge_ai_process_window(const sensor_reading_t *window, uint16_t sample_count, ai_inference_result_t *out_result);

#ifdef __cplusplus
}
#endif

#endif /* EDGE_AI_ENGINE_H_ */

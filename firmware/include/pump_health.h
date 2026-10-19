#ifndef PUMP_HEALTH_H_
#define PUMP_HEALTH_H_

#include "edge_ai_engine.h"
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    MAINT_PRIORITY_NORMAL = 0,
    MAINT_PRIORITY_MONITOR = 1,
    MAINT_PRIORITY_INSPECT_SOON = 2,
    MAINT_PRIORITY_HIGH_PRIORITY = 3,
    MAINT_PRIORITY_CRITICAL = 4
} maintenance_priority_t;

typedef struct {
    float pump_health_score;        /* 0 - 100 */
    float flow_efficiency;          /* 0.0 - 1.0 */
    float tank_recovery_factor;     /* 0.0 - 1.0 */
    float water_reliability_score;  /* 0 - 100 prototype metric */
    maintenance_priority_t priority;
    char recommendation[128];
    uint32_t est_maint_window_hours_min;
    uint32_t est_maint_window_hours_max;
} water_impact_assessment_t;

void pump_health_compute_impact(const ai_inference_result_t *ai_res, float current_tank_recovery, water_impact_assessment_t *out_assessment);

#ifdef __cplusplus
}
#endif

#endif /* PUMP_HEALTH_H_ */

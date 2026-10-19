#ifndef SENSOR_MANAGER_H_
#define SENSOR_MANAGER_H_

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    float vibration_x;      /* g */
    float vibration_y;      /* g */
    float vibration_z;      /* g */
    float motor_current;    /* Amperes (RMS) */
    float temperature;      /* Degrees Celsius */
    float flow_rate;        /* Liters per minute */
    float tank_level;       /* Percentage 0.0 - 100.0 */
    uint32_t timestamp_ms;
} sensor_reading_t;

int sensor_manager_init(bool use_simulated_mode);
int sensor_manager_read(sensor_reading_t *out_reading);
void sensor_manager_set_simulation_fault(int fault_type, float severity);

#ifdef __cplusplus
}
#endif

#endif /* SENSOR_MANAGER_H_ */

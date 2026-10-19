#include "sensor_manager.h"
#include <math.h>
#include <string.h>

static bool s_simulated_mode = true;
static int s_fault_type = 0;
static float s_fault_severity = 0.0f;
static uint32_t s_ticks = 0;

int sensor_manager_init(bool use_simulated_mode)
{
    s_simulated_mode = use_simulated_mode;
    s_fault_type = 0;
    s_fault_severity = 0.0f;
    s_ticks = 0;
    return 0;
}

void sensor_manager_set_simulation_fault(int fault_type, float severity)
{
    s_fault_type = fault_type;
    s_fault_severity = (severity < 0.0f) ? 0.0f : (severity > 1.0f ? 1.0f : severity);
}

int sensor_manager_read(sensor_reading_t *out_reading)
{
    if (!out_reading) return -1;
    s_ticks++;

    if (s_simulated_mode) {
        /* Baseline nominal parameters */
        float base_vib_x = 0.12f + 0.02f * sinf(s_ticks * 0.1f);
        float base_vib_y = 0.10f + 0.02f * cosf(s_ticks * 0.1f);
        float base_vib_z = 0.98f + 0.01f * sinf(s_ticks * 0.05f);
        float base_current = 4.2f + 0.1f * sinf(s_ticks * 0.05f);
        float base_temp = 42.0f;
        float base_flow = 85.0f; /* L/min */
        float base_tank = 78.0f;

        /* Fault injection adjustments */
        if (s_fault_type == 1) {
            /* BEARING DEGRADATION: Sharp high-frequency vibration spike & thermal creep */
            base_vib_x += (0.65f * s_fault_severity) + (0.25f * s_fault_severity * sinf(s_ticks * 0.8f));
            base_vib_y += (0.50f * s_fault_severity);
            base_temp += (18.0f * s_fault_severity);
            base_flow -= (12.0f * s_fault_severity);
        } else if (s_fault_type == 2) {
            /* OVERLOAD / HIGH CURRENT: Current surge & motor winding temp ramp */
            base_current += (3.5f * s_fault_severity);
            base_temp += (24.0f * s_fault_severity);
            base_vib_x += (0.20f * s_fault_severity);
        } else if (s_fault_type == 3) {
            /* BLOCKED INTAKE / LOW FLOW: Flow drops severely, tank level drops */
            base_flow -= (55.0f * s_fault_severity);
            base_current -= (0.8f * s_fault_severity);
            base_tank -= (30.0f * s_fault_severity);
        } else if (s_fault_type == 4) {
            /* OVERHEATING */
            base_temp += (35.0f * s_fault_severity);
        }

        out_reading->vibration_x = base_vib_x;
        out_reading->vibration_y = base_vib_y;
        out_reading->vibration_z = base_vib_z;
        out_reading->motor_current = base_current;
        out_reading->temperature = base_temp;
        out_reading->flow_rate = (base_flow < 0.0f) ? 0.0f : base_flow;
        out_reading->tank_level = (base_tank < 0.0f) ? 0.0f : base_tank;
        out_reading->timestamp_ms = s_ticks * 100;
        return 0;
    }

    /* Hardware Acquisition Path:
     * When building on nRF54LM20 DK with physical sensors enabled:
     * - ADXL355/LIS3DH read over SPI/I2C
     * - SCT-013 read via SAADC (Successive Approximation ADC)
     * - DS18B20 1-Wire read via GPIO
     * - YF-S201 read via Zephyr Timer / Counter driver
     */
    return -2; /* Not implemented without physical sensor peripherals */
}

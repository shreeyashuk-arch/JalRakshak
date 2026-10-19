#ifndef AQUAMESH_H_
#define AQUAMESH_H_

#include <stdint.h>
#include <stdbool.h>
#include "pump_health.h"

#ifdef __cplusplus
extern "C" {
#endif

#define AQUAMESH_MAX_NODE_ID_LEN 16

typedef enum {
    NODE_TYPE_PUMP = 1,
    NODE_TYPE_TANK = 2,
    NODE_TYPE_GATEWAY = 3
} aquamesh_node_type_t;

/* Packed Bluetooth Mesh Telemetry Payload (Fits in BLE Mesh Adv / Unsegmented PDU) */
typedef struct __attribute__((packed)) {
    uint8_t protocol_version;
    uint8_t node_id;
    uint8_t node_type;
    uint8_t health_score;       /* 0 - 100 */
    uint8_t reliability_score;  /* 0 - 100 */
    uint8_t risk_level;         /* 0: LOW, 1: MED, 2: HIGH, 3: CRIT */
    uint8_t maint_priority;     /* 0: NORMAL .. 4: CRITICAL */
    uint16_t vib_rms_milli_g;   /* milli-g */
    uint16_t current_rms_milli_a;
    int16_t temp_deci_c;        /* 0.1 deg C */
    uint16_t flow_deci_lpm;     /* 0.1 LPM */
    uint32_t seq_num;
} aquamesh_telemetry_pkt_t;

int aquamesh_init(void);
int aquamesh_publish_telemetry(const aquamesh_telemetry_pkt_t *pkt);
int aquamesh_sync_buffered_events(void);

#ifdef __cplusplus
}
#endif

#endif /* AQUAMESH_H_ */

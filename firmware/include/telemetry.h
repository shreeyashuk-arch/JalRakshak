#ifndef TELEMETRY_H_
#define TELEMETRY_H_

#include <stdint.h>
#include <stdbool.h>
#include "aquamesh.h"

#ifdef __cplusplus
extern "C" {
#endif

#define TELEMETRY_BUFFER_SIZE 64

int telemetry_init(void);
int telemetry_buffer_packet(const aquamesh_telemetry_pkt_t *pkt);
int telemetry_get_unflushed_count(void);
int telemetry_flush_to_gateway(void);

#ifdef __cplusplus
}
#endif

#endif /* TELEMETRY_H_ */

#include "telemetry.h"
#include <string.h>

static aquamesh_telemetry_pkt_t s_buffer[TELEMETRY_BUFFER_SIZE];
static uint16_t s_head = 0;
static uint16_t s_count = 0;

int telemetry_init(void)
{
    s_head = 0;
    s_count = 0;
    return 0;
}

int telemetry_buffer_packet(const aquamesh_telemetry_pkt_t *pkt)
{
    if (!pkt) return -1;

    s_buffer[s_head] = *pkt;
    s_head = (s_head + 1) % TELEMETRY_BUFFER_SIZE;
    if (s_count < TELEMETRY_BUFFER_SIZE) {
        s_count++;
    }
    return 0;
}

int telemetry_get_unflushed_count(void)
{
    return s_count;
}

int telemetry_flush_to_gateway(void)
{
    int flushed = s_count;
    s_count = 0;
    s_head = 0;
    return flushed;
}

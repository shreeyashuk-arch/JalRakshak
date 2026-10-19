cmake_minimum_required(VERSION 3.20.0)

find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(jalrakshak_firmware)

target_include_directories(app PRIVATE include)

target_sources(app PRIVATE
    src/main.c
    src/sensors/sensor_manager.c
    src/ai/edge_ai_engine.c
    src/health/pump_health.c
    src/bluetooth/aquamesh.c
    src/telemetry/telemetry.c
)

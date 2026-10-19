# AquaMesh: Bluetooth Low Energy & Mesh Architecture

**Platform:** Nordic Semiconductor nRF54LM20 DK  
**Radio Protocol:** Bluetooth Mesh v1.1 / BLE 5.4  
**Zephyr SDK Configuration:** `CONFIG_BT=y`, `CONFIG_BT_MESH=y`, `CONFIG_BT_MESH_RELAY=y`

---

## 1. Network Topology

```
+-------------------+        BLE Mesh Relay        +--------------------+
| Borehole Pump A   |<────────────────────────────>| Overhead Tank 01   |
| (nRF54LM20 Node)  |                              | (Telemetry Node)   |
+-------------------+                              +--------------------+
          │                                                   │
          │ BLE Mesh Advertisement                            │
          ▼                                                   ▼
+-------------------+                              +--------------------+
| Booster Station B |                              | Roaming Technician |
| (nRF54LM20 Node)  |<── Offline BLE Data Mule ───>| Handheld Gateway   |
+-------------------+                              +--------------------+
```

---

## 2. Key Architectural Tenets

### 1. Peer-to-Peer Pump-to-Tank Coordination
If a primary borehole pump experiences flow choking or bearing overheating, it publishes a mesh message to the downstream storage tank node. The tank node adjusts its recovery horizon calculation and flags a water-reliability warning before the tank empties.

### 2. Offline-First "Data Mule" Synchronization
In remote areas with no cellular infrastructure:
- The nRF54LM20 DK buffers health and sensor snapshots into an on-chip flash ring buffer (`firmware/src/telemetry/telemetry.c`).
- When a service technician visits the wellfield, their smartphone or handheld gateway (`GW-TECH01`) connects via BLE, ingests the buffered telemetry, and forwards it to the central cloud once connectivity is restored.

---

## 3. Wire Protocol & Binary PDU

The AquaMesh packet (`firmware/include/aquamesh.h`) is structured to fit inside an unsegmented Bluetooth Mesh Access Payload (11 octets payload):

| Field | Size | Unit / Format | Description |
| :--- | :---: | :--- | :--- |
| `protocol_version` | 1 byte | uint8 | Version identifier (v1) |
| `node_id` | 1 byte | uint8 | Unique node address in mesh network |
| `node_type` | 1 byte | enum | 1: Pump, 2: Tank, 3: Gateway |
| `health_score` | 1 byte | 0 – 100 | On-device computed health score |
| `reliability_score`| 1 byte | 0 – 100 | Composite water reliability score |
| `risk_level` | 1 byte | enum | 0: Low, 1: Medium, 2: High, 3: Critical |
| `maint_priority` | 1 byte | enum | 0: Normal .. 4: Critical |
| `vib_rms_milli_g` | 2 bytes | milli-g | Vibration RMS acceleration |
| `temp_deci_c` | 2 bytes | 0.1 °C | Operating temperature |
| `flow_deci_lpm` | 2 bytes | 0.1 LPM | Volumetric flow rate |

---
*Implementation Note: Physical mesh multi-hop requires flashing to physical nRF54LM20 DK boards. Software representations in the dashboard reflect this exact binary structure.*

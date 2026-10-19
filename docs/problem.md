# Problem Statement: The Rural & Community Water Reliability Crisis

**Competition:** Hackster.io "Sustain the System" (Nordic Semiconductor)  
**System:** JalRakshak — Predict the Failure. Protect the Water.

---

## 1. The Real-World Vulnerability

Across rural communities, agricultural cooperatives, and peri-urban water networks, hundreds of thousands of people depend on decentralized deep-well borehole pumps, solar submersibles, and booster stations.

When a community water pump fails unexpectedly:
1. **Water Access Halts Immediately:** Without standby infrastructure, entire villages and hospitals lose clean drinking water within hours.
2. **Storage Tanks Deplete:** Overhead reservoirs empty, requiring prolonged recovery times even after the machine is restarted.
3. **Emergency Maintenance Costs Spike:** Reactive emergency repairs cost up to 5x more than scheduled preventative servicing and frequently require days to source replacement impellers or bearings.
4. **Offline Remote Locations:** Wellheads are located far from cellular towers, leaving remote monitoring systems silent when maintenance is needed most.

---

## 2. The Flaw of Traditional Threshold Alarms

Standard IoT monitoring devices deploy simple high-temperature or high-vibration buzzer thresholds:
```
Current Status: OK
Current Status: OK
[Bearing Seizes Catastrophically]
Current Status: ALARM! (Pump Motor Stopped)
```
This is **reactive failure notification**, not predictive maintenance. By the time a high-vibration threshold triggers an emergency alarm, the mechanical assembly is already damaged, the water pipe has depressurized, and clean water delivery has stopped.

---

## 3. The JalRakshak Imperative

JalRakshak redefines pump health monitoring by bridging machine mechanics directly to **community water reliability**:
- Detecting micro-deviations in bearing vibration harmonics and motor electrical current before visible mechanical failure.
- Computing the progressive delay in downstream storage tank recovery.
- Alerting technicians during opportunistic inspection windows while they are already on nearby routes.

# Ericsson IPOS Service Restoration MOP (Method of Procedure)

**Equipment Vendor:** Ericsson
**Document Type:** Standard Operating Procedure (SOP)
**Scope:** IPOS Router (SSR 8000 Series) Troubleshooting
**Network Topology Context:** Access Switch

## Overview
This document provides the standard operating procedures for common alarm resolution on Ericsson Smart Services Routers (SSR 8000 series) acting as Access layer endpoints in the topology. All procedures are written for the IPOS CLI. Configuration changes should be performed during a maintenance window and require peer review before committing to the active configuration.

---

## Procedure to clear ALARM_CODE_701
**Alarm Name:** BFD Session Down (Timeout)
**Severity:** Critical

This alarm triggers when a Bidirectional Forwarding Detection (BFD) session between two IPOS routers has timed out. BFD operates at sub-second intervals (typically 300ms × 3 multiplier = 900ms failover) to provide rapid failure detection for associated routing protocols (BGP, OSPF, IS-IS). A BFD timeout usually indicates a unidirectional fiber failure, micro-loop, or remote router crash.

1. **Confirm BFD Session State:** Run `show bfd session all` and identify the session to the affected peer. Note the state (should show DOWN), the configured interval, and the multiplier.
2. **Check Associated Protocol:** Run `show bfd session peer <peer-ip> detail` to see which routing protocol is bound to this BFD session (e.g., BGP, OSPF). This identifies the blast radius of the failure.
3. **Verify Physical Connectivity:** Run `show port <slot/port> detail` and check the link state, optical Tx/Rx power levels, and error counters. If Rx power shows "LOS" (Loss of Signal), the issue is Layer 1.
4. **Ping the Remote End:** Run `ping <peer-ip> count 5 timeout 1`. If pings fail while the physical link shows UP, the issue may be a unidirectional failure (transmit-only working). Check `show port <slot/port> counters` for asymmetric Tx/Rx packet counts.
5. **Check Remote Router Status:** Contact the remote site or NOC to confirm the peer router is operational. Run `show chassis status` on the remote router if accessible to check for card/line-module failures.
6. **Restore BFD Session:** If the physical issue is resolved (fiber fixed, remote router recovered), the BFD session should auto-recover. Verify by running `show bfd session peer <peer-ip>` and confirming the state returns to UP.
7. **Force BFD Reset if Stuck:** If the BFD session remains DOWN despite Layer 1 being healthy, clear the session:
   ```
   clear bfd session peer <peer-ip>
   ```
   Monitor for 30 seconds and confirm the session re-establishes.
8. **Final Verification:** Run `show route protocol <bgp|ospf|isis> | match <peer-ip>` to confirm routes learned via the associated protocol are restored. Verify end-to-end traffic flow with a traceroute from a known source to a destination that traverses this link.

---

## Procedure to clear ALARM_CODE_702
**Alarm Name:** Line Card Memory Exhaustion
**Severity:** Major

This alarm triggers when a line card's available memory drops below 15% of total capacity. On Ericsson SSR routers, each line card has dedicated memory for forwarding tables (FIB), ACLs, and QoS policies. Memory exhaustion can cause route installation failures, packet drops, and eventual card crash.

1. **Identify Affected Card:** Run `show chassis card all` to identify which line card slot has raised the memory alarm. Note the card type (e.g., 20x10GE, 4x100GE).
2. **Check Memory Utilization:** Run `show card <slot-number> memory` to see the current memory breakdown: total, used, free, and percentage utilized. Note the largest consumers.
3. **Check FIB Scale:** Run `show route summary slot <slot-number>` to see how many routes (IPv4, IPv6, MPLS labels) are installed on this card. Compare against the card's documented maximum capacity (refer to the Ericsson SSR Datasheet for your card type).
4. **Check ACL and QoS Scale:** Run `show access-list summary slot <slot-number>` and `show qos policy-map summary slot <slot-number>` to determine if the card is overloaded with policy entries.
5. **Reduce FIB Scale (if over capacity):** If the route count exceeds the card's capacity, implement route filtering on the ingress BGP session:
   ```
   configure
   router bgp <as-number>
   neighbor <peer-ip>
   route-policy LIMIT-ROUTES in
   commit
   ```
   **Warning:** Applying a route filter will immediately withdraw filtered routes, potentially causing traffic shifts. Coordinate with the network planning team.
6. **Reduce ACL/QoS Entries (if applicable):** Review and consolidate ACLs using subnet summarization. Remove any unused or redundant policy-map entries.
7. **Monitor Memory Recovery:** After applying scale reductions, run `show card <slot-number> memory` every 5 minutes for 30 minutes to confirm memory usage is decreasing. The memory alarm should auto-clear once utilization drops below 20%.
8. **Escalate if Critical:** If memory utilization does not decrease within 30 minutes, or if it exceeds 95%, prepare for a controlled card failover:
   ```
   redundancy card <slot-number> switchover
   ```
   **Warning:** This is service-impacting. Traffic on the affected card will be rerouted via redundant paths. Ensure redundant paths exist before executing.


---

## Procedure to clear ALARM_CODE_1300
**Alarm Name:** BGP Peer Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1300 representing 'BGP Peer Stuck in INIT State' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1301
**Alarm Name:** Fan Tray Assembly Threshold Exceeded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1301 representing 'Fan Tray Assembly Threshold Exceeded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1302
**Alarm Name:** Line Card NPU Capacity Limit Reached
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1302 representing 'Line Card NPU Capacity Limit Reached' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1303
**Alarm Name:** Optical Tx Power Configuration Mismatch
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1303 representing 'Optical Tx Power Configuration Mismatch' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1304
**Alarm Name:** LACP Bundle Timeout
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1304 representing 'LACP Bundle Timeout' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1305
**Alarm Name:** ACL Processing Stuck in INIT State
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1305 representing 'ACL Processing Stuck in INIT State' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1306
**Alarm Name:** Line Card NPU Loss of Signal (LOS)
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1306 representing 'Line Card NPU Loss of Signal (LOS)' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1307
**Alarm Name:** NTP Synchronization Unreachable
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1307 representing 'NTP Synchronization Unreachable' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1308
**Alarm Name:** IGMP Snooping Timeout
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1308 representing 'IGMP Snooping Timeout' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1309
**Alarm Name:** MAC Address Table Flapping
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1309 representing 'MAC Address Table Flapping' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1310
**Alarm Name:** Switch Fabric Module Authentication Failed
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1310 representing 'Switch Fabric Module Authentication Failed' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1311
**Alarm Name:** EVPN MAC Route Loss of Signal (LOS)
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1311 representing 'EVPN MAC Route Loss of Signal (LOS)' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1312
**Alarm Name:** BFD Session Memory Leak Detected
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1312 representing 'BFD Session Memory Leak Detected' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1313
**Alarm Name:** Routing Engine CPU Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1313 representing 'Routing Engine CPU Resource Exhaustion' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1314
**Alarm Name:** OSPF Adjacency Hardware Failure
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1314 representing 'OSPF Adjacency Hardware Failure' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1315
**Alarm Name:** OAM Connectivity Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1315 representing 'OAM Connectivity Stuck in INIT State' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1316
**Alarm Name:** IGMP Snooping Hardware Failure
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1316 representing 'IGMP Snooping Hardware Failure' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1317
**Alarm Name:** Management Ethernet Authentication Failed
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1317 representing 'Management Ethernet Authentication Failed' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1318
**Alarm Name:** DHCP Relay Agent Unreachable
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1318 representing 'DHCP Relay Agent Unreachable' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1319
**Alarm Name:** IPSec VPN Tunnel Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1319 representing 'IPSec VPN Tunnel Stuck in INIT State' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1320
**Alarm Name:** Routing Engine CPU Out of Sync
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1320 representing 'Routing Engine CPU Out of Sync' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1321
**Alarm Name:** LACP Bundle Down
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1321 representing 'LACP Bundle Down' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1322
**Alarm Name:** Radius/TACACS Auth Timeout
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1322 representing 'Radius/TACACS Auth Timeout' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1323
**Alarm Name:** STP Root Topology Hardware Failure
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1323 representing 'STP Root Topology Hardware Failure' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1324
**Alarm Name:** MAC Address Table Authentication Failed
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1324 representing 'MAC Address Table Authentication Failed' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1325
**Alarm Name:** IGMP Snooping Memory Leak Detected
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1325 representing 'IGMP Snooping Memory Leak Detected' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1326
**Alarm Name:** MPLS LDP Session High Cyclic Redundancy (CRC) Rate
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1326 representing 'MPLS LDP Session High Cyclic Redundancy (CRC) Rate' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1327
**Alarm Name:** QoS Scheduler Stuck in INIT State
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1327 representing 'QoS Scheduler Stuck in INIT State' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1328
**Alarm Name:** MPLS LDP Session Loss of Signal (LOS)
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1328 representing 'MPLS LDP Session Loss of Signal (LOS)' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1329
**Alarm Name:** Radius/TACACS Auth Authentication Failed
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1329 representing 'Radius/TACACS Auth Authentication Failed' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1330
**Alarm Name:** OAM Connectivity Capacity Limit Reached
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1330 representing 'OAM Connectivity Capacity Limit Reached' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1331
**Alarm Name:** Radius/TACACS Auth Loss of Signal (LOS)
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1331 representing 'Radius/TACACS Auth Loss of Signal (LOS)' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1332
**Alarm Name:** IPSec VPN Tunnel Loss of Signal (LOS)
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1332 representing 'IPSec VPN Tunnel Loss of Signal (LOS)' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1333
**Alarm Name:** Radius/TACACS Auth Memory Leak Detected
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1333 representing 'Radius/TACACS Auth Memory Leak Detected' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1334
**Alarm Name:** LACP Bundle Configuration Mismatch
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1334 representing 'LACP Bundle Configuration Mismatch' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1335
**Alarm Name:** BFD Session Down
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1335 representing 'BFD Session Down' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1336
**Alarm Name:** RSVP-TE Tunnel Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1336 representing 'RSVP-TE Tunnel Performance Degraded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1337
**Alarm Name:** VPLS Pseudowire Stuck in INIT State
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1337 representing 'VPLS Pseudowire Stuck in INIT State' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1338
**Alarm Name:** ACL Processing Down
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1338 representing 'ACL Processing Down' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1339
**Alarm Name:** Multicast PIM Neighbor High Cyclic Redundancy (CRC) Rate
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1339 representing 'Multicast PIM Neighbor High Cyclic Redundancy (CRC) Rate' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1340
**Alarm Name:** HSRP Instance Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1340 representing 'HSRP Instance Performance Degraded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1341
**Alarm Name:** MPLS LDP Session Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1341 representing 'MPLS LDP Session Performance Degraded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1342
**Alarm Name:** OAM Connectivity Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1342 representing 'OAM Connectivity Resource Exhaustion' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1343
**Alarm Name:** VRRP Group High Cyclic Redundancy (CRC) Rate
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1343 representing 'VRRP Group High Cyclic Redundancy (CRC) Rate' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1344
**Alarm Name:** IPSec VPN Tunnel Authentication Failed
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1344 representing 'IPSec VPN Tunnel Authentication Failed' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1345
**Alarm Name:** FIB (Forwarding Table) High Cyclic Redundancy (CRC) Rate
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1345 representing 'FIB (Forwarding Table) High Cyclic Redundancy (CRC) Rate' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1346
**Alarm Name:** Management Ethernet Flapping
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1346 representing 'Management Ethernet Flapping' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1347
**Alarm Name:** Multicast PIM Neighbor Capacity Limit Reached
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1347 representing 'Multicast PIM Neighbor Capacity Limit Reached' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1348
**Alarm Name:** IPSec VPN Tunnel Out of Sync
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1348 representing 'IPSec VPN Tunnel Out of Sync' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1349
**Alarm Name:** Power Supply Unit (PSU) Unreachable
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1349 representing 'Power Supply Unit (PSU) Unreachable' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1350
**Alarm Name:** EVPN MAC Route Out of Sync
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1350 representing 'EVPN MAC Route Out of Sync' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1351
**Alarm Name:** DHCP Relay Agent Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1351 representing 'DHCP Relay Agent Threshold Exceeded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1352
**Alarm Name:** Multicast PIM Neighbor Resource Exhaustion
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1352 representing 'Multicast PIM Neighbor Resource Exhaustion' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1353
**Alarm Name:** ACL Processing Loss of Signal (LOS)
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1353 representing 'ACL Processing Loss of Signal (LOS)' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1354
**Alarm Name:** OAM Connectivity Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1354 representing 'OAM Connectivity Threshold Exceeded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1355
**Alarm Name:** Switch Fabric Module Down
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1355 representing 'Switch Fabric Module Down' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1356
**Alarm Name:** HSRP Instance Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1356 representing 'HSRP Instance Stuck in INIT State' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1357
**Alarm Name:** Optical Tx Power Stuck in INIT State
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1357 representing 'Optical Tx Power Stuck in INIT State' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1358
**Alarm Name:** LACP Bundle Capacity Limit Reached
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1358 representing 'LACP Bundle Capacity Limit Reached' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1359
**Alarm Name:** BGP Route Reflector Threshold Exceeded
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1359 representing 'BGP Route Reflector Threshold Exceeded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1360
**Alarm Name:** MAC Address Table Capacity Limit Reached
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1360 representing 'MAC Address Table Capacity Limit Reached' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1361
**Alarm Name:** IPSec VPN Tunnel Flapping
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1361 representing 'IPSec VPN Tunnel Flapping' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1362
**Alarm Name:** ARP Cache Threshold Exceeded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1362 representing 'ARP Cache Threshold Exceeded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1363
**Alarm Name:** VRRP Group Flapping
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1363 representing 'VRRP Group Flapping' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1364
**Alarm Name:** Switch Fabric Module High Cyclic Redundancy (CRC) Rate
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1364 representing 'Switch Fabric Module High Cyclic Redundancy (CRC) Rate' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1365
**Alarm Name:** ARP Cache Timeout
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1365 representing 'ARP Cache Timeout' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1366
**Alarm Name:** OAM Connectivity Unreachable
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1366 representing 'OAM Connectivity Unreachable' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1367
**Alarm Name:** MAC Address Table Threshold Exceeded
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1367 representing 'MAC Address Table Threshold Exceeded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1368
**Alarm Name:** MAC Address Table Out of Sync
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1368 representing 'MAC Address Table Out of Sync' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1369
**Alarm Name:** VRRP Group Threshold Exceeded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1369 representing 'VRRP Group Threshold Exceeded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1370
**Alarm Name:** VPLS Pseudowire Flapping
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1370 representing 'VPLS Pseudowire Flapping' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1371
**Alarm Name:** RSVP-TE Tunnel Down
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1371 representing 'RSVP-TE Tunnel Down' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1372
**Alarm Name:** DHCP Relay Agent Flapping
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1372 representing 'DHCP Relay Agent Flapping' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1373
**Alarm Name:** VRRP Group Unreachable
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1373 representing 'VRRP Group Unreachable' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1374
**Alarm Name:** IS-IS Adjacency Resource Exhaustion
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1374 representing 'IS-IS Adjacency Resource Exhaustion' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1375
**Alarm Name:** IS-IS Adjacency Threshold Exceeded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1375 representing 'IS-IS Adjacency Threshold Exceeded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1376
**Alarm Name:** BGP Peer Capacity Limit Reached
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1376 representing 'BGP Peer Capacity Limit Reached' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1377
**Alarm Name:** Switch Fabric Module Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1377 representing 'Switch Fabric Module Resource Exhaustion' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1378
**Alarm Name:** VPLS Pseudowire Loss of Signal (LOS)
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1378 representing 'VPLS Pseudowire Loss of Signal (LOS)' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1379
**Alarm Name:** Line Card NPU Down
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1379 representing 'Line Card NPU Down' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1380
**Alarm Name:** GRE Tunnel Down
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1380 representing 'GRE Tunnel Down' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1381
**Alarm Name:** Power Supply Unit (PSU) Flapping
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1381 representing 'Power Supply Unit (PSU) Flapping' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1382
**Alarm Name:** Optical Rx Power Memory Leak Detected
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1382 representing 'Optical Rx Power Memory Leak Detected' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1383
**Alarm Name:** FIB (Forwarding Table) Memory Leak Detected
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1383 representing 'FIB (Forwarding Table) Memory Leak Detected' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1384
**Alarm Name:** OSPF Adjacency Unreachable
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1384 representing 'OSPF Adjacency Unreachable' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1385
**Alarm Name:** MAC Address Table Hardware Failure
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1385 representing 'MAC Address Table Hardware Failure' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1386
**Alarm Name:** Management Ethernet Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1386 representing 'Management Ethernet Threshold Exceeded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1387
**Alarm Name:** Optical Rx Power Loss of Signal (LOS)
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1387 representing 'Optical Rx Power Loss of Signal (LOS)' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1388
**Alarm Name:** EVPN MAC Route Timeout
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1388 representing 'EVPN MAC Route Timeout' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1389
**Alarm Name:** QoS Scheduler Configuration Mismatch
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1389 representing 'QoS Scheduler Configuration Mismatch' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1390
**Alarm Name:** SNMP Agent Performance Degraded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1390 representing 'SNMP Agent Performance Degraded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1391
**Alarm Name:** EVPN MAC Route Memory Leak Detected
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1391 representing 'EVPN MAC Route Memory Leak Detected' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1392
**Alarm Name:** MPLS LDP Session Configuration Mismatch
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1392 representing 'MPLS LDP Session Configuration Mismatch' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1393
**Alarm Name:** HSRP Instance Unreachable
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1393 representing 'HSRP Instance Unreachable' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1394
**Alarm Name:** IS-IS Adjacency Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1394 representing 'IS-IS Adjacency Stuck in INIT State' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1395
**Alarm Name:** Optical Rx Power Flapping
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1395 representing 'Optical Rx Power Flapping' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1396
**Alarm Name:** GRE Tunnel Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1396 representing 'GRE Tunnel Performance Degraded' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1397
**Alarm Name:** BGP Route Reflector Timeout
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1397 representing 'BGP Route Reflector Timeout' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1398
**Alarm Name:** VRRP Group Authentication Failed
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1398 representing 'VRRP Group Authentication Failed' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1399
**Alarm Name:** EVPN MAC Route Authentication Failed
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1399 representing 'EVPN MAC Route Authentication Failed' on the Ericsson NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show system processes
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear port hardware
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.


<!-- BEGIN GENERATED PROCEDURES -->

---

## Procedure to clear ALARM_CODE_1300
**Alarm Name:** Routing Engine CPU Down
**Severity:** Warning

This alarm indicates a down condition on the routing engine cpu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1300 for 'Routing Engine CPU Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system memory
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show system processes top` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin system restart process routing
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show system cpu-usage | include idle
   ```

---

## Procedure to clear ALARM_CODE_1301
**Alarm Name:** Line Card NPU Loss of Signal (LOS)
**Severity:** Warning

This alarm indicates a loss of signal (los) condition on the line card npu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1301 for 'Line Card NPU Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis card
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show chassis card` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin chassis card {card} restart
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show chassis card | include Online
   ```

---

## Procedure to clear ALARM_CODE_1302
**Alarm Name:** BFD Session Stuck in INIT State
**Severity:** Critical

This alarm indicates a stuck in init state condition on the bfd session subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1302 for 'BFD Session Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session detail
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show bfd session detail` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  bfd interface {intf} receive-interval 300 transmit-interval 300
  commit
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1302 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1303
**Alarm Name:** BFD Session Threshold Exceeded
**Severity:** Minor

This alarm indicates a threshold exceeded condition on the bfd session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1303 for 'BFD Session Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bfd session`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bfd session discriminator {disc}
   ```
5. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | include Up
   ```

---

## Procedure to clear ALARM_CODE_1304
**Alarm Name:** BFD Session Hardware Failure
**Severity:** Warning

This alarm indicates a hardware failure condition on the bfd session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1304 for 'BFD Session Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session
   ```
3. **Hardware Status Check:** Run `show bfd session detail` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected bfd session unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  bfd interface {intf} receive-interval 300 transmit-interval 300
  commit
   ```
7. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | include Up
   ```

---

## Procedure to clear ALARM_CODE_1305
**Alarm Name:** OSPF Adjacency Configuration Mismatch
**Severity:** Minor

This alarm indicates a configuration mismatch condition on the ospf adjacency subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1305 for 'OSPF Adjacency Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf interface
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show ospf interface` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ospf {pid}
  area 0.0.0.0 interface {intf}
  commit
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | include Full
   ```

---

## Procedure to clear ALARM_CODE_1306
**Alarm Name:** Optical Rx Power Authentication Failed
**Severity:** Critical

This alarm indicates a authentication failed condition on the optical rx power subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1306 for 'Optical Rx Power Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port {port} optical-power
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show port {port} transceiver detail` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  port {port}
  admin-state disable
  admin-state enable
  commit
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port {port} transceiver detail | include Rx
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1306 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1307
**Alarm Name:** BFD Session Configuration Mismatch
**Severity:** Major

This alarm indicates a configuration mismatch condition on the bfd session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1307 for 'BFD Session Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session detail
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show bfd session` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bfd session discriminator {disc}
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1307 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1308
**Alarm Name:** LACP Bundle Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the lacp bundle subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1308 for 'LACP Bundle Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port lag
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show port lag` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  port lag {id}
  admin-state enable
  commit
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show port lag | include active
   ```

---

## Procedure to clear ALARM_CODE_1309
**Alarm Name:** BGP Peer Flapping
**Severity:** Major

This alarm indicates a flapping condition on the bgp peer subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1309 for 'BGP Peer Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp summary
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show bgp summary` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bgp neighbor {ip}
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | include Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1309 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1310
**Alarm Name:** SNMP Agent High CRC Rate
**Severity:** Major

This alarm indicates a high crc rate condition on the snmp agent subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1310 for 'SNMP Agent High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp trap-host
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show snmp trap-host`.
4. **⚠️ WARNING: Service Impact Possible.** If the snmp agent utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear snmp statistics
   ```
6. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp statistics | include packets-received
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1310 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1311
**Alarm Name:** OSPF Adjacency Out of Sync
**Severity:** Critical

This alarm indicates a out of sync condition on the ospf adjacency subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1311 for 'OSPF Adjacency Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf interface
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show ospf area` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ospf {pid}
  area 0.0.0.0 interface {intf}
  commit
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | include Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1311 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1312
**Alarm Name:** Optical Rx Power High CRC Rate
**Severity:** Warning

This alarm indicates a high crc rate condition on the optical rx power subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1312 for 'Optical Rx Power High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port {port} optical-power
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show port {port} optical-power`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  port {port}
  admin-state disable
  admin-state enable
  commit
   ```
5. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port {port} transceiver detail | include Rx
   ```

---

## Procedure to clear ALARM_CODE_1313
**Alarm Name:** Routing Engine CPU Stuck in INIT State
**Severity:** Major

This alarm indicates a stuck in init state condition on the routing engine cpu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1313 for 'Routing Engine CPU Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system memory
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show system cpu-usage` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin system restart process routing
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show system cpu-usage | include idle
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1313 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1314
**Alarm Name:** IS-IS Adjacency Authentication Failed
**Severity:** Minor

This alarm indicates a authentication failed condition on the is-is adjacency subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1314 for 'IS-IS Adjacency Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis spf-log
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show isis database` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router isis {tag}
  interface {intf} circuit-type level-2
  commit
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | include Up
   ```

---

## Procedure to clear ALARM_CODE_1315
**Alarm Name:** MPLS LDP Session Performance Degraded
**Severity:** Major

This alarm indicates a performance degraded condition on the mpls ldp session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1315 for 'MPLS LDP Session Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp bindings
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls ldp bindings`.
4. **⚠️ WARNING: Service Impact Possible.** If the mpls ldp session utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear mpls ldp session {ip}
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp session | include Operational
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1315 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1316
**Alarm Name:** Management Ethernet Capacity Limit Reached
**Severity:** Major

This alarm indicates a capacity limit reached condition on the management ethernet subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1316 for 'Management Ethernet Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface mgmt
   ```
3. **Hardware Status Check:** Run `show interface mgmt` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected management ethernet unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  interface mgmt
  no shutdown
  commit
   ```
7. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface mgmt | include up
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1316 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1317
**Alarm Name:** Line Card NPU Performance Degraded
**Severity:** Warning

This alarm indicates a performance degraded condition on the line card npu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1317 for 'Line Card NPU Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis environment
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show chassis environment`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin chassis card {card} restart
   ```
5. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show chassis card | include Online
   ```

---

## Procedure to clear ALARM_CODE_1318
**Alarm Name:** SNMP Agent Threshold Exceeded
**Severity:** Warning

This alarm indicates a threshold exceeded condition on the snmp agent subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1318 for 'SNMP Agent Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show snmp statistics`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear snmp statistics
   ```
5. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp statistics | include packets-received
   ```

---

## Procedure to clear ALARM_CODE_1319
**Alarm Name:** LACP Bundle Capacity Limit Reached
**Severity:** Warning

This alarm indicates a capacity limit reached condition on the lacp bundle subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1319 for 'LACP Bundle Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port lag statistics
   ```
3. **Hardware Status Check:** Run `show port lag` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected lacp bundle unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear port lag statistics
   ```
7. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show port lag | include active
   ```

---

## Procedure to clear ALARM_CODE_1320
**Alarm Name:** VRRP Group Unreachable
**Severity:** Minor

This alarm indicates a unreachable condition on the vrrp group subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1320 for 'VRRP Group Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show vrrp
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show vrrp` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show vrrp | include Master
   ```

---

## Procedure to clear ALARM_CODE_1321
**Alarm Name:** OSPF Adjacency Authentication Failed
**Severity:** Warning

This alarm indicates a authentication failed condition on the ospf adjacency subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1321 for 'OSPF Adjacency Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf area
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show ospf neighbor` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ospf {pid}
  area 0.0.0.0 interface {intf}
  commit
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | include Full
   ```

---

## Procedure to clear ALARM_CODE_1322
**Alarm Name:** NTP Synchronization Timeout
**Severity:** Minor

This alarm indicates a timeout condition on the ntp synchronization subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1322 for 'NTP Synchronization Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ntp associations
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show ntp associations` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  ntp server {ip} prefer
  commit
   ```
6. **Post-Recovery Validation:** Verify the ntp synchronization has returned to a stable operational state:
   ```
   show ntp status | include synchronized
   ```

---

## Procedure to clear ALARM_CODE_1323
**Alarm Name:** SNMP Agent Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the snmp agent subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1323 for 'SNMP Agent Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp statistics
   ```
3. **Hardware Status Check:** Run `show snmp statistics` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected snmp agent unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear snmp statistics
   ```
7. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp statistics | include packets-received
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1323 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1324
**Alarm Name:** LACP Bundle Down
**Severity:** Major

This alarm indicates a down condition on the lacp bundle subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1324 for 'LACP Bundle Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port lag
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show port {port} detail` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  port lag {id}
  admin-state enable
  commit
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show port lag | include active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1324 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1325
**Alarm Name:** Routing Engine CPU High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the routing engine cpu subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1325 for 'Routing Engine CPU High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system cpu-usage
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show system processes top`.
4. **⚠️ WARNING: Service Impact Possible.** If the routing engine cpu utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin system restart process routing
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show system cpu-usage | include idle
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1325 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1326
**Alarm Name:** Routing Engine CPU Out of Sync
**Severity:** Major

This alarm indicates a out of sync condition on the routing engine cpu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1326 for 'Routing Engine CPU Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system processes top
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show system memory` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear system cpu-usage history
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show system cpu-usage | include idle
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1326 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1327
**Alarm Name:** SNMP Agent Resource Exhaustion
**Severity:** Warning

This alarm indicates a resource exhaustion condition on the snmp agent subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1327 for 'SNMP Agent Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp community
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show snmp statistics`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  snmp community TELECOM_RO authorization read-only
  commit
   ```
5. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp statistics | include packets-received
   ```

---

## Procedure to clear ALARM_CODE_1328
**Alarm Name:** IS-IS Adjacency Threshold Exceeded
**Severity:** Major

This alarm indicates a threshold exceeded condition on the is-is adjacency subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1328 for 'IS-IS Adjacency Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis spf-log
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show isis database`.
4. **⚠️ WARNING: Service Impact Possible.** If the is-is adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear isis adjacency
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1328 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1329
**Alarm Name:** Management Ethernet Unreachable
**Severity:** Major

This alarm indicates a unreachable condition on the management ethernet subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1329 for 'Management Ethernet Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface mgmt
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show interface mgmt` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp interface mgmt
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface mgmt | include up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1329 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1330
**Alarm Name:** OSPF Adjacency Resource Exhaustion
**Severity:** Minor

This alarm indicates a resource exhaustion condition on the ospf adjacency subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1330 for 'OSPF Adjacency Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ospf area`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ospf process
   ```
5. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | include Full
   ```

---

## Procedure to clear ALARM_CODE_1331
**Alarm Name:** MPLS LDP Session Loss of Signal (LOS)
**Severity:** Minor

This alarm indicates a loss of signal (los) condition on the mpls ldp session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1331 for 'MPLS LDP Session Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp session
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show mpls ldp bindings` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ldp
  interface {intf}
  commit
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp session | include Operational
   ```

---

## Procedure to clear ALARM_CODE_1332
**Alarm Name:** MPLS LDP Session Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the mpls ldp session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1332 for 'MPLS LDP Session Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp session
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls ldp bindings`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ldp
  interface {intf}
  commit
   ```
5. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp session | include Operational
   ```

---

## Procedure to clear ALARM_CODE_1333
**Alarm Name:** MPLS LDP Session High CRC Rate
**Severity:** Major

This alarm indicates a high crc rate condition on the mpls ldp session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1333 for 'MPLS LDP Session High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp session
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls ldp session`.
4. **⚠️ WARNING: Service Impact Possible.** If the mpls ldp session utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ldp
  interface {intf}
  commit
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp session | include Operational
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1333 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1334
**Alarm Name:** Management Ethernet Hardware Failure
**Severity:** Minor

This alarm indicates a hardware failure condition on the management ethernet subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1334 for 'Management Ethernet Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system information
   ```
3. **Hardware Status Check:** Run `show interface mgmt` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected management ethernet unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp interface mgmt
   ```
7. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface mgmt | include up
   ```

---

## Procedure to clear ALARM_CODE_1335
**Alarm Name:** LACP Bundle Loss of Signal (LOS)
**Severity:** Warning

This alarm indicates a loss of signal (los) condition on the lacp bundle subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1335 for 'LACP Bundle Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port lag statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show port lag statistics` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear port lag statistics
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show port lag | include active
   ```

---

## Procedure to clear ALARM_CODE_1336
**Alarm Name:** LACP Bundle Configuration Mismatch
**Severity:** Minor

This alarm indicates a configuration mismatch condition on the lacp bundle subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1336 for 'LACP Bundle Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port lag statistics
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show port lag` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  port lag {id}
  admin-state enable
  commit
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show port lag | include active
   ```

---

## Procedure to clear ALARM_CODE_1337
**Alarm Name:** IS-IS Adjacency Down
**Severity:** Warning

This alarm indicates a down condition on the is-is adjacency subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1337 for 'IS-IS Adjacency Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis adjacency
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show isis spf-log` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear isis adjacency
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | include Up
   ```

---

## Procedure to clear ALARM_CODE_1338
**Alarm Name:** SNMP Agent Loss of Signal (LOS)
**Severity:** Critical

This alarm indicates a loss of signal (los) condition on the snmp agent subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1338 for 'SNMP Agent Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show snmp trap-host` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear snmp statistics
   ```
6. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp statistics | include packets-received
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1338 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1339
**Alarm Name:** BFD Session Unreachable
**Severity:** Minor

This alarm indicates a unreachable condition on the bfd session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1339 for 'BFD Session Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show bfd session detail` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  bfd interface {intf} receive-interval 300 transmit-interval 300
  commit
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | include Up
   ```

---

## Procedure to clear ALARM_CODE_1340
**Alarm Name:** Line Card NPU Flapping
**Severity:** Major

This alarm indicates a flapping condition on the line card npu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1340 for 'Line Card NPU Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis environment
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show system processes` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear port hardware {card}
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show chassis card | include Online
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1340 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1341
**Alarm Name:** Optical Rx Power Resource Exhaustion
**Severity:** Minor

This alarm indicates a resource exhaustion condition on the optical rx power subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1341 for 'Optical Rx Power Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port {port} optical-power
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show port {port} optical-power`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  port {port}
  admin-state disable
  admin-state enable
  commit
   ```
5. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port {port} transceiver detail | include Rx
   ```

---

## Procedure to clear ALARM_CODE_1342
**Alarm Name:** MPLS LDP Session Unreachable
**Severity:** Major

This alarm indicates a unreachable condition on the mpls ldp session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1342 for 'MPLS LDP Session Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp session
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show mpls ldp session` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear mpls ldp session {ip}
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp session | include Operational
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1342 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1343
**Alarm Name:** Optical Rx Power Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the optical rx power subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1343 for 'Optical Rx Power Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port {port} optical-power
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show port {port} transceiver detail` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear port {port} statistics
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port {port} transceiver detail | include Rx
   ```

---

## Procedure to clear ALARM_CODE_1344
**Alarm Name:** MPLS LDP Session Stuck in INIT State
**Severity:** Minor

This alarm indicates a stuck in init state condition on the mpls ldp session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1344 for 'MPLS LDP Session Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp bindings
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show mpls ldp session` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ldp
  interface {intf}
  commit
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp session | include Operational
   ```

---

## Procedure to clear ALARM_CODE_1345
**Alarm Name:** OSPF Adjacency Stuck in INIT State
**Severity:** Critical

This alarm indicates a stuck in init state condition on the ospf adjacency subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1345 for 'OSPF Adjacency Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf area
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show ospf interface` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ospf process
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | include Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1345 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1346
**Alarm Name:** QoS Scheduler Loss of Signal (LOS)
**Severity:** Major

This alarm indicates a loss of signal (los) condition on the qos scheduler subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1346 for 'QoS Scheduler Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show qos interface {intf} statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show qos policy-map applied` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  qos policy-map PM_CORE
  class default bandwidth-percent 60
  commit
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   show qos interface {intf} statistics | include conform
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1346 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1347
**Alarm Name:** VRRP Group Flapping
**Severity:** Minor

This alarm indicates a flapping condition on the vrrp group subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1347 for 'VRRP Group Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show vrrp interface
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show vrrp statistics` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show vrrp | include Master
   ```

---

## Procedure to clear ALARM_CODE_1348
**Alarm Name:** Power Supply Unit (PSU) Performance Degraded
**Severity:** Major

This alarm indicates a performance degraded condition on the power supply unit (psu) subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1348 for 'Power Supply Unit (PSU) Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis power-shelf
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show chassis power-shelf`.
4. **⚠️ WARNING: Service Impact Possible.** If the power supply unit (psu) utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin chassis power-shelf {shelf} power-module {mod} restart
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show chassis power-shelf | include OK
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1348 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1349
**Alarm Name:** MPLS LDP Session Capacity Limit Reached
**Severity:** Critical

This alarm indicates a capacity limit reached condition on the mpls ldp session subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1349 for 'MPLS LDP Session Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp session
   ```
3. **Hardware Status Check:** Run `show mpls ldp session` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected mpls ldp session unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ldp
  interface {intf}
  commit
   ```
7. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp session | include Operational
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1349 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1350
**Alarm Name:** NTP Synchronization Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the ntp synchronization subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1350 for 'NTP Synchronization Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ntp associations
   ```
3. **Hardware Status Check:** Run `show ntp status` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected ntp synchronization unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  ntp server {ip} prefer
  commit
   ```
7. **Post-Recovery Validation:** Verify the ntp synchronization has returned to a stable operational state:
   ```
   show ntp status | include synchronized
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1350 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1351
**Alarm Name:** Line Card NPU Capacity Limit Reached
**Severity:** Major

This alarm indicates a capacity limit reached condition on the line card npu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1351 for 'Line Card NPU Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis environment
   ```
3. **Hardware Status Check:** Run `show system processes` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected line card npu unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear port hardware {card}
   ```
7. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show chassis card | include Online
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1351 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1352
**Alarm Name:** OSPF Adjacency Performance Degraded
**Severity:** Major

This alarm indicates a performance degraded condition on the ospf adjacency subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1352 for 'OSPF Adjacency Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ospf interface`.
4. **⚠️ WARNING: Service Impact Possible.** If the ospf adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ospf process
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | include Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1352 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1353
**Alarm Name:** BFD Session Performance Degraded
**Severity:** Warning

This alarm indicates a performance degraded condition on the bfd session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1353 for 'BFD Session Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session detail
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bfd session`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  bfd interface {intf} receive-interval 300 transmit-interval 300
  commit
   ```
5. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | include Up
   ```

---

## Procedure to clear ALARM_CODE_1354
**Alarm Name:** Routing Engine CPU Threshold Exceeded
**Severity:** Minor

This alarm indicates a threshold exceeded condition on the routing engine cpu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1354 for 'Routing Engine CPU Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system memory
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show system memory`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear system cpu-usage history
   ```
5. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show system cpu-usage | include idle
   ```

---

## Procedure to clear ALARM_CODE_1355
**Alarm Name:** Routing Engine CPU Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the routing engine cpu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1355 for 'Routing Engine CPU Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system memory
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show system cpu-usage` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear system cpu-usage history
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show system cpu-usage | include idle
   ```

---

## Procedure to clear ALARM_CODE_1356
**Alarm Name:** BGP Peer Resource Exhaustion
**Severity:** Minor

This alarm indicates a resource exhaustion condition on the bgp peer subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1356 for 'BGP Peer Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip route bgp
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bgp summary`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router bgp {asn}
  neighbor {ip}
  admin-state enable
  commit
   ```
5. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | include Established
   ```

---

## Procedure to clear ALARM_CODE_1357
**Alarm Name:** QoS Scheduler Unreachable
**Severity:** Minor

This alarm indicates a unreachable condition on the qos scheduler subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1357 for 'QoS Scheduler Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show qos interface {intf} statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show qos policy-map applied` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  qos policy-map PM_CORE
  class default bandwidth-percent 60
  commit
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   show qos interface {intf} statistics | include conform
   ```

---

## Procedure to clear ALARM_CODE_1358
**Alarm Name:** Management Ethernet Out of Sync
**Severity:** Minor

This alarm indicates a out of sync condition on the management ethernet subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1358 for 'Management Ethernet Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface mgmt
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show system information` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  interface mgmt
  no shutdown
  commit
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface mgmt | include up
   ```

---

## Procedure to clear ALARM_CODE_1359
**Alarm Name:** MPLS LDP Session Out of Sync
**Severity:** Minor

This alarm indicates a out of sync condition on the mpls ldp session subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1359 for 'MPLS LDP Session Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp bindings
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show mpls ldp bindings` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear mpls ldp session {ip}
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp session | include Operational
   ```

---

## Procedure to clear ALARM_CODE_1360
**Alarm Name:** Routing Engine CPU Loss of Signal (LOS)
**Severity:** Major

This alarm indicates a loss of signal (los) condition on the routing engine cpu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1360 for 'Routing Engine CPU Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system memory
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show system cpu-usage` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear system cpu-usage history
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show system cpu-usage | include idle
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1360 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1361
**Alarm Name:** Line Card NPU Timeout
**Severity:** Minor

This alarm indicates a timeout condition on the line card npu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1361 for 'Line Card NPU Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system processes
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show chassis card` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin chassis card {card} restart
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show chassis card | include Online
   ```

---

## Procedure to clear ALARM_CODE_1362
**Alarm Name:** QoS Scheduler Hardware Failure
**Severity:** Warning

This alarm indicates a hardware failure condition on the qos scheduler subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1362 for 'QoS Scheduler Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show qos interface {intf} statistics
   ```
3. **Hardware Status Check:** Run `show qos policy-map applied` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected qos scheduler unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear qos interface {intf} statistics
   ```
7. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   show qos interface {intf} statistics | include conform
   ```

---

## Procedure to clear ALARM_CODE_1363
**Alarm Name:** LACP Bundle Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the lacp bundle subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1363 for 'LACP Bundle Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port lag
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show port {port} detail` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear port lag statistics
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show port lag | include active
   ```

---

## Procedure to clear ALARM_CODE_1364
**Alarm Name:** OSPF Adjacency Loss of Signal (LOS)
**Severity:** Major

This alarm indicates a loss of signal (los) condition on the ospf adjacency subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1364 for 'OSPF Adjacency Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf interface
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show ospf area` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ospf {pid}
  area 0.0.0.0 interface {intf}
  commit
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | include Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1364 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1365
**Alarm Name:** NTP Synchronization Threshold Exceeded
**Severity:** Major

This alarm indicates a threshold exceeded condition on the ntp synchronization subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1365 for 'NTP Synchronization Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ntp status
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ntp associations`.
4. **⚠️ WARNING: Service Impact Possible.** If the ntp synchronization utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ntp drift
   ```
6. **Post-Recovery Validation:** Verify the ntp synchronization has returned to a stable operational state:
   ```
   show ntp status | include synchronized
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1365 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1366
**Alarm Name:** SNMP Agent Out of Sync
**Severity:** Minor

This alarm indicates a out of sync condition on the snmp agent subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1366 for 'SNMP Agent Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp trap-host
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show snmp statistics` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear snmp statistics
   ```
6. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp statistics | include packets-received
   ```

---

## Procedure to clear ALARM_CODE_1367
**Alarm Name:** VRRP Group Hardware Failure
**Severity:** Critical

This alarm indicates a hardware failure condition on the vrrp group subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1367 for 'VRRP Group Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show vrrp statistics
   ```
3. **Hardware Status Check:** Run `show vrrp statistics` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected vrrp group unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear vrrp statistics
   ```
7. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show vrrp | include Master
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1367 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1368
**Alarm Name:** VRRP Group Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the vrrp group subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1368 for 'VRRP Group Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show vrrp interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show vrrp`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear vrrp statistics
   ```
5. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show vrrp | include Master
   ```

---

## Procedure to clear ALARM_CODE_1369
**Alarm Name:** Routing Engine CPU Memory Leak Detected
**Severity:** Major

This alarm indicates a memory leak detected condition on the routing engine cpu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1369 for 'Routing Engine CPU Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system cpu-usage
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show system memory`.
4. **⚠️ WARNING: Service Impact Possible.** If the routing engine cpu utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear system cpu-usage history
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show system cpu-usage | include idle
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1369 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1370
**Alarm Name:** OSPF Adjacency Down
**Severity:** Critical

This alarm indicates a down condition on the ospf adjacency subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1370 for 'OSPF Adjacency Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf neighbor
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show ospf interface` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ospf {pid}
  area 0.0.0.0 interface {intf}
  commit
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | include Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1370 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1371
**Alarm Name:** Power Supply Unit (PSU) Flapping
**Severity:** Minor

This alarm indicates a flapping condition on the power supply unit (psu) subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1371 for 'Power Supply Unit (PSU) Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis power-shelf
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show chassis environment` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin chassis power-shelf {shelf} power-module {mod} restart
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show chassis power-shelf | include OK
   ```

---

## Procedure to clear ALARM_CODE_1372
**Alarm Name:** IS-IS Adjacency Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the is-is adjacency subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1372 for 'IS-IS Adjacency Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis adjacency
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show isis database`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear isis adjacency
   ```
5. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | include Up
   ```

---

## Procedure to clear ALARM_CODE_1373
**Alarm Name:** Management Ethernet Configuration Mismatch
**Severity:** Major

This alarm indicates a configuration mismatch condition on the management ethernet subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1373 for 'Management Ethernet Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface mgmt
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show system information` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp interface mgmt
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface mgmt | include up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1373 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1374
**Alarm Name:** Power Supply Unit (PSU) Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the power supply unit (psu) subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1374 for 'Power Supply Unit (PSU) Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis power-shelf
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show chassis environment` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin chassis power-shelf {shelf} power-module {mod} restart
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show chassis power-shelf | include OK
   ```

---

## Procedure to clear ALARM_CODE_1375
**Alarm Name:** Routing Engine CPU Timeout
**Severity:** Major

This alarm indicates a timeout condition on the routing engine cpu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1375 for 'Routing Engine CPU Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system memory
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show system processes top` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear system cpu-usage history
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show system cpu-usage | include idle
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1375 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1376
**Alarm Name:** LACP Bundle Performance Degraded
**Severity:** Warning

This alarm indicates a performance degraded condition on the lacp bundle subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1376 for 'LACP Bundle Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port {port} detail
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show port {port} detail`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  port lag {id}
  admin-state enable
  commit
   ```
5. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show port lag | include active
   ```

---

## Procedure to clear ALARM_CODE_1377
**Alarm Name:** NTP Synchronization Resource Exhaustion
**Severity:** Critical

This alarm indicates a resource exhaustion condition on the ntp synchronization subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1377 for 'NTP Synchronization Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ntp status
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ntp associations`.
4. **⚠️ WARNING: Service Impact Possible.** If the ntp synchronization utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  ntp server {ip} prefer
  commit
   ```
6. **Post-Recovery Validation:** Verify the ntp synchronization has returned to a stable operational state:
   ```
   show ntp status | include synchronized
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1377 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1378
**Alarm Name:** Line Card NPU Down
**Severity:** Critical

This alarm indicates a down condition on the line card npu subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1378 for 'Line Card NPU Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system processes
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show chassis environment` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin chassis card {card} restart
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show chassis card | include Online
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1378 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1379
**Alarm Name:** BGP Peer High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the bgp peer subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1379 for 'BGP Peer High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp summary
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bgp summary`.
4. **⚠️ WARNING: Service Impact Possible.** If the bgp peer utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router bgp {asn}
  neighbor {ip}
  admin-state enable
  commit
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | include Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1379 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1380
**Alarm Name:** QoS Scheduler High CRC Rate
**Severity:** Major

This alarm indicates a high crc rate condition on the qos scheduler subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1380 for 'QoS Scheduler High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show qos policy-map applied
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show qos policy-map applied`.
4. **⚠️ WARNING: Service Impact Possible.** If the qos scheduler utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  qos policy-map PM_CORE
  class default bandwidth-percent 60
  commit
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   show qos interface {intf} statistics | include conform
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1380 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1381
**Alarm Name:** Management Ethernet Down
**Severity:** Minor

This alarm indicates a down condition on the management ethernet subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1381 for 'Management Ethernet Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface mgmt
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show system information` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp interface mgmt
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface mgmt | include up
   ```

---

## Procedure to clear ALARM_CODE_1382
**Alarm Name:** VRRP Group Out of Sync
**Severity:** Major

This alarm indicates a out of sync condition on the vrrp group subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1382 for 'VRRP Group Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show vrrp interface
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show vrrp statistics` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router vrrp {id}
  priority 150
  preempt
  admin-state enable
  commit
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show vrrp | include Master
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1382 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1383
**Alarm Name:** Routing Engine CPU Hardware Failure
**Severity:** Critical

This alarm indicates a hardware failure condition on the routing engine cpu subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1383 for 'Routing Engine CPU Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system cpu-usage
   ```
3. **Hardware Status Check:** Run `show system cpu-usage` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected routing engine cpu unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear system cpu-usage history
   ```
7. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show system cpu-usage | include idle
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1383 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1384
**Alarm Name:** BFD Session Down
**Severity:** Critical

This alarm indicates a down condition on the bfd session subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1384 for 'BFD Session Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session detail
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show bfd session detail` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  bfd interface {intf} receive-interval 300 transmit-interval 300
  commit
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1384 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1385
**Alarm Name:** VRRP Group Timeout
**Severity:** Critical

This alarm indicates a timeout condition on the vrrp group subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1385 for 'VRRP Group Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show vrrp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show vrrp` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show vrrp | include Master
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1385 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1386
**Alarm Name:** LACP Bundle Timeout
**Severity:** Major

This alarm indicates a timeout condition on the lacp bundle subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1386 for 'LACP Bundle Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port {port} detail
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show port {port} detail` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  port lag {id}
  admin-state enable
  commit
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show port lag | include active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1386 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1387
**Alarm Name:** VRRP Group Loss of Signal (LOS)
**Severity:** Minor

This alarm indicates a loss of signal (los) condition on the vrrp group subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1387 for 'VRRP Group Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show vrrp statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show vrrp` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router vrrp {id}
  priority 150
  preempt
  admin-state enable
  commit
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show vrrp | include Master
   ```

---

## Procedure to clear ALARM_CODE_1388
**Alarm Name:** Line Card NPU Out of Sync
**Severity:** Minor

This alarm indicates a out of sync condition on the line card npu subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1388 for 'Line Card NPU Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis card
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show chassis environment` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear port hardware {card}
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show chassis card | include Online
   ```

---

## Procedure to clear ALARM_CODE_1389
**Alarm Name:** QoS Scheduler Authentication Failed
**Severity:** Major

This alarm indicates a authentication failed condition on the qos scheduler subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1389 for 'QoS Scheduler Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show qos interface {intf} statistics
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show qos policy-map applied` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear qos interface {intf} statistics
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   show qos interface {intf} statistics | include conform
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1389 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1390
**Alarm Name:** OSPF Adjacency Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the ospf adjacency subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1390 for 'OSPF Adjacency Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf area
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show ospf interface` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ospf {pid}
  area 0.0.0.0 interface {intf}
  commit
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | include Full
   ```

---

## Procedure to clear ALARM_CODE_1391
**Alarm Name:** BGP Peer Out of Sync
**Severity:** Warning

This alarm indicates a out of sync condition on the bgp peer subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1391 for 'BGP Peer Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp summary
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show bgp neighbor {ip} detail` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bgp neighbor {ip}
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | include Established
   ```

---

## Procedure to clear ALARM_CODE_1392
**Alarm Name:** Management Ethernet Memory Leak Detected
**Severity:** Critical

This alarm indicates a memory leak detected condition on the management ethernet subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1392 for 'Management Ethernet Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface mgmt
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show interface mgmt`.
4. **⚠️ WARNING: Service Impact Possible.** If the management ethernet utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp interface mgmt
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface mgmt | include up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1392 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1393
**Alarm Name:** NTP Synchronization Down
**Severity:** Critical

This alarm indicates a down condition on the ntp synchronization subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1393 for 'NTP Synchronization Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ntp status
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show ntp associations` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ntp drift
   ```
6. **Post-Recovery Validation:** Verify the ntp synchronization has returned to a stable operational state:
   ```
   show ntp status | include synchronized
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1393 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1394
**Alarm Name:** Optical Rx Power Flapping
**Severity:** Major

This alarm indicates a flapping condition on the optical rx power subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1394 for 'Optical Rx Power Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port {port} optical-power
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show port {port} optical-power` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  port {port}
  admin-state disable
  admin-state enable
  commit
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port {port} transceiver detail | include Rx
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1394 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1395
**Alarm Name:** IS-IS Adjacency Capacity Limit Reached
**Severity:** Critical

This alarm indicates a capacity limit reached condition on the is-is adjacency subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1395 for 'IS-IS Adjacency Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis spf-log
   ```
3. **Hardware Status Check:** Run `show isis adjacency` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected is-is adjacency unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router isis {tag}
  interface {intf} circuit-type level-2
  commit
   ```
7. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | include Up
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1395 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1396
**Alarm Name:** Optical Rx Power Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the optical rx power subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1396 for 'Optical Rx Power Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port {port} transceiver detail
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show port {port} optical-power`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  port {port}
  admin-state disable
  admin-state enable
  commit
   ```
5. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port {port} transceiver detail | include Rx
   ```

---

## Procedure to clear ALARM_CODE_1397
**Alarm Name:** OSPF Adjacency Threshold Exceeded
**Severity:** Minor

This alarm indicates a threshold exceeded condition on the ospf adjacency subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1397 for 'OSPF Adjacency Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ospf area`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  router ospf {pid}
  area 0.0.0.0 interface {intf}
  commit
   ```
5. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | include Full
   ```

---

## Procedure to clear ALARM_CODE_1398
**Alarm Name:** MPLS LDP Session Timeout
**Severity:** Critical

This alarm indicates a timeout condition on the mpls ldp session subsystem of Ericsson equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1398 for 'MPLS LDP Session Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp session
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show mpls ldp session` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear mpls ldp session {ip}
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp session | include Operational
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Ericsson TAC (Technical Assistance Center) with the alarm code 1398 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1399
**Alarm Name:** Management Ethernet Flapping
**Severity:** Warning

This alarm indicates a flapping condition on the management ethernet subsystem of Ericsson equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Ericsson NMS dashboard and confirm alarm code 1399 for 'Management Ethernet Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface mgmt
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show interface mgmt` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure
  interface mgmt
  no shutdown
  commit
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface mgmt | include up
   ```

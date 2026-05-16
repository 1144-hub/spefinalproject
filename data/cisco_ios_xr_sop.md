# Cisco IOS-XR Service Restoration MOP (Method of Procedure)

**Equipment Vendor:** Cisco
**Document Type:** Standard Operating Procedure (SOP)
**Scope:** IOS-XR Troubleshooting (ASR 9000 / NCS 5500 Series)
**Network Topology Context:** Provider Edge (PE) Router

## Overview
This document outlines the standard procedural steps to identify, troubleshoot, and resolve common network alarms on Cisco IOS-XR routers acting as Provider Edge (PE) nodes. If an alarm occurs on an Edge Router connected to a Customer Edge (CE) switch, do not reset the core-facing interface without verifying SLA tags first. All procedures must be followed sequentially. Do not skip any mandatory steps. Obtain Change Advisory Board (CAB) approval before executing any configuration changes on production routers.

---

## Procedure to clear ALARM_CODE_301
**Alarm Name:** OSPF Neighbor Down (Authentication Mismatch)
**Severity:** Critical

This alarm triggers when an OSPF adjacency fails to form due to an MD5 authentication key mismatch between two directly connected IOS-XR routers. Traffic will black-hole until the adjacency is restored.

1. **Confirm the Alarm:** Run `show ospf neighbor` on the affected router to verify the neighbor is stuck in INIT or DOWN state.
2. **Check OSPF Logs:** Review OSPF-specific logs by running `show logging | include OSPF` to identify authentication failure messages and the timestamp of the last successful adjacency.
3. **Verify Interface Configuration:** Run `show running-config router ospf <process-id> area <area-id> interface <interface-name>` and confirm the `authentication message-digest` and `message-digest-key <key-id> md5` lines are present.
4. **Compare Keys with Peer:** Contact the administrator of the peer router and compare the MD5 key ID and key string. Both sides must match exactly (key ID and key value).
5. **Update Key if Mismatch Found:** Enter configuration mode:
   ```
   configure terminal
   router ospf <process-id>
   area <area-id>
   interface <interface-name>
   message-digest-key <key-id> md5 <NEW_MATCHING_KEY>
   commit
   end
   ```
6. **Clear OSPF Process:** Run `clear ospf <process-id> process` to force adjacency renegotiation. **Warning:** This will momentarily disrupt all OSPF adjacencies on this process.
7. **Final Verification:** Run `show ospf neighbor` and confirm the neighbor state transitions to FULL. Verify traffic restoration with `show cef ipv4 adjacency <peer-ip>`.

---

## Procedure to clear ALARM_CODE_302
**Alarm Name:** Interface CRC Error Threshold Exceeded
**Severity:** Major

This alarm indicates that the Cyclic Redundancy Check (CRC) error counter on a physical interface has exceeded the threshold of 1000 errors per 5-minute interval, indicating potential Layer 1 (physical) issues such as a damaged fiber, dirty optic, or faulty SFP transceiver.

1. **Check Error Counters:** Run `show interface <interface-name> | include CRC` to view the current CRC error count and the rate of increase.
2. **Baseline the Error Rate:** Run `show interface <interface-name> accounting` and note the current counters. Wait 60 seconds, then run the command again. Calculate the delta to determine if errors are actively incrementing.
3. **Check Optical Power Levels:** Run `show controllers optics <interface-name>` and verify both Tx and Rx power levels are within the SFP vendor's specified operating range (typically between -1 dBm and -12 dBm for short-reach optics).
4. **Physical Layer Inspection:** If Rx power is below the acceptable threshold, dispatch a technician to:
   - Inspect the fiber patch cord for bends or damage.
   - Clean both fiber end-faces using a one-click fiber cleaner tool.
   - Verify the fiber is seated correctly in the SFP cage.
5. **Re-seat the SFP Module:** If cleaning does not resolve the issue, have the technician carefully remove and re-insert the SFP transceiver module. Run `show inventory | include <slot>` to confirm the SFP is re-detected.
6. **Replace SFP if Persistent:** If CRC errors continue after re-seating, replace the SFP module with a Cisco-compatible spare. Run `show controllers optics <interface-name>` to verify the new SFP reports normal Tx/Rx power.
7. **Clear Counters and Monitor:** Run `clear counters <interface-name>` and monitor for 15 minutes using `show interface <interface-name> | include CRC` to confirm errorscount remains at zero.
8. **Escalate if Unresolved:** If CRC errors persist after SFP replacement, the issue is likely in the fiber plant (damaged trunk fiber). Escalate to the Fiber/Transport team with the optical power readings and error timestamps.


---

## Procedure to clear ALARM_CODE_1000
**Alarm Name:** MPLS LDP Session Out of Sync
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1000 representing 'MPLS LDP Session Out of Sync' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1001
**Alarm Name:** MAC Address Table Loss of Signal (LOS)
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1001 representing 'MAC Address Table Loss of Signal (LOS)' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1002
**Alarm Name:** SNMP Agent Down
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1002 representing 'SNMP Agent Down' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1003
**Alarm Name:** IGMP Snooping Down
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1003 representing 'IGMP Snooping Down' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1004
**Alarm Name:** MPLS LDP Session Hardware Failure
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1004 representing 'MPLS LDP Session Hardware Failure' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1005
**Alarm Name:** ACL Processing High Cyclic Redundancy (CRC) Rate
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1005 representing 'ACL Processing High Cyclic Redundancy (CRC) Rate' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1006
**Alarm Name:** Management Ethernet Memory Leak Detected
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1006 representing 'Management Ethernet Memory Leak Detected' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1007
**Alarm Name:** STP Root Topology Configuration Mismatch
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1007 representing 'STP Root Topology Configuration Mismatch' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1008
**Alarm Name:** GRE Tunnel Authentication Failed
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1008 representing 'GRE Tunnel Authentication Failed' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1009
**Alarm Name:** Optical Rx Power Timeout
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1009 representing 'Optical Rx Power Timeout' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1010
**Alarm Name:** OSPF Adjacency Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1010 representing 'OSPF Adjacency Resource Exhaustion' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1011
**Alarm Name:** BFD Session High Cyclic Redundancy (CRC) Rate
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1011 representing 'BFD Session High Cyclic Redundancy (CRC) Rate' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1012
**Alarm Name:** BFD Session Flapping
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1012 representing 'BFD Session Flapping' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1013
**Alarm Name:** VRRP Group Capacity Limit Reached
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1013 representing 'VRRP Group Capacity Limit Reached' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1014
**Alarm Name:** QoS Scheduler Memory Leak Detected
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1014 representing 'QoS Scheduler Memory Leak Detected' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1015
**Alarm Name:** QoS Scheduler Resource Exhaustion
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1015 representing 'QoS Scheduler Resource Exhaustion' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1016
**Alarm Name:** LACP Bundle Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1016 representing 'LACP Bundle Resource Exhaustion' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1017
**Alarm Name:** RSVP-TE Tunnel Flapping
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1017 representing 'RSVP-TE Tunnel Flapping' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1018
**Alarm Name:** QoS Scheduler High Cyclic Redundancy (CRC) Rate
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1018 representing 'QoS Scheduler High Cyclic Redundancy (CRC) Rate' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1019
**Alarm Name:** Switch Fabric Module Memory Leak Detected
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1019 representing 'Switch Fabric Module Memory Leak Detected' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1020
**Alarm Name:** Line Card NPU Authentication Failed
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1020 representing 'Line Card NPU Authentication Failed' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1021
**Alarm Name:** OSPF Adjacency Stuck in INIT State
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1021 representing 'OSPF Adjacency Stuck in INIT State' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1022
**Alarm Name:** Power Supply Unit (PSU) Stuck in INIT State
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1022 representing 'Power Supply Unit (PSU) Stuck in INIT State' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1023
**Alarm Name:** BFD Session Stuck in INIT State
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1023 representing 'BFD Session Stuck in INIT State' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1024
**Alarm Name:** MPLS LDP Session Flapping
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1024 representing 'MPLS LDP Session Flapping' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1025
**Alarm Name:** Fan Tray Assembly Configuration Mismatch
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1025 representing 'Fan Tray Assembly Configuration Mismatch' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1026
**Alarm Name:** Power Supply Unit (PSU) Memory Leak Detected
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1026 representing 'Power Supply Unit (PSU) Memory Leak Detected' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1027
**Alarm Name:** GRE Tunnel Threshold Exceeded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1027 representing 'GRE Tunnel Threshold Exceeded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1028
**Alarm Name:** ARP Cache Performance Degraded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1028 representing 'ARP Cache Performance Degraded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1029
**Alarm Name:** Multicast PIM Neighbor Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1029 representing 'Multicast PIM Neighbor Performance Degraded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1030
**Alarm Name:** HSRP Instance Threshold Exceeded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1030 representing 'HSRP Instance Threshold Exceeded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1031
**Alarm Name:** IGMP Snooping Configuration Mismatch
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1031 representing 'IGMP Snooping Configuration Mismatch' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1032
**Alarm Name:** Management Ethernet Configuration Mismatch
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1032 representing 'Management Ethernet Configuration Mismatch' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1033
**Alarm Name:** Routing Engine CPU Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1033 representing 'Routing Engine CPU Performance Degraded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1034
**Alarm Name:** OSPF Adjacency Out of Sync
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1034 representing 'OSPF Adjacency Out of Sync' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1035
**Alarm Name:** LACP Bundle Hardware Failure
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1035 representing 'LACP Bundle Hardware Failure' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1036
**Alarm Name:** Power Supply Unit (PSU) High Cyclic Redundancy (CRC) Rate
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1036 representing 'Power Supply Unit (PSU) High Cyclic Redundancy (CRC) Rate' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1037
**Alarm Name:** IS-IS Adjacency Out of Sync
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1037 representing 'IS-IS Adjacency Out of Sync' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1038
**Alarm Name:** NTP Synchronization Down
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1038 representing 'NTP Synchronization Down' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1039
**Alarm Name:** RSVP-TE Tunnel Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1039 representing 'RSVP-TE Tunnel Resource Exhaustion' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1040
**Alarm Name:** Fan Tray Assembly Timeout
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1040 representing 'Fan Tray Assembly Timeout' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1041
**Alarm Name:** SNMP Agent High Cyclic Redundancy (CRC) Rate
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1041 representing 'SNMP Agent High Cyclic Redundancy (CRC) Rate' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1042
**Alarm Name:** SNMP Agent Memory Leak Detected
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1042 representing 'SNMP Agent Memory Leak Detected' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1043
**Alarm Name:** BGP Route Reflector Out of Sync
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1043 representing 'BGP Route Reflector Out of Sync' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1044
**Alarm Name:** Power Supply Unit (PSU) Configuration Mismatch
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1044 representing 'Power Supply Unit (PSU) Configuration Mismatch' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1045
**Alarm Name:** OSPF Adjacency Authentication Failed
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1045 representing 'OSPF Adjacency Authentication Failed' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1046
**Alarm Name:** Power Supply Unit (PSU) Down
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1046 representing 'Power Supply Unit (PSU) Down' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1047
**Alarm Name:** DHCP Relay Agent Capacity Limit Reached
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1047 representing 'DHCP Relay Agent Capacity Limit Reached' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1048
**Alarm Name:** EVPN MAC Route Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1048 representing 'EVPN MAC Route Performance Degraded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1049
**Alarm Name:** IS-IS Adjacency Capacity Limit Reached
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1049 representing 'IS-IS Adjacency Capacity Limit Reached' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1050
**Alarm Name:** Multicast PIM Neighbor Authentication Failed
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1050 representing 'Multicast PIM Neighbor Authentication Failed' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1051
**Alarm Name:** Power Supply Unit (PSU) Performance Degraded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1051 representing 'Power Supply Unit (PSU) Performance Degraded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1052
**Alarm Name:** Switch Fabric Module Out of Sync
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1052 representing 'Switch Fabric Module Out of Sync' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1053
**Alarm Name:** OSPF Adjacency Memory Leak Detected
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1053 representing 'OSPF Adjacency Memory Leak Detected' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1054
**Alarm Name:** BGP Peer Flapping
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1054 representing 'BGP Peer Flapping' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1055
**Alarm Name:** Line Card NPU Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1055 representing 'Line Card NPU Threshold Exceeded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1056
**Alarm Name:** ACL Processing Hardware Failure
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1056 representing 'ACL Processing Hardware Failure' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1057
**Alarm Name:** BGP Peer Timeout
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1057 representing 'BGP Peer Timeout' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1058
**Alarm Name:** STP Root Topology Authentication Failed
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1058 representing 'STP Root Topology Authentication Failed' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1059
**Alarm Name:** IS-IS Adjacency Hardware Failure
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1059 representing 'IS-IS Adjacency Hardware Failure' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1060
**Alarm Name:** BFD Session Capacity Limit Reached
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1060 representing 'BFD Session Capacity Limit Reached' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1061
**Alarm Name:** MPLS LDP Session Timeout
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1061 representing 'MPLS LDP Session Timeout' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1062
**Alarm Name:** EVPN MAC Route High Cyclic Redundancy (CRC) Rate
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1062 representing 'EVPN MAC Route High Cyclic Redundancy (CRC) Rate' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1063
**Alarm Name:** OSPF Adjacency Capacity Limit Reached
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1063 representing 'OSPF Adjacency Capacity Limit Reached' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1064
**Alarm Name:** SNMP Agent Configuration Mismatch
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1064 representing 'SNMP Agent Configuration Mismatch' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1065
**Alarm Name:** OSPF Adjacency High Cyclic Redundancy (CRC) Rate
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1065 representing 'OSPF Adjacency High Cyclic Redundancy (CRC) Rate' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1066
**Alarm Name:** DHCP Relay Agent Authentication Failed
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1066 representing 'DHCP Relay Agent Authentication Failed' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1067
**Alarm Name:** MPLS LDP Session Capacity Limit Reached
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1067 representing 'MPLS LDP Session Capacity Limit Reached' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1068
**Alarm Name:** ACL Processing Performance Degraded
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1068 representing 'ACL Processing Performance Degraded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1069
**Alarm Name:** LACP Bundle Unreachable
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1069 representing 'LACP Bundle Unreachable' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1070
**Alarm Name:** NTP Synchronization Flapping
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1070 representing 'NTP Synchronization Flapping' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1071
**Alarm Name:** Radius/TACACS Auth Down
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1071 representing 'Radius/TACACS Auth Down' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1072
**Alarm Name:** MAC Address Table Timeout
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1072 representing 'MAC Address Table Timeout' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1073
**Alarm Name:** IS-IS Adjacency Down
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1073 representing 'IS-IS Adjacency Down' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1074
**Alarm Name:** Multicast PIM Neighbor Unreachable
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1074 representing 'Multicast PIM Neighbor Unreachable' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1075
**Alarm Name:** BFD Session Unreachable
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1075 representing 'BFD Session Unreachable' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1076
**Alarm Name:** Optical Rx Power Capacity Limit Reached
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1076 representing 'Optical Rx Power Capacity Limit Reached' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1077
**Alarm Name:** Line Card NPU Out of Sync
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1077 representing 'Line Card NPU Out of Sync' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1078
**Alarm Name:** IS-IS Adjacency Unreachable
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1078 representing 'IS-IS Adjacency Unreachable' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1079
**Alarm Name:** Routing Engine CPU Authentication Failed
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1079 representing 'Routing Engine CPU Authentication Failed' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1080
**Alarm Name:** Multicast PIM Neighbor Hardware Failure
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1080 representing 'Multicast PIM Neighbor Hardware Failure' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1081
**Alarm Name:** GRE Tunnel Out of Sync
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1081 representing 'GRE Tunnel Out of Sync' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1082
**Alarm Name:** SNMP Agent Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1082 representing 'SNMP Agent Stuck in INIT State' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1083
**Alarm Name:** Switch Fabric Module Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1083 representing 'Switch Fabric Module Threshold Exceeded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1084
**Alarm Name:** ARP Cache Resource Exhaustion
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1084 representing 'ARP Cache Resource Exhaustion' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1085
**Alarm Name:** NTP Synchronization Performance Degraded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1085 representing 'NTP Synchronization Performance Degraded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1086
**Alarm Name:** Routing Engine CPU High Cyclic Redundancy (CRC) Rate
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1086 representing 'Routing Engine CPU High Cyclic Redundancy (CRC) Rate' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1087
**Alarm Name:** ACL Processing Authentication Failed
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1087 representing 'ACL Processing Authentication Failed' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1088
**Alarm Name:** STP Root Topology Threshold Exceeded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1088 representing 'STP Root Topology Threshold Exceeded' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1089
**Alarm Name:** Routing Engine CPU Timeout
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1089 representing 'Routing Engine CPU Timeout' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1090
**Alarm Name:** MPLS LDP Session Resource Exhaustion
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1090 representing 'MPLS LDP Session Resource Exhaustion' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1091
**Alarm Name:** Power Supply Unit (PSU) Authentication Failed
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1091 representing 'Power Supply Unit (PSU) Authentication Failed' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1092
**Alarm Name:** Fan Tray Assembly Down
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1092 representing 'Fan Tray Assembly Down' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1093
**Alarm Name:** MPLS LDP Session Unreachable
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1093 representing 'MPLS LDP Session Unreachable' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1094
**Alarm Name:** VRRP Group Configuration Mismatch
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1094 representing 'VRRP Group Configuration Mismatch' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1095
**Alarm Name:** VPLS Pseudowire Capacity Limit Reached
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1095 representing 'VPLS Pseudowire Capacity Limit Reached' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1096
**Alarm Name:** OAM Connectivity Out of Sync
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1096 representing 'OAM Connectivity Out of Sync' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1097
**Alarm Name:** MAC Address Table Resource Exhaustion
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1097 representing 'MAC Address Table Resource Exhaustion' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1098
**Alarm Name:** MAC Address Table Down
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1098 representing 'MAC Address Table Down' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1099
**Alarm Name:** ARP Cache High Cyclic Redundancy (CRC) Rate
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1099 representing 'ARP Cache High Cyclic Redundancy (CRC) Rate' on the Cisco NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show running-config
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear ip route *
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.


<!-- BEGIN GENERATED PROCEDURES -->

---

## Procedure to clear ALARM_CODE_1000
**Alarm Name:** Power Supply Unit (PSU) Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the power supply unit (psu) subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1000 for 'Power Supply Unit (PSU) Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show platform
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show environment power` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   power disable module {slot}
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show environment power | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1001
**Alarm Name:** RSVP-TE Tunnel Performance Degraded
**Severity:** Minor

This alarm indicates a performance degraded condition on the rsvp-te tunnel subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1001 for 'RSVP-TE Tunnel Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show rsvp interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls traffic-eng tunnels brief`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear rsvp session tunnel-id {id}
   ```
5. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show mpls traffic-eng tunnels | include Up
   ```

---

## Procedure to clear ALARM_CODE_1002
**Alarm Name:** BGP Peer Memory Leak Detected
**Severity:** Critical

This alarm indicates a memory leak detected condition on the bgp peer subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1002 for 'BGP Peer Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp neighbors {ip} detail
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bgp ipv4 unicast summary`.
4. **⚠️ WARNING: Service Impact Possible.** If the bgp peer utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   router bgp 65000
  neighbor {ip} activate
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp ipv4 unicast summary | include Estab
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1002 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1003
**Alarm Name:** MPLS LDP Session Hardware Failure
**Severity:** Warning

This alarm indicates a hardware failure condition on the mpls ldp session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1003 for 'MPLS LDP Session Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls forwarding-table
   ```
3. **Hardware Status Check:** Run `show mpls ldp discovery` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected mpls ldp session unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   mpls ldp router-id Loopback0 force
   ```
7. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp neighbor | include Oper
   ```

---

## Procedure to clear ALARM_CODE_1004
**Alarm Name:** LACP Bundle Authentication Failed
**Severity:** Critical

This alarm indicates a authentication failed condition on the lacp bundle subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1004 for 'LACP Bundle Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bundle Bundle-Ether1
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show lacp neighbor` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface Bundle-Ether1
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show bundle Bundle-Ether1 | include Active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1004 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1005
**Alarm Name:** MPLS LDP Session Authentication Failed
**Severity:** Minor

This alarm indicates a authentication failed condition on the mpls ldp session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1005 for 'MPLS LDP Session Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp discovery
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show mpls ldp neighbor` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   mpls ldp router-id Loopback0 force
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp neighbor | include Oper
   ```

---

## Procedure to clear ALARM_CODE_1006
**Alarm Name:** Management Ethernet Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the management ethernet subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1006 for 'Management Ethernet Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip interface brief
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ip interface brief`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp
   ```
5. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0 | include up/up
   ```

---

## Procedure to clear ALARM_CODE_1007
**Alarm Name:** Power Supply Unit (PSU) Hardware Failure
**Severity:** Minor

This alarm indicates a hardware failure condition on the power supply unit (psu) subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1007 for 'Power Supply Unit (PSU) Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show environment power
   ```
3. **Hardware Status Check:** Run `show redundancy` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected power supply unit (psu) unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   power enable module {slot}
   ```
7. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show environment power | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1008
**Alarm Name:** RSVP-TE Tunnel Hardware Failure
**Severity:** Critical

This alarm indicates a hardware failure condition on the rsvp-te tunnel subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1008 for 'RSVP-TE Tunnel Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show rsvp session
   ```
3. **Hardware Status Check:** Run `show rsvp interface` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected rsvp-te tunnel unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear rsvp session tunnel-id {id}
   ```
7. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show mpls traffic-eng tunnels | include Up
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1008 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1009
**Alarm Name:** Line Card NPU Stuck in INIT State
**Severity:** Critical

This alarm indicates a stuck in init state condition on the line card npu subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1009 for 'Line Card NPU Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show controllers npu resources all location 0/0/CPU0
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show controllers npu resources all location 0/0/CPU0` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin clear controller fabric plane all
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show platform | include IOS XR RUN
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1009 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1010
**Alarm Name:** LACP Bundle Hardware Failure
**Severity:** Minor

This alarm indicates a hardware failure condition on the lacp bundle subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1010 for 'LACP Bundle Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lacp neighbor
   ```
3. **Hardware Status Check:** Run `show bundle Bundle-Ether1` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected lacp bundle unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear lacp counters
   ```
7. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show bundle Bundle-Ether1 | include Active
   ```

---

## Procedure to clear ALARM_CODE_1011
**Alarm Name:** RSVP-TE Tunnel Configuration Mismatch
**Severity:** Major

This alarm indicates a configuration mismatch condition on the rsvp-te tunnel subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1011 for 'RSVP-TE Tunnel Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show rsvp session
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show rsvp session` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear rsvp session tunnel-id {id}
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show mpls traffic-eng tunnels | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1011 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1012
**Alarm Name:** Line Card NPU Capacity Limit Reached
**Severity:** Major

This alarm indicates a capacity limit reached condition on the line card npu subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1012 for 'Line Card NPU Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show platform
   ```
3. **Hardware Status Check:** Run `show platform` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected line card npu unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   hw-module location 0/0/CPU0 reload
   ```
7. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show platform | include IOS XR RUN
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1012 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1013
**Alarm Name:** NTP Synchronization Timeout
**Severity:** Major

This alarm indicates a timeout condition on the ntp synchronization subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1013 for 'NTP Synchronization Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ntp status
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show ntp associations` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ntp drift
   ```
6. **Post-Recovery Validation:** Verify the ntp synchronization has returned to a stable operational state:
   ```
   show ntp status | include synchronized
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1013 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1014
**Alarm Name:** SNMP Agent Stuck in INIT State
**Severity:** Major

This alarm indicates a stuck in init state condition on the snmp agent subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1014 for 'SNMP Agent Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp traps
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show snmp` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   snmp-server community TELECOM_RO RO
   ```
6. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp | include packets
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1014 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1015
**Alarm Name:** MPLS LDP Session Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the mpls ldp session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1015 for 'MPLS LDP Session Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp neighbor
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show mpls ldp discovery` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   mpls ldp router-id Loopback0 force
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp neighbor | include Oper
   ```

---

## Procedure to clear ALARM_CODE_1016
**Alarm Name:** Management Ethernet Down
**Severity:** Major

This alarm indicates a down condition on the management ethernet subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1016 for 'Management Ethernet Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip interface brief
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show ip interface brief` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface MgmtEth0/RSP0/CPU0/0
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0 | include up/up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1016 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1017
**Alarm Name:** BFD Session Capacity Limit Reached
**Severity:** Warning

This alarm indicates a capacity limit reached condition on the bfd session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1017 for 'BFD Session Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session detail
   ```
3. **Hardware Status Check:** Run `show bfd counters` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected bfd session unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   bfd interval 300 min_rx 300 multiplier 3
   ```
7. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd neighbors | include Up
   ```

---

## Procedure to clear ALARM_CODE_1018
**Alarm Name:** Optical Rx Power Resource Exhaustion
**Severity:** Critical

This alarm indicates a resource exhaustion condition on the optical rx power subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1018 for 'Optical Rx Power Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show hw-module fpd
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show controllers optics 0/0/0/1`.
4. **⚠️ WARNING: Service Impact Possible.** If the optical rx power utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   controller optics 0/0/0/1
  sec-admin-state normal
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show controllers optics 0/0/0/1 | include Rx
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1018 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1019
**Alarm Name:** Optical Rx Power Flapping
**Severity:** Warning

This alarm indicates a flapping condition on the optical rx power subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1019 for 'Optical Rx Power Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show hw-module fpd
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show controllers optics 0/0/0/1` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   hw-module location 0/0/CPU0 reload
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show controllers optics 0/0/0/1 | include Rx
   ```

---

## Procedure to clear ALARM_CODE_1020
**Alarm Name:** Optical Rx Power Memory Leak Detected
**Severity:** Major

This alarm indicates a memory leak detected condition on the optical rx power subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1020 for 'Optical Rx Power Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show hw-module fpd
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show hw-module fpd`.
4. **⚠️ WARNING: Service Impact Possible.** If the optical rx power utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   hw-module location 0/0/CPU0 reload
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show controllers optics 0/0/0/1 | include Rx
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1020 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1021
**Alarm Name:** LACP Bundle Flapping
**Severity:** Critical

This alarm indicates a flapping condition on the lacp bundle subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1021 for 'LACP Bundle Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lacp neighbor
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show lacp counters` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface Bundle-Ether1
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show bundle Bundle-Ether1 | include Active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1021 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1022
**Alarm Name:** BFD Session Down
**Severity:** Major

This alarm indicates a down condition on the bfd session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1022 for 'BFD Session Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd neighbors
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show bfd neighbors` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bfd counters
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd neighbors | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1022 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1023
**Alarm Name:** Optical Rx Power Authentication Failed
**Severity:** Warning

This alarm indicates a authentication failed condition on the optical rx power subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1023 for 'Optical Rx Power Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show controllers optics 0/0/0/1
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show controllers optics 0/0/0/1` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   hw-module location 0/0/CPU0 reload
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show controllers optics 0/0/0/1 | include Rx
   ```

---

## Procedure to clear ALARM_CODE_1024
**Alarm Name:** Power Supply Unit (PSU) Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the power supply unit (psu) subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1024 for 'Power Supply Unit (PSU) Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show redundancy
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show platform`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   power enable module {slot}
   ```
5. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show environment power | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1025
**Alarm Name:** MPLS LDP Session Resource Exhaustion
**Severity:** Major

This alarm indicates a resource exhaustion condition on the mpls ldp session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1025 for 'MPLS LDP Session Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp neighbor
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls ldp discovery`.
4. **⚠️ WARNING: Service Impact Possible.** If the mpls ldp session utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   mpls ldp router-id Loopback0 force
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp neighbor | include Oper
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1025 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1026
**Alarm Name:** FIB (Forwarding Table) Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the fib (forwarding table) subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1026 for 'FIB (Forwarding Table) Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show cef ipv4 inconsistency
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show cef ipv4 summary` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear cef ipv4 inconsistency
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show cef ipv4 summary | include resolved
   ```

---

## Procedure to clear ALARM_CODE_1027
**Alarm Name:** FIB (Forwarding Table) Resource Exhaustion
**Severity:** Critical

This alarm indicates a resource exhaustion condition on the fib (forwarding table) subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1027 for 'FIB (Forwarding Table) Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show cef ipv4 summary
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show cef ipv4 inconsistency`.
4. **⚠️ WARNING: Service Impact Possible.** If the fib (forwarding table) utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear cef ipv4 inconsistency
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show cef ipv4 summary | include resolved
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1027 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1028
**Alarm Name:** BGP Peer Flapping
**Severity:** Major

This alarm indicates a flapping condition on the bgp peer subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1028 for 'BGP Peer Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip route bgp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show bgp neighbors {ip} detail` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bgp ipv4 unicast {ip} soft in
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp ipv4 unicast summary | include Estab
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1028 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1029
**Alarm Name:** RSVP-TE Tunnel Threshold Exceeded
**Severity:** Major

This alarm indicates a threshold exceeded condition on the rsvp-te tunnel subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1029 for 'RSVP-TE Tunnel Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show rsvp interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show rsvp session`.
4. **⚠️ WARNING: Service Impact Possible.** If the rsvp-te tunnel utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface tunnel-te1
  shutdown
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show mpls traffic-eng tunnels | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1029 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1030
**Alarm Name:** OSPF Adjacency Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the ospf adjacency subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1030 for 'OSPF Adjacency Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip ospf interface brief
   ```
3. **Hardware Status Check:** Run `show ip ospf interface brief` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected ospf adjacency unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface GigabitEthernet0/0/0
  ip ospf cost 10
   ```
7. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ip ospf neighbor | include FULL
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1030 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1031
**Alarm Name:** NTP Synchronization Hardware Failure
**Severity:** Minor

This alarm indicates a hardware failure condition on the ntp synchronization subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1031 for 'NTP Synchronization Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ntp status
   ```
3. **Hardware Status Check:** Run `show clock` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected ntp synchronization unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ntp drift
   ```
7. **Post-Recovery Validation:** Verify the ntp synchronization has returned to a stable operational state:
   ```
   show ntp status | include synchronized
   ```

---

## Procedure to clear ALARM_CODE_1032
**Alarm Name:** Management Ethernet Out of Sync
**Severity:** Major

This alarm indicates a out of sync condition on the management ethernet subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1032 for 'Management Ethernet Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show ip interface brief` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface MgmtEth0/RSP0/CPU0/0
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0 | include up/up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1032 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1033
**Alarm Name:** QoS Scheduler Capacity Limit Reached
**Severity:** Minor

This alarm indicates a capacity limit reached condition on the qos scheduler subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1033 for 'QoS Scheduler Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show policy-map interface te0/0/0/1
   ```
3. **Hardware Status Check:** Run `show qos interface te0/0/0/1` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected qos scheduler unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear qos counters interface te0/0/0/1
   ```
7. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   show policy-map interface te0/0/0/1 | include conform
   ```

---

## Procedure to clear ALARM_CODE_1034
**Alarm Name:** OSPF Adjacency Loss of Signal (LOS)
**Severity:** Critical

This alarm indicates a loss of signal (los) condition on the ospf adjacency subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1034 for 'OSPF Adjacency Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip ospf neighbor
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show ip ospf neighbor` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface GigabitEthernet0/0/0
  ip ospf cost 10
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ip ospf neighbor | include FULL
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1034 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1035
**Alarm Name:** LACP Bundle Performance Degraded
**Severity:** Major

This alarm indicates a performance degraded condition on the lacp bundle subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1035 for 'LACP Bundle Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bundle Bundle-Ether1
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bundle Bundle-Ether1`.
4. **⚠️ WARNING: Service Impact Possible.** If the lacp bundle utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear lacp counters
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show bundle Bundle-Ether1 | include Active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1035 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1036
**Alarm Name:** Line Card NPU Threshold Exceeded
**Severity:** Warning

This alarm indicates a threshold exceeded condition on the line card npu subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1036 for 'Line Card NPU Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show controllers npu resources all location 0/0/CPU0
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show controllers npu resources all location 0/0/CPU0`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin clear controller fabric plane all
   ```
5. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show platform | include IOS XR RUN
   ```

---

## Procedure to clear ALARM_CODE_1037
**Alarm Name:** Power Supply Unit (PSU) Timeout
**Severity:** Minor

This alarm indicates a timeout condition on the power supply unit (psu) subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1037 for 'Power Supply Unit (PSU) Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show environment power
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show platform` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   power disable module {slot}
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show environment power | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1038
**Alarm Name:** BFD Session Performance Degraded
**Severity:** Warning

This alarm indicates a performance degraded condition on the bfd session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1038 for 'BFD Session Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd counters
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bfd neighbors`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bfd counters
   ```
5. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd neighbors | include Up
   ```

---

## Procedure to clear ALARM_CODE_1039
**Alarm Name:** FIB (Forwarding Table) Memory Leak Detected
**Severity:** Major

This alarm indicates a memory leak detected condition on the fib (forwarding table) subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1039 for 'FIB (Forwarding Table) Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show cef ipv4 inconsistency
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show cef ipv4 inconsistency`.
4. **⚠️ WARNING: Service Impact Possible.** If the fib (forwarding table) utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear cef ipv4 inconsistency
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show cef ipv4 summary | include resolved
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1039 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1040
**Alarm Name:** SNMP Agent Hardware Failure
**Severity:** Warning

This alarm indicates a hardware failure condition on the snmp agent subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1040 for 'SNMP Agent Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp
   ```
3. **Hardware Status Check:** Run `show snmp host` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected snmp agent unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   snmp-server host 10.0.0.1 TELECOM_RO
   ```
7. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp | include packets
   ```

---

## Procedure to clear ALARM_CODE_1041
**Alarm Name:** BGP Peer Resource Exhaustion
**Severity:** Minor

This alarm indicates a resource exhaustion condition on the bgp peer subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1041 for 'BGP Peer Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp neighbors {ip} detail
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bgp ipv4 unicast summary`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   router bgp 65000
  neighbor {ip} activate
   ```
5. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp ipv4 unicast summary | include Estab
   ```

---

## Procedure to clear ALARM_CODE_1042
**Alarm Name:** MPLS LDP Session Threshold Exceeded
**Severity:** Major

This alarm indicates a threshold exceeded condition on the mpls ldp session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1042 for 'MPLS LDP Session Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp neighbor
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls ldp discovery`.
4. **⚠️ WARNING: Service Impact Possible.** If the mpls ldp session utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   mpls ldp router-id Loopback0 force
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp neighbor | include Oper
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1042 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1043
**Alarm Name:** Line Card NPU Flapping
**Severity:** Critical

This alarm indicates a flapping condition on the line card npu subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1043 for 'Line Card NPU Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show platform
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show controllers npu resources all location 0/0/CPU0` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin clear controller fabric plane all
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show platform | include IOS XR RUN
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1043 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1044
**Alarm Name:** SNMP Agent High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the snmp agent subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1044 for 'SNMP Agent High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show snmp host`.
4. **⚠️ WARNING: Service Impact Possible.** If the snmp agent utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   snmp-server community TELECOM_RO RO
   ```
6. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp | include packets
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1044 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1045
**Alarm Name:** QoS Scheduler Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the qos scheduler subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1045 for 'QoS Scheduler Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show qos interface te0/0/0/1
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show qos interface te0/0/0/1` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   policy-map PM_CORE
  class class-default
  bandwidth percent 50
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   show policy-map interface te0/0/0/1 | include conform
   ```

---

## Procedure to clear ALARM_CODE_1046
**Alarm Name:** LACP Bundle Resource Exhaustion
**Severity:** Minor

This alarm indicates a resource exhaustion condition on the lacp bundle subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1046 for 'LACP Bundle Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lacp neighbor
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show lacp neighbor`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface Bundle-Ether1
  no shutdown
   ```
5. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show bundle Bundle-Ether1 | include Active
   ```

---

## Procedure to clear ALARM_CODE_1047
**Alarm Name:** OSPF Adjacency Timeout
**Severity:** Critical

This alarm indicates a timeout condition on the ospf adjacency subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1047 for 'OSPF Adjacency Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip ospf database
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show ip ospf database` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ip ospf process
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ip ospf neighbor | include FULL
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1047 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1048
**Alarm Name:** Management Ethernet High CRC Rate
**Severity:** Warning

This alarm indicates a high crc rate condition on the management ethernet subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1048 for 'Management Ethernet High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip interface brief
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show interface MgmtEth0/RSP0/CPU0/0`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface MgmtEth0/RSP0/CPU0/0
  no shutdown
   ```
5. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0 | include up/up
   ```

---

## Procedure to clear ALARM_CODE_1049
**Alarm Name:** IS-IS Adjacency Performance Degraded
**Severity:** Critical

This alarm indicates a performance degraded condition on the is-is adjacency subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1049 for 'IS-IS Adjacency Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis topology
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show isis neighbors`.
4. **⚠️ WARNING: Service Impact Possible.** If the is-is adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear isis process
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis neighbors | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1049 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1050
**Alarm Name:** IS-IS Adjacency Out of Sync
**Severity:** Minor

This alarm indicates a out of sync condition on the is-is adjacency subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1050 for 'IS-IS Adjacency Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis topology
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show isis topology` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   router isis 1
  net 49.0001.0000.0001.00
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis neighbors | include Up
   ```

---

## Procedure to clear ALARM_CODE_1051
**Alarm Name:** Optical Rx Power Threshold Exceeded
**Severity:** Minor

This alarm indicates a threshold exceeded condition on the optical rx power subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1051 for 'Optical Rx Power Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show hw-module fpd
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show hw-module fpd`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   controller optics 0/0/0/1
  sec-admin-state normal
   ```
5. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show controllers optics 0/0/0/1 | include Rx
   ```

---

## Procedure to clear ALARM_CODE_1052
**Alarm Name:** NTP Synchronization Capacity Limit Reached
**Severity:** Warning

This alarm indicates a capacity limit reached condition on the ntp synchronization subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1052 for 'NTP Synchronization Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show clock
   ```
3. **Hardware Status Check:** Run `show ntp associations` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected ntp synchronization unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   ntp server 10.0.0.254 prefer
   ```
7. **Post-Recovery Validation:** Verify the ntp synchronization has returned to a stable operational state:
   ```
   show ntp status | include synchronized
   ```

---

## Procedure to clear ALARM_CODE_1053
**Alarm Name:** LACP Bundle Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the lacp bundle subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1053 for 'LACP Bundle Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lacp neighbor
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bundle Bundle-Ether1`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear lacp counters
   ```
5. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show bundle Bundle-Ether1 | include Active
   ```

---

## Procedure to clear ALARM_CODE_1054
**Alarm Name:** IS-IS Adjacency Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the is-is adjacency subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1054 for 'IS-IS Adjacency Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis neighbors
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show isis topology`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear isis process
   ```
5. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis neighbors | include Up
   ```

---

## Procedure to clear ALARM_CODE_1055
**Alarm Name:** FIB (Forwarding Table) Flapping
**Severity:** Warning

This alarm indicates a flapping condition on the fib (forwarding table) subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1055 for 'FIB (Forwarding Table) Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show cef ipv4 summary
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show cef ipv4 inconsistency` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear route-ha eof
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show cef ipv4 summary | include resolved
   ```

---

## Procedure to clear ALARM_CODE_1056
**Alarm Name:** Power Supply Unit (PSU) Flapping
**Severity:** Critical

This alarm indicates a flapping condition on the power supply unit (psu) subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1056 for 'Power Supply Unit (PSU) Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show platform
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show platform` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   power disable module {slot}
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show environment power | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1056 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1057
**Alarm Name:** RSVP-TE Tunnel Unreachable
**Severity:** Major

This alarm indicates a unreachable condition on the rsvp-te tunnel subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1057 for 'RSVP-TE Tunnel Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show rsvp interface
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show mpls traffic-eng tunnels brief` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface tunnel-te1
  shutdown
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show mpls traffic-eng tunnels | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1057 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1058
**Alarm Name:** IS-IS Adjacency Down
**Severity:** Major

This alarm indicates a down condition on the is-is adjacency subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1058 for 'IS-IS Adjacency Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis database detail
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show isis neighbors` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   router isis 1
  net 49.0001.0000.0001.00
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis neighbors | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1058 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1059
**Alarm Name:** IS-IS Adjacency Capacity Limit Reached
**Severity:** Major

This alarm indicates a capacity limit reached condition on the is-is adjacency subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1059 for 'IS-IS Adjacency Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis neighbors
   ```
3. **Hardware Status Check:** Run `show isis database detail` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected is-is adjacency unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear isis process
   ```
7. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis neighbors | include Up
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1059 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1060
**Alarm Name:** Management Ethernet Flapping
**Severity:** Warning

This alarm indicates a flapping condition on the management ethernet subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1060 for 'Management Ethernet Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show ip interface brief` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0 | include up/up
   ```

---

## Procedure to clear ALARM_CODE_1061
**Alarm Name:** SNMP Agent Timeout
**Severity:** Critical

This alarm indicates a timeout condition on the snmp agent subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1061 for 'SNMP Agent Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show snmp traps` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   snmp-server host 10.0.0.1 TELECOM_RO
   ```
6. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp | include packets
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1061 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1062
**Alarm Name:** QoS Scheduler Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the qos scheduler subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1062 for 'QoS Scheduler Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show qos interface te0/0/0/1
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show qos interface te0/0/0/1`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear qos counters interface te0/0/0/1
   ```
5. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   show policy-map interface te0/0/0/1 | include conform
   ```

---

## Procedure to clear ALARM_CODE_1063
**Alarm Name:** Management Ethernet Configuration Mismatch
**Severity:** Major

This alarm indicates a configuration mismatch condition on the management ethernet subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1063 for 'Management Ethernet Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip interface brief
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show interface MgmtEth0/RSP0/CPU0/0` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface MgmtEth0/RSP0/CPU0/0
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0 | include up/up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1063 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1064
**Alarm Name:** Optical Rx Power Stuck in INIT State
**Severity:** Minor

This alarm indicates a stuck in init state condition on the optical rx power subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1064 for 'Optical Rx Power Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show hw-module fpd
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show controllers optics 0/0/0/1` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   controller optics 0/0/0/1
  sec-admin-state normal
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show controllers optics 0/0/0/1 | include Rx
   ```

---

## Procedure to clear ALARM_CODE_1065
**Alarm Name:** NTP Synchronization Down
**Severity:** Minor

This alarm indicates a down condition on the ntp synchronization subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1065 for 'NTP Synchronization Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ntp status
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show ntp associations` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   ntp server 10.0.0.254 prefer
   ```
6. **Post-Recovery Validation:** Verify the ntp synchronization has returned to a stable operational state:
   ```
   show ntp status | include synchronized
   ```

---

## Procedure to clear ALARM_CODE_1066
**Alarm Name:** BFD Session Memory Leak Detected
**Severity:** Critical

This alarm indicates a memory leak detected condition on the bfd session subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1066 for 'BFD Session Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd counters
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bfd session detail`.
4. **⚠️ WARNING: Service Impact Possible.** If the bfd session utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bfd counters
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd neighbors | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1066 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1067
**Alarm Name:** MPLS LDP Session Down
**Severity:** Minor

This alarm indicates a down condition on the mpls ldp session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1067 for 'MPLS LDP Session Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls forwarding-table
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show mpls forwarding-table` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   mpls ldp router-id Loopback0 force
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp neighbor | include Oper
   ```

---

## Procedure to clear ALARM_CODE_1068
**Alarm Name:** Optical Rx Power Performance Degraded
**Severity:** Critical

This alarm indicates a performance degraded condition on the optical rx power subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1068 for 'Optical Rx Power Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show hw-module fpd
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show hw-module fpd`.
4. **⚠️ WARNING: Service Impact Possible.** If the optical rx power utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   hw-module location 0/0/CPU0 reload
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show controllers optics 0/0/0/1 | include Rx
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1068 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1069
**Alarm Name:** SNMP Agent Out of Sync
**Severity:** Warning

This alarm indicates a out of sync condition on the snmp agent subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1069 for 'SNMP Agent Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show snmp host` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   snmp-server host 10.0.0.1 TELECOM_RO
   ```
6. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp | include packets
   ```

---

## Procedure to clear ALARM_CODE_1070
**Alarm Name:** MPLS LDP Session Flapping
**Severity:** Warning

This alarm indicates a flapping condition on the mpls ldp session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1070 for 'MPLS LDP Session Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp discovery
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show mpls ldp discovery` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear mpls ldp neighbor {ip}
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp neighbor | include Oper
   ```

---

## Procedure to clear ALARM_CODE_1071
**Alarm Name:** OSPF Adjacency Authentication Failed
**Severity:** Major

This alarm indicates a authentication failed condition on the ospf adjacency subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1071 for 'OSPF Adjacency Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip ospf interface brief
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show ip ospf neighbor` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface GigabitEthernet0/0/0
  ip ospf cost 10
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ip ospf neighbor | include FULL
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1071 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1072
**Alarm Name:** MPLS LDP Session Performance Degraded
**Severity:** Warning

This alarm indicates a performance degraded condition on the mpls ldp session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1072 for 'MPLS LDP Session Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp discovery
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls ldp discovery`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear mpls ldp neighbor {ip}
   ```
5. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp neighbor | include Oper
   ```

---

## Procedure to clear ALARM_CODE_1073
**Alarm Name:** Power Supply Unit (PSU) Threshold Exceeded
**Severity:** Minor

This alarm indicates a threshold exceeded condition on the power supply unit (psu) subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1073 for 'Power Supply Unit (PSU) Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show platform
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show platform`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   power enable module {slot}
   ```
5. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show environment power | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1074
**Alarm Name:** Optical Rx Power Capacity Limit Reached
**Severity:** Minor

This alarm indicates a capacity limit reached condition on the optical rx power subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1074 for 'Optical Rx Power Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show controllers optics 0/0/0/1
   ```
3. **Hardware Status Check:** Run `show hw-module fpd` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected optical rx power unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   hw-module location 0/0/CPU0 reload
   ```
7. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show controllers optics 0/0/0/1 | include Rx
   ```

---

## Procedure to clear ALARM_CODE_1075
**Alarm Name:** Management Ethernet Unreachable
**Severity:** Minor

This alarm indicates a unreachable condition on the management ethernet subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1075 for 'Management Ethernet Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show ip interface brief` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0 | include up/up
   ```

---

## Procedure to clear ALARM_CODE_1076
**Alarm Name:** OSPF Adjacency Threshold Exceeded
**Severity:** Critical

This alarm indicates a threshold exceeded condition on the ospf adjacency subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1076 for 'OSPF Adjacency Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip ospf neighbor
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ip ospf neighbor`.
4. **⚠️ WARNING: Service Impact Possible.** If the ospf adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface GigabitEthernet0/0/0
  ip ospf cost 10
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ip ospf neighbor | include FULL
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1076 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1077
**Alarm Name:** Power Supply Unit (PSU) Authentication Failed
**Severity:** Major

This alarm indicates a authentication failed condition on the power supply unit (psu) subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1077 for 'Power Supply Unit (PSU) Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show redundancy
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show environment power` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   power enable module {slot}
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show environment power | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1077 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1078
**Alarm Name:** Management Ethernet Hardware Failure
**Severity:** Critical

This alarm indicates a hardware failure condition on the management ethernet subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1078 for 'Management Ethernet Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0
   ```
3. **Hardware Status Check:** Run `show ip interface brief` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected management ethernet unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp
   ```
7. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0 | include up/up
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1078 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1079
**Alarm Name:** SNMP Agent Performance Degraded
**Severity:** Warning

This alarm indicates a performance degraded condition on the snmp agent subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1079 for 'SNMP Agent Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp host
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show snmp`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   snmp-server host 10.0.0.1 TELECOM_RO
   ```
5. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp | include packets
   ```

---

## Procedure to clear ALARM_CODE_1080
**Alarm Name:** IS-IS Adjacency Authentication Failed
**Severity:** Major

This alarm indicates a authentication failed condition on the is-is adjacency subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1080 for 'IS-IS Adjacency Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis neighbors
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show isis topology` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   router isis 1
  net 49.0001.0000.0001.00
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis neighbors | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1080 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1081
**Alarm Name:** FIB (Forwarding Table) Configuration Mismatch
**Severity:** Critical

This alarm indicates a configuration mismatch condition on the fib (forwarding table) subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1081 for 'FIB (Forwarding Table) Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show cef ipv4 summary
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show cef ipv4 summary` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear route-ha eof
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show cef ipv4 summary | include resolved
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1081 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1082
**Alarm Name:** RSVP-TE Tunnel Stuck in INIT State
**Severity:** Major

This alarm indicates a stuck in init state condition on the rsvp-te tunnel subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1082 for 'RSVP-TE Tunnel Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show rsvp interface
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show rsvp session` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface tunnel-te1
  shutdown
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show mpls traffic-eng tunnels | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1082 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1083
**Alarm Name:** MPLS LDP Session High CRC Rate
**Severity:** Major

This alarm indicates a high crc rate condition on the mpls ldp session subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1083 for 'MPLS LDP Session High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp discovery
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls ldp discovery`.
4. **⚠️ WARNING: Service Impact Possible.** If the mpls ldp session utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear mpls ldp neighbor {ip}
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp neighbor | include Oper
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1083 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1084
**Alarm Name:** RSVP-TE Tunnel High CRC Rate
**Severity:** Major

This alarm indicates a high crc rate condition on the rsvp-te tunnel subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1084 for 'RSVP-TE Tunnel High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls traffic-eng tunnels brief
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls traffic-eng tunnels brief`.
4. **⚠️ WARNING: Service Impact Possible.** If the rsvp-te tunnel utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear rsvp session tunnel-id {id}
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show mpls traffic-eng tunnels | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1084 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1085
**Alarm Name:** Line Card NPU Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the line card npu subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1085 for 'Line Card NPU Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show platform
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show platform`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin clear controller fabric plane all
   ```
5. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show platform | include IOS XR RUN
   ```

---

## Procedure to clear ALARM_CODE_1086
**Alarm Name:** FIB (Forwarding Table) Timeout
**Severity:** Major

This alarm indicates a timeout condition on the fib (forwarding table) subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1086 for 'FIB (Forwarding Table) Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show cef ipv4 inconsistency
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show cef ipv4 summary` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear route-ha eof
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show cef ipv4 summary | include resolved
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1086 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1087
**Alarm Name:** IS-IS Adjacency Timeout
**Severity:** Major

This alarm indicates a timeout condition on the is-is adjacency subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1087 for 'IS-IS Adjacency Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis database detail
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show isis topology` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear isis process
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis neighbors | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1087 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1088
**Alarm Name:** MPLS LDP Session Configuration Mismatch
**Severity:** Critical

This alarm indicates a configuration mismatch condition on the mpls ldp session subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1088 for 'MPLS LDP Session Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls ldp neighbor
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show mpls ldp neighbor` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear mpls ldp neighbor {ip}
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show mpls ldp neighbor | include Oper
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1088 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1089
**Alarm Name:** BFD Session Configuration Mismatch
**Severity:** Critical

This alarm indicates a configuration mismatch condition on the bfd session subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1089 for 'BFD Session Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd neighbors
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show bfd neighbors` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bfd counters
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd neighbors | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1089 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1090
**Alarm Name:** Optical Rx Power Loss of Signal (LOS)
**Severity:** Critical

This alarm indicates a loss of signal (los) condition on the optical rx power subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1090 for 'Optical Rx Power Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show controllers optics 0/0/0/1
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show hw-module fpd` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   controller optics 0/0/0/1
  sec-admin-state normal
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show controllers optics 0/0/0/1 | include Rx
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1090 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1091
**Alarm Name:** FIB (Forwarding Table) Threshold Exceeded
**Severity:** Critical

This alarm indicates a threshold exceeded condition on the fib (forwarding table) subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1091 for 'FIB (Forwarding Table) Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show cef ipv4 summary
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show cef ipv4 summary`.
4. **⚠️ WARNING: Service Impact Possible.** If the fib (forwarding table) utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear route-ha eof
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show cef ipv4 summary | include resolved
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1091 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1092
**Alarm Name:** BFD Session High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the bfd session subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1092 for 'BFD Session High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd counters
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bfd counters`.
4. **⚠️ WARNING: Service Impact Possible.** If the bfd session utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bfd counters
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd neighbors | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1092 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1093
**Alarm Name:** QoS Scheduler Down
**Severity:** Minor

This alarm indicates a down condition on the qos scheduler subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1093 for 'QoS Scheduler Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show policy-map interface te0/0/0/1
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show policy-map interface te0/0/0/1` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   policy-map PM_CORE
  class class-default
  bandwidth percent 50
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   show policy-map interface te0/0/0/1 | include conform
   ```

---

## Procedure to clear ALARM_CODE_1094
**Alarm Name:** OSPF Adjacency Resource Exhaustion
**Severity:** Warning

This alarm indicates a resource exhaustion condition on the ospf adjacency subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1094 for 'OSPF Adjacency Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ip ospf database
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ip ospf interface brief`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface GigabitEthernet0/0/0
  ip ospf cost 10
   ```
5. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ip ospf neighbor | include FULL
   ```

---

## Procedure to clear ALARM_CODE_1095
**Alarm Name:** SNMP Agent Memory Leak Detected
**Severity:** Critical

This alarm indicates a memory leak detected condition on the snmp agent subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1095 for 'SNMP Agent Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show snmp host
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show snmp`.
4. **⚠️ WARNING: Service Impact Possible.** If the snmp agent utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   snmp-server host 10.0.0.1 TELECOM_RO
   ```
6. **Post-Recovery Validation:** Verify the snmp agent has returned to a stable operational state:
   ```
   show snmp | include packets
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1095 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1096
**Alarm Name:** RSVP-TE Tunnel Memory Leak Detected
**Severity:** Major

This alarm indicates a memory leak detected condition on the rsvp-te tunnel subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1096 for 'RSVP-TE Tunnel Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mpls traffic-eng tunnels brief
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls traffic-eng tunnels brief`.
4. **⚠️ WARNING: Service Impact Possible.** If the rsvp-te tunnel utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface tunnel-te1
  shutdown
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show mpls traffic-eng tunnels | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1096 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1097
**Alarm Name:** Optical Rx Power High CRC Rate
**Severity:** Major

This alarm indicates a high crc rate condition on the optical rx power subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1097 for 'Optical Rx Power High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show controllers optics 0/0/0/1
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show controllers optics 0/0/0/1`.
4. **⚠️ WARNING: Service Impact Possible.** If the optical rx power utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   hw-module location 0/0/CPU0 reload
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show controllers optics 0/0/0/1 | include Rx
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1097 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1098
**Alarm Name:** Power Supply Unit (PSU) Configuration Mismatch
**Severity:** Critical

This alarm indicates a configuration mismatch condition on the power supply unit (psu) subsystem of Cisco equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1098 for 'Power Supply Unit (PSU) Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show redundancy
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show platform` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   power disable module {slot}
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show environment power | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Cisco TAC (Technical Assistance Center) with the alarm code 1098 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1099
**Alarm Name:** Management Ethernet Stuck in INIT State
**Severity:** Minor

This alarm indicates a stuck in init state condition on the management ethernet subsystem of Cisco equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Cisco NMS dashboard and confirm alarm code 1099 for 'Management Ethernet Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show interface MgmtEth0/RSP0/CPU0/0` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   interface MgmtEth0/RSP0/CPU0/0
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show interface MgmtEth0/RSP0/CPU0/0 | include up/up
   ```

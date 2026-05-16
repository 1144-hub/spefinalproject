# Nokia Service Restoration MOP (Method of Procedure)

**Equipment Vendor:** Nokia
**Document Type:** Standard Operating Procedure (SOP)
**Scope:** Core Router Troubleshooting
**Network Topology Context:** Core Router

## Overview
This document outlines the standard procedural steps to identify, troubleshoot, and resolve common network alarms on Nokia Service Routers (SR-Series) operating natively as CORE routing nodes. Impact to Core routers has a cascading failure effect on all connected Provider Edge (PE) routers. Do not skip any mandatory steps.

---

## Procedure to clear ALARM_CODE_404
**Alarm Name:** BGP Peer Down (Authentication Failure)
**Severity:** Critical

This alarm indicates that a BGP peering session has dropped due to an MD5 authentication mismatch.

1. **Verify the Alarm Status:** Run the command `show router bgp neighbor status` to confirm the neighbor is in an Active/Idle state.
2. **Check Logs:** Check the system logs for authentication errors by running `show log log-id 99 | match "auth"`.
3. **Validate Key:** Contact the BGP peer administrator to verify the shared MD5 authentication key.
4. **Update Key:** Enter configure mode `configure router bgp group "EXTERNAL" neighbor 192.168.1.1` and run `authentication-key <NEW_KEY>`.
5. **Clear Session:** Soft reset the BGP session using `clear router bgp protocol`.
6. **Final Verification:** Issue `show router bgp neighbor 192.168.1.1` to confirm the state is now 'Established'.

---

## Procedure to clear ALARM_CODE_501
**Alarm Name:** Interface Link Down (Optical Rx Loss)
**Severity:** Major

This alarm triggers when the optical receiver (Rx) on an SFP module drops below acceptable light levels (-24 dBm).

1. **Check Optical Levels:** Run `show port 1/1/1 optical` to check the current Tx and Rx power levels.
2. **Physical Inspection:** If Rx is below -24 dBm, request remote hands to inspect the fiber patch cord in port 1/1/1 for bends or dirt.
3. **Clean Fiber:** Have the technician clean both ends of the fiber patch cord using an approved optical cleaning pen.
4. **Re-seat SFP:** If cleaning fails, have the technician re-seat (unplug and plug back in) the SFP optic module.
5. **Replace SFP:** If the power levels do not improve, the SFP module is faulty. Replace the SFP module in port 1/1/1 with a new spare.
6. **Verify Link:** Run `show port 1/1/1` to ensure the Operational State is 'Up'.


---

## Procedure to clear ALARM_CODE_1100
**Alarm Name:** BGP Peer Unreachable
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1100 representing 'BGP Peer Unreachable' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1101
**Alarm Name:** Multicast PIM Neighbor Loss of Signal (LOS)
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1101 representing 'Multicast PIM Neighbor Loss of Signal (LOS)' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1102
**Alarm Name:** BGP Route Reflector Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1102 representing 'BGP Route Reflector Performance Degraded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1103
**Alarm Name:** OSPF Adjacency Flapping
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1103 representing 'OSPF Adjacency Flapping' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1104
**Alarm Name:** VPLS Pseudowire High Cyclic Redundancy (CRC) Rate
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1104 representing 'VPLS Pseudowire High Cyclic Redundancy (CRC) Rate' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1105
**Alarm Name:** LACP Bundle Authentication Failed
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1105 representing 'LACP Bundle Authentication Failed' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1106
**Alarm Name:** IS-IS Adjacency Loss of Signal (LOS)
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1106 representing 'IS-IS Adjacency Loss of Signal (LOS)' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1107
**Alarm Name:** IGMP Snooping Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1107 representing 'IGMP Snooping Stuck in INIT State' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1108
**Alarm Name:** OAM Connectivity High Cyclic Redundancy (CRC) Rate
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1108 representing 'OAM Connectivity High Cyclic Redundancy (CRC) Rate' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1109
**Alarm Name:** IGMP Snooping Unreachable
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1109 representing 'IGMP Snooping Unreachable' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1110
**Alarm Name:** Optical Rx Power Down
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1110 representing 'Optical Rx Power Down' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1111
**Alarm Name:** EVPN MAC Route Stuck in INIT State
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1111 representing 'EVPN MAC Route Stuck in INIT State' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1112
**Alarm Name:** Fan Tray Assembly Flapping
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1112 representing 'Fan Tray Assembly Flapping' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1113
**Alarm Name:** MPLS LDP Session Memory Leak Detected
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1113 representing 'MPLS LDP Session Memory Leak Detected' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1114
**Alarm Name:** Routing Engine CPU Configuration Mismatch
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1114 representing 'Routing Engine CPU Configuration Mismatch' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1115
**Alarm Name:** IPSec VPN Tunnel High Cyclic Redundancy (CRC) Rate
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1115 representing 'IPSec VPN Tunnel High Cyclic Redundancy (CRC) Rate' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1116
**Alarm Name:** STP Root Topology Loss of Signal (LOS)
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1116 representing 'STP Root Topology Loss of Signal (LOS)' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1117
**Alarm Name:** FIB (Forwarding Table) Timeout
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1117 representing 'FIB (Forwarding Table) Timeout' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1118
**Alarm Name:** Optical Rx Power Resource Exhaustion
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1118 representing 'Optical Rx Power Resource Exhaustion' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1119
**Alarm Name:** ACL Processing Out of Sync
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1119 representing 'ACL Processing Out of Sync' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1120
**Alarm Name:** Power Supply Unit (PSU) Out of Sync
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1120 representing 'Power Supply Unit (PSU) Out of Sync' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1121
**Alarm Name:** BGP Peer Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1121 representing 'BGP Peer Resource Exhaustion' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1122
**Alarm Name:** IS-IS Adjacency Configuration Mismatch
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1122 representing 'IS-IS Adjacency Configuration Mismatch' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1123
**Alarm Name:** OAM Connectivity Performance Degraded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1123 representing 'OAM Connectivity Performance Degraded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1124
**Alarm Name:** Management Ethernet Out of Sync
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1124 representing 'Management Ethernet Out of Sync' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1125
**Alarm Name:** VPLS Pseudowire Configuration Mismatch
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1125 representing 'VPLS Pseudowire Configuration Mismatch' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1126
**Alarm Name:** Fan Tray Assembly Out of Sync
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1126 representing 'Fan Tray Assembly Out of Sync' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1127
**Alarm Name:** Routing Engine CPU Stuck in INIT State
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1127 representing 'Routing Engine CPU Stuck in INIT State' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1128
**Alarm Name:** VRRP Group Loss of Signal (LOS)
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1128 representing 'VRRP Group Loss of Signal (LOS)' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1129
**Alarm Name:** STP Root Topology Memory Leak Detected
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1129 representing 'STP Root Topology Memory Leak Detected' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1130
**Alarm Name:** RSVP-TE Tunnel Unreachable
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1130 representing 'RSVP-TE Tunnel Unreachable' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1131
**Alarm Name:** BGP Peer Performance Degraded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1131 representing 'BGP Peer Performance Degraded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1132
**Alarm Name:** QoS Scheduler Hardware Failure
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1132 representing 'QoS Scheduler Hardware Failure' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1133
**Alarm Name:** SNMP Agent Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1133 representing 'SNMP Agent Resource Exhaustion' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1134
**Alarm Name:** GRE Tunnel Timeout
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1134 representing 'GRE Tunnel Timeout' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1135
**Alarm Name:** BGP Peer High Cyclic Redundancy (CRC) Rate
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1135 representing 'BGP Peer High Cyclic Redundancy (CRC) Rate' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1136
**Alarm Name:** Line Card NPU Hardware Failure
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1136 representing 'Line Card NPU Hardware Failure' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1137
**Alarm Name:** Optical Tx Power Resource Exhaustion
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1137 representing 'Optical Tx Power Resource Exhaustion' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1138
**Alarm Name:** Optical Rx Power Performance Degraded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1138 representing 'Optical Rx Power Performance Degraded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1139
**Alarm Name:** Multicast PIM Neighbor Threshold Exceeded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1139 representing 'Multicast PIM Neighbor Threshold Exceeded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1140
**Alarm Name:** FIB (Forwarding Table) Unreachable
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1140 representing 'FIB (Forwarding Table) Unreachable' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1141
**Alarm Name:** MAC Address Table Memory Leak Detected
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1141 representing 'MAC Address Table Memory Leak Detected' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1142
**Alarm Name:** Fan Tray Assembly High Cyclic Redundancy (CRC) Rate
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1142 representing 'Fan Tray Assembly High Cyclic Redundancy (CRC) Rate' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1143
**Alarm Name:** IPSec VPN Tunnel Down
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1143 representing 'IPSec VPN Tunnel Down' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1144
**Alarm Name:** QoS Scheduler Loss of Signal (LOS)
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1144 representing 'QoS Scheduler Loss of Signal (LOS)' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1145
**Alarm Name:** MPLS LDP Session Down
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1145 representing 'MPLS LDP Session Down' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1146
**Alarm Name:** QoS Scheduler Performance Degraded
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1146 representing 'QoS Scheduler Performance Degraded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1147
**Alarm Name:** Optical Tx Power Performance Degraded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1147 representing 'Optical Tx Power Performance Degraded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1148
**Alarm Name:** LACP Bundle Loss of Signal (LOS)
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1148 representing 'LACP Bundle Loss of Signal (LOS)' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1149
**Alarm Name:** Fan Tray Assembly Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1149 representing 'Fan Tray Assembly Resource Exhaustion' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1150
**Alarm Name:** Multicast PIM Neighbor Stuck in INIT State
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1150 representing 'Multicast PIM Neighbor Stuck in INIT State' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1151
**Alarm Name:** NTP Synchronization Out of Sync
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1151 representing 'NTP Synchronization Out of Sync' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1152
**Alarm Name:** Optical Rx Power Stuck in INIT State
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1152 representing 'Optical Rx Power Stuck in INIT State' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1153
**Alarm Name:** Line Card NPU Unreachable
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1153 representing 'Line Card NPU Unreachable' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1154
**Alarm Name:** OSPF Adjacency Performance Degraded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1154 representing 'OSPF Adjacency Performance Degraded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1155
**Alarm Name:** BFD Session Authentication Failed
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1155 representing 'BFD Session Authentication Failed' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1156
**Alarm Name:** IS-IS Adjacency Timeout
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1156 representing 'IS-IS Adjacency Timeout' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1157
**Alarm Name:** Management Ethernet Timeout
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1157 representing 'Management Ethernet Timeout' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1158
**Alarm Name:** BFD Session Threshold Exceeded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1158 representing 'BFD Session Threshold Exceeded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1159
**Alarm Name:** HSRP Instance Flapping
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1159 representing 'HSRP Instance Flapping' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1160
**Alarm Name:** IPSec VPN Tunnel Memory Leak Detected
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1160 representing 'IPSec VPN Tunnel Memory Leak Detected' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1161
**Alarm Name:** VRRP Group Out of Sync
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1161 representing 'VRRP Group Out of Sync' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1162
**Alarm Name:** Power Supply Unit (PSU) Loss of Signal (LOS)
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1162 representing 'Power Supply Unit (PSU) Loss of Signal (LOS)' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1163
**Alarm Name:** SNMP Agent Capacity Limit Reached
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1163 representing 'SNMP Agent Capacity Limit Reached' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1164
**Alarm Name:** BGP Peer Configuration Mismatch
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1164 representing 'BGP Peer Configuration Mismatch' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1165
**Alarm Name:** ARP Cache Down
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1165 representing 'ARP Cache Down' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1166
**Alarm Name:** LACP Bundle Memory Leak Detected
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1166 representing 'LACP Bundle Memory Leak Detected' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1167
**Alarm Name:** Management Ethernet Loss of Signal (LOS)
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1167 representing 'Management Ethernet Loss of Signal (LOS)' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1168
**Alarm Name:** STP Root Topology Stuck in INIT State
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1168 representing 'STP Root Topology Stuck in INIT State' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1169
**Alarm Name:** IPSec VPN Tunnel Performance Degraded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1169 representing 'IPSec VPN Tunnel Performance Degraded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1170
**Alarm Name:** IGMP Snooping Performance Degraded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1170 representing 'IGMP Snooping Performance Degraded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1171
**Alarm Name:** Power Supply Unit (PSU) Timeout
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1171 representing 'Power Supply Unit (PSU) Timeout' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1172
**Alarm Name:** GRE Tunnel Unreachable
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1172 representing 'GRE Tunnel Unreachable' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1173
**Alarm Name:** Multicast PIM Neighbor Memory Leak Detected
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1173 representing 'Multicast PIM Neighbor Memory Leak Detected' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1174
**Alarm Name:** GRE Tunnel Flapping
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1174 representing 'GRE Tunnel Flapping' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1175
**Alarm Name:** Routing Engine CPU Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1175 representing 'Routing Engine CPU Threshold Exceeded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1176
**Alarm Name:** Routing Engine CPU Down
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1176 representing 'Routing Engine CPU Down' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1177
**Alarm Name:** BGP Route Reflector Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1177 representing 'BGP Route Reflector Stuck in INIT State' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1178
**Alarm Name:** IPSec VPN Tunnel Hardware Failure
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1178 representing 'IPSec VPN Tunnel Hardware Failure' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1179
**Alarm Name:** HSRP Instance High Cyclic Redundancy (CRC) Rate
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1179 representing 'HSRP Instance High Cyclic Redundancy (CRC) Rate' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1180
**Alarm Name:** Radius/TACACS Auth Hardware Failure
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1180 representing 'Radius/TACACS Auth Hardware Failure' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1181
**Alarm Name:** RSVP-TE Tunnel Authentication Failed
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1181 representing 'RSVP-TE Tunnel Authentication Failed' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1182
**Alarm Name:** SNMP Agent Threshold Exceeded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1182 representing 'SNMP Agent Threshold Exceeded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1183
**Alarm Name:** VRRP Group Hardware Failure
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1183 representing 'VRRP Group Hardware Failure' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1184
**Alarm Name:** OAM Connectivity Authentication Failed
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1184 representing 'OAM Connectivity Authentication Failed' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1185
**Alarm Name:** Optical Tx Power Capacity Limit Reached
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1185 representing 'Optical Tx Power Capacity Limit Reached' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1186
**Alarm Name:** DHCP Relay Agent Memory Leak Detected
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1186 representing 'DHCP Relay Agent Memory Leak Detected' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1187
**Alarm Name:** BGP Peer Loss of Signal (LOS)
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1187 representing 'BGP Peer Loss of Signal (LOS)' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1188
**Alarm Name:** OAM Connectivity Down
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1188 representing 'OAM Connectivity Down' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1189
**Alarm Name:** LACP Bundle High Cyclic Redundancy (CRC) Rate
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1189 representing 'LACP Bundle High Cyclic Redundancy (CRC) Rate' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1190
**Alarm Name:** SNMP Agent Hardware Failure
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1190 representing 'SNMP Agent Hardware Failure' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1191
**Alarm Name:** SNMP Agent Authentication Failed
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1191 representing 'SNMP Agent Authentication Failed' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1192
**Alarm Name:** Optical Rx Power High Cyclic Redundancy (CRC) Rate
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1192 representing 'Optical Rx Power High Cyclic Redundancy (CRC) Rate' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1193
**Alarm Name:** OAM Connectivity Hardware Failure
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1193 representing 'OAM Connectivity Hardware Failure' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1194
**Alarm Name:** Optical Tx Power Out of Sync
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1194 representing 'Optical Tx Power Out of Sync' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1195
**Alarm Name:** QoS Scheduler Threshold Exceeded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1195 representing 'QoS Scheduler Threshold Exceeded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1196
**Alarm Name:** IPSec VPN Tunnel Unreachable
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1196 representing 'IPSec VPN Tunnel Unreachable' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1197
**Alarm Name:** GRE Tunnel Capacity Limit Reached
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1197 representing 'GRE Tunnel Capacity Limit Reached' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1198
**Alarm Name:** NTP Synchronization Hardware Failure
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1198 representing 'NTP Synchronization Hardware Failure' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1199
**Alarm Name:** Switch Fabric Module Performance Degraded
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1199 representing 'Switch Fabric Module Performance Degraded' on the Nokia NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show router status
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear router ospf
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.


<!-- BEGIN GENERATED PROCEDURES -->

---

## Procedure to clear ALARM_CODE_1100
**Alarm Name:** Switch Fabric Module Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the switch fabric module subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1100 for 'Switch Fabric Module Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis environment
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show chassis environment` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure system switch-fabric {id}
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the switch fabric module has returned to a stable operational state:
   ```
   show system switch-fabric | match active
   ```

---

## Procedure to clear ALARM_CODE_1101
**Alarm Name:** Power Supply Unit (PSU) Unreachable
**Severity:** Critical

This alarm indicates a unreachable condition on the power supply unit (psu) subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1101 for 'Power Supply Unit (PSU) Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis power-supply
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show chassis power-supply` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   tools perform system power-check
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show chassis power-supply | match up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1101 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1102
**Alarm Name:** BGP Peer Threshold Exceeded
**Severity:** Warning

This alarm indicates a threshold exceeded condition on the bgp peer subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1102 for 'BGP Peer Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router bgp routes ipv4
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router bgp neighbor {ip}`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router bgp group EXTERNAL neighbor {ip}
  admin-state enable
   ```
5. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show router bgp summary | match Established
   ```

---

## Procedure to clear ALARM_CODE_1103
**Alarm Name:** RSVP-TE Tunnel High CRC Rate
**Severity:** Major

This alarm indicates a high crc rate condition on the rsvp-te tunnel subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1103 for 'RSVP-TE Tunnel High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router mpls lsp
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router mpls lsp`.
4. **⚠️ WARNING: Service Impact Possible.** If the rsvp-te tunnel utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router rsvp session lsp-name {name}
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show router mpls lsp | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1103 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1104
**Alarm Name:** Fan Tray Assembly Memory Leak Detected
**Severity:** Critical

This alarm indicates a memory leak detected condition on the fan tray assembly subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1104 for 'Fan Tray Assembly Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system alarms active
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show chassis environment`.
4. **⚠️ WARNING: Service Impact Possible.** If the fan tray assembly utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   tools dump system-resources
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   show chassis environment | match Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1104 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1105
**Alarm Name:** Management Ethernet High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the management ethernet subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1105 for 'Management Ethernet High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router interface mgmt
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router interface mgmt`.
4. **⚠️ WARNING: Service Impact Possible.** If the management ethernet utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin save
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show router interface mgmt | match up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1105 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1106
**Alarm Name:** BGP Peer Stuck in INIT State
**Severity:** Major

This alarm indicates a stuck in init state condition on the bgp peer subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1106 for 'BGP Peer Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router bgp summary
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router bgp summary` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router bgp neighbor {ip} soft
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show router bgp summary | match Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1106 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1107
**Alarm Name:** Management Ethernet Flapping
**Severity:** Warning

This alarm indicates a flapping condition on the management ethernet subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1107 for 'Management Ethernet Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system information
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router interface mgmt` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin save
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show router interface mgmt | match up
   ```

---

## Procedure to clear ALARM_CODE_1108
**Alarm Name:** EVPN MAC Route Flapping
**Severity:** Minor

This alarm indicates a flapping condition on the evpn mac route subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1108 for 'EVPN MAC Route Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show service evpn
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show service evpn mac-table` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear service evpn mac-table
   ```
6. **Post-Recovery Validation:** Verify the evpn mac route has returned to a stable operational state:
   ```
   show service evpn | match active
   ```

---

## Procedure to clear ALARM_CODE_1109
**Alarm Name:** Optical Rx Power High CRC Rate
**Severity:** Warning

This alarm indicates a high crc rate condition on the optical rx power subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1109 for 'Optical Rx Power High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system alarms
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show port 1/1/1 detail`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin port 1/1/1 shutdown
admin port 1/1/1 no shutdown
   ```
5. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port 1/1/1 | match Up
   ```

---

## Procedure to clear ALARM_CODE_1110
**Alarm Name:** VPLS Pseudowire Unreachable
**Severity:** Critical

This alarm indicates a unreachable condition on the vpls pseudowire subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1110 for 'VPLS Pseudowire Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show service sdp-using
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show service sdp-using` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure service vpls {id}
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the vpls pseudowire has returned to a stable operational state:
   ```
   show service sdp-using | match operUp
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1110 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1111
**Alarm Name:** LACP Bundle Resource Exhaustion
**Severity:** Major

This alarm indicates a resource exhaustion condition on the lacp bundle subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1111 for 'LACP Bundle Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lag 1 statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show lag 1 port`.
4. **⚠️ WARNING: Service Impact Possible.** If the lacp bundle utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear lag statistics
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show lag 1 | match active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1111 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1112
**Alarm Name:** EVPN MAC Route Down
**Severity:** Major

This alarm indicates a down condition on the evpn mac route subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1112 for 'EVPN MAC Route Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router bgp evpn routes
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show service evpn mac-table` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear service evpn mac-table
   ```
6. **Post-Recovery Validation:** Verify the evpn mac route has returned to a stable operational state:
   ```
   show service evpn | match active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1112 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1113
**Alarm Name:** Switch Fabric Module Capacity Limit Reached
**Severity:** Critical

This alarm indicates a capacity limit reached condition on the switch fabric module subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1113 for 'Switch Fabric Module Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis environment
   ```
3. **Hardware Status Check:** Run `show system switch-fabric` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected switch fabric module unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin switch-fabric {id} reboot
   ```
7. **Post-Recovery Validation:** Verify the switch fabric module has returned to a stable operational state:
   ```
   show system switch-fabric | match active
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1113 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1114
**Alarm Name:** BGP Peer Out of Sync
**Severity:** Minor

This alarm indicates a out of sync condition on the bgp peer subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1114 for 'BGP Peer Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router bgp neighbor {ip}
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router bgp neighbor {ip}` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router bgp group EXTERNAL neighbor {ip}
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show router bgp summary | match Established
   ```

---

## Procedure to clear ALARM_CODE_1115
**Alarm Name:** BGP Peer Timeout
**Severity:** Minor

This alarm indicates a timeout condition on the bgp peer subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1115 for 'BGP Peer Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router bgp summary
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router bgp neighbor {ip}` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router bgp neighbor {ip} soft
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show router bgp summary | match Established
   ```

---

## Procedure to clear ALARM_CODE_1116
**Alarm Name:** Power Supply Unit (PSU) Timeout
**Severity:** Critical

This alarm indicates a timeout condition on the power supply unit (psu) subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1116 for 'Power Supply Unit (PSU) Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show environment power
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show environment power` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin power-shelf {id} power-module {mod} reboot
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show chassis power-supply | match up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1116 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1117
**Alarm Name:** BGP Peer Down
**Severity:** Minor

This alarm indicates a down condition on the bgp peer subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1117 for 'BGP Peer Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router bgp routes ipv4
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show router bgp routes ipv4` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router bgp group EXTERNAL neighbor {ip}
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show router bgp summary | match Established
   ```

---

## Procedure to clear ALARM_CODE_1118
**Alarm Name:** EVPN MAC Route Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the evpn mac route subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1118 for 'EVPN MAC Route Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router bgp evpn routes
   ```
3. **Hardware Status Check:** Run `show service evpn mac-table` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected evpn mac route unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure service vpls {id} bgp-evpn
  admin-state enable
   ```
7. **Post-Recovery Validation:** Verify the evpn mac route has returned to a stable operational state:
   ```
   show service evpn | match active
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1118 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1119
**Alarm Name:** VRRP Group Down
**Severity:** Minor

This alarm indicates a down condition on the vrrp group subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1119 for 'VRRP Group Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router vrrp statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show router vrrp statistics` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show router vrrp instance | match Master
   ```

---

## Procedure to clear ALARM_CODE_1120
**Alarm Name:** VPLS Pseudowire Stuck in INIT State
**Severity:** Critical

This alarm indicates a stuck in init state condition on the vpls pseudowire subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1120 for 'VPLS Pseudowire Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show service sdp-using
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router ldp bindings active prefixes` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure service vpls {id}
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the vpls pseudowire has returned to a stable operational state:
   ```
   show service sdp-using | match operUp
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1120 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1121
**Alarm Name:** RSVP-TE Tunnel Timeout
**Severity:** Major

This alarm indicates a timeout condition on the rsvp-te tunnel subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1121 for 'RSVP-TE Tunnel Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router mpls lsp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router rsvp interface` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router mpls lsp {name}
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show router mpls lsp | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1121 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1122
**Alarm Name:** RSVP-TE Tunnel Authentication Failed
**Severity:** Minor

This alarm indicates a authentication failed condition on the rsvp-te tunnel subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1122 for 'RSVP-TE Tunnel Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router mpls lsp
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show router rsvp interface` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router mpls lsp {name}
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show router mpls lsp | match Up
   ```

---

## Procedure to clear ALARM_CODE_1123
**Alarm Name:** Line Card NPU Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the line card npu subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1123 for 'Line Card NPU Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show card state
   ```
3. **Hardware Status Check:** Run `show chassis` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected line card npu unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin card {slot} reboot
   ```
7. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show card state | match up/active
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1123 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1124
**Alarm Name:** Fan Tray Assembly Threshold Exceeded
**Severity:** Critical

This alarm indicates a threshold exceeded condition on the fan tray assembly subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1124 for 'Fan Tray Assembly Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system alarms active
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show chassis environment`.
4. **⚠️ WARNING: Service Impact Possible.** If the fan tray assembly utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   tools dump system-resources
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   show chassis environment | match Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1124 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1125
**Alarm Name:** OSPF Adjacency High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the ospf adjacency subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1125 for 'OSPF Adjacency High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ospf database
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router ospf neighbor`.
4. **⚠️ WARNING: Service Impact Possible.** If the ospf adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router ospf 0 area 0.0.0.0 interface to-PE
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show router ospf neighbor | match Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1125 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1126
**Alarm Name:** Optical Rx Power Memory Leak Detected
**Severity:** Critical

This alarm indicates a memory leak detected condition on the optical rx power subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1126 for 'Optical Rx Power Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port 1/1/1 detail
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show port 1/1/1 optical`.
4. **⚠️ WARNING: Service Impact Possible.** If the optical rx power utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure port 1/1/1
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port 1/1/1 | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1126 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1127
**Alarm Name:** VRRP Group Configuration Mismatch
**Severity:** Warning

This alarm indicates a configuration mismatch condition on the vrrp group subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1127 for 'VRRP Group Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router vrrp statistics
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show router vrrp statistics` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show router vrrp instance | match Master
   ```

---

## Procedure to clear ALARM_CODE_1128
**Alarm Name:** MPLS LDP Session Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the mpls ldp session subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1128 for 'MPLS LDP Session Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router mpls status
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router mpls status`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router ldp
  admin-state enable
   ```
5. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show router ldp session | match Established
   ```

---

## Procedure to clear ALARM_CODE_1129
**Alarm Name:** VRRP Group Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the vrrp group subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1129 for 'VRRP Group Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router vrrp statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router vrrp instance`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router vrrp {id} backup {ip}
  admin-state enable
  priority 200
   ```
5. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show router vrrp instance | match Master
   ```

---

## Procedure to clear ALARM_CODE_1130
**Alarm Name:** Line Card NPU Unreachable
**Severity:** Critical

This alarm indicates a unreachable condition on the line card npu subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1130 for 'Line Card NPU Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show mda detail` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin card {slot} reboot
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show card state | match up/active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1130 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1131
**Alarm Name:** VRRP Group High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the vrrp group subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1131 for 'VRRP Group High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router vrrp instance
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router vrrp instance`.
4. **⚠️ WARNING: Service Impact Possible.** If the vrrp group utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show router vrrp instance | match Master
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1131 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1132
**Alarm Name:** Switch Fabric Module Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the switch fabric module subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1132 for 'Switch Fabric Module Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system switch-fabric
   ```
3. **Hardware Status Check:** Run `show chassis environment` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected switch fabric module unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure system switch-fabric {id}
  admin-state enable
   ```
7. **Post-Recovery Validation:** Verify the switch fabric module has returned to a stable operational state:
   ```
   show system switch-fabric | match active
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1132 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1133
**Alarm Name:** MPLS LDP Session Performance Degraded
**Severity:** Major

This alarm indicates a performance degraded condition on the mpls ldp session subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1133 for 'MPLS LDP Session Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ldp session
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router ldp bindings`.
4. **⚠️ WARNING: Service Impact Possible.** If the mpls ldp session utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router ldp
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show router ldp session | match Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1133 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1134
**Alarm Name:** IS-IS Adjacency Timeout
**Severity:** Major

This alarm indicates a timeout condition on the is-is adjacency subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1134 for 'IS-IS Adjacency Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router isis database
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router isis database` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router isis 1 interface to-PE
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show router isis adjacency | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1134 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1135
**Alarm Name:** EVPN MAC Route Capacity Limit Reached
**Severity:** Critical

This alarm indicates a capacity limit reached condition on the evpn mac route subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1135 for 'EVPN MAC Route Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show service evpn
   ```
3. **Hardware Status Check:** Run `show router bgp evpn routes` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected evpn mac route unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure service vpls {id} bgp-evpn
  admin-state enable
   ```
7. **Post-Recovery Validation:** Verify the evpn mac route has returned to a stable operational state:
   ```
   show service evpn | match active
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1135 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1136
**Alarm Name:** Fan Tray Assembly Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the fan tray assembly subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1136 for 'Fan Tray Assembly Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system alarms active
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show system alarms active` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin environment fan-tray {id} reboot
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   show chassis environment | match Normal
   ```

---

## Procedure to clear ALARM_CODE_1137
**Alarm Name:** MPLS LDP Session Authentication Failed
**Severity:** Major

This alarm indicates a authentication failed condition on the mpls ldp session subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1137 for 'MPLS LDP Session Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ldp bindings
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show router mpls status` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router ldp
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show router ldp session | match Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1137 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1138
**Alarm Name:** Fan Tray Assembly Flapping
**Severity:** Major

This alarm indicates a flapping condition on the fan tray assembly subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1138 for 'Fan Tray Assembly Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis environment
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show chassis environment` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin environment fan-tray {id} reboot
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   show chassis environment | match Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1138 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1139
**Alarm Name:** Switch Fabric Module Performance Degraded
**Severity:** Minor

This alarm indicates a performance degraded condition on the switch fabric module subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1139 for 'Switch Fabric Module Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis environment
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show system switch-fabric`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin switch-fabric {id} reboot
   ```
5. **Post-Recovery Validation:** Verify the switch fabric module has returned to a stable operational state:
   ```
   show system switch-fabric | match active
   ```

---

## Procedure to clear ALARM_CODE_1140
**Alarm Name:** VRRP Group Authentication Failed
**Severity:** Minor

This alarm indicates a authentication failed condition on the vrrp group subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1140 for 'VRRP Group Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router vrrp instance
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show router vrrp statistics` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show router vrrp instance | match Master
   ```

---

## Procedure to clear ALARM_CODE_1141
**Alarm Name:** Switch Fabric Module Down
**Severity:** Minor

This alarm indicates a down condition on the switch fabric module subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1141 for 'Switch Fabric Module Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system switch-fabric
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show system switch-fabric` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin switch-fabric {id} reboot
   ```
6. **Post-Recovery Validation:** Verify the switch fabric module has returned to a stable operational state:
   ```
   show system switch-fabric | match active
   ```

---

## Procedure to clear ALARM_CODE_1142
**Alarm Name:** IS-IS Adjacency Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the is-is adjacency subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1142 for 'IS-IS Adjacency Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router isis adjacency
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router isis adjacency`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router isis 1 interface to-PE
  admin-state enable
   ```
5. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show router isis adjacency | match Up
   ```

---

## Procedure to clear ALARM_CODE_1143
**Alarm Name:** Line Card NPU Loss of Signal (LOS)
**Severity:** Major

This alarm indicates a loss of signal (los) condition on the line card npu subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1143 for 'Line Card NPU Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show card state
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show card state` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin card {slot} reboot
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show card state | match up/active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1143 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1144
**Alarm Name:** Power Supply Unit (PSU) Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the power supply unit (psu) subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1144 for 'Power Supply Unit (PSU) Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis power-supply
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show environment power` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   tools perform system power-check
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show chassis power-supply | match up
   ```

---

## Procedure to clear ALARM_CODE_1145
**Alarm Name:** Optical Rx Power Out of Sync
**Severity:** Warning

This alarm indicates a out of sync condition on the optical rx power subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1145 for 'Optical Rx Power Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port 1/1/1 detail
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show port 1/1/1 optical` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin port 1/1/1 shutdown
admin port 1/1/1 no shutdown
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port 1/1/1 | match Up
   ```

---

## Procedure to clear ALARM_CODE_1146
**Alarm Name:** EVPN MAC Route Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the evpn mac route subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1146 for 'EVPN MAC Route Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router bgp evpn routes
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show service evpn mac-table` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure service vpls {id} bgp-evpn
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the evpn mac route has returned to a stable operational state:
   ```
   show service evpn | match active
   ```

---

## Procedure to clear ALARM_CODE_1147
**Alarm Name:** Switch Fabric Module Authentication Failed
**Severity:** Major

This alarm indicates a authentication failed condition on the switch fabric module subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1147 for 'Switch Fabric Module Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis environment
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show chassis environment` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure system switch-fabric {id}
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the switch fabric module has returned to a stable operational state:
   ```
   show system switch-fabric | match active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1147 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1148
**Alarm Name:** MPLS LDP Session Loss of Signal (LOS)
**Severity:** Major

This alarm indicates a loss of signal (los) condition on the mpls ldp session subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1148 for 'MPLS LDP Session Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router mpls status
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show router ldp session` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router ldp session {ip}
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show router ldp session | match Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1148 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1149
**Alarm Name:** Fan Tray Assembly Configuration Mismatch
**Severity:** Minor

This alarm indicates a configuration mismatch condition on the fan tray assembly subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1149 for 'Fan Tray Assembly Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis environment
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show system alarms active` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   tools dump system-resources
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   show chassis environment | match Normal
   ```

---

## Procedure to clear ALARM_CODE_1150
**Alarm Name:** IS-IS Adjacency Hardware Failure
**Severity:** Minor

This alarm indicates a hardware failure condition on the is-is adjacency subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1150 for 'IS-IS Adjacency Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router isis database
   ```
3. **Hardware Status Check:** Run `show router isis database` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected is-is adjacency unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router isis adjacency
   ```
7. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show router isis adjacency | match Up
   ```

---

## Procedure to clear ALARM_CODE_1151
**Alarm Name:** OSPF Adjacency Authentication Failed
**Severity:** Warning

This alarm indicates a authentication failed condition on the ospf adjacency subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1151 for 'OSPF Adjacency Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ospf status
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show router ospf status` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router ospf neighbor all
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show router ospf neighbor | match Full
   ```

---

## Procedure to clear ALARM_CODE_1152
**Alarm Name:** Management Ethernet Performance Degraded
**Severity:** Critical

This alarm indicates a performance degraded condition on the management ethernet subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1152 for 'Management Ethernet Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router interface mgmt
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router interface mgmt`.
4. **⚠️ WARNING: Service Impact Possible.** If the management ethernet utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router management
  interface mgmt
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show router interface mgmt | match up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1152 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1153
**Alarm Name:** Line Card NPU Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the line card npu subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1153 for 'Line Card NPU Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show mda detail
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show chassis`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin card {slot} reboot
   ```
5. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show card state | match up/active
   ```

---

## Procedure to clear ALARM_CODE_1154
**Alarm Name:** Switch Fabric Module Memory Leak Detected
**Severity:** Major

This alarm indicates a memory leak detected condition on the switch fabric module subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1154 for 'Switch Fabric Module Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system switch-fabric
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show system switch-fabric`.
4. **⚠️ WARNING: Service Impact Possible.** If the switch fabric module utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin switch-fabric {id} reboot
   ```
6. **Post-Recovery Validation:** Verify the switch fabric module has returned to a stable operational state:
   ```
   show system switch-fabric | match active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1154 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1155
**Alarm Name:** RSVP-TE Tunnel Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the rsvp-te tunnel subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1155 for 'RSVP-TE Tunnel Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router rsvp interface
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show router rsvp interface` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router rsvp session lsp-name {name}
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show router mpls lsp | match Up
   ```

---

## Procedure to clear ALARM_CODE_1156
**Alarm Name:** MPLS LDP Session Down
**Severity:** Major

This alarm indicates a down condition on the mpls ldp session subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1156 for 'MPLS LDP Session Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ldp session
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show router mpls status` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router ldp session {ip}
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show router ldp session | match Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1156 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1157
**Alarm Name:** BGP Peer Memory Leak Detected
**Severity:** Critical

This alarm indicates a memory leak detected condition on the bgp peer subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1157 for 'BGP Peer Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router bgp neighbor {ip}
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router bgp summary`.
4. **⚠️ WARNING: Service Impact Possible.** If the bgp peer utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router bgp group EXTERNAL neighbor {ip}
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show router bgp summary | match Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1157 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1158
**Alarm Name:** RSVP-TE Tunnel Hardware Failure
**Severity:** Minor

This alarm indicates a hardware failure condition on the rsvp-te tunnel subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1158 for 'RSVP-TE Tunnel Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router mpls lsp
   ```
3. **Hardware Status Check:** Run `show router mpls lsp` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected rsvp-te tunnel unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router rsvp session lsp-name {name}
   ```
7. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show router mpls lsp | match Up
   ```

---

## Procedure to clear ALARM_CODE_1159
**Alarm Name:** Line Card NPU Down
**Severity:** Major

This alarm indicates a down condition on the line card npu subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1159 for 'Line Card NPU Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show card state
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show chassis` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure card {slot}
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   show card state | match up/active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1159 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1160
**Alarm Name:** IS-IS Adjacency Capacity Limit Reached
**Severity:** Minor

This alarm indicates a capacity limit reached condition on the is-is adjacency subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1160 for 'IS-IS Adjacency Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router isis adjacency
   ```
3. **Hardware Status Check:** Run `show router isis database` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected is-is adjacency unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router isis adjacency
   ```
7. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show router isis adjacency | match Up
   ```

---

## Procedure to clear ALARM_CODE_1161
**Alarm Name:** OSPF Adjacency Flapping
**Severity:** Major

This alarm indicates a flapping condition on the ospf adjacency subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1161 for 'OSPF Adjacency Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ospf database
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router ospf status` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router ospf neighbor all
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show router ospf neighbor | match Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1161 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1162
**Alarm Name:** VRRP Group Flapping
**Severity:** Warning

This alarm indicates a flapping condition on the vrrp group subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1162 for 'VRRP Group Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router vrrp instance
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router vrrp instance` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show router vrrp instance | match Master
   ```

---

## Procedure to clear ALARM_CODE_1163
**Alarm Name:** LACP Bundle Timeout
**Severity:** Minor

This alarm indicates a timeout condition on the lacp bundle subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1163 for 'LACP Bundle Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lag 1 port
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show lag 1 port` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear lag statistics
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show lag 1 | match active
   ```

---

## Procedure to clear ALARM_CODE_1164
**Alarm Name:** RSVP-TE Tunnel Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the rsvp-te tunnel subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1164 for 'RSVP-TE Tunnel Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router mpls lsp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router rsvp session` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router rsvp session lsp-name {name}
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show router mpls lsp | match Up
   ```

---

## Procedure to clear ALARM_CODE_1165
**Alarm Name:** RSVP-TE Tunnel Out of Sync
**Severity:** Critical

This alarm indicates a out of sync condition on the rsvp-te tunnel subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1165 for 'RSVP-TE Tunnel Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router mpls lsp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router rsvp session` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router mpls lsp {name}
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show router mpls lsp | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1165 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1166
**Alarm Name:** Optical Rx Power Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the optical rx power subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1166 for 'Optical Rx Power Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port 1/1/1 optical
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show system alarms` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure port 1/1/1
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port 1/1/1 | match Up
   ```

---

## Procedure to clear ALARM_CODE_1167
**Alarm Name:** VPLS Pseudowire Loss of Signal (LOS)
**Severity:** Major

This alarm indicates a loss of signal (los) condition on the vpls pseudowire subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1167 for 'VPLS Pseudowire Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ldp bindings active prefixes
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show service sdp-using` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure service vpls {id}
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the vpls pseudowire has returned to a stable operational state:
   ```
   show service sdp-using | match operUp
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1167 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1168
**Alarm Name:** Fan Tray Assembly High CRC Rate
**Severity:** Major

This alarm indicates a high crc rate condition on the fan tray assembly subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1168 for 'Fan Tray Assembly High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system alarms active
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show system alarms active`.
4. **⚠️ WARNING: Service Impact Possible.** If the fan tray assembly utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin environment fan-tray {id} reboot
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   show chassis environment | match Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1168 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1169
**Alarm Name:** Optical Rx Power Configuration Mismatch
**Severity:** Warning

This alarm indicates a configuration mismatch condition on the optical rx power subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1169 for 'Optical Rx Power Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system alarms
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show port 1/1/1 optical` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin port 1/1/1 shutdown
admin port 1/1/1 no shutdown
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port 1/1/1 | match Up
   ```

---

## Procedure to clear ALARM_CODE_1170
**Alarm Name:** Optical Rx Power Stuck in INIT State
**Severity:** Major

This alarm indicates a stuck in init state condition on the optical rx power subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1170 for 'Optical Rx Power Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show port 1/1/1 detail
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show system alarms` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure port 1/1/1
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port 1/1/1 | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1170 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1171
**Alarm Name:** Fan Tray Assembly Down
**Severity:** Warning

This alarm indicates a down condition on the fan tray assembly subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1171 for 'Fan Tray Assembly Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis environment
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show system alarms active` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   tools dump system-resources
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   show chassis environment | match Normal
   ```

---

## Procedure to clear ALARM_CODE_1172
**Alarm Name:** LACP Bundle Flapping
**Severity:** Minor

This alarm indicates a flapping condition on the lacp bundle subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1172 for 'LACP Bundle Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lag 1 port
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show lag 1 statistics` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure lag 1
  admin-state enable
  port 1/1/1
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show lag 1 | match active
   ```

---

## Procedure to clear ALARM_CODE_1173
**Alarm Name:** Management Ethernet Resource Exhaustion
**Severity:** Major

This alarm indicates a resource exhaustion condition on the management ethernet subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1173 for 'Management Ethernet Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router interface mgmt
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router interface mgmt`.
4. **⚠️ WARNING: Service Impact Possible.** If the management ethernet utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin save
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show router interface mgmt | match up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1173 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1174
**Alarm Name:** Management Ethernet Hardware Failure
**Severity:** Minor

This alarm indicates a hardware failure condition on the management ethernet subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1174 for 'Management Ethernet Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router interface mgmt
   ```
3. **Hardware Status Check:** Run `show router interface mgmt` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected management ethernet unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router management
  interface mgmt
  no shutdown
   ```
7. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show router interface mgmt | match up
   ```

---

## Procedure to clear ALARM_CODE_1175
**Alarm Name:** Power Supply Unit (PSU) Out of Sync
**Severity:** Warning

This alarm indicates a out of sync condition on the power supply unit (psu) subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1175 for 'Power Supply Unit (PSU) Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show environment power
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show environment power` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin power-shelf {id} power-module {mod} reboot
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show chassis power-supply | match up
   ```

---

## Procedure to clear ALARM_CODE_1176
**Alarm Name:** Optical Rx Power Loss of Signal (LOS)
**Severity:** Minor

This alarm indicates a loss of signal (los) condition on the optical rx power subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1176 for 'Optical Rx Power Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system alarms
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show port 1/1/1 detail` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin port 1/1/1 shutdown
admin port 1/1/1 no shutdown
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show port 1/1/1 | match Up
   ```

---

## Procedure to clear ALARM_CODE_1177
**Alarm Name:** VPLS Pseudowire Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the vpls pseudowire subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1177 for 'VPLS Pseudowire Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show service sdp-using
   ```
3. **Hardware Status Check:** Run `show service id {id} base` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected vpls pseudowire unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear service id {id} spoke-sdp {spoke}
   ```
7. **Post-Recovery Validation:** Verify the vpls pseudowire has returned to a stable operational state:
   ```
   show service sdp-using | match operUp
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1177 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1178
**Alarm Name:** VRRP Group Performance Degraded
**Severity:** Major

This alarm indicates a performance degraded condition on the vrrp group subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1178 for 'VRRP Group Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router vrrp statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router vrrp statistics`.
4. **⚠️ WARNING: Service Impact Possible.** If the vrrp group utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show router vrrp instance | match Master
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1178 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1179
**Alarm Name:** RSVP-TE Tunnel Memory Leak Detected
**Severity:** Major

This alarm indicates a memory leak detected condition on the rsvp-te tunnel subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1179 for 'RSVP-TE Tunnel Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router mpls lsp
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router rsvp interface`.
4. **⚠️ WARNING: Service Impact Possible.** If the rsvp-te tunnel utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router rsvp session lsp-name {name}
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show router mpls lsp | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1179 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1180
**Alarm Name:** BGP Peer Configuration Mismatch
**Severity:** Critical

This alarm indicates a configuration mismatch condition on the bgp peer subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1180 for 'BGP Peer Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router bgp neighbor {ip}
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show router bgp summary` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router bgp neighbor {ip} soft
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show router bgp summary | match Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1180 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1181
**Alarm Name:** OSPF Adjacency Loss of Signal (LOS)
**Severity:** Warning

This alarm indicates a loss of signal (los) condition on the ospf adjacency subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1181 for 'OSPF Adjacency Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ospf status
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show router ospf status` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router ospf 0 area 0.0.0.0 interface to-PE
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show router ospf neighbor | match Full
   ```

---

## Procedure to clear ALARM_CODE_1182
**Alarm Name:** OSPF Adjacency Performance Degraded
**Severity:** Major

This alarm indicates a performance degraded condition on the ospf adjacency subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1182 for 'OSPF Adjacency Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ospf database
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show router ospf neighbor`.
4. **⚠️ WARNING: Service Impact Possible.** If the ospf adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router ospf 0 area 0.0.0.0 interface to-PE
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show router ospf neighbor | match Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1182 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1183
**Alarm Name:** LACP Bundle Unreachable
**Severity:** Major

This alarm indicates a unreachable condition on the lacp bundle subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1183 for 'LACP Bundle Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lag 1 port
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show lag 1 statistics` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear lag statistics
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show lag 1 | match active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1183 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1184
**Alarm Name:** VPLS Pseudowire Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the vpls pseudowire subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1184 for 'VPLS Pseudowire Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ldp bindings active prefixes
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show service id {id} base`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear service id {id} spoke-sdp {spoke}
   ```
5. **Post-Recovery Validation:** Verify the vpls pseudowire has returned to a stable operational state:
   ```
   show service sdp-using | match operUp
   ```

---

## Procedure to clear ALARM_CODE_1185
**Alarm Name:** MPLS LDP Session Out of Sync
**Severity:** Major

This alarm indicates a out of sync condition on the mpls ldp session subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1185 for 'MPLS LDP Session Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router mpls status
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router ldp session` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router ldp
  admin-state enable
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show router ldp session | match Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1185 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1186
**Alarm Name:** Management Ethernet Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the management ethernet subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1186 for 'Management Ethernet Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router interface mgmt
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router interface mgmt` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router management
  interface mgmt
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show router interface mgmt | match up
   ```

---

## Procedure to clear ALARM_CODE_1187
**Alarm Name:** Power Supply Unit (PSU) Hardware Failure
**Severity:** Critical

This alarm indicates a hardware failure condition on the power supply unit (psu) subsystem of Nokia equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1187 for 'Power Supply Unit (PSU) Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show environment power
   ```
3. **Hardware Status Check:** Run `show chassis power-supply` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected power supply unit (psu) unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   tools perform system power-check
   ```
7. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show chassis power-supply | match up
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1187 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1188
**Alarm Name:** Fan Tray Assembly Loss of Signal (LOS)
**Severity:** Minor

This alarm indicates a loss of signal (los) condition on the fan tray assembly subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1188 for 'Fan Tray Assembly Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system alarms active
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show chassis environment` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin environment fan-tray {id} reboot
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   show chassis environment | match Normal
   ```

---

## Procedure to clear ALARM_CODE_1189
**Alarm Name:** Power Supply Unit (PSU) Down
**Severity:** Warning

This alarm indicates a down condition on the power supply unit (psu) subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1189 for 'Power Supply Unit (PSU) Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis power-supply
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show environment power` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   admin power-shelf {id} power-module {mod} reboot
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show chassis power-supply | match up
   ```

---

## Procedure to clear ALARM_CODE_1190
**Alarm Name:** MPLS LDP Session Stuck in INIT State
**Severity:** Minor

This alarm indicates a stuck in init state condition on the mpls ldp session subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1190 for 'MPLS LDP Session Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ldp session
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router mpls status` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router ldp session {ip}
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show router ldp session | match Established
   ```

---

## Procedure to clear ALARM_CODE_1191
**Alarm Name:** Management Ethernet Capacity Limit Reached
**Severity:** Minor

This alarm indicates a capacity limit reached condition on the management ethernet subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1191 for 'Management Ethernet Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router interface mgmt
   ```
3. **Hardware Status Check:** Run `show router interface mgmt` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected management ethernet unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router management
  interface mgmt
  no shutdown
   ```
7. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show router interface mgmt | match up
   ```

---

## Procedure to clear ALARM_CODE_1192
**Alarm Name:** Management Ethernet Timeout
**Severity:** Warning

This alarm indicates a timeout condition on the management ethernet subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1192 for 'Management Ethernet Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system information
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show system information` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   configure router management
  interface mgmt
  no shutdown
   ```
6. **Post-Recovery Validation:** Verify the management ethernet has returned to a stable operational state:
   ```
   show router interface mgmt | match up
   ```

---

## Procedure to clear ALARM_CODE_1193
**Alarm Name:** VPLS Pseudowire Flapping
**Severity:** Major

This alarm indicates a flapping condition on the vpls pseudowire subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1193 for 'VPLS Pseudowire Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show service sdp-using
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show service id {id} base` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear service id {id} spoke-sdp {spoke}
   ```
6. **Post-Recovery Validation:** Verify the vpls pseudowire has returned to a stable operational state:
   ```
   show service sdp-using | match operUp
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1193 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1194
**Alarm Name:** VRRP Group Stuck in INIT State
**Severity:** Minor

This alarm indicates a stuck in init state condition on the vrrp group subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1194 for 'VRRP Group Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router vrrp statistics
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router vrrp statistics` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   show router vrrp instance | match Master
   ```

---

## Procedure to clear ALARM_CODE_1195
**Alarm Name:** VPLS Pseudowire Down
**Severity:** Warning

This alarm indicates a down condition on the vpls pseudowire subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1195 for 'VPLS Pseudowire Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show service sdp-using
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show service sdp-using` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear service id {id} spoke-sdp {spoke}
   ```
6. **Post-Recovery Validation:** Verify the vpls pseudowire has returned to a stable operational state:
   ```
   show service sdp-using | match operUp
   ```

---

## Procedure to clear ALARM_CODE_1196
**Alarm Name:** RSVP-TE Tunnel Down
**Severity:** Minor

This alarm indicates a down condition on the rsvp-te tunnel subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1196 for 'RSVP-TE Tunnel Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router rsvp session
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show router rsvp interface` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear router rsvp session lsp-name {name}
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show router mpls lsp | match Up
   ```

---

## Procedure to clear ALARM_CODE_1197
**Alarm Name:** Power Supply Unit (PSU) Authentication Failed
**Severity:** Major

This alarm indicates a authentication failed condition on the power supply unit (psu) subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1197 for 'Power Supply Unit (PSU) Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis power-supply
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show environment power` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   tools perform system power-check
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   show chassis power-supply | match up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1197 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1198
**Alarm Name:** VPLS Pseudowire Out of Sync
**Severity:** Major

This alarm indicates a out of sync condition on the vpls pseudowire subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1198 for 'VPLS Pseudowire Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router ldp bindings active prefixes
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router ldp bindings active prefixes` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear service id {id} spoke-sdp {spoke}
   ```
6. **Post-Recovery Validation:** Verify the vpls pseudowire has returned to a stable operational state:
   ```
   show service sdp-using | match operUp
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Nokia TAC (Technical Assistance Center) with the alarm code 1198 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1199
**Alarm Name:** EVPN MAC Route Out of Sync
**Severity:** Minor

This alarm indicates a out of sync condition on the evpn mac route subsystem of Nokia equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Nokia NMS dashboard and confirm alarm code 1199 for 'EVPN MAC Route Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show router bgp evpn routes
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show router bgp evpn routes` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear service evpn mac-table
   ```
6. **Post-Recovery Validation:** Verify the evpn mac route has returned to a stable operational state:
   ```
   show service evpn | match active
   ```

# Juniper JunOS Service Restoration MOP (Method of Procedure)

**Equipment Vendor:** Juniper
**Document Type:** Standard Operating Procedure (SOP)
**Scope:** JunOS MX-Series / PTX-Series Router Troubleshooting
**Network Topology Context:** Provider Edge (PE) Router

## Overview
This document provides the standard operating procedures for resolving common alarms on Juniper Networks MX-Series and PTX-Series routers running JunOS as Provider Edge (PE) nodes. Always verify Customer SLA tags. All commands must be executed from the CLI operational mode unless otherwise stated. Configuration changes require `commit confirm 5` to auto-rollback if connectivity is lost.

---

## Procedure to clear ALARM_CODE_601
**Alarm Name:** IS-IS Adjacency Failure (MTU Mismatch)
**Severity:** Critical

This alarm triggers when an IS-IS adjacency between two Juniper routers fails to reach the UP state due to a Maximum Transmission Unit (MTU) mismatch on the interconnecting interface. IS-IS PDUs larger than the smallest MTU on the link will be silently discarded, preventing adjacency formation.

1. **Confirm Adjacency State:** Run `show isis adjacency` to verify the neighbor is in the INIT or DOWN state, not UP.
2. **Check IS-IS Interface Details:** Run `show isis interface <interface-name> detail` and note the reported MTU value under "PDU MTU size".
3. **Check Physical MTU:** Run `show interfaces <interface-name> | match MTU` to see the configured interface MTU (e.g., 9192 for jumbo frames or 1514 for standard Ethernet).
4. **Compare with Remote Router:** SSH to the remote peer and run the same `show interfaces` command. The IS-IS MTU must match on both ends. Common mismatch: one side has jumbo frames (9192) enabled and the other uses default (1514).
5. **Align the MTU:** On the side that needs to change, enter configuration mode:
   ```
   configure
   set interfaces <interface-name> mtu <CORRECT_MTU_VALUE>
   commit confirm 5
   ```
   **Warning:** Use `commit confirm 5` so the router will automatically rollback in 5 minutes if you lose connectivity due to the change.
6. **Confirm and Finalize:** Once the IS-IS adjacency comes up (visible via `show isis adjacency`), confirm the commit:
   ```
   commit
   ```
7. **Verify Routing Table:** Run `show route protocol isis` to verify IS-IS routes are being learned from the peer. Confirm end-to-end reachability with `ping <remote-loopback-ip> source <local-loopback-ip> size 8972 do-not-fragment` to validate jumbo MTU is working.

---

## Procedure to clear ALARM_CODE_602
**Alarm Name:** Routing Engine High CPU Utilization
**Severity:** Warning

This alarm fires when the Routing Engine (RE) CPU utilization exceeds 85% for more than 5 consecutive minutes. Sustained high CPU can cause protocol timeouts (BGP, OSPF, IS-IS), delayed CLI response, and potential traffic forwarding degradation.

1. **Check Overall CPU:** Run `show chassis routing-engine` to see current CPU utilization for both RE0 and RE1 (if dual-RE). Note the "CPU utilization" percentages for User, System, and Interrupt.
2. **Identify Top Processes:** Run `show system processes extensive | match "PID|%CPU" | head 20` to list the top CPU-consuming processes. Common culprits include `rpd` (routing protocol daemon), `dfwd` (firewall daemon), or `snmpd`.
3. **Check for Route Churn:** If `rpd` is the top consumer, run `show route summary` and compare the total route count against the baseline. A route leak or flapping peer can cause massive churn. Run `show bgp summary | match Estab` to identify any peers that are flapping.
4. **Check SNMP Polling:** If `snmpd` is the culprit, a misconfigured NMS (Network Management System) may be polling too aggressively. Run `show snmp statistics` and check the "Get-request" counter rate. Contact the NMS team to reduce polling frequency to no less than 300-second intervals.
5. **Check for DDoS Protection Events:** Run `show ddos-protection protocols statistics terse` to see if the control plane is being hit by a traffic storm (e.g., ARP, ICMP, or TTL-expired packets).
6. **Mitigate if DDoS Detected:** If a specific protocol is exceeding its policer, increase the policer bandwidth temporarily:
   ```
   configure
   set system ddos-protection protocols <protocol-name> aggregate bandwidth <new-value>
   commit confirm 5
   ```
7. **Monitor Recovery:** Run `show chassis routing-engine` every 60 seconds for 5 minutes and confirm CPU returns below 70%. If CPU remains elevated, capture a diagnostic snapshot:
   ```
   request system diagnostics running-config-check
   file archive compress source /var/log/ destination /var/tmp/cpu-diag.tgz
   ```
   Escalate to Juniper JTAC with the diagnostic archive attached.


---

## Procedure to clear ALARM_CODE_1200
**Alarm Name:** Radius/TACACS Auth Stuck in INIT State
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1200 representing 'Radius/TACACS Auth Stuck in INIT State' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1201
**Alarm Name:** BFD Session Out of Sync
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1201 representing 'BFD Session Out of Sync' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1202
**Alarm Name:** RSVP-TE Tunnel Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1202 representing 'RSVP-TE Tunnel Stuck in INIT State' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1203
**Alarm Name:** EVPN MAC Route Capacity Limit Reached
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1203 representing 'EVPN MAC Route Capacity Limit Reached' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1204
**Alarm Name:** FIB (Forwarding Table) Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1204 representing 'FIB (Forwarding Table) Stuck in INIT State' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1205
**Alarm Name:** Multicast PIM Neighbor Flapping
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1205 representing 'Multicast PIM Neighbor Flapping' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1206
**Alarm Name:** DHCP Relay Agent Configuration Mismatch
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1206 representing 'DHCP Relay Agent Configuration Mismatch' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1207
**Alarm Name:** BFD Session Performance Degraded
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1207 representing 'BFD Session Performance Degraded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1208
**Alarm Name:** BGP Route Reflector Authentication Failed
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1208 representing 'BGP Route Reflector Authentication Failed' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1209
**Alarm Name:** VPLS Pseudowire Authentication Failed
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1209 representing 'VPLS Pseudowire Authentication Failed' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1210
**Alarm Name:** HSRP Instance Capacity Limit Reached
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1210 representing 'HSRP Instance Capacity Limit Reached' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1211
**Alarm Name:** GRE Tunnel Configuration Mismatch
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1211 representing 'GRE Tunnel Configuration Mismatch' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1212
**Alarm Name:** IGMP Snooping High Cyclic Redundancy (CRC) Rate
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1212 representing 'IGMP Snooping High Cyclic Redundancy (CRC) Rate' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1213
**Alarm Name:** FIB (Forwarding Table) Configuration Mismatch
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1213 representing 'FIB (Forwarding Table) Configuration Mismatch' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1214
**Alarm Name:** Line Card NPU Configuration Mismatch
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1214 representing 'Line Card NPU Configuration Mismatch' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1215
**Alarm Name:** Multicast PIM Neighbor Configuration Mismatch
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1215 representing 'Multicast PIM Neighbor Configuration Mismatch' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1216
**Alarm Name:** Switch Fabric Module Timeout
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1216 representing 'Switch Fabric Module Timeout' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1217
**Alarm Name:** HSRP Instance Down
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1217 representing 'HSRP Instance Down' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1218
**Alarm Name:** Radius/TACACS Auth Unreachable
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1218 representing 'Radius/TACACS Auth Unreachable' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1219
**Alarm Name:** MPLS LDP Session Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1219 representing 'MPLS LDP Session Threshold Exceeded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1220
**Alarm Name:** Line Card NPU Memory Leak Detected
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1220 representing 'Line Card NPU Memory Leak Detected' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1221
**Alarm Name:** FIB (Forwarding Table) Authentication Failed
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1221 representing 'FIB (Forwarding Table) Authentication Failed' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1222
**Alarm Name:** VRRP Group Resource Exhaustion
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1222 representing 'VRRP Group Resource Exhaustion' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1223
**Alarm Name:** QoS Scheduler Authentication Failed
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1223 representing 'QoS Scheduler Authentication Failed' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1224
**Alarm Name:** Line Card NPU Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1224 representing 'Line Card NPU Performance Degraded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1225
**Alarm Name:** Management Ethernet Stuck in INIT State
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1225 representing 'Management Ethernet Stuck in INIT State' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1226
**Alarm Name:** OSPF Adjacency Loss of Signal (LOS)
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1226 representing 'OSPF Adjacency Loss of Signal (LOS)' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1227
**Alarm Name:** ARP Cache Unreachable
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1227 representing 'ARP Cache Unreachable' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1228
**Alarm Name:** QoS Scheduler Unreachable
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1228 representing 'QoS Scheduler Unreachable' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1229
**Alarm Name:** EVPN MAC Route Down
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1229 representing 'EVPN MAC Route Down' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1230
**Alarm Name:** HSRP Instance Timeout
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1230 representing 'HSRP Instance Timeout' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1231
**Alarm Name:** Switch Fabric Module Unreachable
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1231 representing 'Switch Fabric Module Unreachable' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1232
**Alarm Name:** RSVP-TE Tunnel Loss of Signal (LOS)
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1232 representing 'RSVP-TE Tunnel Loss of Signal (LOS)' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1233
**Alarm Name:** VRRP Group Timeout
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1233 representing 'VRRP Group Timeout' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1234
**Alarm Name:** Management Ethernet Unreachable
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1234 representing 'Management Ethernet Unreachable' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1235
**Alarm Name:** Optical Rx Power Unreachable
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1235 representing 'Optical Rx Power Unreachable' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1236
**Alarm Name:** IGMP Snooping Resource Exhaustion
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1236 representing 'IGMP Snooping Resource Exhaustion' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1237
**Alarm Name:** Optical Tx Power Memory Leak Detected
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1237 representing 'Optical Tx Power Memory Leak Detected' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1238
**Alarm Name:** Fan Tray Assembly Capacity Limit Reached
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1238 representing 'Fan Tray Assembly Capacity Limit Reached' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1239
**Alarm Name:** OSPF Adjacency Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1239 representing 'OSPF Adjacency Threshold Exceeded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1240
**Alarm Name:** SNMP Agent Timeout
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1240 representing 'SNMP Agent Timeout' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1241
**Alarm Name:** IGMP Snooping Flapping
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1241 representing 'IGMP Snooping Flapping' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1242
**Alarm Name:** OAM Connectivity Loss of Signal (LOS)
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1242 representing 'OAM Connectivity Loss of Signal (LOS)' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1243
**Alarm Name:** HSRP Instance Hardware Failure
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1243 representing 'HSRP Instance Hardware Failure' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1244
**Alarm Name:** IS-IS Adjacency High Cyclic Redundancy (CRC) Rate
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1244 representing 'IS-IS Adjacency High Cyclic Redundancy (CRC) Rate' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1245
**Alarm Name:** Line Card NPU Flapping
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1245 representing 'Line Card NPU Flapping' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1246
**Alarm Name:** Line Card NPU Timeout
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1246 representing 'Line Card NPU Timeout' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1247
**Alarm Name:** VRRP Group Performance Degraded
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1247 representing 'VRRP Group Performance Degraded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1248
**Alarm Name:** Optical Tx Power Authentication Failed
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1248 representing 'Optical Tx Power Authentication Failed' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1249
**Alarm Name:** Switch Fabric Module Flapping
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1249 representing 'Switch Fabric Module Flapping' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1250
**Alarm Name:** GRE Tunnel Memory Leak Detected
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1250 representing 'GRE Tunnel Memory Leak Detected' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1251
**Alarm Name:** ACL Processing Unreachable
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1251 representing 'ACL Processing Unreachable' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1252
**Alarm Name:** VRRP Group Down
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1252 representing 'VRRP Group Down' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1253
**Alarm Name:** STP Root Topology Flapping
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1253 representing 'STP Root Topology Flapping' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1254
**Alarm Name:** FIB (Forwarding Table) Flapping
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1254 representing 'FIB (Forwarding Table) Flapping' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1255
**Alarm Name:** Multicast PIM Neighbor Out of Sync
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1255 representing 'Multicast PIM Neighbor Out of Sync' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1256
**Alarm Name:** VPLS Pseudowire Down
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1256 representing 'VPLS Pseudowire Down' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1257
**Alarm Name:** RSVP-TE Tunnel Configuration Mismatch
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1257 representing 'RSVP-TE Tunnel Configuration Mismatch' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1258
**Alarm Name:** DHCP Relay Agent Performance Degraded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1258 representing 'DHCP Relay Agent Performance Degraded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1259
**Alarm Name:** Optical Tx Power Flapping
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1259 representing 'Optical Tx Power Flapping' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1260
**Alarm Name:** Power Supply Unit (PSU) Threshold Exceeded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1260 representing 'Power Supply Unit (PSU) Threshold Exceeded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1261
**Alarm Name:** ACL Processing Configuration Mismatch
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1261 representing 'ACL Processing Configuration Mismatch' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1262
**Alarm Name:** GRE Tunnel High Cyclic Redundancy (CRC) Rate
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1262 representing 'GRE Tunnel High Cyclic Redundancy (CRC) Rate' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1263
**Alarm Name:** IGMP Snooping Out of Sync
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1263 representing 'IGMP Snooping Out of Sync' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1264
**Alarm Name:** IPSec VPN Tunnel Timeout
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1264 representing 'IPSec VPN Tunnel Timeout' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1265
**Alarm Name:** BGP Route Reflector Memory Leak Detected
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1265 representing 'BGP Route Reflector Memory Leak Detected' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1266
**Alarm Name:** Optical Tx Power Timeout
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1266 representing 'Optical Tx Power Timeout' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1267
**Alarm Name:** STP Root Topology High Cyclic Redundancy (CRC) Rate
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1267 representing 'STP Root Topology High Cyclic Redundancy (CRC) Rate' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1268
**Alarm Name:** Management Ethernet Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1268 representing 'Management Ethernet Performance Degraded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1269
**Alarm Name:** BGP Peer Authentication Failed
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1269 representing 'BGP Peer Authentication Failed' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1270
**Alarm Name:** BGP Route Reflector Configuration Mismatch
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1270 representing 'BGP Route Reflector Configuration Mismatch' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1271
**Alarm Name:** IPSec VPN Tunnel Configuration Mismatch
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1271 representing 'IPSec VPN Tunnel Configuration Mismatch' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1272
**Alarm Name:** MAC Address Table Performance Degraded
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1272 representing 'MAC Address Table Performance Degraded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1273
**Alarm Name:** IS-IS Adjacency Memory Leak Detected
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1273 representing 'IS-IS Adjacency Memory Leak Detected' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1274
**Alarm Name:** STP Root Topology Performance Degraded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1274 representing 'STP Root Topology Performance Degraded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1275
**Alarm Name:** NTP Synchronization Capacity Limit Reached
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1275 representing 'NTP Synchronization Capacity Limit Reached' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1276
**Alarm Name:** HSRP Instance Configuration Mismatch
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1276 representing 'HSRP Instance Configuration Mismatch' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1277
**Alarm Name:** MPLS LDP Session Authentication Failed
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1277 representing 'MPLS LDP Session Authentication Failed' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1278
**Alarm Name:** Switch Fabric Module Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1278 representing 'Switch Fabric Module Stuck in INIT State' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1279
**Alarm Name:** BGP Route Reflector Unreachable
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1279 representing 'BGP Route Reflector Unreachable' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1280
**Alarm Name:** VRRP Group Memory Leak Detected
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1280 representing 'VRRP Group Memory Leak Detected' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1281
**Alarm Name:** Multicast PIM Neighbor Timeout
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1281 representing 'Multicast PIM Neighbor Timeout' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1282
**Alarm Name:** IPSec VPN Tunnel Resource Exhaustion
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1282 representing 'IPSec VPN Tunnel Resource Exhaustion' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1283
**Alarm Name:** IS-IS Adjacency Flapping
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1283 representing 'IS-IS Adjacency Flapping' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1284
**Alarm Name:** ARP Cache Authentication Failed
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1284 representing 'ARP Cache Authentication Failed' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1285
**Alarm Name:** Radius/TACACS Auth Out of Sync
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1285 representing 'Radius/TACACS Auth Out of Sync' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1286
**Alarm Name:** EVPN MAC Route Hardware Failure
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1286 representing 'EVPN MAC Route Hardware Failure' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1287
**Alarm Name:** Radius/TACACS Auth Threshold Exceeded
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1287 representing 'Radius/TACACS Auth Threshold Exceeded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1288
**Alarm Name:** Management Ethernet Capacity Limit Reached
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1288 representing 'Management Ethernet Capacity Limit Reached' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1289
**Alarm Name:** GRE Tunnel Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1289 representing 'GRE Tunnel Stuck in INIT State' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1290
**Alarm Name:** SNMP Agent Unreachable
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1290 representing 'SNMP Agent Unreachable' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1291
**Alarm Name:** ARP Cache Hardware Failure
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1291 representing 'ARP Cache Hardware Failure' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1292
**Alarm Name:** DHCP Relay Agent Down
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1292 representing 'DHCP Relay Agent Down' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1293
**Alarm Name:** Radius/TACACS Auth Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1293 representing 'Radius/TACACS Auth Performance Degraded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1294
**Alarm Name:** LACP Bundle Out of Sync
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1294 representing 'LACP Bundle Out of Sync' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1295
**Alarm Name:** Management Ethernet Resource Exhaustion
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1295 representing 'Management Ethernet Resource Exhaustion' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1296
**Alarm Name:** Fan Tray Assembly Stuck in INIT State
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1296 representing 'Fan Tray Assembly Stuck in INIT State' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1297
**Alarm Name:** RSVP-TE Tunnel Threshold Exceeded
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1297 representing 'RSVP-TE Tunnel Threshold Exceeded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1298
**Alarm Name:** Multicast PIM Neighbor Down
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1298 representing 'Multicast PIM Neighbor Down' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1299
**Alarm Name:** FIB (Forwarding Table) Performance Degraded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1299 representing 'FIB (Forwarding Table) Performance Degraded' on the Juniper NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   show chassis hardware
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   clear bgp neighbor
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.


<!-- BEGIN GENERATED PROCEDURES -->

---

## Procedure to clear ALARM_CODE_1200
**Alarm Name:** BFD Session Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the bfd session subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1200 for 'BFD Session Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session summary
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bfd session summary`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bfd session address {ip}
   ```
5. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | match Up
   ```

---

## Procedure to clear ALARM_CODE_1201
**Alarm Name:** IS-IS Adjacency Loss of Signal (LOS)
**Severity:** Major

This alarm indicates a loss of signal (los) condition on the is-is adjacency subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1201 for 'IS-IS Adjacency Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis interface
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show isis adjacency` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols isis interface ge-0/0/0 level 2
commit
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1201 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1202
**Alarm Name:** IPSec VPN Tunnel Capacity Limit Reached
**Severity:** Critical

This alarm indicates a capacity limit reached condition on the ipsec vpn tunnel subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1202 for 'IPSec VPN Tunnel Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show security ipsec sa
   ```
3. **Hardware Status Check:** Run `show security ipsec statistics` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected ipsec vpn tunnel unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear security ipsec sa
   ```
7. **Post-Recovery Validation:** Verify the ipsec vpn tunnel has returned to a stable operational state:
   ```
   show security ipsec sa | match "Total active"
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1202 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1203
**Alarm Name:** Routing Engine CPU High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the routing engine cpu subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1203 for 'Routing Engine CPU High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system processes extensive
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show system processes extensive`.
4. **⚠️ WARNING: Service Impact Possible.** If the routing engine cpu utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   restart routing immediately
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show chassis routing-engine | match "Idle"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1203 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1204
**Alarm Name:** ARP Cache Performance Degraded
**Severity:** Critical

This alarm indicates a performance degraded condition on the arp cache subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1204 for 'ARP Cache Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show arp
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show arp`.
4. **⚠️ WARNING: Service Impact Possible.** If the arp cache utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp hostname {host}
   ```
6. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   show arp | match "Total entries"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1204 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1205
**Alarm Name:** FIB (Forwarding Table) Timeout
**Severity:** Warning

This alarm indicates a timeout condition on the fib (forwarding table) subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1205 for 'FIB (Forwarding Table) Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route forwarding-table
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show route forwarding-table` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear route forwarding-table
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show krt queue | match "0 queued"
   ```

---

## Procedure to clear ALARM_CODE_1206
**Alarm Name:** Optical Rx Power Threshold Exceeded
**Severity:** Warning

This alarm indicates a threshold exceeded condition on the optical rx power subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1206 for 'Optical Rx Power Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interfaces diagnostics optics ge-0/0/1
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show chassis hardware`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   request interface diagnostics optics ge-0/0/1
   ```
5. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show interfaces diagnostics optics ge-0/0/1 | match "Rx power"
   ```

---

## Procedure to clear ALARM_CODE_1207
**Alarm Name:** OSPF Adjacency Unreachable
**Severity:** Major

This alarm indicates a unreachable condition on the ospf adjacency subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1207 for 'OSPF Adjacency Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf interface
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show ospf database` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ospf neighbor all
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | match Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1207 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1208
**Alarm Name:** ACL Processing Flapping
**Severity:** Major

This alarm indicates a flapping condition on the acl processing subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1208 for 'ACL Processing Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show firewall counter
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show firewall counter` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear firewall filter PROTECT_RE counter
   ```
6. **Post-Recovery Validation:** Verify the acl processing has returned to a stable operational state:
   ```
   show firewall counter | match ALLOW_BGP
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1208 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1209
**Alarm Name:** BGP Peer Flapping
**Severity:** Major

This alarm indicates a flapping condition on the bgp peer subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1209 for 'BGP Peer Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp neighbor {ip}
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show bgp neighbor {ip}` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols bgp group EXTERNAL neighbor {ip}
commit
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | match Estab
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1209 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1210
**Alarm Name:** BGP Peer Out of Sync
**Severity:** Major

This alarm indicates a out of sync condition on the bgp peer subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1210 for 'BGP Peer Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp neighbor {ip}
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show bgp neighbor {ip}` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bgp neighbor {ip}
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | match Estab
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1210 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1211
**Alarm Name:** Optical Rx Power Resource Exhaustion
**Severity:** Major

This alarm indicates a resource exhaustion condition on the optical rx power subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1211 for 'Optical Rx Power Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis hardware
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show interfaces diagnostics optics ge-0/0/1`.
4. **⚠️ WARNING: Service Impact Possible.** If the optical rx power utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   request interface diagnostics optics ge-0/0/1
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show interfaces diagnostics optics ge-0/0/1 | match "Rx power"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1211 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1212
**Alarm Name:** IPSec VPN Tunnel Threshold Exceeded
**Severity:** Major

This alarm indicates a threshold exceeded condition on the ipsec vpn tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1212 for 'IPSec VPN Tunnel Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show security ipsec statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show security ipsec sa`.
4. **⚠️ WARNING: Service Impact Possible.** If the ipsec vpn tunnel utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear security ipsec sa
   ```
6. **Post-Recovery Validation:** Verify the ipsec vpn tunnel has returned to a stable operational state:
   ```
   show security ipsec sa | match "Total active"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1212 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1213
**Alarm Name:** Routing Engine CPU Authentication Failed
**Severity:** Critical

This alarm indicates a authentication failed condition on the routing engine cpu subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1213 for 'Routing Engine CPU Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system uptime
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show system processes extensive` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   restart routing immediately
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show chassis routing-engine | match "Idle"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1213 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1214
**Alarm Name:** BFD Session Hardware Failure
**Severity:** Critical

This alarm indicates a hardware failure condition on the bfd session subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1214 for 'BFD Session Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session
   ```
3. **Hardware Status Check:** Run `show bfd session detail` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected bfd session unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bfd session address {ip}
   ```
7. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | match Up
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1214 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1215
**Alarm Name:** OSPF Adjacency High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the ospf adjacency subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1215 for 'OSPF Adjacency High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf neighbor
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ospf database`.
4. **⚠️ WARNING: Service Impact Possible.** If the ospf adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ospf neighbor all
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | match Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1215 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1216
**Alarm Name:** RSVP-TE Tunnel Unreachable
**Severity:** Major

This alarm indicates a unreachable condition on the rsvp-te tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1216 for 'RSVP-TE Tunnel Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show rsvp session
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show rsvp session` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear rsvp session lsp-name {name}
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show mpls lsp | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1216 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1217
**Alarm Name:** BFD Session Resource Exhaustion
**Severity:** Critical

This alarm indicates a resource exhaustion condition on the bfd session subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1217 for 'BFD Session Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session detail
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bfd session`.
4. **⚠️ WARNING: Service Impact Possible.** If the bfd session utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ospf area 0 interface ge-0/0/0 bfd-liveness-detection minimum-interval 300
commit
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1217 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1218
**Alarm Name:** LACP Bundle Authentication Failed
**Severity:** Warning

This alarm indicates a authentication failed condition on the lacp bundle subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1218 for 'LACP Bundle Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lacp statistics
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show interfaces ae0` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set interfaces ae0
  aggregated-ether-options lacp active
commit
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show interfaces ae0 | match "Physical link is Up"
   ```

---

## Procedure to clear ALARM_CODE_1219
**Alarm Name:** IS-IS Adjacency Flapping
**Severity:** Warning

This alarm indicates a flapping condition on the is-is adjacency subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1219 for 'IS-IS Adjacency Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis database
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show isis database` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols isis interface ge-0/0/0 level 2
commit
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | match Up
   ```

---

## Procedure to clear ALARM_CODE_1220
**Alarm Name:** FIB (Forwarding Table) Hardware Failure
**Severity:** Minor

This alarm indicates a hardware failure condition on the fib (forwarding table) subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1220 for 'FIB (Forwarding Table) Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route forwarding-table
   ```
3. **Hardware Status Check:** Run `show route summary` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected fib (forwarding table) unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   request route consistency-check
   ```
7. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show krt queue | match "0 queued"
   ```

---

## Procedure to clear ALARM_CODE_1221
**Alarm Name:** IS-IS Adjacency Configuration Mismatch
**Severity:** Warning

This alarm indicates a configuration mismatch condition on the is-is adjacency subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1221 for 'IS-IS Adjacency Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis adjacency
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show isis database` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols isis interface ge-0/0/0 level 2
commit
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | match Up
   ```

---

## Procedure to clear ALARM_CODE_1222
**Alarm Name:** IS-IS Adjacency Down
**Severity:** Minor

This alarm indicates a down condition on the is-is adjacency subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1222 for 'IS-IS Adjacency Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis database
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show isis adjacency` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear isis adjacency
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | match Up
   ```

---

## Procedure to clear ALARM_CODE_1223
**Alarm Name:** Routing Engine CPU Hardware Failure
**Severity:** Critical

This alarm indicates a hardware failure condition on the routing engine cpu subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1223 for 'Routing Engine CPU Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system processes extensive
   ```
3. **Hardware Status Check:** Run `show system processes extensive` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected routing engine cpu unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   restart routing immediately
   ```
7. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show chassis routing-engine | match "Idle"
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1223 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1224
**Alarm Name:** BFD Session Capacity Limit Reached
**Severity:** Minor

This alarm indicates a capacity limit reached condition on the bfd session subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1224 for 'BFD Session Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session detail
   ```
3. **Hardware Status Check:** Run `show bfd session detail` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected bfd session unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bfd session address {ip}
   ```
7. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | match Up
   ```

---

## Procedure to clear ALARM_CODE_1225
**Alarm Name:** RSVP-TE Tunnel Memory Leak Detected
**Severity:** Critical

This alarm indicates a memory leak detected condition on the rsvp-te tunnel subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1225 for 'RSVP-TE Tunnel Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show rsvp interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls lsp`.
4. **⚠️ WARNING: Service Impact Possible.** If the rsvp-te tunnel utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols mpls label-switched-path {name}
  no-install
  deactivate
commit
activate
commit
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   show mpls lsp | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1225 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1226
**Alarm Name:** GRE Tunnel Threshold Exceeded
**Severity:** Major

This alarm indicates a threshold exceeded condition on the gre tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1226 for 'GRE Tunnel Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interfaces gr-0/0/0
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show route table inet.0 protocol static`.
4. **⚠️ WARNING: Service Impact Possible.** If the gre tunnel utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear interfaces statistics gr-0/0/0
   ```
6. **Post-Recovery Validation:** Verify the gre tunnel has returned to a stable operational state:
   ```
   show interfaces gr-0/0/0 | match "Link is Up"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1226 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1227
**Alarm Name:** BGP Peer Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the bgp peer subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1227 for 'BGP Peer Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp neighbor {ip}
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bgp summary`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols bgp group EXTERNAL neighbor {ip}
commit
   ```
5. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | match Estab
   ```

---

## Procedure to clear ALARM_CODE_1228
**Alarm Name:** Optical Rx Power Configuration Mismatch
**Severity:** Minor

This alarm indicates a configuration mismatch condition on the optical rx power subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1228 for 'Optical Rx Power Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interfaces diagnostics optics ge-0/0/1
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show chassis hardware` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   request interface diagnostics optics ge-0/0/1
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show interfaces diagnostics optics ge-0/0/1 | match "Rx power"
   ```

---

## Procedure to clear ALARM_CODE_1229
**Alarm Name:** Multicast PIM Neighbor Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the multicast pim neighbor subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1229 for 'Multicast PIM Neighbor Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show multicast route
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show pim neighbors`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear pim join all
   ```
5. **Post-Recovery Validation:** Verify the multicast pim neighbor has returned to a stable operational state:
   ```
   show pim neighbors | match ge-
   ```

---

## Procedure to clear ALARM_CODE_1230
**Alarm Name:** ARP Cache Configuration Mismatch
**Severity:** Major

This alarm indicates a configuration mismatch condition on the arp cache subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1230 for 'ARP Cache Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show arp statistics
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show interfaces ge-0/0/0` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp hostname {host}
   ```
6. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   show arp | match "Total entries"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1230 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1231
**Alarm Name:** FIB (Forwarding Table) Flapping
**Severity:** Warning

This alarm indicates a flapping condition on the fib (forwarding table) subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1231 for 'FIB (Forwarding Table) Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route forwarding-table
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show route forwarding-table` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear route forwarding-table
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show krt queue | match "0 queued"
   ```

---

## Procedure to clear ALARM_CODE_1232
**Alarm Name:** OSPF Adjacency Configuration Mismatch
**Severity:** Minor

This alarm indicates a configuration mismatch condition on the ospf adjacency subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1232 for 'OSPF Adjacency Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf interface
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show ospf neighbor` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ospf area 0.0.0.0 interface ge-0/0/0
commit
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | match Full
   ```

---

## Procedure to clear ALARM_CODE_1233
**Alarm Name:** BGP Peer Resource Exhaustion
**Severity:** Warning

This alarm indicates a resource exhaustion condition on the bgp peer subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1233 for 'BGP Peer Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route protocol bgp
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bgp neighbor {ip}`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bgp neighbor {ip}
   ```
5. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | match Estab
   ```

---

## Procedure to clear ALARM_CODE_1234
**Alarm Name:** LACP Bundle Hardware Failure
**Severity:** Critical

This alarm indicates a hardware failure condition on the lacp bundle subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1234 for 'LACP Bundle Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lacp interfaces
   ```
3. **Hardware Status Check:** Run `show interfaces ae0` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected lacp bundle unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear lacp statistics
   ```
7. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show interfaces ae0 | match "Physical link is Up"
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1234 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1235
**Alarm Name:** IS-IS Adjacency Performance Degraded
**Severity:** Critical

This alarm indicates a performance degraded condition on the is-is adjacency subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1235 for 'IS-IS Adjacency Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis adjacency
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show isis database`.
4. **⚠️ WARNING: Service Impact Possible.** If the is-is adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols isis interface ge-0/0/0 level 2
commit
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1235 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1236
**Alarm Name:** BGP Peer Timeout
**Severity:** Major

This alarm indicates a timeout condition on the bgp peer subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1236 for 'BGP Peer Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp neighbor {ip}
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show bgp neighbor {ip}` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bgp neighbor {ip}
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | match Estab
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1236 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1237
**Alarm Name:** GRE Tunnel Timeout
**Severity:** Major

This alarm indicates a timeout condition on the gre tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1237 for 'GRE Tunnel Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interfaces gr-0/0/0
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show route table inet.0 protocol static` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set interfaces gr-0/0/0 unit 0 tunnel source {src} destination {dst}
commit
   ```
6. **Post-Recovery Validation:** Verify the gre tunnel has returned to a stable operational state:
   ```
   show interfaces gr-0/0/0 | match "Link is Up"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1237 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1238
**Alarm Name:** FIB (Forwarding Table) Authentication Failed
**Severity:** Minor

This alarm indicates a authentication failed condition on the fib (forwarding table) subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1238 for 'FIB (Forwarding Table) Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route forwarding-table
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show route forwarding-table` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear route forwarding-table
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show krt queue | match "0 queued"
   ```

---

## Procedure to clear ALARM_CODE_1239
**Alarm Name:** Routing Engine CPU Flapping
**Severity:** Minor

This alarm indicates a flapping condition on the routing engine cpu subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1239 for 'Routing Engine CPU Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system processes extensive
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show system processes extensive` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   restart routing immediately
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show chassis routing-engine | match "Idle"
   ```

---

## Procedure to clear ALARM_CODE_1240
**Alarm Name:** Multicast PIM Neighbor Resource Exhaustion
**Severity:** Minor

This alarm indicates a resource exhaustion condition on the multicast pim neighbor subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1240 for 'Multicast PIM Neighbor Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show pim join
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show pim join`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols pim interface ge-0/0/0 mode sparse
commit
   ```
5. **Post-Recovery Validation:** Verify the multicast pim neighbor has returned to a stable operational state:
   ```
   show pim neighbors | match ge-
   ```

---

## Procedure to clear ALARM_CODE_1241
**Alarm Name:** MPLS LDP Session Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the mpls ldp session subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1241 for 'MPLS LDP Session Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ldp session
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ldp neighbor`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ldp session {ip}
   ```
5. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show ldp session | match Operational
   ```

---

## Procedure to clear ALARM_CODE_1242
**Alarm Name:** IPSec VPN Tunnel Timeout
**Severity:** Minor

This alarm indicates a timeout condition on the ipsec vpn tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1242 for 'IPSec VPN Tunnel Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show security ipsec sa
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show security ipsec statistics` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear security ike sa
   ```
6. **Post-Recovery Validation:** Verify the ipsec vpn tunnel has returned to a stable operational state:
   ```
   show security ipsec sa | match "Total active"
   ```

---

## Procedure to clear ALARM_CODE_1243
**Alarm Name:** MPLS LDP Session Threshold Exceeded
**Severity:** Warning

This alarm indicates a threshold exceeded condition on the mpls ldp session subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1243 for 'MPLS LDP Session Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ldp session
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show mpls interface`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ldp interface ge-0/0/0
commit
   ```
5. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show ldp session | match Operational
   ```

---

## Procedure to clear ALARM_CODE_1244
**Alarm Name:** Optical Rx Power Authentication Failed
**Severity:** Critical

This alarm indicates a authentication failed condition on the optical rx power subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1244 for 'Optical Rx Power Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis hardware
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show chassis hardware` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   request interface diagnostics optics ge-0/0/1
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   show interfaces diagnostics optics ge-0/0/1 | match "Rx power"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1244 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1245
**Alarm Name:** LACP Bundle Memory Leak Detected
**Severity:** Major

This alarm indicates a memory leak detected condition on the lacp bundle subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1245 for 'LACP Bundle Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interfaces ae0
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show lacp statistics`.
4. **⚠️ WARNING: Service Impact Possible.** If the lacp bundle utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set interfaces ae0
  aggregated-ether-options lacp active
commit
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show interfaces ae0 | match "Physical link is Up"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1245 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1246
**Alarm Name:** FIB (Forwarding Table) Out of Sync
**Severity:** Major

This alarm indicates a out of sync condition on the fib (forwarding table) subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1246 for 'FIB (Forwarding Table) Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route summary
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show krt queue` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear route forwarding-table
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show krt queue | match "0 queued"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1246 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1247
**Alarm Name:** ACL Processing Authentication Failed
**Severity:** Major

This alarm indicates a authentication failed condition on the acl processing subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1247 for 'ACL Processing Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show firewall log
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show firewall counter` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set firewall filter PROTECT_RE term ALLOW_BGP then count
commit
   ```
6. **Post-Recovery Validation:** Verify the acl processing has returned to a stable operational state:
   ```
   show firewall counter | match ALLOW_BGP
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1247 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1248
**Alarm Name:** BGP Peer Capacity Limit Reached
**Severity:** Minor

This alarm indicates a capacity limit reached condition on the bgp peer subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1248 for 'BGP Peer Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp neighbor {ip}
   ```
3. **Hardware Status Check:** Run `show bgp neighbor {ip}` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected bgp peer unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bgp neighbor {ip}
   ```
7. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | match Estab
   ```

---

## Procedure to clear ALARM_CODE_1249
**Alarm Name:** IPSec VPN Tunnel Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the ipsec vpn tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1249 for 'IPSec VPN Tunnel Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show security ike sa
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show security ipsec sa` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear security ipsec sa
   ```
6. **Post-Recovery Validation:** Verify the ipsec vpn tunnel has returned to a stable operational state:
   ```
   show security ipsec sa | match "Total active"
   ```

---

## Procedure to clear ALARM_CODE_1250
**Alarm Name:** GRE Tunnel Memory Leak Detected
**Severity:** Major

This alarm indicates a memory leak detected condition on the gre tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1250 for 'GRE Tunnel Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route table inet.0 protocol static
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show interfaces gr-0/0/0`.
4. **⚠️ WARNING: Service Impact Possible.** If the gre tunnel utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear interfaces statistics gr-0/0/0
   ```
6. **Post-Recovery Validation:** Verify the gre tunnel has returned to a stable operational state:
   ```
   show interfaces gr-0/0/0 | match "Link is Up"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1250 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1251
**Alarm Name:** LACP Bundle Threshold Exceeded
**Severity:** Minor

This alarm indicates a threshold exceeded condition on the lacp bundle subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1251 for 'LACP Bundle Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lacp statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show interfaces ae0`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear lacp statistics
   ```
5. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show interfaces ae0 | match "Physical link is Up"
   ```

---

## Procedure to clear ALARM_CODE_1252
**Alarm Name:** OSPF Adjacency Authentication Failed
**Severity:** Warning

This alarm indicates a authentication failed condition on the ospf adjacency subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1252 for 'OSPF Adjacency Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf interface
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show ospf interface` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ospf neighbor all
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | match Full
   ```

---

## Procedure to clear ALARM_CODE_1253
**Alarm Name:** OSPF Adjacency Down
**Severity:** Major

This alarm indicates a down condition on the ospf adjacency subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1253 for 'OSPF Adjacency Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf neighbor
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show ospf interface` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ospf neighbor all
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | match Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1253 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1254
**Alarm Name:** GRE Tunnel Loss of Signal (LOS)
**Severity:** Critical

This alarm indicates a loss of signal (los) condition on the gre tunnel subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1254 for 'GRE Tunnel Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route table inet.0 protocol static
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show interfaces gr-0/0/0` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear interfaces statistics gr-0/0/0
   ```
6. **Post-Recovery Validation:** Verify the gre tunnel has returned to a stable operational state:
   ```
   show interfaces gr-0/0/0 | match "Link is Up"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1254 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1255
**Alarm Name:** Routing Engine CPU Resource Exhaustion
**Severity:** Minor

This alarm indicates a resource exhaustion condition on the routing engine cpu subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1255 for 'Routing Engine CPU Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system uptime
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show system uptime`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   request system software rollback
   ```
5. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show chassis routing-engine | match "Idle"
   ```

---

## Procedure to clear ALARM_CODE_1256
**Alarm Name:** IS-IS Adjacency Out of Sync
**Severity:** Critical

This alarm indicates a out of sync condition on the is-is adjacency subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1256 for 'IS-IS Adjacency Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis database
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show isis adjacency` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols isis interface ge-0/0/0 level 2
commit
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1256 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1257
**Alarm Name:** FIB (Forwarding Table) Resource Exhaustion
**Severity:** Critical

This alarm indicates a resource exhaustion condition on the fib (forwarding table) subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1257 for 'FIB (Forwarding Table) Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route summary
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show route forwarding-table`.
4. **⚠️ WARNING: Service Impact Possible.** If the fib (forwarding table) utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear route forwarding-table
   ```
6. **Post-Recovery Validation:** Verify the fib (forwarding table) has returned to a stable operational state:
   ```
   show krt queue | match "0 queued"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1257 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1258
**Alarm Name:** GRE Tunnel Out of Sync
**Severity:** Major

This alarm indicates a out of sync condition on the gre tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1258 for 'GRE Tunnel Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route table inet.0 protocol static
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show interfaces gr-0/0/0` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear interfaces statistics gr-0/0/0
   ```
6. **Post-Recovery Validation:** Verify the gre tunnel has returned to a stable operational state:
   ```
   show interfaces gr-0/0/0 | match "Link is Up"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1258 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1259
**Alarm Name:** ACL Processing Loss of Signal (LOS)
**Severity:** Critical

This alarm indicates a loss of signal (los) condition on the acl processing subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1259 for 'ACL Processing Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show firewall filter
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show firewall counter` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set firewall filter PROTECT_RE term ALLOW_BGP then count
commit
   ```
6. **Post-Recovery Validation:** Verify the acl processing has returned to a stable operational state:
   ```
   show firewall counter | match ALLOW_BGP
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1259 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1260
**Alarm Name:** ARP Cache Timeout
**Severity:** Warning

This alarm indicates a timeout condition on the arp cache subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1260 for 'ARP Cache Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show arp statistics
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show arp` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp interface ge-0/0/0
   ```
6. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   show arp | match "Total entries"
   ```

---

## Procedure to clear ALARM_CODE_1261
**Alarm Name:** GRE Tunnel Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the gre tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1261 for 'GRE Tunnel Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route table inet.0 protocol static
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show interfaces gr-0/0/0` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set interfaces gr-0/0/0 unit 0 tunnel source {src} destination {dst}
commit
   ```
6. **Post-Recovery Validation:** Verify the gre tunnel has returned to a stable operational state:
   ```
   show interfaces gr-0/0/0 | match "Link is Up"
   ```

---

## Procedure to clear ALARM_CODE_1262
**Alarm Name:** LACP Bundle Down
**Severity:** Warning

This alarm indicates a down condition on the lacp bundle subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1262 for 'LACP Bundle Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lacp statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show interfaces ae0` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear lacp statistics
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show interfaces ae0 | match "Physical link is Up"
   ```

---

## Procedure to clear ALARM_CODE_1263
**Alarm Name:** ACL Processing Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the acl processing subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1263 for 'ACL Processing Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show firewall counter
   ```
3. **Hardware Status Check:** Run `show firewall counter` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected acl processing unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear firewall filter PROTECT_RE counter
   ```
7. **Post-Recovery Validation:** Verify the acl processing has returned to a stable operational state:
   ```
   show firewall counter | match ALLOW_BGP
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1263 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1264
**Alarm Name:** BFD Session Flapping
**Severity:** Minor

This alarm indicates a flapping condition on the bfd session subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1264 for 'BFD Session Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session summary
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show bfd session` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ospf area 0 interface ge-0/0/0 bfd-liveness-detection minimum-interval 300
commit
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | match Up
   ```

---

## Procedure to clear ALARM_CODE_1265
**Alarm Name:** Routing Engine CPU Capacity Limit Reached
**Severity:** Minor

This alarm indicates a capacity limit reached condition on the routing engine cpu subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1265 for 'Routing Engine CPU Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system uptime
   ```
3. **Hardware Status Check:** Run `show system uptime` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected routing engine cpu unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   request system software rollback
   ```
7. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show chassis routing-engine | match "Idle"
   ```

---

## Procedure to clear ALARM_CODE_1266
**Alarm Name:** LACP Bundle High CRC Rate
**Severity:** Warning

This alarm indicates a high crc rate condition on the lacp bundle subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1266 for 'LACP Bundle High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interfaces ae0
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show lacp interfaces`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   set interfaces ae0
  aggregated-ether-options lacp active
commit
   ```
5. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show interfaces ae0 | match "Physical link is Up"
   ```

---

## Procedure to clear ALARM_CODE_1267
**Alarm Name:** MPLS LDP Session Flapping
**Severity:** Critical

This alarm indicates a flapping condition on the mpls ldp session subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1267 for 'MPLS LDP Session Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ldp neighbor
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show ldp neighbor` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ldp session {ip}
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show ldp session | match Operational
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1267 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1268
**Alarm Name:** OSPF Adjacency Flapping
**Severity:** Minor

This alarm indicates a flapping condition on the ospf adjacency subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1268 for 'OSPF Adjacency Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf neighbor
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show ospf database` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ospf area 0.0.0.0 interface ge-0/0/0
commit
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | match Full
   ```

---

## Procedure to clear ALARM_CODE_1269
**Alarm Name:** BFD Session Out of Sync
**Severity:** Critical

This alarm indicates a out of sync condition on the bfd session subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1269 for 'BFD Session Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session summary
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show bfd session detail` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ospf area 0 interface ge-0/0/0 bfd-liveness-detection minimum-interval 300
commit
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1269 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1270
**Alarm Name:** BFD Session Stuck in INIT State
**Severity:** Major

This alarm indicates a stuck in init state condition on the bfd session subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1270 for 'BFD Session Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session summary
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show bfd session summary` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ospf area 0 interface ge-0/0/0 bfd-liveness-detection minimum-interval 300
commit
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1270 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1271
**Alarm Name:** GRE Tunnel High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the gre tunnel subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1271 for 'GRE Tunnel High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route table inet.0 protocol static
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show route table inet.0 protocol static`.
4. **⚠️ WARNING: Service Impact Possible.** If the gre tunnel utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear interfaces statistics gr-0/0/0
   ```
6. **Post-Recovery Validation:** Verify the gre tunnel has returned to a stable operational state:
   ```
   show interfaces gr-0/0/0 | match "Link is Up"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1271 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1272
**Alarm Name:** BGP Peer Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the bgp peer subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1272 for 'BGP Peer Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp summary
   ```
3. **Hardware Status Check:** Run `show bgp neighbor {ip}` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected bgp peer unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols bgp group EXTERNAL neighbor {ip}
commit
   ```
7. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | match Estab
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1272 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1273
**Alarm Name:** OSPF Adjacency Loss of Signal (LOS)
**Severity:** Critical

This alarm indicates a loss of signal (los) condition on the ospf adjacency subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1273 for 'OSPF Adjacency Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf database
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show ospf interface` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ospf area 0.0.0.0 interface ge-0/0/0
commit
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | match Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1273 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1274
**Alarm Name:** BGP Peer Unreachable
**Severity:** Minor

This alarm indicates a unreachable condition on the bgp peer subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1274 for 'BGP Peer Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bgp neighbor {ip}
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show bgp neighbor {ip}` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols bgp group EXTERNAL neighbor {ip}
commit
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | match Estab
   ```

---

## Procedure to clear ALARM_CODE_1275
**Alarm Name:** GRE Tunnel Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the gre tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1275 for 'GRE Tunnel Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interfaces gr-0/0/0
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show route table inet.0 protocol static` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set interfaces gr-0/0/0 unit 0 tunnel source {src} destination {dst}
commit
   ```
6. **Post-Recovery Validation:** Verify the gre tunnel has returned to a stable operational state:
   ```
   show interfaces gr-0/0/0 | match "Link is Up"
   ```

---

## Procedure to clear ALARM_CODE_1276
**Alarm Name:** ARP Cache Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the arp cache subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1276 for 'ARP Cache Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interfaces ge-0/0/0
   ```
3. **Hardware Status Check:** Run `show arp` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected arp cache unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp interface ge-0/0/0
   ```
7. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   show arp | match "Total entries"
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1276 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1277
**Alarm Name:** BFD Session High CRC Rate
**Severity:** Major

This alarm indicates a high crc rate condition on the bfd session subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1277 for 'BFD Session High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bfd session`.
4. **⚠️ WARNING: Service Impact Possible.** If the bfd session utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear bfd session address {ip}
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1277 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1278
**Alarm Name:** IPSec VPN Tunnel Configuration Mismatch
**Severity:** Warning

This alarm indicates a configuration mismatch condition on the ipsec vpn tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1278 for 'IPSec VPN Tunnel Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show security ike sa
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show security ipsec statistics` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear security ipsec sa
   ```
6. **Post-Recovery Validation:** Verify the ipsec vpn tunnel has returned to a stable operational state:
   ```
   show security ipsec sa | match "Total active"
   ```

---

## Procedure to clear ALARM_CODE_1279
**Alarm Name:** IPSec VPN Tunnel High CRC Rate
**Severity:** Minor

This alarm indicates a high crc rate condition on the ipsec vpn tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1279 for 'IPSec VPN Tunnel High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show security ipsec statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show security ike sa`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear security ipsec sa
   ```
5. **Post-Recovery Validation:** Verify the ipsec vpn tunnel has returned to a stable operational state:
   ```
   show security ipsec sa | match "Total active"
   ```

---

## Procedure to clear ALARM_CODE_1280
**Alarm Name:** Multicast PIM Neighbor Hardware Failure
**Severity:** Minor

This alarm indicates a hardware failure condition on the multicast pim neighbor subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1280 for 'Multicast PIM Neighbor Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show multicast route
   ```
3. **Hardware Status Check:** Run `show pim neighbors` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected multicast pim neighbor unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear pim join all
   ```
7. **Post-Recovery Validation:** Verify the multicast pim neighbor has returned to a stable operational state:
   ```
   show pim neighbors | match ge-
   ```

---

## Procedure to clear ALARM_CODE_1281
**Alarm Name:** Routing Engine CPU Memory Leak Detected
**Severity:** Major

This alarm indicates a memory leak detected condition on the routing engine cpu subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1281 for 'Routing Engine CPU Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show system processes extensive
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show system uptime`.
4. **⚠️ WARNING: Service Impact Possible.** If the routing engine cpu utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   request system software rollback
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show chassis routing-engine | match "Idle"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1281 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1282
**Alarm Name:** Routing Engine CPU Down
**Severity:** Major

This alarm indicates a down condition on the routing engine cpu subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1282 for 'Routing Engine CPU Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show chassis routing-engine
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show system uptime` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   request system software rollback
   ```
6. **Post-Recovery Validation:** Verify the routing engine cpu has returned to a stable operational state:
   ```
   show chassis routing-engine | match "Idle"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1282 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1283
**Alarm Name:** Multicast PIM Neighbor Flapping
**Severity:** Critical

This alarm indicates a flapping condition on the multicast pim neighbor subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1283 for 'Multicast PIM Neighbor Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show multicast route
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show pim neighbors` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear pim join all
   ```
6. **Post-Recovery Validation:** Verify the multicast pim neighbor has returned to a stable operational state:
   ```
   show pim neighbors | match ge-
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1283 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1284
**Alarm Name:** Multicast PIM Neighbor High CRC Rate
**Severity:** Minor

This alarm indicates a high crc rate condition on the multicast pim neighbor subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1284 for 'Multicast PIM Neighbor High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show pim neighbors
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show multicast route`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols pim interface ge-0/0/0 mode sparse
commit
   ```
5. **Post-Recovery Validation:** Verify the multicast pim neighbor has returned to a stable operational state:
   ```
   show pim neighbors | match ge-
   ```

---

## Procedure to clear ALARM_CODE_1285
**Alarm Name:** IPSec VPN Tunnel Performance Degraded
**Severity:** Warning

This alarm indicates a performance degraded condition on the ipsec vpn tunnel subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1285 for 'IPSec VPN Tunnel Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show security ike sa
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show security ipsec statistics`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear security ipsec sa
   ```
5. **Post-Recovery Validation:** Verify the ipsec vpn tunnel has returned to a stable operational state:
   ```
   show security ipsec sa | match "Total active"
   ```

---

## Procedure to clear ALARM_CODE_1286
**Alarm Name:** BGP Peer High CRC Rate
**Severity:** Warning

This alarm indicates a high crc rate condition on the bgp peer subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1286 for 'BGP Peer High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show route protocol bgp
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show bgp neighbor {ip}`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols bgp group EXTERNAL neighbor {ip}
commit
   ```
5. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   show bgp summary | match Estab
   ```

---

## Procedure to clear ALARM_CODE_1287
**Alarm Name:** LACP Bundle Loss of Signal (LOS)
**Severity:** Major

This alarm indicates a loss of signal (los) condition on the lacp bundle subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1287 for 'LACP Bundle Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show interfaces ae0
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show lacp statistics` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear lacp statistics
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show interfaces ae0 | match "Physical link is Up"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1287 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1288
**Alarm Name:** OSPF Adjacency Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the ospf adjacency subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1288 for 'OSPF Adjacency Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf neighbor
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ospf database`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ospf area 0.0.0.0 interface ge-0/0/0
commit
   ```
5. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | match Full
   ```

---

## Procedure to clear ALARM_CODE_1289
**Alarm Name:** ARP Cache Down
**Severity:** Warning

This alarm indicates a down condition on the arp cache subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1289 for 'ARP Cache Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show arp
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show arp` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp hostname {host}
   ```
6. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   show arp | match "Total entries"
   ```

---

## Procedure to clear ALARM_CODE_1290
**Alarm Name:** Multicast PIM Neighbor Configuration Mismatch
**Severity:** Minor

This alarm indicates a configuration mismatch condition on the multicast pim neighbor subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1290 for 'Multicast PIM Neighbor Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show multicast route
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show multicast route` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear pim join all
   ```
6. **Post-Recovery Validation:** Verify the multicast pim neighbor has returned to a stable operational state:
   ```
   show pim neighbors | match ge-
   ```

---

## Procedure to clear ALARM_CODE_1291
**Alarm Name:** OSPF Adjacency Performance Degraded
**Severity:** Critical

This alarm indicates a performance degraded condition on the ospf adjacency subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1291 for 'OSPF Adjacency Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ospf neighbor
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show ospf interface`.
4. **⚠️ WARNING: Service Impact Possible.** If the ospf adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear ospf neighbor all
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   show ospf neighbor | match Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1291 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1292
**Alarm Name:** LACP Bundle Unreachable
**Severity:** Major

This alarm indicates a unreachable condition on the lacp bundle subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1292 for 'LACP Bundle Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show lacp interfaces
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show lacp statistics` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set interfaces ae0
  aggregated-ether-options lacp active
commit
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   show interfaces ae0 | match "Physical link is Up"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1292 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1293
**Alarm Name:** IS-IS Adjacency Unreachable
**Severity:** Major

This alarm indicates a unreachable condition on the is-is adjacency subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1293 for 'IS-IS Adjacency Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show isis interface
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show isis adjacency` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear isis adjacency
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   show isis adjacency | match Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1293 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1294
**Alarm Name:** ACL Processing Configuration Mismatch
**Severity:** Warning

This alarm indicates a configuration mismatch condition on the acl processing subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1294 for 'ACL Processing Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show firewall counter
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `show firewall log` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear firewall filter PROTECT_RE counter
   ```
6. **Post-Recovery Validation:** Verify the acl processing has returned to a stable operational state:
   ```
   show firewall counter | match ALLOW_BGP
   ```

---

## Procedure to clear ALARM_CODE_1295
**Alarm Name:** ACL Processing Performance Degraded
**Severity:** Warning

This alarm indicates a performance degraded condition on the acl processing subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1295 for 'ACL Processing Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show firewall filter
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `show firewall counter`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear firewall filter PROTECT_RE counter
   ```
5. **Post-Recovery Validation:** Verify the acl processing has returned to a stable operational state:
   ```
   show firewall counter | match ALLOW_BGP
   ```

---

## Procedure to clear ALARM_CODE_1296
**Alarm Name:** BFD Session Down
**Severity:** Minor

This alarm indicates a down condition on the bfd session subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1296 for 'BFD Session Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show bfd session detail` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ospf area 0 interface ge-0/0/0 bfd-liveness-detection minimum-interval 300
commit
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | match Up
   ```

---

## Procedure to clear ALARM_CODE_1297
**Alarm Name:** BFD Session Unreachable
**Severity:** Minor

This alarm indicates a unreachable condition on the bfd session subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1297 for 'BFD Session Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show bfd session detail
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show bfd session detail` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ospf area 0 interface ge-0/0/0 bfd-liveness-detection minimum-interval 300
commit
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   show bfd session | match Up
   ```

---

## Procedure to clear ALARM_CODE_1298
**Alarm Name:** MPLS LDP Session Out of Sync
**Severity:** Major

This alarm indicates a out of sync condition on the mpls ldp session subsystem of Juniper equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1298 for 'MPLS LDP Session Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show ldp session
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `show ldp session` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   set protocols ldp interface ge-0/0/0
commit
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   show ldp session | match Operational
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1298 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1299
**Alarm Name:** ARP Cache Unreachable
**Severity:** Critical

This alarm indicates a unreachable condition on the arp cache subsystem of Juniper equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Juniper NMS dashboard and confirm alarm code 1299 for 'ARP Cache Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   show arp statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `show interfaces ge-0/0/0` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   clear arp interface ge-0/0/0
   ```
6. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   show arp | match "Total entries"
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Juniper TAC (Technical Assistance Center) with the alarm code 1299 and diagnostic outputs collected above.

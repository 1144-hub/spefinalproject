# Huawei VRP Service Restoration MOP (Method of Procedure)

**Equipment Vendor:** Huawei
**Document Type:** Standard Operating Procedure (SOP)
**Scope:** VRP (Versatile Routing Platform) — NE40E / NE8000 Series Troubleshooting
**Network Topology Context:** Core Router

## Overview
This document provides the standard operating procedures for resolving common alarms on Huawei NE40E and NE8000 series CORE routers running VRP (Versatile Routing Platform). Since they act as Core, any interface restart cascades failures. All CLI commands are executed in User View or System View as indicated. Configuration changes must be saved with `save` after committing.

---

## Procedure to clear ALARM_CODE_801
**Alarm Name:** MPLS LDP Session Failure
**Severity:** Critical

This alarm indicates that an MPLS Label Distribution Protocol (LDP) session between two Huawei routers has gone down. LDP sessions are used to distribute labels for MPLS forwarding. Loss of an LDP session will cause MPLS LSP (Label Switched Path) failure, breaking L3VPN, VPLS, and traffic-engineered services that depend on this label path.

1. **Confirm LDP Session Status:** Run `display mpls ldp session all` and identify the session to the affected peer. Note the session state (should show "Non-existent" or "Initialized" instead of "Operational"), the local and remote LDP IDs, and the transport address.
2. **Check TCP Connectivity:** LDP runs over TCP port 646. Run `ping -a <local-transport-ip> <remote-transport-ip>` to verify IP reachability to the peer's LDP transport address (usually the Loopback0 IP).
3. **Verify IGP Route to Peer:** Run `display ip routing-table <remote-transport-ip>` to confirm the route to the peer's transport address exists. If the route is missing, the underlying IGP (OSPF/IS-IS) may have an issue — refer to the appropriate IGP SOP.
4. **Check LDP Configuration:** Run `display current-configuration | section mpls ldp` and verify:
   - LDP is enabled globally (`mpls ldp`).
   - The correct transport address is configured (`transport-address <loopback-ip>`).
   - The interface facing the peer has LDP enabled (`interface <name>` → `mpls ldp`).
5. **Check for TCP Blockage:** Run `display acl all` and inspect any ACLs applied on the interface or in the control plane. Ensure TCP port 646 is not being blocked. Also check `display cpu-defend statistics all` for LDP packet drops.
6. **Restart LDP Process (if configuration is correct):** If the configuration matches on both ends and IP reachability is confirmed, restart the LDP process:
   ```
   system-view
   mpls ldp
   reset mpls ldp session <remote-transport-ip>
   quit
   ```
7. **Final Verification:** Run `display mpls ldp session <remote-transport-ip>` and confirm the session state transitions to "Operational". Then verify MPLS forwarding with `display mpls lsp | include <remote-transport-ip>` to confirm LSPs are re-established.
8. **Verify Service Restoration:** For each L3VPN affected, run `display ip routing-table vpn-instance <VPN_NAME>` to confirm VPN routes are re-learned via the MPLS backbone. Test end-to-end with a VPN-aware ping: `ping -vpn-instance <VPN_NAME> <remote-ce-ip>`.

---

## Procedure to clear ALARM_CODE_802
**Alarm Name:** Power Supply Unit Degradation
**Severity:** Warning

This alarm triggers when one of the redundant Power Supply Units (PSUs) in a Huawei NE40E/NE8000 chassis reports abnormal voltage, temperature, or fan speed readings. While the router continues to operate on the remaining healthy PSU(s), the loss of redundancy means a second PSU failure would cause a full chassis power-down.

1. **Identify Affected PSU:** Run `display power` to list all PSU slots and their current status. Identify which PSU shows "Abnormal" or "Absent". Note the slot number (e.g., PWR1, PWR2).
2. **Check PSU Details:** Run `display power slot <slot-number>` to see detailed readings: input voltage, output voltage, current draw, temperature, and fan RPM. Compare against the PSU specification:
   - Normal input voltage: 176V–264V AC (for AC PSU) or 40V–72V DC (for DC PSU).
   - Normal temperature: below 65°C.
   - Fan speed: above 3000 RPM.
3. **Check Environmental Conditions:** Run `display environment` to check the chassis inlet air temperature. If the ambient temperature exceeds 40°C, the issue may be environmental (data center cooling failure). Contact the facilities team.
4. **Reseat the PSU (if Abnormal):** If the PSU shows abnormal readings but is physically present, coordinate with the on-site technician to:
   - Power off the affected PSU using the physical toggle switch.
   - Wait 30 seconds for capacitors to discharge.
   - Remove the PSU from the chassis slot.
   - Re-insert the PSU firmly until the retention clip locks.
   - Power the PSU back on.
5. **Verify After Reseat:** Run `display power` and confirm the reseated PSU now shows "Normal" status.
6. **Replace if Reseat Fails:** If the PSU continues to show abnormal after reseating, it is faulty and must be replaced:
   - Order the replacement PSU part number from Huawei spare parts (refer to `display device manufacture-info` for the exact PSU model).
   - The PSU is hot-swappable — no maintenance window required as long as at least one healthy PSU remains.
   - Install the new PSU and run `display power` to confirm "Normal" status.
7. **Confirm Redundancy Restored:** Run `display power` and verify all PSU slots show "Normal". The ALARM_CODE_802 should auto-clear within 60 seconds of redundancy restoration.
8. **Document for CMDB:** Log the faulty PSU serial number (via `display device manufacture-info`) and the replacement serial number in the Configuration Management Database for asset tracking.


---

## Procedure to clear ALARM_CODE_1400
**Alarm Name:** NTP Synchronization Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1400 representing 'NTP Synchronization Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1401
**Alarm Name:** Optical Rx Power Hardware Failure
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1401 representing 'Optical Rx Power Hardware Failure' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1402
**Alarm Name:** NTP Synchronization Threshold Exceeded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1402 representing 'NTP Synchronization Threshold Exceeded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1403
**Alarm Name:** STP Root Topology Down
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1403 representing 'STP Root Topology Down' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1404
**Alarm Name:** DHCP Relay Agent Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1404 representing 'DHCP Relay Agent Stuck in INIT State' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1405
**Alarm Name:** NTP Synchronization Stuck in INIT State
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1405 representing 'NTP Synchronization Stuck in INIT State' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1406
**Alarm Name:** Switch Fabric Module Configuration Mismatch
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1406 representing 'Switch Fabric Module Configuration Mismatch' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1407
**Alarm Name:** Power Supply Unit (PSU) Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1407 representing 'Power Supply Unit (PSU) Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1408
**Alarm Name:** SNMP Agent Out of Sync
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1408 representing 'SNMP Agent Out of Sync' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1409
**Alarm Name:** IGMP Snooping Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1409 representing 'IGMP Snooping Threshold Exceeded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1410
**Alarm Name:** VRRP Group Stuck in INIT State
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1410 representing 'VRRP Group Stuck in INIT State' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1411
**Alarm Name:** BGP Peer Out of Sync
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1411 representing 'BGP Peer Out of Sync' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1412
**Alarm Name:** ARP Cache Configuration Mismatch
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1412 representing 'ARP Cache Configuration Mismatch' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1413
**Alarm Name:** BGP Route Reflector Flapping
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1413 representing 'BGP Route Reflector Flapping' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1414
**Alarm Name:** BGP Peer Down
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1414 representing 'BGP Peer Down' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1415
**Alarm Name:** BGP Peer Memory Leak Detected
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1415 representing 'BGP Peer Memory Leak Detected' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1416
**Alarm Name:** Fan Tray Assembly Performance Degraded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1416 representing 'Fan Tray Assembly Performance Degraded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1417
**Alarm Name:** Optical Tx Power Unreachable
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1417 representing 'Optical Tx Power Unreachable' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1418
**Alarm Name:** BFD Session Hardware Failure
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1418 representing 'BFD Session Hardware Failure' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1419
**Alarm Name:** EVPN MAC Route Flapping
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1419 representing 'EVPN MAC Route Flapping' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1420
**Alarm Name:** BFD Session Configuration Mismatch
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1420 representing 'BFD Session Configuration Mismatch' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1421
**Alarm Name:** RSVP-TE Tunnel Out of Sync
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1421 representing 'RSVP-TE Tunnel Out of Sync' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1422
**Alarm Name:** DHCP Relay Agent Timeout
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1422 representing 'DHCP Relay Agent Timeout' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1423
**Alarm Name:** IPSec VPN Tunnel Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1423 representing 'IPSec VPN Tunnel Threshold Exceeded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1424
**Alarm Name:** BGP Route Reflector Resource Exhaustion
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1424 representing 'BGP Route Reflector Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1425
**Alarm Name:** STP Root Topology Timeout
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1425 representing 'STP Root Topology Timeout' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1426
**Alarm Name:** ACL Processing Capacity Limit Reached
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1426 representing 'ACL Processing Capacity Limit Reached' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1427
**Alarm Name:** FIB (Forwarding Table) Capacity Limit Reached
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1427 representing 'FIB (Forwarding Table) Capacity Limit Reached' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1428
**Alarm Name:** Switch Fabric Module Capacity Limit Reached
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1428 representing 'Switch Fabric Module Capacity Limit Reached' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1429
**Alarm Name:** FIB (Forwarding Table) Out of Sync
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1429 representing 'FIB (Forwarding Table) Out of Sync' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1430
**Alarm Name:** OAM Connectivity Configuration Mismatch
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1430 representing 'OAM Connectivity Configuration Mismatch' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1431
**Alarm Name:** EVPN MAC Route Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1431 representing 'EVPN MAC Route Threshold Exceeded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1432
**Alarm Name:** Optical Rx Power Authentication Failed
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1432 representing 'Optical Rx Power Authentication Failed' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1433
**Alarm Name:** GRE Tunnel Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1433 representing 'GRE Tunnel Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1434
**Alarm Name:** Line Card NPU Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1434 representing 'Line Card NPU Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1435
**Alarm Name:** GRE Tunnel Loss of Signal (LOS)
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1435 representing 'GRE Tunnel Loss of Signal (LOS)' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1436
**Alarm Name:** HSRP Instance Out of Sync
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1436 representing 'HSRP Instance Out of Sync' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1437
**Alarm Name:** NTP Synchronization Authentication Failed
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1437 representing 'NTP Synchronization Authentication Failed' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1438
**Alarm Name:** Fan Tray Assembly Authentication Failed
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1438 representing 'Fan Tray Assembly Authentication Failed' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1439
**Alarm Name:** Optical Tx Power Threshold Exceeded
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1439 representing 'Optical Tx Power Threshold Exceeded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1440
**Alarm Name:** Management Ethernet High Cyclic Redundancy (CRC) Rate
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1440 representing 'Management Ethernet High Cyclic Redundancy (CRC) Rate' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1441
**Alarm Name:** IGMP Snooping Capacity Limit Reached
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1441 representing 'IGMP Snooping Capacity Limit Reached' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1442
**Alarm Name:** ARP Cache Out of Sync
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1442 representing 'ARP Cache Out of Sync' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1443
**Alarm Name:** OAM Connectivity Flapping
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1443 representing 'OAM Connectivity Flapping' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1444
**Alarm Name:** STP Root Topology Capacity Limit Reached
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1444 representing 'STP Root Topology Capacity Limit Reached' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1445
**Alarm Name:** ARP Cache Loss of Signal (LOS)
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1445 representing 'ARP Cache Loss of Signal (LOS)' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1446
**Alarm Name:** VPLS Pseudowire Resource Exhaustion
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1446 representing 'VPLS Pseudowire Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1447
**Alarm Name:** QoS Scheduler Out of Sync
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1447 representing 'QoS Scheduler Out of Sync' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1448
**Alarm Name:** VPLS Pseudowire Out of Sync
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1448 representing 'VPLS Pseudowire Out of Sync' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1449
**Alarm Name:** BGP Peer Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1449 representing 'BGP Peer Threshold Exceeded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1450
**Alarm Name:** SNMP Agent Loss of Signal (LOS)
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1450 representing 'SNMP Agent Loss of Signal (LOS)' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1451
**Alarm Name:** GRE Tunnel Hardware Failure
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1451 representing 'GRE Tunnel Hardware Failure' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1452
**Alarm Name:** Optical Rx Power Configuration Mismatch
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1452 representing 'Optical Rx Power Configuration Mismatch' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1453
**Alarm Name:** BFD Session Resource Exhaustion
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1453 representing 'BFD Session Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1454
**Alarm Name:** Radius/TACACS Auth Configuration Mismatch
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1454 representing 'Radius/TACACS Auth Configuration Mismatch' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1455
**Alarm Name:** DHCP Relay Agent Loss of Signal (LOS)
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1455 representing 'DHCP Relay Agent Loss of Signal (LOS)' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1456
**Alarm Name:** ACL Processing Memory Leak Detected
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1456 representing 'ACL Processing Memory Leak Detected' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1457
**Alarm Name:** FIB (Forwarding Table) Hardware Failure
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1457 representing 'FIB (Forwarding Table) Hardware Failure' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1458
**Alarm Name:** LACP Bundle Performance Degraded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1458 representing 'LACP Bundle Performance Degraded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1459
**Alarm Name:** BFD Session Loss of Signal (LOS)
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1459 representing 'BFD Session Loss of Signal (LOS)' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1460
**Alarm Name:** DHCP Relay Agent Hardware Failure
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1460 representing 'DHCP Relay Agent Hardware Failure' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1461
**Alarm Name:** Optical Tx Power Loss of Signal (LOS)
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1461 representing 'Optical Tx Power Loss of Signal (LOS)' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1462
**Alarm Name:** Power Supply Unit (PSU) Capacity Limit Reached
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1462 representing 'Power Supply Unit (PSU) Capacity Limit Reached' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1463
**Alarm Name:** Fan Tray Assembly Memory Leak Detected
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1463 representing 'Fan Tray Assembly Memory Leak Detected' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1464
**Alarm Name:** Routing Engine CPU Hardware Failure
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1464 representing 'Routing Engine CPU Hardware Failure' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1465
**Alarm Name:** STP Root Topology Unreachable
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1465 representing 'STP Root Topology Unreachable' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1466
**Alarm Name:** ACL Processing Timeout
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1466 representing 'ACL Processing Timeout' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1467
**Alarm Name:** DHCP Relay Agent Resource Exhaustion
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1467 representing 'DHCP Relay Agent Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1468
**Alarm Name:** ARP Cache Stuck in INIT State
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1468 representing 'ARP Cache Stuck in INIT State' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1469
**Alarm Name:** Switch Fabric Module Hardware Failure
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1469 representing 'Switch Fabric Module Hardware Failure' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1470
**Alarm Name:** VPLS Pseudowire Performance Degraded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1470 representing 'VPLS Pseudowire Performance Degraded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1471
**Alarm Name:** ACL Processing Resource Exhaustion
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1471 representing 'ACL Processing Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1472
**Alarm Name:** MAC Address Table Unreachable
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1472 representing 'MAC Address Table Unreachable' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1473
**Alarm Name:** QoS Scheduler Down
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1473 representing 'QoS Scheduler Down' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1474
**Alarm Name:** ACL Processing Flapping
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1474 representing 'ACL Processing Flapping' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1475
**Alarm Name:** ACL Processing Threshold Exceeded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1475 representing 'ACL Processing Threshold Exceeded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1476
**Alarm Name:** RSVP-TE Tunnel Timeout
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1476 representing 'RSVP-TE Tunnel Timeout' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1477
**Alarm Name:** HSRP Instance Memory Leak Detected
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1477 representing 'HSRP Instance Memory Leak Detected' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1478
**Alarm Name:** BGP Route Reflector Loss of Signal (LOS)
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1478 representing 'BGP Route Reflector Loss of Signal (LOS)' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1479
**Alarm Name:** NTP Synchronization Timeout
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1479 representing 'NTP Synchronization Timeout' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1480
**Alarm Name:** IS-IS Adjacency Authentication Failed
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1480 representing 'IS-IS Adjacency Authentication Failed' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1481
**Alarm Name:** Optical Rx Power Out of Sync
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1481 representing 'Optical Rx Power Out of Sync' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1482
**Alarm Name:** VPLS Pseudowire Unreachable
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1482 representing 'VPLS Pseudowire Unreachable' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1483
**Alarm Name:** Optical Rx Power Threshold Exceeded
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1483 representing 'Optical Rx Power Threshold Exceeded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1484
**Alarm Name:** Radius/TACACS Auth Resource Exhaustion
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1484 representing 'Radius/TACACS Auth Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1485
**Alarm Name:** Management Ethernet Hardware Failure
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1485 representing 'Management Ethernet Hardware Failure' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1486
**Alarm Name:** MAC Address Table High Cyclic Redundancy (CRC) Rate
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1486 representing 'MAC Address Table High Cyclic Redundancy (CRC) Rate' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1487
**Alarm Name:** FIB (Forwarding Table) Threshold Exceeded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1487 representing 'FIB (Forwarding Table) Threshold Exceeded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1488
**Alarm Name:** Radius/TACACS Auth High Cyclic Redundancy (CRC) Rate
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1488 representing 'Radius/TACACS Auth High Cyclic Redundancy (CRC) Rate' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1489
**Alarm Name:** NTP Synchronization Loss of Signal (LOS)
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1489 representing 'NTP Synchronization Loss of Signal (LOS)' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1490
**Alarm Name:** VPLS Pseudowire Threshold Exceeded
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1490 representing 'VPLS Pseudowire Threshold Exceeded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1491
**Alarm Name:** RSVP-TE Tunnel Memory Leak Detected
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1491 representing 'RSVP-TE Tunnel Memory Leak Detected' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1492
**Alarm Name:** QoS Scheduler Timeout
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1492 representing 'QoS Scheduler Timeout' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1493
**Alarm Name:** IS-IS Adjacency Performance Degraded
**Severity:** Major

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1493 representing 'IS-IS Adjacency Performance Degraded' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1494
**Alarm Name:** QoS Scheduler Flapping
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1494 representing 'QoS Scheduler Flapping' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1495
**Alarm Name:** STP Root Topology Resource Exhaustion
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1495 representing 'STP Root Topology Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1496
**Alarm Name:** MAC Address Table Configuration Mismatch
**Severity:** Warning

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1496 representing 'MAC Address Table Configuration Mismatch' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1497
**Alarm Name:** LACP Bundle Flapping
**Severity:** Critical

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1497 representing 'LACP Bundle Flapping' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1498
**Alarm Name:** NTP Synchronization High Cyclic Redundancy (CRC) Rate
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1498 representing 'NTP Synchronization High Cyclic Redundancy (CRC) Rate' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.

---

## Procedure to clear ALARM_CODE_1499
**Alarm Name:** EVPN MAC Route Resource Exhaustion
**Severity:** Minor

This alarm represents a unique fault vector. Immediate validation is required to avoid SLA breaches.

1. **Acknowledge Alarm:** Confirm the alarm code 1499 representing 'EVPN MAC Route Resource Exhaustion' on the Huawei NMS dashboard.
2. **Diagnostic Check:** Run the vendor-specific diagnostic check:
   ```
   display device
   ```
3. **Restoration Execution:** Perform the restoration sequence below to reset the affected logic:
   ```
   reset counters interface
   ```
4. **Post-Check Validation:** Verify the state has stabilized and clear the alarm administratively.


<!-- BEGIN GENERATED PROCEDURES -->

---

## Procedure to clear ALARM_CODE_1400
**Alarm Name:** RSVP-TE Tunnel Down
**Severity:** Minor

This alarm indicates a down condition on the rsvp-te tunnel subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1400 for 'RSVP-TE Tunnel Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display rsvp-te session
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display mpls te tunnel-interface` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset rsvp-te session tunnel {id}
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   display mpls te tunnel-interface | include Up
   ```

---

## Procedure to clear ALARM_CODE_1401
**Alarm Name:** Line Card NPU Out of Sync
**Severity:** Minor

This alarm indicates a out of sync condition on the line card npu subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1401 for 'Line Card NPU Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display device slot
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display device` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset slot {slot}
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   display device | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1402
**Alarm Name:** LACP Bundle Out of Sync
**Severity:** Major

This alarm indicates a out of sync condition on the lacp bundle subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1402 for 'LACP Bundle Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display lacp statistics eth-trunk {id}
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display eth-trunk {id}` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface Eth-Trunk{id}
  undo shutdown
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   display eth-trunk {id} | include active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1402 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1403
**Alarm Name:** Fan Tray Assembly Threshold Exceeded
**Severity:** Major

This alarm indicates a threshold exceeded condition on the fan tray assembly subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1403 for 'Fan Tray Assembly Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display fan
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display environment`.
4. **⚠️ WARNING: Service Impact Possible.** If the fan tray assembly utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   display environment
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   display fan | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1403 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1404
**Alarm Name:** OSPF Adjacency Configuration Mismatch
**Severity:** Minor

This alarm indicates a configuration mismatch condition on the ospf adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1404 for 'OSPF Adjacency Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display ospf interface
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `display ospf peer` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset ospf process
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   display ospf peer | include Full
   ```

---

## Procedure to clear ALARM_CODE_1405
**Alarm Name:** IS-IS Adjacency Threshold Exceeded
**Severity:** Warning

This alarm indicates a threshold exceeded condition on the is-is adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1405 for 'IS-IS Adjacency Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display isis interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display isis peer`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset isis all
   ```
5. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   display isis peer | include Up
   ```

---

## Procedure to clear ALARM_CODE_1406
**Alarm Name:** QoS Scheduler Out of Sync
**Severity:** Warning

This alarm indicates a out of sync condition on the qos scheduler subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1406 for 'QoS Scheduler Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display qos policy applied-statistics interface {intf} outbound
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display qos policy applied-statistics interface {intf} outbound` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  traffic-policy TP_CORE outbound
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   display qos policy applied-statistics interface {intf} | include pass
   ```

---

## Procedure to clear ALARM_CODE_1407
**Alarm Name:** Fan Tray Assembly Unreachable
**Severity:** Minor

This alarm indicates a unreachable condition on the fan tray assembly subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1407 for 'Fan Tray Assembly Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display fan
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display fan` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   display environment
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   display fan | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1408
**Alarm Name:** Line Card NPU Down
**Severity:** Warning

This alarm indicates a down condition on the line card npu subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1408 for 'Line Card NPU Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display device manufacture-info
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display device` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset counters interface {intf}
   ```
6. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   display device | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1409
**Alarm Name:** DHCP Relay Agent High CRC Rate
**Severity:** Minor

This alarm indicates a high crc rate condition on the dhcp relay agent subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1409 for 'DHCP Relay Agent High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display dhcp relay statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display dhcp relay all`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  dhcp enable
  interface {intf}
  dhcp relay server-ip {server_ip}
   ```
5. **Post-Recovery Validation:** Verify the dhcp relay agent has returned to a stable operational state:
   ```
   display dhcp relay statistics | include received
   ```

---

## Procedure to clear ALARM_CODE_1410
**Alarm Name:** QoS Scheduler Resource Exhaustion
**Severity:** Major

This alarm indicates a resource exhaustion condition on the qos scheduler subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1410 for 'QoS Scheduler Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display traffic-policy statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display qos policy applied-statistics interface {intf} outbound`.
4. **⚠️ WARNING: Service Impact Possible.** If the qos scheduler utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  traffic-policy TP_CORE outbound
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   display qos policy applied-statistics interface {intf} | include pass
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1410 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1411
**Alarm Name:** DHCP Relay Agent Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the dhcp relay agent subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1411 for 'DHCP Relay Agent Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display dhcp relay statistics
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display dhcp relay all` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  dhcp enable
  interface {intf}
  dhcp relay server-ip {server_ip}
   ```
6. **Post-Recovery Validation:** Verify the dhcp relay agent has returned to a stable operational state:
   ```
   display dhcp relay statistics | include received
   ```

---

## Procedure to clear ALARM_CODE_1412
**Alarm Name:** ARP Cache Performance Degraded
**Severity:** Critical

This alarm indicates a performance degraded condition on the arp cache subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1412 for 'ARP Cache Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display arp statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display arp statistics`.
4. **⚠️ WARNING: Service Impact Possible.** If the arp cache utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   arp static {ip} {mac}
   ```
6. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   display arp | include Total
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1412 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1413
**Alarm Name:** IS-IS Adjacency Performance Degraded
**Severity:** Major

This alarm indicates a performance degraded condition on the is-is adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1413 for 'IS-IS Adjacency Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display isis interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display isis interface`.
4. **⚠️ WARNING: Service Impact Possible.** If the is-is adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  isis {tag}
  network-entity 49.0001.0000.0001.00
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   display isis peer | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1413 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1414
**Alarm Name:** ARP Cache Authentication Failed
**Severity:** Minor

This alarm indicates a authentication failed condition on the arp cache subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1414 for 'ARP Cache Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display arp statistics
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `display arp` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   arp static {ip} {mac}
   ```
6. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   display arp | include Total
   ```

---

## Procedure to clear ALARM_CODE_1415
**Alarm Name:** IS-IS Adjacency Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the is-is adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1415 for 'IS-IS Adjacency Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display isis lsdb
   ```
3. **Hardware Status Check:** Run `display isis peer` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected is-is adjacency unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset isis all
   ```
7. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   display isis peer | include Up
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1415 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1416
**Alarm Name:** Power Supply Unit (PSU) Stuck in INIT State
**Severity:** Major

This alarm indicates a stuck in init state condition on the power supply unit (psu) subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1416 for 'Power Supply Unit (PSU) Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display power
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display power` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset power module {mod}
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   display environment | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1416 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1417
**Alarm Name:** Optical Rx Power Out of Sync
**Severity:** Major

This alarm indicates a out of sync condition on the optical rx power subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1417 for 'Optical Rx Power Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display interface {port} transceiver
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display transceiver {port}` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface {port}
  undo shutdown
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   display transceiver {port} | include Rx
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1417 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1418
**Alarm Name:** BFD Session Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the bfd session subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1418 for 'BFD Session Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display bfd session all
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display bfd session all`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  bfd {name}
  discriminator local {local} remote {remote}
  commit
   ```
5. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   display bfd session all | include Up
   ```

---

## Procedure to clear ALARM_CODE_1419
**Alarm Name:** Power Supply Unit (PSU) Loss of Signal (LOS)
**Severity:** Warning

This alarm indicates a loss of signal (los) condition on the power supply unit (psu) subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1419 for 'Power Supply Unit (PSU) Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display power
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display environment` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   display power | include Normal
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   display environment | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1420
**Alarm Name:** Power Supply Unit (PSU) Threshold Exceeded
**Severity:** Minor

This alarm indicates a threshold exceeded condition on the power supply unit (psu) subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1420 for 'Power Supply Unit (PSU) Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display environment
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display power`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset power module {mod}
   ```
5. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   display environment | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1421
**Alarm Name:** IS-IS Adjacency High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the is-is adjacency subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1421 for 'IS-IS Adjacency High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display isis interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display isis interface`.
4. **⚠️ WARNING: Service Impact Possible.** If the is-is adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset isis all
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   display isis peer | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1421 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1422
**Alarm Name:** ARP Cache High CRC Rate
**Severity:** Critical

This alarm indicates a high crc rate condition on the arp cache subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1422 for 'ARP Cache High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display arp
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display arp`.
4. **⚠️ WARNING: Service Impact Possible.** If the arp cache utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   arp static {ip} {mac}
   ```
6. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   display arp | include Total
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1422 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1423
**Alarm Name:** Fan Tray Assembly Stuck in INIT State
**Severity:** Minor

This alarm indicates a stuck in init state condition on the fan tray assembly subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1423 for 'Fan Tray Assembly Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display fan
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display environment` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   display environment
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   display fan | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1424
**Alarm Name:** Fan Tray Assembly Performance Degraded
**Severity:** Minor

This alarm indicates a performance degraded condition on the fan tray assembly subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1424 for 'Fan Tray Assembly Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display environment
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display fan`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset fan module {mod}
   ```
5. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   display fan | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1425
**Alarm Name:** OSPF Adjacency Unreachable
**Severity:** Major

This alarm indicates a unreachable condition on the ospf adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1425 for 'OSPF Adjacency Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display ospf peer
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display ospf lsdb` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset ospf process
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   display ospf peer | include Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1425 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1426
**Alarm Name:** QoS Scheduler Hardware Failure
**Severity:** Critical

This alarm indicates a hardware failure condition on the qos scheduler subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1426 for 'QoS Scheduler Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display traffic-policy statistics
   ```
3. **Hardware Status Check:** Run `display qos policy applied-statistics interface {intf} outbound` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected qos scheduler unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset traffic-policy statistics interface {intf} outbound
   ```
7. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   display qos policy applied-statistics interface {intf} | include pass
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1426 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1427
**Alarm Name:** MPLS LDP Session Performance Degraded
**Severity:** Warning

This alarm indicates a performance degraded condition on the mpls ldp session subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1427 for 'MPLS LDP Session Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display mpls lsp
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display mpls ldp lsp`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  mpls ldp
  interface {intf}
  mpls ldp enable
   ```
5. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   display mpls ldp session | include Operational
   ```

---

## Procedure to clear ALARM_CODE_1428
**Alarm Name:** Optical Rx Power Resource Exhaustion
**Severity:** Critical

This alarm indicates a resource exhaustion condition on the optical rx power subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1428 for 'Optical Rx Power Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display transceiver {port}
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display interface {port} transceiver`.
4. **⚠️ WARNING: Service Impact Possible.** If the optical rx power utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface {port}
  undo shutdown
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   display transceiver {port} | include Rx
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1428 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1429
**Alarm Name:** BGP Peer Authentication Failed
**Severity:** Minor

This alarm indicates a authentication failed condition on the bgp peer subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1429 for 'BGP Peer Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display bgp peer
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `display bgp routing-table` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset bgp {ip}
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   display bgp peer | include Established
   ```

---

## Procedure to clear ALARM_CODE_1430
**Alarm Name:** DHCP Relay Agent Down
**Severity:** Critical

This alarm indicates a down condition on the dhcp relay agent subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1430 for 'DHCP Relay Agent Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display dhcp relay statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display dhcp relay statistics` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset dhcp relay statistics
   ```
6. **Post-Recovery Validation:** Verify the dhcp relay agent has returned to a stable operational state:
   ```
   display dhcp relay statistics | include received
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1430 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1431
**Alarm Name:** VRRP Group Performance Degraded
**Severity:** Major

This alarm indicates a performance degraded condition on the vrrp group subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1431 for 'VRRP Group Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display vrrp statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display vrrp`.
4. **⚠️ WARNING: Service Impact Possible.** If the vrrp group utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface GigabitEthernet0/0/0
  vrrp vrid {id} virtual-ip {vip}
  vrrp vrid {id} priority 120
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   display vrrp | include Master
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1431 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1432
**Alarm Name:** Power Supply Unit (PSU) Timeout
**Severity:** Critical

This alarm indicates a timeout condition on the power supply unit (psu) subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1432 for 'Power Supply Unit (PSU) Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display power
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display power` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset power module {mod}
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   display environment | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1432 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1433
**Alarm Name:** Line Card NPU Capacity Limit Reached
**Severity:** Warning

This alarm indicates a capacity limit reached condition on the line card npu subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1433 for 'Line Card NPU Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display device manufacture-info
   ```
3. **Hardware Status Check:** Run `display device` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected line card npu unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset counters interface {intf}
   ```
7. **Post-Recovery Validation:** Verify the line card npu has returned to a stable operational state:
   ```
   display device | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1434
**Alarm Name:** QoS Scheduler High CRC Rate
**Severity:** Warning

This alarm indicates a high crc rate condition on the qos scheduler subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1434 for 'QoS Scheduler High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display traffic-policy statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display traffic-policy statistics`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  traffic-policy TP_CORE outbound
   ```
5. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   display qos policy applied-statistics interface {intf} | include pass
   ```

---

## Procedure to clear ALARM_CODE_1435
**Alarm Name:** RSVP-TE Tunnel Timeout
**Severity:** Critical

This alarm indicates a timeout condition on the rsvp-te tunnel subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1435 for 'RSVP-TE Tunnel Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display mpls te tunnel-interface
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display rsvp-te session` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface Tunnel{id}
  undo shutdown
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   display mpls te tunnel-interface | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1435 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1436
**Alarm Name:** QoS Scheduler Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the qos scheduler subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1436 for 'QoS Scheduler Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display traffic-policy statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display traffic-policy statistics` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  traffic-policy TP_CORE outbound
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   display qos policy applied-statistics interface {intf} | include pass
   ```

---

## Procedure to clear ALARM_CODE_1437
**Alarm Name:** Power Supply Unit (PSU) Memory Leak Detected
**Severity:** Critical

This alarm indicates a memory leak detected condition on the power supply unit (psu) subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1437 for 'Power Supply Unit (PSU) Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display environment
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display power`.
4. **⚠️ WARNING: Service Impact Possible.** If the power supply unit (psu) utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   display power | include Normal
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   display environment | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1437 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1438
**Alarm Name:** QoS Scheduler Performance Degraded
**Severity:** Minor

This alarm indicates a performance degraded condition on the qos scheduler subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1438 for 'QoS Scheduler Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display qos policy applied-statistics interface {intf} outbound
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display qos policy applied-statistics interface {intf} outbound`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  traffic-policy TP_CORE outbound
   ```
5. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   display qos policy applied-statistics interface {intf} | include pass
   ```

---

## Procedure to clear ALARM_CODE_1439
**Alarm Name:** Optical Rx Power Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the optical rx power subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1439 for 'Optical Rx Power Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display transceiver {port}
   ```
3. **Hardware Status Check:** Run `display transceiver {port}` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected optical rx power unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface {port}
  undo shutdown
   ```
7. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   display transceiver {port} | include Rx
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1439 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1440
**Alarm Name:** OSPF Adjacency Down
**Severity:** Warning

This alarm indicates a down condition on the ospf adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1440 for 'OSPF Adjacency Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display ospf peer
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display ospf interface` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  ospf {pid}
  area 0.0.0.0
  network {net} {mask}
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   display ospf peer | include Full
   ```

---

## Procedure to clear ALARM_CODE_1441
**Alarm Name:** MPLS LDP Session Unreachable
**Severity:** Warning

This alarm indicates a unreachable condition on the mpls ldp session subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1441 for 'MPLS LDP Session Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display mpls lsp
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display mpls lsp` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  mpls ldp
  interface {intf}
  mpls ldp enable
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   display mpls ldp session | include Operational
   ```

---

## Procedure to clear ALARM_CODE_1442
**Alarm Name:** QoS Scheduler Down
**Severity:** Warning

This alarm indicates a down condition on the qos scheduler subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1442 for 'QoS Scheduler Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display qos policy applied-statistics interface {intf} outbound
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display qos policy applied-statistics interface {intf} outbound` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset traffic-policy statistics interface {intf} outbound
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   display qos policy applied-statistics interface {intf} | include pass
   ```

---

## Procedure to clear ALARM_CODE_1443
**Alarm Name:** ARP Cache Flapping
**Severity:** Minor

This alarm indicates a flapping condition on the arp cache subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1443 for 'ARP Cache Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display arp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display arp` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   arp static {ip} {mac}
   ```
6. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   display arp | include Total
   ```

---

## Procedure to clear ALARM_CODE_1444
**Alarm Name:** DHCP Relay Agent Threshold Exceeded
**Severity:** Critical

This alarm indicates a threshold exceeded condition on the dhcp relay agent subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1444 for 'DHCP Relay Agent Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display dhcp relay statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display dhcp relay statistics`.
4. **⚠️ WARNING: Service Impact Possible.** If the dhcp relay agent utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset dhcp relay statistics
   ```
6. **Post-Recovery Validation:** Verify the dhcp relay agent has returned to a stable operational state:
   ```
   display dhcp relay statistics | include received
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1444 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1445
**Alarm Name:** LACP Bundle Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the lacp bundle subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1445 for 'LACP Bundle Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display lacp statistics eth-trunk {id}
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display lacp statistics eth-trunk {id}`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface Eth-Trunk{id}
  undo shutdown
   ```
5. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   display eth-trunk {id} | include active
   ```

---

## Procedure to clear ALARM_CODE_1446
**Alarm Name:** OSPF Adjacency Timeout
**Severity:** Critical

This alarm indicates a timeout condition on the ospf adjacency subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1446 for 'OSPF Adjacency Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display ospf lsdb
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display ospf interface` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset ospf process
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   display ospf peer | include Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1446 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1447
**Alarm Name:** QoS Scheduler Flapping
**Severity:** Critical

This alarm indicates a flapping condition on the qos scheduler subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1447 for 'QoS Scheduler Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display traffic-policy statistics
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display traffic-policy statistics` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  traffic-policy TP_CORE outbound
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   display qos policy applied-statistics interface {intf} | include pass
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1447 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1448
**Alarm Name:** LACP Bundle Resource Exhaustion
**Severity:** Major

This alarm indicates a resource exhaustion condition on the lacp bundle subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1448 for 'LACP Bundle Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display lacp statistics eth-trunk {id}
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display lacp statistics eth-trunk {id}`.
4. **⚠️ WARNING: Service Impact Possible.** If the lacp bundle utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface Eth-Trunk{id}
  undo shutdown
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   display eth-trunk {id} | include active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1448 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1449
**Alarm Name:** Fan Tray Assembly Capacity Limit Reached
**Severity:** Minor

This alarm indicates a capacity limit reached condition on the fan tray assembly subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1449 for 'Fan Tray Assembly Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display fan
   ```
3. **Hardware Status Check:** Run `display environment` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected fan tray assembly unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset fan module {mod}
   ```
7. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   display fan | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1450
**Alarm Name:** MPLS LDP Session Capacity Limit Reached
**Severity:** Minor

This alarm indicates a capacity limit reached condition on the mpls ldp session subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1450 for 'MPLS LDP Session Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display mpls ldp session
   ```
3. **Hardware Status Check:** Run `display mpls ldp lsp` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected mpls ldp session unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset mpls ldp session peer {ip}
   ```
7. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   display mpls ldp session | include Operational
   ```

---

## Procedure to clear ALARM_CODE_1451
**Alarm Name:** BGP Peer Timeout
**Severity:** Warning

This alarm indicates a timeout condition on the bgp peer subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1451 for 'BGP Peer Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display bgp peer
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display bgp peer` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset bgp {ip}
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   display bgp peer | include Established
   ```

---

## Procedure to clear ALARM_CODE_1452
**Alarm Name:** VRRP Group Authentication Failed
**Severity:** Major

This alarm indicates a authentication failed condition on the vrrp group subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1452 for 'VRRP Group Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display vrrp
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `display vrrp` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   display vrrp | include Master
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1452 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1453
**Alarm Name:** Fan Tray Assembly Memory Leak Detected
**Severity:** Major

This alarm indicates a memory leak detected condition on the fan tray assembly subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1453 for 'Fan Tray Assembly Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display environment
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display environment`.
4. **⚠️ WARNING: Service Impact Possible.** If the fan tray assembly utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset fan module {mod}
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   display fan | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1453 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1454
**Alarm Name:** VRRP Group Down
**Severity:** Critical

This alarm indicates a down condition on the vrrp group subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1454 for 'VRRP Group Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display vrrp statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display vrrp` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface GigabitEthernet0/0/0
  vrrp vrid {id} virtual-ip {vip}
  vrrp vrid {id} priority 120
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   display vrrp | include Master
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1454 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1455
**Alarm Name:** Power Supply Unit (PSU) Performance Degraded
**Severity:** Critical

This alarm indicates a performance degraded condition on the power supply unit (psu) subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1455 for 'Power Supply Unit (PSU) Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display environment
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display environment`.
4. **⚠️ WARNING: Service Impact Possible.** If the power supply unit (psu) utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   display power | include Normal
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   display environment | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1455 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1456
**Alarm Name:** DHCP Relay Agent Resource Exhaustion
**Severity:** Major

This alarm indicates a resource exhaustion condition on the dhcp relay agent subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1456 for 'DHCP Relay Agent Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display dhcp relay statistics
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display dhcp relay all`.
4. **⚠️ WARNING: Service Impact Possible.** If the dhcp relay agent utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  dhcp enable
  interface {intf}
  dhcp relay server-ip {server_ip}
   ```
6. **Post-Recovery Validation:** Verify the dhcp relay agent has returned to a stable operational state:
   ```
   display dhcp relay statistics | include received
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1456 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1457
**Alarm Name:** VRRP Group Timeout
**Severity:** Minor

This alarm indicates a timeout condition on the vrrp group subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1457 for 'VRRP Group Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display vrrp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display vrrp` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface GigabitEthernet0/0/0
  vrrp vrid {id} virtual-ip {vip}
  vrrp vrid {id} priority 120
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   display vrrp | include Master
   ```

---

## Procedure to clear ALARM_CODE_1458
**Alarm Name:** Power Supply Unit (PSU) Configuration Mismatch
**Severity:** Major

This alarm indicates a configuration mismatch condition on the power supply unit (psu) subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1458 for 'Power Supply Unit (PSU) Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display power
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `display environment` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset power module {mod}
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   display environment | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1458 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1459
**Alarm Name:** IS-IS Adjacency Memory Leak Detected
**Severity:** Major

This alarm indicates a memory leak detected condition on the is-is adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1459 for 'IS-IS Adjacency Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display isis interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display isis peer`.
4. **⚠️ WARNING: Service Impact Possible.** If the is-is adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  isis {tag}
  network-entity 49.0001.0000.0001.00
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   display isis peer | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1459 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1460
**Alarm Name:** LACP Bundle Loss of Signal (LOS)
**Severity:** Warning

This alarm indicates a loss of signal (los) condition on the lacp bundle subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1460 for 'LACP Bundle Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display lacp statistics eth-trunk {id}
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display eth-trunk {id}` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface Eth-Trunk{id}
  undo shutdown
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   display eth-trunk {id} | include active
   ```

---

## Procedure to clear ALARM_CODE_1461
**Alarm Name:** MPLS LDP Session Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the mpls ldp session subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1461 for 'MPLS LDP Session Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display mpls ldp session
   ```
3. **Hardware Status Check:** Run `display mpls lsp` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected mpls ldp session unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  mpls ldp
  interface {intf}
  mpls ldp enable
   ```
7. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   display mpls ldp session | include Operational
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1461 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1462
**Alarm Name:** BGP Peer Unreachable
**Severity:** Critical

This alarm indicates a unreachable condition on the bgp peer subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1462 for 'BGP Peer Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display bgp peer
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display bgp routing-table` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset bgp {ip}
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   display bgp peer | include Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1462 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1463
**Alarm Name:** MPLS LDP Session Down
**Severity:** Critical

This alarm indicates a down condition on the mpls ldp session subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1463 for 'MPLS LDP Session Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display mpls ldp session
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display mpls lsp` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  mpls ldp
  interface {intf}
  mpls ldp enable
   ```
6. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   display mpls ldp session | include Operational
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1463 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1464
**Alarm Name:** RSVP-TE Tunnel Flapping
**Severity:** Major

This alarm indicates a flapping condition on the rsvp-te tunnel subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1464 for 'RSVP-TE Tunnel Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display mpls te tunnel-interface
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display rsvp-te session` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface Tunnel{id}
  undo shutdown
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   display mpls te tunnel-interface | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1464 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1465
**Alarm Name:** LACP Bundle Threshold Exceeded
**Severity:** Minor

This alarm indicates a threshold exceeded condition on the lacp bundle subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1465 for 'LACP Bundle Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display eth-trunk {id}
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display lacp statistics eth-trunk {id}`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset lacp statistics eth-trunk {id}
   ```
5. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   display eth-trunk {id} | include active
   ```

---

## Procedure to clear ALARM_CODE_1466
**Alarm Name:** Optical Rx Power Threshold Exceeded
**Severity:** Warning

This alarm indicates a threshold exceeded condition on the optical rx power subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1466 for 'Optical Rx Power Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display transceiver {port}
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display interface {port} transceiver`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface {port}
  undo shutdown
   ```
5. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   display transceiver {port} | include Rx
   ```

---

## Procedure to clear ALARM_CODE_1467
**Alarm Name:** OSPF Adjacency Stuck in INIT State
**Severity:** Minor

This alarm indicates a stuck in init state condition on the ospf adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1467 for 'OSPF Adjacency Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display ospf interface
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display ospf peer` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset ospf process
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   display ospf peer | include Full
   ```

---

## Procedure to clear ALARM_CODE_1468
**Alarm Name:** OSPF Adjacency Loss of Signal (LOS)
**Severity:** Critical

This alarm indicates a loss of signal (los) condition on the ospf adjacency subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1468 for 'OSPF Adjacency Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display ospf peer
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display ospf lsdb` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset ospf process
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   display ospf peer | include Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1468 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1469
**Alarm Name:** ARP Cache Memory Leak Detected
**Severity:** Warning

This alarm indicates a memory leak detected condition on the arp cache subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1469 for 'ARP Cache Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display arp
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display arp statistics`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset arp interface {intf}
   ```
5. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   display arp | include Total
   ```

---

## Procedure to clear ALARM_CODE_1470
**Alarm Name:** QoS Scheduler Threshold Exceeded
**Severity:** Major

This alarm indicates a threshold exceeded condition on the qos scheduler subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1470 for 'QoS Scheduler Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display qos policy applied-statistics interface {intf} outbound
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display traffic-policy statistics`.
4. **⚠️ WARNING: Service Impact Possible.** If the qos scheduler utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  traffic-policy TP_CORE outbound
   ```
6. **Post-Recovery Validation:** Verify the qos scheduler has returned to a stable operational state:
   ```
   display qos policy applied-statistics interface {intf} | include pass
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1470 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1471
**Alarm Name:** Power Supply Unit (PSU) Hardware Failure
**Severity:** Major

This alarm indicates a hardware failure condition on the power supply unit (psu) subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1471 for 'Power Supply Unit (PSU) Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display power
   ```
3. **Hardware Status Check:** Run `display environment` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected power supply unit (psu) unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   display power | include Normal
   ```
7. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   display environment | include Normal
   ```
8. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1471 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1472
**Alarm Name:** Fan Tray Assembly Timeout
**Severity:** Warning

This alarm indicates a timeout condition on the fan tray assembly subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1472 for 'Fan Tray Assembly Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display environment
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display environment` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   display environment
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   display fan | include Normal
   ```

---

## Procedure to clear ALARM_CODE_1473
**Alarm Name:** Fan Tray Assembly Resource Exhaustion
**Severity:** Critical

This alarm indicates a resource exhaustion condition on the fan tray assembly subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1473 for 'Fan Tray Assembly Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display environment
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display fan`.
4. **⚠️ WARNING: Service Impact Possible.** If the fan tray assembly utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   display environment
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   display fan | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1473 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1474
**Alarm Name:** BGP Peer Performance Degraded
**Severity:** Minor

This alarm indicates a performance degraded condition on the bgp peer subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1474 for 'BGP Peer Performance Degraded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display bgp peer {ip} verbose
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display bgp peer`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  bgp {asn}
  peer {ip} enable
   ```
5. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   display bgp peer | include Established
   ```

---

## Procedure to clear ALARM_CODE_1475
**Alarm Name:** BFD Session Down
**Severity:** Minor

This alarm indicates a down condition on the bfd session subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1475 for 'BFD Session Down' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display bfd statistics
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display bfd session all` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  bfd {name}
  discriminator local {local} remote {remote}
  commit
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   display bfd session all | include Up
   ```

---

## Procedure to clear ALARM_CODE_1476
**Alarm Name:** ARP Cache Stuck in INIT State
**Severity:** Warning

This alarm indicates a stuck in init state condition on the arp cache subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1476 for 'ARP Cache Stuck in INIT State' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display arp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display arp` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset arp interface {intf}
   ```
6. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   display arp | include Total
   ```

---

## Procedure to clear ALARM_CODE_1477
**Alarm Name:** BGP Peer Threshold Exceeded
**Severity:** Warning

This alarm indicates a threshold exceeded condition on the bgp peer subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1477 for 'BGP Peer Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display bgp routing-table
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display bgp peer {ip} verbose`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  bgp {asn}
  peer {ip} enable
   ```
5. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   display bgp peer | include Established
   ```

---

## Procedure to clear ALARM_CODE_1478
**Alarm Name:** VRRP Group Memory Leak Detected
**Severity:** Minor

This alarm indicates a memory leak detected condition on the vrrp group subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1478 for 'VRRP Group Memory Leak Detected' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display vrrp
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display vrrp statistics`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface GigabitEthernet0/0/0
  vrrp vrid {id} virtual-ip {vip}
  vrrp vrid {id} priority 120
   ```
5. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   display vrrp | include Master
   ```

---

## Procedure to clear ALARM_CODE_1479
**Alarm Name:** BFD Session Configuration Mismatch
**Severity:** Critical

This alarm indicates a configuration mismatch condition on the bfd session subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1479 for 'BFD Session Configuration Mismatch' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display bfd session all
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `display bfd session all` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset bfd session discriminator {disc}
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   display bfd session all | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1479 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1480
**Alarm Name:** Fan Tray Assembly Authentication Failed
**Severity:** Critical

This alarm indicates a authentication failed condition on the fan tray assembly subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1480 for 'Fan Tray Assembly Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display fan
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `display environment` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset fan module {mod}
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   display fan | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1480 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1481
**Alarm Name:** OSPF Adjacency Flapping
**Severity:** Warning

This alarm indicates a flapping condition on the ospf adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1481 for 'OSPF Adjacency Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display ospf lsdb
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display ospf lsdb` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  ospf {pid}
  area 0.0.0.0
  network {net} {mask}
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   display ospf peer | include Full
   ```

---

## Procedure to clear ALARM_CODE_1482
**Alarm Name:** BFD Session Timeout
**Severity:** Minor

This alarm indicates a timeout condition on the bfd session subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1482 for 'BFD Session Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display bfd session all
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display bfd session all` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  bfd {name}
  discriminator local {local} remote {remote}
  commit
   ```
6. **Post-Recovery Validation:** Verify the bfd session has returned to a stable operational state:
   ```
   display bfd session all | include Up
   ```

---

## Procedure to clear ALARM_CODE_1483
**Alarm Name:** LACP Bundle Hardware Failure
**Severity:** Warning

This alarm indicates a hardware failure condition on the lacp bundle subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1483 for 'LACP Bundle Hardware Failure' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display lacp statistics eth-trunk {id}
   ```
3. **Hardware Status Check:** Run `display lacp statistics eth-trunk {id}` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected lacp bundle unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface Eth-Trunk{id}
  undo shutdown
   ```
7. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   display eth-trunk {id} | include active
   ```

---

## Procedure to clear ALARM_CODE_1484
**Alarm Name:** ARP Cache Timeout
**Severity:** Warning

This alarm indicates a timeout condition on the arp cache subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1484 for 'ARP Cache Timeout' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display arp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display arp statistics` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset arp interface {intf}
   ```
6. **Post-Recovery Validation:** Verify the arp cache has returned to a stable operational state:
   ```
   display arp | include Total
   ```

---

## Procedure to clear ALARM_CODE_1485
**Alarm Name:** MPLS LDP Session Threshold Exceeded
**Severity:** Warning

This alarm indicates a threshold exceeded condition on the mpls ldp session subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1485 for 'MPLS LDP Session Threshold Exceeded' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display mpls ldp session
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display mpls ldp session`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  mpls ldp
  interface {intf}
  mpls ldp enable
   ```
5. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   display mpls ldp session | include Operational
   ```

---

## Procedure to clear ALARM_CODE_1486
**Alarm Name:** VRRP Group Out of Sync
**Severity:** Warning

This alarm indicates a out of sync condition on the vrrp group subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1486 for 'VRRP Group Out of Sync' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display vrrp
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display vrrp statistics` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset vrrp statistics
   ```
6. **Post-Recovery Validation:** Verify the vrrp group has returned to a stable operational state:
   ```
   display vrrp | include Master
   ```

---

## Procedure to clear ALARM_CODE_1487
**Alarm Name:** BGP Peer Loss of Signal (LOS)
**Severity:** Critical

This alarm indicates a loss of signal (los) condition on the bgp peer subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1487 for 'BGP Peer Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display bgp peer {ip} verbose
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display bgp peer {ip} verbose` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset bgp {ip}
   ```
6. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   display bgp peer | include Established
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1487 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1488
**Alarm Name:** RSVP-TE Tunnel Capacity Limit Reached
**Severity:** Minor

This alarm indicates a capacity limit reached condition on the rsvp-te tunnel subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1488 for 'RSVP-TE Tunnel Capacity Limit Reached' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display rsvp-te session
   ```
3. **Hardware Status Check:** Run `display rsvp-te session` to identify the specific failed hardware module, slot, or component.
4. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy mechanisms (standby modules, ECMP paths) are active before performing hardware operations.
5. **Physical Intervention:** Dispatch a field technician to inspect and, if necessary, reseat or replace the affected rsvp-te tunnel unit. Open an RMA case.
6. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset rsvp-te session tunnel {id}
   ```
7. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   display mpls te tunnel-interface | include Up
   ```

---

## Procedure to clear ALARM_CODE_1489
**Alarm Name:** Fan Tray Assembly Loss of Signal (LOS)
**Severity:** Major

This alarm indicates a loss of signal (los) condition on the fan tray assembly subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1489 for 'Fan Tray Assembly Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display environment
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display environment` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset fan module {mod}
   ```
6. **Post-Recovery Validation:** Verify the fan tray assembly has returned to a stable operational state:
   ```
   display fan | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1489 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1490
**Alarm Name:** MPLS LDP Session High CRC Rate
**Severity:** Minor

This alarm indicates a high crc rate condition on the mpls ldp session subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1490 for 'MPLS LDP Session High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display mpls ldp session
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display mpls ldp lsp`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  mpls ldp
  interface {intf}
  mpls ldp enable
   ```
5. **Post-Recovery Validation:** Verify the mpls ldp session has returned to a stable operational state:
   ```
   display mpls ldp session | include Operational
   ```

---

## Procedure to clear ALARM_CODE_1491
**Alarm Name:** Optical Rx Power Loss of Signal (LOS)
**Severity:** Major

This alarm indicates a loss of signal (los) condition on the optical rx power subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1491 for 'Optical Rx Power Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display interface {port} transceiver
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display transceiver {port}` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   restart interface {port}
   ```
6. **Post-Recovery Validation:** Verify the optical rx power has returned to a stable operational state:
   ```
   display transceiver {port} | include Rx
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1491 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1492
**Alarm Name:** OSPF Adjacency Resource Exhaustion
**Severity:** Warning

This alarm indicates a resource exhaustion condition on the ospf adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1492 for 'OSPF Adjacency Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display ospf lsdb
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display ospf lsdb`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset ospf process
   ```
5. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   display ospf peer | include Full
   ```

---

## Procedure to clear ALARM_CODE_1493
**Alarm Name:** IS-IS Adjacency Unreachable
**Severity:** Critical

This alarm indicates a unreachable condition on the is-is adjacency subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1493 for 'IS-IS Adjacency Unreachable' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display isis peer
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display isis peer` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset isis all
   ```
6. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   display isis peer | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1493 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1494
**Alarm Name:** OSPF Adjacency High CRC Rate
**Severity:** Major

This alarm indicates a high crc rate condition on the ospf adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1494 for 'OSPF Adjacency High CRC Rate' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display ospf interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display ospf lsdb`.
4. **⚠️ WARNING: Service Impact Possible.** If the ospf adjacency utilization exceeds 90%, consider emergency traffic rerouting before proceeding.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset ospf process
   ```
6. **Post-Recovery Validation:** Verify the ospf adjacency has returned to a stable operational state:
   ```
   display ospf peer | include Full
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1494 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1495
**Alarm Name:** IS-IS Adjacency Resource Exhaustion
**Severity:** Minor

This alarm indicates a resource exhaustion condition on the is-is adjacency subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1495 for 'IS-IS Adjacency Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display isis interface
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display isis peer`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  isis {tag}
  network-entity 49.0001.0000.0001.00
   ```
5. **Post-Recovery Validation:** Verify the is-is adjacency has returned to a stable operational state:
   ```
   display isis peer | include Up
   ```

---

## Procedure to clear ALARM_CODE_1496
**Alarm Name:** LACP Bundle Authentication Failed
**Severity:** Critical

This alarm indicates a authentication failed condition on the lacp bundle subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1496 for 'LACP Bundle Authentication Failed' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display lacp statistics eth-trunk {id}
   ```
3. **Configuration Audit:** Compare the running configuration against the golden config template. Run `display eth-trunk {id}` to verify key parameters.
4. **Peer Coordination:** Contact the peer administrator to verify matching configuration parameters (keys, ASN, timers, etc.).
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   system-view
  interface Eth-Trunk{id}
  undo shutdown
   ```
6. **Post-Recovery Validation:** Verify the lacp bundle has returned to a stable operational state:
   ```
   display eth-trunk {id} | include active
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1496 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1497
**Alarm Name:** BGP Peer Resource Exhaustion
**Severity:** Warning

This alarm indicates a resource exhaustion condition on the bgp peer subsystem of Huawei equipment. Follow the steps below to restore normal operation.

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1497 for 'BGP Peer Resource Exhaustion' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display bgp peer
   ```
3. **Baseline Comparison:** Compare current performance metrics against the last known good baseline. Run `display bgp peer`.
4. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset bgp {ip}
   ```
5. **Post-Recovery Validation:** Verify the bgp peer has returned to a stable operational state:
   ```
   display bgp peer | include Established
   ```

---

## Procedure to clear ALARM_CODE_1498
**Alarm Name:** RSVP-TE Tunnel Loss of Signal (LOS)
**Severity:** Critical

This alarm indicates a loss of signal (los) condition on the rsvp-te tunnel subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1498 for 'RSVP-TE Tunnel Loss of Signal (LOS)' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display mpls te tunnel-interface
   ```
3. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, and SFP transceiver status on the affected port. Request remote-hands inspection if needed.
4. **Check Layer 3 Reachability:** Run `display mpls te tunnel-interface` to verify IP-level connectivity and routing table entries for the peer address.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset rsvp-te session tunnel {id}
   ```
6. **Post-Recovery Validation:** Verify the rsvp-te tunnel has returned to a stable operational state:
   ```
   display mpls te tunnel-interface | include Up
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1498 and diagnostic outputs collected above.

---

## Procedure to clear ALARM_CODE_1499
**Alarm Name:** Power Supply Unit (PSU) Flapping
**Severity:** Critical

This alarm indicates a flapping condition on the power supply unit (psu) subsystem of Huawei equipment. **Immediate action is required to prevent SLA breach.**

1. **Acknowledge Alarm:** Log into the Huawei NMS dashboard and confirm alarm code 1499 for 'Power Supply Unit (PSU) Flapping' on the affected node.
2. **Initial Diagnostic:** Run the following command to assess the current state:
   ```
   display power
   ```
3. **Analyze Event Correlation:** Review the system event logs for recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.
4. **Check Interface Counters:** Run `display environment` to identify input errors, CRC errors, or frame drops that indicate a physical or L2 issue.
5. **Execute Restoration:** Apply the restoration procedure:
   ```
   reset power module {mod}
   ```
6. **Post-Recovery Validation:** Verify the power supply unit (psu) has returned to a stable operational state:
   ```
   display environment | include Normal
   ```
7. **Escalation:** If the alarm persists after 15 minutes, escalate to the Huawei TAC (Technical Assistance Center) with the alarm code 1499 and diagnostic outputs collected above.

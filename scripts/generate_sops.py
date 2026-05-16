"""
Realistic SOP Generator for Telecom RAG Dataset.

Generates 100 unique Standard Operating Procedures per vendor (500 total)
with diverse, component-specific diagnostic commands, variable step counts,
and vendor-appropriate CLI syntax.

Usage:
    cd scripts/
    python generate_sops.py

The script is idempotent: it detects a marker in each SOP file and replaces
any previously generated content.  Original hand-written procedures are preserved.
"""

import os
import random

MARKER = "\n\n<!-- BEGIN GENERATED PROCEDURES -->\n"

VENDORS = {
    "Cisco": "../data/cisco_ios_xr_sop.md",
    "Nokia": "../data/nokia_router_mop.md",
    "Juniper": "../data/juniper_junos_sop.md",
    "Ericsson": "../data/ericsson_ipos_sop.md",
    "Huawei": "../data/huawei_vrp_sop.md",
}

SEVERITIES = ["Critical", "Major", "Minor", "Warning"]

# ---------------------------------------------------------------------------
# Component-specific diagnostic and restoration commands PER VENDOR
# Each entry: (component, [diag_cmds], [restore_cmds], [verify_cmds])
# ---------------------------------------------------------------------------
COMPONENT_COMMANDS = {
    "Cisco": [
        ("BGP Peer", ["show bgp ipv4 unicast summary", "show bgp neighbors {ip} detail", "show ip route bgp"],
         ["clear bgp ipv4 unicast {ip} soft in", "router bgp 65000\n  neighbor {ip} activate"],
         ["show bgp ipv4 unicast summary | include Estab"]),
        ("OSPF Adjacency", ["show ip ospf neighbor", "show ip ospf interface brief", "show ip ospf database"],
         ["clear ip ospf process", "interface GigabitEthernet0/0/0\n  ip ospf cost 10"],
         ["show ip ospf neighbor | include FULL"]),
        ("IS-IS Adjacency", ["show isis neighbors", "show isis database detail", "show isis topology"],
         ["clear isis process", "router isis 1\n  net 49.0001.0000.0001.00"],
         ["show isis neighbors | include Up"]),
        ("MPLS LDP Session", ["show mpls ldp neighbor", "show mpls forwarding-table", "show mpls ldp discovery"],
         ["clear mpls ldp neighbor {ip}", "mpls ldp router-id Loopback0 force"],
         ["show mpls ldp neighbor | include Oper"]),
        ("RSVP-TE Tunnel", ["show mpls traffic-eng tunnels brief", "show rsvp session", "show rsvp interface"],
         ["clear rsvp session tunnel-id {id}", "interface tunnel-te1\n  shutdown\n  no shutdown"],
         ["show mpls traffic-eng tunnels | include Up"]),
        ("BFD Session", ["show bfd neighbors", "show bfd counters", "show bfd session detail"],
         ["clear bfd counters", "bfd interval 300 min_rx 300 multiplier 3"],
         ["show bfd neighbors | include Up"]),
        ("LACP Bundle", ["show lacp counters", "show bundle Bundle-Ether1", "show lacp neighbor"],
         ["clear lacp counters", "interface Bundle-Ether1\n  no shutdown"],
         ["show bundle Bundle-Ether1 | include Active"]),
        ("Optical Rx Power", ["show controllers optics 0/0/0/1", "show hw-module fpd"],
         ["controller optics 0/0/0/1\n  sec-admin-state normal", "hw-module location 0/0/CPU0 reload"],
         ["show controllers optics 0/0/0/1 | include Rx"]),
        ("Line Card NPU", ["show platform", "show controllers npu resources all location 0/0/CPU0"],
         ["hw-module location 0/0/CPU0 reload", "admin clear controller fabric plane all"],
         ["show platform | include IOS XR RUN"]),
        ("Power Supply Unit (PSU)", ["show environment power", "show redundancy", "show platform"],
         ["power disable module {slot}", "power enable module {slot}"],
         ["show environment power | include Normal"]),
        ("QoS Scheduler", ["show policy-map interface te0/0/0/1", "show qos interface te0/0/0/1"],
         ["clear qos counters interface te0/0/0/1", "policy-map PM_CORE\n  class class-default\n  bandwidth percent 50"],
         ["show policy-map interface te0/0/0/1 | include conform"]),
        ("FIB (Forwarding Table)", ["show cef ipv4 summary", "show cef ipv4 inconsistency"],
         ["clear cef ipv4 inconsistency", "clear route-ha eof"],
         ["show cef ipv4 summary | include resolved"]),
        ("Management Ethernet", ["show interface MgmtEth0/RSP0/CPU0/0", "show ip interface brief"],
         ["interface MgmtEth0/RSP0/CPU0/0\n  no shutdown", "clear arp"],
         ["show interface MgmtEth0/RSP0/CPU0/0 | include up/up"]),
        ("SNMP Agent", ["show snmp", "show snmp traps", "show snmp host"],
         ["snmp-server community TELECOM_RO RO", "snmp-server host 10.0.0.1 TELECOM_RO"],
         ["show snmp | include packets"]),
        ("NTP Synchronization", ["show ntp status", "show ntp associations", "show clock"],
         ["clear ntp drift", "ntp server 10.0.0.254 prefer"],
         ["show ntp status | include synchronized"]),
    ],
    "Nokia": [
        ("BGP Peer", ["show router bgp summary", "show router bgp neighbor {ip}", "show router bgp routes ipv4"],
         ["clear router bgp neighbor {ip} soft", "configure router bgp group EXTERNAL neighbor {ip}\n  admin-state enable"],
         ["show router bgp summary | match Established"]),
        ("OSPF Adjacency", ["show router ospf neighbor", "show router ospf status", "show router ospf database"],
         ["clear router ospf neighbor all", "configure router ospf 0 area 0.0.0.0 interface to-PE\n  admin-state enable"],
         ["show router ospf neighbor | match Full"]),
        ("IS-IS Adjacency", ["show router isis adjacency", "show router isis database", "show router isis topology"],
         ["clear router isis adjacency", "configure router isis 1 interface to-PE\n  admin-state enable"],
         ["show router isis adjacency | match Up"]),
        ("MPLS LDP Session", ["show router ldp session", "show router ldp bindings", "show router mpls status"],
         ["clear router ldp session {ip}", "configure router ldp\n  admin-state enable"],
         ["show router ldp session | match Established"]),
        ("RSVP-TE Tunnel", ["show router rsvp session", "show router mpls lsp", "show router rsvp interface"],
         ["clear router rsvp session lsp-name {name}", "configure router mpls lsp {name}\n  no shutdown"],
         ["show router mpls lsp | match Up"]),
        ("VRRP Group", ["show router vrrp instance", "show router vrrp statistics"],
         ["clear router vrrp statistics", "configure router vrrp {id} backup {ip}\n  admin-state enable\n  priority 200"],
         ["show router vrrp instance | match Master"]),
        ("LACP Bundle", ["show lag 1", "show lag 1 port", "show lag 1 statistics"],
         ["clear lag statistics", "configure lag 1\n  admin-state enable\n  port 1/1/1"],
         ["show lag 1 | match active"]),
        ("Optical Rx Power", ["show port 1/1/1 optical", "show port 1/1/1 detail", "show system alarms"],
         ["admin port 1/1/1 shutdown\nadmin port 1/1/1 no shutdown", "configure port 1/1/1\n  no shutdown"],
         ["show port 1/1/1 | match Up"]),
        ("Line Card NPU", ["show chassis", "show card state", "show mda detail"],
         ["admin card {slot} reboot", "configure card {slot}\n  admin-state enable"],
         ["show card state | match up/active"]),
        ("Switch Fabric Module", ["show system switch-fabric", "show chassis environment"],
         ["admin switch-fabric {id} reboot", "configure system switch-fabric {id}\n  admin-state enable"],
         ["show system switch-fabric | match active"]),
        ("Fan Tray Assembly", ["show chassis environment", "show system alarms active"],
         ["admin environment fan-tray {id} reboot", "tools dump system-resources"],
         ["show chassis environment | match Normal"]),
        ("Power Supply Unit (PSU)", ["show chassis power-supply", "show environment power"],
         ["admin power-shelf {id} power-module {mod} reboot", "tools perform system power-check"],
         ["show chassis power-supply | match up"]),
        ("VPLS Pseudowire", ["show service sdp-using", "show service id {id} base", "show router ldp bindings active prefixes"],
         ["clear service id {id} spoke-sdp {spoke}", "configure service vpls {id}\n  admin-state enable"],
         ["show service sdp-using | match operUp"]),
        ("Management Ethernet", ["show router interface mgmt", "show system information"],
         ["configure router management\n  interface mgmt\n  no shutdown", "admin save"],
         ["show router interface mgmt | match up"]),
        ("EVPN MAC Route", ["show service evpn", "show service evpn mac-table", "show router bgp evpn routes"],
         ["clear service evpn mac-table", "configure service vpls {id} bgp-evpn\n  admin-state enable"],
         ["show service evpn | match active"]),
    ],
    "Juniper": [
        ("BGP Peer", ["show bgp summary", "show bgp neighbor {ip}", "show route protocol bgp"],
         ["clear bgp neighbor {ip}", "set protocols bgp group EXTERNAL neighbor {ip}\ncommit"],
         ["show bgp summary | match Estab"]),
        ("OSPF Adjacency", ["show ospf neighbor", "show ospf interface", "show ospf database"],
         ["clear ospf neighbor all", "set protocols ospf area 0.0.0.0 interface ge-0/0/0\ncommit"],
         ["show ospf neighbor | match Full"]),
        ("IS-IS Adjacency", ["show isis adjacency", "show isis database", "show isis interface"],
         ["clear isis adjacency", "set protocols isis interface ge-0/0/0 level 2\ncommit"],
         ["show isis adjacency | match Up"]),
        ("MPLS LDP Session", ["show ldp session", "show ldp neighbor", "show mpls interface"],
         ["clear ldp session {ip}", "set protocols ldp interface ge-0/0/0\ncommit"],
         ["show ldp session | match Operational"]),
        ("RSVP-TE Tunnel", ["show rsvp session", "show mpls lsp", "show rsvp interface"],
         ["clear rsvp session lsp-name {name}", "set protocols mpls label-switched-path {name}\n  no-install\n  deactivate\ncommit\nactivate\ncommit"],
         ["show mpls lsp | match Up"]),
        ("BFD Session", ["show bfd session", "show bfd session detail", "show bfd session summary"],
         ["clear bfd session address {ip}", "set protocols ospf area 0 interface ge-0/0/0 bfd-liveness-detection minimum-interval 300\ncommit"],
         ["show bfd session | match Up"]),
        ("LACP Bundle", ["show lacp interfaces", "show interfaces ae0", "show lacp statistics"],
         ["clear lacp statistics", "set interfaces ae0\n  aggregated-ether-options lacp active\ncommit"],
         ["show interfaces ae0 | match \"Physical link is Up\""]),
        ("Optical Rx Power", ["show interfaces diagnostics optics ge-0/0/1", "show chassis hardware"],
         ["request interface diagnostics optics ge-0/0/1", "set interfaces ge-0/0/1 disable\ndelete interfaces ge-0/0/1 disable\ncommit"],
         ["show interfaces diagnostics optics ge-0/0/1 | match \"Rx power\""]),
        ("Routing Engine CPU", ["show chassis routing-engine", "show system processes extensive", "show system uptime"],
         ["request system software rollback", "restart routing immediately"],
         ["show chassis routing-engine | match \"Idle\""]),
        ("FIB (Forwarding Table)", ["show route forwarding-table", "show route summary", "show krt queue"],
         ["clear route forwarding-table", "request route consistency-check"],
         ["show krt queue | match \"0 queued\""]),
        ("ACL Processing", ["show firewall filter", "show firewall counter", "show firewall log"],
         ["clear firewall filter PROTECT_RE counter", "set firewall filter PROTECT_RE term ALLOW_BGP then count\ncommit"],
         ["show firewall counter | match ALLOW_BGP"]),
        ("ARP Cache", ["show arp", "show arp statistics", "show interfaces ge-0/0/0"],
         ["clear arp interface ge-0/0/0", "clear arp hostname {host}"],
         ["show arp | match \"Total entries\""]),
        ("IPSec VPN Tunnel", ["show security ipsec sa", "show security ike sa", "show security ipsec statistics"],
         ["clear security ike sa", "clear security ipsec sa"],
         ["show security ipsec sa | match \"Total active\""]),
        ("GRE Tunnel", ["show interfaces gr-0/0/0", "show route table inet.0 protocol static"],
         ["clear interfaces statistics gr-0/0/0", "set interfaces gr-0/0/0 unit 0 tunnel source {src} destination {dst}\ncommit"],
         ["show interfaces gr-0/0/0 | match \"Link is Up\""]),
        ("Multicast PIM Neighbor", ["show pim neighbors", "show pim join", "show multicast route"],
         ["clear pim join all", "set protocols pim interface ge-0/0/0 mode sparse\ncommit"],
         ["show pim neighbors | match ge-"]),
    ],
    "Ericsson": [
        ("BGP Peer", ["show bgp summary", "show bgp neighbor {ip} detail", "show ip route bgp"],
         ["clear bgp neighbor {ip}", "configure\n  router bgp {asn}\n  neighbor {ip}\n  admin-state enable\n  commit"],
         ["show bgp summary | include Established"]),
        ("OSPF Adjacency", ["show ospf neighbor", "show ospf interface", "show ospf area"],
         ["clear ospf process", "configure\n  router ospf {pid}\n  area 0.0.0.0 interface {intf}\n  commit"],
         ["show ospf neighbor | include Full"]),
        ("IS-IS Adjacency", ["show isis adjacency", "show isis database", "show isis spf-log"],
         ["clear isis adjacency", "configure\n  router isis {tag}\n  interface {intf} circuit-type level-2\n  commit"],
         ["show isis adjacency | include Up"]),
        ("MPLS LDP Session", ["show mpls ldp session", "show mpls ldp bindings"],
         ["clear mpls ldp session {ip}", "configure\n  router ldp\n  interface {intf}\n  commit"],
         ["show mpls ldp session | include Operational"]),
        ("BFD Session", ["show bfd session", "show bfd session detail"],
         ["clear bfd session discriminator {disc}", "configure\n  bfd interface {intf} receive-interval 300 transmit-interval 300\n  commit"],
         ["show bfd session | include Up"]),
        ("LACP Bundle", ["show port lag", "show port {port} detail", "show port lag statistics"],
         ["clear port lag statistics", "configure\n  port lag {id}\n  admin-state enable\n  commit"],
         ["show port lag | include active"]),
        ("Optical Rx Power", ["show port {port} transceiver detail", "show port {port} optical-power"],
         ["clear port {port} statistics", "configure\n  port {port}\n  admin-state disable\n  admin-state enable\n  commit"],
         ["show port {port} transceiver detail | include Rx"]),
        ("Line Card NPU", ["show system processes", "show chassis card", "show chassis environment"],
         ["clear port hardware {card}", "admin chassis card {card} restart"],
         ["show chassis card | include Online"]),
        ("Routing Engine CPU", ["show system cpu-usage", "show system memory", "show system processes top"],
         ["clear system cpu-usage history", "admin system restart process routing"],
         ["show system cpu-usage | include idle"]),
        ("Power Supply Unit (PSU)", ["show chassis power-shelf", "show chassis environment"],
         ["admin chassis power-shelf {shelf} power-module {mod} restart", "show chassis power-shelf detail"],
         ["show chassis power-shelf | include OK"]),
        ("VRRP Group", ["show vrrp", "show vrrp statistics", "show vrrp interface"],
         ["clear vrrp statistics", "configure\n  router vrrp {id}\n  priority 150\n  preempt\n  admin-state enable\n  commit"],
         ["show vrrp | include Master"]),
        ("QoS Scheduler", ["show qos policy-map applied", "show qos interface {intf} statistics"],
         ["clear qos interface {intf} statistics", "configure\n  qos policy-map PM_CORE\n  class default bandwidth-percent 60\n  commit"],
         ["show qos interface {intf} statistics | include conform"]),
        ("SNMP Agent", ["show snmp community", "show snmp statistics", "show snmp trap-host"],
         ["clear snmp statistics", "configure\n  snmp community TELECOM_RO authorization read-only\n  commit"],
         ["show snmp statistics | include packets-received"]),
        ("NTP Synchronization", ["show ntp status", "show ntp associations"],
         ["clear ntp drift", "configure\n  ntp server {ip} prefer\n  commit"],
         ["show ntp status | include synchronized"]),
        ("Management Ethernet", ["show interface mgmt", "show system information"],
         ["configure\n  interface mgmt\n  no shutdown\n  commit", "clear arp interface mgmt"],
         ["show interface mgmt | include up"]),
    ],
    "Huawei": [
        ("BGP Peer", ["display bgp peer", "display bgp peer {ip} verbose", "display bgp routing-table"],
         ["reset bgp {ip}", "system-view\n  bgp {asn}\n  peer {ip} enable"],
         ["display bgp peer | include Established"]),
        ("OSPF Adjacency", ["display ospf peer", "display ospf interface", "display ospf lsdb"],
         ["reset ospf process", "system-view\n  ospf {pid}\n  area 0.0.0.0\n  network {net} {mask}"],
         ["display ospf peer | include Full"]),
        ("IS-IS Adjacency", ["display isis peer", "display isis lsdb", "display isis interface"],
         ["reset isis all", "system-view\n  isis {tag}\n  network-entity 49.0001.0000.0001.00"],
         ["display isis peer | include Up"]),
        ("MPLS LDP Session", ["display mpls ldp session", "display mpls ldp lsp", "display mpls lsp"],
         ["reset mpls ldp session peer {ip}", "system-view\n  mpls ldp\n  interface {intf}\n  mpls ldp enable"],
         ["display mpls ldp session | include Operational"]),
        ("RSVP-TE Tunnel", ["display mpls te tunnel-interface", "display rsvp-te session"],
         ["reset rsvp-te session tunnel {id}", "system-view\n  interface Tunnel{id}\n  undo shutdown"],
         ["display mpls te tunnel-interface | include Up"]),
        ("BFD Session", ["display bfd session all", "display bfd statistics"],
         ["reset bfd session discriminator {disc}", "system-view\n  bfd {name}\n  discriminator local {local} remote {remote}\n  commit"],
         ["display bfd session all | include Up"]),
        ("LACP Bundle", ["display eth-trunk {id}", "display lacp statistics eth-trunk {id}"],
         ["reset lacp statistics eth-trunk {id}", "system-view\n  interface Eth-Trunk{id}\n  undo shutdown"],
         ["display eth-trunk {id} | include active"]),
        ("Optical Rx Power", ["display transceiver {port}", "display interface {port} transceiver"],
         ["restart interface {port}", "system-view\n  interface {port}\n  undo shutdown"],
         ["display transceiver {port} | include Rx"]),
        ("Line Card NPU", ["display device", "display device slot", "display device manufacture-info"],
         ["reset counters interface {intf}", "reset slot {slot}"],
         ["display device | include Normal"]),
        ("Power Supply Unit (PSU)", ["display power", "display environment"],
         ["reset power module {mod}", "display power | include Normal"],
         ["display environment | include Normal"]),
        ("Fan Tray Assembly", ["display fan", "display environment"],
         ["reset fan module {mod}", "display environment"],
         ["display fan | include Normal"]),
        ("VRRP Group", ["display vrrp", "display vrrp statistics"],
         ["reset vrrp statistics", "system-view\n  interface GigabitEthernet0/0/0\n  vrrp vrid {id} virtual-ip {vip}\n  vrrp vrid {id} priority 120"],
         ["display vrrp | include Master"]),
        ("QoS Scheduler", ["display qos policy applied-statistics interface {intf} outbound", "display traffic-policy statistics"],
         ["reset traffic-policy statistics interface {intf} outbound", "system-view\n  traffic-policy TP_CORE outbound"],
         ["display qos policy applied-statistics interface {intf} | include pass"]),
        ("ARP Cache", ["display arp", "display arp statistics"],
         ["reset arp interface {intf}", "arp static {ip} {mac}"],
         ["display arp | include Total"]),
        ("DHCP Relay Agent", ["display dhcp relay all", "display dhcp relay statistics"],
         ["reset dhcp relay statistics", "system-view\n  dhcp enable\n  interface {intf}\n  dhcp relay server-ip {server_ip}"],
         ["display dhcp relay statistics | include received"]),
    ],
}

# Fault conditions grouped by category for appropriate procedure templates
FAULT_CONDITIONS = {
    "connectivity_loss": ["Down", "Unreachable", "Loss of Signal (LOS)"],
    "instability": ["Flapping", "Timeout", "Stuck in INIT State", "Out of Sync"],
    "performance": ["Performance Degraded", "Resource Exhaustion", "Threshold Exceeded", "High CRC Rate", "Memory Leak Detected"],
    "config": ["Configuration Mismatch", "Authentication Failed"],
    "hardware": ["Hardware Failure", "Capacity Limit Reached"],
}

ALL_CONDITIONS = []
for conds in FAULT_CONDITIONS.values():
    ALL_CONDITIONS.extend(conds)


def _get_fault_category(condition: str) -> str:
    """Map a fault condition to its category."""
    for cat, conds in FAULT_CONDITIONS.items():
        if condition in conds:
            return cat
    return "connectivity_loss"


def generate_procedure(vendor: str, component: str, condition: str, alarm_code: int,
                       diag_cmds: list, restore_cmds: list, verify_cmds: list) -> str:
    """Generate a single, unique SOP procedure with variable structure."""
    severity = random.choice(SEVERITIES)
    category = _get_fault_category(condition)
    alarm_name = f"{component} {condition}"

    # Pick a random subset of diagnostic commands (1-2)
    diag_1 = random.choice(diag_cmds)
    diag_2 = random.choice(diag_cmds) if len(diag_cmds) > 1 else diag_1

    restore_cmd = random.choice(restore_cmds)
    verify_cmd = random.choice(verify_cmds)

    # Build procedure steps - vary structure by fault category
    steps = []
    step_num = 1

    # Step 1: Always acknowledge
    steps.append(f"{step_num}. **Acknowledge Alarm:** Log into the {vendor} NMS dashboard "
                 f"and confirm alarm code {alarm_code} for '{alarm_name}' on the affected node.")
    step_num += 1

    # Step 2: Initial diagnostic
    steps.append(f"{step_num}. **Initial Diagnostic:** Run the following command to assess the current state:\n"
                 f"   ```\n   {diag_1}\n   ```")
    step_num += 1

    # Category-specific steps
    if category == "connectivity_loss":
        steps.append(f"{step_num}. **Verify Physical Layer:** Check the physical connectivity, fiber integrity, "
                     f"and SFP transceiver status on the affected port. Request remote-hands inspection if needed.")
        step_num += 1
        steps.append(f"{step_num}. **Check Layer 3 Reachability:** Run `{diag_2}` to verify IP-level connectivity "
                     f"and routing table entries for the peer address.")
        step_num += 1
    elif category == "instability":
        steps.append(f"{step_num}. **Analyze Event Correlation:** Review the system event logs for "
                     f"recurring patterns. Look for correlating alarms on adjacent nodes that may indicate an upstream trigger.")
        step_num += 1
        steps.append(f"{step_num}. **Check Interface Counters:** Run `{diag_2}` to identify "
                     f"input errors, CRC errors, or frame drops that indicate a physical or L2 issue.")
        step_num += 1
    elif category == "performance":
        steps.append(f"{step_num}. **Baseline Comparison:** Compare current performance metrics against "
                     f"the last known good baseline. Run `{diag_2}`.")
        step_num += 1
        if severity in ["Critical", "Major"]:
            steps.append(f"{step_num}. **⚠️ WARNING: Service Impact Possible.** If the {component.lower()} "
                         f"utilization exceeds 90%, consider emergency traffic rerouting before proceeding.")
            step_num += 1
    elif category == "config":
        steps.append(f"{step_num}. **Configuration Audit:** Compare the running configuration against the "
                     f"golden config template. Run `{diag_2}` to verify key parameters.")
        step_num += 1
        steps.append(f"{step_num}. **Peer Coordination:** Contact the peer administrator to verify "
                     f"matching configuration parameters (keys, ASN, timers, etc.).")
        step_num += 1
    elif category == "hardware":
        steps.append(f"{step_num}. **Hardware Status Check:** Run `{diag_2}` to identify the specific "
                     f"failed hardware module, slot, or component.")
        step_num += 1
        steps.append(f"{step_num}. **⚠️ CRITICAL: Potential Traffic Impact.** Verify that redundancy "
                     f"mechanisms (standby modules, ECMP paths) are active before performing hardware operations.")
        step_num += 1
        steps.append(f"{step_num}. **Physical Intervention:** Dispatch a field technician to inspect "
                     f"and, if necessary, reseat or replace the affected {component.lower()} unit. Open an RMA case.")
        step_num += 1

    # Restoration step (always present)
    steps.append(f"{step_num}. **Execute Restoration:** Apply the restoration procedure:\n"
                 f"   ```\n   {restore_cmd}\n   ```")
    step_num += 1

    # Post-validation step (always present)
    steps.append(f"{step_num}. **Post-Recovery Validation:** Verify the {component.lower()} has returned to "
                 f"a stable operational state:\n"
                 f"   ```\n   {verify_cmd}\n   ```")
    step_num += 1

    # Escalation step for Critical/Major severities
    if severity in ["Critical", "Major"]:
        steps.append(f"{step_num}. **Escalation:** If the alarm persists after 15 minutes, escalate to the "
                     f"{vendor} TAC (Technical Assistance Center) with the alarm code {alarm_code} "
                     f"and diagnostic outputs collected above.")
        step_num += 1

    steps_text = "\n".join(steps)

    return f"""
---

## Procedure to clear ALARM_CODE_{alarm_code}
**Alarm Name:** {alarm_name}
**Severity:** {severity}

This alarm indicates a {condition.lower()} condition on the {component.lower()} subsystem of {vendor} equipment. {'**Immediate action is required to prevent SLA breach.**' if severity == 'Critical' else 'Follow the steps below to restore normal operation.'}

{steps_text}
"""


def main():
    """Generate and append 100 unique procedures per vendor."""
    # Build all unique (component, condition) combinations
    all_combos = []
    for vendor, cmd_list in COMPONENT_COMMANDS.items():
        for component, diag, restore, verify in cmd_list:
            for condition in ALL_CONDITIONS:
                all_combos.append((vendor, component, condition, diag, restore, verify))

    random.shuffle(all_combos)

    # Distribute 100 per vendor
    vendor_queues = {v: [] for v in VENDORS}
    for combo in all_combos:
        vendor = combo[0]
        if len(vendor_queues[vendor]) < 100:
            vendor_queues[vendor].append(combo)

    global_code = 1000

    for vendor, path in VENDORS.items():
        if not os.path.exists(path):
            print(f"⚠️  {path} not found, skipping {vendor}")
            continue

        # Read existing content and strip previously generated procedures
        with open(path, "r") as f:
            content = f.read()

        marker_pos = content.find(MARKER)
        if marker_pos != -1:
            content = content[:marker_pos]
            print(f"♻️  Stripped old generated procedures from {path}")

        # Generate new procedures
        new_content = MARKER
        for combo in vendor_queues[vendor]:
            _, component, condition, diag_cmds, restore_cmds, verify_cmds = combo
            new_content += generate_procedure(
                vendor, component, condition, global_code,
                diag_cmds, restore_cmds, verify_cmds
            )
            global_code += 1

        # Write back
        with open(path, "w") as f:
            f.write(content + new_content)

        print(f"✅ Appended 100 unique procedures to {path} (codes {global_code - 100}–{global_code - 1})")

    print(f"\n🎯 Total: {global_code - 1000} procedures generated across {len(VENDORS)} vendors")


if __name__ == "__main__":
    main()

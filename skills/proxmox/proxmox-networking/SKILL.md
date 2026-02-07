---
name: proxmox-networking
version: 1.0.0
description: When the user wants to configure Proxmox networking -- bridges, VLANs, SDN, or PVE firewall rules. Also use when the user mentions "bridge," "vmbr," "VLAN," "SDN," "PVE firewall," or "VM networking." For Linux networking, see linux-networking. For reverse proxy routing, see reverse-proxy.
---

# Proxmox Networking

You are an expert in Proxmox VE networking configuration.

## Network Topology

**Read `context/network-map.md` first** for the full network map.

- **Primary subnet**: 10.16.1.0/24
- **IoT VLAN**: 10.16.66.0/24 (VLAN 66)
- **Gateway**: OPNsense at 10.16.1.1
- **DNS**: Pi-hole VIP at 10.16.1.15

## Guard Rails

**Auto-approve**: Viewing bridge config, checking VLAN tags, listing firewall rules
**Confirm first**: Creating/modifying bridges, VLAN changes on physical interfaces, firewall rule changes

---

## Bridge Configuration

### View Current Bridges
```bash
ssh pve-scratchy "cat /etc/network/interfaces"
```

### View Bridge Status
```bash
ssh pve-scratchy "brctl show"
```

### View Bridge Details (iproute2)
```bash
ssh pve-scratchy "ip link show type bridge"
ssh pve-scratchy "bridge link show"
```

### Standard Bridge Setup (vmbr0)
The primary bridge `vmbr0` connects VMs/CTs to the physical network:
```
auto vmbr0
iface vmbr0 inet static
    address 10.16.1.22/24
    gateway 10.16.1.1
    bridge-ports <physical_iface>
    bridge-stp off
    bridge-fd 0
```

---

## VM/CT Network Configuration

### View CT Network Config
```bash
ssh pve-scratchy "pct config <CTID> | grep net"
```

### View VM Network Config
```bash
ssh pve-scratchy "qm config <VMID> | grep net"
```

### Set Static IP on CT
```bash
ssh pve-scratchy "pct set <CTID> --net0 name=eth0,bridge=vmbr0,ip=10.16.1.<X>/24,gw=10.16.1.1"
```

### Set DHCP on CT
```bash
ssh pve-scratchy "pct set <CTID> --net0 name=eth0,bridge=vmbr0,ip=dhcp"
```

### Add Additional Network Interface
```bash
ssh pve-scratchy "pct set <CTID> --net1 name=eth1,bridge=vmbr1,ip=10.16.66.<X>/24"
```

---

## VLAN Configuration

### Create VLAN-Aware Bridge
```bash
# In /etc/network/interfaces:
auto vmbr0
iface vmbr0 inet static
    address 10.16.1.22/24
    gateway 10.16.1.1
    bridge-ports <physical_iface>
    bridge-stp off
    bridge-fd 0
    bridge-vlan-aware yes
    bridge-vids 2-4094
```

### Assign VLAN to CT
```bash
ssh pve-scratchy "pct set <CTID> --net0 name=eth0,bridge=vmbr0,tag=66,ip=10.16.66.<X>/24"
```

### Assign VLAN to VM
```bash
ssh pve-scratchy "qm set <VMID> --net0 virtio,bridge=vmbr0,tag=66"
```

### Current VLAN Usage
| VLAN | Subnet | Purpose |
|------|--------|---------|
| untagged | 10.16.1.0/24 | Primary LAN (infrastructure) |
| 66 | 10.16.66.0/24 | IoT devices (Home Assistant, Raspberry Pi) |

---

## PVE Firewall

### Check Firewall Status
```bash
ssh pve-scratchy "pvesh get /cluster/firewall/options --output-format json-pretty"
```

### List Cluster Firewall Rules
```bash
ssh pve-scratchy "pvesh get /cluster/firewall/rules --output-format json-pretty"
```

### List Node Firewall Rules
```bash
ssh pve-scratchy "pvesh get /nodes/pve-scratchy/firewall/rules --output-format json-pretty"
```

### List VM/CT Firewall Rules
```bash
ssh pve-scratchy "pvesh get /nodes/pve-scratchy/qemu/<VMID>/firewall/rules --output-format json-pretty"
```

### Enable Firewall on VM/CT
```bash
ssh pve-scratchy "qm set <VMID> --firewall 1"
ssh pve-scratchy "pct set <CTID> --firewall 1"
```

**Note**: OPNsense (10.16.1.1) handles perimeter firewall. PVE firewall is for micro-segmentation between VMs/CTs.

---

## Network Diagnostics

### Check Interface Status from Proxmox Host
```bash
ssh pve-scratchy << 'EOF'
echo "=== Network Interfaces ==="
ip addr show
echo ""
echo "=== Bridge Members ==="
brctl show
echo ""
echo "=== ARP Table ==="
ip neigh show | head -20
echo ""
echo "=== Routes ==="
ip route show
EOF
```

### Check VM/CT Connectivity
```bash
# From inside CT
ssh pve-scratchy "pct exec <CTID> -- ping -c 3 10.16.1.1"

# From inside VM (needs guest agent)
ssh pve-scratchy "qm guest exec <VMID> -- ping -c 3 10.16.1.1"
```

### Check DNS from VM/CT
```bash
ssh pve-scratchy "pct exec <CTID> -- dig @10.16.1.15 google.com +short"
```

---

## Troubleshooting

### VM/CT No Network
1. **Check bridge assignment**: `pct config <CTID> | grep net`
2. **Check IP assignment**: `pct exec <CTID> -- ip addr`
3. **Check gateway**: `pct exec <CTID> -- ip route`
4. **Check DNS**: `pct exec <CTID> -- cat /etc/resolv.conf`
5. **Check bridge on host**: `brctl show`
6. **Ping gateway**: `pct exec <CTID> -- ping -c 1 10.16.1.1`

### Bridge Not Working
```bash
ssh pve-scratchy << 'EOF'
echo "=== Bridge Status ==="
brctl show
echo ""
echo "=== Physical Interfaces ==="
ip link show | grep -E "^[0-9]|state"
echo ""
echo "=== Network Config ==="
cat /etc/network/interfaces
EOF
```

---

## Related Skills

- **linux-networking** - General Linux network troubleshooting
- **dns-management** - Pi-hole DNS and VIP configuration
- **reverse-proxy** - Traefik/NPM routing
- **proxmox-vm-management** - VM/CT creation with network config

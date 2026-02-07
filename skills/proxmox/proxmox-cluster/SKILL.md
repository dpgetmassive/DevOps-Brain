---
name: proxmox-cluster
version: 1.0.0
description: When the user wants to check or manage the Proxmox cluster -- cluster health, quorum status, corosync, node management, or HA groups. Also use when the user mentions "cluster status," "quorum," "corosync," "pvecm," "node offline," or "HA failover." For VM/CT operations, see proxmox-vm-management. For Proxmox networking, see proxmox-networking.
---

# Proxmox Cluster Management

You are an expert in Proxmox VE cluster administration. The homelab runs a 2-node cluster with an external quorum device.

## Cluster Topology

**Read `context/infrastructure-context.md` first.**

| Component | Host | IP | Role |
|-----------|------|-----|------|
| Primary node | pve-scratchy | 10.16.1.22 | Hosts majority of workloads |
| Secondary node | pve-itchy | 10.16.1.8 | Backup node, hosts TrueNAS DR VM |
| Quorum device | n100uck | 10.16.1.18 | corosync-qnetd (independent witness) |
| Web UI | pve-scratchy | https://10.16.1.22:8006 | Primary management interface |
| Web UI | pve-itchy | https://10.16.1.8:8006 | Secondary management interface |

## Guard Rails

**Auto-approve**: Status checks, node listing, resource queries
**Confirm first**: `pvecm` commands affecting quorum, node removal, HA group changes, force quorum

---

## Cluster Health Check

### Quick Status
```bash
ssh pve-scratchy "pvecm status"
```

### Detailed Cluster Status
```bash
ssh pve-scratchy << 'EOF'
echo "=== CLUSTER STATUS ==="
pvecm status
echo ""
echo "=== NODE LIST ==="
pvecm nodes
echo ""
echo "=== QUORUM STATUS ==="
corosync-quorumtool -s
echo ""
echo "=== QDEVICE STATUS ==="
corosync-quorumtool -s | grep -A5 "Qdevice"
echo ""
echo "=== RESOURCE USAGE ==="
pvesh get /cluster/resources --type node --output-format json-pretty
EOF
```

### Check Qnetd on Witness Node
```bash
ssh n100uck "systemctl status corosync-qnetd --no-pager"
```

### Check Cluster From Both Nodes
```bash
echo "=== pve-scratchy ===" && ssh pve-scratchy "pvecm status | head -20"
echo ""
echo "=== pve-itchy ===" && ssh pve-itchy "pvecm status | head -20"
```

---

## Node Management

### List All Nodes
```bash
ssh pve-scratchy "pvecm nodes"
```

### Check Node Online Status
```bash
ssh pve-scratchy "pvesh get /nodes --output-format json-pretty"
```

### View Node Resources
```bash
ssh pve-scratchy "pvesh get /nodes/pve-scratchy/status --output-format json-pretty"
```

### List All VMs and CTs Across Cluster
```bash
ssh pve-scratchy "pvesh get /cluster/resources --type vm --output-format json-pretty"
```

---

## Quorum Management

### Check Quorum Status
```bash
ssh pve-scratchy "corosync-quorumtool -s"
```

### Expected Quorum (Healthy State)
- 2 nodes + 1 qdevice = quorum with any 2 of 3 votes
- Both nodes online: Full quorum
- One node down + qdevice: Still quorate

### Force Quorum (Emergency - Single Node)
```bash
# DANGER: Only use when one node is permanently down
# and you need the remaining node to operate alone
ssh pve-itchy "pvecm expected 1"
```

### Check Corosync Ring
```bash
ssh pve-scratchy "corosync-cfgtool -s"
```

---

## HA (High Availability)

### List HA Resources
```bash
ssh pve-scratchy "ha-manager status"
```

### List HA Groups
```bash
ssh pve-scratchy "pvesh get /cluster/ha/groups --output-format json-pretty"
```

### Add VM to HA
```bash
ssh pve-scratchy "ha-manager add vm:<VMID> --group <group_name>"
```

### Remove VM from HA
```bash
ssh pve-scratchy "ha-manager remove vm:<VMID>"
```

### Check HA Manager Status
```bash
ssh pve-scratchy "systemctl status pve-ha-lrm pve-ha-crm --no-pager"
```

---

## Cluster Tasks and Logs

### View Recent Cluster Tasks
```bash
ssh pve-scratchy "pvesh get /cluster/tasks --output-format json-pretty" | head -50
```

### View Cluster Log
```bash
ssh pve-scratchy "pvesh get /cluster/log --max 20 --output-format json-pretty"
```

### Check Corosync Logs
```bash
ssh pve-scratchy "journalctl -u corosync -n 30 --no-pager"
```

---

## Node Failover Procedures

### pve-scratchy Down (Primary Node)

1. **Verify from secondary**:
   ```bash
   ssh pve-itchy "pvecm status"
   ssh pve-itchy "pvecm nodes"
   ```

2. **Check quorum** (should still be quorate with qdevice):
   ```bash
   ssh pve-itchy "corosync-quorumtool -s"
   ```

3. **If quorum lost** (both primary and qdevice down):
   ```bash
   ssh pve-itchy "pvecm expected 1"
   ```

4. **Access UI on secondary**: https://10.16.1.8:8006

5. **Migrate VMs if needed**:
   See `proxmox-vm-management` skill for migration procedures.

### Qnetd Down (Witness Node)

1. **Check from either Proxmox node**:
   ```bash
   ssh pve-scratchy "corosync-quorumtool -s | grep Qdevice"
   ```

2. **Cluster still operational** (2 nodes = majority without qdevice)

3. **Restart qnetd on n100uck**:
   ```bash
   ssh n100uck "systemctl restart corosync-qnetd"
   ```

4. **Verify qdevice reconnected**:
   ```bash
   ssh pve-scratchy "corosync-quorumtool -s | grep -A3 Qdevice"
   ```

---

## Troubleshooting

### Cluster Communication Issues
```bash
ssh pve-scratchy << 'EOF'
echo "=== Corosync Ring Status ==="
corosync-cfgtool -s
echo ""
echo "=== Ping Secondary ==="
ping -c 3 10.16.1.8
echo ""
echo "=== Corosync Logs ==="
journalctl -u corosync -S '10 min ago' --no-pager
EOF
```

### Split Brain Detection
```bash
# Check both nodes claim to be quorate
echo "=== pve-scratchy ===" && ssh pve-scratchy "corosync-quorumtool -s | grep Quorate"
echo "=== pve-itchy ===" && ssh pve-itchy "corosync-quorumtool -s | grep Quorate"
```

---

## Related Skills

- **proxmox-vm-management** - VM/CT lifecycle and migration
- **proxmox-backup-restore** - Backup and restore operations
- **proxmox-networking** - Cluster network configuration
- **monitoring-ops** - Cluster monitoring via n100uck

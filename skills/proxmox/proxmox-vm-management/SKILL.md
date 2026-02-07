---
name: proxmox-vm-management
version: 1.0.0
description: When the user wants to manage Proxmox VMs or containers -- create, start, stop, clone, template, migrate, resize, or configure VMs and CTs. Also use when the user mentions "create VM," "create container," "LXC," "clone," "template," "migrate," "qm," "pct," or "VM settings." For cluster operations, see proxmox-cluster. For backups, see proxmox-backup-restore.
---

# Proxmox VM/CT Management

You are an expert in Proxmox VE virtual machine and container management.

## Initial Assessment

**Read `context/infrastructure-context.md` first** for the full VM/CT inventory.

Before operating:
1. **Identify the target** - VM ID, name, and which node it runs on
2. **Check current state** - Running, stopped, or locked?
3. **Verify resources** - Enough CPU/RAM/disk on the target node?

## Guard Rails

**Auto-approve**: Status checks, listing VMs/CTs, viewing configs, snapshots
**Confirm first**: VM/CT destruction, bulk operations, migrations during business hours

---

## Listing VMs and CTs

### List All on Primary Node
```bash
ssh pve-scratchy << 'EOF'
echo "=== VMs ==="
qm list
echo ""
echo "=== Containers ==="
pct list
EOF
```

### List All on Secondary Node
```bash
ssh pve-itchy << 'EOF'
echo "=== VMs ==="
qm list
echo ""
echo "=== Containers ==="
pct list
EOF
```

### List All Cluster Resources
```bash
ssh pve-scratchy "pvesh get /cluster/resources --type vm --output-format json-pretty"
```

---

## Container (LXC) Operations

### Start / Stop / Restart
```bash
ssh pve-scratchy "pct start <CTID>"
ssh pve-scratchy "pct stop <CTID>"
ssh pve-scratchy "pct reboot <CTID>"
ssh pve-scratchy "pct shutdown <CTID>"  # Graceful
```

### Check Status
```bash
ssh pve-scratchy "pct status <CTID>"
```

### View Config
```bash
ssh pve-scratchy "pct config <CTID>"
```

### Execute Command Inside CT
```bash
ssh pve-scratchy "pct exec <CTID> -- <command>"
# Example: check disk in CT 121 (no SSH)
ssh pve-scratchy "pct exec 121 -- df -h"
```

### Create New Container
```bash
ssh pve-scratchy << 'EOF'
pct create <CTID> local:vztmpl/<template>.tar.zst \
  --hostname <name> \
  --memory 1024 \
  --cores 2 \
  --rootfs local-lvm:8 \
  --net0 name=eth0,bridge=vmbr0,ip=10.16.1.<X>/24,gw=10.16.1.1 \
  --nameserver 10.16.1.15 \
  --unprivileged 1 \
  --start 1
EOF
```

### Resize Container Disk
```bash
ssh pve-scratchy "pct resize <CTID> rootfs +5G"
```

### Modify Resources
```bash
ssh pve-scratchy "pct set <CTID> --memory 2048 --cores 4"
```

---

## VM (QEMU) Operations

### Start / Stop / Restart
```bash
ssh pve-scratchy "qm start <VMID>"
ssh pve-scratchy "qm stop <VMID>"
ssh pve-scratchy "qm reboot <VMID>"
ssh pve-scratchy "qm shutdown <VMID>"  # Graceful via ACPI
```

### Check Status
```bash
ssh pve-scratchy "qm status <VMID>"
```

### View Config
```bash
ssh pve-scratchy "qm config <VMID>"
```

### Create New VM
```bash
ssh pve-scratchy << 'EOF'
qm create <VMID> \
  --name <name> \
  --memory 2048 \
  --cores 2 \
  --sockets 1 \
  --net0 virtio,bridge=vmbr0 \
  --scsihw virtio-scsi-single \
  --scsi0 local-lvm:32 \
  --ide2 local:iso/<iso_name>.iso,media=cdrom \
  --boot order=scsi0;ide2 \
  --ostype l26
EOF
```

### Resize VM Disk
```bash
ssh pve-scratchy "qm resize <VMID> scsi0 +10G"
```

### Execute Command in VM (requires guest agent)
```bash
ssh pve-scratchy "qm guest exec <VMID> -- <command>"
```

---

## Snapshots

### Create Snapshot
```bash
# Container
ssh pve-scratchy "pct snapshot <CTID> <snapname> --description 'Before update'"

# VM
ssh pve-scratchy "qm snapshot <VMID> <snapname> --description 'Before update'"
```

### List Snapshots
```bash
ssh pve-scratchy "pct listsnapshot <CTID>"
ssh pve-scratchy "qm listsnapshot <VMID>"
```

### Rollback to Snapshot
```bash
ssh pve-scratchy "pct rollback <CTID> <snapname>"
ssh pve-scratchy "qm rollback <VMID> <snapname>"
```

### Delete Snapshot
```bash
ssh pve-scratchy "pct delsnapshot <CTID> <snapname>"
ssh pve-scratchy "qm delsnapshot <VMID> <snapname>"
```

---

## Templates and Cloning

### Convert CT to Template
```bash
ssh pve-scratchy "pct template <CTID>"
```

### Clone from Template
```bash
# Full clone (independent)
ssh pve-scratchy "pct clone <TEMPLATE_CTID> <NEW_CTID> --full --hostname <name>"

# Linked clone (uses less storage, depends on template)
ssh pve-scratchy "pct clone <TEMPLATE_CTID> <NEW_CTID> --hostname <name>"
```

### Clone a VM
```bash
ssh pve-scratchy "qm clone <TEMPLATE_VMID> <NEW_VMID> --full --name <name>"
```

---

## Migration

### Live Migrate VM (Online)
```bash
ssh pve-scratchy "qm migrate <VMID> pve-itchy --online"
```

### Migrate CT
```bash
ssh pve-scratchy "pct migrate <CTID> pve-itchy"
```

### Check Migration Status
```bash
ssh pve-scratchy "pvesh get /nodes/pve-scratchy/tasks --output-format json-pretty" | head -20
```

---

## Resource Monitoring

### Check Node Resource Usage
```bash
ssh pve-scratchy << 'EOF'
echo "=== CPU/Memory ==="
pvesh get /nodes/pve-scratchy/status --output-format json-pretty | grep -E '"(cpu|memory|maxmem|uptime)"'
echo ""
echo "=== Storage ==="
pvesh get /nodes/pve-scratchy/storage --output-format json-pretty
EOF
```

### Check VM/CT Resource Usage
```bash
ssh pve-scratchy "pvesh get /nodes/pve-scratchy/qemu/<VMID>/status/current --output-format json-pretty"
```

---

## Troubleshooting

### Container Won't Start
```bash
ssh pve-scratchy << 'EOF'
echo "=== CT Config ==="
pct config <CTID>
echo ""
echo "=== Start with Debug ==="
pct start <CTID> --debug
echo ""
echo "=== CT Logs ==="
journalctl -u pve-container@<CTID> -n 30 --no-pager
EOF
```

### VM Locked
```bash
# Check lock
ssh pve-scratchy "qm config <VMID> | grep lock"

# Remove lock (use with caution)
ssh pve-scratchy "qm unlock <VMID>"
```

---

## Related Skills

- **proxmox-cluster** - Cluster health and quorum
- **proxmox-backup-restore** - Backup and restore VMs/CTs
- **proxmox-networking** - VM/CT network configuration
- **linux-admin** - Post-creation OS configuration

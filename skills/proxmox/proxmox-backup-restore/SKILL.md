---
name: proxmox-backup-restore
version: 1.0.0
description: When the user wants to manage Proxmox backups, restore VMs/CTs, check backup status, or configure retention policies. Also use when the user mentions "backup," "restore," "vzdump," "backup schedule," "retention," "PBS," or "disaster recovery." For ZFS/TrueNAS storage, see storage-management. For monitoring backup status, see monitoring-ops.
---

# Proxmox Backup & Restore

You are an expert in Proxmox backup and restore operations.

## Backup Architecture

**Read `context/infrastructure-context.md` first** for the full backup topology.

| Layer | Schedule | Source | Target | Method |
|-------|----------|--------|--------|--------|
| Proxmox Native | 2:45 AM daily | All VMs/CTs (except 110, 115, 107, 112) | TrueNAS DR NFS | vzdump (zstd) |
| ZFS Replication | 2:10 AM daily | Tank/FileServer | TrueNAS DR | ZFS incremental |
| ZFS Replication (gm-ai) | 3:00 AM daily | homelab pool | TrueNAS DR | zfs send/recv |
| CloudSync | 4:00 AM daily | TrueNAS DR | Backblaze B2 | CloudSync |

**Backup storage**: `/mnt/pve/pve-bk-truenas-dr/dump/` (NFS from TrueNAS DR at 10.16.1.20)
**Retention**: 7 daily + 1 monthly
**Excluded VMs**: 110 (TrueNAS Primary), 115 (TrueNAS DR) -- too large and backed up differently
**Excluded CTs**: 107 (Sonarr), 112 (Radarr) -- can be rebuilt from config

## Guard Rails

**Auto-approve**: Backup status checks, listing backups, viewing logs, verify backup integrity
**Confirm first**: Manual restores to production, changing retention policies, deleting backups

---

## Backup Status

### Quick Check (via monitoring)
```bash
ssh n100uck "cat /var/run/backup-status.state"
```

### Check Backup Storage Space
```bash
ssh pve-scratchy "df -h /mnt/pve/pve-bk-truenas-dr"
```

### List Recent Backups
```bash
ssh pve-scratchy "ls -lht /mnt/pve/pve-bk-truenas-dr/dump/ | head -30"
```

### List Backups for Specific VM/CT
```bash
# VM 100
ssh pve-scratchy "ls -lh /mnt/pve/pve-bk-truenas-dr/dump/vzdump-qemu-100-*"

# CT 200
ssh pve-scratchy "ls -lh /mnt/pve/pve-bk-truenas-dr/dump/vzdump-lxc-200-*"
```

### Check Last Backup Time
```bash
ssh pve-scratchy "ls -lt /mnt/pve/pve-bk-truenas-dr/dump/vzdump-*.log | head -5"
```

### View Backup Job Log
```bash
ssh pve-scratchy "ls -lt /var/log/pve/tasks/ | head -10"
```

---

## Manual Backup

### Backup Single VM
```bash
ssh pve-scratchy "vzdump <VMID> --storage pve-bk-truenas-dr --compress zstd --mode snapshot"
```

### Backup Single CT
```bash
ssh pve-scratchy "vzdump <CTID> --storage pve-bk-truenas-dr --compress zstd --mode snapshot"
```

### Backup with Notes
```bash
ssh pve-scratchy "vzdump <VMID> --storage pve-bk-truenas-dr --compress zstd --mode snapshot --notes 'Pre-upgrade backup'"
```

---

## Restore Operations

### Verify Backup Integrity First
```bash
ssh pve-scratchy "vzdump info /mnt/pve/pve-bk-truenas-dr/dump/<backup_file>"
```

### Restore VM
```bash
# List available backups
ssh pve-scratchy "ls -lh /mnt/pve/pve-bk-truenas-dr/dump/vzdump-qemu-<VMID>-*"

# Restore (will overwrite existing VM with same ID)
ssh pve-scratchy "qmrestore /mnt/pve/pve-bk-truenas-dr/dump/vzdump-qemu-<VMID>-<date>.vma.zst <VMID>"

# Start after restore
ssh pve-scratchy "qm start <VMID>"

# Verify
ssh pve-scratchy "qm status <VMID>"
```

### Restore CT
```bash
ssh pve-scratchy "pct restore <CTID> /mnt/pve/pve-bk-truenas-dr/dump/vzdump-lxc-<CTID>-<date>.tar.zst"
ssh pve-scratchy "pct start <CTID>"
```

### Restore to Different ID
```bash
ssh pve-scratchy "qmrestore /mnt/pve/pve-bk-truenas-dr/dump/vzdump-qemu-100-<date>.vma.zst 999"
```

### Restore to Different Node
```bash
ssh pve-itchy "qmrestore /mnt/pve/pve-bk-truenas-dr/dump/vzdump-qemu-<VMID>-<date>.vma.zst <VMID>"
```

---

## Backup Schedule Management

### View Scheduled Backups
```bash
ssh pve-scratchy "pvesh get /cluster/backup --output-format json-pretty"
```

### Current Schedule
- **Time**: 02:45 AM daily
- **Compression**: zstd
- **Storage**: pve-bk-truenas-dr
- **Retention**: 7 daily + 1 monthly

---

## Retention Management

### Check Old Backups
```bash
ssh pve-scratchy "find /mnt/pve/pve-bk-truenas-dr/dump -name '*.vma.zst' -mtime +30 | wc -l"
```

### Clean Backups Older Than 30 Days (manual)
```bash
# List first
ssh pve-scratchy "find /mnt/pve/pve-bk-truenas-dr/dump -name '*.vma.zst' -mtime +30"

# Delete (confirm first!)
ssh pve-scratchy "find /mnt/pve/pve-bk-truenas-dr/dump -name '*.vma.zst' -mtime +30 -delete"
```

---

## Recovery Scenarios

### Single VM Failure
1. List backups: `ls /mnt/pve/pve-bk-truenas-dr/dump/vzdump-qemu-<VMID>-*`
2. Restore: `qmrestore <backup_file> <VMID>`
3. Start: `qm start <VMID>`
4. Verify: `qm status <VMID>`
5. **RTO**: 15-30 minutes, **RPO**: < 24 hours

### Primary Node Failure (pve-scratchy down)
1. Access pve-itchy: https://10.16.1.8:8006
2. Check quorum: `pvecm status` (should still have quorum with qnetd)
3. Restore VMs from NFS backups to pve-itchy
4. **RTO**: 2-4 hours, **RPO**: < 24 hours

### Catastrophic Failure
1. Restore from Backblaze B2 offsite
2. See `context/infrastructure-context.md` for full DR procedure
3. **RTO**: 1-2 days, **RPO**: < 24 hours

---

## Troubleshooting

### Backup Storage Full
```bash
ssh pve-scratchy "df -h /mnt/pve/pve-bk-truenas-dr"
ssh truenas-dr "zfs list -o name,quota,used,available"
```

### NFS Mount Missing
```bash
# Check mount
ssh pve-scratchy "mount | grep pve-bk-truenas-dr"

# Remount
ssh pve-scratchy "mount -a"

# Check TrueNAS DR is online
ping -c 1 10.16.1.20
```

### Backup Job Failed
```bash
ssh pve-scratchy << 'EOF'
echo "=== Recent Backup Tasks ==="
ls -lt /var/log/pve/tasks/ | head -10
echo ""
echo "=== Backup Storage ==="
df -h /mnt/pve/pve-bk-truenas-dr
echo ""
echo "=== NFS Status ==="
mount | grep truenas
EOF
```

---

## Related Skills

- **proxmox-cluster** - Cluster health affecting backups
- **proxmox-vm-management** - VM/CT operations post-restore
- **storage-management** - ZFS replication and TrueNAS management
- **monitoring-ops** - Backup monitoring alerts

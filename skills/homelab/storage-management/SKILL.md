---
name: storage-management
version: 1.0.0
description: When the user wants to manage storage -- ZFS pools, TrueNAS datasets, replication, NFS/SMB shares, or storage capacity. Also use when the user mentions "ZFS," "TrueNAS," "NFS," "SMB," "replication," "pool," "dataset," "snapshot," "quota," or "storage full." For Proxmox backup storage, see proxmox-backup-restore.
---

# Storage Management

You are an expert in ZFS and TrueNAS storage management.

## Storage Architecture

**Read `context/infrastructure-context.md` first** for the full storage topology.

| Host | IP | Pool | Key Datasets | Role |
|------|-----|------|-------------|------|
| TrueNAS Primary | 10.16.1.6 | Tank | FileServer (923GB) | Primary storage, NFS |
| TrueNAS DR | 10.16.1.20 | Tank | Data-DR-Copy | Replication target, backup NFS |
| gm-ai | 10.16.1.9 | homelab | ai-services (26.6G), docker (4.1G) | AI host storage |

## Guard Rails

**Auto-approve**: Status checks, listing datasets, viewing snapshots, checking replication
**Confirm first**: ZFS destroy, pool changes, dataset deletion, quota changes, snapshot purging

---

## ZFS Pool Status

### Check Pool Health (TrueNAS Primary)
```bash
ssh truenas-scale "zpool status"
```

### Check Pool Health (TrueNAS DR)
```bash
ssh truenas-dr "zpool status"
```

### Check Pool Health (gm-ai)
```bash
ssh gm-ai "sudo zpool status"
```

### List All Datasets
```bash
ssh truenas-scale "zfs list"
ssh truenas-dr "zfs list"
ssh gm-ai "sudo zfs list"
```

### Check Dataset Usage
```bash
ssh truenas-scale "zfs list -o name,quota,used,available,mountpoint Tank/FileServer"
```

---

## Snapshots

### List Snapshots
```bash
ssh truenas-scale "zfs list -t snapshot Tank/FileServer | tail -10"
```

### Create Manual Snapshot
```bash
ssh truenas-scale "zfs snapshot Tank/FileServer@manual-$(date +%Y%m%d-%H%M)"
```

### Browse Snapshot Contents
```bash
ssh truenas-scale "ls /mnt/Tank/FileServer/.zfs/snapshot/"
```

### Restore File from Snapshot
```bash
ssh truenas-scale "cp /mnt/Tank/FileServer/.zfs/snapshot/<snapshot_name>/<path_to_file> /mnt/Tank/FileServer/<path_to_file>"
```

### Delete Snapshot
```bash
# Confirm first!
ssh truenas-scale "zfs destroy Tank/FileServer@<snapshot_name>"
```

---

## ZFS Replication

### Check TrueNAS Replication Status
```bash
ssh truenas-scale "midclt call replication.query | jq '.[] | select(.name==\"FileServer-to-DR\") | {state, last_run: .state.datetime}'"
```

### Check gm-ai Replication Status
```bash
ssh gm-ai "sudo systemctl status zfs-replicate-dr.timer --no-pager"
ssh gm-ai "sudo tail -20 /var/log/zfs-replicate-dr.log"
```

### Compare Primary vs DR Snapshots
```bash
echo "=== Primary ===" && ssh truenas-scale "zfs list -t snapshot Tank/FileServer | tail -5"
echo "=== DR ===" && ssh truenas-dr "zfs list -t snapshot Tank/Data-DR-Copy/FileServer | tail -5"
```

### Compare gm-ai vs DR Snapshots
```bash
echo "=== gm-ai ===" && ssh gm-ai "sudo zfs list -t snapshot -r homelab | grep dr-daily | tail -5"
echo "=== DR ===" && ssh truenas-dr "zfs list -t snapshot -r Tank/Data-DR-Copy/gm-ai-homelab | grep dr-daily | tail -5"
```

### Trigger Manual Replication (TrueNAS)
```bash
ssh truenas-scale "midclt call replication.run 1"  # Run replication task ID 1
```

### Trigger Manual Replication (gm-ai)
```bash
ssh gm-ai "sudo /usr/local/bin/zfs-replicate-dr.sh"
```

---

## NFS Management

### Check NFS Exports (TrueNAS Primary)
```bash
ssh truenas-scale "showmount -e localhost"
```

### Check NFS Mount (Proxmox Backup Storage)
```bash
ssh pve-scratchy "df -h /mnt/pve/pve-bk-truenas-dr"
ssh pve-scratchy "mount | grep truenas"
```

### Remount NFS (if dropped)
```bash
ssh pve-scratchy "umount /mnt/pve/pve-bk-truenas-dr; mount -a"
```

---

## Quota Management

### Check Quotas
```bash
ssh truenas-dr "zfs list -o name,quota,used,available Tank/Data-DR-Copy"
```

### Increase Quota (if replication failing due to space)
```bash
ssh truenas-dr "zfs set quota=10T Tank/Data-DR-Copy/Downloads"
```

---

## Storage Capacity Monitoring

### Full Storage Overview
```bash
ssh truenas-scale << 'EOF'
echo "=== PRIMARY STORAGE ==="
echo "--- Pool Status ---"
zpool list
echo ""
echo "--- Key Datasets ---"
zfs list -o name,used,available,quota Tank/FileServer
echo ""
echo "--- FileServer Breakdown ---"
du -sh /mnt/Tank/FileServer/* 2>/dev/null
EOF
```

### DR Storage Overview
```bash
ssh truenas-dr << 'EOF'
echo "=== DR STORAGE ==="
zpool list
echo ""
zfs list -o name,used,available,quota -r Tank/Data-DR-Copy
EOF
```

---

## TrueNAS Config Backups

### Check Config Backups
```bash
ssh truenas-scale "ls -lh /mnt/Tank/FileServer/HomeLab/truenas-configs/"
```

### Manual Config Backup
```bash
ssh truenas-scale "cat /data/freenas-v1.db > /mnt/Tank/FileServer/HomeLab/truenas-configs/truenas-primary-config-$(date +%Y%m%d-%H%M%S).db"
```

---

## Troubleshooting

### Replication Failing
```bash
# Check TrueNAS replication
ssh truenas-scale "midclt call replication.query | jq '.[] | select(.name==\"FileServer-to-DR\") | .state'"

# Check DR quota
ssh truenas-dr "zfs list -o name,quota,used,available Tank/Data-DR-Copy/FileServer Tank/Data-DR-Copy/Downloads"

# Check network
ssh truenas-scale "ping -c 3 10.16.1.20"
```

### Pool Degraded
```bash
# Check pool status
ssh truenas-scale "zpool status -v"

# Check for errors
ssh truenas-scale "zpool status | grep -E 'DEGRADED|FAULTED|OFFLINE|UNAVAIL'"
```

### Storage Full
```bash
# Check what's using space
ssh truenas-scale "zfs list -o name,used,compressratio -s used -r Tank | tail -20"

# Check snapshot usage
ssh truenas-scale "zfs list -t snapshot -o name,used -s used -r Tank | tail -20"
```

---

## Related Skills

- **proxmox-backup-restore** - Proxmox backup to TrueNAS DR
- **monitoring-ops** - Data protection monitoring
- **linux-admin** - Host disk management

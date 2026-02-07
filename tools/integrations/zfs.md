# ZFS CLI

ZFS provides advanced filesystem and volume management via command-line tools. Used for storage pools, datasets, snapshots, and replication across TrueNAS and gm-ai hosts.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | N | No REST API (use TrueNAS API for TrueNAS hosts) |
| MCP | N | No MCP server available |
| CLI | Y | `zpool` and `zfs` command-line tools |
| SDK | Y | Python `libzfs`, Go `zfs` libraries (low-level) |

## Authentication

**CLI Access**: Requires root or sudo access on hosts with ZFS pools.

**Pool Permissions**: ZFS pools are root-owned. Dataset permissions follow standard Unix permissions.

**Replication**: Uses SSH for `zfs send/recv` operations. Requires SSH key authentication.

## Common Agent Operations

### Pool Status

```bash
# List all pools
zpool list

# Detailed pool status
zpool status

# Status for specific pool
zpool status Tank

# Pool health summary
zpool status -x
```

### Pool Information

```bash
# List pools with details
zpool list -v

# Get pool properties
zpool get all Tank

# Get specific property
zpool get health Tank
```

### Dataset Operations

```bash
# List all datasets
zfs list

# List datasets in pool
zfs list -r Tank

# List with snapshot info
zfs list -t all Tank/FileServer

# Get dataset properties
zfs get all Tank/FileServer

# Get specific property
zfs get used Tank/FileServer
```

### Create Dataset

```bash
# Create filesystem dataset
zfs create Tank/new-dataset

# Create with properties
zfs create -o compression=lz4 -o quota=100G Tank/new-dataset

# Create volume (block device)
zfs create -V 10G Tank/new-volume
```

### Snapshot Management

```bash
# Create snapshot
zfs snapshot Tank/FileServer@manual-20260208

# Create recursive snapshot
zfs snapshot -r Tank/FileServer@manual-20260208

# List snapshots
zfs list -t snapshot Tank/FileServer

# Destroy snapshot
zfs destroy Tank/FileServer@manual-20260208

# Destroy recursive snapshots
zfs destroy -r Tank/FileServer@manual-20260208
```

### Snapshot Replication (Send/Receive)

```bash
# Send snapshot to remote host
zfs send Tank/FileServer@snapshot-20260208 | \
  ssh truenas-dr "zfs receive Tank/Data-DR-Copy/FileServer"

# Incremental send (from previous snapshot)
zfs send -i Tank/FileServer@previous Tank/FileServer@current | \
  ssh truenas-dr "zfs receive Tank/Data-DR-Copy/FileServer"

# Send with compression
zfs send -c Tank/FileServer@snapshot | \
  ssh truenas-dr "zfs receive Tank/Data-DR-Copy/FileServer"
```

### Dataset Properties

```bash
# Set property
zfs set compression=lz4 Tank/FileServer

# Set quota
zfs set quota=500G Tank/FileServer

# Set reservation
zfs set reservation=100G Tank/FileServer

# Get property
zfs get compression Tank/FileServer
```

### Pool Scrub

```bash
# Start scrub
zpool scrub Tank

# Check scrub status
zpool status Tank

# Cancel scrub
zpool scrub -s Tank
```

### Destroy Dataset

```bash
# Destroy dataset (WARNING: irreversible)
zfs destroy Tank/old-dataset

# Destroy with snapshots
zfs destroy -r Tank/old-dataset

# Force destroy (if mounted)
zfs destroy -f Tank/old-dataset
```

### Replication Script Example

```bash
# Example: Replicate dataset to DR host
SOURCE_POOL="homelab"
SOURCE_DATASET="homelab"
DEST_HOST="truenas-dr"
DEST_POOL="Tank"
DEST_DATASET="Data-DR-Copy/gm-ai-homelab"

# Get latest snapshot
LATEST_SNAP=$(zfs list -t snapshot -o name -S creation \
  $SOURCE_POOL/$SOURCE_DATASET | head -n 1 | cut -d'@' -f2)

# Send incremental
zfs send -i $SOURCE_POOL/$SOURCE_DATASET@previous \
  $SOURCE_POOL/$SOURCE_DATASET@$LATEST_SNAP | \
  ssh $DEST_HOST "zfs receive $DEST_POOL/$DEST_DATASET"
```

## Key Objects/Metrics

- **Pools**: Storage pools (Tank on TrueNAS, homelab on gm-ai)
- **Datasets**: Filesystems or volumes within pools
- **Snapshots**: Point-in-time copies of datasets
- **Properties**: Compression, quota, reservation, encryption, etc.
- **Health**: Pool health status (ONLINE, DEGRADED, FAULTED)
- **Scrub**: Data integrity verification process

## When to Use

- **Storage management**: Check pool health, dataset usage, available space
- **Snapshot operations**: Create manual snapshots, verify automated snapshots
- **Replication**: Set up or verify ZFS replication between hosts
- **Troubleshooting**: Diagnose pool errors, check scrub status
- **Backup verification**: Verify snapshots exist, check replication status
- **Direct host operations**: Operations on gm-ai or TrueNAS hosts (not via API)

## Rate Limits

No rate limits. ZFS operations:
- Are synchronous (block until complete)
- Can take time for large datasets (scrub, send/recv)
- Use system resources (CPU, memory, disk I/O)

## Relevant Skills

- `storage-management` - Pool and dataset operations
- `proxmox-backup-restore` - Snapshot and replication verification
- `monitoring-ops` - Pool health and dataset usage monitoring
- `data-protection` - Snapshot and replication management

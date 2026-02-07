# TrueNAS SCALE API

TrueNAS SCALE API provides REST access to manage storage pools, datasets, snapshots, replication, and system configuration. Also supports `midclt` CLI for local operations.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `https://<host>/api/v2.0/`, requires API key |
| MCP | N | No MCP server available |
| CLI | Y | `midclt` command-line tool (local only, runs on TrueNAS host) |
| SDK | Y | Python `truenas-client`, JavaScript libraries available |

## Authentication

**API Key**: Generate in TrueNAS Web UI (System → API Keys). Format: `api_key:api_secret`.

```bash
# Use API key in Authorization header
curl -k -H "Authorization: Bearer api_key:api_secret" \
  https://10.16.1.6/api/v2.0/pool

# Or use basic auth format
curl -k -u "api_key:api_secret" \
  https://10.16.1.6/api/v2.0/pool
```

**midclt CLI**: Runs locally on TrueNAS host, uses system authentication.

```bash
# SSH to TrueNAS and use midclt
ssh truenas-scale "midclt call pool.query"
```

## Common Agent Operations

### Get Pool Status

```bash
# Via REST API
curl -k -H "Authorization: Bearer api_key:api_secret" \
  https://10.16.1.6/api/v2.0/pool

# Via midclt (on TrueNAS host)
ssh truenas-scale "midclt call pool.query"
```

### List Datasets

```bash
# Via REST API
curl -k -H "Authorization: Bearer api_key:api_secret" \
  https://10.16.1.6/api/v2.0/pool/dataset

# Via midclt
ssh truenas-scale "midclt call pool.dataset.query"
```

### Get Dataset Details

```bash
# Via REST API
curl -k -H "Authorization: Bearer api_key:api_secret" \
  "https://10.16.1.6/api/v2.0/pool/dataset/id/Tank%2FFileServer"

# Via midclt
ssh truenas-scale "midclt call pool.dataset.query [['id', '=', 'Tank/FileServer']]"
```

### List Snapshots

```bash
# Via REST API
curl -k -H "Authorization: Bearer api_key:api_secret" \
  "https://10.16.1.6/api/v2.0/pool/snapshot?dataset=Tank/FileServer"

# Via midclt
ssh truenas-scale "midclt call pool.snapshot.query [['dataset', '=', 'Tank/FileServer']]"
```

### Create Snapshot

```bash
# Via REST API
curl -k -X POST -H "Authorization: Bearer api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"dataset": "Tank/FileServer", "name": "manual-20260208", "recursive": false}' \
  https://10.16.1.6/api/v2.0/pool/snapshot

# Via midclt
ssh truenas-scale "midclt call pool.snapshot.create '{\"dataset\": \"Tank/FileServer\", \"name\": \"manual-20260208\", \"recursive\": false}'"
```

### Query Replication Tasks

```bash
# Via REST API
curl -k -H "Authorization: Bearer api_key:api_secret" \
  https://10.16.1.6/api/v2.0/replication

# Via midclt
ssh truenas-scale "midclt call replication.query"
```

### Get System Information

```bash
# Via REST API
curl -k -H "Authorization: Bearer api_key:api_secret" \
  https://10.16.1.6/api/v2.0/system/info

# Via midclt
ssh truenas-scale "midclt call system.info"
```

### Get NFS Share Status

```bash
# Via REST API
curl -k -H "Authorization: Bearer api_key:api_secret" \
  https://10.16.1.6/api/v2.0/sharing/nfs

# Via midclt
ssh truenas-scale "midclt call sharing.nfs.query"
```

## Key Objects/Metrics

- **Pools**: ZFS storage pools (Tank on both TrueNAS hosts)
- **Datasets**: Filesystems within pools (Tank/FileServer, Tank/Data-DR-Copy)
- **Snapshots**: Point-in-time copies (used for replication and backups)
- **Replication**: Tasks syncing datasets between TrueNAS hosts
- **NFS Shares**: Exported filesystems (FileServer to Proxmox hosts)
- **System Info**: CPU, memory, disk usage, uptime

## When to Use

- **Storage monitoring**: Check pool health, dataset usage, available space
- **Snapshot management**: Create manual snapshots, verify automated snapshots
- **Replication verification**: Check replication task status, verify DR sync
- **Backup validation**: Verify backup storage availability and capacity
- **NFS management**: Query NFS share status, verify exports

## Rate Limits

No explicit rate limits documented. TrueNAS recommends:
- Avoid rapid API calls (< 500ms between requests)
- Use pagination for large result sets
- Cache system info queries; they're expensive

## Relevant Skills

- `storage-management` - Pool and dataset operations
- `proxmox-backup-restore` - Backup storage verification
- `monitoring-ops` - Storage health monitoring
- `data-protection` - Replication and snapshot verification

# Proxmox VE API

Proxmox VE API provides programmatic access to manage VMs, containers, clusters, storage, and backups. Supports both REST API and CLI (`pvesh`) interfaces.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `https://<node>:8006/api2/json/`, requires authentication |
| MCP | N | No MCP server available |
| CLI | Y | `pvesh` command-line tool, wraps API calls |
| SDK | Y | Python `proxmoxer`, JavaScript `proxmox-client`, Go `proxmox-api-go` |

## Authentication

**PVE Ticket**: Cookie-based auth via `/api2/json/access/ticket` endpoint. Username/password required.

```bash
# Get ticket via API
curl -k -d 'username=root@pam&password=yourpass' \
  https://10.16.1.22:8006/api2/json/access/ticket

# Response includes ticket and CSRF token
# Use ticket as cookie: PVEAuthCookie=<ticket>
# Use CSRF token in header: CSRFPreventionToken: <token>
```

**API Token**: Token-based auth (preferred for automation). Format: `token-id@realm!token-name=secret`.

```bash
# Use token in Authorization header
curl -k -H "Authorization: PVEAPIToken=root@pam!monitoring=abc123..." \
  https://10.16.1.22:8006/api2/json/cluster/resources
```

**CLI Auth**: `pvesh` uses `~/.proxmox-auth` or environment variables `PROXMOX_USER` and `PROXMOX_PASSWORD`.

## Common Agent Operations

### Get Cluster Status

```bash
# Via CLI
pvesh get /cluster/status

# Via REST API
curl -k -H "Authorization: PVEAPIToken=..." \
  https://10.16.1.22:8006/api2/json/cluster/status
```

### List All Resources (VMs, CTs, Nodes)

```bash
# Via CLI
pvesh get /cluster/resources --type vm --type lxc --type node

# Via REST API
curl -k -H "Authorization: PVEAPIToken=..." \
  "https://10.16.1.22:8006/api2/json/cluster/resources?type=vm&type=lxc&type=node"
```

### Get Node Information

```bash
# Via CLI
pvesh get /nodes/pve-scratchy/status

# Via REST API
curl -k -H "Authorization: PVEAPIToken=..." \
  https://10.16.1.22:8006/api2/json/nodes/pve-scratchy/status
```

### List VMs/CTs on Node

```bash
# Via CLI
pvesh get /nodes/pve-scratchy/qemu
pvesh get /nodes/pve-scratchy/lxc

# Via REST API
curl -k -H "Authorization: PVEAPIToken=..." \
  https://10.16.1.22:8006/api2/json/nodes/pve-scratchy/qemu
```

### Start/Stop/Restart VM

```bash
# Via CLI
pvesh create /nodes/pve-scratchy/qemu/100/status/start
pvesh create /nodes/pve-scratchy/qemu/100/status/stop
pvesh create /nodes/pve-scratchy/qemu/100/status/reset

# Via REST API
curl -k -X POST -H "Authorization: PVEAPIToken=..." \
  https://10.16.1.22:8006/api2/json/nodes/pve-scratchy/qemu/100/status/start
```

### Execute Command in Container

```bash
# Via CLI (pct on node)
ssh pve-scratchy "pct exec 200 -- bash -c 'systemctl status nginx'"

# Via API (requires guest agent)
curl -k -X POST -H "Authorization: PVEAPIToken=..." \
  -d 'command=bash&args=-c,uptime' \
  https://10.16.1.22:8006/api2/json/nodes/pve-scratchy/qemu/100/agent/exec
```

### List Storage

```bash
# Via CLI
pvesh get /nodes/pve-scratchy/storage

# Via REST API
curl -k -H "Authorization: PVEAPIToken=..." \
  https://10.16.1.22:8006/api2/json/nodes/pve-scratchy/storage
```

### Backup Operations

```bash
# List backup jobs
pvesh get /nodes/pve-scratchy/vzdump

# Create backup
curl -k -X POST -H "Authorization: PVEAPIToken=..." \
  -d 'vmid=100&storage=pve-bk-truenas-dr&compress=zstd' \
  https://10.16.1.22:8006/api2/json/nodes/pve-scratchy/vzdump
```

## Key Objects/Metrics

- **Nodes**: Cluster members (pve-scratchy, pve-itchy)
- **VMs**: QEMU/KVM virtual machines (VMID 100+)
- **CTs**: LXC containers (CTID 100+)
- **Storage**: Local, NFS, ZFS pools
- **Backups**: vzdump snapshots stored on storage
- **Cluster**: Quorum status, HA groups, resources

## When to Use

- **Cluster monitoring**: Check node status, resource usage, quorum health
- **VM/CT lifecycle**: Start, stop, restart, migrate workloads
- **Backup management**: Create backups, verify backup jobs, check retention
- **Storage operations**: List storage, check capacity, manage snapshots
- **Automation**: Integrate Proxmox operations into scripts and monitoring

## Rate Limits

No explicit rate limits documented. Proxmox recommends:
- Avoid rapid-fire API calls (< 1 second between requests)
- Use connection pooling for multiple requests
- Monitor API response times; slow responses indicate overload

## Relevant Skills

- `proxmox-cluster` - Cluster management and HA operations
- `proxmox-backup-restore` - Backup creation and restoration
- `proxmox-networking` - Network configuration and troubleshooting
- `monitoring-ops` - Infrastructure health monitoring

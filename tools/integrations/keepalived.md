# Keepalived

Keepalived provides high availability via VRRP (Virtual Router Redundancy Protocol) for VIP (Virtual IP) management. Used for Pi-hole DNS HA failover.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | N | No REST API available |
| MCP | N | No MCP server available |
| CLI | Y | `systemctl` for service management, `ip` for VIP monitoring |
| SDK | N | No SDK available |

## Authentication

**Service Management**: Requires root or sudo access on hosts running Keepalived.

**Configuration**: Config file at `/etc/keepalived/keepalived.conf` (root-owned, 644 permissions).

**VRRP Protocol**: Uses multicast (224.0.0.18) for VRRP advertisements. No authentication by default (can enable VRRP authentication in config).

## Common Agent Operations

### Check Service Status

```bash
# Check if Keepalived is running
ssh piholed "systemctl status keepalived"

# Check on all Pi-hole hosts
for host in piholed 10.16.1.15 10.16.1.16 10.16.1.18; do
  ssh $host "systemctl status keepalived --no-pager"
done
```

### Start/Stop/Restart Service

```bash
# Start Keepalived
ssh piholed "systemctl start keepalived"

# Stop Keepalived
ssh piholed "systemctl stop keepalived"

# Restart Keepalived
ssh piholed "systemctl restart keepalived"

# Reload configuration (without restart)
ssh piholed "systemctl reload keepalived"
```

### Check VIP Status

```bash
# Check if VIP is active on host
ssh piholed "ip addr show | grep 10.16.1.15"

# Or use specific interface
ssh piholed "ip addr show eth0 | grep 10.16.1.15"

# Check VIP on all hosts
for host in piholed 10.16.1.16 10.16.1.18; do
  echo "=== $host ==="
  ssh $host "ip addr show | grep 10.16.1.15 || echo 'VIP not present'"
done
```

### View Configuration

```bash
# View Keepalived config
ssh piholed "cat /etc/keepalived/keepalived.conf"

# Validate config syntax
ssh piholed "keepalived -t -f /etc/keepalived/keepalived.conf"
```

### Check VRRP Status

```bash
# View VRRP status (if available in logs)
ssh piholed "journalctl -u keepalived -n 50 --no-pager"

# Real-time log monitoring
ssh piholed "journalctl -u keepalived -f"
```

### Verify Failover

```bash
# Check current master
for host in piholed 10.16.1.16 10.16.1.18; do
  vip_status=$(ssh $host "ip addr show | grep -c '10.16.1.15' || echo '0'")
  if [ "$vip_status" -gt "0" ]; then
    echo "$host is MASTER (VIP active)"
  else
    echo "$host is BACKUP (VIP not active)"
  fi
done
```

### Test Failover

```bash
# Stop Keepalived on master to trigger failover
ssh piholed "systemctl stop keepalived"

# Wait a few seconds, then check VIP moved to backup
sleep 5
ssh 10.16.1.16 "ip addr show | grep 10.16.1.15"

# Restore master
ssh piholed "systemctl start keepalived"
```

## Key Objects/Metrics

- **VIP**: Virtual IP address (e.g., 10.16.1.15 for Pi-hole HA)
- **VRRP State**: MASTER (owns VIP) or BACKUP (standby)
- **Priority**: VRRP priority (higher = more likely to be master)
- **Health Checks**: Scripts that determine if host should hold VIP
- **VRRP Group**: Group of hosts participating in failover

## When to Use

- **HA verification**: Check which host currently holds the VIP
- **Failover testing**: Verify automatic failover works correctly
- **Troubleshooting**: Diagnose why VIP isn't moving or staying on wrong host
- **Service management**: Start/stop Keepalived for maintenance
- **Configuration updates**: Modify VRRP settings, priorities, health checks

## Rate Limits

No rate limits. Keepalived:
- Sends VRRP advertisements every few seconds
- Responds to state changes immediately
- Health checks run at configured intervals (typically 1-5 seconds)

## Relevant Skills

- `dns-management` - Pi-hole HA failover verification
- `monitoring-ops` - VIP status monitoring and failover health
- `linux-networking` - VRRP configuration and troubleshooting

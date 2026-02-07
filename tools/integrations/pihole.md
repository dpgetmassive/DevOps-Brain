# Pi-hole API

Pi-hole provides DNS filtering and management via REST API and CLI tools. Used for ad blocking, custom DNS records, and DNS query management across the homelab.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `http://<host>/admin/api.php`, no auth required (local network) |
| MCP | N | No MCP server available |
| CLI | Y | `pihole` command-line tool, config files at `/etc/pihole/` |
| SDK | N | No official SDK, use REST API directly |

## Authentication

**REST API**: No authentication required for local network access. API endpoints are public within the network.

**Web UI**: Password protected at `http://<host>/admin/`. Password stored in `/etc/pihole/setupVars.conf` (`WEBPASSWORD`).

**CLI**: Requires root or sudo access on Pi-hole host.

## Common Agent Operations

### Get Statistics

```bash
# Via REST API
curl "http://10.16.1.15/admin/api.php?summary"

# Response includes:
# - domains_being_blocked
# - dns_queries_today
# - ads_blocked_today
# - ads_percentage_today
# - unique_clients
```

### Get Query Log

```bash
# Recent queries (last 100)
curl "http://10.16.1.15/admin/api.php?getQueryTypes&auth=<webpassword>"

# Top blocked domains
curl "http://10.16.1.15/admin/api.php?topBlocked&auth=<webpassword>"
```

### Enable/Disable Pi-hole

```bash
# Disable blocking (for troubleshooting)
curl "http://10.16.1.15/admin/api.php?disable=300&auth=<webpassword>"
# Disables for 300 seconds (5 minutes)

# Enable blocking
curl "http://10.16.1.15/admin/api.php?enable&auth=<webpassword>"

# Via CLI
ssh piholed "pihole disable 300"
ssh piholed "pihole enable"
```

### Update Gravity (Block Lists)

```bash
# Via CLI
ssh piholed "pihole -g"

# Via API (triggers update)
curl -X POST "http://10.16.1.15/admin/api.php?updateGravity&auth=<webpassword>"
```

### Add Custom DNS Record

```bash
# Via CLI (adds to /etc/pihole/custom.list)
ssh piholed "pihole -a customdns example.local 10.16.1.50"

# Via config file edit
ssh piholed "echo '10.16.1.50 example.local' >> /etc/pihole/custom.list"
ssh piholed "pihole restartdns"
```

### List Custom DNS Records

```bash
# Via CLI
ssh piholed "pihole -q customdns"

# Via config file
ssh piholed "cat /etc/pihole/custom.list"
```

### Get Client List

```bash
# Via REST API
curl "http://10.16.1.15/admin/api.php?clients&auth=<webpassword>"
```

### Get DNS Query Types

```bash
# Via REST API
curl "http://10.16.1.15/admin/api.php?getQueryTypes&auth=<webpassword>"
```

### Restart DNS Service

```bash
# Via CLI
ssh piholed "pihole restartdns"

# Or via systemctl
ssh piholed "systemctl restart pihole-FTL"
```

## Key Objects/Metrics

- **DNS Queries**: Total queries processed, blocked queries, allowed queries
- **Block Lists**: Gravity database with blocked domains
- **Custom DNS**: Local DNS records (custom.list)
- **Clients**: Devices using Pi-hole for DNS resolution
- **Query Types**: Breakdown by A, AAAA, PTR, etc.
- **Top Domains**: Most queried domains, most blocked domains

## When to Use

- **DNS troubleshooting**: Check query logs, verify DNS resolution
- **Ad blocking management**: Enable/disable blocking, update block lists
- **Custom DNS records**: Add local domain records (e.g., services.gmdojo.tech)
- **Monitoring**: Track DNS query volume, blocked ads, client activity
- **Service discovery**: Verify DNS records for homelab services

## Rate Limits

No explicit rate limits. Pi-hole handles:
- High query volumes (thousands per second)
- API requests are lightweight
- Gravity updates may take 1-2 minutes

## Relevant Skills

- `dns-management` - DNS record creation and management
- `monitoring-ops` - DNS query monitoring and troubleshooting
- `linux-networking` - DNS configuration and troubleshooting

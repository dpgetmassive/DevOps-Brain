# Tailscale CLI and API

Tailscale provides mesh VPN and secure remote access via CLI (`tailscale`) and Admin API (`api.tailscale.com`). Used for VPN connectivity, subnet routing, exit nodes, and ACL management across homelab nodes.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | Admin API at `https://api.tailscale.com/api/v2/`, requires API key |
| MCP | N | No MCP server available |
| CLI | Y | `tailscale` command-line tool for local node operations |
| SDK | Y | Go SDK available, REST API can be used from any language |

## Authentication

**CLI**: Uses local Tailscale daemon authentication. No explicit auth needed for local commands.

**Admin API**: Requires API key from Tailscale admin console. Set via `TAILSCALE_API_KEY` environment variable.

```bash
# Set API key
export TAILSCALE_API_KEY=tskey-api-xxxxxxxxxxxx

# Use in API calls
curl -H "Authorization: Bearer $TAILSCALE_API_KEY" \
  https://api.tailscale.com/api/v2/tailnet/your-tailnet/devices
```

**Tailnet**: Homelab uses Tailscale tailnet for mesh VPN. Nodes authenticate via MagicDNS.

## Common Agent Operations

### Check Status

```bash
# Check Tailscale status (all nodes)
tailscale status

# Check status on remote node
ssh pve-scratchy "pct exec 901 -- tailscale status"

# Get local node IP
tailscale ip -4

# Get status on specific node
ssh pve-scratchy "pct exec 901 -- tailscale ip -4"
```

### Node and Route Management

```bash
# List all nodes (via API)
curl -H "Authorization: Bearer $TAILSCALE_API_KEY" \
  https://api.tailscale.com/api/v2/tailnet/your-tailnet/devices

# Enable subnet routes
tailscale up --advertise-routes=10.16.1.0/24

# Accept routes (on client)
tailscale up --accept-routes=true

# Advertise as exit node
tailscale up --advertise-exit-node

# Use exit node
tailscale up --exit-node=<node-name>

# View ACL policy (via API)
curl -H "Authorization: Bearer $TAILSCALE_API_KEY" \
  https://api.tailscale.com/api/v2/tailnet/your-tailnet/acl
```

### Homelab Nodes

```bash
# Check tailscaler (CT 901)
ssh pve-scratchy "pct exec 901 -- tailscale status"

# Check cp-tailscale (CT 117)
ssh pve-scratchy "pct exec 117 -- tailscale status"

# Restart Tailscale service
ssh pve-scratchy "pct exec 901 -- systemctl restart tailscaled"

# Check Tailscale IPs
ssh pve-scratchy "pct exec 901 -- tailscale ip -4"
```

## Key Objects/Metrics

- **Nodes**: Devices in Tailscale mesh network
- **Routes**: Subnet routes advertised and accepted
- **Exit Nodes**: Nodes that can route traffic to internet
- **ACLs**: Access control lists defining network policies
- **MagicDNS**: Automatic DNS resolution for Tailscale nodes
- **Keys**: Authentication keys for node access

## When to Use

- **Remote access**: Connect to homelab services via Tailscale VPN
- **Subnet routing**: Route traffic to homelab subnets (10.16.1.0/24)
- **Exit node configuration**: Route internet traffic through homelab
- **Network troubleshooting**: Check node connectivity, verify routes
- **ACL management**: Configure access policies for Tailscale network
- **Service discovery**: Use MagicDNS to resolve homelab services

## Rate Limits

**Admin API**: 120 requests/minute per API key
**CLI**: No explicit rate limits (uses local daemon)

Rate limit headers:
- `X-Rate-Limit-Limit`: Requests per minute
- `X-Rate-Limit-Remaining`: Requests remaining
- `X-Rate-Limit-Reset`: Unix timestamp when limit resets

```bash
# Check rate limit (in response headers)
curl -I -H "Authorization: Bearer $TAILSCALE_API_KEY" \
  https://api.tailscale.com/api/v2/tailnet/your-tailnet/devices
```

## Relevant Skills

- `linux-networking` - Tailscale CLI operations and troubleshooting
- `monitoring-ops` - VPN connectivity monitoring
- `linux-admin` - Tailscale service management
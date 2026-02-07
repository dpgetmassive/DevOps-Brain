# Cloudflare API and CLI

Cloudflare provides DNS, CDN, and security services via REST API (`api.cloudflare.com`) and Wrangler CLI (`wrangler`). Used for DNS record management, Cloudflare Tunnels, Page Rules, and SSL/TLS certificate automation.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `https://api.cloudflare.com/client/v4/`, requires API token |
| MCP | N | No MCP server available |
| CLI | Y | `wrangler` CLI for Workers, Pages, and Tunnels; `cloudflared` for tunnels |
| SDK | Y | Official SDKs for Python, JavaScript, Go, Rust |

## Authentication

**API Token**: Create token in Cloudflare dashboard (My Profile > API Tokens). Set via `CLOUDFLARE_API_TOKEN` environment variable.

```bash
# Set API token
export CLOUDFLARE_API_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Use in API calls
curl -X GET \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  https://api.cloudflare.com/client/v4/zones
```

**Email + Global API Key**: Legacy auth method. Use `X-Auth-Email` and `X-Auth-Key` headers.

**Wrangler**: Authenticate via `wrangler login` (browser-based) or `wrangler config` (API token).

```bash
# Login interactively
wrangler login

# Configure with API token
wrangler config
```

## Common Agent Operations

### DNS Records and Tunnels

```bash
# List DNS records
curl -X GET \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/<zone-id>/dns_records"

# Create DNS record
curl -X POST \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"A","name":"example","content":"10.16.1.50","ttl":3600}' \
  "https://api.cloudflare.com/client/v4/zones/<zone-id>/dns_records"

# Get tunnel info (uptime-gm-hq)
ssh pve-scratchy "pct exec 114 -- cloudflared tunnel info uptime-gm-hq"

# Check tunnel status
ssh pve-scratchy "pct exec 114 -- cloudflared tunnel status"

# View tunnel routes
cloudflared tunnel route dns list
```

### Zones and SSL

```bash
# List zones
curl -X GET \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  https://api.cloudflare.com/client/v4/zones

# Get zone ID by name
curl -X GET \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones?name=example.com" | jq -r '.result[0].id'

# Check certificate status
curl -X GET \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/zones/<zone-id>/ssl/universal/settings"
```

### DNS Challenge for Traefik

Traefik uses Cloudflare DNS challenge for Let's Encrypt wildcard certificates:

```bash
# Verify DNS API token works
curl -X GET \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  "https://api.cloudflare.com/client/v4/user/tokens/verify"

# Traefik config uses CLOUDFLARE_DNS_API_TOKEN environment variable
# Certificates auto-renew via ACME DNS challenge
```

## Key Objects/Metrics

- **Zones**: DNS zones (domains) managed in Cloudflare
- **DNS Records**: A, AAAA, CNAME, MX, TXT records
- **Tunnels**: Cloudflare Tunnel connections (cloudflared CT 114)
- **Certificates**: SSL/TLS certificates (Let's Encrypt via DNS challenge)

## When to Use

- **DNS management**: Create/update/delete DNS records for homelab services
- **Tunnel management**: Monitor Cloudflare Tunnel status (uptime-gm-hq)
- **SSL automation**: DNS challenge for Let's Encrypt wildcard certificates
- **Service exposure**: Expose homelab services via Cloudflare Tunnel

## Rate Limits

**API**: 1,200 requests per 5 minutes per API token
**Rate limit headers**:
- `X-RateLimit-Limit`: Requests per time window
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Unix timestamp when limit resets

```bash
# Check rate limit (in response headers)
curl -I -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  https://api.cloudflare.com/client/v4/zones
```

**Best practices**: Cache zone IDs to reduce API calls, batch operations when possible

## Relevant Skills

- `reverse-proxy-management` - Cloudflare Tunnel and DNS configuration
- `ssl-certificate-management` - Let's Encrypt via Cloudflare DNS challenge
- `dns-management` - External DNS record management
- `monitoring-ops` - Tunnel and DNS health monitoring
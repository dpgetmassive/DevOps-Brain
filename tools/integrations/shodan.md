# Shodan Internet Search Engine

Shodan is a search engine for internet-connected devices and services. Provides OSINT capabilities to discover exposed services, vulnerabilities, and infrastructure information via REST API and CLI tool.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `https://api.shodan.io/`, JSON responses |
| MCP | N | No MCP server available |
| CLI | Y | `shodan` command-line tool (`pip install shodan`) |
| SDK | Y | Python `shodan`, Go `github.com/shodan/shodan-go` |

## Authentication

**API Key**: Required for all API requests. Get free API key at https://account.shodan.io/. Set via environment variable or CLI init.

```bash
# Initialize CLI with API key
shodan init YOUR_API_KEY

# Set environment variable
export SHODAN_API_KEY=YOUR_API_KEY

# Use in API requests
curl "https://api.shodan.io/shodan/host/8.8.8.8?key=YOUR_API_KEY"
```

**Rate Limits**: Free tier: 1 query/second. Paid plans: Higher limits (Member: 10/sec, Corporate: 100/sec).

## Common Agent Operations

### CLI Installation

```bash
# Install Shodan CLI
pip install shodan

# Initialize with API key
shodan init YOUR_API_KEY

# Verify API key
shodan info
```

### Host Information

```bash
# Get host information via CLI
shodan host 8.8.8.8

# Get host information via API
curl "https://api.shodan.io/shodan/host/8.8.8.8?key=YOUR_API_KEY"

# Get host information with history
shodan host --history 8.8.8.8
```

### Search Queries

```bash
# Search via CLI
shodan search "nginx"

# Search with filters
shodan search "nginx country:US"

# Search with output format
shodan search --fields ip_str,port,hostnames "nginx" --limit 10

# Search via API
curl "https://api.shodan.io/shodan/host/search?key=YOUR_API_KEY&query=nginx"
```

### DNS and IP Operations

```bash
# Resolve hostname
shodan domain example.com
curl "https://api.shodan.io/dns/resolve?key=YOUR_API_KEY&hostnames=example.com"

# Reverse DNS lookup
curl "https://api.shodan.io/dns/reverse?key=YOUR_API_KEY&ips=8.8.8.8"

# Get your public IP
shodan myip
```

### Alert Management

```bash
# Create alert for IP
shodan alert create "Homelab Monitor" 10.16.1.0/24

# List and manage alerts
shodan alert list
shodan alert info ALERT_ID
shodan alert delete ALERT_ID
```

### Common Search Filters

```bash
# Search by product, country, port, organization
shodan search "product:nginx"
shodan search "country:US nginx"
shodan search "port:443 ssl"
shodan search "org:Google"
```

## Key Objects/Metrics

- **Hosts**: IP addresses with open ports and services
- **Services**: Running services (HTTP, SSH, FTP, etc.) with banners
- **Products**: Software products detected (nginx, Apache, OpenSSH, etc.)
- **Vulnerabilities**: CVEs and security issues associated with hosts
- **Geolocation**: Country, city, and coordinates for IPs
- **Banners**: Service banners revealing version and configuration info
- **Alerts**: Notifications for IP changes or new services

## When to Use

- **OSINT reconnaissance**: Discover exposed services and infrastructure
- **Security research**: Identify vulnerable systems and misconfigurations
- **Asset discovery**: Find internet-facing assets and services
- **Threat intelligence**: Monitor for exposed credentials, databases, or services
- **Compliance checks**: Verify what's exposed to the internet from your infrastructure
- **Network mapping**: Understand external attack surface

## Rate Limits

Rate limits depend on subscription plan:
- **Free**: 1 query/second, 100 results/month
- **Member ($59/month)**: 10 queries/second, unlimited results
- **Corporate**: 100 queries/second, unlimited results

Respect rate limits to avoid API key suspension. Use `--limit` flag to control result count.

## Relevant Skills

- `osint-recon` - OSINT reconnaissance and information gathering
- `smb1001-security-ops` - Security operations and threat intelligence
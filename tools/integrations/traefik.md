# Traefik API

Traefik provides reverse proxy and load balancing with dynamic configuration via REST API and dashboard. Used for routing auth services and managing SSL certificates.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `http://<host>:8080/api/`, dashboard at `http://<host>:8080/dashboard/` |
| MCP | N | No MCP server available |
| CLI | N | No CLI tool, configuration via files or API |
| SDK | Y | Go SDK available, Python/JavaScript libraries exist |

## Authentication

**API/Dashboard**: No authentication by default. Traefik recommends:
- Restrict access via firewall (local network only)
- Enable basic auth middleware for production
- Use IP whitelisting

**Configuration**: Traefik reads config from:
- File: `/etc/traefik/traefik.yml` (static config)
- Docker labels: Dynamic routing from container labels
- API: REST API for dynamic configuration

## Common Agent Operations

### Get API Overview

```bash
# List all API endpoints
curl http://10.16.1.26:8080/api/overview

# Get version info
curl http://10.16.1.26:8080/api/version
```

### List Routers

```bash
# Get all HTTP routers
curl http://10.16.1.26:8080/api/http/routers

# Get specific router
curl http://10.16.1.26:8080/api/http/routers/<router-name>
```

### List Services

```bash
# Get all HTTP services
curl http://10.16.1.26:8080/api/http/services

# Get specific service
curl http://10.16.1.26:8080/api/http/services/<service-name>
```

### List Middlewares

```bash
# Get all HTTP middlewares
curl http://10.16.1.26:8080/api/http/middlewares

# Common middlewares: auth, headers, redirect, rate-limit
```

### List Entrypoints

```bash
# Get all entrypoints
curl http://10.16.1.26:8080/api/http/entrypoints

# Common entrypoints: web (80), websecure (443)
```

### Get TLS Certificates

```bash
# List TLS certificates
curl http://10.16.1.26:8080/api/http/routers | jq '.[] | select(.tls != null)'

# Check ACME/Let's Encrypt certificates
curl http://10.16.1.26:8080/api/http/routers | jq '.[] | .tls.certResolver'
```

### Get Service Health

```bash
# Check if service is responding
curl http://10.16.1.26:8080/api/http/services/<service-name>

# Response includes server status, load balancing info
```

### Dynamic Configuration (API)

```bash
# Add HTTP router via API
curl -X POST http://10.16.1.26:8080/api/http/routers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "example-router",
    "rule": "Host(`example.local`)",
    "service": "example-service",
    "entryPoints": ["websecure"],
    "tls": {
      "certResolver": "letsencrypt"
    }
  }'
```

### View Dashboard

```bash
# Dashboard available at
http://10.16.1.26:8080/dashboard/

# Shows real-time routing, services, middlewares
```

## Key Objects/Metrics

- **Routers**: Request routing rules (Host, Path, Headers)
- **Services**: Backend services (load balancing, health checks)
- **Middlewares**: Request/response modifiers (auth, headers, redirects)
- **Entrypoints**: Network entry points (ports 80, 443)
- **TLS**: SSL/TLS certificates (Let's Encrypt via ACME)
- **Providers**: Configuration sources (file, docker, kubernetes)

## When to Use

- **Routing inspection**: Verify routes, check service endpoints
- **SSL certificate management**: Check Let's Encrypt certificate status
- **Service health**: Verify backend services are reachable
- **Troubleshooting**: Debug routing issues, check middleware chains
- **Dynamic configuration**: Add/modify routes without restarting Traefik

## Rate Limits

No explicit rate limits. Traefik handles:
- High request volumes (thousands per second)
- API requests are lightweight
- Dynamic config updates are immediate

## Relevant Skills

- `reverse-proxy-management` - Traefik routing and SSL configuration
- `monitoring-ops` - Service health and routing verification
- `ssl-certificate-management` - Let's Encrypt certificate monitoring

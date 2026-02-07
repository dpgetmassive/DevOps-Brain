# Certbot (Let's Encrypt)

CLI tool for obtaining and managing SSL/TLS certificates from Let's Encrypt.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | - | Uses ACME protocol internally |
| MCP | - | Not available |
| CLI | Y | certbot command |
| SDK | - | Not applicable |

## Authentication

- **Type**: ACME account (auto-created on first run)
- **DNS challenge**: Requires DNS provider API credentials (e.g., Cloudflare)
- **HTTP challenge**: Requires port 80 open to the internet

## Common Agent Operations

### Obtain Certificate (HTTP Challenge)
```bash
certbot certonly --standalone -d <domain>
```

### Obtain Certificate (DNS Challenge - Cloudflare)
```bash
certbot certonly --dns-cloudflare \
  --dns-cloudflare-credentials /etc/letsencrypt/cloudflare.ini \
  -d <domain> -d "*.<domain>"
```

### Renew All Certificates
```bash
certbot renew
```

### Dry Run Renewal
```bash
certbot renew --dry-run
```

### List Certificates
```bash
certbot certificates
```

### Delete Certificate
```bash
certbot delete --cert-name <domain>
```

### Check Certificate Expiry
```bash
echo | openssl s_client -connect <domain>:443 2>/dev/null | openssl x509 -noout -enddate
```

## Key Files

| File | Location |
|------|----------|
| Certificates | `/etc/letsencrypt/live/<domain>/` |
| Fullchain | `/etc/letsencrypt/live/<domain>/fullchain.pem` |
| Private key | `/etc/letsencrypt/live/<domain>/privkey.pem` |
| Renewal config | `/etc/letsencrypt/renewal/<domain>.conf` |

## When to Use

- Obtaining SSL certificates for new services
- Managing certificate renewals
- Wildcard certificates via DNS challenge
- Standalone cert management (not via Traefik)

**Note**: Traefik handles its own Let's Encrypt via Cloudflare DNS challenge. Certbot is for services outside Traefik.

## Rate Limits

- 50 certificates per registered domain per week
- 5 duplicate certificates per week
- 300 new orders per account per 3 hours

## Relevant Skills

- reverse-proxy
- linux-admin

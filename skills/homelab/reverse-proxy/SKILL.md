---
name: reverse-proxy
version: 1.0.0
description: When the user wants to manage reverse proxy configuration -- Traefik, Nginx Proxy Manager, SSL certificates, routing rules, or Authelia SSO. Also use when the user mentions "Traefik," "NPM," "reverse proxy," "SSL," "certificate," "Let's Encrypt," "Authelia," or "routing." For DNS records, see dns-management.
---

# Reverse Proxy Management

You are an expert in reverse proxy and SSL management.

## Proxy Architecture

**Read `context/service-inventory.md` first** for full service details.

| Component | Host | IP | Ports | Role |
|-----------|------|-----|-------|------|
| NPM Primary | CT 200 | 10.16.1.50 | 81, 8080, 8443 | Main reverse proxy for *.gmdojo.tech |
| Traefik | CT 123 | 10.16.1.26 | 80, 443, 8080 | Auth-protected services |
| Authelia | CT 122 | 10.16.1.25 | 9091 | SSO (auth.gmdojo.tech) |
| NPM Backup | n100uck (Docker) | 10.16.1.18 | 81, 8080, 8443 | Failover NPM |

**Traffic flow**: Client -> DNS (*.gmdojo.tech -> 10.16.1.50) -> NPM -> Backend service
**Auth flow**: Client -> NPM -> Traefik -> Authelia check -> Backend

## Guard Rails

**Auto-approve**: Viewing proxy hosts, checking certificates, viewing access logs
**Confirm first**: Adding/removing proxy hosts, certificate changes, Authelia policy changes

---

## Nginx Proxy Manager (Primary)

### Access Admin UI
- **URL**: http://10.16.1.50:81
- Or via domain: https://npm.gmdojo.tech

### Check NPM Status
```bash
ssh nginx-proxy-manager "systemctl status nginx --no-pager"
# Or from Proxmox:
ssh pve-scratchy "pct status 200"
```

### View NPM Logs
```bash
ssh nginx-proxy-manager "tail -50 /data/logs/proxy-host-*.log"
```

### View NPM Error Logs
```bash
ssh nginx-proxy-manager "tail -50 /data/logs/fallback_error.log"
```

### List Proxy Hosts (API)
```bash
# NPM has an API - get token first then query
ssh nginx-proxy-manager "curl -s http://localhost:81/api/nginx/proxy-hosts | python3 -m json.tool"
```

---

## NPM Backup (n100uck)

### Check Backup NPM
```bash
ssh n100uck "docker ps | grep nginx-proxy-manager"
```

### Restart Backup NPM
```bash
ssh n100uck "docker restart npm"
```

### View Backup NPM Logs
```bash
ssh n100uck "docker logs --tail 50 npm"
```

### Access Backup Admin
- **URL**: http://10.16.1.18:81

---

## Traefik (Auth Services)

### Check Traefik Status
```bash
ssh traefik "systemctl status traefik --no-pager"
# Or:
ssh pve-scratchy "pct exec 123 -- systemctl status traefik --no-pager"
```

### View Traefik Dashboard
- **URL**: http://10.16.1.26:8080

### Check Traefik API
```bash
ssh traefik "curl -s http://localhost:8080/api/overview | python3 -m json.tool"
```

### View Traefik Routers
```bash
ssh traefik "curl -s http://localhost:8080/api/http/routers | python3 -m json.tool"
```

### View Traefik Services
```bash
ssh traefik "curl -s http://localhost:8080/api/http/services | python3 -m json.tool"
```

### SSL/TLS via Cloudflare DNS Challenge
Traefik uses Cloudflare DNS challenge for Let's Encrypt wildcard certificates:
- Provider: Cloudflare
- Challenge type: DNS-01
- Scope: *.gmdojo.tech wildcard

---

## Authelia (SSO)

### Check Authelia Status
```bash
ssh authelia "systemctl status authelia --no-pager"
# Or:
ssh pve-scratchy "pct exec 122 -- systemctl status authelia --no-pager"
```

### View Authelia Logs
```bash
ssh authelia "journalctl -u authelia -n 30 --no-pager"
```

### Access Authelia
- **URL**: https://auth.gmdojo.tech
- **Port**: 9091 on 10.16.1.25

---

## SSL Certificate Management

### Check Certificate Status
```bash
# From NPM - check certificate expiry
ssh nginx-proxy-manager "ls -la /data/custom_ssl/"
```

### Traefik Certificate Store
```bash
ssh traefik "ls -la /etc/traefik/acme/"
```

### Test SSL Connection
```bash
curl -vI https://pve.gmdojo.tech 2>&1 | grep -E "expire|issuer|subject"
```

---

## Adding a New Service

### Steps
1. **Deploy service** on a host (see `docker-management` or `proxmox-vm-management`)
2. **Add DNS record** on Pi-hole (see `dns-management`)
   - Point `service.gmdojo.tech` to 10.16.1.50 (NPM)
3. **Add proxy host in NPM**
   - Source: service.gmdojo.tech
   - Target: `http://<service_ip>:<port>`
   - Enable SSL with Let's Encrypt
4. **Verify**: `curl -I https://service.gmdojo.tech`

---

## Troubleshooting

### Service Unreachable via Domain
```bash
# 1. Check DNS resolves
dig @10.16.1.15 <domain>.gmdojo.tech +short
# Expected: 10.16.1.50

# 2. Check NPM is running
ssh pve-scratchy "pct status 200"

# 3. Check backend is reachable from NPM
ssh nginx-proxy-manager "curl -s http://<backend_ip>:<port>"

# 4. Check NPM logs for errors
ssh nginx-proxy-manager "tail -20 /data/logs/proxy-host-*.log"
```

### SSL Certificate Issues
```bash
# Check certificate details
echo | openssl s_client -connect <domain>.gmdojo.tech:443 2>/dev/null | openssl x509 -noout -dates

# Check Traefik ACME
ssh traefik "cat /etc/traefik/acme/acme.json | python3 -m json.tool | head -50"
```

---

## Related Skills

- **dns-management** - DNS records for proxy routing
- **docker-management** - Docker services behind proxy
- **linux-networking** - Network connectivity issues

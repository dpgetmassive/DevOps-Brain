# Service Inventory

Complete catalog of running services across the homelab infrastructure.

**Last Updated**: 2026-02-07

## Critical Services

### DNS (Pi-hole HA)

| Component | Host | IP | Port | Protocol | Health Check |
|-----------|------|-----|------|----------|-------------|
| Pi-hole Primary | piholed (CT 111) | 10.16.1.16 | 53, 80, 443 | DNS, HTTP/S | `dig @10.16.1.16 google.com` |
| Pi-hole Secondary | n100uck | 10.16.1.18 | 53, 80, 443 | DNS, HTTP/S | `dig @10.16.1.18 google.com` |
| DNS VIP | keepalived | 10.16.1.15 | 53 | DNS | `dig @10.16.1.15 google.com` |
| Keepalived (primary) | piholed | 10.16.1.16 | -- | VRRP | `systemctl status keepalived` |
| Keepalived (secondary) | n100uck | 10.16.1.18 | -- | VRRP | `systemctl status keepalived` |

**Web UIs**: http://10.16.1.15/admin (VIP), http://10.16.1.16/admin (primary), http://10.16.1.18/admin (secondary)

### Reverse Proxy

| Component | Host | IP | Port | Protocol | Health Check |
|-----------|------|-----|------|----------|-------------|
| NPM Primary | CT 200 | 10.16.1.50 | 81, 8080, 8443 | HTTP/S | `curl -s http://10.16.1.50:81` |
| NPM Backup | n100uck (Docker) | 10.16.1.18 | 81, 8080, 8443 | HTTP/S | `docker ps \| grep npm` |
| Traefik | CT 123 | 10.16.1.26 | 80, 443, 8080 | HTTP/S | `curl -s http://10.16.1.26:8080/api/overview` |
| Authelia | CT 122 | 10.16.1.25 | 9091 | HTTP | `curl -s http://10.16.1.25:9091/api/health` |

### Cluster & Quorum

| Component | Host | IP | Port | Protocol | Health Check |
|-----------|------|-----|------|----------|-------------|
| Proxmox (primary) | pve-scratchy | 10.16.1.22 | 8006 | HTTPS | `ssh pve-scratchy "pvecm status"` |
| Proxmox (secondary) | pve-itchy | 10.16.1.8 | 8006 | HTTPS | `ssh pve-itchy "pvecm status"` |
| corosync-qnetd | n100uck | 10.16.1.18 | 5405 | UDP | `systemctl status corosync-qnetd` |

### Storage

| Component | Host | IP | Port | Protocol | Health Check |
|-----------|------|-----|------|----------|-------------|
| TrueNAS Primary | truenas-scale | 10.16.1.6 | 443 | HTTPS | `ssh truenas-scale "midclt call system.info"` |
| TrueNAS DR | truenas-dr | 10.16.1.20 | 443 | HTTPS | `ssh truenas-dr "midclt call system.info"` |
| NFS (backup storage) | truenas-dr | 10.16.1.20 | 2049 | NFS | `ssh pve-scratchy "df -h /mnt/pve/pve-bk-truenas-dr"` |

### Monitoring

| Component | Host | IP | Port | Protocol | Health Check |
|-----------|------|-----|------|----------|-------------|
| Monitoring Dashboard | n100uck | 10.16.1.18 | 8081 | HTTP | `curl -s http://10.16.1.18:8081/api/status` |
| Mailrise SMTP | n100uck | 10.16.1.18 | 25 | SMTP | `systemctl status mailrise` |

## Application Services

### Media Stack

| Service | Host | CT ID | IP | Port | Health Check |
|---------|------|-------|-----|------|-------------|
| Sonarr | CT 107 | 107 | 10.16.1.13 | 8989 | `curl -s http://10.16.1.13:8989` |
| Radarr | CT 112 | 112 | 10.16.1.14 | 7878 | `curl -s http://10.16.1.14:7878` |
| Plex | CT 108 | 108 | 10.16.1.36 | 32400 | `curl -s http://10.16.1.36:32400/web` |

### Photo Management

| Service | Host | CT ID | IP | Port | Health Check |
|---------|------|-------|-----|------|-------------|
| Immich | CT 118 | 118 | 10.16.1.19 | 2283 | `curl -s http://10.16.1.19:2283` |

### Home Automation

| Service | Host | IP | Port | Health Check |
|---------|------|-----|------|-------------|
| Home Assistant | homeassistant | 10.16.66.9 | 8123 | `curl -s http://10.16.66.9:8123` |

### Web Applications

| Service | Host | CT ID | IP | Port | Health Check |
|---------|------|-------|-----|------|-------------|
| FamilyFramed | CT 201 | 201 | 10.16.1.11 | -- | `ssh family-framed-srv "systemctl status"` |
| EWP Banking | CT 121 | 121 | 10.16.1.24 | -- | Via `pct exec 121` (no sshd) |
| Homer Dashboard | CT 204 | 204 | 10.16.1.7 | 8080 | `curl -s http://10.16.1.7:8080` |

### Network & Security

| Service | Host | CT ID | IP | Port | Health Check |
|---------|------|-------|-----|------|-------------|
| WatchYourLAN | CT 101 | 101 | 10.16.1.104 | 8840 | `curl -s http://10.16.1.17:8840/api/all` |
| Cloudflare Tunnel | CT 114 | 114 | 10.16.1.3 | -- | `ssh pve-scratchy "pct exec 114 -- cloudflared tunnel info"` |
| OPNsense Firewall | opnsense | -- | 10.16.1.1 | 443 | `ping -c 1 10.16.1.1` |

### Docker Hosts

| Service | Host | CT/VM ID | IP | Health Check |
|---------|------|----------|-----|-------------|
| dockc | VM 100 | 100 | 10.16.1.4 | `ssh dockc "docker ps"` |
| docker00 | CT 106 | 106 | 10.16.1.40 | `ssh pve-scratchy "pct exec 106 -- docker ps"` |

### AI Services (gm-ai)

| Service | Host | IP | Port | Health Check |
|---------|------|-----|------|-------------|
| Ollama | gm-ai | 10.16.1.9 | 11434 | `curl -s http://10.16.1.9:11434/api/tags` |
| Open WebUI | gm-ai | 10.16.1.9 | 3000 | `curl -s http://10.16.1.9:3000` |
| clawdbot Gateway | gm-ai | 10.16.1.9 | TBD | TBD (needs discovery) |
| Cockpit | gm-ai | 10.16.1.9 | 9090 | `curl -sk https://10.16.1.9:9090` |

### Gaming

| Service | Host | CT ID | IP | Health Check |
|---------|------|-------|-----|-------------|
| Crafty (pve-scratchy) | CT 129 | 129 | 10.16.1.29 | -- |
| Crafty Controller (pve-itchy) | CT 120 | 120 | -- | -- |

### VPN / Remote Access

| Service | Host | CT ID | IP | Health Check |
|---------|------|-------|-----|-------------|
| Tailscale Node | CT 901 | 901 | 10.16.1.31 | `ssh pve-scratchy "pct exec 901 -- tailscale status"` |
| CP Tailscale | CT 117 | 117 | 10.16.10.2 | `ssh pve-scratchy "pct exec 117 -- tailscale status"` |
| KASM | VM 119 | 119 | -- | On pve-itchy |

## Service Dependencies

```
DNS (Pi-hole VIP 10.16.1.15)
├── All services depend on DNS for name resolution
├── Pi-hole Primary (CT 111) + Keepalived
└── Pi-hole Secondary (n100uck) + Keepalived

Reverse Proxy (NPM CT 200, 10.16.1.50)
├── All *.gmdojo.tech domains route through NPM
├── Traefik (CT 123) handles auth-protected routes
│   └── Authelia (CT 122) provides SSO
└── NPM Backup (n100uck Docker) for failover

Storage (TrueNAS Primary 10.16.1.6)
├── NFS exports to Proxmox hosts
├── ZFS replication to TrueNAS DR (10.16.1.20)
│   └── CloudSync to Backblaze B2
└── Media stack reads from FileServer

Proxmox Cluster
├── pve-scratchy (primary) - hosts most workloads
├── pve-itchy (secondary) - hosts TrueNAS DR VM
└── corosync-qnetd (n100uck) - quorum device

Monitoring (n100uck)
├── 5 monitoring scripts (independent)
├── Flask dashboard (port 8081)
├── Mailrise SMTP relay (port 25)
└── ntfy.sh/homelab-status (consolidated alerts)
```

## Startup Order (After Full Outage)

1. **OPNsense** (10.16.1.1) - Network/gateway must be first
2. **pve-scratchy** (10.16.1.22) - Primary hypervisor
3. **pve-itchy** (10.16.1.8) - Secondary hypervisor
4. **TrueNAS DR VM** (VM 115 on pve-itchy) - Backup storage and NFS
5. **TrueNAS Primary** (10.16.1.6) - Primary storage
6. **Pi-hole Primary** (CT 111) + Keepalived - DNS resolution
7. **n100uck** (10.16.1.18) - Monitoring, secondary Pi-hole, qnetd
8. **NPM** (CT 200) - Reverse proxy for all services
9. **Remaining CTs/VMs** - Application services in any order
10. **gm-ai** (10.16.1.9) - AI services (independent)

## Credential References

**Note**: No actual credentials stored here. Reference locations only.

| Service | Credential Location |
|---------|-------------------|
| Proxmox Web UI | Browser saved / PAM auth |
| TrueNAS Web UI | Browser saved |
| Pi-hole Admin | Per-instance admin password |
| NPM Admin | Browser saved |
| Authelia | LDAP/file backend |
| Keepalived VRRP | Auth pass in `/etc/keepalived/keepalived.conf` |
| SSH Keys | `~/.ssh/id_rsa`, `~/.ssh/id_ed25519` |
| ntfy | Public topic (no auth) |
| Backblaze B2 | TrueNAS CloudSync credential store |

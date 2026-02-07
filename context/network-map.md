# Network Map

Network topology and addressing for the Get Massive Dojo homelab.

**Last Updated**: 2026-02-07

## Subnet Layout

### Primary LAN: 10.16.1.0/24

| IP | Hostname | Role |
|----|----------|------|
| 10.16.1.1 | opnsense | Firewall/gateway |
| 10.16.1.3 | cloudflared (CT 114) | Cloudflare tunnel |
| 10.16.1.4 | dockc (VM 100) | Docker host |
| 10.16.1.6 | truenas-scale | Primary TrueNAS storage |
| 10.16.1.7 | homer (CT 204) | Dashboard |
| 10.16.1.8 | pve-itchy | Secondary Proxmox node |
| 10.16.1.9 | gm-ai | AI/ML services (physical) |
| 10.16.1.11 | family-framed-srv (CT 201) | FamilyFramed backend |
| 10.16.1.13 | sonarr (CT 107) | TV show management |
| 10.16.1.14 | radarr (CT 112) | Movie management |
| 10.16.1.15 | **DNS VIP** | Pi-hole HA floating IP (keepalived) |
| 10.16.1.16 | piholed (CT 111) | Primary Pi-hole DNS |
| 10.16.1.17 | -- | WatchYourLAN UI endpoint |
| 10.16.1.18 | n100uck | Monitoring witness (physical) |
| 10.16.1.19 | immich (CT 118) | Photo management |
| 10.16.1.20 | truenas-dr (VM 115) | DR TrueNAS storage |
| 10.16.1.22 | pve-scratchy | Primary Proxmox node |
| 10.16.1.24 | ewp-banking (CT 121) | Banking app |
| 10.16.1.25 | authelia (CT 122) | Authelia SSO |
| 10.16.1.26 | traefik (CT 123) | Traefik reverse proxy |
| 10.16.1.29 | crafty-s (CT 129) | Minecraft server |
| 10.16.1.31 | tailscaler (CT 901) | Tailscale node |
| 10.16.1.36 | plexpunnisher (CT 108) | Plex management |
| 10.16.1.40 | docker00 (CT 106) | Docker host |
| 10.16.1.41 | proxbackupsrv (CT 900) | Proxmox backup service |
| 10.16.1.50 | nginx-proxy-manager (CT 200) | Primary NPM reverse proxy |
| 10.16.1.104 | watchyourlan (CT 101) | Network scanner |

### IoT VLAN: 10.16.66.0/24 (VLAN 66)

| IP | Hostname | Role |
|----|----------|------|
| 10.16.66.9 | homeassistant | Home Assistant OS |
| 10.16.66.10 | familyframed-pi | Raspberry Pi |

### Tailscale: 10.16.10.0/24

| IP | Hostname | Role |
|----|----------|------|
| 10.16.10.2 | cp-tailscale (CT 117) | Tailscale for Cyber People |

## Virtual IPs (VIPs)

| VIP | Purpose | Protocol | Primary | Secondary |
|-----|---------|----------|---------|-----------|
| 10.16.1.15 | Pi-hole DNS HA | VRRP (keepalived) | piholed (10.16.1.16, priority 100) | n100uck (10.16.1.18, priority 90) |

**VRRP Config**:
- Virtual Router ID: 15
- Advertisement interval: 1 second
- Auth: PASS (piholedns2025)
- Primary interface: eth0 (piholed), enp3s0 (n100uck)

## DNS Configuration

### Internal DNS (Pi-hole)

**Service IP**: 10.16.1.15 (VIP, auto-failover)
- Primary: piholed (10.16.1.16)
- Secondary: n100uck (10.16.1.18)
- Pi-hole version: v6.2.2

**Upstream resolvers**: 1.1.1.1, 1.0.0.1 (Cloudflare)
**Cache size**: 10000

### Local DNS Records (*.gmdojo.tech -> 10.16.1.50)

All resolve to NPM (10.16.1.50) for reverse proxy routing:

| Domain | Points To | Service |
|--------|-----------|---------|
| pve.gmdojo.tech | 10.16.1.50 | Proxmox Web UI |
| uptime.gmdojo.tech | 10.16.1.50 | Uptime monitoring |
| grafana.gmdojo.tech | 10.16.1.50 | Grafana dashboards |
| nas.gmdojo.tech | 10.16.1.50 | TrueNAS Web UI |
| pihole.gmdojo.tech | 10.16.1.50 | Pi-hole admin |
| home.gmdojo.tech | 10.16.1.50 | Home Assistant |
| status.gmdojo.tech | 10.16.1.50 | Status page |
| npm.gmdojo.tech | 10.16.1.50 | NPM admin |
| plex.gmdojo.tech | 10.16.1.50 | Plex |
| firewall-node1.gmdojo.tech | 10.16.1.50 | OPNsense |
| unifi.gmdojo.tech | 10.16.1.50 | UniFi controller |
| really.gmdojo.tech | 10.16.1.50 | -- |

**DNS sync**: Custom records sync hourly from piholed to n100uck via `/root/sync-pihole-dns.sh`

### Cloudflare

- **DNS challenge**: Used by Traefik for Let's Encrypt wildcard certs
- **Tunnel**: `uptime-gm-hq` for external access to select services
- **Tunnel CT**: cloudflared (CT 114, 10.16.1.3)

## Tailscale

- **Subnet routing**: Via TrueNAS for homelab access
- **Nodes**: tailscaler (CT 901), cp-tailscale (CT 117)
- **External access**: dp-macbook-secondary (100.86.205.100)

## Reverse Proxy Architecture

### Primary: Nginx Proxy Manager (CT 200, 10.16.1.50)
- Admin: port 81
- HTTP: port 8080
- HTTPS: port 8443
- Routes all `*.gmdojo.tech` domains

### Auth Layer: Traefik + Authelia (CT 123 + CT 122)
- Traefik: HTTP/80, HTTPS/443, Dashboard/8080 (10.16.1.26)
- Authelia: SSO on port 9091 (10.16.1.25, auth.gmdojo.tech)
- Handles authentication middleware for protected services

### Backup: NPM on n100uck (Docker)
- Admin: port 81
- HTTP: port 8080
- HTTPS: port 8443

## Notification Channels

| Channel | Endpoint | Purpose |
|---------|----------|---------|
| ntfy (consolidated) | https://ntfy.sh/homelab-status | All monitoring alerts |
| ntfy (DNS sync) | https://ntfy.sh/gmdojo-monitoring | Pi-hole DNS sync alerts |
| Mailrise SMTP | 10.16.1.18:25 | Email-to-ntfy relay for legacy apps |

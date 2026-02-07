---
name: homelab-services
version: 1.0.0
description: When the user wants to see what services are running, check service health, understand dependencies, or manage the service catalog. Also use when the user mentions "what's running," "service catalog," "service status," "service dependencies," or "infrastructure overview." For specific service management, see domain-specific skills.
---

# Homelab Services

You are an expert in homelab infrastructure services. This skill provides the master service inventory and dependency map.

## Service Overview

**Read `context/service-inventory.md` first** for the complete service catalog with ports and health checks.

**Total Infrastructure**: 7 physical/hypervisor hosts, ~19 VMs/CTs, multiple Docker services

---

## Full Infrastructure Health Sweep

```bash
for host in n100uck pve-scratchy pve-itchy opnsense truenas-scale truenas-dr piholed gm-ai dockc nginx-proxy-manager family-framed-srv; do
    echo -n "$host: "
    ssh -o ConnectTimeout=5 -o BatchMode=yes $host "hostname && uptime" 2>&1 | tr '\n' ' '
    echo ""
done
```

## Quick Service Checks

### Critical Services (Must Be Running)
```bash
echo "=== DNS ===" && dig @10.16.1.15 google.com +short
echo "=== Proxmox ===" && ssh pve-scratchy "pvecm status | head -5"
echo "=== TrueNAS ===" && ssh truenas-scale "uptime"
echo "=== Monitoring ===" && curl -s http://10.16.1.18:8081/api/status | python3 -c "import sys,json; d=json.load(sys.stdin); print('Dashboard OK')" 2>/dev/null || echo "Dashboard DOWN"
echo "=== NPM ===" && ssh pve-scratchy "pct status 200"
```

### Daily Readiness (Best Single Check)
```bash
ssh n100uck "cat /var/run/daily-readiness.state"
```

---

## Service Dependency Chain

```
Internet
└── OPNsense (10.16.1.1) - Gateway/Firewall
    └── DNS (Pi-hole VIP 10.16.1.15)
        ├── All internal services depend on DNS
        └── NPM (10.16.1.50) - Reverse Proxy
            ├── Traefik (10.16.1.26) + Authelia (10.16.1.25) - Auth
            └── All *.gmdojo.tech services

Proxmox Cluster
├── pve-scratchy (10.16.1.22) - Most workloads
├── pve-itchy (10.16.1.8) - DR, some workloads
└── corosync-qnetd (n100uck) - Quorum

Storage
├── TrueNAS Primary (10.16.1.6) - FileServer, NFS
└── TrueNAS DR (10.16.1.20) - Replication target
    └── Backblaze B2 - Offsite

Monitoring (n100uck)
├── 5 independent monitor scripts
├── Flask dashboard (:8081)
└── ntfy.sh/homelab-status
```

---

## Services by Category

### Tier 1: Critical Infrastructure
| Service | Host | Status Command |
|---------|------|----------------|
| OPNsense | 10.16.1.1 | `ping -c 1 10.16.1.1` |
| Proxmox Primary | pve-scratchy | `ssh pve-scratchy "pvecm status"` |
| Proxmox Secondary | pve-itchy | `ssh pve-itchy "pvecm status"` |
| TrueNAS Primary | truenas-scale | `ssh truenas-scale "midclt call system.info"` |
| TrueNAS DR | truenas-dr | `ssh truenas-dr "midclt call system.info"` |
| Pi-hole DNS | VIP 10.16.1.15 | `dig @10.16.1.15 google.com` |

### Tier 2: Core Services
| Service | Host | Status Command |
|---------|------|----------------|
| NPM Reverse Proxy | CT 200 | `ssh pve-scratchy "pct status 200"` |
| Monitoring | n100uck | `curl -s http://10.16.1.18:8081/api/status` |
| Corosync Qnetd | n100uck | `ssh n100uck "systemctl is-active corosync-qnetd"` |
| Keepalived | piholed + n100uck | `ssh piholed "systemctl is-active keepalived"` |

### Tier 3: Application Services
| Service | Host | Status Command |
|---------|------|----------------|
| Traefik | CT 123 | `ssh pve-scratchy "pct status 123"` |
| Authelia | CT 122 | `ssh pve-scratchy "pct status 122"` |
| Immich | CT 118 | `ssh pve-scratchy "pct status 118"` |
| Home Assistant | 10.16.66.9 | `curl -s http://10.16.66.9:8123` |

### Tier 4: Media & Utility
| Service | Host | Status Command |
|---------|------|----------------|
| Sonarr | CT 107 | `ssh pve-scratchy "pct status 107"` |
| Radarr | CT 112 | `ssh pve-scratchy "pct status 112"` |
| Plex | CT 108 | `ssh pve-scratchy "pct status 108"` |
| Homer Dashboard | CT 204 | `ssh pve-scratchy "pct status 204"` |

---

## Startup Order (After Full Outage)

1. OPNsense (10.16.1.1)
2. pve-scratchy (10.16.1.22)
3. pve-itchy (10.16.1.8)
4. TrueNAS DR (VM 115 on pve-itchy)
5. TrueNAS Primary (10.16.1.6)
6. Pi-hole Primary (CT 111) + Keepalived
7. n100uck (10.16.1.18) - Monitoring, Pi-hole secondary, qnetd
8. NPM (CT 200)
9. All remaining CTs/VMs
10. gm-ai (10.16.1.9)

---

## Related Skills

- **monitoring-ops** - Alert management and monitoring scripts
- **proxmox-cluster** - Cluster and node health
- **dns-management** - DNS service management
- **reverse-proxy** - Proxy routing for services
- **docker-management** - Docker-based services

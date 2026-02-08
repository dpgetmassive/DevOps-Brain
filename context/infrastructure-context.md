# Infrastructure Context

Environment-specific context for the Get Massive Dojo homelab. **Read this file before executing any skill.**

**Last Updated**: 2026-02-07
**Source**: Compiled from homelab/Docco/ documentation

## Host Registry

### Physical Infrastructure / Hypervisors

| SSH Alias | IP | User | OS | Role |
|-----------|-----|------|-----|------|
| `n100uck` | 10.16.1.18 | root | Debian 12 | Monitoring witness, Pi-hole secondary, NPM backup, Ansible control, corosync-qnetd |
| `pve-scratchy` | 10.16.1.22 | root | Proxmox 8.x | Primary Proxmox node (hosts most CTs/VMs) |
| `pve-itchy` | 10.16.1.8 | root | Proxmox 8.x | Secondary Proxmox node |
| `opnsense` | 10.16.1.1 | root | OPNsense | Firewall/gateway |
| `truenas-scale` | 10.16.1.6 | root | TrueNAS SCALE | Primary ZFS storage, NFS exports |
| `truenas-dr` | 10.16.1.20 | root | TrueNAS SCALE | DR storage, ZFS replication target, backup storage |
| `gm-ai` | 10.16.1.9 | gm-admin | Debian 12 | Physical box, AI/ML services, Cockpit on :9090 |

### Service Containers/VMs on pve-scratchy

| SSH Alias | IP | User | CT/VM ID | Role |
|-----------|-----|------|----------|------|
| `dockc` | 10.16.1.4 | root | VM 100 | Docker host |
| `nginx-proxy-manager` | 10.16.1.50 | root | CT 200 | Primary reverse proxy (NPM) |
| `family-framed-srv` | 10.16.1.11 | root | CT 201 | FamilyFramed backend |
| `authelia` | 10.16.1.25 | root | CT 122 | Authelia SSO (auth.gmdojo.tech) |
| `traefik` | 10.16.1.26 | root | CT 123 | Traefik reverse proxy (auth services) |
| `ewp-banking` | 10.16.1.24 | root | CT 121 | Banking app (no sshd) |
| `piholed` | 10.16.1.16 | root | CT 111 | Primary Pi-hole DNS |

### Other Running CTs on pve-scratchy (access via `pct exec`)

| CT ID | Name | IP | Role |
|-------|------|-----|------|
| 101 | watchyourlan | 10.16.1.104 | Network scanner (UI: http://10.16.1.17:8840) |
| 106 | docker00 | 10.16.1.40 | Docker host |
| 107 | sonarr | 10.16.1.13 | TV show management |
| 108 | plexpunnisher | 10.16.1.36 | Plex management |
| 112 | radarr | 10.16.1.14 | Movie management |
| 114 | cloudflared | 10.16.1.3 | Cloudflare tunnel |
| 117 | cp-tailscale | 10.16.10.2 | Tailscale for Cyber People |
| 118 | immich | 10.16.1.19 | Photo management |
| 129 | crafty-s | 10.16.1.29 | Minecraft server |
| 204 | homer | 10.16.1.7 | Dashboard |
| 900 | proxbackupsrv | 10.16.1.41 | Proxmox backup service |
| 901 | tailscaler | 10.16.1.31 | Tailscale node |

### VMs/CTs on pve-itchy

| VM/CT ID | Name | IP | Status |
|----------|------|-----|--------|
| 109 | docka | -- | Stopped |
| 115 | truenas-scale-DR | -- | Running (TrueNAS DR VM) |
| 116 | winblows | -- | Running (Windows) |
| 119 | kasm | -- | Running |
| 120 | crafty-controller | -- | Running |

### IoT / VLAN 66

| SSH Alias | IP | User | Role |
|-----------|-----|------|------|
| `homeassistant` | 10.16.66.9 | dp | Home Assistant OS |
| `familyframed-pi` | 10.16.66.10 | dp | Raspberry Pi |

### External / Tailscale

| SSH Alias | Host | User | Notes |
|-----------|------|------|-------|
| `cp-staging` | staging.cyber-people.tech | developer | Cyber People staging |
| `perrett.tech` | www.perrett.tech | root | Personal site |
| `dp-macbook-secondary` | 100.86.205.100 | dp | Tailscale, uses id_ed25519 |

## SSH Access

All hosts configured in `~/.ssh/config` with key-based auth. SSH multiplexing enabled for all 10.16.x hosts via ControlMaster.

**Connection pattern**: Always use SSH alias, never raw IPs.

**Fallback chain**:
1. `ssh <alias>` (preferred)
2. `ssh root@<ip>` (explicit)
3. `ssh -i ~/.ssh/id_rsa root@<ip>` (explicit key)
4. Via Proxmox: `ssh pve-scratchy "pct exec <CTID> -- <command>"` (containers)
5. Via Proxmox: `ssh pve-scratchy "qm guest exec <VMID> -- <command>"` (VMs)

### SSH Key Setup

**Primary SSH Key**: `~/.ssh/id_rsa` (or `~/.ssh/id_ed25519`)

All homelab hosts are configured to accept key-based authentication. The same SSH key is typically authorized across all hosts for consistency.

**SSH Config Example** (`~/.ssh/config`):

```ssh-config
# Homelab Infrastructure
Host n100uck
    HostName 10.16.1.18
    User root
    IdentityFile ~/.ssh/id_rsa
    ControlMaster auto
    ControlPath ~/.ssh/control-%h-%p-%r
    ControlPersist 10m

Host pve-scratchy
    HostName 10.16.1.22
    User root
    IdentityFile ~/.ssh/id_rsa
    ControlMaster auto
    ControlPath ~/.ssh/control-%h-%p-%r
    ControlPersist 10m

Host pve-itchy
    HostName 10.16.1.8
    User root
    IdentityFile ~/.ssh/id_rsa
    ControlMaster auto
    ControlPath ~/.ssh/control-%h-%p-%r
    ControlPersist 10m

Host opnsense
    HostName 10.16.1.1
    User root
    IdentityFile ~/.ssh/id_rsa
    ControlMaster auto
    ControlPath ~/.ssh/control-%h-%p-%r
    ControlPersist 10m

Host truenas-scale
    HostName 10.16.1.6
    User root
    IdentityFile ~/.ssh/id_rsa
    ControlMaster auto
    ControlPath ~/.ssh/control-%h-%p-%r
    ControlPersist 10m

Host truenas-dr
    HostName 10.16.1.20
    User root
    IdentityFile ~/.ssh/id_rsa
    ControlMaster auto
    ControlPath ~/.ssh/control-%h-%p-%r
    ControlPersist 10m

Host gm-ai
    HostName 10.16.1.9
    User gm-admin
    IdentityFile ~/.ssh/id_rsa
    ControlMaster auto
    ControlPath ~/.ssh/control-%h-%p-%r
    ControlPersist 10m

# Service Containers/VMs
Host dockc
    HostName 10.16.1.4
    User root
    IdentityFile ~/.ssh/id_rsa
    ProxyJump pve-scratchy

Host nginx-proxy-manager
    HostName 10.16.1.50
    User root
    IdentityFile ~/.ssh/id_rsa
    ProxyJump pve-scratchy

Host piholed
    HostName 10.16.1.16
    User root
    IdentityFile ~/.ssh/id_rsa
    ProxyJump pve-scratchy

Host authelia
    HostName 10.16.1.25
    User root
    IdentityFile ~/.ssh/id_rsa
    ProxyJump pve-scratchy

Host traefik
    HostName 10.16.1.26
    User root
    IdentityFile ~/.ssh/id_rsa
    ProxyJump pve-scratchy

# IoT VLAN
Host homeassistant
    HostName 10.16.66.9
    User dp
    IdentityFile ~/.ssh/id_rsa

Host familyframed-pi
    HostName 10.16.66.10
    User dp
    IdentityFile ~/.ssh/id_rsa

# External/Tailscale
Host cp-staging
    HostName staging.cyber-people.tech
    User developer
    IdentityFile ~/.ssh/id_rsa

Host dp-macbook-secondary
    HostName 100.86.205.100
    User dp
    IdentityFile ~/.ssh/id_ed25519
```

**Key Features**:
- **ControlMaster**: Enables SSH connection multiplexing (reuses existing connections)
- **ControlPath**: Socket location for multiplexing
- **ControlPersist**: Keeps connection alive for 10 minutes after last use
- **ProxyJump**: For containers/VMs, routes through Proxmox host

### Setting Up SSH Access

**For a new user/agent**:

1. **Generate SSH key** (if not exists):
   ```bash
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -C "your-email@example.com"
   # Or use ed25519:
   ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -C "your-email@example.com"
   ```

2. **Copy public key to hosts**:
   ```bash
   # Manual copy (one-time per host)
   ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.16.1.18  # n100uck
   ssh-copy-id -i ~/.ssh/id_rsa.pub root@10.16.1.22  # pve-scratchy
   # ... repeat for all hosts
   
   # Or via Ansible (if available):
   ssh n100uck "cd ~/developerland/homelab/ansible && ansible-playbook deploy-ssh-key.yml -i inventory.ini"
   ```

3. **Create/update `~/.ssh/config`**:
   - Copy the example config above
   - Adjust `IdentityFile` path if using different key
   - Adjust `User` if different username required

4. **Test connection**:
   ```bash
   ssh n100uck "hostname"  # Should work without password
   ssh pve-scratchy "hostname"
   ```

5. **Verify multiplexing**:
   ```bash
   # First connection
   ssh n100uck "hostname"
   # Second connection should reuse the first (check with `ssh -O check n100uck`)
   ssh -O check n100uck
   ```

### SSH Key Management

**Key Distribution**:
- All homelab hosts accept the same SSH public key
- Keys are managed via Ansible (on n100uck) for consistency
- New keys can be added via `ansible-playbook` or manual `ssh-copy-id`

**Key Rotation**:
- Rotate keys periodically (recommended: annually)
- Update `~/.ssh/config` with new key path
- Deploy new public key to all hosts via Ansible
- Remove old keys from `~/.ssh/authorized_keys` on hosts

**Troubleshooting**:
- **Connection refused**: Check host is online, firewall allows SSH (port 22)
- **Permission denied**: Verify public key is in `~/.ssh/authorized_keys` on target host
- **Host key verification failed**: Add host to `~/.ssh/known_hosts` or use `-o StrictHostKeyChecking=no` (not recommended for production)
- **Multiplexing not working**: Check `~/.ssh/control-*` sockets exist, verify ControlMaster config

## Proxmox Cluster

- **Cluster name**: 180-homelab
- **Primary node**: pve-scratchy (10.16.1.22) - hosts majority of workloads
- **Secondary node**: pve-itchy (10.16.1.8) - backup node, hosts TrueNAS DR VM
- **Quorum device**: corosync-qnetd on n100uck (10.16.1.18)
- **Web UI**: https://10.16.1.22:8006 (primary), https://10.16.1.8:8006 (secondary)
- **Total workloads**: ~19 VMs/CTs

## Storage Architecture

### TrueNAS Primary (10.16.1.6)
- **Pool**: Tank
- **Key dataset**: Tank/FileServer (923GB) - Downloads, Media, HomeLab configs
- **NFS exports**: FileServer to Proxmox hosts
- **Config backups**: `/mnt/Tank/FileServer/HomeLab/truenas-configs/`

### TrueNAS DR (10.16.1.20)
- **Pool**: Tank
- **Key dataset**: Tank/Data-DR-Copy
  - `FileServer/` - Replicated from Primary (daily 2:10 AM)
  - `gm-ai-homelab/` - Replicated from gm-ai (daily 3:00 AM)
- **NFS export**: `/mnt/pve/pve-bk-truenas-dr/dump/` - Proxmox backup storage
- **Offsite sync**: Backblaze B2 via CloudSync (daily 4:00 AM)

### gm-ai Storage (10.16.1.9)
- **Pool**: homelab (single NVMe, no RAID)
- **Datasets**:
  - `homelab/` (12.6G) - configs, scripts, projects
  - `homelab/ai-services` (26.6G) - clawdbot gateway, AI services
  - `homelab/docker` (4.1G) - container volumes
- **Replication**: Daily 3:00 AM to TrueNAS DR via `zfs-replicate-dr.timer`

## Backup Architecture (3-2-1 Rule)

| Layer | Schedule | Source | Target | Method |
|-------|----------|--------|--------|--------|
| Proxmox Native | 2:45 AM daily | All VMs/CTs (except 110, 115, 107, 112) | TrueNAS DR NFS | vzdump (zstd) |
| ZFS Replication (TrueNAS) | 2:10 AM daily | Tank/FileServer (Primary) | Tank/Data-DR-Copy (DR) | Incremental ZFS |
| ZFS Replication (gm-ai) | 3:00 AM daily | homelab pool (gm-ai) | Tank/Data-DR-Copy/gm-ai-homelab (DR) | zfs send/recv |
| Backblaze CloudSync | 4:00 AM daily | Tank/Data-DR-Copy (DR) | Backblaze B2 | CloudSync |
| Infra Orchestration | 1:30 AM daily | TrueNAS configs | FileServer/HomeLab/truenas-configs | truenas-orchestration.sh |

**Retention**: 7 daily + 1 monthly (Proxmox), ~22 rolling snapshots (ZFS), 7 daily (gm-ai)

## Monitoring Architecture (v2.2)

**Witness node**: n100uck (10.16.1.18) - independent from Proxmox hosts
**Alert topic**: `homelab-status` (consolidated, ntfy.sh)
**Dashboard**: http://10.16.1.18:8081 (Flask, API at /api/status)

| Monitor | Schedule | Script | Log |
|---------|----------|--------|-----|
| Host Availability | Every 5 min | monitor-host-availability.sh | /var/log/host-availability.log |
| Backup Status | 6:00 AM daily | monitor-backup-status.sh | /var/log/backup-status.log |
| Data Protection | 6:30 AM daily | monitor-data-protection.sh | /var/log/data-protection.log |
| System Health | Every 15 min | monitor-system-health.sh | /var/log/system-health.log |
| Daily Readiness | 6:45 AM daily | daily-readiness-check.sh | /var/log/daily-readiness.log |

**Scripts location**: `/usr/local/bin/` on n100uck
**State files**: `/var/run/*.state` on n100uck

## AI Services (gm-ai - 10.16.1.9)

- **Ollama**: Local LLM inference engine
- **Open WebUI**: Chat interface for Ollama models
- **clawdbot**: Custom API gateway for AI services
- **Management**: Cockpit on https://10.16.1.9:9090
- **SSH**: `ssh gm-ai` (user: gm-admin, sudo for admin operations)

## Automation

### Ansible (on n100uck)
- **Patching**: `ansible/patching/quick_patch_all.yml` - automated patching across 19 hosts
- **Discovery**: `ansible_auto_discovery.sh` - weekly auto-discovery from Proxmox
- **Daily report**: `patch_status_report.yml` - daily 2 AM status report
- **Orchestrator**: `ansible_daily_automation.sh` - master automation runner

### GitHub Actions
- `cp-www-staging` - Staging deployment for Cyber People
- `smb1001-gap-analysis` - CI (lint, type-check, build) + staging deploy

## Guard Rails

### Auto-approve (just do it)
- All read-only operations (status checks, logs, diagnostics, monitoring)
- Service restarts (systemctl restart, docker restart, pct reboot)
- Container start/stop/restart, config file edits
- SSH key distribution, log rotation, package updates on containers
- DNS record changes on piholed, cron job edits, certificate renewals
- Docker image pulls and container recreations, snapshot creation

### Confirm with user first
- **Physical host reboots**: pve-scratchy, pve-itchy, n100uck, opnsense, truenas-scale, truenas-dr, gm-ai
- **ZFS destruction**: `zfs destroy`, pool removal, dataset deletion
- **Firewall changes**: Any rule modifications on opnsense
- **Cluster operations**: `pvecm` commands that affect quorum
- **Bulk operations**: Actions targeting 3+ hosts simultaneously
- **Network-wide impact**: Anything that would take DNS, routing, or the full lab offline
- **Data deletion**: Removing backups, purging snapshots, dropping databases

## Related Projects

| Project | Path | Purpose |
|---------|------|---------|
| Homelab Docs | `~/developerland/homelab/` | Infrastructure documentation and scripts |
| SMB1001 Gap Analysis | `~/developerland/smb1001-gap-analysis/` | SMB1001 certification assessment tool |
| SMB1001 Assessment Agent | `~/developerland/smb1001-assessment-agent/` | AI-powered SMB1001 assessment (Frances) |
| Cyber People Staging | `~/developerland/cp-www-staging/` | Cyber People website |

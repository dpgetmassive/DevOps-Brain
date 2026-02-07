# DevOps Tools Registry

Quick reference for AI agents to discover tool capabilities and integration methods.

## How to Use This Registry

1. **Find tools by category** - Browse sections below for tools in each domain
2. **Check integration methods** - See what APIs, CLIs, or MCPs are available
3. **Read integration guides** - Detailed setup and operations in `integrations/`

---

## Tool Index

| Tool | Category | API | MCP | CLI | SDK | Guide |
|------|----------|:---:|:---:|:---:|:---:|-------|
| proxmox-api | Virtualization | Y | - | Y | Y | [proxmox-api.md](integrations/proxmox-api.md) |
| truenas-api | Storage | Y | - | - | Y | [truenas-api.md](integrations/truenas-api.md) |
| ansible | Automation | - | - | Y | Y | [ansible.md](integrations/ansible.md) |
| docker | Containers | Y | - | Y | Y | [docker.md](integrations/docker.md) |
| github | CI/CD | Y | Y | Y | Y | [github.md](integrations/github.md) |
| pihole | DNS | Y | - | Y | - | [pihole.md](integrations/pihole.md) |
| traefik | Proxy | Y | - | - | - | [traefik.md](integrations/traefik.md) |
| ntfy | Notifications | Y | - | Y | - | [ntfy.md](integrations/ntfy.md) |
| tailscale | VPN | Y | - | Y | - | [tailscale.md](integrations/tailscale.md) |
| cloudflare | DNS/CDN | Y | - | Y | Y | [cloudflare.md](integrations/cloudflare.md) |
| ollama | AI/LLM | Y | - | Y | Y | [ollama.md](integrations/ollama.md) |
| open-webui | AI/LLM | Y | - | - | - | [open-webui.md](integrations/open-webui.md) |
| keepalived | HA | - | - | Y | - | [keepalived.md](integrations/keepalived.md) |
| zfs | Storage | - | - | Y | - | [zfs.md](integrations/zfs.md) |
| systemctl | Services | - | - | Y | - | [systemctl.md](integrations/systemctl.md) |
| ms-graph | M365/Entra | Y | - | Y | Y | [ms-graph.md](integrations/ms-graph.md) |
| powershell | Scripting | - | - | Y | Y | [powershell.md](integrations/powershell.md) |
| exchange-online | Email | Y | - | Y | Y | [exchange-online.md](integrations/exchange-online.md) |
| nuclei | Security | - | - | Y | - | [nuclei.md](integrations/nuclei.md) |
| trivy | Security | - | - | Y | - | [trivy.md](integrations/trivy.md) |
| openvas | Security | Y | - | Y | - | [openvas.md](integrations/openvas.md) |
| shodan | OSINT | Y | - | Y | Y | [shodan.md](integrations/shodan.md) |
| mkdocs | Documentation | - | - | Y | Y | [mkdocs.md](integrations/mkdocs.md) |
| mermaid | Diagrams | - | - | Y | - | [mermaid.md](integrations/mermaid.md) |
| certbot | Certificates | - | - | Y | - | [certbot.md](integrations/certbot.md) |

---

## By Category

### Virtualization & Compute

| Tool | Best For | In Use |
|------|----------|:------:|
| **proxmox-api** | VM/CT management, cluster operations | Y |

**Agent recommendation**: Use pvesh CLI for quick operations, REST API for automation scripts.

### Storage

| Tool | Best For | In Use |
|------|----------|:------:|
| **truenas-api** | Dataset management, replication, snapshots | Y |
| **zfs** | Pool/dataset CLI operations | Y |

**Agent recommendation**: TrueNAS API for scheduled tasks and monitoring. ZFS CLI for direct host operations.

### Networking & DNS

| Tool | Best For | In Use |
|------|----------|:------:|
| **pihole** | DNS management, ad blocking, custom records | Y |
| **traefik** | Reverse proxy, SSL, auth middleware | Y |
| **keepalived** | VIP management, HA failover | Y |
| **tailscale** | VPN mesh, remote access | Y |
| **cloudflare** | External DNS, tunnels, DDoS protection | Y |
| **certbot** | SSL certificate management | Y |

**Agent recommendation**: Pi-hole API for DNS changes. Traefik API for routing inspection. Tailscale CLI for VPN management.

### Containers & Orchestration

| Tool | Best For | In Use |
|------|----------|:------:|
| **docker** | Container lifecycle, compose stacks | Y |

**Agent recommendation**: Docker CLI for direct operations. Compose for multi-container stacks.

### Automation & CI/CD

| Tool | Best For | In Use |
|------|----------|:------:|
| **ansible** | Configuration management, patching | Y |
| **github** | Source control, CI/CD workflows, PRs | Y |

**Agent recommendation**: Ansible for infrastructure tasks. GitHub Actions for application CI/CD.

### AI / LLM

| Tool | Best For | In Use |
|------|----------|:------:|
| **ollama** | Local LLM model management and inference | Y |
| **open-webui** | Chat interface for Ollama models | Y |

**Agent recommendation**: Ollama REST API for model operations. Open WebUI for user-facing chat.

### Monitoring & Notifications

| Tool | Best For | In Use |
|------|----------|:------:|
| **ntfy** | Push notifications, alert routing | Y |
| **systemctl** | Service management, systemd timers | Y |

**Agent recommendation**: ntfy REST API for programmatic alerts. systemctl for service lifecycle.

### M365 / Entra ID

| Tool | Best For | In Use |
|------|----------|:------:|
| **ms-graph** | User/group management, conditional access | Planned |
| **powershell** | M365 admin automation | Planned |
| **exchange-online** | Exchange Online management | Planned |

**Agent recommendation**: Microsoft.Graph PowerShell module for admin tasks. Graph API for automation.

### Security & OSINT

| Tool | Best For | In Use |
|------|----------|:------:|
| **nuclei** | Template-based vulnerability scanning | Planned |
| **trivy** | Container and IaC vulnerability scanning | Planned |
| **openvas** | Network vulnerability assessment | Planned |
| **shodan** | External attack surface discovery | Planned |

**Agent recommendation**: Nuclei for targeted scanning. Trivy for container security. Shodan for external recon.

### Documentation

| Tool | Best For | In Use |
|------|----------|:------:|
| **mkdocs** | Static documentation sites | Planned |
| **mermaid** | Architecture and flow diagrams | Y |

**Agent recommendation**: Mermaid for inline diagrams in markdown. MkDocs for published documentation sites.

---

## Quick Start by Use Case

### Check infrastructure health
1. Read [proxmox-api.md](integrations/proxmox-api.md) for cluster status
2. Read [ntfy.md](integrations/ntfy.md) for alert history

### Manage DNS records
1. Read [pihole.md](integrations/pihole.md) for Pi-hole admin API
2. Read [cloudflare.md](integrations/cloudflare.md) for external DNS

### Deploy a new service
1. Read [docker.md](integrations/docker.md) for container deployment
2. Read [traefik.md](integrations/traefik.md) for reverse proxy setup
3. Read [pihole.md](integrations/pihole.md) for DNS record creation

### Run a security scan
1. Read [nuclei.md](integrations/nuclei.md) for vulnerability scanning
2. Read [trivy.md](integrations/trivy.md) for container scanning
3. Read [shodan.md](integrations/shodan.md) for external recon

### Manage M365 tenant
1. Read [ms-graph.md](integrations/ms-graph.md) for Graph API operations
2. Read [powershell.md](integrations/powershell.md) for PowerShell automation

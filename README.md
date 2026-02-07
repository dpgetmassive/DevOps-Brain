# DevOps Brain - Agentic DevOps Toolkit

A collection of AI agent skills for DevOps operations across homelab infrastructure, cloud services, security, and automation. Built for the Get Massive Dojo infrastructure and Cyber People security practice.

Modeled after the [Agent Skills specification](https://agentskills.io/specification.md) and the [Marketing Skills](https://github.com/coreyhaines31/marketingskills) pattern.

## What are Skills?

Skills are markdown files that give AI agents specialized knowledge and workflows for specific DevOps tasks. When installed, agents can recognize infrastructure operations and apply the right procedures, commands, and best practices for your specific environment.

## Available Skills

<!-- SKILLS:START -->
| Domain | Skill | Description |
|--------|-------|-------------|
| **Linux** | [linux-admin](skills/linux/linux-admin/) | User/group management, package operations, filesystem, cron jobs |
| | [linux-hardening](skills/linux/linux-hardening/) | SSH hardening, firewall rules, CIS benchmarks, fail2ban |
| | [linux-networking](skills/linux/linux-networking/) | Interface config, routing, DNS troubleshooting, Tailscale |
| | [systemd-management](skills/linux/systemd-management/) | Service units, timers, journalctl, boot targets |
| **Proxmox** | [proxmox-cluster](skills/proxmox/proxmox-cluster/) | Cluster health, quorum, corosync, node management |
| | [proxmox-vm-management](skills/proxmox/proxmox-vm-management/) | VM/CT lifecycle, templates, cloning, migration |
| | [proxmox-backup-restore](skills/proxmox/proxmox-backup-restore/) | Backup jobs, restore procedures, retention policies |
| | [proxmox-networking](skills/proxmox/proxmox-networking/) | Bridges, VLANs, SDN, PVE firewall |
| **Homelab** | [docker-management](skills/homelab/docker-management/) | Compose stacks, networking, volumes, updates |
| | [dns-management](skills/homelab/dns-management/) | Pi-hole HA, gravity sync, custom DNS, keepalived |
| | [reverse-proxy](skills/homelab/reverse-proxy/) | Traefik, NPM, SSL certificates, Authelia |
| | [storage-management](skills/homelab/storage-management/) | ZFS pools, TrueNAS, replication, NFS/SMB |
| | [monitoring-ops](skills/homelab/monitoring-ops/) | ntfy alerts, dashboards, log analysis, uptime |
| | [homelab-services](skills/homelab/homelab-services/) | Service catalog, dependencies, health checks |
| **M365/Entra** | [entra-admin](skills/m365/entra-admin/) | Users, groups, conditional access, MFA, roles |
| | [m365-admin](skills/m365/m365-admin/) | Exchange, SharePoint, Teams, licensing |
| | [m365-security](skills/m365/m365-security/) | Defender, compliance, audit logs, DLP |
| **AI/LLM** | [llm-hosting](skills/ai/llm-hosting/) | Ollama model management, Open WebUI, resource monitoring |
| | [ai-gateway](skills/ai/ai-gateway/) | clawdbot gateway, model routing, API management |
| | [ai-development](skills/ai/ai-development/) | Agent frameworks, RAG pipelines, prompt engineering |
| **CI/CD** | [ansible-ops](skills/cicd/ansible-ops/) | Playbooks, inventory, vault, patching automation |
| | [github-actions](skills/cicd/github-actions/) | Workflows, secrets, runners, matrix builds |
| | [git-workflow](skills/cicd/git-workflow/) | Branching strategy, PR conventions, releases |
| | [container-ops](skills/cicd/container-ops/) | Dockerfiles, multi-stage builds, image scanning |
| **Security** | [vuln-scanning](skills/security/vuln-scanning/) | Nuclei, Trivy, OpenVAS, CVE tracking |
| | [osint-recon](skills/security/osint-recon/) | Shodan, DNS enumeration, attack surface discovery |
| | [patch-compliance](skills/security/patch-compliance/) | Compliance tracking, reporting, remediation |
| | [hardening-audit](skills/security/hardening-audit/) | CIS benchmarks, SSH audit, configuration review |
| | [smb1001-security-ops](skills/security/smb1001-security-ops/) | SMB1001 controls, evidence collection, compliance |
| **Documentation** | [runbook-writer](skills/documentation/runbook-writer/) | Structured runbooks with verification and rollback |
| | [infra-documentation](skills/documentation/infra-documentation/) | Architecture diagrams, ADRs, service catalogs |
| | [incident-report](skills/documentation/incident-report/) | Post-mortems, root cause analysis, action tracking |
<!-- SKILLS:END -->

## Installation

### Option 1: Clone and Copy

```bash
git clone https://github.com/your-org/gm-agentic-devops-brain.git
cp -r gm-agentic-devops-brain/skills/* .claude/skills/
cp -r gm-agentic-devops-brain/context/ .claude/context/
```

### Option 2: Git Submodule

```bash
git submodule add https://github.com/your-org/gm-agentic-devops-brain.git .claude/devops-brain
```

### Option 3: Direct Reference

Point your AI agent's skill path to this repository's `skills/` directory.

## Usage

Once installed, ask your AI agent to help with DevOps tasks:

```
"Check the health of the Proxmox cluster"
-> Uses proxmox-cluster skill

"Harden SSH on the new container"
-> Uses linux-hardening skill

"Set up a backup job for VM 100"
-> Uses proxmox-backup-restore skill

"Run a vulnerability scan on the homelab"
-> Uses vuln-scanning skill

"Write a runbook for TrueNAS failover"
-> Uses runbook-writer skill
```

## Environment Context

The `context/` directory contains environment-specific information that makes skills produce accurate, targeted output instead of generic documentation:

- **[infrastructure-context.md](context/infrastructure-context.md)** - Host registry, IPs, roles, OS versions
- **[network-map.md](context/network-map.md)** - Network topology, VLANs, VIPs, DNS
- **[service-inventory.md](context/service-inventory.md)** - Running services, ports, dependencies

## Tool Integrations

The `tools/` directory contains integration guides for DevOps tools:

- **[REGISTRY.md](tools/REGISTRY.md)** - Central index of all tools with capability matrix
- **[integrations/](tools/integrations/)** - Per-tool guides with API endpoints, auth, and operations

## Key Design Principle

Each skill answers: "Given the current state of THIS environment, what EXACTLY should be done, and how do I verify it worked?" -- not generic documentation.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding or improving skills.

## License

MIT

---

**Last Updated**: 2026-02-07
**Version**: 1.0.0
**Maintained by**: Get Massive Dojo Infrastructure Team

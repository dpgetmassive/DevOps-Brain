# DevOps Brain -- User Guide

A practical guide to getting the most out of the DevOps Brain agentic toolkit. Written for an engineer who has access to the toolkit and wants to understand how to think about, interact with, and get predictable results from it.

---

## What Is This?

DevOps Brain is a library of **32 agent skills** and **25 tool integration guides** that turn a general-purpose AI coding assistant into an environment-aware DevOps operator. Instead of getting generic "how to use Proxmox" answers, your agent produces commands with the correct IPs, SSH aliases, service names, and verification steps for the Get Massive Dojo homelab and Cyber People infrastructure.

The key difference between this and a wiki: **skills are instructions for an AI agent, not documentation for a human.** The agent reads the skill, reads your environment context, and produces targeted operational output. You are the pilot; the skills are the flight manual the copilot has memorized.

---

## How It Works

### The Context-First Pattern

Every skill depends on three context files that describe your specific environment:

| File | What It Contains | When It's Read |
|------|-----------------|----------------|
| `context/infrastructure-context.md` | Every host, IP, SSH alias, VM/CT ID, role | Always (before any skill) |
| `context/network-map.md` | Subnets, VLANs, VIPs, DNS records, proxy routing | Networking and service tasks |
| `context/service-inventory.md` | Running services with ports, health checks, dependencies | Service management tasks |

**This is the single most important concept.** When your context files are accurate, skills produce accurate output. When they drift, output drifts. Treat context files as living documents -- update them when you add a host, change an IP, or deploy a new service.

### The Three Layers

```
┌─────────────────────────────────────────────┐
│  YOU (natural language request)              │
├─────────────────────────────────────────────┤
│  SKILLS (32 domain-specific instruction     │
│  sets with guard rails, procedures,         │
│  verification, and rollback)                │
├─────────────────────────────────────────────┤
│  CONTEXT (your actual environment --        │
│  hosts, IPs, services, topology)            │
├─────────────────────────────────────────────┤
│  TOOLS (25 integration guides with         │
│  API endpoints, CLI commands, auth)         │
└─────────────────────────────────────────────┘
```

You talk to the agent. The agent reads the relevant skill. The skill references context files for environment data and tool integrations for API/CLI details. The agent produces environment-specific commands and procedures.

---

## When to Use Which Skill

### "I need to do something on a Linux host"

| What You Want | Skill | Example Prompt |
|--------------|-------|----------------|
| Install packages, manage users, check disk | `linux-admin` | "Check disk space on all hosts" |
| Lock down SSH, set up firewall, fail2ban | `linux-hardening` | "Harden SSH on the new container" |
| Fix networking, DNS, Tailscale issues | `linux-networking` | "CT 118 can't resolve DNS" |
| Manage systemd services, timers, logs | `systemd-management` | "Create a systemd timer for the backup script" |

### "I need to do something with Proxmox"

| What You Want | Skill | Example Prompt |
|--------------|-------|----------------|
| Check cluster health, quorum, failover | `proxmox-cluster` | "Is the cluster healthy?" |
| Create, clone, migrate, resize VMs/CTs | `proxmox-vm-management` | "Clone CT 200 to create a test proxy" |
| Backup, restore, check retention | `proxmox-backup-restore` | "Restore VM 100 from yesterday's backup" |
| Bridges, VLANs, VM networking | `proxmox-networking` | "Put the new CT on VLAN 66" |

### "Something is wrong / I need to check status"

| What You Want | Skill | Example Prompt |
|--------------|-------|----------------|
| Check all monitoring, alerts, dashboard | `monitoring-ops` | "What does the daily readiness check say?" |
| See what's running, dependencies, health | `homelab-services` | "Full infrastructure health sweep" |
| DNS not working, VIP issues | `dns-management` | "DNS isn't resolving through the VIP" |
| Backup failure, storage full | `storage-management` | "Why did replication fail last night?" |

### "I need to write or build something"

| What You Want | Skill | Example Prompt |
|--------------|-------|----------------|
| Write a Dockerfile, scan images | `container-ops` | "Write a multi-stage Dockerfile for the API" |
| Set up CI/CD pipeline | `github-actions` | "Create a deploy workflow for the staging server" |
| Automate with Ansible | `ansible-ops` | "Write a playbook to deploy Fail2ban everywhere" |
| Create operational documentation | `runbook-writer` | "Write a runbook for TrueNAS failover" |
| Draw architecture diagrams | `infra-documentation` | "Create a Mermaid diagram of the backup flow" |

### "I need to check security posture"

| What You Want | Skill | Example Prompt |
|--------------|-------|----------------|
| Scan for vulnerabilities | `vuln-scanning` | "Scan the Proxmox web UIs for known CVEs" |
| External attack surface | `osint-recon` | "What's externally visible for gmdojo.tech?" |
| Are hosts patched? | `patch-compliance` | "Generate a compliance report for all hosts" |
| Audit configurations | `hardening-audit` | "Run a security audit on pve-scratchy" |
| SMB1001 evidence | `smb1001-security-ops` | "Collect evidence for SMB1001 Device Security" |

---

## How to Interact With It

### Be Specific About What and Where

The more specific your request, the more targeted the output.

| Vague (works, but generic) | Specific (best results) |
|---------------------------|------------------------|
| "Check backups" | "Check if last night's Proxmox backup for VM 100 completed" |
| "Fix DNS" | "Pi-hole VIP isn't responding on 10.16.1.15" |
| "Harden the server" | "Harden SSH on CT 122 (authelia)" |
| "Set up monitoring" | "Add a systemd timer on n100uck to check NFS mount health" |

### Let the Agent Read Context

You don't need to recite IPs or hostnames. The agent reads context files. Just use the names you know:

- "Check TrueNAS replication status" -- the agent knows Primary is 10.16.1.6 and DR is 10.16.1.20
- "Restart the backup NPM" -- the agent knows that's a Docker container on n100uck
- "What's the cluster quorum status?" -- the agent knows to check pve-scratchy and the qnetd on n100uck

### Multi-Step Operations

For complex tasks, describe the outcome you want. The skill's built-in verification and rollback patterns will structure the execution:

- "Migrate VM 100 from pve-scratchy to pve-itchy" -- the agent will check prerequisites, perform the migration, and verify
- "Deploy a new service behind the reverse proxy" -- the agent will combine docker-management, dns-management, and reverse-proxy skills

---

## What to Think About Before Starting a Task

### 1. Is This Read-Only or State-Changing?

Every skill defines **guard rails**:

- **Auto-approve** operations are safe to run anytime: status checks, logs, queries, listing resources. The agent will execute these without hesitation.
- **Confirm first** operations change state: reboots, deletions, firewall changes, bulk operations. The agent should pause and ask you before executing these.

If you're exploring or diagnosing, say so: "Just check the status, don't change anything."

### 2. Which Host Am I Targeting?

Be clear about the target. The homelab has multiple Docker hosts, multiple Proxmox nodes, and services spread across 30+ IPs. Ambiguity here is the #1 source of wrong commands.

Good: "Check Docker containers on gm-ai"
Risky: "Check Docker containers" (which of the 4 Docker hosts?)

### 3. Do I Need a Snapshot First?

Before any change to a running VM or container, consider asking for a snapshot. It's cheap insurance:

```
"Snapshot CT 200 before we change the NPM config"
```

The proxmox-vm-management skill includes snapshot operations. Several skills prompt for this automatically before destructive operations.

### 4. What's My Rollback Plan?

Every operational skill includes rollback instructions, but think about it yourself:

- **Config change?** The agent backs up the file first.
- **Service change?** Note the current state so you can revert.
- **Network change?** Have console access ready in case SSH breaks.
- **Cluster change?** Understand quorum implications.

### 5. Is This a Good Time?

Check the daily schedule in `context/infrastructure-context.md`:

| Window | What Happens |
|--------|-------------|
| 01:30 - 02:45 AM | Infrastructure orchestration and ZFS replication |
| 02:45 - 04:00 AM | Proxmox backups and CloudSync |
| 06:00 - 06:45 AM | Monitoring checks (backup, data protection, readiness) |

Avoid making storage, backup, or replication changes during these windows. VM migrations during backup windows can cause failures.

---

## Understanding the Skill Anatomy

Every skill follows the same structure. Knowing this helps you predict what the agent will do:

```
1. Read context files (environment awareness)
2. Check guard rails (safe to proceed?)
3. Verify before (what's the current state?)
4. Execute operation (the actual task)
5. Verify after (did it work?)
6. Suggest rollback if needed (what if it didn't?)
```

When you see the agent running verification commands before your requested operation, that's the skill working as designed. Don't skip these -- they catch problems early.

---

## The Tool Registry

Skills tell the agent *what* to do. Tool integrations tell it *how* to talk to specific systems. The 25 tool guides in `tools/integrations/` provide:

- **API endpoints** with real URLs and authentication methods
- **CLI commands** with actual syntax and flags
- **Common operations** as copy-paste code blocks
- **Rate limits** to avoid hitting throttles

You rarely need to read tool integrations yourself. They're agent reference material. But if you're curious how the agent will interact with a specific system, check the relevant integration guide.

---

## Keeping It Accurate

### When to Update Context Files

Update `context/` files whenever you:

- Add or remove a host
- Change an IP address
- Deploy a new service
- Change a port or protocol
- Modify the backup schedule
- Add a new DNS record
- Change the network topology

The agent cannot know about changes it hasn't been told about. Stale context is the most common cause of incorrect commands.

### When to Update Skills

Update a skill when:

- A procedure changes (new tool version, different commands)
- You discover a better approach through experience
- A new edge case or failure mode emerges
- Environment changes make existing instructions inaccurate

### Version Tracking

`VERSIONS.md` tracks every skill version. Increment the version when making meaningful changes. This lets agents detect when skills have been updated.

---

## Domain-Specific Notes

### Homelab (Most Mature)

The Linux, Proxmox, and Homelab skills are the most detailed because they're built from extensive existing documentation. Context files are populated with real infrastructure data. These skills should produce highly accurate output immediately.

### Security / SMB1001 (Bridges to Cyber People)

The `smb1001-security-ops` skill is designed to automate evidence collection across the 5 SMB1001 security pillars. It connects to the `smb1001-gap-analysis` and `smb1001-assessment-agent` projects. If you're working on client assessments, start here to understand how operational checks map to certification controls.

### AI/LLM (Needs Discovery)

The `ai-gateway` skill for clawdbot is partially templated -- the exact port, Docker Compose configuration, and routing setup need to be discovered by SSH'ing into gm-ai. Run the discovery commands in the skill to fill in the gaps, then update the skill and context files with what you find.

### M365/Entra (Needs Tenant Details)

M365 skills provide complete PowerShell workflows but need tenant-specific data (tenant ID, subscription level, existing policies) populated in the context. These skills are fully functional once you connect to a tenant.

---

## Common Patterns

### "Morning Check" Routine

```
"What's the daily readiness status?"
```

This triggers `monitoring-ops` which reads the aggregated state from all 5 monitors on n100uck. One command, full infrastructure status.

### "Something Broke" Troubleshooting

```
"DNS isn't working"
```

The agent will follow a diagnostic chain: test VIP, test each Pi-hole, check keepalived, check services, check resolv.conf on affected hosts. Every skill includes a Troubleshooting section with exactly this kind of systematic approach.

### "New Service" Deployment

```
"Deploy a new web app on Docker, behind the reverse proxy, with DNS"
```

This chains multiple skills: `docker-management` (deploy), `dns-management` (add record), `reverse-proxy` (add proxy host), and verifies each step.

### "Security Review" for a Client

```
"Run a full SMB1001 evidence collection for the homelab"
```

The `smb1001-security-ops` skill runs automated checks across all 5 pillars, producing structured output that maps directly to SMB1001 control IDs.

---

## Tips for Best Results

1. **Start with status checks.** Before changing anything, ask the agent to check the current state. This builds shared understanding and catches issues early.

2. **Trust the guard rails.** If a skill says "confirm first," the agent should ask you before proceeding. Don't bypass this for speed.

3. **Update context after changes.** If you add a host manually, tell the agent to update the context files. Future operations will be more accurate.

4. **Use the right skill scope.** If you ask a `linux-admin` question that's really a `systemd-management` task, the agent might give you a cron-based answer instead of a timer-based one. The skill's `description` field tells you exactly when to use it.

5. **Check related skills.** Every skill ends with a "Related Skills" section. If the agent's output doesn't quite match what you need, the answer might be in an adjacent skill.

6. **Don't fight the SSH pattern.** Every command runs through `ssh <alias> "<command>"`. This is deliberate -- it ensures you're running on the right host, with the right user, every time. The aliases are defined in `~/.ssh/config` and the agent knows them from context.

7. **Iterate on skills.** If a skill's output is consistently missing something, improve the skill. This is a toolkit that gets better with use.

---

## Architecture at a Glance

```
gm-agentic-devops-brain/
├── context/                          # YOUR environment (update this!)
│   ├── infrastructure-context.md     # Hosts, IPs, roles
│   ├── network-map.md               # Network topology
│   └── service-inventory.md         # Services, ports, dependencies
│
├── skills/                           # Agent instruction sets
│   ├── linux/ (4)                    # OS administration
│   ├── proxmox/ (4)                  # Virtualization
│   ├── homelab/ (6)                  # Infrastructure services
│   ├── m365/ (3)                     # Microsoft 365
│   ├── ai/ (3)                       # AI/LLM hosting
│   ├── cicd/ (4)                     # Automation and pipelines
│   ├── security/ (5)                 # Security and compliance
│   └── documentation/ (3)           # Operational documentation
│
├── tools/                            # Tool reference material
│   ├── REGISTRY.md                   # Capability matrix (25 tools)
│   └── integrations/                 # Per-tool API/CLI guides
│
├── README.md                         # Project overview
├── AGENTS.md                         # Guidelines for AI agents
├── VERSIONS.md                       # Skill version tracking
└── CONTRIBUTING.md                   # How to add/improve skills
```

**32 skills. 25 tool integrations. 3 context files. One brain.**

---

**Last Updated**: 2026-02-07

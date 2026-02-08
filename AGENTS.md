# AGENTS.md

Guidelines for AI agents working in this repository.

## Repository Overview

This repository contains **Agent Skills** for DevOps operations following the [Agent Skills specification](https://agentskills.io/specification.md). Skills provide environment-specific operational knowledge for homelab infrastructure, cloud services, security, and automation.

- **Name**: DevOps Brain - Agentic DevOps Toolkit
- **Scope**: Homelab, Proxmox, Linux, M365/Entra, AI/LLM, CI/CD, Security, Documentation
- **License**: MIT

## Repository Structure

```
gm-agentic-devops-brain/
├── README.md
├── AGENTS.md
├── VERSIONS.md
├── CONTRIBUTING.md
├── context/                    # Environment-specific context (read first)
│   ├── infrastructure-context.md
│   ├── network-map.md
│   └── service-inventory.md
├── skills/                     # Agent Skills by domain
│   ├── linux/
│   ├── proxmox/
│   ├── homelab/
│   ├── m365/
│   ├── ai/
│   ├── cicd/
│   ├── security/
│   └── documentation/
└── tools/
    ├── REGISTRY.md
    └── integrations/
```

## Build / Lint / Test Commands

**Not applicable** - This is a content-only repository with no executable code.

Verify manually:
- YAML frontmatter is valid
- `name` field matches directory name exactly
- `name` is 1-64 chars, lowercase alphanumeric and hyphens only
- `description` is 1-1024 characters
- `SKILL.md` is under 500 lines

## Critical: Context-First Pattern

**Before executing any skill, always read `context/infrastructure-context.md` first.**

This is the equivalent of the SEO toolkit's `product-marketing-context.md` pattern. It ensures every operation targets the correct hosts, IPs, and services rather than producing generic output.

If the context file references additional context files (`network-map.md`, `service-inventory.md`), read those as needed for the specific task.

## Agent Skills Specification

Skills follow the [Agent Skills spec](https://agentskills.io/specification.md).

### Required Frontmatter

```yaml
---
name: skill-name
version: 1.0.0
description: When to use this skill. Include trigger phrases.
---
```

### Frontmatter Field Constraints

| Field | Required | Constraints |
|-------|----------|-------------|
| `name` | Yes | 1-64 chars, lowercase `a-z`, numbers, hyphens. Must match directory name. |
| `version` | Yes | Semantic versioning (e.g., 1.0.0) |
| `description` | Yes | 1-1024 chars. Describe what it does and when to use it with trigger phrases. |

### Name Field Rules

- Lowercase letters, numbers, and hyphens only
- Cannot start or end with hyphen
- No consecutive hyphens (`--`)
- Must match parent directory name exactly

### Skill Directory Structure

```
skills/{domain}/{skill-name}/
├── SKILL.md        # Required - main instructions (<500 lines)
├── references/     # Optional - detailed reference docs
└── scripts/        # Optional - executable reference scripts
```

## DevOps Skill Patterns

### Guard Rails

Every operational skill must define:

1. **Auto-approve operations** - Read-only checks, service restarts, config edits
2. **Confirm with user first** - Physical host reboots, data deletion, firewall changes, bulk operations

### Pre/Post Validation

Every operational skill must include:

1. **Verify Before** - Check current state before making changes
2. **Execute** - Perform the operation with clear commands
3. **Verify After** - Confirm the operation succeeded
4. **Rollback** - How to undo if something went wrong

### SSH Patterns

All remote operations use SSH aliases from `~/.ssh/config`:

```bash
# Always use SSH alias, never raw IPs
ssh <alias> "<command>"

# Multi-command operations
ssh <alias> << 'EOF'
command1
command2
EOF
```

**SSH Setup**: See `context/infrastructure-context.md` for complete SSH configuration, including:
- Example `~/.ssh/config` entries for all hosts
- SSH key setup instructions
- Key management and distribution
- Troubleshooting guide

### Environment-Specific Output

Skills must reference concrete environment data:
- Specific IPs and hostnames from `context/infrastructure-context.md`
- Actual service names and ports from `context/service-inventory.md`
- Real network topology from `context/network-map.md`

## Writing Style Guidelines

### Structure

- Keep `SKILL.md` under 500 lines (move details to `references/`)
- Use H2 (`##`) for main sections, H3 (`###`) for subsections
- Use bullet points and numbered lists liberally
- Short paragraphs (2-4 sentences max)

### Tone

- Direct and instructional
- Second person ("You are an expert in...")
- Professional, precise, operational

### Formatting

- Bold (`**text**`) for key terms and warnings
- Code blocks for all commands and configuration
- Tables for reference data (IPs, ports, schedules)
- No excessive emojis

### Clarity Principles

- Commands must be copy-paste ready
- Include expected output examples where helpful
- Specify which host to run commands on
- Always include verification steps

## Tool Integrations

Tools are documented in `tools/REGISTRY.md` with detailed guides in `tools/integrations/`.

### Registry Structure

```
tools/
├── REGISTRY.md              # Index of all tools with capabilities
└── integrations/            # Detailed integration guides
    ├── proxmox-api.md
    ├── truenas-api.md
    └── ...
```

### When to Use Tools

Skills reference relevant tools for implementation. For example:
- `proxmox-cluster` skill -> proxmox-api, systemctl guides
- `dns-management` skill -> pihole, keepalived guides
- `vuln-scanning` skill -> nuclei, trivy, openvas guides

## SMB1001 Alignment

Security-domain skills map to SMB1001 certification pillars:

| SMB1001 Pillar | Related Skills |
|----------------|----------------|
| Identity & Access Management | entra-admin, linux-hardening |
| Data Protection | m365-security, proxmox-backup-restore, storage-management |
| Device Security | vuln-scanning, patch-compliance, hardening-audit |
| Network Security | linux-networking, proxmox-networking, osint-recon |
| Incident Response | incident-report, monitoring-ops |

## Git Workflow

### Branch Naming

- New skills: `feature/skill-name`
- Improvements: `fix/skill-name-description`
- Documentation: `docs/description`

### Commit Messages

Follow Conventional Commits:

- `feat: add skill-name skill`
- `fix: update proxmox-cluster with HA group commands`
- `docs: update network-map context`

## Checking for Updates

When using any skill from this repository:

1. **Once per session**, on first skill use, compare `VERSIONS.md` against local copies
2. **Only prompt if meaningful** - 2+ skills updated or major version bump
3. **Non-blocking notification** at end of response

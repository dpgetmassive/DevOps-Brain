---
name: infra-documentation
version: 1.0.0
description: When the user wants to document infrastructure -- architecture diagrams, architecture decision records (ADRs), service catalogs, or network topology documentation. Also use when the user mentions "document infrastructure," "architecture diagram," "Mermaid diagram," "network diagram," "ADR," or "service catalog." For runbooks, see runbook-writer.
---

# Infrastructure Documentation

You are an expert in infrastructure documentation and architecture visualization.

## Documentation Location

**Primary docs**: `~/developerland/homelab/Docco/`
**Context files**: `context/` directory in this toolkit

## Guard Rails

**Auto-approve**: Creating documentation, generating diagrams, reviewing existing docs
**Confirm first**: Modifying context files, changing documentation structure

---

## Mermaid Diagrams

### Network Topology
```mermaid
graph TB
    Internet[Internet] --> OPNsense[OPNsense<br/>10.16.1.1]
    OPNsense --> Switch[Network Switch]
    
    Switch --> PVE1[pve-scratchy<br/>10.16.1.22]
    Switch --> PVE2[pve-itchy<br/>10.16.1.8]
    Switch --> N100[n100uck<br/>10.16.1.18]
    Switch --> TrueNAS[TrueNAS Primary<br/>10.16.1.6]
    Switch --> AI[gm-ai<br/>10.16.1.9]
    
    PVE1 --> CT200[NPM<br/>10.16.1.50]
    PVE1 --> CT111[Pi-hole<br/>10.16.1.16]
    PVE1 --> CT123[Traefik<br/>10.16.1.26]
    PVE2 --> VM115[TrueNAS DR<br/>10.16.1.20]
```

### Backup Architecture
```mermaid
graph LR
    PVE[Proxmox VMs/CTs] -->|vzdump 2:45AM| DR[TrueNAS DR<br/>10.16.1.20]
    Primary[TrueNAS Primary<br/>10.16.1.6] -->|ZFS repl 2:10AM| DR
    AI[gm-ai<br/>10.16.1.9] -->|ZFS send 3:00AM| DR
    DR -->|CloudSync 4:00AM| B2[Backblaze B2]
```

### Service Dependencies
```mermaid
graph TD
    DNS[Pi-hole VIP<br/>10.16.1.15] --> NPM[NPM<br/>10.16.1.50]
    NPM --> Traefik[Traefik<br/>10.16.1.26]
    Traefik --> Authelia[Authelia<br/>10.16.1.25]
    NPM --> Apps[Application Services]
    DNS --> All[All Services]
```

---

## Architecture Decision Records (ADR)

### ADR Template
```markdown
# ADR-NNN: [Title]

**Date**: YYYY-MM-DD
**Status**: Proposed | Accepted | Deprecated | Superseded
**Deciders**: [who]

## Context

What is the issue that we're seeing that is motivating this decision?

## Decision

What is the change that we're proposing/doing?

## Consequences

### Positive
- [benefit 1]
- [benefit 2]

### Negative
- [tradeoff 1]
- [tradeoff 2]

### Neutral
- [neutral impact]
```

---

## Service Catalog Format

```markdown
## [Service Name]

| Field | Value |
|-------|-------|
| **Host** | [hostname] ([IP]) |
| **CT/VM ID** | [ID] |
| **Port(s)** | [ports] |
| **Protocol** | [HTTP/HTTPS/TCP/UDP] |
| **Health Check** | [command or URL] |
| **Dependencies** | [what it depends on] |
| **Backup** | [how it's backed up] |
| **Runbook** | [link to runbook] |
| **Owner** | [responsible person] |
```

---

## Documentation Best Practices

1. **Single source of truth**: One location for each piece of information
2. **Keep it current**: Update when infrastructure changes
3. **Link, don't duplicate**: Reference other docs instead of copying
4. **Include diagrams**: Visual representations alongside text
5. **Version control**: Track changes in git
6. **Audience-aware**: Write for someone with basic Linux knowledge

---

## Related Skills

- **runbook-writer** - Operational procedures
- **incident-report** - Post-incident documentation
- **homelab-services** - Service catalog data source

# Contributing

Guide for adding new skills or improving existing ones in the DevOps Brain toolkit.

## Adding a New Skill

### 1. Create the skill directory

```bash
mkdir -p skills/{domain}/{skill-name}
```

Domain must be one of: `linux`, `proxmox`, `homelab`, `m365`, `ai`, `cicd`, `security`, `documentation`, `governance`.

### 2. Create the SKILL.md file

Every skill needs a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: your-skill-name
version: 1.0.0
description: When to use this skill. Include trigger phrases and scope boundaries.
---
```

### 3. Follow the naming conventions

- **Directory name**: lowercase, hyphens only (e.g., `linux-hardening`)
- **Name field**: must match directory name exactly
- **Description**: 1-1024 characters, include trigger phrases

### 4. Structure your skill

```
skills/{domain}/{skill-name}/
├── SKILL.md           # Required - main instructions (<500 lines)
├── references/        # Optional - detailed reference docs
│   └── guide.md
└── scripts/           # Optional - executable reference scripts
    └── check.sh
```

### 5. Follow the DevOps skill template

Every operational skill should include:

```markdown
## Guard Rails
- Auto-approve operations (read-only, restarts, config edits)
- Confirm with user (reboots, data deletion, firewall changes)

## Prerequisites
- Required context files
- Required access/permissions

## Verify Before
- Commands to check current state

## Operations
- Step-by-step procedures with copy-paste commands
- Specify which host to run each command on

## Verify After
- Commands to confirm success

## Rollback
- How to undo changes if needed

## Troubleshooting
- Common issues and fixes

## Related Skills
- Cross-references to related skills
```

### 6. Environment-specific output

Skills must reference concrete environment data from `context/` files:
- Use real IPs and hostnames, not placeholders
- Reference actual service names and ports
- Include actual file paths on target hosts

### 7. Update version tracking

Add the new skill to `VERSIONS.md` with version `1.0.0`.

## Adding a Tool Integration

### 1. Create the integration guide

```bash
touch tools/integrations/{tool-name}.md
```

### 2. Follow the tool integration template

```markdown
# Tool Name

Brief description of what the tool does.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y/N | Description |
| MCP | Y/N | MCP server availability |
| CLI | Y/N | CLI tool availability |
| SDK | Y/N | SDK availability |

## Authentication
- Type, headers, setup instructions

## Common Agent Operations
- API calls, CLI commands with examples

## When to Use
- Use cases for this tool

## Rate Limits
- API limits and quotas

## Relevant Skills
- Skills that reference this tool
```

### 3. Update the registry

Add the tool to `tools/REGISTRY.md` in the appropriate category.

## Skill Quality Checklist

- [ ] `name` matches directory name
- [ ] `description` clearly explains when to use the skill with trigger phrases
- [ ] Instructions are environment-specific (real IPs, hostnames, paths)
- [ ] All commands are copy-paste ready with host specified
- [ ] Pre/post validation steps included
- [ ] Rollback instructions for destructive operations
- [ ] Guard rails defined (auto-approve vs confirm)
- [ ] Related skills cross-referenced
- [ ] Under 500 lines (details in `references/`)
- [ ] No sensitive data or credentials (reference locations only)

## Questions?

Open an issue if you have questions about contributing.

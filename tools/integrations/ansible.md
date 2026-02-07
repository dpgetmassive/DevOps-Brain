# Ansible CLI

Ansible provides infrastructure automation via CLI tools (ansible, ansible-playbook, ansible-vault, ansible-galaxy). Used for configuration management, patching, and orchestration across the homelab infrastructure.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | N | No REST API, CLI-based tool |
| MCP | N | No MCP server available |
| CLI | Y | `ansible`, `ansible-playbook`, `ansible-vault`, `ansible-galaxy` |
| SDK | Y | Python `ansible-core`, `ansible-runner` for programmatic execution |

## Authentication

**SSH Key-based**: Ansible uses SSH keys from `~/.ssh/` for host authentication. All homelab hosts configured with key-based auth.

**Inventory**: Hosts defined in inventory files (INI or YAML format). Default location: `~/developerland/homelab/ansible/patching/inventory.ini`.

**Vault**: Encrypted secrets stored in `ansible-vault` encrypted files. Password stored securely or via `ANSIBLE_VAULT_PASSWORD_FILE`.

**Control Node**: n100uck (10.16.1.18) serves as Ansible control node with inventory and playbooks.

## Common Agent Operations

### Run Ad-Hoc Command

```bash
# Ping all hosts
ansible all -i ~/developerland/homelab/ansible/patching/inventory.ini -m ping

# Run command on specific group
ansible proxmox -i ~/developerland/homelab/ansible/patching/inventory.ini -a "uptime"

# Check package updates on Debian hosts
ansible debian -i ~/developerland/homelab/ansible/patching/inventory.ini -m apt -a "update_cache=yes"
```

### Execute Playbook

```bash
# Run patching playbook
ansible-playbook -i ~/developerland/homelab/ansible/patching/inventory.ini \
  ~/developerland/homelab/ansible/patching/quick_patch_all.yml

# Dry run (check mode)
ansible-playbook -i ~/developerland/homelab/ansible/patching/inventory.ini \
  --check ~/developerland/homelab/ansible/patching/quick_patch_all.yml

# Limit to specific hosts
ansible-playbook -i ~/developerland/homelab/ansible/patching/inventory.ini \
  --limit "pve-scratchy,pve-itchy" \
  ~/developerland/homelab/ansible/patching/quick_patch_all.yml
```

### Inventory and Vault

```bash
# List all hosts
ansible-inventory -i ~/developerland/homelab/ansible/patching/inventory.ini --list

# Encrypt file
ansible-vault encrypt ~/developerland/homelab/ansible/patching/secrets.yml

# Edit encrypted file
ansible-vault edit ~/developerland/homelab/ansible/patching/secrets.yml

# Use vault password file
ansible-playbook -i ~/developerland/homelab/ansible/patching/inventory.ini \
  --vault-password-file ~/.ansible/vault_pass \
  ~/developerland/homelab/ansible/patching/quick_patch_all.yml
```

### Galaxy and Facts

```bash
# Install collection
ansible-galaxy collection install community.general

# Gather facts for all hosts
ansible all -i ~/developerland/homelab/ansible/patching/inventory.ini -m setup

# Get specific fact
ansible all -i ~/developerland/homelab/ansible/patching/inventory.ini -m setup -a "filter=ansible_distribution*"
```

## Key Objects/Metrics

- **Inventory**: Host definitions organized by groups (proxmox, debian, truenas, etc.)
- **Playbooks**: YAML files defining automation tasks
- **Modules**: Built-in and community modules (apt, systemd, copy, template)
- **Facts**: Host information gathered automatically (ansible_facts)
- **Vault**: Encrypted secrets for sensitive data
- **Collections**: Reusable automation content from Ansible Galaxy

## When to Use

- **Configuration management**: Apply consistent configs across multiple hosts
- **Patching automation**: Automated package updates across homelab (19 hosts)
- **Service management**: Start/stop/restart services on multiple hosts
- **File distribution**: Copy configs, scripts, or files to multiple hosts
- **Discovery**: Auto-discover hosts from Proxmox and update inventory
- **Reporting**: Generate status reports across infrastructure

## Rate Limits

No explicit rate limits. Ansible handles:
- Sequential execution by default (use `-f` for parallel forks)
- SSH connection pooling via ControlMaster
- Recommended: 5-10 parallel forks for homelab scale

## Relevant Skills

- `ansible-ops` - Playbook development and execution
- `patch-compliance` - Automated patching workflows
- `monitoring-ops` - Infrastructure health checks via Ansible
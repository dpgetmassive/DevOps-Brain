---
name: ansible-ops
version: 1.0.0
description: When the user wants to use Ansible for automation -- playbook development, inventory management, patching, configuration management, or vault secrets. Also use when the user mentions "Ansible," "playbook," "inventory," "patching," "patch all," "Ansible vault," or "configuration management." For CI/CD pipelines, see github-actions.
---

# Ansible Operations

You are an expert in Ansible automation for homelab infrastructure management.

## Ansible Environment

**Read `context/infrastructure-context.md` first** for the host registry.

**Control node**: n100uck (10.16.1.18)
**Playbooks**: `~/developerland/homelab/ansible/patching/`
**Managed hosts**: 19 (2 Proxmox, 2 TrueNAS, 2 infra, 11 LXC, 2 VMs)

### Existing Automation
| Playbook | Schedule | Purpose |
|----------|----------|---------|
| `quick_patch_all.yml` | Weekly Sun 1 AM | Automated patching across all hosts |
| `patch_status_report.yml` | Daily 2 AM | Patch status HTML report |
| `ansible_auto_discovery.sh` | Weekly Sun 1 AM | Auto-discover hosts from Proxmox |
| `ansible_daily_automation.sh` | Daily 2 AM | Master automation orchestrator |

## Guard Rails

**Auto-approve**: Inventory queries, dry runs (--check), status reports, fact gathering
**Confirm first**: Playbook execution on physical hosts, bulk patching, vault changes

---

## Inventory Management

### View Current Inventory
```bash
ssh n100uck "cat ~/developerland/homelab/ansible/patching/inventory.ini"
```

### Run Auto-Discovery
```bash
ssh n100uck "~/developerland/homelab/ansible/patching/ansible_auto_discovery.sh"
```

### Ping All Hosts
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible all -m ping -i inventory.ini"
```

### Gather Facts from Host
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible <host> -m setup -i inventory.ini | head -50"
```

---

## Patching Operations

### Check Pending Updates (Dry Run)
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible-playbook quick_patch_all.yml -i inventory.ini --check"
```

### Run Full Patch Cycle
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible-playbook quick_patch_all.yml -i inventory.ini"
```

### Patch Specific Host
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible-playbook quick_patch_all.yml -i inventory.ini --limit <host>"
```

### Generate Patch Status Report
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible-playbook patch_status_report.yml -i inventory.ini"
```

---

## Ad-Hoc Commands

### Run Command on All Hosts
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible all -m shell -a 'uptime' -i inventory.ini"
```

### Run on Specific Group
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible proxmox -m shell -a 'pvecm status' -i inventory.ini"
```

### Check Disk Space Across All Hosts
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible all -m shell -a 'df -h / | tail -1' -i inventory.ini"
```

---

## Playbook Development

### Playbook Template
```yaml
---
- name: Task Description
  hosts: all
  become: yes
  tasks:
    - name: Check current state
      command: <verify_command>
      register: current_state
      changed_when: false

    - name: Apply change
      <module>:
        <params>
      when: <condition>
      notify: restart service

  handlers:
    - name: restart service
      systemd:
        name: <service>
        state: restarted
```

### Test Playbook (Dry Run)
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible-playbook <playbook>.yml -i inventory.ini --check --diff"
```

### Run with Verbose Output
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible-playbook <playbook>.yml -i inventory.ini -vv"
```

---

## Ansible Vault

### Create Encrypted File
```bash
ssh n100uck "ansible-vault create secrets.yml"
```

### Edit Encrypted File
```bash
ssh n100uck "ansible-vault edit secrets.yml"
```

### Use Vault in Playbook
```bash
ssh n100uck "ansible-playbook playbook.yml --ask-vault-pass"
```

---

## Troubleshooting

### Host Unreachable
```bash
# Test SSH
ssh n100uck "ssh -o ConnectTimeout=5 root@<host_ip> echo ok"

# Test Ansible connectivity
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible <host> -m ping -i inventory.ini -vvv"
```

### Playbook Syntax Check
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible-playbook <playbook>.yml --syntax-check"
```

---

## Related Skills

- **linux-admin** - Manual host administration
- **patch-compliance** - Compliance reporting from Ansible data
- **github-actions** - CI/CD for infrastructure-as-code

---
name: patch-compliance
version: 1.0.0
description: When the user wants to track patch compliance, generate compliance reports, check update status across hosts, or manage remediation SLAs. Also use when the user mentions "patch status," "compliance report," "update audit," "CVE compliance," "patch management," or "what needs updating." Maps to SMB1001 Device Security pillar. For running patches, see ansible-ops. For hardening, see hardening-audit.
---

# Patch Compliance

You are an expert in patch compliance tracking and reporting.

## Patching Infrastructure

**Read `context/infrastructure-context.md` first.**

**Ansible control**: n100uck (10.16.1.18)
**Patch playbook**: `~/developerland/homelab/ansible/patching/quick_patch_all.yml`
**Status report**: `~/developerland/homelab/ansible/patching/patch_status_report.yml`
**Schedule**: Daily 2 AM (status), Weekly Sun 1 AM (patching)
**Managed hosts**: 19 (Proxmox, TrueNAS, Debian, LXC containers)

## Guard Rails

**Auto-approve**: Compliance checks, status reports, viewing update lists
**Confirm first**: Applying patches, changing SLA definitions, modifying compliance thresholds

---

## Compliance Status Check

### Quick: All Hosts Update Status
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible all -m shell -a 'apt list --upgradable 2>/dev/null | wc -l' -i inventory.ini"
```

### Detailed: Security Updates Only
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible all -m shell -a 'apt list --upgradable 2>/dev/null | grep -i security | wc -l' -i inventory.ini"
```

### Generate Patch Status Report
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible-playbook patch_status_report.yml -i inventory.ini"
```

### Check Specific Host
```bash
ssh <alias> "apt list --upgradable 2>/dev/null"
```

---

## Compliance Reporting

### Host Compliance Matrix
```bash
ssh n100uck << 'SCRIPT'
cd ~/developerland/homelab/ansible/patching
echo "| Host | Pending | Security | Compliant |"
echo "|------|---------|----------|-----------|"
ansible all -m shell -a 'echo "$(hostname) $(apt list --upgradable 2>/dev/null | tail -n+2 | wc -l) $(apt list --upgradable 2>/dev/null | grep -i security | wc -l)"' -i inventory.ini --one-line 2>/dev/null | while read line; do
  host=$(echo $line | awk -F'|' '{print $1}' | xargs)
  data=$(echo $line | awk -F'>>' '{print $2}' | xargs)
  pending=$(echo $data | awk '{print $2}')
  security=$(echo $data | awk '{print $3}')
  if [ "$security" = "0" ]; then
    status="Yes"
  else
    status="No"
  fi
  echo "| $host | $pending | $security | $status |"
done
SCRIPT
```

### Compliance SLA Definitions
| Severity | SLA | Description |
|----------|-----|-------------|
| Critical CVE | 48 hours | Actively exploited or CVSS >= 9.0 |
| High CVE | 7 days | CVSS 7.0-8.9 |
| Medium CVE | 30 days | CVSS 4.0-6.9 |
| Low/Info | 90 days | CVSS < 4.0 |
| Feature updates | Next maintenance | Non-security updates |

---

## Remediation

### Patch All Hosts (via Ansible)
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible-playbook quick_patch_all.yml -i inventory.ini"
```

### Patch Single Host
```bash
ssh n100uck "cd ~/developerland/homelab/ansible/patching && ansible-playbook quick_patch_all.yml -i inventory.ini --limit <host>"
```

### Manual Patch
```bash
ssh <alias> "apt update && apt upgrade -y"
```

### Verify After Patching
```bash
ssh <alias> "apt list --upgradable 2>/dev/null | wc -l"
# Should return 0 or near-zero
```

---

## Exception Management

### Document Exception
When a patch cannot be applied:
1. **Host**: Which host
2. **Package**: Which package/CVE
3. **Reason**: Why it can't be patched (compatibility, dependency, etc.)
4. **Mitigation**: Alternative controls in place
5. **Review date**: When to re-evaluate

---

## SMB1001 Alignment

Maps to **SMB1001 Device Security** pillar:
- **Control 1.2.0.1**: Operating system patches applied regularly
- **Control 1.2.0.2**: Application patches applied regularly
- **Evidence**: Patch compliance reports show all hosts patched within SLA

---

## Related Skills

- **ansible-ops** - Ansible playbook execution for patching
- **linux-admin** - Manual package management
- **hardening-audit** - Security configuration auditing
- **smb1001-security-ops** - SMB1001 compliance evidence

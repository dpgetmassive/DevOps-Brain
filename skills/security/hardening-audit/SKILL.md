---
name: hardening-audit
version: 1.0.0
description: When the user wants to audit security configuration -- CIS benchmarks, SSH audit, service minimization, or configuration review. Also use when the user mentions "hardening audit," "CIS benchmark," "security baseline," "configuration audit," "security review," or "compliance check." For applying hardening, see linux-hardening. For vulnerability scanning, see vuln-scanning.
---

# Hardening Audit

You are an expert in security configuration auditing aligned with CIS benchmarks and SMB1001 controls.

## Audit Scope

**Read `context/infrastructure-context.md` first** to identify audit targets.

| Host Type | Count | Key Concerns |
|-----------|-------|-------------|
| Physical hosts | 7 | SSH, services, firewall, accounts |
| LXC containers | 11+ | Minimal services, no unnecessary packages |
| VMs | 2+ | Full OS audit |
| Network | 1 | OPNsense firewall rules |

## Guard Rails

**Auto-approve**: All audit/read operations, configuration checks
**Confirm first**: Applying remediation, changing configurations

---

## Quick Security Audit (Any Host)

```bash
ssh <alias> << 'EOF'
echo "=== SECURITY AUDIT: $(hostname) ==="
echo ""
echo "--- 1. SSH Configuration ---"
grep -E "PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|MaxAuthTries" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/* 2>/dev/null
echo ""
echo "--- 2. Users with Shell Access ---"
grep -v "nologin\|false\|sync" /etc/passwd | cut -d: -f1,7
echo ""
echo "--- 3. Sudo Users ---"
getent group sudo 2>/dev/null || getent group wheel 2>/dev/null
echo ""
echo "--- 4. Listening Services ---"
ss -tlnp | grep LISTEN
echo ""
echo "--- 5. Firewall Status ---"
ufw status 2>/dev/null || iptables -L -n 2>/dev/null | head -10
echo ""
echo "--- 6. SUID Binaries ---"
find / -perm -4000 -type f 2>/dev/null | wc -l | xargs -I{} echo "SUID files: {}"
echo ""
echo "--- 7. World-Writable Files in /etc ---"
find /etc -perm -o+w -type f 2>/dev/null | wc -l | xargs -I{} echo "World-writable: {}"
echo ""
echo "--- 8. Unattended Upgrades ---"
systemctl is-active unattended-upgrades 2>/dev/null || echo "Not installed"
echo ""
echo "--- 9. Fail2ban ---"
systemctl is-active fail2ban 2>/dev/null || echo "Not installed"
echo ""
echo "--- 10. Pending Updates ---"
apt list --upgradable 2>/dev/null | tail -n+2 | wc -l | xargs -I{} echo "Pending: {}"
EOF
```

---

## CIS Benchmark Checks

### CIS Level 1 - Essential
| Check | Command | Expected |
|-------|---------|----------|
| SSH root login | `grep PermitRootLogin /etc/ssh/sshd_config` | `prohibit-password` or `no` |
| SSH password auth | `grep PasswordAuthentication /etc/ssh/sshd_config` | `no` |
| Firewall enabled | `ufw status` | `active` |
| Auto updates | `systemctl is-active unattended-upgrades` | `active` |
| No empty passwords | `awk -F: '($2==""){print $1}' /etc/shadow` | (empty) |
| Log retention | `journalctl --disk-usage` | Configured |

### CIS Level 2 - Enhanced
| Check | Command | Expected |
|-------|---------|----------|
| Kernel hardening | `sysctl net.ipv4.conf.all.rp_filter` | `1` |
| No unnecessary services | `systemctl list-units --type=service --state=running` | Minimal |
| File integrity | `dpkg --verify` | No unexpected changes |

---

## Infrastructure-Wide Audit

### Audit All Physical Hosts
```bash
for host in n100uck pve-scratchy pve-itchy truenas-scale truenas-dr gm-ai; do
  echo "=== $host ==="
  ssh -o ConnectTimeout=5 $host << 'AUDIT'
echo "SSH: $(grep PasswordAuthentication /etc/ssh/sshd_config 2>/dev/null | head -1)"
echo "Users: $(grep -vc 'nologin\|false' /etc/passwd)"
echo "Ports: $(ss -tlnp | grep LISTEN | wc -l)"
echo "Updates: $(apt list --upgradable 2>/dev/null | tail -n+2 | wc -l)"
AUDIT
  echo ""
done
```

---

## Audit Report Format

### Per-Host Report
```
Host: <hostname> (<ip>)
Date: <date>
Auditor: <who>

PASS/FAIL | Check | Finding | Remediation
----------|-------|---------|------------
PASS | SSH key-only auth | PasswordAuthentication no |
FAIL | Firewall enabled | UFW not installed | apt install ufw && ufw enable
PASS | Auto-updates | unattended-upgrades active |
FAIL | Fail2ban | Not installed | apt install fail2ban
```

---

## SMB1001 Alignment

Maps to multiple SMB1001 pillars:
- **Device Security**: OS hardening, updates, firewall
- **Identity & Access Management**: User accounts, SSH config, sudo
- **Network Security**: Listening services, firewall rules
- **Data Protection**: File permissions, encryption

---

## Related Skills

- **linux-hardening** - Apply hardening remediations
- **vuln-scanning** - Vulnerability scanning
- **patch-compliance** - Patch status tracking
- **smb1001-security-ops** - SMB1001 control mapping

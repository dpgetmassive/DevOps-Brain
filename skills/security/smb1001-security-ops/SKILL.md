---
name: smb1001-security-ops
version: 1.0.0
description: When the user wants to perform SMB1001 certification operations -- compliance checks, evidence collection, control assessment automation, or security posture evaluation. Also use when the user mentions "SMB1001," "certification," "compliance check," "security assessment," "evidence collection," or "cyber security certification." Bridges to smb1001-gap-analysis and smb1001-assessment-agent (Frances) projects.
---

# SMB1001 Security Operations

You are an expert in SMB1001 cybersecurity certification. This skill automates operational security checks mapped to SMB1001 controls and collects evidence for assessments.

## SMB1001 Framework

### Tier Model (Cumulative)
| Tier | Level | Controls | Cumulative |
|------|-------|----------|------------|
| Bronze | 1 | 7 foundational | 7 |
| Silver | 2 | +7 | 14 |
| Gold | 3 | +9 | 23 |
| Platinum | 4 | +6 | 29 |
| Diamond | 5 | +7 | 36 |

### Five Security Pillars
1. **Identity & Access Management** (IAM)
2. **Data Protection**
3. **Device Security**
4. **Network Security**
5. **Incident Response**

## Related Projects

| Project | Path | Purpose |
|---------|------|---------|
| SMB1001 Gap Analysis | `~/developerland/smb1001-gap-analysis/` | Structured assessment tool for Cyber People |
| SMB1001 Assessment Agent | `~/developerland/smb1001-assessment-agent/` | AI-powered conversational assessment (Frances) |

## Guard Rails

**Auto-approve**: Evidence collection, compliance checks, report generation
**Confirm first**: Modifying security configurations, automated remediation

---

## Automated Evidence Collection

### Pillar 1: Identity & Access Management
```bash
ssh <alias> << 'EOF'
echo "=== IAM EVIDENCE: $(hostname) ==="
echo ""
echo "--- User Accounts ---"
cat /etc/passwd | grep -v nologin | grep -v false
echo ""
echo "--- Sudo Users ---"
getent group sudo 2>/dev/null
echo ""
echo "--- SSH Auth Config ---"
grep -E "PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|MaxAuthTries" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/* 2>/dev/null
echo ""
echo "--- Failed Login Attempts (24h) ---"
journalctl -u sshd -S '24 hours ago' --no-pager 2>/dev/null | grep -c "Failed" | xargs -I{} echo "Failed logins: {}"
echo ""
echo "--- Password Policy ---"
grep -E "PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_WARN_AGE" /etc/login.defs
EOF
```

### Pillar 2: Data Protection
```bash
echo "=== DATA PROTECTION EVIDENCE ==="
echo ""
echo "--- Backup Status ---"
ssh n100uck "cat /var/run/backup-status.state"
echo ""
echo "--- Replication Status ---"
ssh n100uck "cat /var/run/data-protection.state"
echo ""
echo "--- Encryption (disk) ---"
ssh <alias> "lsblk -o NAME,FSTYPE,SIZE,MOUNTPOINT,ENCRYPTED 2>/dev/null || lsblk"
echo ""
echo "--- Backup Storage ---"
ssh pve-scratchy "df -h /mnt/pve/pve-bk-truenas-dr"
```

### Pillar 3: Device Security
```bash
ssh <alias> << 'EOF'
echo "=== DEVICE SECURITY EVIDENCE: $(hostname) ==="
echo ""
echo "--- OS Version ---"
cat /etc/os-release | grep PRETTY_NAME
echo ""
echo "--- Pending Updates ---"
apt list --upgradable 2>/dev/null | tail -n+2 | wc -l | xargs -I{} echo "Pending updates: {}"
echo ""
echo "--- Security Updates ---"
apt list --upgradable 2>/dev/null | grep -ic security | xargs -I{} echo "Security updates: {}"
echo ""
echo "--- Firewall ---"
ufw status 2>/dev/null || echo "UFW not installed"
echo ""
echo "--- Auto-updates ---"
systemctl is-active unattended-upgrades 2>/dev/null || echo "Not configured"
echo ""
echo "--- Antivirus ---"
which clamscan 2>/dev/null && clamscan --version || echo "ClamAV not installed"
EOF
```

### Pillar 4: Network Security
```bash
echo "=== NETWORK SECURITY EVIDENCE ==="
echo ""
echo "--- Firewall (OPNsense) ---"
ping -c 1 10.16.1.1 > /dev/null && echo "OPNsense: Online" || echo "OPNsense: OFFLINE"
echo ""
echo "--- DNS Security (Pi-hole) ---"
dig @10.16.1.15 google.com +short > /dev/null && echo "DNS VIP: Working" || echo "DNS VIP: FAILED"
echo ""
echo "--- VPN (Tailscale) ---"
ssh pve-scratchy "pct exec 901 -- tailscale status 2>/dev/null | head -5" || echo "Tailscale check failed"
echo ""
echo "--- Open Ports ---"
ssh <alias> "ss -tlnp | grep LISTEN"
echo ""
echo "--- Cloudflare Tunnel ---"
ssh pve-scratchy "pct exec 114 -- cloudflared tunnel info 2>/dev/null | head -5" || echo "Tunnel check failed"
```

### Pillar 5: Incident Response
```bash
echo "=== INCIDENT RESPONSE EVIDENCE ==="
echo ""
echo "--- Monitoring Active ---"
ssh n100uck "crontab -l | grep -c monitor- | xargs -I{} echo 'Active monitors: {}'"
echo ""
echo "--- Alert Channel ---"
curl -sI https://ntfy.sh/homelab-status | head -3
echo ""
echo "--- Recent Alerts (24h) ---"
curl -s "https://ntfy.sh/homelab-status/json?poll=1&since=24h" 2>/dev/null | wc -l | xargs -I{} echo "Alerts in 24h: {}"
echo ""
echo "--- Log Retention ---"
ssh n100uck "journalctl --disk-usage"
echo ""
echo "--- Daily Readiness ---"
ssh n100uck "cat /var/run/daily-readiness.state 2>/dev/null | head -3"
```

---

## Compliance Score Calculation

### Scoring Method
- **Compliant** = 100% weight
- **Partially Compliant** = 50% weight
- **Non-Compliant** = 0% weight

### Readiness Levels
| Score | Level | Meaning |
|-------|-------|---------|
| 90%+ | Ready | Ready for certification |
| 70-89% | Nearly Ready | Minor gaps to address |
| 40-69% | Significant Gaps | Multiple areas need work |
| <40% | Early Stage | Foundational work needed |

---

## Full Infrastructure Assessment

### Run Complete Evidence Collection
```bash
echo "========================================="
echo "SMB1001 EVIDENCE COLLECTION"
echo "Date: $(date)"
echo "========================================="

# Run all 5 pillars
for host in n100uck pve-scratchy pve-itchy truenas-scale gm-ai piholed; do
  echo ""
  echo "===== HOST: $host ====="
  ssh -o ConnectTimeout=5 $host << 'AUDIT'
echo "OS: $(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d= -f2)"
echo "Updates: $(apt list --upgradable 2>/dev/null | tail -n+2 | wc -l)"
echo "SSH: $(grep PasswordAuthentication /etc/ssh/sshd_config 2>/dev/null | head -1)"
echo "Firewall: $(ufw status 2>/dev/null | head -1 || echo 'N/A')"
echo "Services: $(systemctl list-units --type=service --state=running 2>/dev/null | wc -l)"
AUDIT
done
```

---

## Integration with Cyber People Tools

### smb1001-gap-analysis
- Path: `~/developerland/smb1001-gap-analysis/`
- Automated evidence from this skill can populate assessment responses
- Control IDs (e.g., "1.2.0.1") map directly to evidence collection scripts

### smb1001-assessment-agent (Frances)
- Path: `~/developerland/smb1001-assessment-agent/`
- Evidence collection supports conversational assessment answers
- GRC reports use compliance scores from operational checks

---

## Related Skills

- **hardening-audit** - CIS benchmark auditing
- **vuln-scanning** - Vulnerability scanning
- **patch-compliance** - Patch management tracking
- **linux-hardening** - Applying hardening controls
- **monitoring-ops** - Monitoring for incident response

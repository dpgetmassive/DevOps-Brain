---
name: linux-hardening
version: 1.0.0
description: When the user wants to harden, secure, or audit Linux systems. Also use when the user mentions "SSH hardening," "firewall rules," "CIS benchmark," "fail2ban," "security audit," "unattended upgrades," or "secure the server." Maps to SMB1001 Device Security pillar. For general admin, see linux-admin. For network security, see linux-networking.
---

# Linux Hardening

You are an expert in Linux security hardening. Operations target the Get Massive Dojo homelab running Debian 12 and Proxmox 8.x.

## Initial Assessment

**Read `context/infrastructure-context.md` first** to identify target hosts.

Before hardening, determine:
1. **Target host** and its role (physical host vs container vs VM)
2. **Current security posture** - Run audit checks first
3. **Impact assessment** - Will changes affect running services?

## Guard Rails

**Auto-approve**: Security audits, checking configurations, viewing logs
**Confirm first**: Firewall rule changes on opnsense, SSH config changes on physical hosts, disabling services

---

## SSH Hardening

### Audit Current SSH Config
```bash
ssh <alias> << 'EOF'
echo "=== SSH Configuration Audit ==="
echo "--- Key Settings ---"
grep -E "^(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|Port|MaxAuthTries|AllowUsers|AllowGroups)" /etc/ssh/sshd_config
echo ""
echo "--- Authorized Keys ---"
cat /root/.ssh/authorized_keys 2>/dev/null | wc -l | xargs -I{} echo "Root authorized keys: {}"
echo ""
echo "--- Active Sessions ---"
who
EOF
```

### Recommended SSH Settings
```bash
ssh <alias> << 'EOF'
cat > /etc/ssh/sshd_config.d/hardening.conf << 'SSHEOF'
# SSH Hardening
PermitRootLogin prohibit-password
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowAgentForwarding no
SSHEOF
sshd -t && echo "Config valid" || echo "Config ERROR"
systemctl restart sshd
EOF
```

### Verify After
```bash
ssh <alias> "sshd -T | grep -E 'permitrootlogin|passwordauthentication|pubkeyauthentication|maxauthtries'"
```

---

## Firewall (UFW/nftables)

### Check Current Firewall Status
```bash
ssh <alias> "ufw status verbose 2>/dev/null || iptables -L -n --line-numbers"
```

### Enable UFW with Basic Rules
```bash
ssh <alias> << 'EOF'
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw --force enable
ufw status numbered
EOF
```

### Add Service Rule
```bash
ssh <alias> "ufw allow from 10.16.1.0/24 to any port <PORT>"
```

### Remove Rule
```bash
ssh <alias> "ufw status numbered"
# Then delete by number:
ssh <alias> "ufw delete <RULE_NUMBER>"
```

**Note**: OPNsense (10.16.1.1) handles perimeter firewall. Host firewalls are for defense-in-depth.

---

## Fail2ban

### Install and Configure
```bash
ssh <alias> << 'EOF'
apt install -y fail2ban
cat > /etc/fail2ban/jail.local << 'F2BEOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
F2BEOF
systemctl enable fail2ban
systemctl restart fail2ban
EOF
```

### Check Status
```bash
ssh <alias> "fail2ban-client status sshd"
```

### View Banned IPs
```bash
ssh <alias> "fail2ban-client status sshd | grep 'Banned IP'"
```

### Unban IP
```bash
ssh <alias> "fail2ban-client set sshd unbanip <IP>"
```

---

## Automatic Security Updates

### Enable Unattended Upgrades
```bash
ssh <alias> << 'EOF'
apt install -y unattended-upgrades apt-listchanges
dpkg-reconfigure -plow unattended-upgrades
EOF
```

### Check Status
```bash
ssh <alias> "systemctl status unattended-upgrades"
ssh <alias> "cat /var/log/unattended-upgrades/unattended-upgrades.log | tail -20"
```

### Check Pending Security Updates
```bash
ssh <alias> "apt list --upgradable 2>/dev/null | grep -i security"
```

---

## Security Audit Checklist

### Quick Security Scan
```bash
ssh <alias> << 'EOF'
echo "=== SECURITY AUDIT: $(hostname) ==="
echo ""
echo "--- SSH ---"
grep "PasswordAuthentication" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/* 2>/dev/null
echo ""
echo "--- Root Login ---"
grep "PermitRootLogin" /etc/ssh/sshd_config /etc/ssh/sshd_config.d/* 2>/dev/null
echo ""
echo "--- Users with Shell ---"
cat /etc/passwd | grep -v nologin | grep -v false | grep -v sync
echo ""
echo "--- SUID Binaries ---"
find / -perm -4000 -type f 2>/dev/null | head -20
echo ""
echo "--- World-Writable Files ---"
find /etc -perm -o+w -type f 2>/dev/null
echo ""
echo "--- Listening Ports ---"
ss -tlnp
echo ""
echo "--- Firewall ---"
ufw status 2>/dev/null || iptables -L -n 2>/dev/null | head -20
echo ""
echo "--- Pending Updates ---"
apt list --upgradable 2>/dev/null | wc -l | xargs -I{} echo "Upgradable packages: {}"
echo ""
echo "--- Fail2ban ---"
systemctl is-active fail2ban 2>/dev/null || echo "Not installed"
EOF
```

---

## Kernel Hardening (sysctl)

### Apply Recommended Settings
```bash
ssh <alias> << 'EOF'
cat > /etc/sysctl.d/99-hardening.conf << 'SYSEOF'
# Network hardening
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1
net.ipv4.icmp_echo_ignore_broadcasts = 1
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.tcp_syncookies = 1

# Kernel hardening
kernel.randomize_va_space = 2
fs.protected_hardlinks = 1
fs.protected_symlinks = 1
SYSEOF
sysctl --system
EOF
```

---

## SMB1001 Alignment

This skill maps to **SMB1001 Device Security** pillar:
- **Control 1.2.0.1**: Operating system updates (automatic security updates)
- **Control 1.2.0.2**: Application updates (package management)
- **Control 1.2.0.4**: Firewall enabled (UFW/host firewall)
- **Control 1.2.0.5**: Antivirus/anti-malware (ClamAV if needed)

---

## Related Skills

- **linux-admin** - General system administration
- **linux-networking** - Network configuration and troubleshooting
- **patch-compliance** - Compliance tracking and reporting
- **hardening-audit** - CIS benchmark auditing
- **vuln-scanning** - Vulnerability scanning with Nuclei/Trivy

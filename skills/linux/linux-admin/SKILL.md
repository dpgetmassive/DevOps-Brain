---
name: linux-admin
version: 1.0.0
description: When the user wants to manage Linux systems -- user/group management, package operations, disk space, cron jobs, filesystem operations, or general system administration. Also use when the user mentions "add user," "install package," "disk space," "cron job," "file permissions," or "system info." For hardening, see linux-hardening. For networking, see linux-networking. For systemd services, see systemd-management.
---

# Linux Administration

You are an expert Linux system administrator. Your operations target the Get Massive Dojo homelab infrastructure running primarily Debian 12 and Proxmox 8.x hosts.

## Initial Assessment

**Read `context/infrastructure-context.md` first** to identify the target host, its IP, SSH alias, and role.

Before executing, confirm:
1. **Target host** - Which host(s) need the operation?
2. **Operation type** - Read-only check or state-changing operation?
3. **Access method** - Direct SSH or via Proxmox `pct exec`?

## Guard Rails

**Auto-approve**: Package queries, disk checks, user listings, log viewing, cron listing
**Confirm first**: User creation/deletion on physical hosts, bulk package installs, filesystem changes affecting services

---

## User & Group Management

### List Users
```bash
ssh <alias> "cat /etc/passwd | grep -v nologin | grep -v false"
```

### Add User
```bash
ssh <alias> "useradd -m -s /bin/bash -G sudo <username>"
ssh <alias> "passwd <username>"  # Set password interactively
```

### Add to Group
```bash
ssh <alias> "usermod -aG <group> <username>"
```

### Remove User
```bash
# Verify before
ssh <alias> "id <username>"

# Remove (preserve home dir)
ssh <alias> "userdel <username>"

# Remove with home dir
ssh <alias> "userdel -r <username>"
```

### Check Sudo Access
```bash
ssh <alias> "getent group sudo"
```

---

## Package Management (apt)

### Update Package Lists
```bash
ssh <alias> "apt update"
```

### Check for Upgrades
```bash
ssh <alias> "apt list --upgradable"
```

### Install Package
```bash
ssh <alias> "apt install -y <package>"
```

### Remove Package
```bash
ssh <alias> "apt remove <package>"
# Or purge (remove config too):
ssh <alias> "apt purge <package>"
```

### Search for Package
```bash
ssh <alias> "apt search <keyword>"
```

### Check Installed Version
```bash
ssh <alias> "dpkg -l | grep <package>"
```

### Full System Upgrade
```bash
ssh <alias> "apt update && apt upgrade -y"
```

**Note**: For bulk patching across all hosts, use the `ansible-ops` skill with `quick_patch_all.yml`.

---

## Disk & Filesystem

### Check Disk Usage
```bash
ssh <alias> "df -h"
```

### Check Inode Usage
```bash
ssh <alias> "df -i"
```

### Find Large Files
```bash
ssh <alias> "du -sh /* 2>/dev/null | sort -hr | head -10"
```

### Find Large Files in Specific Directory
```bash
ssh <alias> "find /var/log -type f -size +100M -exec ls -lh {} \;"
```

### Check Directory Size
```bash
ssh <alias> "du -sh /path/to/directory"
```

### Clean Package Cache
```bash
ssh <alias> "apt clean && apt autoclean && apt autoremove -y"
```

### Clean Journal Logs
```bash
ssh <alias> "journalctl --vacuum-time=7d"
```

---

## Cron Jobs

### List Cron Jobs
```bash
ssh <alias> "crontab -l"
```

### List System Cron
```bash
ssh <alias> "ls -la /etc/cron.d/ /etc/cron.daily/ /etc/cron.hourly/"
```

### Edit Cron
```bash
ssh <alias> "crontab -e"
```

### Add Cron Job (non-interactive)
```bash
ssh <alias> "(crontab -l 2>/dev/null; echo '0 2 * * * /path/to/script.sh') | crontab -"
```

**Note**: Prefer systemd timers over cron for new tasks. See `systemd-management` skill.

---

## System Information

### Quick Health Check
```bash
ssh <alias> << 'EOF'
echo "=== $(hostname) HEALTH ==="
echo "Uptime: $(uptime)"
echo "Disk: $(df -h / | tail -1)"
echo "Memory: $(free -h | grep Mem)"
echo "Load: $(cat /proc/loadavg)"
EOF
```

### OS Version
```bash
ssh <alias> "cat /etc/os-release"
```

### Kernel Version
```bash
ssh <alias> "uname -a"
```

### Hardware Info
```bash
ssh <alias> "lscpu | head -20"
ssh <alias> "free -h"
ssh <alias> "lsblk"
```

### Running Processes (Top Consumers)
```bash
ssh <alias> "ps aux --sort=-%mem | head -15"
```

---

## File Operations

### Set Permissions
```bash
ssh <alias> "chmod 644 /path/to/file"
ssh <alias> "chmod 755 /path/to/directory"
```

### Set Ownership
```bash
ssh <alias> "chown user:group /path/to/file"
ssh <alias> "chown -R user:group /path/to/directory"
```

### Find Files
```bash
ssh <alias> "find /path -name 'pattern' -type f"
```

---

## Proxmox Container Access

For containers without direct SSH, use `pct exec` from the Proxmox host:

```bash
# Execute command in container
ssh pve-scratchy "pct exec <CTID> -- <command>"

# Interactive shell
ssh pve-scratchy "pct exec <CTID> -- bash"

# Example: check disk on CT 121 (ewp-banking, no sshd)
ssh pve-scratchy "pct exec 121 -- df -h"
```

---

## Troubleshooting

### Check Failed Services
```bash
ssh <alias> "systemctl --failed"
```

### Recent Errors
```bash
ssh <alias> "journalctl -p err -S '1 hour ago' --no-pager"
```

### Auth Failures
```bash
ssh <alias> "journalctl -u sshd -S '1 hour ago' --no-pager | grep -i fail"
```

### Kernel Messages
```bash
ssh <alias> "dmesg | tail -30"
```

---

## Related Skills

- **linux-hardening** - Security hardening, CIS benchmarks, firewall
- **linux-networking** - Network configuration, DNS, routing
- **systemd-management** - Services, timers, journalctl
- **ansible-ops** - Bulk operations across all hosts

---
name: systemd-management
version: 1.0.0
description: When the user wants to manage systemd services, timers, or journals. Also use when the user mentions "systemctl," "service status," "restart service," "timer," "journalctl," "boot target," "enable service," or "service logs." For general Linux admin, see linux-admin.
---

# systemd Management

You are an expert in systemd service management. Operations target Debian 12 and Proxmox 8.x hosts in the Get Massive Dojo homelab.

## Initial Assessment

**Read `context/infrastructure-context.md` first** to identify the target host.

Before operating:
1. **Target host** - Which host runs the service?
2. **Service name** - Exact unit name
3. **Current state** - Check before making changes

## Guard Rails

**Auto-approve**: Status checks, log viewing, listing units
**Confirm first**: Disabling critical services, changing boot targets on physical hosts

---

## Service Management

### Check Service Status
```bash
ssh <alias> "systemctl status <service> --no-pager"
```

### Start / Stop / Restart
```bash
ssh <alias> "systemctl start <service>"
ssh <alias> "systemctl stop <service>"
ssh <alias> "systemctl restart <service>"
ssh <alias> "systemctl reload <service>"  # Reload config without restart
```

### Enable / Disable at Boot
```bash
ssh <alias> "systemctl enable <service>"
ssh <alias> "systemctl disable <service>"
```

### Check if Active
```bash
ssh <alias> "systemctl is-active <service>"
ssh <alias> "systemctl is-enabled <service>"
```

### List All Failed Services
```bash
ssh <alias> "systemctl --failed"
```

### List Running Services
```bash
ssh <alias> "systemctl list-units --type=service --state=running"
```

---

## Key Services by Host

### n100uck (10.16.1.18)
| Service | Unit | Purpose |
|---------|------|---------|
| Pi-hole DNS | `pihole-FTL` | DNS resolution (secondary) |
| Keepalived | `keepalived` | DNS VIP failover |
| corosync-qnetd | `corosync-qnetd` | Proxmox cluster quorum |
| Monitoring Dashboard | `proxmox-monitoring` | Flask dashboard (port 8081) |
| Mailrise | `mailrise` | SMTP-to-ntfy relay |
| Docker (NPM) | `docker` | NPM backup container |

### pve-scratchy (10.16.1.22) / pve-itchy (10.16.1.8)
| Service | Unit | Purpose |
|---------|------|---------|
| Proxmox services | `pvedaemon`, `pveproxy`, `pvestatd` | Proxmox cluster |
| Corosync | `corosync` | Cluster communication |
| Container mgmt | `pve-container@<CTID>` | Per-container service |

### gm-ai (10.16.1.9)
| Service | Unit | Purpose |
|---------|------|---------|
| Cockpit | `cockpit` | Web management (port 9090) |
| ZFS Replication | `zfs-replicate-dr.timer` | Daily replication to DR |

---

## systemd Timers (Preferred Over Cron)

### List All Timers
```bash
ssh <alias> "systemctl list-timers --all"
```

### Create a Timer

**Step 1: Create the service unit**
```bash
ssh <alias> "cat > /etc/systemd/system/my-task.service << 'EOF'
[Unit]
Description=My Scheduled Task

[Service]
Type=oneshot
ExecStart=/usr/local/bin/my-script.sh
EOF"
```

**Step 2: Create the timer unit**
```bash
ssh <alias> "cat > /etc/systemd/system/my-task.timer << 'EOF'
[Unit]
Description=Run My Task Daily

[Timer]
OnCalendar=*-*-* 06:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF"
```

**Step 3: Enable and start**
```bash
ssh <alias> "systemctl daemon-reload && systemctl enable my-task.timer && systemctl start my-task.timer"
```

### Timer Schedules (OnCalendar syntax)
| Schedule | Syntax |
|----------|--------|
| Every 5 minutes | `*:0/5` |
| Every 15 minutes | `*:0/15` |
| Daily at 2 AM | `*-*-* 02:00:00` |
| Weekly Sunday 1 AM | `Sun *-*-* 01:00:00` |
| Monthly 1st at midnight | `*-*-01 00:00:00` |

### Test Timer Schedule
```bash
ssh <alias> "systemd-analyze calendar '*-*-* 06:00:00'"
```

---

## Journal (Logs)

### View Service Logs
```bash
ssh <alias> "journalctl -u <service> -n 50 --no-pager"
```

### Follow Logs (Live)
```bash
ssh <alias> "journalctl -u <service> -f"
```

### Logs Since Time
```bash
ssh <alias> "journalctl -u <service> -S '1 hour ago' --no-pager"
ssh <alias> "journalctl -u <service> -S today --no-pager"
```

### Error-Level Logs Only
```bash
ssh <alias> "journalctl -p err -S '1 hour ago' --no-pager"
```

### Check Journal Disk Usage
```bash
ssh <alias> "journalctl --disk-usage"
```

### Clean Old Journals
```bash
ssh <alias> "journalctl --vacuum-time=7d"
ssh <alias> "journalctl --vacuum-size=500M"
```

---

## Creating Custom Services

### Template for a Long-Running Service
```bash
ssh <alias> "cat > /etc/systemd/system/my-app.service << 'EOF'
[Unit]
Description=My Application
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/my-app
ExecStart=/opt/my-app/run.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF"
```

### Enable and Start
```bash
ssh <alias> "systemctl daemon-reload && systemctl enable my-app && systemctl start my-app"
```

### Verify
```bash
ssh <alias> "systemctl status my-app --no-pager"
```

---

## Troubleshooting

### Service Won't Start
```bash
ssh <alias> << 'EOF'
echo "=== Service Diagnostics: <service> ==="
systemctl status <service> --no-pager -l
echo ""
echo "--- Recent Logs ---"
journalctl -u <service> -n 30 --no-pager
echo ""
echo "--- Unit File ---"
systemctl cat <service>
EOF
```

### Find Unit File Location
```bash
ssh <alias> "systemctl show -p FragmentPath <service>"
```

### Reload After Editing Unit Files
```bash
ssh <alias> "systemctl daemon-reload"
```

---

## Related Skills

- **linux-admin** - General system administration
- **monitoring-ops** - Monitoring scripts and timers on n100uck
- **docker-management** - Docker service management

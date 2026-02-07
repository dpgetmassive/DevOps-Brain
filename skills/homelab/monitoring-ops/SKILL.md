---
name: monitoring-ops
version: 1.0.0
description: When the user wants to check monitoring status, manage alerts, view dashboards, or troubleshoot monitoring scripts. Also use when the user mentions "monitoring," "alerts," "ntfy," "dashboard," "uptime," "host availability," "backup monitor," or "daily readiness." For service-specific management, see homelab-services.
---

# Monitoring Operations

You are an expert in homelab monitoring. The monitoring system runs on n100uck (10.16.1.18) as an independent witness node.

## Monitoring Architecture (v2.2)

**Read `context/infrastructure-context.md` first.**

| Monitor | Schedule | Script | Checks |
|---------|----------|--------|--------|
| Host Availability | Every 5 min | monitor-host-availability.sh | pve-scratchy, pve-itchy, TrueNAS Primary/DR |
| Backup Status | 6:00 AM daily | monitor-backup-status.sh | Backup age, storage capacity, config backups |
| Data Protection | 6:30 AM daily | monitor-data-protection.sh | ZFS replication, snapshots, quota, CloudSync |
| System Health | Every 15 min | monitor-system-health.sh | CPU, memory, storage, services, updates |
| Daily Readiness | 6:45 AM daily | daily-readiness-check.sh | Aggregates all monitors, services, quorum |

**Alert topic**: https://ntfy.sh/homelab-status (consolidated)
**Dashboard**: http://10.16.1.18:8081 (Flask API at /api/status)
**Scripts**: `/usr/local/bin/` on n100uck
**Logs**: `/var/log/` on n100uck
**State files**: `/var/run/*.state` on n100uck

## Guard Rails

**Auto-approve**: Status checks, log viewing, manual monitor runs, ntfy queries
**Confirm first**: Disabling monitors, changing cron schedules, modifying scripts

---

## Quick Status Check

### Read All Monitor States
```bash
ssh n100uck << 'EOF'
echo "=== HOST AVAILABILITY ===" && cat /var/run/host-availability.state 2>/dev/null && echo ""
echo "=== BACKUP STATUS ===" && cat /var/run/backup-status.state 2>/dev/null && echo ""
echo "=== DATA PROTECTION ===" && cat /var/run/data-protection.state 2>/dev/null && echo ""
echo "=== DAILY READINESS ===" && cat /var/run/daily-readiness.state 2>/dev/null
EOF
```

### Check Dashboard
```bash
curl -s http://10.16.1.18:8081/api/status | python3 -m json.tool
```

### Check Recent Alerts
```bash
curl -s "https://ntfy.sh/homelab-status/json?poll=1&since=24h" | jq -r '.message'
```

---

## Run Monitors Manually

```bash
# Host availability
ssh n100uck "/usr/local/bin/monitor-host-availability.sh"

# Backup status
ssh n100uck "/usr/local/bin/monitor-backup-status.sh"

# Data protection
ssh n100uck "/usr/local/bin/monitor-data-protection.sh"

# System health
ssh n100uck "/usr/local/bin/monitor-system-health.sh"

# Daily readiness (aggregation)
ssh n100uck "/usr/local/bin/daily-readiness-check.sh"
```

---

## View Monitor Logs

```bash
ssh n100uck "tail -30 /var/log/host-availability.log"
ssh n100uck "tail -30 /var/log/backup-status.log"
ssh n100uck "tail -30 /var/log/data-protection.log"
ssh n100uck "tail -30 /var/log/system-health.log"
ssh n100uck "tail -50 /var/log/daily-readiness.log"
```

---

## Cron Schedule

### View All Monitor Cron Jobs
```bash
ssh n100uck "crontab -l | grep -E 'monitor-|readiness'"
```

### Expected Schedule
```
*/5 * * * * /usr/local/bin/monitor-host-availability.sh
0 6 * * * /usr/local/bin/monitor-backup-status.sh
30 6 * * * /usr/local/bin/monitor-data-protection.sh
*/15 * * * * /usr/local/bin/monitor-system-health.sh
45 6 * * * /usr/local/bin/daily-readiness-check.sh
```

---

## Dashboard Management

### Check Dashboard Process
```bash
ssh n100uck "lsof -ti:8081 | xargs ps -p 2>/dev/null || echo 'Not running'"
```

### Restart Dashboard
```bash
ssh n100uck << 'EOF'
lsof -ti:8081 | xargs kill -9 2>/dev/null
sleep 2
cd /opt/proxmox-monitoring && source venv/bin/activate && python3 proxmox_status.py > /var/log/proxmox-monitoring.log 2>&1 &
sleep 2
lsof -ti:8081 && echo "Dashboard started" || echo "Dashboard failed"
EOF
```

---

## Alert Triage

### Priority Levels
| Priority | Meaning | Examples |
|----------|---------|---------|
| 1-2 | Success/Info | Backups completed, host recovered |
| 3 | Warning | Stale replication, high resources |
| 4-5 | Critical | Host down, backup failed, quota exceeded |

### Common Alert Responses

**Host Down**: Check `host-availability.state`, ping host, check Proxmox UI
**Backup Failed**: Check NFS mount, TrueNAS DR status, disk space
**Replication Stale**: Check DR quota, network, replication logs
**Quota Exceeded**: Increase quota: `ssh truenas-dr "zfs set quota=<size> <dataset>"`

---

## Troubleshooting

### Monitors Not Running
```bash
ssh n100uck << 'EOF'
echo "=== Cron Jobs ==="
crontab -l | grep monitor-
echo ""
echo "=== Script Permissions ==="
ls -l /usr/local/bin/monitor-*.sh /usr/local/bin/daily-readiness-check.sh
echo ""
echo "=== ntfy Connectivity ==="
curl -sI https://ntfy.sh/homelab-status | head -3
echo ""
echo "=== SSH to Monitored Hosts ==="
for host in 10.16.1.22 10.16.1.8 10.16.1.6 10.16.1.20; do
  ssh -o ConnectTimeout=5 root@$host "echo ok" 2>/dev/null && echo "$host OK" || echo "$host FAIL"
done
EOF
```

---

## Related Skills

- **homelab-services** - Service catalog and dependencies
- **proxmox-backup-restore** - Backup operations that monitors check
- **storage-management** - Replication that data protection monitors

# systemd/systemctl

systemd provides service management, logging, and system initialization via `systemctl` and `journalctl`. Used for managing services across all Linux hosts in the homelab.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | N | No REST API (use systemd D-Bus API for programmatic access) |
| MCP | N | No MCP server available |
| CLI | Y | `systemctl` and `journalctl` command-line tools |
| SDK | Y | Python `systemd-python`, Go `coreos/go-systemd` |

## Authentication

**Service Management**: Requires root or sudo access for most operations.

**Read-only Operations**: Some commands (status, list) work without root.

**D-Bus**: Systemd exposes D-Bus API for programmatic access (requires appropriate permissions).

## Common Agent Operations

### Service Lifecycle

```bash
# Start service
systemctl start <service-name>

# Stop service
systemctl stop <service-name>

# Restart service
systemctl restart <service-name>

# Reload service (if supported)
systemctl reload <service-name>

# Enable service (start on boot)
systemctl enable <service-name>

# Disable service
systemctl disable <service-name>

# Enable and start
systemctl enable --now <service-name>
```

### Service Status

```bash
# Check service status
systemctl status <service-name>

# Brief status
systemctl is-active <service-name>
systemctl is-enabled <service-name>
systemctl is-failed <service-name>

# List all services
systemctl list-units

# List running services
systemctl list-units --state=running

# List failed services
systemctl list-units --state=failed
```

### Service Logs

```bash
# View service logs
journalctl -u <service-name>

# Follow logs (tail -f)
journalctl -u <service-name> -f

# Last 100 lines
journalctl -u <service-name> -n 100

# Logs since today
journalctl -u <service-name> --since today

# Logs with time range
journalctl -u <service-name> --since "2026-02-08 00:00:00" --until "2026-02-08 23:59:59"
```

### System Logs

```bash
# All system logs
journalctl

# Kernel logs
journalctl -k

# Boot logs
journalctl -b

# Logs since boot
journalctl --since boot

# Logs with priority filter
journalctl -p err  # errors and above
journalctl -p warning  # warnings and above
```

### System Analysis

```bash
# Analyze boot time
systemd-analyze

# Show time per service
systemd-analyze blame

# Show critical chain
systemd-analyze critical-chain

# Show service dependencies
systemctl list-dependencies <service-name>
```

### Timers (Cron Alternative)

```bash
# List all timers
systemctl list-timers

# List active timers
systemctl list-timers --all

# Check timer status
systemctl status <timer-name>.timer

# Start timer
systemctl start <timer-name>.timer

# Enable timer
systemctl enable <timer-name>.timer
```

### Create Service Unit File

```bash
# Create service file
sudo nano /etc/systemd/system/my-service.service

# Example service file:
[Unit]
Description=My Custom Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/my-service.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Reload systemd after creating/modifying unit files
sudo systemctl daemon-reload

# Enable and start
sudo systemctl enable --now my-service.service
```

### Create Timer Unit File

```bash
# Create timer file
sudo nano /etc/systemd/system/my-backup.timer

# Example timer file:
[Unit]
Description=Daily Backup Timer

[Timer]
OnCalendar=daily
OnCalendar=02:00
Persistent=true

[Install]
WantedBy=timers.target

# Create corresponding service
sudo nano /etc/systemd/system/my-backup.service

[Unit]
Description=Daily Backup Service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh

# Enable timer
sudo systemctl daemon-reload
sudo systemctl enable --now my-backup.timer
```

### Remote Operations

```bash
# Check service on remote host
ssh pve-scratchy "systemctl status nginx"

# Restart service on remote host
ssh piholed "systemctl restart pihole-FTL"

# View logs on remote host
ssh n100uck "journalctl -u monitor-host-availability -n 50"
```

## Key Objects/Metrics

- **Services**: Systemd service units (.service files)
- **Timers**: Scheduled tasks (.timer files)
- **Targets**: System states (multi-user.target, graphical.target)
- **Logs**: Journal entries (systemd-journald)
- **Boot Time**: System startup duration and service initialization times
- **Dependencies**: Service dependencies and ordering

## When to Use

- **Service management**: Start, stop, restart services (nginx, docker, pihole-FTL, keepalived)
- **Log inspection**: Troubleshoot service issues, check error logs
- **Boot analysis**: Diagnose slow boot times, identify problematic services
- **Timer management**: Manage scheduled tasks (backups, monitoring scripts)
- **Service creation**: Create custom services and timers for automation
- **System health**: Check failed services, verify service status

## Rate Limits

No rate limits. Systemd operations:
- Are immediate (start/stop/restart)
- Log operations may be slow for large logs
- Daemon reload required after unit file changes

## Relevant Skills

- `linux-service-management` - Service lifecycle and troubleshooting
- `monitoring-ops` - Service health monitoring and log analysis
- `backup-management` - Timer-based backup scheduling
- `system-maintenance` - Service management during maintenance windows

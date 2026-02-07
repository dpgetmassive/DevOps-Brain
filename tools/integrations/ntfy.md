# ntfy

ntfy provides simple pub/sub messaging and push notifications via REST API. Used for homelab alerting and status notifications.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `https://ntfy.sh/` (public) or self-hosted instance |
| MCP | N | No MCP server available |
| CLI | Y | `ntfy` command-line client (optional, for subscribing) |
| SDK | Y | Python `ntfy`, JavaScript libraries, Go client |

## Authentication

**Public Instance**: No authentication required for public topics. Use topic names that are hard to guess.

**Self-hosted**: Can enable authentication via username/password or access tokens.

**Topic-based**: Topics act as channels. Anyone with topic name can publish/subscribe.

```bash
# Public topic (no auth)
curl -d "Alert message" https://ntfy.sh/homelab-status

# With authentication (if enabled)
curl -u user:pass -d "Alert message" https://ntfy.sh/homelab-status
```

## Common Agent Operations

### Publish Message

```bash
# Simple message
curl -d "Backup completed successfully" \
  https://ntfy.sh/homelab-status

# With title
curl -H "Title: Backup Status" \
  -d "Backup completed successfully" \
  https://ntfy.sh/homelab-status

# With priority (1=min, 2=low, 3=default, 4=high, 5=max)
curl -H "Priority: 4" \
  -H "Title: Critical Alert" \
  -d "Host pve-scratchy is down!" \
  https://ntfy.sh/homelab-status

# With tags (emoji or text)
curl -H "Tags: warning,server" \
  -d "High CPU usage detected" \
  https://ntfy.sh/homelab-status
```

### Publish JSON Message

```bash
# Structured message
curl -H "Content-Type: application/json" \
  -d '{
    "topic": "homelab-status",
    "message": "Backup completed",
    "title": "Backup Status",
    "priority": 3,
    "tags": ["backup", "success"]
  }' \
  https://ntfy.sh/
```

### Subscribe to Topic (Polling)

```bash
# Poll for messages (last 10)
curl https://ntfy.sh/homelab-status/json?poll=1&since=10m

# Stream messages (long polling)
curl -N https://ntfy.sh/homelab-status/json?poll=1
```

### Subscribe via CLI

```bash
# Install ntfy CLI (if not installed)
# macOS: brew install ntfy
# Linux: Download from https://ntfy.sh/docs/install/

# Subscribe to topic
ntfy sub homelab-status

# Subscribe with filters
ntfy sub homelab-status --since 1h
```

### Publish from Scripts

```bash
# Example: Send alert from monitoring script
send_alert() {
  local priority=$1
  local title=$2
  local message=$3
  
  curl -s -H "Priority: $priority" \
    -H "Title: $title" \
    -d "$message" \
    https://ntfy.sh/homelab-status > /dev/null
}

# Usage
send_alert 4 "Host Down" "pve-scratchy (10.16.1.22) is not responding"
```

### Check Topic Stats

```bash
# Get topic information (if self-hosted with stats enabled)
curl https://ntfy.sh/homelab-status/stats
```

## Key Objects/Metrics

- **Topics**: Named channels for messages (e.g., `homelab-status`)
- **Messages**: Text content, titles, priorities, tags
- **Priority**: 1=min, 2=low, 3=default, 4=high, 5=max
- **Tags**: Emoji or text labels for categorization
- **Subscriptions**: Active subscribers to a topic

## When to Use

- **Alert notifications**: Send alerts from monitoring scripts (host availability, backups, system health)
- **Status updates**: Report on automated task completion (backups, updates, deployments)
- **Incident reporting**: Notify on critical issues requiring immediate attention
- **Daily reports**: Send summary reports (backup status, system health, patch status)
- **Integration**: Connect monitoring tools to send alerts via webhooks

## Rate Limits

**Public Instance (ntfy.sh)**:
- 80 messages per topic per day (free tier)
- 3 messages per topic per minute
- 250 API requests per hour

**Self-hosted**: No limits by default (configurable).

## Relevant Skills

- `monitoring-ops` - Send alerts for host availability, backups, system health
- `incident-report` - Send incident notifications
- `backup-management` - Notify on backup completion/failure
- `patch-compliance` - Send patch status reports

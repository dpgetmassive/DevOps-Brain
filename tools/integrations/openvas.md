# Greenbone OpenVAS/GVM

OpenVAS (Open Vulnerability Assessment Scanner) is a comprehensive vulnerability scanning framework managed via Greenbone Vulnerability Manager (GVM). Provides network vulnerability scanning, web application testing, and compliance checking via web UI and REST API.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API (GMP protocol) at port 9390, XML-based |
| MCP | N | No MCP server available |
| CLI | Y | `gvm-cli` command-line tool, `omp` (OpenVAS Management Protocol) |
| SDK | Y | Python `python-gvm`, Go `gogvm` |

## Authentication

**Web UI**: Default credentials `admin`/`admin` (change on first login). Access at `https://<host>:9392`.

**REST API**: Authenticate via `/omp` endpoint with username/password or API token.

```bash
# Authenticate via CLI
gvm-cli --gmp-username admin --gmp-password admin socket --xml '<get_version/>'

# Authenticate via API
curl -k -u admin:admin https://10.16.1.50:9390/omp
```

**API Token**: Generate token in web UI (Configuration > Users > API Keys) for programmatic access.

## Common Agent Operations

### Docker Deployment

```bash
# Run OpenVAS scanner container
docker run -d --name openvas \
  -p 9392:9392 \
  -e PASSWORD=admin \
  greenbone/openvas-scanner:latest

# Run full GVM stack (scanner + manager + web UI)
docker-compose up -d
```

### Create Scan Target

```bash
# Via CLI
gvm-cli --gmp-username admin --gmp-password admin socket --xml '
<create_target>
  <name>Homelab Network</name>
  <hosts>10.16.1.0/24</hosts>
</create_target>'

# Via API
curl -k -u admin:admin -X POST \
  -d '<create_target><name>Homelab Network</name><hosts>10.16.1.0/24</hosts></create_target>' \
  https://10.16.1.50:9390/omp
```

### Create and Start Scan Task

```bash
# Create task via CLI
gvm-cli --gmp-username admin --gmp-password admin socket --xml '
<create_task>
  <name>Weekly Homelab Scan</name>
  <config id="daba56c8-73ec-11ea-a475-571927d15491"/>
  <target id="target-uuid"/>
</create_task>'

# Start scan
gvm-cli --gmp-username admin --gmp-password admin socket --xml '
<start_task task_id="task-uuid"/>'

# Get scan status
gvm-cli --gmp-username admin --gmp-password admin socket --xml '
<get_tasks task_id="task-uuid"/>'
```

### Get Scan Report

```bash
# Get report via CLI
gvm-cli --gmp-username admin --gmp-password admin socket --xml '
<get_reports report_id="report-uuid"/>'

# Export report as PDF
gvm-cli --gmp-username admin --gmp-password admin socket --xml '
<get_reports report_id="report-uuid" format_id="c402cc3e-b531-11e1-9163-406186ea4fc5"/>' > report.pdf
```

### List Operations

```bash
# List scan configs
gvm-cli --gmp-username admin --gmp-password admin socket --xml '<get_configs/>'

# List all tasks
gvm-cli --gmp-username admin --gmp-password admin socket --xml '<get_tasks/>'
```

## Key Objects/Metrics

- **Targets**: IP addresses, hostnames, or CIDR ranges to scan
- **Scan Configs**: Predefined scan configurations (Full and Fast, Full and Fast Ultimate, etc.)
- **Tasks**: Scan jobs with target, config, and schedule
- **Reports**: Scan results with vulnerabilities, severity, and remediation
- **NVTs**: Network Vulnerability Tests (scan plugins)
- **Severity Levels**: Log, Low, Medium, High, Critical
- **Scan Status**: New, Requested, Running, Stop Requested, Stopped, Done, Error

## When to Use

- **Network vulnerability scanning**: Comprehensive security assessment of homelab infrastructure
- **Compliance checking**: Verify security posture against standards (PCI-DSS, HIPAA, etc.)
- **Regular audits**: Scheduled vulnerability scans for continuous security monitoring
- **Web application testing**: Scan web services and applications for vulnerabilities
- **Infrastructure hardening**: Identify misconfigurations and security gaps

## Rate Limits

No explicit rate limits. OpenVAS:
- Processes scans sequentially by default (can configure concurrent scans)
- Resource-intensive (CPU and memory usage during scans)
- Scan duration depends on target size and scan config (Full scan: hours to days)

## Relevant Skills

- `vuln-scanning` - Vulnerability scanning workflows and reporting
- `smb1001-security-ops` - Security operations and compliance scanning
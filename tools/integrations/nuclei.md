# ProjectDiscovery Nuclei

Nuclei is a fast, template-based vulnerability scanner that uses YAML templates to identify security issues across web applications, networks, and infrastructure. Used for automated vulnerability scanning and security assessments.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | N | CLI-only tool, no REST API |
| MCP | N | No MCP server available |
| CLI | Y | `nuclei` command-line tool (Go binary) |
| SDK | N | No official SDK, use CLI directly |

## Authentication

**CLI Tool**: No authentication required. Nuclei runs locally and scans targets you specify.

**Template Updates**: Update templates via `nuclei -update-templates` or `nuclei -update`. Templates stored in `~/.local/share/nuclei/templates/`.

## Common Agent Operations

### Basic Scanning

```bash
# Scan single URL
nuclei -u https://example.com

# Scan with severity filter
nuclei -u https://example.com -severity critical,high

# Scan from file list
nuclei -l targets.txt

# Scan with rate limiting and concurrency
nuclei -l targets.txt -rate-limit 10 -c 25
```

### Template Categories

```bash
# Scan CVEs only
nuclei -u https://example.com -t cves/

# Scan misconfigurations
nuclei -u https://example.com -t misconfiguration/

# Scan exposures (sensitive data)
nuclei -u https://example.com -t exposures/

# Scan technology-specific templates
nuclei -u https://example.com -t technologies/nginx
```

### Output Formats

```bash
# JSON output
nuclei -u https://example.com -json -o results.json

# Markdown output
nuclei -u https://example.com -markdown-export results.md

# Silent mode (no stdout)
nuclei -u https://example.com -silent -o results.json
```

### Advanced Options

```bash
# Scan with custom headers
nuclei -u https://example.com -H "Authorization: Bearer token"

# Scan with proxy
nuclei -u https://example.com -proxy http://127.0.0.1:8080

# List available templates
nuclei -tl

# Update templates
nuclei -update-templates
```

## Key Objects/Metrics

- **Templates**: YAML-based scan templates (CVE, misconfiguration, exposure, technology)
- **Findings**: Vulnerabilities identified with severity, description, and references
- **Targets**: URLs, IPs, or hostnames to scan
- **Severity Levels**: info, low, medium, high, critical
- **Template Tags**: Categories like cve, exposure, misconfiguration, rce, xss
- **Scan Results**: JSON, markdown, or CSV formatted output

## When to Use

- **Vulnerability scanning**: Automated CVE detection across web applications and services
- **Security assessments**: Identify misconfigurations, exposures, and security issues
- **Technology detection**: Scan for specific technologies (nginx, apache, proxmox, etc.)
- **Continuous scanning**: Integrate into CI/CD pipelines for automated security checks
- **Compliance audits**: Regular security scanning for homelab infrastructure

## Rate Limits

No built-in rate limits. Control via:
- `-rate-limit`: Requests per second (default: 150)
- `-c`: Concurrent requests (default: 25)
- `-timeout`: Request timeout in seconds (default: 5)

Adjust based on target capacity and network conditions.

## Relevant Skills

- `vuln-scanning` - Vulnerability scanning workflows and reporting
- `smb1001-security-ops` - Security operations and compliance scanning
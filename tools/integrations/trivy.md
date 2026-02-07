# Aqua Security Trivy

Trivy is a comprehensive security scanner for containers, filesystems, git repositories, and infrastructure-as-code. Detects vulnerabilities, misconfigurations, secrets, and license issues across multiple targets.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | N | CLI-only tool, no REST API |
| MCP | N | No MCP server available |
| CLI | Y | `trivy` command-line tool |
| SDK | Y | Go SDK available, Python wrapper `trivy-python` |

## Authentication

**CLI Tool**: No authentication required for local scanning. Trivy runs locally and scans targets you specify.

**Private Registries**: Authenticate via `~/.docker/config.json` or environment variables (`TRIVY_USERNAME`, `TRIVY_PASSWORD`).

**Git Repositories**: Use SSH keys or HTTPS credentials for private repos.

## Common Agent Operations

### Container Image Scanning

```bash
# Scan container image
trivy image nginx:latest

# Scan with severity filter
trivy image --severity HIGH,CRITICAL nginx:latest

# Scan with output formats
trivy image --format json -o results.json nginx:latest
trivy image --format sarif -o results.sarif nginx:latest

# CI-friendly with exit code
trivy image --exit-code 1 --severity HIGH,CRITICAL nginx:latest
```

### Filesystem Scanning

```bash
# Scan filesystem directory
trivy fs /path/to/directory

# Scan with severity filter
trivy fs --severity HIGH,CRITICAL /path/to/directory

# Scan with output format
trivy fs --format json -o results.json /path/to/directory
```

### Infrastructure-as-Code Scanning

```bash
# Scan Terraform files
trivy config /path/to/terraform

# Scan Kubernetes manifests
trivy k8s cluster --context my-context

# Scan Dockerfile
trivy config Dockerfile

# Scan with misconfiguration checks
trivy config --security-checks config /path/to/iac
```

### Git Repository Scanning

```bash
# Scan git repository
trivy repo https://github.com/user/repo

# Scan private repo (requires auth)
trivy repo git@github.com:user/repo.git
```

### Database Management

```bash
# Download vulnerability database
trivy image --download-db-only

# Clear cache
trivy image --clear-cache
```

## Key Objects/Metrics

- **Vulnerabilities**: CVEs with severity, package, and fix versions
- **Misconfigurations**: Security issues in IaC files (Terraform, Kubernetes, Dockerfile)
- **Secrets**: Exposed API keys, passwords, tokens in code
- **Licenses**: License compliance issues in dependencies
- **Severity Levels**: UNKNOWN, LOW, MEDIUM, HIGH, CRITICAL
- **Targets**: Container images, filesystems, git repos, IaC files

## When to Use

- **Container security**: Scan container images before deployment
- **CI/CD integration**: Automated vulnerability scanning in pipelines
- **IaC security**: Check Terraform, Kubernetes, and Dockerfile configurations
- **Secret detection**: Find exposed credentials in code repositories
- **Compliance scanning**: Regular security audits for homelab infrastructure
- **Dependency scanning**: Check application dependencies for vulnerabilities

## Rate Limits

No rate limits for local scanning. For remote operations:
- **Container registries**: Respect registry rate limits (Docker Hub: 100 pulls/6 hours anonymous)
- **Git repositories**: Respect provider rate limits (GitHub: 5000 requests/hour authenticated)
- **Database updates**: Trivy vulnerability database updates are rate-limited by Aqua Security

## Relevant Skills

- `vuln-scanning` - Vulnerability scanning workflows and reporting
- `container-ops` - Container security and image scanning
- `smb1001-security-ops` - Security operations and compliance scanning
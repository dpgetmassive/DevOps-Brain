---
name: vuln-scanning
version: 1.0.0
description: When the user wants to scan for vulnerabilities -- network scanning with Nuclei, container scanning with Trivy, or OpenVAS assessments. Also use when the user mentions "vulnerability scan," "CVE," "Nuclei," "Trivy," "OpenVAS," "security scan," or "scan network." Maps to SMB1001 Device Security and Network Security pillars. For patch compliance, see patch-compliance. For hardening, see hardening-audit.
---

# Vulnerability Scanning

You are an expert in vulnerability scanning and assessment.

## Scanning Tools

| Tool | Purpose | Target | Installation |
|------|---------|--------|-------------|
| Nuclei | Template-based web/network scanning | URLs, IPs, ranges | `go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest` |
| Trivy | Container, filesystem, and IaC scanning | Images, repos, configs | `apt install trivy` or Docker |
| OpenVAS | Full network vulnerability assessment | Subnets, hosts | Docker (Greenbone Community) |

## Guard Rails

**Auto-approve**: Scanning homelab internal hosts, viewing scan results
**Confirm first**: Scanning external targets, running aggressive scans, automated remediation

---

## Nuclei Scanning

### Install/Update Nuclei
```bash
# On scanning host
go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
nuclei -update-templates
```

### Scan Single Host
```bash
nuclei -u http://10.16.1.50:81 -severity medium,high,critical
```

### Scan Multiple Hosts
```bash
echo "http://10.16.1.22:8006
http://10.16.1.8:8006
http://10.16.1.6:443
http://10.16.1.18:8081
http://10.16.1.50:81" > targets.txt
nuclei -l targets.txt -severity high,critical
```

### Scan with Specific Templates
```bash
nuclei -u http://<target> -t cves/
nuclei -u http://<target> -t exposures/
nuclei -u http://<target> -t misconfiguration/
```

### Output to JSON Report
```bash
nuclei -l targets.txt -severity medium,high,critical -j -o scan-results.json
```

---

## Trivy Scanning

### Scan Container Image
```bash
ssh <docker_host> "trivy image <image>:<tag>"
```

### Scan with Severity Filter
```bash
ssh <docker_host> "trivy image --severity HIGH,CRITICAL <image>:<tag>"
```

### Scan Local Filesystem
```bash
ssh <alias> "trivy fs /path/to/project"
```

### Scan IaC (Terraform, Dockerfile, etc.)
```bash
trivy config .
trivy config Dockerfile
```

### Scan Docker Compose
```bash
trivy config docker-compose.yml
```

### Generate Report
```bash
ssh <docker_host> "trivy image --format json -o report.json <image>:<tag>"
```

---

## OpenVAS (Greenbone Community)

### Deploy OpenVAS (Docker)
```bash
docker run -d --name openvas \
  -p 9392:9392 \
  -e PASSWORD=admin \
  greenbone/openvas-scanner
```

### Access Web UI
- **URL**: http://<host>:9392
- **Default credentials**: admin / admin (change immediately)

### Create Scan Target
Via web UI: Configuration -> Targets -> New Target
- Name: Homelab Internal
- Hosts: 10.16.1.0/24

### Run Scan
Via web UI: Scans -> Tasks -> New Task
- Select target and scan config
- Start scan

---

## Homelab Scan Targets

### Internal Infrastructure
| Target | IP/Range | Services | Priority |
|--------|----------|----------|----------|
| Proxmox Hosts | 10.16.1.22, 10.16.1.8 | 8006 | High |
| TrueNAS | 10.16.1.6, 10.16.1.20 | 443 | High |
| Pi-hole | 10.16.1.16, 10.16.1.18 | 53, 80 | High |
| NPM | 10.16.1.50 | 81, 8080, 8443 | Medium |
| Authelia | 10.16.1.25 | 9091 | High |
| Traefik | 10.16.1.26 | 80, 443, 8080 | High |
| gm-ai | 10.16.1.9 | 11434, 3000, 9090 | Medium |
| All CTs | 10.16.1.0/24 | Various | Low |

---

## Remediation Workflow

1. **Scan**: Run vulnerability scan
2. **Triage**: Prioritize by severity (Critical > High > Medium > Low)
3. **Validate**: Confirm findings are real (not false positives)
4. **Remediate**: Apply patches, config changes, or mitigations
5. **Verify**: Re-scan to confirm fix
6. **Document**: Record in compliance tracking

---

## SMB1001 Alignment

Maps to SMB1001 pillars:
- **Device Security**: Host vulnerability scanning, container scanning
- **Network Security**: Network-level vulnerability assessment

---

## Related Skills

- **patch-compliance** - Patch management and compliance tracking
- **hardening-audit** - Configuration auditing
- **linux-hardening** - Remediation of findings
- **container-ops** - Container image scanning in CI/CD
- **smb1001-security-ops** - SMB1001 compliance evidence

---
name: osint-recon
version: 1.0.0
description: When the user wants to perform external reconnaissance -- attack surface discovery, OSINT, domain intelligence, or exposed service detection. Also use when the user mentions "OSINT," "reconnaissance," "attack surface," "Shodan," "Censys," "domain intel," "certificate transparency," or "exposed services." For internal scanning, see vuln-scanning.
---

# OSINT & Reconnaissance

You are an expert in open-source intelligence and attack surface reconnaissance.

## Scope

This skill covers three use cases:
1. **Homelab**: Discover externally exposed services from the homelab
2. **External recon**: Attack surface monitoring for domains/IPs
3. **Client assessments**: OSINT for Cyber People SMB1001 engagements

## Guard Rails

**Auto-approve**: Passive reconnaissance (DNS lookups, certificate queries, public data)
**Confirm first**: Active scanning of external targets, client domain scanning

---

## Domain Reconnaissance

### DNS Enumeration
```bash
# A records
dig <domain> A +short

# MX records (email)
dig <domain> MX +short

# TXT records (SPF, DKIM, DMARC)
dig <domain> TXT +short

# NS records
dig <domain> NS +short

# All records
dig <domain> ANY +short
```

### Subdomain Discovery
```bash
# Certificate transparency logs
curl -s "https://crt.sh/?q=%25.<domain>&output=json" | jq -r '.[].name_value' | sort -u

# DNS brute force (if subfinder installed)
subfinder -d <domain> -silent
```

### WHOIS
```bash
whois <domain>
```

---

## Shodan (Internet-Wide Scanning)

### Search by IP
```bash
shodan host <ip>
```

### Search by Query
```bash
shodan search "org:\"<company>\" port:443"
shodan search "hostname:<domain>"
```

### Check Your External IP
```bash
shodan myip
```

### Monitor Homelab External Exposure
```bash
# Check what's visible from outside
shodan host <external_ip>

# Check Cloudflare tunnel exposure
shodan search "ssl.cert.subject.CN:<domain>"
```

---

## Certificate Transparency

### Find Certificates for Domain
```bash
curl -s "https://crt.sh/?q=<domain>&output=json" | jq -r '.[] | "\(.not_before) \(.name_value)"' | sort -u
```

### Check Certificate Details
```bash
echo | openssl s_client -connect <domain>:443 2>/dev/null | openssl x509 -noout -text | head -30
```

---

## Email Security Assessment

### SPF Check
```bash
dig <domain> TXT +short | grep spf
```

### DMARC Check
```bash
dig _dmarc.<domain> TXT +short
```

### DKIM Check
```bash
dig <selector>._domainkey.<domain> TXT +short
```

### MX Records
```bash
dig <domain> MX +short
```

---

## Web Technology Fingerprinting

### HTTP Headers
```bash
curl -sI https://<domain> | head -20
```

### Server Detection
```bash
curl -sI https://<domain> | grep -i "server\|x-powered-by\|x-aspnet"
```

### SSL/TLS Analysis
```bash
# Check SSL configuration
nmap --script ssl-enum-ciphers -p 443 <target>

# Or use testssl.sh
testssl.sh <domain>
```

---

## Homelab External Exposure Check

### What's Visible via Cloudflare Tunnel
```bash
# Check Cloudflare tunnel status
ssh pve-scratchy "pct exec 114 -- cloudflared tunnel info"

# Check what domains route through the tunnel
dig +short <domain> | head -5
```

### External Port Exposure
```bash
# Check from external perspective (via Shodan or nmap from outside)
# These should NOT be directly exposed:
# - 8006 (Proxmox)
# - 443 (TrueNAS)
# - 22 (SSH)
# - 53 (DNS)
```

---

## Client Assessment Template

For SMB1001 external assessments:

1. **Domain enumeration**: Subdomains, DNS records
2. **Email security**: SPF, DKIM, DMARC
3. **Web exposure**: Public-facing services, SSL config
4. **Credential leaks**: Check HaveIBeenPwned API
5. **Social media**: LinkedIn, public employee info
6. **Technology stack**: Identify frameworks, CMS, cloud providers

---

## SMB1001 Alignment

Maps to SMB1001 pillars:
- **Network Security**: External attack surface monitoring
- **Identity & Access Management**: Credential leak detection
- **Data Protection**: Email security (SPF/DKIM/DMARC)

---

## Related Skills

- **vuln-scanning** - Internal vulnerability scanning
- **hardening-audit** - Configuration security review
- **smb1001-security-ops** - SMB1001 compliance evidence collection

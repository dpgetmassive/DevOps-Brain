---
name: m365-security
version: 1.0.0
description: When the user wants to manage M365 security -- Defender for M365, compliance policies, audit logs, or DLP rules. Also use when the user mentions "Defender," "M365 security," "compliance," "audit log," "DLP," "data loss prevention," or "secure score." Maps to SMB1001 Data Protection pillar. For identity security, see entra-admin.
---

# M365 Security & Compliance

You are an expert in Microsoft 365 security and compliance administration.

## Prerequisites

**PowerShell modules**:
```powershell
Install-Module Microsoft.Graph -Scope CurrentUser
Install-Module ExchangeOnlineManagement -Scope CurrentUser
```

**Connect with security scopes**:
```powershell
Connect-MgGraph -Scopes "SecurityEvents.Read.All", "AuditLog.Read.All", "Policy.Read.All"
Connect-ExchangeOnline -UserPrincipalName <admin@domain>
```

## Guard Rails

**Auto-approve**: Viewing security scores, audit logs, alert summaries, compliance status
**Confirm first**: Policy creation/modification, DLP rule changes, alert suppression

---

## Secure Score

### View Current Secure Score
```powershell
Get-MgSecuritySecureScore -Top 1 | Select-Object CurrentScore, MaxScore, @{N='Percentage';E={[math]::Round(($_.CurrentScore/$_.MaxScore)*100,1)}}
```

### View Improvement Actions
```powershell
Get-MgSecuritySecureScoreControlProfile | Select-Object Title, @{N='MaxScore';E={$_.MaxScore}} | Sort-Object MaxScore -Descending | Format-Table
```

---

## Audit Log

### Search Audit Log (Last 24h)
```powershell
$start = (Get-Date).AddDays(-1).ToString("yyyy-MM-dd")
$end = (Get-Date).ToString("yyyy-MM-dd")
Search-UnifiedAuditLog -StartDate $start -EndDate $end -ResultSize 50 | Select-Object CreationDate, UserIds, Operations | Format-Table
```

### Search for Specific Activity
```powershell
Search-UnifiedAuditLog -StartDate $start -EndDate $end -Operations "UserLoggedIn" -ResultSize 20
```

### Search Failed Logins
```powershell
Search-UnifiedAuditLog -StartDate $start -EndDate $end -Operations "UserLoginFailed" -ResultSize 50 | Select-Object CreationDate, UserIds
```

---

## Defender for Microsoft 365

### View Security Alerts
```powershell
Get-MgSecurityAlert -Top 20 | Select-Object Title, Severity, Status, CreatedDateTime | Format-Table
```

### View Threat Intelligence
```powershell
Get-MgSecurityThreatIntelligenceArticle -Top 10 | Select-Object Title, CreatedDateTime
```

---

## Data Loss Prevention (DLP)

### List DLP Policies
```powershell
Get-DlpCompliancePolicy | Select-Object Name, Mode, Enabled | Format-Table
```

### List DLP Rules
```powershell
Get-DlpComplianceRule | Select-Object Name, Policy, Disabled | Format-Table
```

### View DLP Incidents
```powershell
# Via compliance center or Graph API
Get-MgSecurityAlert -Filter "category eq 'DataLossPrevention'" | Select-Object Title, Severity
```

---

## Anti-Phishing

### Check Anti-Phishing Policies
```powershell
Get-AntiPhishPolicy | Select-Object Name, Enabled, PhishThresholdLevel | Format-Table
```

### Check Safe Links Policies
```powershell
Get-SafeLinksPolicy | Select-Object Name, IsEnabled | Format-Table
```

### Check Safe Attachments Policies
```powershell
Get-SafeAttachmentPolicy | Select-Object Name, Enable | Format-Table
```

---

## Compliance

### View Compliance Score
Access via: https://compliance.microsoft.com/compliancemanager

### View Retention Policies
```powershell
Get-RetentionCompliancePolicy | Select-Object Name, Enabled, Mode | Format-Table
```

### View Sensitivity Labels
```powershell
Get-Label | Select-Object DisplayName, Priority, Disabled | Format-Table
```

---

## SMB1001 Alignment

Maps to **SMB1001 Data Protection** pillar:
- **Control**: Email security (anti-phishing, safe links/attachments)
- **Control**: Data classification and DLP
- **Control**: Audit logging enabled
- **Control**: Security monitoring active

Also maps to **Identity & Access Management**:
- **Control**: Security alerts monitored
- **Control**: Secure score tracked and improved

---

## Related Skills

- **entra-admin** - Identity and conditional access
- **m365-admin** - Service administration
- **smb1001-security-ops** - SMB1001 compliance evidence

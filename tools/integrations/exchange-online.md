# Exchange Online Management

Exchange Online Management PowerShell module (`ExchangeOnlineManagement`) provides cmdlets for managing Exchange Online mailboxes, transport rules, compliance policies, and mail flow. Requires modern authentication via `Connect-ExchangeOnline`.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | N | Exchange Online REST API exists but module wraps it via PowerShell |
| MCP | N | No MCP server available |
| CLI | Y | PowerShell cmdlets via `ExchangeOnlineManagement` module |
| SDK | Y | PowerShell module only (no separate SDK) |

## Authentication

**Modern Authentication**: Connect using `Connect-ExchangeOnline` with interactive login or certificate-based app-only auth.

```powershell
# Interactive login (browser-based)
Connect-ExchangeOnline

# With user principal name
Connect-ExchangeOnline -UserPrincipalName "admin@domain.com"

# Certificate-based (app-only, unattended)
Connect-ExchangeOnline -AppId "app-id" -CertificateFilePath "cert.pfx" -CertificatePassword (ConvertTo-SecureString -String "password" -AsPlainText -Force) -Organization "domain.com"

# Show connection status
Get-ConnectionInformation
```

**Module Installation**: Install from PowerShell Gallery.

```powershell
# Install module
Install-Module ExchangeOnlineManagement -Scope CurrentUser

# Update module
Update-Module ExchangeOnlineManagement

# Import module
Import-Module ExchangeOnlineManagement
```

## Common Agent Operations

### Mailbox Management

```powershell
# List and query mailboxes
Get-EXOMailbox -ResultSize Unlimited
Get-EXOMailbox -Identity "user@domain.com"
Get-EXOMailboxStatistics -Identity "user@domain.com"
Get-EXOMailboxPermission -Identity "user@domain.com"
Get-EXOMailboxFolderStatistics -Identity "user@domain.com"
```

### Transport Rules and Policies

```powershell
# Transport rules
Get-TransportRule
Get-TransportRule -Identity "Rule Name"
New-TransportRule -Name "Block External" -FromScope NotInOrganization -RejectMessageReasonText "External emails blocked"
Set-TransportRule -Identity "Rule Name" -Enabled $true

# Anti-phish policies
Get-AntiPhishPolicy
Get-AntiPhishPolicy -Identity "Policy Name"
New-AntiPhishPolicy -Name "Strict Policy" -Enabled $true -AdminDisplayName "Strict Anti-Phish"

# Mail flow
Get-MailFlowRule
Test-MailFlow -TargetEmailAddress "user@domain.com"
```

### Compliance and Message Trace

```powershell
# Compliance policies
Get-RetentionCompliancePolicy
Get-RetentionComplianceTag
Get-DlpCompliancePolicy
Get-AdminAuditLogConfig

# Message trace
Get-MessageTrace -StartDate (Get-Date).AddDays(-1) -EndDate (Get-Date)
Get-MessageTraceDetail -MessageTraceId "trace-id"
```

## Key Objects/Metrics

- **Mailboxes**: User mailboxes, shared mailboxes, resource mailboxes, statistics
- **Transport Rules**: Mail flow rules, conditions, actions
- **Anti-Phish Policies**: Phishing protection settings, impersonation protection
- **Compliance Policies**: Data loss prevention (DLP), retention policies, eDiscovery
- **Message Trace**: Email delivery tracking, routing information
- **Permissions**: Mailbox permissions, send-as, full access

## When to Use

- **Mailbox administration**: Manage mailboxes, check statistics, configure permissions
- **Mail flow management**: Create transport rules, configure routing, troubleshoot delivery
- **Security policies**: Configure anti-phish policies, DLP policies, compliance rules
- **Troubleshooting**: Trace messages, check delivery status, investigate mail flow issues
- **Compliance**: Configure retention policies, manage eDiscovery, audit mailbox access

## Rate Limits

Exchange Online cmdlets are subject to throttling (typically 10-30 requests per second per user). Use `-ResultSize Unlimited` for pagination, implement retry logic for 429 responses, and batch operations.

## Relevant Skills

- `m365-admin` - Microsoft 365 tenant administration including Exchange
- `m365-security` - Security policy management and compliance

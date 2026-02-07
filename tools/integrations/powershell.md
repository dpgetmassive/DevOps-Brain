# PowerShell 7 + Microsoft.Graph Module

PowerShell 7 (pwsh) is the cross-platform command-line shell and scripting language. The Microsoft.Graph module provides cmdlets for managing Microsoft 365 and Azure AD (Entra ID) services. Used for automation, user management, and administrative tasks.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | N | PowerShell IS the CLI tool (wraps Microsoft Graph API calls) |
| MCP | N | No MCP server available |
| CLI | Y | `pwsh` (PowerShell 7) command-line tool, cross-platform |
| SDK | Y | PowerShell modules: `Microsoft.Graph`, `ExchangeOnlineManagement`, `MicrosoftTeams` |

## Authentication

**Microsoft Graph**: Connect using `Connect-MgGraph` with scopes or client credentials.

```powershell
# Interactive login with scopes
Connect-MgGraph -Scopes "User.Read.All", "Group.ReadWrite.All"

# Client credentials (service principal)
Connect-MgGraph -ClientId "app-id" -ClientSecret "secret" -TenantId "tenant-id"

# Device code flow (non-interactive)
Connect-MgGraph -Scopes "User.Read.All" -UseDeviceAuthentication

# Check connection
Get-MgContext
```

**Exchange Online**: Connect using `Connect-ExchangeOnline` with modern authentication.

```powershell
# Interactive login
Connect-ExchangeOnline

# With user principal name
Connect-ExchangeOnline -UserPrincipalName "admin@domain.com"

# With certificate (app-only)
Connect-ExchangeOnline -AppId "app-id" -CertificateFilePath "cert.pfx" -Organization "domain.com"
```

**Module Installation**: Install modules from PowerShell Gallery.

```powershell
# Install modules
Install-Module Microsoft.Graph -Scope CurrentUser
Install-Module ExchangeOnlineManagement -Scope CurrentUser
Update-Module Microsoft.Graph
```

## Common Agent Operations

### Microsoft Graph Operations

```powershell
# User management
Get-MgUser -All
Get-MgUser -UserId "user@domain.com"
New-MgUser -DisplayName "John Doe" -UserPrincipalName "john@domain.com" -PasswordProfile @{Password="TempPass123!"}
Update-MgUser -UserId "user-id" -DisplayName "Updated Name"

# Group management
Get-MgGroup -All
Get-MgGroupMember -GroupId "group-id"
New-MgGroup -DisplayName "New Group" -MailEnabled:$false -SecurityEnabled:$true
New-MgGroupMember -GroupId "group-id" -DirectoryObjectId "user-id"
```

### Exchange Online Operations

```powershell
# Mailbox management
Get-EXOMailbox -ResultSize Unlimited
Get-EXOMailbox -Identity "user@domain.com"
Get-EXOMailboxStatistics -Identity "user@domain.com"

# Transport rules and policies
Get-TransportRule
Get-AntiPhishPolicy
Get-MailFlowRule
```

### Module and Script Management

```powershell
# Module operations
Get-Module -ListAvailable
Import-Module Microsoft.Graph
Get-Command -Module Microsoft.Graph

# Script execution
pwsh -File script.ps1
pwsh -Command "Get-MgUser -All"
```

## Key Objects/Metrics

- **Users**: User accounts, profiles, licenses, authentication methods
- **Groups**: Security groups, Microsoft 365 groups, distribution lists
- **Mailboxes**: Exchange mailboxes, statistics, permissions
- **Policies**: Conditional access, anti-phish, transport rules

## When to Use

- **User management**: Bulk user operations, license assignment, profile updates
- **Group management**: Create groups, manage membership, assign roles
- **Exchange administration**: Mailbox management, transport rules, compliance policies
- **Automation**: Scheduled scripts, bulk operations, reporting
## Rate Limits

PowerShell cmdlets inherit rate limits from Microsoft Graph API (typically 10,000 requests per 10 minutes) and Exchange Online API. Use `-All` parameter for pagination, implement retry logic for 429 responses, and batch operations.

## Relevant Skills

- `entra-admin` - Azure AD user and group management via PowerShell
- `m365-admin` - Microsoft 365 tenant administration
- `m365-security` - Security monitoring and compliance operations

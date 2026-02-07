# Microsoft Graph API

Microsoft Graph API provides programmatic access to Microsoft 365 and Azure AD (Entra ID) services including users, groups, applications, security, and audit logs. REST API endpoint at `https://graph.microsoft.com/v1.0/` with OAuth 2.0 authentication.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `https://graph.microsoft.com/v1.0/`, also beta endpoint at `/v1.0/` |
| MCP | N | No MCP server available |
| CLI | Y | PowerShell `Microsoft.Graph` module (`Connect-MgGraph`, cmdlets) |
| SDK | Y | PowerShell, Python (`msgraph-sdk`), C# (`Microsoft.Graph`), JavaScript (`@microsoft/microsoft-graph-client`) |

## Authentication

**OAuth 2.0 Client Credentials**: App registration with client ID and secret (service principal). Use for unattended automation.

```bash
# PowerShell - Connect with client credentials
Connect-MgGraph -ClientId "app-id" -ClientSecret "secret" -TenantId "tenant-id"

# Python example
from msal import ConfidentialClientApplication
app = ConfidentialClientApplication(
    client_id="app-id",
    client_credential="secret",
    authority="https://login.microsoftonline.com/tenant-id"
)
token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
```

**OAuth 2.0 Delegated**: User authentication with interactive login or device code flow. Use for user-scoped operations.

```bash
# PowerShell - Interactive login
Connect-MgGraph -Scopes "User.Read.All", "Group.ReadWrite.All"

# PowerShell - Device code flow (non-interactive)
Connect-MgGraph -Scopes "User.Read.All" -UseDeviceAuthentication
```

**Access Token**: Use bearer token in Authorization header for REST API calls.

```bash
# REST API call with token
curl -H "Authorization: Bearer $TOKEN" \
  https://graph.microsoft.com/v1.0/users
```

## Common Agent Operations

### User and Group Management

```bash
# PowerShell - Users
Get-MgUser -All
Get-MgUser -UserId "user@domain.com"
New-MgUser -DisplayName "John Doe" -UserPrincipalName "john@domain.com" -PasswordProfile @{Password="TempPass123!"} -AccountEnabled

# PowerShell - Groups
Get-MgGroup -All
Get-MgGroupMember -GroupId "group-id"
New-MgGroupMember -GroupId "group-id" -DirectoryObjectId "user-id"

# REST API
curl -H "Authorization: Bearer $TOKEN" https://graph.microsoft.com/v1.0/users
curl -H "Authorization: Bearer $TOKEN" https://graph.microsoft.com/v1.0/groups
```

### Security and Compliance

```bash
# PowerShell - Audit logs
Get-MgAuditLogSignIn -All
Get-MgAuditLogDirectoryAudit -All

# PowerShell - Conditional Access
Get-MgIdentityConditionalAccessPolicy
Get-MgIdentityConditionalAccessPolicy -ConditionalAccessPolicyId "policy-id"

# REST API
curl -H "Authorization: Bearer $TOKEN" "https://graph.microsoft.com/v1.0/auditLogs/signIns"
curl -H "Authorization: Bearer $TOKEN" https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies
```

## Key Objects/Metrics

- **Users**: User accounts, profiles, licenses, sign-in activity
- **Groups**: Security groups, Microsoft 365 groups, membership
- **Applications**: App registrations, service principals, permissions
- **Directory Roles**: Azure AD roles and assignments
- **Audit Logs**: Sign-in logs, directory audit logs, provisioning logs
- **Conditional Access**: Policies, risk detections, compliance status

## When to Use

- **User management**: Create users, assign licenses, manage profiles, reset passwords
- **Group management**: Create groups, manage membership, assign roles
- **Security monitoring**: Review sign-in logs, audit directory changes, investigate anomalies
- **Compliance**: Export audit logs, verify conditional access policies, check compliance status
- **Automation**: Bulk user operations, license management, group synchronization

## Rate Limits

**Throttling**: Microsoft Graph implements throttling based on workload and tenant size.

- **Default limits**: Varies by endpoint (typically 10,000 requests per 10 minutes)
- **429 responses**: Throttled requests return HTTP 429 with `Retry-After` header
- **Best practices**: Implement exponential backoff, batch requests, use delta queries

```bash
# Check throttling headers
curl -I -H "Authorization: Bearer $TOKEN" https://graph.microsoft.com/v1.0/users
```

## Relevant Skills

- `entra-admin` - Azure AD user and group management
- `m365-admin` - Microsoft 365 tenant administration
- `m365-security` - Security monitoring and compliance

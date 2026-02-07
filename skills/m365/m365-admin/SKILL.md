---
name: m365-admin
version: 1.0.0
description: When the user wants to administer Microsoft 365 services -- Exchange Online, SharePoint, Teams, or licensing. Also use when the user mentions "M365," "Exchange Online," "SharePoint," "Teams," "licensing," "mailbox," or "Office 365." For identity management, see entra-admin. For security, see m365-security.
---

# M365 Administration

You are an expert in Microsoft 365 tenant administration.

## Prerequisites

**PowerShell modules**:
```powershell
Install-Module Microsoft.Graph -Scope CurrentUser
Install-Module ExchangeOnlineManagement -Scope CurrentUser
```

**Connect to Exchange Online**:
```powershell
Connect-ExchangeOnline -UserPrincipalName <admin@domain>
```

**Connect to Graph (for Teams/SharePoint)**:
```powershell
Connect-MgGraph -Scopes "User.Read.All", "Organization.Read.All"
```

**NOTE**: Tenant details need to be populated when available.

## Guard Rails

**Auto-approve**: Viewing licenses, mailbox info, Teams policies, SharePoint sites
**Confirm first**: License assignment/removal, mailbox creation, policy changes

---

## License Management

### View Available Licenses
```powershell
Get-MgSubscribedSku | Select-Object SkuPartNumber, ConsumedUnits, @{N='Total';E={$_.PrepaidUnits.Enabled}} | Format-Table
```

### Check User License
```powershell
Get-MgUserLicenseDetail -UserId "<user@domain>" | Select-Object SkuPartNumber | Format-Table
```

### Assign License
```powershell
$sku = Get-MgSubscribedSku | Where-Object { $_.SkuPartNumber -eq "<SkuName>" }
Set-MgUserLicense -UserId "<user@domain>" -AddLicenses @{SkuId = $sku.SkuId} -RemoveLicenses @()
```

### Remove License
```powershell
$sku = Get-MgSubscribedSku | Where-Object { $_.SkuPartNumber -eq "<SkuName>" }
Set-MgUserLicense -UserId "<user@domain>" -AddLicenses @() -RemoveLicenses @($sku.SkuId)
```

---

## Exchange Online

### List Mailboxes
```powershell
Get-EXOMailbox | Select-Object DisplayName, PrimarySmtpAddress, RecipientType | Format-Table
```

### Check Mailbox Size
```powershell
Get-EXOMailboxStatistics -Identity "<user@domain>" | Select-Object DisplayName, TotalItemSize, ItemCount
```

### Create Shared Mailbox
```powershell
New-Mailbox -Shared -Name "<Name>" -DisplayName "<Display Name>" -Alias "<alias>"
```

### Set Auto-Reply
```powershell
Set-MailboxAutoReplyConfiguration -Identity "<user@domain>" -AutoReplyState Enabled -InternalMessage "Out of office" -ExternalMessage "Out of office"
```

### View Mail Flow Rules
```powershell
Get-TransportRule | Select-Object Name, State, Priority | Format-Table
```

---

## SharePoint Online

### List Sites
```powershell
Get-MgSite -Search "*" | Select-Object DisplayName, WebUrl | Format-Table
```

### Check Site Storage
```powershell
# Via SharePoint Admin PowerShell
Get-SPOSite -Limit All | Select-Object Url, StorageUsageCurrent, StorageQuota | Format-Table
```

---

## Teams Administration

### List Teams
```powershell
Get-MgGroup -Filter "resourceProvisioningOptions/any(x:x eq 'Team')" | Select-Object DisplayName, Id | Format-Table
```

### Create Team
```powershell
$params = @{
    "template@odata.bind" = "https://graph.microsoft.com/v1.0/teamsTemplates('standard')"
    DisplayName = "<Team Name>"
    Description = "<Description>"
}
New-MgTeam -BodyParameter $params
```

---

## Tenant Information

### View Tenant Details
```powershell
Get-MgOrganization | Select-Object DisplayName, VerifiedDomains, TechnicalNotificationMails
```

### View Service Health
```powershell
Get-MgServiceAnnouncementHealthOverview | Select-Object Service, Status | Format-Table
```

---

## Related Skills

- **entra-admin** - Identity and access management
- **m365-security** - Security and compliance
- **smb1001-security-ops** - SMB1001 compliance

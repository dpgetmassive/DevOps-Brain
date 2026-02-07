---
name: entra-admin
version: 1.0.0
description: When the user wants to manage Microsoft Entra ID (Azure AD) -- user/group lifecycle, conditional access policies, MFA enforcement, role assignments, or security defaults. Also use when the user mentions "Entra," "Azure AD," "conditional access," "MFA," "users," "groups," or "identity management." For M365 service admin, see m365-admin. For security, see m365-security.
---

# Entra ID Administration

You are an expert in Microsoft Entra ID (formerly Azure AD) tenant administration.

## Prerequisites

**PowerShell modules required**:
```powershell
Install-Module Microsoft.Graph -Scope CurrentUser
Install-Module Microsoft.Graph.Beta -Scope CurrentUser
```

**Authentication**:
```powershell
Connect-MgGraph -Scopes "User.ReadWrite.All", "Group.ReadWrite.All", "Policy.ReadWrite.ConditionalAccess", "RoleManagement.ReadWrite.Directory"
```

**NOTE**: M365 tenant details (tenant ID, subscription level, existing policies) need to be populated in `context/infrastructure-context.md` when available.

## Guard Rails

**Auto-approve**: User/group listing, policy viewing, role assignments review
**Confirm first**: User creation/deletion, conditional access changes, MFA enforcement changes

---

## User Management

### List All Users
```powershell
Get-MgUser -All | Select-Object DisplayName, UserPrincipalName, AccountEnabled | Format-Table
```

### Create User
```powershell
$PasswordProfile = @{
    Password = '<TempPassword123!>'
    ForceChangePasswordNextSignIn = $true
}
New-MgUser -DisplayName "<Name>" `
  -MailNickname "<alias>" `
  -UserPrincipalName "<user>@<domain>" `
  -PasswordProfile $PasswordProfile `
  -AccountEnabled
```

### Disable User
```powershell
Update-MgUser -UserId "<user@domain>" -AccountEnabled:$false
```

### Reset Password
```powershell
$params = @{
    PasswordProfile = @{
        Password = "<NewTempPassword!>"
        ForceChangePasswordNextSignIn = $true
    }
}
Update-MgUser -UserId "<user@domain>" -BodyParameter $params
```

### Delete User
```powershell
Remove-MgUser -UserId "<user@domain>"
```

---

## Group Management

### List Groups
```powershell
Get-MgGroup -All | Select-Object DisplayName, GroupTypes, SecurityEnabled | Format-Table
```

### Create Security Group
```powershell
New-MgGroup -DisplayName "<GroupName>" -SecurityEnabled -MailEnabled:$false -MailNickname "<nickname>"
```

### Add User to Group
```powershell
New-MgGroupMember -GroupId "<group-id>" -DirectoryObjectId "<user-id>"
```

### List Group Members
```powershell
Get-MgGroupMember -GroupId "<group-id>" | Select-Object Id, AdditionalProperties
```

---

## Conditional Access

### List Policies
```powershell
Get-MgIdentityConditionalAccessPolicy | Select-Object DisplayName, State | Format-Table
```

### Create Basic MFA Policy
```powershell
$params = @{
    DisplayName = "Require MFA for all users"
    State = "enabledForReportingButNotEnforced"
    Conditions = @{
        Users = @{ IncludeUsers = @("All") }
        Applications = @{ IncludeApplications = @("All") }
    }
    GrantControls = @{
        Operator = "OR"
        BuiltInControls = @("mfa")
    }
}
New-MgIdentityConditionalAccessPolicy -BodyParameter $params
```

### Block Legacy Authentication
```powershell
$params = @{
    DisplayName = "Block legacy authentication"
    State = "enabled"
    Conditions = @{
        Users = @{ IncludeUsers = @("All") }
        Applications = @{ IncludeApplications = @("All") }
        ClientAppTypes = @("exchangeActiveSync", "other")
    }
    GrantControls = @{
        Operator = "OR"
        BuiltInControls = @("block")
    }
}
New-MgIdentityConditionalAccessPolicy -BodyParameter $params
```

---

## MFA Management

### Check MFA Status for Users
```powershell
Get-MgUser -All | ForEach-Object {
    $methods = Get-MgUserAuthenticationMethod -UserId $_.Id
    [PSCustomObject]@{
        User = $_.DisplayName
        Methods = $methods.Count
    }
} | Format-Table
```

---

## Role Assignments

### List Admin Roles
```powershell
Get-MgDirectoryRole | Select-Object DisplayName, Id | Format-Table
```

### List Global Admins
```powershell
$role = Get-MgDirectoryRole | Where-Object { $_.DisplayName -eq "Global Administrator" }
Get-MgDirectoryRoleMember -DirectoryRoleId $role.Id
```

---

## SMB1001 Alignment

Maps to **SMB1001 Identity & Access Management** pillar:
- **Control**: Unique user accounts
- **Control**: MFA enabled for all users
- **Control**: Admin access restricted and monitored
- **Control**: Access reviews conducted

---

## Related Skills

- **m365-admin** - M365 service administration
- **m365-security** - Defender and compliance
- **smb1001-security-ops** - SMB1001 IAM controls

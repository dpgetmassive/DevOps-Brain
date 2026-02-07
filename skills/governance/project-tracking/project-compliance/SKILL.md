---
name: project-compliance
version: 1.0.0
description: When the user wants to validate project compliance, check compliance checklist status, generate compliance reports, or assess SMB1001 alignment. Also use when the user mentions "compliance check," "validate compliance," "compliance audit," "check project compliance," "SMB1001 check," or "compliance status." Provides soft warnings (reminders) but does not block merges.
---

# Project Compliance

You are an expert in project compliance validation. You check projects against SMB1001 controls, security requirements, and operational standards. You provide soft warnings (reminders) but do not block operations.

## Guard Rails

**Auto-approve**: Compliance checks, status reports, checklist validation, evidence collection
**Confirm first**: Modifying compliance thresholds, changing compliance definitions, automated remediation

---

## Prerequisites

**Read `context/infrastructure-context.md` first** to understand the environment.

**Read `context/projects-registry.md`** to see active projects.

**Required context**:
- Project directory: `projects/{project-name}/`
- Compliance checklist: `projects/{project-name}/compliance/checklist.md`
- Project metadata: `projects/{project-name}/.project-metadata.yml`

---

## Compliance Validation Process

### Step 1: Load Project Metadata

```bash
PROJECT_NAME="monitoring-dashboard"
PROJECT_DIR="projects/${PROJECT_NAME}"

# Read metadata
if [ -f "${PROJECT_DIR}/.project-metadata.yml" ]; then
  # Parse YAML (requires yq or similar)
  OWNER=$(yq '.project.owner' "${PROJECT_DIR}/.project-metadata.yml")
  TYPE=$(yq '.project.type' "${PROJECT_DIR}/.project-metadata.yml")
  STATUS=$(yq '.project.status' "${PROJECT_DIR}/.project-metadata.yml")
fi
```

### Step 2: Check Compliance Checklist

```bash
# Read checklist
CHECKLIST="${PROJECT_DIR}/compliance/checklist.md"

# Count completed vs total items
TOTAL=$(grep -c "^- \[" "${CHECKLIST}" || echo "0")
COMPLETED=$(grep -c "^- \[x\]" "${CHECKLIST}" || echo "0")
PENDING=$((TOTAL - COMPLETED))

# Calculate completion percentage
if [ "$TOTAL" -gt 0 ]; then
  PERCENT=$((COMPLETED * 100 / TOTAL))
else
  PERCENT=0
fi
```

### Step 3: Validate by Category

```bash
# Infrastructure compliance
INFRA_TOTAL=$(grep -A 20 "## Infrastructure" "${CHECKLIST}" | grep -c "^- \[" || echo "0")
INFRA_DONE=$(grep -A 20 "## Infrastructure" "${CHECKLIST}" | grep -c "^- \[x\]" || echo "0")

# Security compliance
SEC_TOTAL=$(grep -A 20 "## Security" "${CHECKLIST}" | grep -c "^- \[" || echo "0")
SEC_DONE=$(grep -A 20 "## Security" "${CHECKLIST}" | grep -c "^- \[x\]" || echo "0")

# Documentation compliance
DOCS_TOTAL=$(grep -A 20 "## Documentation" "${CHECKLIST}" | grep -c "^- \[" || echo "0")
DOCS_DONE=$(grep -A 20 "## Documentation" "${CHECKLIST}" | grep -c "^- \[x\]" || echo "0")

# Testing compliance
TEST_TOTAL=$(grep -A 20 "## Testing" "${CHECKLIST}" | grep -c "^- \[" || echo "0")
TEST_DONE=$(grep -A 20 "## Testing" "${CHECKLIST}" | grep -c "^- \[x\]" || echo "0")
```

---

## Compliance Report Generation

### Generate Report

```bash
cat > "${PROJECT_DIR}/compliance/report-$(date +%Y%m%d).md" << EOF
# Compliance Report: ${PROJECT_NAME}

**Date**: $(date +%Y-%m-%d)
**Status**: $([ "$PERCENT" -eq 100 ] && echo "✅ Compliant" || echo "⚠️ In Progress")
**Completion**: ${PERCENT}% (${COMPLETED}/${TOTAL} items)

## Summary

| Category | Completed | Total | Status |
|----------|-----------|-------|--------|
| Infrastructure | ${INFRA_DONE} | ${INFRA_TOTAL} | $([ "$INFRA_DONE" -eq "$INFRA_TOTAL" ] && echo "✅" || echo "⚠️") |
| Security | ${SEC_DONE} | ${SEC_TOTAL} | $([ "$SEC_DONE" -eq "$SEC_TOTAL" ] && echo "✅" || echo "⚠️") |
| Documentation | ${DOCS_DONE} | ${DOCS_TOTAL} | $([ "$DOCS_DONE" -eq "$DOCS_TOTAL" ] && echo "✅" || echo "⚠️") |
| Testing | ${TEST_DONE} | ${TEST_TOTAL} | $([ "$TEST_DONE" -eq "$TEST_TOTAL" ] && echo "✅" || echo "⚠️") |

## Pending Items

$(grep -B 1 "^- \[ \]" "${CHECKLIST}" | grep "^-" | sed 's/^- \[ \]/- /')

## Recommendations

$([ "$PERCENT" -lt 50 ] && echo "- ⚠️ **Low compliance**: Consider completing critical items before deployment")
$([ "$PERCENT" -ge 50 ] && [ "$PERCENT" -lt 100 ] && echo "- ℹ️ **Partial compliance**: Review pending items before production deployment")
$([ "$PERCENT" -eq 100 ] && echo "- ✅ **Full compliance**: All checklist items completed")
EOF
```

---

## SMB1001 Control Mapping

### Check SMB1001 Mapping

```bash
SMB1001_MAP="${PROJECT_DIR}/compliance/smb1001-mapping.md"

if [ -f "${SMB1001_MAP}" ]; then
  # Count mapped controls
  CONTROLS=$(grep -c "^###" "${SMB1001_MAP}" || echo "0")
  
  echo "SMB1001 Controls Mapped: ${CONTROLS}"
  
  # List affected controls
  grep "^###" "${SMB1001_MAP}" | sed 's/^### //'
else
  echo "⚠️ No SMB1001 mapping found. Consider running SMB1001 assessment."
fi
```

### Generate SMB1001 Evidence Checklist

```bash
# Use smb1001-security-ops skill to collect evidence
# Reference: skills/security/smb1001-security-ops/SKILL.md

cat > "${PROJECT_DIR}/compliance/smb1001-evidence-checklist.md" << EOF
# SMB1001 Evidence Checklist

## Identity & Access Management
- [ ] User accounts documented
- [ ] Access controls defined
- [ ] MFA requirements documented
- [ ] SSH configuration hardened

## Data Protection
- [ ] Backup strategy documented
- [ ] Encryption requirements defined
- [ ] Data retention policy documented

## Device Security
- [ ] Patch compliance verified
- [ ] Hardening checklist completed
- [ ] Vulnerability scanning scheduled

## Network Security
- [ ] Network requirements documented
- [ ] Firewall rules defined
- [ ] Network segmentation verified

## Incident Response
- [ ] Monitoring configured
- [ ] Alerting configured
- [ ] Incident response plan documented
EOF
```

---

## Soft Warning System

### Generate PR Comment (GitHub)

When compliance is incomplete, generate a soft warning comment:

```bash
# Check compliance before PR merge
COMPLIANCE_REPORT="${PROJECT_DIR}/compliance/report-$(date +%Y%m%d).md"

if [ -f "${COMPLIANCE_REPORT}" ]; then
  PERCENT=$(grep "Completion:" "${COMPLIANCE_REPORT}" | grep -oP '\d+%' | sed 's/%//')
  
  if [ "$PERCENT" -lt 100 ]; then
    cat > /tmp/compliance-comment.md << EOF
## ⚠️ Compliance Reminder

This project has **${PERCENT}% compliance** completion. Please review pending items:

$(grep -A 50 "## Pending Items" "${COMPLIANCE_REPORT}")

**Note**: This is a reminder only. Merge is not blocked, but consider completing critical items before production deployment.

[View full compliance report](${COMPLIANCE_REPORT})
EOF
    
    # Post as PR comment (example - adjust PR number)
    gh pr comment 1 --body-file /tmp/compliance-comment.md
  fi
fi
```

### Generate Reminder Notification

```bash
# Send reminder via ntfy (if configured)
if [ "$PERCENT" -lt 100 ]; then
  ntfy send "Project ${PROJECT_NAME}: ${PERCENT}% compliance - ${PENDING} items pending"
fi
```

---

## Compliance Validation Checklist

### Pre-Deployment Check

```bash
# Critical items that should be completed before production
CRITICAL_ITEMS=(
  "Security review completed"
  "Backup strategy defined"
  "Rollback procedure documented"
  "Monitoring configured"
  "Test plan created"
)

for item in "${CRITICAL_ITEMS[@]}"; do
  if ! grep -q "\[x\].*${item}" "${CHECKLIST}"; then
    echo "⚠️ Missing critical item: ${item}"
  fi
done
```

### Post-Deployment Audit

```bash
# Verify compliance after deployment
cat > "${PROJECT_DIR}/compliance/post-deployment-audit.md" << EOF
# Post-Deployment Compliance Audit

**Deployment Date**: $(date +%Y-%m-%d)
**Deployed By**: [name]

## Verification

- [ ] Service is running and healthy
- [ ] Monitoring is active
- [ ] Alerts are configured
- [ ] Backup is working
- [ ] Documentation is updated
- [ ] Runbook is tested
- [ ] SMB1001 evidence collected

## Issues Found

[Document any compliance gaps]

## Remediation Plan

[Plan to address any gaps]
EOF
```

---

## Verify After

1. **Compliance report generated**: Check `compliance/report-*.md`
2. **Checklist status**: Review completion percentage
3. **SMB1001 mapping**: Verify controls are mapped
4. **Evidence collected**: Check `compliance/evidence/` directory

---

## Rollback

Compliance validation is read-only. No rollback needed.

---

## Troubleshooting

### Checklist file not found
- Check if project was initialized with `project-initiation` skill
- Create checklist manually using template from `project-initiation` skill

### SMB1001 mapping missing
- Use `smb1001-security-ops` skill to assess controls
- Create mapping file manually: `compliance/smb1001-mapping.md`

### Compliance percentage calculation errors
- Ensure checklist uses markdown format: `- [ ]` and `- [x]`
- Check for proper section headers: `## Infrastructure`, `## Security`, etc.

---

## Related Skills

- **project-initiation** - Creates compliance checklist during setup
- **smb1001-security-ops** - SMB1001 control assessment and evidence collection
- **patch-compliance** - Patch compliance tracking
- **hardening-audit** - Security hardening validation
- **project-tracking** - Update compliance status on project board

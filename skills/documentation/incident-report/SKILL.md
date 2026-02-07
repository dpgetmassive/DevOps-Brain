---
name: incident-report
version: 1.0.0
description: When the user wants to document incidents -- post-mortems, root cause analysis, outage reports, or action item tracking. Also use when the user mentions "incident," "post-mortem," "root cause," "outage," "what happened," or "incident report." For runbooks, see runbook-writer.
---

# Incident Report

You are an expert in incident management and post-incident documentation.

## Guard Rails

**Auto-approve**: Creating reports, reviewing incidents, documenting timelines
**Confirm first**: Closing incidents, assigning action items to others

---

## Incident Report Template

```markdown
# Incident Report: [Title]

**Incident ID**: INC-YYYY-NNN
**Date**: YYYY-MM-DD
**Duration**: [start time] - [end time] ([total duration])
**Severity**: Critical | High | Medium | Low
**Status**: Open | Resolved | Closed
**Author**: [name]

## Summary

One-paragraph description of what happened, the impact, and the resolution.

## Timeline

| Time (UTC) | Event |
|------------|-------|
| HH:MM | [First indication of problem] |
| HH:MM | [Alert triggered / user report] |
| HH:MM | [Investigation started] |
| HH:MM | [Root cause identified] |
| HH:MM | [Fix applied] |
| HH:MM | [Service restored] |
| HH:MM | [Verified resolution] |

## Impact

- **Services affected**: [list]
- **Users affected**: [number/scope]
- **Data loss**: [yes/no, details]
- **Duration**: [total downtime]

## Root Cause

Detailed technical explanation of what caused the incident.

## Resolution

Step-by-step description of how the incident was resolved.

## Detection

How was the incident detected?
- [ ] Monitoring alert (automated)
- [ ] User report
- [ ] Routine check
- [ ] Other: [describe]

**Detection time**: [time from incident start to detection]

## Contributing Factors

1. [Factor 1 - e.g., no monitoring for this specific condition]
2. [Factor 2 - e.g., missing redundancy]
3. [Factor 3 - e.g., untested configuration change]

## Action Items

| # | Action | Owner | Priority | Due Date | Status |
|---|--------|-------|----------|----------|--------|
| 1 | [Preventive action] | [who] | High | YYYY-MM-DD | Open |
| 2 | [Monitoring improvement] | [who] | Medium | YYYY-MM-DD | Open |
| 3 | [Documentation update] | [who] | Low | YYYY-MM-DD | Open |

## Lessons Learned

### What went well
- [positive 1]
- [positive 2]

### What could be improved
- [improvement 1]
- [improvement 2]

## Related

- **Monitoring alerts**: [link to ntfy/dashboard]
- **Runbook used**: [link to runbook]
- **Previous similar incidents**: [references]

---

**Report Created**: YYYY-MM-DD
**Last Updated**: YYYY-MM-DD
```

---

## Severity Levels

| Severity | Definition | Response Time |
|----------|-----------|---------------|
| Critical | Full service outage, data loss risk | Immediate |
| High | Partial outage, significant degradation | < 1 hour |
| Medium | Minor degradation, workaround available | < 4 hours |
| Low | Cosmetic issue, no user impact | Next business day |

---

## Post-Incident Process

1. **During incident**: Focus on resolution, take notes
2. **Within 24h**: Draft incident report with timeline
3. **Within 48h**: Complete root cause analysis
4. **Within 1 week**: Define and assign action items
5. **Follow-up**: Track action items to completion

---

## Common Homelab Incidents

| Scenario | Typical Root Cause | Key Metrics |
|----------|-------------------|-------------|
| DNS outage | Keepalived failure, Pi-hole crash | VIP status, FTL service |
| Backup failure | NFS mount, TrueNAS DR down, quota | Backup storage, mount status |
| Replication lag | DR quota exceeded, network | Snapshot comparison |
| Host down | Hardware, power, network | Ping, Proxmox cluster |
| Container crash | OOM, disk full, config error | Docker logs, resources |

---

## Related Skills

- **runbook-writer** - Create prevention procedures
- **infra-documentation** - Architecture documentation
- **monitoring-ops** - Alert data for timeline reconstruction

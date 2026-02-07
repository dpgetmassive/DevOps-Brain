---
name: project-documentation
version: 1.0.0
description: When the user wants to ensure project documentation is complete, generate documentation templates, create ADRs, update runbooks, or validate documentation standards. Also use when the user mentions "project documentation," "update project docs," "documentation checklist," "ADR," "project README," or "documentation standards."
---

# Project Documentation

You are an expert in project documentation standards. You ensure documentation is complete, follows standards, and stays current with the project.

## Guard Rails

**Auto-approve**: Creating documentation, generating templates, reviewing docs, updating documentation
**Confirm first**: Modifying documentation structure, deleting documentation, changing standards

---

## Prerequisites

**Read `context/infrastructure-context.md` first** to understand the environment.

**Read `context/projects-registry.md`** to see active projects.

**Required context**:
- Project directory: `projects/{project-name}/`
- Documentation directory: `projects/{project-name}/docs/`

---

## Documentation Checklist Validation

### Check Documentation Completeness

```bash
PROJECT_NAME="monitoring-dashboard"
PROJECT_DIR="projects/${PROJECT_NAME}"

# Required documentation files
REQUIRED_FILES=(
  "README.md"
  "CHANGELOG.md"
  "docs/architecture.md"
  "docs/runbooks/deployment.md"
)

MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "${PROJECT_DIR}/${file}" ]; then
    MISSING_FILES+=("${file}")
  fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
  echo "⚠️ Missing documentation files:"
  printf '  - %s\n' "${MISSING_FILES[@]}"
else
  echo "✅ All required documentation files present"
fi
```

### Validate README Quality

```bash
README="${PROJECT_DIR}/README.md"

# Check for required sections
REQUIRED_SECTIONS=(
  "Overview"
  "Quick Start"
  "Architecture"
  "Development"
  "Deployment"
  "Testing"
)

for section in "${REQUIRED_SECTIONS[@]}"; do
  if ! grep -q "## ${section}" "${README}"; then
    echo "⚠️ Missing section: ${section}"
  fi
done
```

---

## Generate Documentation Templates

### README Template

```bash
cat > "${PROJECT_DIR}/README.md" << EOF
# ${PROJECT_NAME}

${PROJECT_DESCRIPTION}

## Overview

${DETAILED_DESCRIPTION}

## Quick Start

\`\`\`bash
# Installation
[installation steps]

# Configuration
[configuration steps]

# Run
[run command]
\`\`\`

## Architecture

See [docs/architecture.md](docs/architecture.md)

## Development

### Prerequisites

- [prerequisites]

### Setup

\`\`\`bash
[setup commands]
\`\`\`

### Local Testing

\`\`\`bash
[test commands]
\`\`\`

## Deployment

See [docs/runbooks/deployment.md](docs/runbooks/deployment.md)

## Testing

See [tests/README.md](tests/README.md)

## Compliance

See [compliance/checklist.md](compliance/checklist.md)

## Contributing

[contributing guidelines]

## License

[license]
EOF
```

### Architecture Documentation Template

```bash
cat > "${PROJECT_DIR}/docs/architecture.md" << EOF
# Architecture: ${PROJECT_NAME}

## Overview

[High-level architecture description]

## Components

### Component 1
- **Purpose**: [purpose]
- **Technology**: [tech stack]
- **Dependencies**: [dependencies]

### Component 2
- **Purpose**: [purpose]
- **Technology**: [tech stack]
- **Dependencies**: [dependencies]

## Data Flow

\`\`\`mermaid
graph LR
    A[Input] --> B[Process]
    B --> C[Output]
\`\`\`

## Infrastructure

- **Host**: [hostname/IP]
- **Container/VM**: [ID or name]
- **Network**: [network requirements]
- **Storage**: [storage requirements]

## Security

- **Authentication**: [auth method]
- **Authorization**: [authz method]
- **Encryption**: [encryption details]
- **Network**: [network security]

## Monitoring

- **Metrics**: [metrics collected]
- **Alerts**: [alert rules]
- **Logging**: [logging strategy]

## Scalability

- **Horizontal scaling**: [scaling strategy]
- **Vertical scaling**: [resource limits]
- **Load balancing**: [LB strategy]
EOF
```

### ADR Template

```bash
ADR_NUMBER=$(ls "${PROJECT_DIR}/docs/adr/" 2>/dev/null | wc -l | xargs printf "%04d")
ADR_FILE="${PROJECT_DIR}/docs/adr/${ADR_NUMBER}-${TITLE_SLUG}.md"

cat > "${ADR_FILE}" << EOF
# ADR-${ADR_NUMBER}: ${TITLE}

**Date**: $(date +%Y-%m-%d)
**Status**: Proposed
**Deciders**: [who]

## Context

What is the issue that we're seeing that is motivating this decision?

## Decision

What is the change that we're proposing/doing?

## Consequences

### Positive
- [benefit 1]
- [benefit 2]

### Negative
- [tradeoff 1]
- [tradeoff 2]

### Neutral
- [neutral impact]

## Alternatives Considered

- **Alternative 1**: [description] - Rejected because [reason]
- **Alternative 2**: [description] - Rejected because [reason]
EOF
```

### Deployment Runbook Template

```bash
cat > "${PROJECT_DIR}/docs/runbooks/deployment.md" << EOF
# Deployment Runbook: ${PROJECT_NAME}

## Prerequisites

- [ ] Backup current deployment
- [ ] Verify target environment
- [ ] Review change log
- [ ] Notify stakeholders

## Deployment Steps

### 1. Pre-Deployment Checks

\`\`\`bash
# Check current version
[check command]

# Verify backups
[backup check]
\`\`\`

### 2. Deploy

\`\`\`bash
# Deployment command
[deploy command]
\`\`\`

### 3. Verify Deployment

\`\`\`bash
# Health check
[health check command]

# Smoke tests
[test commands]
\`\`\`

### 4. Post-Deployment

- [ ] Update documentation
- [ ] Update service catalog
- [ ] Notify stakeholders

## Rollback Procedure

If deployment fails:

\`\`\`bash
# Rollback command
[rollback command]

# Verify rollback
[verification command]
\`\`\`

## Troubleshooting

### Issue: [description]
**Solution**: [solution]

### Issue: [description]
**Solution**: [solution]
EOF
```

---

## Update Service Catalog

### Add to Service Catalog

```bash
# Read service inventory
SERVICE_INVENTORY="context/service-inventory.md"

cat >> "${SERVICE_INVENTORY}" << EOF

## ${PROJECT_NAME}

| Field | Value |
|-------|-------|
| **Host** | ${HOSTNAME} (${IP}) |
| **CT/VM ID** | ${ID} |
| **Port(s)** | ${PORTS} |
| **Protocol** | ${PROTOCOL} |
| **Health Check** | ${HEALTH_CHECK} |
| **Dependencies** | ${DEPENDENCIES} |
| **Backup** | ${BACKUP_STRATEGY} |
| **Runbook** | [docs/runbooks/deployment.md](projects/${PROJECT_NAME}/docs/runbooks/deployment.md) |
| **Owner** | ${OWNER} |
EOF
```

---

## Documentation Review

### Check for Outdated Documentation

```bash
# Find documentation older than 90 days
find "${PROJECT_DIR}/docs" -name "*.md" -mtime +90 -exec ls -lh {} \;

# Check if code changed but docs didn't
git log --since="90 days ago" --name-only --pretty=format: "${PROJECT_DIR}" | \
  grep -E "\.(py|js|ts|go|rs)$" && \
  echo "⚠️ Code changed but documentation may be outdated"
```

### Validate Links

```bash
# Check for broken internal links
find "${PROJECT_DIR}/docs" -name "*.md" -exec grep -oP '\[.*?\]\(.*?\)' {} \; | \
  while read link; do
    # Extract path
    path=$(echo "$link" | grep -oP '\(.*?\)' | tr -d '()')
    if [[ "$path" == http* ]]; then
      continue  # Skip external links
    fi
    if [ ! -f "${PROJECT_DIR}/${path}" ]; then
      echo "⚠️ Broken link: ${link}"
    fi
  done
```

---

## Generate API Documentation

### From Code Comments

```bash
# Example: Python docstring extraction
if [ -d "${PROJECT_DIR}/src" ]; then
  # Extract docstrings (requires tooling)
  # python -m pydoc [module] > docs/api.md
fi
```

### OpenAPI/Swagger

```bash
# Generate OpenAPI spec (if API exists)
# swagger-codegen generate -i api.yaml -o docs/api/
```

---

## Verify After

1. **Required files exist**: Check all required documentation files
2. **Sections complete**: Verify README has all sections
3. **Links valid**: Check for broken links
4. **Service catalog updated**: Verify entry in service inventory

---

## Rollback

Documentation changes are version-controlled. Rollback via git:

```bash
git checkout HEAD -- "${PROJECT_DIR}/docs/"
```

---

## Troubleshooting

### Documentation missing
- Use templates from this skill to generate missing docs
- Reference `infra-documentation` skill for architecture diagrams

### Outdated documentation
- Review git history to see when docs were last updated
- Update documentation to match current implementation

### Broken links
- Use link validation script above
- Update links to correct paths

---

## Related Skills

- **project-initiation** - Creates initial documentation structure
- **infra-documentation** - Architecture diagrams and ADRs
- **runbook-writer** - Operational runbooks
- **incident-report** - Post-incident documentation

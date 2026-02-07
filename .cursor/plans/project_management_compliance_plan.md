# Project Management & Compliance Plan

## Overview

Add project management and compliance capabilities to ensure all new services, features, and initiatives follow standardized processes for:
- Project folder structure
- Git repository setup and maintenance
- Documentation requirements
- Testing requirements
- Compliance validation (SMB1001, security, operational)
- Visual planning and tracking (Kanban boards)

## Proposed Domain: `governance`

New domain for project management, compliance, and governance skills.

## Skills to Add

### 1. `project-initiation` (Core)
**Purpose**: Initialize a new project with proper structure, compliance checks, and setup.

**Capabilities**:
- Project folder structure creation
- Git repository initialization (or linking to existing)
- Compliance checklist generation
- Project metadata capture (owner, purpose, scope, dependencies)
- Integration with project tracking tools (GitHub Projects, Linear, etc.)

**Trigger phrases**: "new project", "initiate project", "start new service", "new feature", "project setup", "initialize project"

**Compliance checks**:
- Security review required?
- SMB1001 controls affected?
- Infrastructure changes?
- Documentation plan?
- Testing plan?
- Rollback plan?

### 2. `project-compliance` (Compliance)
**Purpose**: Validate projects against compliance requirements (SMB1001, security, operational standards).

**Capabilities**:
- Compliance checklist validation
- SMB1001 control mapping
- Security review requirements
- Documentation completeness check
- Testing coverage validation
- Evidence collection for audits

**Trigger phrases**: "compliance check", "validate compliance", "compliance audit", "check project compliance", "SMB1001 check"

**Integration with**:
- `smb1001-security-ops` skill
- `patch-compliance` skill
- `hardening-audit` skill

### 3. `project-tracking` (Planning)
**Purpose**: Manage project tracking, Kanban boards, and visual planning tools.

**Capabilities**:
- GitHub Projects board creation/management
- Linear/Jira integration (if used)
- Issue/PR linking to projects
- Status tracking (Backlog, In Progress, Review, Done)
- Milestone management
- Dependency tracking

**Trigger phrases**: "create kanban board", "project board", "track project", "project status", "update project board", "visual planning"

**Tools integration**:
- GitHub Projects API
- GitHub Issues API
- Linear API (if applicable)
- Jira API (if applicable)

### 4. `project-documentation` (Documentation)
**Purpose**: Ensure project documentation follows standards and is complete.

**Capabilities**:
- README.md template generation
- Architecture Decision Records (ADRs)
- Runbook generation
- API documentation requirements
- Change log maintenance
- Service catalog updates

**Trigger phrases**: "project documentation", "update project docs", "documentation checklist", "ADR", "project README"

**Integration with**:
- `runbook-writer` skill
- `infra-documentation` skill

### 5. `project-testing` (Quality)
**Purpose**: Ensure testing requirements are met and validated.

**Capabilities**:
- Testing checklist generation
- Test coverage requirements
- CI/CD integration validation
- Test environment setup
- Test data management
- Test reporting

**Trigger phrases**: "testing requirements", "test plan", "test coverage", "test validation", "testing checklist"

**Integration with**:
- `github-actions` skill
- `container-ops` skill

## Tool Integrations to Add

### 1. GitHub Projects
**File**: `tools/integrations/github-projects.md`

**Capabilities**:
- REST API for project boards
- GraphQL API for advanced queries
- Issue/PR linking
- Field management (custom fields, status fields)
- Automation via GitHub Actions

**Use cases**:
- Create project board for new initiative
- Link issues/PRs to project
- Update project status
- Track milestones

### 2. Linear (Optional)
**File**: `tools/integrations/linear.md`

**Capabilities**:
- GraphQL API
- Issue creation/updates
- Project management
- Cycle planning
- Team management

**Use cases**:
- If Linear is preferred over GitHub Projects
- Advanced project planning
- Sprint/cycle management

### 3. GitHub Issues (Enhancement)
**File**: `tools/integrations/github.md` (update existing)

**Additional capabilities**:
- Issue templates for project initiation
- Issue linking and dependencies
- Labels and milestones
- Project assignment

## Project Folder Structure Template

```
projects/{project-name}/
├── README.md              # Project overview, setup, usage
├── CHANGELOG.md           # Version history
├── docs/
│   ├── architecture.md    # System architecture
│   ├── adr/               # Architecture Decision Records
│   │   └── 0001-*.md
│   └── runbooks/          # Operational runbooks
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/
│   ├── deploy.sh
│   └── rollback.sh
├── .github/
│   ├── workflows/
│   └── ISSUE_TEMPLATE/
├── compliance/
│   ├── checklist.md       # Compliance checklist
│   ├── smb1001-mapping.md # SMB1001 controls affected
│   └── evidence/          # Audit evidence
└── .project-metadata.yml  # Project metadata (owner, scope, deps)
```

## Compliance Checklist Template

```markdown
# Project Compliance Checklist

## Pre-Initiation
- [ ] Project scope defined
- [ ] Owner assigned
- [ ] Dependencies identified
- [ ] Security review scheduled (if required)

## Infrastructure
- [ ] Infrastructure changes documented
- [ ] Network requirements defined
- [ ] Storage requirements defined
- [ ] Backup strategy defined
- [ ] Monitoring/alerting configured

## Security
- [ ] Security review completed
- [ ] SMB1001 controls mapped
- [ ] Hardening checklist completed
- [ ] Vulnerability scanning scheduled
- [ ] Access controls defined

## Documentation
- [ ] README.md complete
- [ ] Architecture documented
- [ ] ADRs created (if applicable)
- [ ] Runbooks created
- [ ] API docs created (if applicable)
- [ ] Service catalog updated

## Testing
- [ ] Test plan created
- [ ] Unit tests written
- [ ] Integration tests written
- [ ] E2E tests written (if applicable)
- [ ] CI/CD pipeline configured
- [ ] Test coverage meets threshold

## Operations
- [ ] Deployment process documented
- [ ] Rollback procedure documented
- [ ] Monitoring configured
- [ ] Alerting configured
- [ ] Backup/restore tested

## Compliance
- [ ] SMB1001 evidence collected
- [ ] Audit trail configured
- [ ] Compliance report generated
```

## Workflow Integration

### New Project Flow

1. **Initiation** (`project-initiation` skill)
   - Engineer requests: "I want to deploy a new service X"
   - Agent creates project folder structure
   - Generates compliance checklist
   - Creates GitHub Project board
   - Initializes Git repo (or links existing)

2. **Planning** (`project-tracking` skill)
   - Creates issues for major tasks
   - Links to project board
   - Sets up milestones
   - Defines dependencies

3. **Development**
   - Engineer works on feature
   - Agent validates compliance at checkpoints
   - Documentation updated incrementally

4. **Compliance Validation** (`project-compliance` skill)
   - Before merge: validates checklist completion
   - Collects SMB1001 evidence
   - Generates compliance report

5. **Documentation** (`project-documentation` skill)
   - Ensures all docs are complete
   - Updates service catalog
   - Creates/updates runbooks

6. **Testing** (`project-testing` skill)
   - Validates test coverage
   - Ensures CI/CD is configured
   - Runs test suite

7. **Deployment**
   - Follows existing deployment skills
   - Updates context files
   - Closes project board

## Context File Updates

### New Context File: `context/projects-registry.md`

```markdown
# Projects Registry

Active and completed projects with metadata, compliance status, and links.

| Project | Owner | Status | Repo | Board | Compliance | Last Updated |
|---------|-------|--------|------|-------|-------------|--------------|
| service-x | @user | Active | github.com/... | #123 | Compliant | 2026-02-07 |
```

## Kanban Board Structure

### Default Columns
- **Backlog**: Ideas, not yet started
- **Planning**: Requirements gathering, design
- **In Progress**: Active development
- **Review**: Code review, compliance check
- **Testing**: QA, test validation
- **Done**: Deployed, documented, closed

### Custom Fields
- **Compliance Status**: Not Started / In Progress / Compliant / Blocked
- **SMB1001 Controls**: List of affected controls
- **Owner**: Project owner
- **Priority**: Low / Medium / High / Critical
- **Dependencies**: Links to other projects/issues

## GitHub Actions Learning Opportunity

Since the user wants to learn about GitHub Actions, the `project-initiation` skill will:

1. **Create a basic GitHub Actions workflow** for common CI/CD tasks:
   - Linting/formatting checks
   - Test execution
   - Build validation
   - (Optional) Deployment steps

2. **Include comments explaining**:
   - What each workflow step does
   - How to customize it
   - Common patterns and examples
   - Links to GitHub Actions documentation

3. **Provide examples** of:
   - PR checks (lint, test)
   - Release workflows
   - Scheduled tasks (cron)
   - Matrix builds (multiple versions)

This serves as both automation and a learning resource.

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Create `governance` domain
- [ ] Add `project-initiation` skill (with interview pattern)
- [ ] Add GitHub Projects integration guide
- [ ] Create project folder template
- [ ] Create compliance checklist template
- [ ] Add basic GitHub Actions workflow template (with learning comments)

### Phase 2: Compliance (Week 2)
- [ ] Add `project-compliance` skill
- [ ] Integrate with SMB1001 skills
- [ ] Create `context/projects-registry.md`
- [ ] Add soft-warning compliance checks (PR comments, reminders)

### Phase 3: Tracking (Week 3)
- [ ] Add `project-tracking` skill
- [ ] Enhance GitHub integration (Projects API)
- [ ] Create Kanban board templates
- [ ] Add project board automation examples

### Phase 4: Documentation & Testing (Week 4)
- [ ] Add `project-documentation` skill
- [ ] Add `project-testing` skill
- [ ] Integrate with existing doc/testing skills
- [ ] Create GitHub Actions examples for testing automation

## Decisions Made

1. **Project tracking tool**: ✅ GitHub Projects (native, free)
2. **Compliance enforcement**: ✅ Soft warnings (reminders, but allow merge)
3. **Automation level**: ✅ Manual skill invocation (with GitHub Actions learning opportunity)
4. **Project metadata**: ✅ Both (`.project-metadata.yml` in project + `context/projects-registry.md`)
5. **Integration scope**: ✅ New projects get full treatment (existing projects can be retrofitted manually)

## Engineer Interview Pattern

**Yes, the agent will interview the engineer before setting up the project structure.**

### Interview Flow

When `project-initiation` skill is triggered, the agent will:

1. **Gather Core Information** (required):
   - Project name (slug-friendly)
   - Project owner (GitHub username or name)
   - Project type (service, feature, infrastructure, documentation, research)
   - Brief description/purpose

2. **Gather Scope Information** (required):
   - What will this project do?
   - What problem does it solve?
   - Is this a new service, feature addition, or infrastructure change?

3. **Gather Technical Information** (context-dependent):
   - Infrastructure requirements? (new VM/CT, Docker container, cloud service)
   - Network requirements? (ports, DNS, reverse proxy)
   - Storage requirements? (databases, file storage)
   - Dependencies on other services/projects?

4. **Gather Compliance Information** (context-dependent):
   - Does this touch production infrastructure?
   - Does this handle sensitive data?
   - Does this expose external endpoints?
   - Any SMB1001 controls likely affected?

5. **Gather Repository Information**:
   - New repository or existing?
   - If existing, repository URL
   - Preferred repository location (organization, personal)

### Interview Style

The agent will:
- Ask questions conversationally (not a rigid form)
- Infer information from context when possible
- Use follow-up questions to clarify ambiguous answers
- Show a summary before proceeding: "Here's what I understand. Should I proceed?"

### Example Interaction

```
User: "I want to start a new project for a monitoring dashboard"

Agent: "Great! Let me gather some information to set this up properly.

1. What should we call this project? (I'll use this for the folder name and repo)
2. Who's the project owner? (GitHub username or name)
3. What type of project is this? (service, feature, infrastructure, etc.)
4. Brief description: What will this monitoring dashboard do?

[User answers]

Agent: "Thanks! A few more questions:

5. Will this be a new Docker service, or integrate with existing monitoring?
6. Does it need a database or persistent storage?
7. Will it be exposed via the reverse proxy (needs DNS/SSL)?
8. Any dependencies on other services?

[User answers]

Agent: "Perfect! Here's what I'll set up:
- Project: monitoring-dashboard
- Owner: @username
- Type: service
- Infrastructure: Docker container, needs reverse proxy, no database
- Repository: New repo at github.com/dpgetmassive/monitoring-dashboard

Should I proceed with creating the project structure?"
```

## Success Metrics

- All new projects have standardized structure
- Compliance checklists completed before deployment
- Documentation coverage > 90%
- Test coverage > 80%
- Project boards track all active initiatives
- SMB1001 evidence collected automatically
- Zero compliance violations in audits

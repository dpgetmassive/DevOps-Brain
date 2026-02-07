---
name: project-initiation
version: 1.0.0
description: When the user wants to start a new project, deploy a new service, or initiate a feature request. Also use when the user mentions "new project," "initiate project," "start new service," "new feature," "project setup," or "initialize project." This skill gathers project requirements through an interview, creates standardized folder structure, sets up Git repository, generates compliance checklist, and creates GitHub Project board.
---

# Project Initiation

You are an expert in project initiation and setup. You guide engineers through a structured interview to gather requirements, then create a complete project structure with compliance checklists, documentation templates, and GitHub integration.

## Guard Rails

**Auto-approve**: Creating project folders, generating templates, creating GitHub Projects boards, generating checklists
**Confirm first**: Creating new GitHub repositories, modifying existing repositories, deleting project folders

---

## Prerequisites

**Read `context/infrastructure-context.md` first** to understand the environment.

**Required tools**:
- `gh` CLI (GitHub CLI) authenticated
- `git` CLI
- Access to create GitHub Projects and repositories

---

## Engineer Interview Pattern

**Before creating any project structure, conduct a structured interview to gather requirements.**

### Step 1: Core Information (Required)

Ask these questions conversationally:

1. **Project name**: "What should we call this project? (I'll use this for the folder name and repository)"
   - Validate: lowercase, hyphens only, no spaces
   - Example: "monitoring-dashboard", "api-gateway", "user-auth-service"

2. **Project owner**: "Who's the project owner? (GitHub username or name)"
   - Use GitHub username if available (for @mentions)

3. **Project type**: "What type of project is this?"
   - Options: `service`, `feature`, `infrastructure`, `documentation`, `research`, `tool`
   - This determines which templates to use

4. **Brief description**: "What will this project do? (One sentence)"
   - Used for README and project board description

### Step 2: Scope Information (Required)

5. **Purpose**: "What problem does this solve?"
   - Helps determine scope and dependencies

6. **Scope boundaries**: "What's in scope vs out of scope?"
   - Helps set expectations and avoid scope creep

### Step 3: Technical Information (Context-Dependent)

Ask based on project type:

**For services/infrastructure**:
7. **Infrastructure requirements**: "Will this be a new VM/CT, Docker container, or cloud service?"
8. **Network requirements**: "Does it need ports, DNS records, or reverse proxy setup?"
9. **Storage requirements**: "Does it need databases, file storage, or persistent volumes?"
10. **Dependencies**: "Does it depend on other services or projects?"

**For features**:
7. **Parent project**: "Which existing project/service does this extend?"
8. **Breaking changes**: "Does this introduce breaking changes?"
9. **Migration needed**: "Does this require data migration?"

### Step 4: Compliance Information (Context-Dependent)

11. **Production impact**: "Does this touch production infrastructure?"
12. **Sensitive data**: "Does this handle sensitive data (PII, credentials, etc.)?"
13. **External exposure**: "Does this expose external endpoints?"
14. **SMB1001 controls**: "Any SMB1001 controls likely affected?" (Use `smb1001-security-ops` skill for reference)

### Step 5: Repository Information

15. **Repository**: "New repository or existing?"
   - If new: "Where should it be created? (organization or personal account)"
   - If existing: "What's the repository URL?"

### Step 6: Confirmation

**Before proceeding, show a summary**:

```
Here's what I understand:
- Project: [name]
- Owner: [owner]
- Type: [type]
- Description: [description]
- Infrastructure: [requirements]
- Repository: [new/existing] at [location]
- Compliance: [notes]

Should I proceed with creating the project structure?
```

**Wait for user confirmation before creating anything.**

---

## Project Structure Creation

### Standard Project Structure

```
projects/{project-name}/
├── README.md                    # Project overview, setup, usage
├── CHANGELOG.md                 # Version history (keepachangelog.com format)
├── .project-metadata.yml        # Project metadata (owner, scope, deps)
├── docs/
│   ├── architecture.md          # System architecture
│   ├── adr/                     # Architecture Decision Records
│   │   └── 0001-template.md
│   └── runbooks/                # Operational runbooks
│       └── deployment.md
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/
│   ├── deploy.sh
│   └── rollback.sh
├── .github/
│   ├── workflows/
│   │   └── ci.yml               # CI workflow (with learning comments)
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       └── feature_request.md
├── compliance/
│   ├── checklist.md             # Compliance checklist
│   ├── smb1001-mapping.md       # SMB1001 controls affected
│   └── evidence/                # Audit evidence (empty initially)
└── .gitignore                   # Language/framework specific
```

### Create Project Structure

```bash
# Set variables from interview
PROJECT_NAME="monitoring-dashboard"
PROJECT_DIR="projects/${PROJECT_NAME}"

# Create directory structure
mkdir -p "${PROJECT_DIR}"/{docs/{adr,runbooks},tests/{unit,integration,e2e},scripts,compliance/evidence,.github/{workflows,ISSUE_TEMPLATE}}

# Create base files (templates below)
```

---

## Template Files

### README.md Template

```markdown
# {Project Name}

{One sentence description}

## Overview

{Detailed description from interview}

## Quick Start

{Setup instructions}

## Architecture

See [docs/architecture.md](docs/architecture.md)

## Development

{Development setup, dependencies, local testing}

## Deployment

See [docs/runbooks/deployment.md](docs/runbooks/deployment.md)

## Testing

{Testing instructions}

## Compliance

See [compliance/checklist.md](compliance/checklist.md)

## Contributing

{Contributing guidelines}

## License

{License}
```

### .project-metadata.yml Template

```yaml
project:
  name: {project-name}
  owner: {owner}
  type: {type}
  description: {description}
  created: {date}
  status: planning

repository:
  url: {repo-url}
  default_branch: main

infrastructure:
  requirements: {requirements}
  network: {network-notes}
  storage: {storage-notes}
  dependencies: {dependencies}

compliance:
  production_impact: {yes/no}
  sensitive_data: {yes/no}
  external_exposure: {yes/no}
  smb1001_controls: {list}
```

### compliance/checklist.md Template

```markdown
# Project Compliance Checklist

## Pre-Initiation ✅
- [x] Project scope defined
- [x] Owner assigned
- [x] Dependencies identified
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

### .github/workflows/ci.yml Template (with learning comments)

```yaml
name: CI

# This workflow runs on every push and pull request
# Learn more: https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

# Jobs run in parallel by default. Use 'needs' to create dependencies.
jobs:
  lint:
    # Run on Ubuntu (other options: windows-latest, macos-latest)
    runs-on: ubuntu-latest
    
    steps:
    # Checkout code (required for any job that needs the code)
    - uses: actions/checkout@v4
    
    # Setup Node.js (example - adjust for your language)
    # - uses: actions/setup-node@v4
    #   with:
    #     node-version: '20'
    
    # Run linter (customize for your project)
    # - name: Run linter
    #   run: npm run lint
    
    # Example: Python linting
    # - name: Run flake8
    #   run: |
    #     pip install flake8
    #     flake8 .

  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    # Setup dependencies (customize for your project)
    # - name: Install dependencies
    #   run: npm install  # or: pip install -r requirements.txt
    
    # Run tests
    # - name: Run tests
    #   run: npm test  # or: pytest
    
    # Example: Python testing with coverage
    # - name: Run tests with coverage
    #   run: |
    #     pip install pytest pytest-cov
    #     pytest --cov=. --cov-report=xml
    
    # Upload coverage (optional)
    # - name: Upload coverage
    #   uses: codecov/codecov-action@v3
    #   with:
    #     file: ./coverage.xml

  build:
    runs-on: ubuntu-latest
    # Only run if lint and test pass
    needs: [lint, test]
    
    steps:
    - uses: actions/checkout@v4
    
    # Build step (customize for your project)
    # - name: Build
    #   run: npm run build  # or: docker build -t app .
    
    # Example: Docker build
    # - name: Build Docker image
    #   run: docker build -t myapp:${{ github.sha }} .
    
    # Example: Upload artifact
    # - name: Upload artifact
    #   uses: actions/upload-artifact@v3
    #   with:
    #     name: dist
    #     path: dist/

# Learn more:
# - Workflow syntax: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions
# - Actions marketplace: https://github.com/marketplace?type=actions
# - Matrix builds: https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs
# - Scheduled workflows: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule
```

---

## Git Repository Setup

### New Repository

```bash
# Initialize git
cd "${PROJECT_DIR}"
git init
git branch -M main

# Create initial commit
git add .
git commit -m "chore: initial project setup"

# Create repository on GitHub
gh repo create dpgetmassive/${PROJECT_NAME} --public --source . --remote origin --push

# Or for organization:
# gh repo create cyberpeople-au/${PROJECT_NAME} --public --source . --remote origin --push
```

### Existing Repository

```bash
cd "${PROJECT_DIR}"
git remote add origin {repository-url}
git fetch origin
git branch --set-upstream-to=origin/main main  # or appropriate branch
```

---

## GitHub Project Board Creation

```bash
# Create GitHub Project board
PROJECT_BOARD_ID=$(gh api repos/dpgetmassive/${PROJECT_NAME}/projects \
  --method POST \
  --field name="${PROJECT_NAME}" \
  --field body="Project board for ${PROJECT_NAME}" \
  --jq '.id')

# Create columns (Backlog, In Progress, Review, Testing, Done)
gh api "projects/${PROJECT_BOARD_ID}/columns" --method POST --field name="Backlog"
gh api "projects/${PROJECT_BOARD_ID}/columns" --method POST --field name="In Progress"
gh api "projects/${PROJECT_BOARD_ID}/columns" --field name="Review"
gh api "projects/${PROJECT_BOARD_ID}/columns" --field name="Testing"
gh api "projects/${PROJECT_BOARD_ID}/columns" --field name="Done"

# Link repository to project
gh api "projects/${PROJECT_BOARD_ID}/repos/dpgetmassive/${PROJECT_NAME}" --method PUT
```

**Note**: GitHub Projects v2 uses GraphQL. See `tools/integrations/github-projects.md` for detailed API usage.

---

## Update Projects Registry

After creating the project, update `context/projects-registry.md`:

```bash
# Append to projects registry
cat >> context/projects-registry.md << EOF

| ${PROJECT_NAME} | ${OWNER} | Planning | ${REPO_URL} | ${PROJECT_BOARD_URL} | In Progress | $(date +%Y-%m-%d) |
EOF
```

---

## Verify After

1. **Project structure exists**: `ls -la projects/${PROJECT_NAME}`
2. **Git repository initialized**: `cd projects/${PROJECT_NAME} && git status`
3. **GitHub repository created**: `gh repo view dpgetmassive/${PROJECT_NAME}`
4. **Project board created**: Check GitHub Projects UI
5. **Templates populated**: Verify key files exist and have content

---

## Rollback

If project creation fails partway through:

```bash
# Remove project directory
rm -rf projects/${PROJECT_NAME}

# Delete GitHub repository (if created)
gh repo delete dpgetmassive/${PROJECT_NAME} --yes

# Delete project board (if created)
# Get board ID first, then:
gh api "projects/${BOARD_ID}" --method DELETE
```

---

## Troubleshooting

### GitHub CLI not authenticated
```bash
gh auth login
```

### Project board creation fails
- Check GitHub Projects API permissions
- Use GraphQL API for Projects v2 (see `tools/integrations/github-projects.md`)

### Repository already exists
- Ask user: "Repository already exists. Link to existing or create new?"
- If link: `git remote add origin {url}` and pull existing structure

---

## Related Skills

- **project-compliance** - Validate compliance checklist
- **project-tracking** - Manage project board and issues
- **project-documentation** - Ensure documentation completeness
- **project-testing** - Validate testing requirements
- **git-workflow** - Branching strategy and PR conventions
- **github-actions** - CI/CD pipeline setup
- **smb1001-security-ops** - SMB1001 control mapping

---
name: project-tracking
version: 1.0.0
description: When the user wants to manage project tracking, create or update Kanban boards, link issues to projects, track project status, or manage milestones. Also use when the user mentions "create kanban board," "project board," "track project," "project status," "update project board," "visual planning," or "project tracking."
---

# Project Tracking

You are an expert in project tracking and Kanban board management using GitHub Projects. You create boards, manage columns, link issues, and track project status.

## Guard Rails

**Auto-approve**: Viewing project boards, listing issues, reading project status
**Confirm first**: Creating project boards, deleting columns, bulk operations

---

## Prerequisites

**Read `context/infrastructure-context.md` first** to understand the environment.

**Read `context/projects-registry.md`** to see active projects.

**Required tools**:
- `gh` CLI authenticated
- GitHub Projects API access

**Reference**: `tools/integrations/github-projects.md` for API details.

---

## Create Project Board

### For New Project

```bash
PROJECT_NAME="monitoring-dashboard"
REPO_OWNER="dpgetmassive"
REPO_NAME="${PROJECT_NAME}"

# Get owner ID
OWNER_ID=$(gh api graphql -f query='query { viewer { id } }' --jq '.data.viewer.id')

# Get repository ID
REPO_ID=$(gh api graphql -f query="query { repository(owner: \"${REPO_OWNER}\", name: \"${REPO_NAME}\") { id } }" --jq '.data.repository.id')

# Create project (Projects v2)
PROJECT=$(gh api graphql -f query="
mutation {
  createProjectV2(input: {
    ownerId: \"${OWNER_ID}\"
    title: \"${PROJECT_NAME}\"
  }) {
    projectV2 {
      id
      title
      url
      number
    }
  }
}")

PROJECT_ID=$(echo $PROJECT | jq -r '.data.createProjectV2.projectV2.id')
PROJECT_URL=$(echo $PROJECT | jq -r '.data.createProjectV2.projectV2.url')
PROJECT_NUMBER=$(echo $PROJECT | jq -r '.data.createProjectV2.projectV2.number')

# Link repository
gh api graphql -f query="
mutation {
  linkProjectV2ToRepository(input: {
    projectId: \"${PROJECT_ID}\"
    repositoryId: \"${REPO_ID}\"
  }) {
    projectV2 { id }
  }
}"

echo "Project board created: ${PROJECT_URL}"
```

### Create Default Columns

```bash
# Default columns for project workflow
COLUMNS=("Backlog" "Planning" "In Progress" "Review" "Testing" "Done")

for COLUMN in "${COLUMNS[@]}"; do
  gh api graphql -f query="
  mutation {
    addProjectV2Column(input: {
      projectId: \"${PROJECT_ID}\"
      name: \"${COLUMN}\"
    }) {
      projectColumn {
        id
        name
      }
    }
  }"
done
```

---

## Link Issue to Project

### Add Issue to Project Board

```bash
ISSUE_NUMBER=1
REPO_OWNER="dpgetmassive"
REPO_NAME="monitoring-dashboard"

# Get issue node ID
ISSUE_ID=$(gh api graphql -f query="
query {
  repository(owner: \"${REPO_OWNER}\", name: \"${REPO_NAME}\") {
    issue(number: ${ISSUE_NUMBER}) {
      id
      title
    }
  }
}" --jq '.data.repository.issue.id')

# Add to project
gh api graphql -f query="
mutation {
  addProjectV2ItemById(input: {
    projectId: \"${PROJECT_ID}\"
    contentId: \"${ISSUE_ID}\"
  }) {
    item {
      id
    }
  }
}"
```

### Move Issue to Column

```bash
# Get project field ID (status field)
STATUS_FIELD_ID=$(gh api graphql -f query="
query {
  node(id: \"${PROJECT_ID}\") {
    ... on ProjectV2 {
      field(name: \"Status\") {
        ... on ProjectV2SingleSelectField {
          id
          options {
            id
            name
          }
        }
      }
    }
  }
}" --jq '.data.node.field.id')

# Get option ID for target column
TARGET_OPTION_ID=$(gh api graphql -f query="
query {
  node(id: \"${PROJECT_ID}\") {
    ... on ProjectV2 {
      field(name: \"Status\") {
        ... on ProjectV2SingleSelectField {
          options {
            id
            name
          }
        }
      }
    }
  }
}" --jq '.data.node.field.options[] | select(.name == "In Progress") | .id')

# Update item field
gh api graphql -f query="
mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: \"${PROJECT_ID}\"
    itemId: \"${ITEM_ID}\"
    fieldId: \"${STATUS_FIELD_ID}\"
    value: { singleSelectOptionId: \"${TARGET_OPTION_ID}\" }
  }) {
    projectV2Item {
      id
    }
  }
}"
```

---

## List Project Items

### View All Items

```bash
gh api graphql -f query="
query {
  node(id: \"${PROJECT_ID}\") {
    ... on ProjectV2 {
      title
      items(first: 20) {
        nodes {
          id
          content {
            ... on Issue {
              title
              number
              url
              state
            }
            ... on PullRequest {
              title
              number
              url
              state
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
              }
            }
          }
        }
      }
    }
  }
}" | jq '.data.node.items.nodes[] | {title: .content.title, status: .fieldValues.nodes[0].name}'
```

### Filter by Status

```bash
# List items in "In Progress" column
gh api graphql -f query="
query {
  node(id: \"${PROJECT_ID}\") {
    ... on ProjectV2 {
      items(first: 20) {
        nodes {
          content {
            ... on Issue {
              title
              number
            }
          }
          fieldValues(first: 10) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
              }
            }
          }
        }
      }
    }
  }
}" | jq '.data.node.items.nodes[] | select(.fieldValues.nodes[0].name == "In Progress")'
```

---

## Create Project Issues

### Create Issue from Template

```bash
# Create issue using template
gh issue create \
  --title "Setup monitoring dashboard" \
  --body-file .github/ISSUE_TEMPLATE/feature_request.md \
  --label "enhancement" \
  --project "${PROJECT_NUMBER}"
```

### Create Issue with Checklist

```bash
cat > /tmp/issue-body.md << EOF
## Description
Setup monitoring dashboard for service health tracking.

## Tasks
- [ ] Design dashboard layout
- [ ] Implement data collection
- [ ] Create visualization components
- [ ] Add alerting rules
- [ ] Write documentation

## Acceptance Criteria
- Dashboard displays service metrics
- Alerts trigger on threshold breaches
- Documentation is complete
EOF

gh issue create \
  --title "Setup monitoring dashboard" \
  --body-file /tmp/issue-body.md \
  --project "${PROJECT_NUMBER}"
```

---

## Update Project Status

### Update Project Metadata

```bash
PROJECT_DIR="projects/${PROJECT_NAME}"

# Update status in metadata
yq eval '.project.status = "In Progress"' -i "${PROJECT_DIR}/.project-metadata.yml"

# Update projects registry
sed -i "s/| ${PROJECT_NAME} |.*| Planning |/| ${PROJECT_NAME} | ${OWNER} | In Progress |/" context/projects-registry.md
```

### Update Compliance Status on Board

```bash
# Create or update compliance status field
# (Requires custom field setup - see GitHub Projects v2 custom fields)

# Get compliance field ID
COMPLIANCE_FIELD_ID=$(gh api graphql -f query="
query {
  node(id: \"${PROJECT_ID}\") {
    ... on ProjectV2 {
      fields(first: 20) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
          }
        }
      }
    }
  }
}" --jq '.data.node.fields.nodes[] | select(.name == "Compliance Status") | .id')

# Update item compliance status
gh api graphql -f query="
mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: \"${PROJECT_ID}\"
    itemId: \"${ITEM_ID}\"
    fieldId: \"${COMPLIANCE_FIELD_ID}\"
    value: { singleSelectOptionId: \"COMPLIANT_OPTION_ID\" }
  }) {
    projectV2Item {
      id
    }
  }
}"
```

---

## Milestone Management

### Create Milestone

```bash
gh api repos/${REPO_OWNER}/${REPO_NAME}/milestones \
  --method POST \
  --field title="v1.0.0 - Initial Release" \
  --field description="First production release" \
  --field due_on="2026-03-01T00:00:00Z"
```

### Link Issues to Milestone

```bash
MILESTONE_NUMBER=1

gh issue edit ${ISSUE_NUMBER} \
  --milestone ${MILESTONE_NUMBER} \
  --repo ${REPO_OWNER}/${REPO_NAME}
```

### View Milestone Progress

```bash
gh api repos/${REPO_OWNER}/${REPO_NAME}/milestones/${MILESTONE_NUMBER} \
  --jq '{title: .title, open_issues: .open_issues, closed_issues: .closed_issues, progress: (.closed_issues / (.open_issues + .closed_issues) * 100)}'
```

---

## Project Board Templates

### Standard Workflow Board

Columns: Backlog → Planning → In Progress → Review → Testing → Done

### Compliance-Focused Board

Columns: Backlog → Planning → In Progress → Compliance Check → Review → Testing → Done

### Feature Development Board

Columns: Backlog → Design → Development → Code Review → QA → Done

---

## Verify After

1. **Project board exists**: Check GitHub Projects UI
2. **Columns created**: Verify all default columns exist
3. **Issues linked**: Confirm issues appear on board
4. **Status updated**: Verify project status in registry

---

## Rollback

### Delete Project Board

```bash
# Delete project (use with caution)
gh api graphql -f query="
mutation {
  deleteProjectV2(input: {
    projectId: \"${PROJECT_ID}\"
  }) {
    projectV2 {
      id
    }
  }
}"
```

### Remove Issue from Board

```bash
gh api graphql -f query="
mutation {
  deleteProjectV2Item(input: {
    projectId: \"${PROJECT_ID}\"
    itemId: \"${ITEM_ID}\"
  }) {
    deletedItemId
  }
}"
```

---

## Troubleshooting

### Project board not found
- Check if project was created via `project-initiation` skill
- Verify repository exists: `gh repo view ${REPO_OWNER}/${REPO_NAME}`

### Cannot add issue to board
- Verify issue exists: `gh issue view ${ISSUE_NUMBER}`
- Check project permissions
- Ensure repository is linked to project

### Column operations fail
- Projects v2 uses fields, not columns
- Use GraphQL API for field operations
- See `tools/integrations/github-projects.md` for details

---

## Related Skills

- **project-initiation** - Creates project board during setup
- **project-compliance** - Updates compliance status on board
- **git-workflow** - Links PRs to project board
- **github-actions** - Automates project board updates

# GitHub Projects

GitHub Projects provides Kanban-style project boards for tracking work, issues, and pull requests. Available via REST API (Projects v1) and GraphQL API (Projects v2).

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API (v1) and GraphQL API (v2) |
| MCP | N | Not available |
| CLI | Y | `gh` CLI supports Projects v2 |
| SDK | Y | GitHub SDKs support both APIs |

**Note**: GitHub Projects v2 (GraphQL) is the current version. Projects v1 (REST) is legacy but still functional.

## Authentication

### GitHub CLI (`gh`)

```bash
# Login (if not already)
gh auth login

# Check authentication
gh auth status
```

### REST API

```bash
# Using gh CLI token
export GITHUB_TOKEN=$(gh auth token)

# Or set personal access token
export GITHUB_TOKEN="ghp_..."
```

### GraphQL API

```bash
# Using gh CLI
gh api graphql -f query='{ viewer { login } }'

# Or with curl
curl -H "Authorization: bearer $GITHUB_TOKEN" \
  -H "Content-Type: application/json" \
  https://api.github.com/graphql \
  -d '{"query":"{ viewer { login } }"}'
```

## Common Agent Operations

### Create Project Board (GraphQL v2)

```bash
# Create project for repository
gh api graphql -f query='
mutation {
  createProjectV2(input: {
    ownerId: "OWNER_ID"
    title: "Project Name"
    repositoryId: "REPO_ID"
  }) {
    projectV2 {
      id
      title
      url
    }
  }
}'

# Get owner ID (user or org)
OWNER_ID=$(gh api graphql -f query='
query {
  viewer {
    id
  }
}' --jq '.data.viewer.id')

# Get repository ID
REPO_ID=$(gh api graphql -f query='
query {
  repository(owner: "dpgetmassive", name: "project-name") {
    id
  }
}' --jq '.data.repository.id')
```

### Create Project Board (REST v1 - Legacy)

```bash
# Create project for repository
gh api repos/dpgetmassive/project-name/projects \
  --method POST \
  --field name="Project Name" \
  --field body="Project description"

# Get project ID
PROJECT_ID=$(gh api repos/dpgetmassive/project-name/projects --jq '.[0].id')
```

### Create Columns

**Projects v2 (GraphQL)**:
```bash
# Get project ID first
PROJECT_ID="PVT_kwDO..."

# Create column
gh api graphql -f query='
mutation {
  addProjectV2Column(input: {
    projectId: "PROJECT_ID"
    name: "In Progress"
  }) {
    projectColumn {
      id
      name
    }
  }
}'
```

**Projects v1 (REST)**:
```bash
# Create column
gh api "projects/${PROJECT_ID}/columns" \
  --method POST \
  --field name="In Progress"
```

### Add Issue to Project

**Projects v2 (GraphQL)**:
```bash
# Get issue node ID
ISSUE_ID=$(gh api graphql -f query='
query {
  repository(owner: "dpgetmassive", name: "project-name") {
    issue(number: 1) {
      id
    }
  }
}' --jq '.data.repository.issue.id')

# Add to project
gh api graphql -f query='
mutation {
  addProjectV2ItemById(input: {
    projectId: "PROJECT_ID"
    contentId: "ISSUE_ID"
  }) {
    item {
      id
    }
  }
}'
```

**Projects v1 (REST)**:
```bash
# Get column ID
COLUMN_ID=$(gh api "projects/${PROJECT_ID}/columns" --jq '.[0].id')

# Add card (issue) to column
gh api "projects/columns/${COLUMN_ID}/cards" \
  --method POST \
  --field content_id="${ISSUE_ID}" \
  --field content_type="Issue"
```

### Move Item Between Columns

**Projects v2 (GraphQL)**:
```bash
# Get item ID and field ID (status field)
gh api graphql -f query='
mutation {
  updateProjectV2ItemFieldValue(input: {
    projectId: "PROJECT_ID"
    itemId: "ITEM_ID"
    fieldId: "STATUS_FIELD_ID"
    value: { singleSelectOptionId: "OPTION_ID" }
  }) {
    projectV2Item {
      id
    }
  }
}'
```

**Projects v1 (REST)**:
```bash
# Move card to different column
gh api "projects/columns/${NEW_COLUMN_ID}/moves" \
  --method POST \
  --field position="top" \
  --field column_id="${OLD_COLUMN_ID}"
```

### List Project Items

**Projects v2 (GraphQL)**:
```bash
gh api graphql -f query='
query {
  node(id: "PROJECT_ID") {
    ... on ProjectV2 {
      items(first: 20) {
        nodes {
          id
          content {
            ... on Issue {
              title
              number
              url
            }
            ... on PullRequest {
              title
              number
              url
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
}'
```

### Link Repository to Project

**Projects v2**:
```bash
# Add repository to project
gh api graphql -f query='
mutation {
  linkProjectV2ToRepository(input: {
    projectId: "PROJECT_ID"
    repositoryId: "REPO_ID"
  }) {
    projectV2 {
      id
    }
  }
}'
```

**Projects v1**:
```bash
# Link repository (already done when creating repo project)
gh api "projects/${PROJECT_ID}/repos/dpgetmassive/project-name" --method PUT
```

## Default Project Structure

### Recommended Columns

| Column | Purpose | Order |
|--------|---------|-------|
| Backlog | Ideas, not yet started | 1 |
| Planning | Requirements, design | 2 |
| In Progress | Active development | 3 |
| Review | Code review, compliance check | 4 |
| Testing | QA, test validation | 5 |
| Done | Deployed, documented | 6 |

### Custom Fields (Projects v2)

- **Compliance Status**: Single select (Not Started / In Progress / Compliant / Blocked)
- **SMB1001 Controls**: Text field (list affected controls)
- **Owner**: User field (project owner)
- **Priority**: Single select (Low / Medium / High / Critical)
- **Dependencies**: Text field (links to other projects/issues)

## When to Use

- **Project tracking**: Track initiatives, features, services
- **Issue organization**: Group related issues by project
- **Compliance tracking**: Track compliance checklist items
- **Milestone planning**: Visualize project phases
- **Team coordination**: Shared view of work status

## Rate Limits

- **REST API**: 5,000 requests/hour (authenticated)
- **GraphQL API**: 5,000 points/hour (authenticated)
- **GraphQL cost**: Queries cost points based on complexity (1 point per node)

## Relevant Skills

- **project-initiation** - Creates project board during setup
- **project-tracking** - Manages project board and items
- **project-compliance** - Tracks compliance status on board

## Examples

### Complete Project Setup Script

```bash
#!/bin/bash
# Create project board with default columns

PROJECT_NAME="monitoring-dashboard"
REPO_OWNER="dpgetmassive"
REPO_NAME="${PROJECT_NAME}"

# Get IDs
OWNER_ID=$(gh api graphql -f query="query { viewer { id } }" --jq '.data.viewer.id')
REPO_ID=$(gh api graphql -f query="query { repository(owner: \"${REPO_OWNER}\", name: \"${REPO_NAME}\") { id } }" --jq ".data.repository.id")

# Create project
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
    }
  }
}")

PROJECT_ID=$(echo $PROJECT | jq -r '.data.createProjectV2.projectV2.id')
PROJECT_URL=$(echo $PROJECT | jq -r '.data.createProjectV2.projectV2.url')

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

echo "Project created: ${PROJECT_URL}"
```

## References

- [GitHub Projects v2 API](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-your-projects)
- [GitHub Projects REST API](https://docs.github.com/en/rest/projects/projects)
- [GitHub CLI Projects](https://cli.github.com/manual/gh_project)

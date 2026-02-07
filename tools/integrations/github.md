# GitHub CLI and API

GitHub provides source control, CI/CD, and project management via GitHub CLI (`gh`) and REST API (`api.github.com`). Used for repository management, GitHub Actions workflows, PRs, issues, and releases.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `https://api.github.com`, GraphQL API available |
| MCP | N | No MCP server available |
| CLI | Y | `gh` command-line tool for GitHub operations |
| SDK | Y | Octokit libraries (JavaScript, Python, Ruby, Go) |

## Authentication

**GitHub CLI**: Authenticate via `gh auth login`. Supports browser, token, or SSH key methods.

```bash
# Login interactively
gh auth login

# Login with token
gh auth login --with-token < token.txt

# Check auth status
gh auth status
```

**API Token**: Use `GITHUB_TOKEN` environment variable or `--token` flag. Personal access tokens or GitHub App tokens.

```bash
# Set token for API calls
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Use token in curl
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

**SSH Keys**: GitHub CLI can use SSH keys for Git operations. Keys configured in `~/.ssh/`.

## Common Agent Operations

### Repositories and PRs

```bash
# Clone repository
gh repo clone owner/repo-name

# List PRs
gh pr list

# Create PR
gh pr create --title "Feature: Add new feature" --body "Description"

# Merge PR
gh pr merge 123 --squash --delete-branch

# View issue
gh issue view 45

# Create issue
gh issue create --title "Bug: Description" --body "Details"
```

### GitHub Actions and API

```bash
# List workflow runs
gh run list

# View workflow logs
gh run view 1234567890 --log

# Rerun failed workflow
gh run rerun 1234567890

# Run workflow manually
gh workflow run workflow-name.yml
```

### Releases and API

```bash
# List workflow runs via API
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo/actions/runs

# Trigger workflow via API
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/owner/repo/actions/workflows/workflow.yml/dispatches \
  -d '{"ref":"main"}'

# Create release
gh release create v1.0.0 --title "Release v1.0.0" --notes "Release notes"
```

## Key Objects/Metrics

- **Repositories**: Source code repositories with branches, tags, releases
- **Pull Requests**: Code review and merge requests
- **Workflows**: GitHub Actions CI/CD pipelines
- **Runs**: Individual workflow execution instances
- **Releases**: Versioned releases with assets

## When to Use

- **CI/CD management**: Monitor workflow runs, trigger deployments, check build status
- **Code review**: Create PRs, review code, merge changes
- **Issue tracking**: Create issues, track bugs, manage project tasks
- **Release management**: Create releases, tag versions, publish artifacts

## Rate Limits

**Authenticated requests**: 5,000 requests/hour per token
**Unauthenticated requests**: 60 requests/hour per IP

Rate limit headers:
- `X-RateLimit-Limit`: Total requests allowed
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Unix timestamp when limit resets

```bash
# Check rate limit status
gh api rate_limit

# Via API
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit
```

## Relevant Skills

- `github-actions` - CI/CD workflow creation and management
- `git-workflow` - Branching strategy and PR conventions
- `container-ops` - Building images in CI/CD pipelines
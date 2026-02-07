---
name: git-workflow
version: 1.0.0
description: When the user wants to manage Git branching strategy, PR conventions, releases, or code review processes. Also use when the user mentions "branching," "PR," "pull request," "code review," "release," "tag," "merge strategy," or "git flow." For CI/CD pipelines, see github-actions.
---

# Git Workflow

You are an expert in Git workflow and version control conventions.

## Branching Strategy

### Branch Naming
| Branch Type | Pattern | Example |
|-------------|---------|---------|
| Main/Production | `main` | `main` |
| Development | `develop` | `develop` |
| Feature | `feature/<description>` | `feature/add-user-auth` |
| Fix | `fix/<description>` | `fix/login-redirect` |
| Hotfix | `hotfix/<description>` | `hotfix/critical-sql-fix` |
| Release | `release/<version>` | `release/1.2.0` |
| Documentation | `docs/<description>` | `docs/api-readme` |
| Infrastructure | `infra/<description>` | `infra/ci-pipeline` |

### Flow
```
feature/xyz ──> develop ──> release/1.x ──> main
                                              │
hotfix/critical ─────────────────────────────>│
```

## Guard Rails

**Auto-approve**: Branch creation, commits, viewing history
**Confirm first**: Force pushes, rebasing shared branches, deleting remote branches

---

## Common Operations

### Create Feature Branch
```bash
git checkout develop
git pull origin develop
git checkout -b feature/<description>
```

### Create PR
```bash
git push -u origin feature/<description>
gh pr create --title "Add feature" --body "## Summary\n- What changed\n\n## Test Plan\n- How to test"
```

### Merge PR
```bash
gh pr merge <number> --squash --delete-branch
```

---

## Commit Conventions

### Conventional Commits
```
<type>: <description>

[optional body]
```

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `refactor` | Code change that neither fixes nor adds |
| `test` | Adding or correcting tests |
| `chore` | Maintenance tasks |
| `ci` | CI/CD changes |
| `infra` | Infrastructure changes |

### Examples
```
feat: add user authentication flow
fix: correct redirect URL after login
docs: update API documentation
infra: add staging deployment workflow
```

---

## Release Process

### Create Release
```bash
git checkout main
git pull origin main
git tag -a v1.2.0 -m "Release 1.2.0: description"
git push origin v1.2.0
gh release create v1.2.0 --title "v1.2.0" --notes "Release notes here"
```

### Semantic Versioning
| Change | Version Bump | Example |
|--------|-------------|---------|
| Breaking changes | Major | 1.0.0 -> 2.0.0 |
| New features | Minor | 1.0.0 -> 1.1.0 |
| Bug fixes | Patch | 1.0.0 -> 1.0.1 |

---

## Related Skills

- **github-actions** - CI/CD automation triggered by Git events
- **container-ops** - Docker image tagging aligned with Git tags

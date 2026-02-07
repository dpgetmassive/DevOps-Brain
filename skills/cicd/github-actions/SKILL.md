---
name: github-actions
version: 1.0.0
description: When the user wants to create or manage GitHub Actions workflows, CI/CD pipelines, or deployment automation. Also use when the user mentions "GitHub Actions," "CI/CD," "workflow," "pipeline," "deploy," "build," or "automated testing." For Ansible-based automation, see ansible-ops. For Git branching, see git-workflow.
---

# GitHub Actions

You are an expert in GitHub Actions CI/CD. The homelab uses GitHub Actions for application deployments.

## Existing Workflows

**Read `context/infrastructure-context.md` first** for deployment targets.

| Project | Workflow | Trigger | Purpose |
|---------|----------|---------|---------|
| cp-www-staging | deploy-staging.yml | Push to main | Deploy to staging.cyber-people.tech |
| smb1001-gap-analysis | ci.yml | Push/PR to main/develop | Lint, type-check, build |
| smb1001-gap-analysis | deploy-staging.yml | Push to develop | Deploy to gap-app.cyber-people.tech |

**Deployment pattern**: GitHub Actions -> rsync over SSH -> systemd restart

## Guard Rails

**Auto-approve**: Viewing workflows, checking run status, reading logs
**Confirm first**: Modifying production deployment workflows, changing secrets

---

## Workflow Authoring

### Basic CI Workflow Template
```yaml
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run build
```

### Deployment Workflow Template
```yaml
name: Deploy Staging
on:
  push:
    branches: [develop]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci && npm run build

      - name: Deploy via rsync
        uses: burnett01/rsync-deployments@6.0.0
        with:
          switches: -avzr --delete
          path: .next/
          remote_path: /opt/app/
          remote_host: ${{ secrets.DEPLOY_HOST }}
          remote_user: ${{ secrets.DEPLOY_USER }}
          remote_key: ${{ secrets.DEPLOY_KEY }}

      - name: Restart service
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.DEPLOY_HOST }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_KEY }}
          script: sudo systemctl restart app.service
```

---

## Secrets Management

### Required Secrets for Deployment
| Secret | Purpose |
|--------|---------|
| `DEPLOY_HOST` | Target server hostname/IP |
| `DEPLOY_USER` | SSH user for deployment |
| `DEPLOY_KEY` | SSH private key |

### Setting Secrets (gh CLI)
```bash
gh secret set DEPLOY_HOST --body "staging.cyber-people.tech"
gh secret set DEPLOY_KEY < ~/.ssh/deploy_key
```

### Listing Secrets
```bash
gh secret list
```

---

## Workflow Management (gh CLI)

### List Recent Runs
```bash
gh run list --limit 10
```

### View Run Details
```bash
gh run view <run_id>
```

### View Run Logs
```bash
gh run view <run_id> --log
```

### Re-run Failed Workflow
```bash
gh run rerun <run_id>
```

### Manually Trigger Workflow
```bash
gh workflow run <workflow_name>
```

---

## Best Practices

### Caching
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

### Matrix Builds
```yaml
strategy:
  matrix:
    node-version: [18, 20]
    os: [ubuntu-latest]
```

### Conditional Steps
```yaml
- name: Deploy
  if: github.ref == 'refs/heads/main' && github.event_name == 'push'
  run: ./deploy.sh
```

---

## Related Skills

- **git-workflow** - Branching strategy and PR conventions
- **container-ops** - Docker builds in CI
- **ansible-ops** - Infrastructure automation

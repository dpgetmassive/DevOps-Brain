# MkDocs Documentation Builder

MkDocs is a static site generator for building documentation from Markdown files. Uses YAML configuration (`mkdocs.yml`) and supports themes like Material for MkDocs. Generates static HTML sites suitable for GitHub Pages or other hosting.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | N | No API (CLI tool only) |
| MCP | N | No MCP server available |
| CLI | Y | `mkdocs` command-line tool (Python package) |
| SDK | Y | Python library (`mkdocs`), plugins available |

## Authentication

**No authentication required** for local builds. GitHub Pages deployment uses Git credentials.

**GitHub Pages**: Deploy via `mkdocs gh-deploy` (requires Git authentication).

```bash
# GitHub Pages deployment (uses Git credentials)
mkdocs gh-deploy

# With custom message
mkdocs gh-deploy -m "Update documentation"
```

## Common Agent Operations

### Project Setup and Development

```bash
# Create new project (creates mkdocs.yml and docs/ directory)
mkdocs new my-project
cd my-project

# Start development server (http://127.0.0.1:8000)
mkdocs serve
mkdocs serve -a 0.0.0.0:8080  # Custom host/port
mkdocs serve --livereload      # Auto-reload on changes

# Build static site
mkdocs build
mkdocs build --clean           # Remove old files
mkdocs build -d output/        # Custom output directory
```

### Configuration (mkdocs.yml)

```yaml
site_name: My Documentation
site_url: https://example.com

theme:
  name: material
  palette:
    - scheme: default
      primary: blue
    - scheme: dark
      primary: blue

nav:
  - Home: index.md
  - Guide: guide.md
  - API: api.md

plugins:
  - search
  - markdown_extensions:
      - codehilite
      - toc
```

### Deployment and Extensions

```bash
# GitHub Pages deployment
mkdocs gh-deploy
mkdocs gh-deploy --remote-name upstream
mkdocs gh-deploy --remote-branch custom-branch

# Install Material theme
pip install mkdocs-material
pip install "mkdocs-material[extras]"

# Install plugins
pip install mkdocs-minify-plugin mkdocs-redirects
```

## Key Objects/Metrics

- **Configuration**: `mkdocs.yml` file with site settings, navigation, theme
- **Source Files**: Markdown files in `docs/` directory
- **Built Site**: Static HTML in `site/` directory (generated)
- **Themes**: Material, ReadTheDocs, Bootstrap, custom themes
- **Plugins**: Search, minify, redirects, markdown extensions

## When to Use

- **Documentation sites**: Build static documentation from Markdown
- **Runbook creation**: Generate operational runbooks with navigation
- **Infrastructure docs**: Document homelab setup, network topology, services
- **API documentation**: Document APIs, endpoints, examples
- **Knowledge base**: Create searchable documentation sites

## Rate Limits

No rate limits for local operations. GitHub Pages deployment subject to Git/GitHub rate limits. Build time depends on number of pages and plugins.

## Relevant Skills

- `runbook-writer` - Create operational runbooks with MkDocs
- `infra-documentation` - Document infrastructure using MkDocs

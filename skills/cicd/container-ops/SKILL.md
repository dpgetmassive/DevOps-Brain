---
name: container-ops
version: 1.0.0
description: When the user wants to build Docker images, write Dockerfiles, manage container registries, or implement multi-stage builds. Also use when the user mentions "Dockerfile," "build image," "container registry," "multi-stage build," "image scanning," or "push image." For running containers, see docker-management.
---

# Container Operations

You are an expert in container image building and registry management.

## Guard Rails

**Auto-approve**: Dockerfile review, image listing, scanning results
**Confirm first**: Pushing to public registries, deleting images from registries

---

## Dockerfile Best Practices

### Multi-Stage Build (Node.js)
```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
USER appuser
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Multi-Stage Build (Python)
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt
COPY . .

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app .
ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000
CMD ["python", "app.py"]
```

### Key Principles
1. **Use specific base image tags** - not `latest`
2. **Multi-stage builds** - separate build and runtime
3. **Non-root user** - `USER appuser`
4. **Minimize layers** - combine RUN commands
5. **Order for cache** - dependencies before source code
6. **Use .dockerignore** - exclude node_modules, .git, etc.

---

## Building Images

### Build Image
```bash
docker build -t <name>:<tag> .
```

### Build with Build Args
```bash
docker build --build-arg NODE_ENV=production -t myapp:1.0 .
```

### Build for Specific Platform
```bash
docker buildx build --platform linux/amd64 -t myapp:1.0 .
```

---

## Image Scanning (Trivy)

### Scan Local Image
```bash
trivy image <image>:<tag>
```

### Scan Dockerfile
```bash
trivy config Dockerfile
```

### Scan with Severity Filter
```bash
trivy image --severity HIGH,CRITICAL <image>:<tag>
```

---

## Docker Compose Best Practices

### Production Compose Template
```yaml
version: '3.8'
services:
  app:
    image: myapp:1.0
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    volumes:
      - app-data:/app/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'

volumes:
  app-data:
```

---

## .dockerignore Template
```
node_modules
.git
.env
*.md
.github
.vscode
dist
coverage
```

---

## Related Skills

- **docker-management** - Running and managing containers
- **github-actions** - Building images in CI/CD
- **vuln-scanning** - Container vulnerability scanning

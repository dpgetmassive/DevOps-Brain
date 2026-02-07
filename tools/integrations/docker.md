# Docker CLI + API

Docker provides container runtime management via CLI (`docker`, `docker-compose`) and REST API (Docker daemon socket). Used for containerized services across the homelab.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `/var/run/docker.sock` (Unix socket) or `http://localhost:2375` (TCP) |
| MCP | N | No MCP server available |
| CLI | Y | `docker` and `docker-compose` command-line tools |
| SDK | Y | Python `docker`, Go `docker/client`, Node.js `dockerode` |

## Authentication

**Docker Socket**: Unix socket at `/var/run/docker.sock` (default). Requires root or docker group membership.

```bash
# Check socket permissions
ls -l /var/run/docker.sock

# Add user to docker group (if needed)
sudo usermod -aG docker $USER
```

**Remote API**: TCP socket requires TLS certificates for secure access. Not typically used in homelab.

**Docker Compose**: Uses same authentication as Docker CLI.

## Common Agent Operations

### List Containers

```bash
# Running containers
docker ps

# All containers (including stopped)
docker ps -a

# Via API (using curl with socket)
curl --unix-socket /var/run/docker.sock \
  http://localhost/containers/json
```

### Container Lifecycle

```bash
# Start container
docker start <container_id_or_name>

# Stop container
docker stop <container_id_or_name>

# Restart container
docker restart <container_id_or_name>

# Remove container
docker rm <container_id_or_name>

# Remove container (force, even if running)
docker rm -f <container_id_or_name>
```

### Container Logs

```bash
# View logs
docker logs <container_id_or_name>

# Follow logs (tail -f)
docker logs -f <container_id_or_name>

# Last 100 lines
docker logs --tail 100 <container_id_or_name>

# Via API
curl --unix-socket /var/run/docker.sock \
  "http://localhost/containers/<container_id>/logs?stdout=1&stderr=1&tail=100"
```

### Execute Command in Container

```bash
# Run command in running container
docker exec <container_id_or_name> <command>

# Interactive shell
docker exec -it <container_id_or_name> /bin/bash

# Via API
curl -X POST --unix-socket /var/run/docker.sock \
  -H "Content-Type: application/json" \
  -d '{"AttachStdin": false, "AttachStdout": true, "AttachStderr": true, "Cmd": ["uptime"]}' \
  http://localhost/containers/<container_id>/exec
```

### Docker Compose Operations

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# Scale service
docker-compose up -d --scale <service>=3
```

### Image Management

```bash
# List images
docker images

# Pull image
docker pull <image:tag>

# Remove image
docker rmi <image_id>

# Prune unused images
docker image prune -a
```

### Network Management

```bash
# List networks
docker network ls

# Inspect network
docker network inspect <network_name>

# Create network
docker network create <network_name>
```

### Volume Management

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect <volume_name>

# Remove volume
docker volume rm <volume_name>

# Prune unused volumes
docker volume prune
```

### Container Stats

```bash
# Real-time stats
docker stats

# Stats for specific container
docker stats <container_id_or_name>

# Via API
curl --unix-socket /var/run/docker.sock \
  http://localhost/containers/<container_id>/stats?stream=false
```

## Key Objects/Metrics

- **Containers**: Running or stopped container instances
- **Images**: Container images (base images, application images)
- **Networks**: Docker networks (bridge, host, custom)
- **Volumes**: Persistent storage volumes
- **Compose Stacks**: Multi-container applications defined in `docker-compose.yml`
- **Stats**: CPU, memory, network I/O, block I/O usage

## When to Use

- **Container management**: Start, stop, restart services (dockc, docker00)
- **Log inspection**: Troubleshoot container issues, verify service health
- **Compose deployments**: Deploy multi-container stacks
- **Image updates**: Pull new images, update running containers
- **Resource monitoring**: Check container resource usage
- **Volume management**: Manage persistent data storage

## Rate Limits

No explicit rate limits. Docker daemon handles:
- Concurrent container operations
- API request queuing
- Resource limits per container (CPU, memory)

## Relevant Skills

- `docker-management` - Container lifecycle and troubleshooting
- `monitoring-ops` - Container health and resource monitoring
- `service-deployment` - Deploying new containerized services

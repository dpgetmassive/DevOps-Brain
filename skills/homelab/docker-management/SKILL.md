---
name: docker-management
version: 1.0.0
description: When the user wants to manage Docker containers, compose stacks, images, networks, or volumes. Also use when the user mentions "docker," "container," "compose," "stack," "docker-compose," "container logs," or "docker update." For Proxmox container (LXC) management, see proxmox-vm-management.
---

# Docker Management

You are an expert in Docker container management across the homelab.

## Docker Hosts

**Read `context/service-inventory.md` first** for the full service catalog.

| Host | IP | Access | Docker Use |
|------|-----|--------|-----------|
| n100uck | 10.16.1.18 | `ssh n100uck` | NPM backup instance |
| dockc | 10.16.1.4 | `ssh dockc` | General Docker host (VM 100) |
| docker00 | 10.16.1.40 | `pct exec 106` | Docker host (CT 106) |
| gm-ai | 10.16.1.9 | `ssh gm-ai` | AI services (Ollama, Open WebUI, clawdbot) |

## Guard Rails

**Auto-approve**: Container status, logs, stats, image listing, network inspection
**Confirm first**: Container deletion, volume removal, network changes affecting multiple services

---

## Container Operations

### List Running Containers
```bash
ssh <alias> "docker ps"
```

### List All Containers (Including Stopped)
```bash
ssh <alias> "docker ps -a"
```

### View Container Logs
```bash
ssh <alias> "docker logs --tail 50 <container>"
ssh <alias> "docker logs -f <container>"  # Follow
```

### Start / Stop / Restart
```bash
ssh <alias> "docker start <container>"
ssh <alias> "docker stop <container>"
ssh <alias> "docker restart <container>"
```

### Resource Usage
```bash
ssh <alias> "docker stats --no-stream"
```

### Execute Command in Container
```bash
ssh <alias> "docker exec -it <container> <command>"
# Example: shell into container
ssh <alias> "docker exec -it <container> /bin/sh"
```

### Container Details
```bash
ssh <alias> "docker inspect <container> | jq '.[0].State'"
```

---

## Docker Compose Operations

### Start Stack
```bash
ssh <alias> "cd /path/to/compose && docker compose up -d"
```

### Stop Stack
```bash
ssh <alias> "cd /path/to/compose && docker compose down"
```

### Restart Stack
```bash
ssh <alias> "cd /path/to/compose && docker compose restart"
```

### View Stack Status
```bash
ssh <alias> "cd /path/to/compose && docker compose ps"
```

### View Stack Logs
```bash
ssh <alias> "cd /path/to/compose && docker compose logs --tail 50"
```

### Pull Updated Images
```bash
ssh <alias> "cd /path/to/compose && docker compose pull"
```

### Update Stack (Pull + Recreate)
```bash
ssh <alias> "cd /path/to/compose && docker compose pull && docker compose up -d"
```

---

## Image Management

### List Images
```bash
ssh <alias> "docker images"
```

### Pull Image
```bash
ssh <alias> "docker pull <image>:<tag>"
```

### Remove Unused Images
```bash
ssh <alias> "docker image prune -f"
```

### Remove All Unused Resources
```bash
ssh <alias> "docker system prune -f"
# Include volumes (caution!):
ssh <alias> "docker system prune -a --volumes -f"
```

### Check Disk Usage
```bash
ssh <alias> "docker system df"
```

---

## Network Management

### List Networks
```bash
ssh <alias> "docker network ls"
```

### Inspect Network
```bash
ssh <alias> "docker network inspect <network>"
```

### Create Network
```bash
ssh <alias> "docker network create <network_name>"
```

---

## Volume Management

### List Volumes
```bash
ssh <alias> "docker volume ls"
```

### Inspect Volume
```bash
ssh <alias> "docker volume inspect <volume>"
```

### Remove Unused Volumes
```bash
ssh <alias> "docker volume prune -f"
```

---

## Known Docker Services

### NPM Backup on n100uck
```bash
# Status
ssh n100uck "docker ps | grep nginx-proxy-manager"

# Logs
ssh n100uck "docker logs --tail 50 npm"

# Restart
ssh n100uck "docker restart npm"

# Ports: 81 (admin), 8080 (HTTP), 8443 (HTTPS)
```

### AI Services on gm-ai
```bash
# Status
ssh gm-ai "docker ps"

# Check Ollama
ssh gm-ai "docker logs --tail 20 ollama"

# Check Open WebUI
ssh gm-ai "docker logs --tail 20 open-webui"
```

---

## Troubleshooting

### Container Won't Start
```bash
ssh <alias> << 'EOF'
echo "=== Container Inspect ==="
docker inspect <container> | jq '.[0].State'
echo ""
echo "=== Container Logs ==="
docker logs --tail 30 <container>
echo ""
echo "=== Disk Space ==="
docker system df
echo ""
echo "=== Host Disk ==="
df -h /
EOF
```

### Container Networking Issues
```bash
ssh <alias> << 'EOF'
echo "=== Container Networks ==="
docker inspect <container> | jq '.[0].NetworkSettings.Networks'
echo ""
echo "=== DNS from Container ==="
docker exec <container> nslookup google.com 2>/dev/null || echo "nslookup not available"
echo ""
echo "=== Host DNS ==="
cat /etc/resolv.conf
EOF
```

---

## Related Skills

- **proxmox-vm-management** - LXC containers (not Docker)
- **container-ops** - Dockerfile best practices, image building
- **reverse-proxy** - Routing to Docker services via Traefik/NPM

---
name: llm-hosting
version: 1.0.0
description: When the user wants to manage local LLM hosting -- Ollama model management, Open WebUI configuration, model selection, or resource monitoring on gm-ai. Also use when the user mentions "Ollama," "model," "deploy model," "pull model," "Open WebUI," "LLM," or "local AI." For the API gateway, see ai-gateway. For AI development patterns, see ai-development.
---

# LLM Hosting

You are an expert in local LLM hosting with Ollama and Open WebUI.

## AI Host: gm-ai (10.16.1.9)

**Read `context/infrastructure-context.md` first.**

| Service | Port | URL | Health Check |
|---------|------|-----|-------------|
| Ollama | 11434 | http://10.16.1.9:11434 | `curl http://10.16.1.9:11434/api/tags` |
| Open WebUI | 3000 | http://10.16.1.9:3000 | `curl http://10.16.1.9:3000` |
| Cockpit | 9090 | https://10.16.1.9:9090 | System management |

**Host**: Physical Debian 12 box, single NVMe (no RAID)
**SSH**: `ssh gm-ai` (user: gm-admin)
**Storage**: homelab ZFS pool - ai-services (26.6G), docker (4.1G)
**Backup**: Daily 3:00 AM ZFS replication to TrueNAS DR

## Guard Rails

**Auto-approve**: Model listing, status checks, pulling models, resource monitoring
**Confirm first**: Deleting models, changing Ollama config, modifying Open WebUI settings

---

## Ollama Model Management

### List Installed Models
```bash
ssh gm-ai "ollama list"
# Or via API:
curl -s http://10.16.1.9:11434/api/tags | python3 -m json.tool
```

### Pull a Model
```bash
ssh gm-ai "ollama pull <model_name>"
# Examples:
ssh gm-ai "ollama pull llama3.2"
ssh gm-ai "ollama pull mistral"
ssh gm-ai "ollama pull codellama"
ssh gm-ai "ollama pull deepseek-r1:8b"
```

### Run Model (Interactive)
```bash
ssh gm-ai "ollama run <model_name>"
```

### Test Model via API
```bash
curl -s http://10.16.1.9:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Hello, how are you?",
  "stream": false
}' | python3 -m json.tool
```

### Chat Completion (OpenAI-Compatible)
```bash
curl -s http://10.16.1.9:11434/v1/chat/completions -d '{
  "model": "llama3.2",
  "messages": [{"role": "user", "content": "Hello"}]
}' | python3 -m json.tool
```

### Delete Model
```bash
# Confirm first!
ssh gm-ai "ollama rm <model_name>"
```

### Show Model Details
```bash
ssh gm-ai "ollama show <model_name>"
```

### Check Running Models
```bash
curl -s http://10.16.1.9:11434/api/ps | python3 -m json.tool
```

---

## Model Selection Guide

| Use Case | Recommended Model | Size | Notes |
|----------|------------------|------|-------|
| General chat | llama3.2 | 3B/8B | Good all-rounder |
| Code generation | codellama | 7B/13B | Specialized for code |
| Instruction following | mistral | 7B | Fast, good quality |
| Reasoning | deepseek-r1 | 8B+ | Strong reasoning |
| Small/fast | phi-3 | 3.8B | Low resource usage |
| Embeddings | nomic-embed-text | 137M | For RAG pipelines |

---

## Open WebUI

### Access
- **URL**: http://10.16.1.9:3000
- **Backend**: Connects to Ollama at localhost:11434

### Check Status
```bash
ssh gm-ai "docker ps | grep open-webui"
```

### View Logs
```bash
ssh gm-ai "docker logs --tail 50 open-webui"
```

### Restart
```bash
ssh gm-ai "docker restart open-webui"
```

---

## Resource Monitoring

### Check System Resources
```bash
ssh gm-ai << 'EOF'
echo "=== gm-ai AI HOST STATUS ==="
echo "--- CPU/Memory ---"
free -h
echo ""
echo "--- Load ---"
uptime
echo ""
echo "--- Disk (ZFS) ---"
sudo zfs list -o name,used,available homelab
sudo zfs list -o name,used,available homelab/ai-services
sudo zfs list -o name,used,available homelab/docker
echo ""
echo "--- Docker Containers ---"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""
echo "--- Ollama Models ---"
ollama list
EOF
```

### Check GPU (if available)
```bash
ssh gm-ai "nvidia-smi 2>/dev/null || echo 'No NVIDIA GPU detected'"
```

---

## Backup & Recovery

### Check Replication Status
```bash
ssh gm-ai "sudo systemctl status zfs-replicate-dr.timer --no-pager"
ssh gm-ai "sudo tail -10 /var/log/zfs-replicate-dr.log"
```

### Verify DR Copy
```bash
ssh truenas-dr "zfs list -r Tank/Data-DR-Copy/gm-ai-homelab"
```

---

## Troubleshooting

### Ollama Not Responding
```bash
ssh gm-ai << 'EOF'
echo "=== Ollama Status ==="
systemctl status ollama 2>/dev/null || docker ps | grep ollama
echo ""
echo "=== Port Check ==="
ss -tlnp | grep 11434
echo ""
echo "=== API Test ==="
curl -s http://localhost:11434/api/tags | head -5
EOF
```

### Out of Disk Space
```bash
ssh gm-ai << 'EOF'
echo "=== ZFS Usage ==="
sudo zfs list -r homelab
echo ""
echo "=== Docker Disk ==="
docker system df
echo ""
echo "=== Ollama Models ==="
ollama list
EOF
```

---

## Related Skills

- **ai-gateway** - clawdbot API gateway configuration
- **ai-development** - Agent and RAG development patterns
- **storage-management** - ZFS backup and replication

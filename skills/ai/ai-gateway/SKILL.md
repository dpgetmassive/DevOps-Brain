---
name: ai-gateway
version: 1.0.0
description: When the user wants to configure the AI API gateway -- clawdbot routing, model endpoints, API key management, or rate limiting. Also use when the user mentions "clawdbot," "API gateway," "AI routing," "model routing," or "AI proxy." For model management, see llm-hosting. For development patterns, see ai-development.
---

# AI Gateway (clawdbot)

You are an expert in AI API gateway management.

## Gateway Overview

**Read `context/infrastructure-context.md` first.**

**Host**: gm-ai (10.16.1.9)
**Service**: clawdbot - Custom API gateway for AI services
**Storage**: `/homelab/ai-services` (26.6G) on gm-ai

**NOTE**: Detailed clawdbot configuration requires SSH discovery on gm-ai. The exact ports, Docker Compose files, and routing configuration need to be verified.

## Guard Rails

**Auto-approve**: Status checks, viewing configuration, API testing
**Confirm first**: Route changes, API key rotation, upstream modifications

---

## Discovery (Run First if Config Unknown)

### Find clawdbot Configuration
```bash
ssh gm-ai << 'EOF'
echo "=== Docker Containers ==="
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Ports}}\t{{.Status}}"
echo ""
echo "=== AI Services Directory ==="
ls -la /homelab/ai-services/ 2>/dev/null || echo "Path not found"
echo ""
echo "=== Docker Compose Files ==="
find /homelab -name "docker-compose*" -type f 2>/dev/null
echo ""
echo "=== Listening Ports ==="
ss -tlnp | grep -E '(3000|8080|11434|5000|4000)'
echo ""
echo "=== Systemd Services ==="
systemctl list-units --type=service | grep -iE '(claw|ai|ollama|webui)'
EOF
```

### Check clawdbot Logs
```bash
ssh gm-ai "docker logs --tail 50 clawdbot 2>/dev/null || echo 'Container not found - check naming'"
```

---

## Gateway Architecture (Expected)

```
Clients (agents, apps)
    │
    ▼
clawdbot Gateway (:PORT)
    │
    ├──> Ollama (:11434) - Local LLM inference
    ├──> Open WebUI (:3000) - Chat interface
    └──> External APIs - OpenAI, Anthropic (if configured)
```

### Key Functions
- **Model routing**: Direct requests to appropriate inference engine
- **API key management**: Centralized authentication
- **Rate limiting**: Protect local resources
- **Logging**: Request/response logging for debugging
- **OpenAI compatibility**: Unified API format across providers

---

## Common Operations

### Check Gateway Health
```bash
ssh gm-ai "curl -s http://localhost:<PORT>/health 2>/dev/null || echo 'Port TBD'"
```

### List Available Models via Gateway
```bash
ssh gm-ai "curl -s http://localhost:<PORT>/v1/models 2>/dev/null"
```

### Test Chat Completion via Gateway
```bash
curl -s http://10.16.1.9:<PORT>/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <api_key>" \
  -d '{
    "model": "llama3.2",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

---

## Configuration Management

### View Configuration
```bash
ssh gm-ai "cat /homelab/ai-services/clawdbot/config.yml 2>/dev/null || find /homelab/ai-services -name '*.yml' -o -name '*.env' 2>/dev/null"
```

### Restart Gateway
```bash
ssh gm-ai "docker restart clawdbot 2>/dev/null || systemctl restart clawdbot 2>/dev/null"
```

---

## Troubleshooting

### Gateway Not Responding
```bash
ssh gm-ai << 'EOF'
echo "=== Container Status ==="
docker ps -a | grep -i claw
echo ""
echo "=== Service Status ==="
systemctl status clawdbot 2>/dev/null || echo "Not a systemd service"
echo ""
echo "=== Port Bindings ==="
ss -tlnp
echo ""
echo "=== Docker Logs ==="
docker logs --tail 20 clawdbot 2>/dev/null
EOF
```

### Upstream Connection Issues
```bash
ssh gm-ai << 'EOF'
echo "=== Ollama Status ==="
curl -s http://localhost:11434/api/tags | head -3
echo ""
echo "=== Open WebUI Status ==="
curl -s http://localhost:3000 | head -3
EOF
```

---

## Related Skills

- **llm-hosting** - Ollama and Open WebUI management
- **ai-development** - Development patterns using the gateway
- **docker-management** - Container operations for gateway

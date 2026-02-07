# Open WebUI

Open WebUI provides a web-based chat interface for Ollama models with multi-model support, document upload, RAG capabilities, and custom prompt management. Deployed on gm-ai (10.16.1.9) via Docker.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `http://10.16.1.9:3000/api/`, management endpoints available |
| MCP | N | No MCP server available |
| CLI | N | No CLI tool, web UI and REST API only |
| SDK | N | No official SDK, use REST API directly |

## Authentication

**Web UI**: Local user accounts managed within Open WebUI. Default admin account created on first launch.

**REST API**: Requires authentication token. Get token from user settings or API key management.

```bash
# Login via API to get token
curl -X POST http://10.16.1.9:3000/api/v1/auths/signin \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'

# Response includes access_token for subsequent requests
```

**Docker Access**: Requires SSH access to gm-ai host for container management.

## Common Agent Operations

### List Available Models

```bash
# Via REST API (requires auth token)
curl http://10.16.1.9:3000/api/v1/models \
  -H "Authorization: Bearer <token>"

# Returns models available from connected Ollama instance
```

### Create Chat Session

```bash
# Via REST API
curl -X POST http://10.16.1.9:3000/api/v1/chats \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "DevOps Discussion",
    "model": "llama3.2:3b"
  }'
```

### Send Message in Chat

```bash
# Via REST API
curl -X POST http://10.16.1.9:3000/api/v1/chats/<chat-id>/messages \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Explain Kubernetes",
    "role": "user"
  }'
```

### Upload Document for RAG

```bash
# Via REST API (multipart form)
curl -X POST http://10.16.1.9:3000/api/v1/documents \
  -H "Authorization: Bearer <token>" \
  -F "file=@document.pdf" \
  -F "name=DevOps Guide"

# Document is processed and indexed for RAG queries
```

### List Documents

```bash
# Via REST API
curl http://10.16.1.9:3000/api/v1/documents \
  -H "Authorization: Bearer <token>"

# Returns uploaded documents with metadata
```

### Get Chat History

```bash
# Via REST API
curl http://10.16.1.9:3000/api/v1/chats \
  -H "Authorization: Bearer <token>"

# Returns all chat sessions for authenticated user
```

### Manage Custom Prompts

```bash
# List prompts
curl http://10.16.1.9:3000/api/v1/prompts \
  -H "Authorization: Bearer <token>"

# Create prompt
curl -X POST http://10.16.1.9:3000/api/v1/prompts \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Code Review",
    "content": "Review this code for security issues..."
  }'
```

### Check Service Status

```bash
# Via Docker (on gm-ai)
ssh gm-ai "docker ps | grep open-webui"

# Via health endpoint
curl http://10.16.1.9:3000/health
```

### Restart Service

```bash
# Via Docker
ssh gm-ai "docker restart open-webui"

# Or via docker-compose if used
ssh gm-ai "cd /path/to/compose && docker-compose restart open-webui"
```

## Key Objects/Metrics

- **Chat Sessions**: Conversation threads with model selection and history
- **Messages**: Individual messages within chat sessions (user/assistant/system)
- **Documents**: Uploaded files processed for RAG (PDF, TXT, MD, etc.)
- **Prompts**: Custom prompt templates for reusable instructions
- **Users**: Local user accounts with authentication
- **Models**: Connected Ollama models available for chat

## When to Use

- **Multi-model chat**: Switch between different LLM models in single interface
- **RAG applications**: Upload documents and query them with context-aware responses
- **Prompt management**: Create and reuse custom prompts for specific tasks
- **Chat history**: Maintain conversation history across sessions
- **User management**: Manage access for multiple users
- **Development**: Test AI features with web-based interface
- **Documentation**: Build knowledge base from uploaded documents

## Rate Limits

No explicit rate limits. Performance depends on:
- Underlying Ollama instance performance
- Document processing capacity
- Concurrent user sessions
- RAG query complexity (document search + generation)

## Relevant Skills

- `llm-hosting` - LLM service management and monitoring
- `ai-development` - AI application development and testing

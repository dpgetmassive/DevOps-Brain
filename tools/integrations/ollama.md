# Ollama LLM Inference Engine

Ollama provides local LLM inference via REST API and CLI tools. Runs models locally on gm-ai (10.16.1.9) with OpenAI-compatible endpoints for easy integration with AI applications.

## Capabilities

| Integration | Available | Notes |
|-------------|-----------|-------|
| API | Y | REST API at `http://10.16.1.9:11434`, OpenAI-compatible at `/v1/chat/completions` |
| MCP | N | No MCP server available |
| CLI | Y | `ollama` command-line tool for model management |
| SDK | Y | OpenAI SDK compatible, Python `ollama` package, JavaScript `ollama` package |

## Authentication

**REST API**: No authentication required for local network access. All endpoints are public within the network.

**CLI**: Requires SSH access to gm-ai host or local installation.

## Common Agent Operations

### List Available Models

```bash
# Via REST API
curl http://10.16.1.9:11434/api/tags

# Via CLI
ssh gm-ai "ollama list"

# Response includes model names, sizes, modified dates
```

### Pull/Download Model

```bash
# Via CLI
ssh gm-ai "ollama pull llama3.2:3b"

# Via REST API (triggers pull)
curl -X POST http://10.16.1.9:11434/api/pull \
  -d '{"name": "llama3.2:3b"}'
```

### Run Chat Completion

```bash
# Via REST API (OpenAI-compatible)
curl http://10.16.1.9:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:3b",
    "messages": [{"role": "user", "content": "Hello"}]
  }'

# Via REST API (native)
curl http://10.16.1.9:11434/api/chat \
  -d '{
    "model": "llama3.2:3b",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": false
  }'
```

### Generate Text (Non-Conversational)

```bash
# Via REST API
curl http://10.16.1.9:11434/api/generate \
  -d '{
    "model": "llama3.2:3b",
    "prompt": "Write a haiku about DevOps",
    "stream": false
  }'
```

### Get Embeddings

```bash
# Via REST API
curl http://10.16.1.9:11434/api/embeddings \
  -d '{
    "model": "nomic-embed-text",
    "prompt": "DevOps automation"
  }'
```

### List Running Models

```bash
# Via REST API
curl http://10.16.1.9:11434/api/ps

# Via CLI
ssh gm-ai "ollama ps"

# Shows active model instances and memory usage
```

### Show Model Information

```bash
# Via CLI
ssh gm-ai "ollama show llama3.2:3b"

# Via REST API
curl http://10.16.1.9:11434/api/show \
  -d '{"name": "llama3.2:3b"}'

# Returns model details, parameters, template, system prompt
```

### Remove Model

```bash
# Via CLI
ssh gm-ai "ollama rm llama3.2:3b"

# Via REST API
curl -X DELETE http://10.16.1.9:11434/api/delete \
  -d '{"name": "llama3.2:3b"}'
```

### Stream Responses

```bash
# Via REST API (streaming)
curl http://10.16.1.9:11434/api/chat \
  -d '{
    "model": "llama3.2:3b",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": true
  }'

# Response is Server-Sent Events (SSE) format
```

## Key Objects/Metrics

- **Models**: LLM models (llama3.2, mistral, codellama, etc.) with version tags
- **Chat Sessions**: Conversation history with role-based messages
- **Embeddings**: Vector embeddings for RAG and semantic search
- **Running Instances**: Active model processes and memory usage
- **Model Metadata**: Size, parameters, template, system prompts

## When to Use

- **LLM inference**: Run local language models for AI applications
- **OpenAI compatibility**: Use OpenAI SDK with local models via `/v1/chat/completions`
- **RAG applications**: Generate embeddings for document search and retrieval
- **Model management**: Pull, list, and remove models from local registry
- **Development**: Test AI features without external API costs
- **Privacy**: Process sensitive data locally without cloud API calls

## Rate Limits

No explicit rate limits. Performance depends on:
- Hardware resources (CPU, GPU, RAM) on gm-ai
- Model size and complexity
- Concurrent requests (Ollama handles multiple requests)
- GPU availability (faster inference with GPU acceleration)

## Relevant Skills

- `llm-hosting` - LLM service management and monitoring
- `ai-development` - AI application development and testing
- `ai-gateway` - AI service routing and load balancing

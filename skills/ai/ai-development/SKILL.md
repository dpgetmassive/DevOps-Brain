---
name: ai-development
version: 1.0.0
description: When the user wants to develop AI applications -- agent frameworks, RAG pipelines, prompt engineering, or AI workflow automation. Also use when the user mentions "agent," "RAG," "prompt engineering," "AI workflow," "embeddings," "vector database," or "AI automation." For model hosting, see llm-hosting. For the gateway, see ai-gateway.
---

# AI Development

You are an expert in AI application development with local LLM infrastructure.

## Development Environment

**Read `context/infrastructure-context.md` first.**

**LLM Backend**: Ollama on gm-ai (10.16.1.9:11434)
**Chat UI**: Open WebUI on gm-ai (10.16.1.9:3000)
**API Gateway**: clawdbot on gm-ai
**Compatible API**: OpenAI-compatible endpoint at `http://10.16.1.9:11434/v1/`

## Guard Rails

**Auto-approve**: Code review, testing prompts, querying models, development guidance
**Confirm first**: Deploying to production, modifying gateway configuration

---

## Using Local Ollama as OpenAI-Compatible Backend

### Python (openai SDK)
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://10.16.1.9:11434/v1/",
    api_key="ollama"  # Ollama doesn't require a real key
)

response = client.chat.completions.create(
    model="llama3.2",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain ZFS snapshots."}
    ]
)
print(response.choices[0].message.content)
```

### Python (requests)
```python
import requests

response = requests.post("http://10.16.1.9:11434/api/generate", json={
    "model": "llama3.2",
    "prompt": "Explain ZFS snapshots briefly.",
    "stream": False
})
print(response.json()["response"])
```

### curl
```bash
curl -s http://10.16.1.9:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2",
    "messages": [{"role": "user", "content": "Hello"}]
  }' | python3 -m json.tool
```

---

## RAG (Retrieval-Augmented Generation)

### Architecture
```
Documents -> Chunking -> Embedding -> Vector Store
                                          │
User Query -> Embedding -> Similarity Search
                                          │
                              Retrieved Context + Query -> LLM -> Response
```

### Embedding with Ollama
```python
import requests

def get_embedding(text, model="nomic-embed-text"):
    response = requests.post("http://10.16.1.9:11434/api/embeddings", json={
        "model": model,
        "prompt": text
    })
    return response.json()["embedding"]

# Pull embedding model first: ollama pull nomic-embed-text
embedding = get_embedding("ZFS replication setup guide")
```

### Simple RAG Pipeline
```python
from openai import OpenAI

client = OpenAI(base_url="http://10.16.1.9:11434/v1/", api_key="ollama")

def rag_query(query, context_docs):
    context = "\n\n".join(context_docs)
    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": f"Answer based on this context:\n{context}"},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content
```

---

## Agent Development Patterns

### Tool-Calling Agent
```python
import json
from openai import OpenAI

client = OpenAI(base_url="http://10.16.1.9:11434/v1/", api_key="ollama")

tools = [{
    "type": "function",
    "function": {
        "name": "check_host_status",
        "description": "Check if a homelab host is online",
        "parameters": {
            "type": "object",
            "properties": {
                "hostname": {"type": "string", "description": "The host alias"}
            },
            "required": ["hostname"]
        }
    }
}]

response = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "Is pve-scratchy online?"}],
    tools=tools
)
```

---

## Prompt Engineering for DevOps

### System Prompts for Infrastructure Tasks
```
You are a DevOps assistant for the Get Massive Dojo homelab.
Key hosts: pve-scratchy (10.16.1.22), pve-itchy (10.16.1.8),
n100uck (10.16.1.18), truenas-scale (10.16.1.6).
Always provide specific commands with the correct SSH alias.
Always include verification steps.
```

### Structured Output
```python
response = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "List 3 steps to check backup status"}],
    response_format={"type": "json_object"}
)
```

---

## Model Selection for Development Tasks

| Task | Model | Why |
|------|-------|-----|
| General coding | codellama:13b | Code-specialized |
| Documentation | llama3.2:8b | Good writing quality |
| Quick responses | phi-3:3.8b | Fast, low memory |
| Embeddings | nomic-embed-text | Purpose-built for RAG |
| Complex reasoning | deepseek-r1:8b | Strong reasoning chain |

---

## Related Skills

- **llm-hosting** - Model management and resource monitoring
- **ai-gateway** - API gateway configuration
- **github-actions** - CI/CD for AI applications


# RepoWhisperer – Agentic Multi-Modal RAG Platform

An enterprise-grade **Agentic RAG (Retrieval-Augmented Generation)** platform built with **LangGraph**, **FastAPI**, **Supabase**, **AWS S3**, **Redis**, and **OpenAI**.

RepoWhisperer allows users to:

- Upload documents and repositories
- Ingest PDFs, DOCX, PPTX, Markdown, TXT, and Websites
- Perform hybrid semantic retrieval
- Use multi-agent orchestration with LangGraph
- Stream contextual AI responses in real-time
- Analyze codebases and project knowledge
- Maintain conversational memory with citations

---

# 🚀 Features

## Core Features

- 📄 Multi-format document ingestion
- 🌐 Website crawling & ingestion
- 🧠 Agentic RAG workflows
- 🔍 Hybrid search (Vector + Keyword)
- ⚡ Multi-query retrieval optimization
- 🤖 LangGraph Supervisor Agents
- 🛡️ Input Guardrails
- 📦 Chunk summarization & embeddings
- 📡 Server-Sent Event (SSE) streaming
- ☁️ AWS S3 document storage
- 🗄️ PostgreSQL + pgvector via Supabase
- 🧵 Async ingestion with Celery + Redis
- 📚 Citation-aware responses
- 🧾 Context-aware chat history

---

# 🏗️ System Architecture

## High-Level Architecture

```text
                    ┌──────────────────────────┐
                    │        Frontend          │
                    │ React / Angular / Next   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │        FastAPI API       │
                    │  Authentication + RAG    │
                    └────────────┬─────────────┘
                                 │
        ┌────────────────────────┼──────────────────────┐
        ▼                        ▼                      ▼
┌──────────────┐      ┌────────────────┐      ┌────────────────┐
│ AWS S3       │      │ Redis Queue    │      │ Supabase DB    │
│ Document     │      │ Celery Tasks   │      │ pgvector       │
│ Storage      │      │ Async Workers  │      │ Metadata       │
└──────┬───────┘      └────────┬───────┘      └────────┬───────┘
       │                        │                        │
       ▼                        ▼                        ▼
┌───────────────────────────────────────────────────────────────┐
│                    LangGraph Agent Layer                     │
│                                                               │
│  Supervisor Agent  ─────► RAG Agent                          │
│           │                    │                              │
│           └──────────────► Web Search Agent                  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │       OpenAI Models      │
                    │ GPT-4o / Embeddings API  │
                    └──────────────────────────┘
```

---

# 📂 Complete Project Flow

## 1. Upload Flow

### Step-by-Step Lifecycle

1. User uploads a document
2. Frontend requests a presigned upload URL
3. Backend generates S3 presigned URL
4. Frontend uploads directly to AWS S3
5. Backend confirms upload
6. Backend queues ingestion task
7. Celery worker starts processing
8. File is partitioned into atomic elements
9. Chunks are generated
10. AI summaries are created
11. Embeddings are generated
12. Data stored into Supabase
13. User starts querying
14. Retrieval pipeline executes
15. LangGraph agents synthesize response
16. SSE stream sends tokens back to frontend

---

# 📥 Ingestion Pipeline

## Supported Sources

### File Types

- PDF
- DOCX
- PPTX
- TXT
- Markdown
- HTML

### Website Sources

- Website crawling using ScrapingBee

---

## Ingestion Architecture

```text
Document / Website
        │
        ▼
Unstructured Partitioning
        │
        ▼
Atomic Elements
(Text / Tables / Images / Headers)
        │
        ▼
Chunking By Title
        │
        ▼
AI Summarization
        │
        ▼
Embeddings Generation
        │
        ▼
Supabase + pgvector Storage
```

---

# 🔍 Retrieval Pipeline

The retrieval system uses an advanced **Multi-Query Hybrid Search** architecture.

## Retrieval Strategy

### Query Expansion

The LLM generates multiple semantic variants of the user query.

Example:

```text
User Query:
"Explain transformer attention"

Generated Queries:
- What is transformer attention?
- How does self-attention work?
- Attention mechanism in transformers
```

---

## Hybrid Search

Each generated query performs:

- Vector similarity search
- Keyword search

Results are merged using:

## Reciprocal Rank Fusion (RRF)

This improves:

- Recall
- Semantic matching
- Keyword precision

---

## Retrieval Flow

```text
User Query
     │
     ▼
Generate Multiple Queries
     │
     ▼
Hybrid Retrieval
(Vector + Keyword)
     │
     ▼
Reciprocal Rank Fusion
     │
     ▼
Final Context
     │
     ▼
Generation Pipeline
```

---

# 🤖 Agent Architecture

RepoWhisperer supports two agent modes:

---

# 1. Simple RAG Agent

A single-agent architecture using LangGraph.

## Responsibilities

- Always call RAG tool
- Retrieve project-specific context
- Answer only using retrieved documents
- Maintain citations

## Flow

```text
START
  │
  ▼
Guardrail Validation
  │
  ▼
RAG Tool Invocation
  │
  ▼
LLM Response Generation
  │
  ▼
END
```

---

# 2. Supervisor Multi-Agent Architecture

Advanced orchestration using LangGraph Supervisor patterns.

## Agents

### Supervisor Agent

Coordinates specialized agents.

### RAG Agent

Handles internal project knowledge.

### Web Search Agent

Handles external internet knowledge.

---

## Supervisor Routing Logic

| Query Type | Routed To |
|---|---|
| Project Docs | RAG Agent |
| Internal Architecture | RAG Agent |
| Current News | Web Agent |
| Mixed Query | Both Agents |

---

## Multi-Agent Flow

```text
User Query
    │
    ▼
Supervisor Agent
    │
 ┌──┴─────────────┐
 ▼                ▼
RAG Agent     Web Agent
 │                │
 └──────┬─────────┘
        ▼
Response Synthesis
        ▼
Streaming Response
```

---

# 🛡️ Guardrails System

The platform contains AI safety validation before execution.

## Checks Performed

### Toxicity Detection

Detect harmful or abusive prompts.

### Prompt Injection Detection

Prevent system prompt manipulation.

### PII Detection

Detect:
- Emails
- Phone numbers
- Sensitive data

---

## Guardrail Flow

```python
Input → Validation → Safe? → Continue / Reject
```

---

# 🧠 Chunking Strategy

Uses `unstructured.chunking.title.chunk_by_title`.

## Strategy

- Preserve semantic sections
- Maintain title hierarchy
- Merge small chunks
- Limit max chunk size

## Configuration

```python
max_characters = 3000
new_after_n_chars = 2400
combine_text_under_n_chars = 500
```

---

# 📊 Multi-Modal Processing

The ingestion engine supports:

| Content Type | Processing |
|---|---|
| Text | Embeddings |
| Tables | HTML + AI Summary |
| Images | Base64 + Vision Summary |

---

# 📡 Streaming Architecture

Uses **Server-Sent Events (SSE)**.

## Benefits

- Real-time token streaming
- Better UX
- Progressive rendering
- Lower latency perception

---

# 🗄️ Database Design

## Core Tables

### projects

Stores projects.

### project_documents

Stores uploaded files metadata.

### document_chunks

Stores vectorized chunks.

### chats

Stores chat sessions.

### messages

Stores chat history.

### project_settings

Stores retrieval configurations.

---

# ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| Agent Framework | LangGraph |
| LLM Framework | LangChain |
| Queue | Redis |
| Worker | Celery |
| Vector DB | Supabase pgvector |
| Storage | AWS S3 |
| Auth | Clerk |
| Crawling | ScrapingBee |
| Embeddings | OpenAI |
| LLM | GPT-4o |
| Parsing | Unstructured |

---

# 🔧 Environment Variables

```env
SUPABASE_API_URL=
SUPABASE_SECRET_KEY=

CLERK_SECRET_KEY=
DOMAIN=

S3_BUCKET_NAME=
AWS_REGION=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=

REDIS_URL=

OPENAI_API_KEY=

SCRAPINGBEE_API_KEY=

TAVILY_API_KEY=
```

---

# 📁 Folder Structure

```text
src/
│
├── agents/
│   ├── simple_agent/
│   └── supervisor_agent/
│
├── rag/
│   ├── ingestion/
│   ├── retrieval/
│   └── generation/
│
├── routes/
│
├── services/
│
├── middleware/
│
├── config/
│
└── models/
```

---

# 🔍 Retrieval Optimization Techniques

## Multi-Query Retrieval

Improves recall using generated semantic variations.

## Hybrid Search

Combines:
- Dense vector search
- Sparse keyword retrieval

## Reciprocal Rank Fusion

Ranks documents using combined scoring.

## Reranking

Optional reranking layer for precision improvement.

---

# 📈 Scalability Design

## Horizontal Scaling

### Stateless FastAPI APIs

Can scale independently.

### Celery Workers

Add workers dynamically.

### Redis Queue

Supports distributed task execution.

### S3 Storage

Infinite scalable storage.

### Supabase pgvector

Scalable vector search.

---

# 🔐 Authentication

Authentication is implemented using Clerk.

## Features

- JWT authentication
- User-scoped projects
- User-scoped chats
- Secure APIs

---

# 🧪 Example Query Flow

## User Query

```text
"Explain the architecture of the ingestion pipeline"
```

---

## Execution

1. Supervisor receives query
2. Routes to RAG Agent
3. RAG Agent invokes retrieval
4. Hybrid search retrieves chunks
5. Relevant chunks fused
6. GPT-4o generates response
7. Citations attached
8. SSE streams response

---

# 📦 AI Summarization Strategy

Tables and images are summarized separately using GPT models.

## Why?

This improves:
- Searchability
- Semantic indexing
- Retrieval relevance

---

# 🖼️ Image Processing

Images are extracted as Base64 payloads.

Vision-capable models generate:
- Descriptions
- Visual insights
- Searchable summaries

---

# 🧠 Embedding Pipeline

## Model

```text
text-embedding-3-large
```

## Batch Processing

Embeddings generated in batches to:
- Avoid API limits
- Improve throughput
- Reduce latency

---

# ⚡ Async Processing

Celery workers process ingestion asynchronously.

## Benefits

- Non-blocking uploads
- Parallel ingestion
- Retry handling
- Scalable architecture

---

# 🧩 LangGraph Design

LangGraph is used for:

- State management
- Tool orchestration
- Multi-agent coordination
- Guardrail routing
- Citation accumulation

---

# 🧠 Why LangGraph?

## Advantages

- Deterministic workflows
- Stateful agents
- Tool routing
- Multi-agent systems
- Streaming support
- Human-in-the-loop support

---

# 📚 Citation Tracking

Custom state accumulates citations across tool calls.

```python
citations: Annotated[List[Dict[str, Any]], lambda x, y: x + y]
```

---

# 🔄 End-to-End Flow Summary

```text
Upload File
    │
    ▼
Store in S3
    │
    ▼
Queue Task
    │
    ▼
Partition Document
    │
    ▼
Chunking
    │
    ▼
AI Summaries
    │
    ▼
Embeddings
    │
    ▼
Store in Supabase
    │
    ▼
User Query
    │
    ▼
Hybrid Retrieval
    │
    ▼
LangGraph Agents
    │
    ▼
Streaming Response
```

---

# 🚀 Future Enhancements

## Planned Features

- Repository code graphing
- Autonomous code agents
- PR review agents
- Code execution sandbox
- Knowledge graph retrieval
- MCP integration
- Deep research workflows
- Semantic caching
- Observability dashboards

---

# 📊 Observability

Structured logging middleware includes:

- Request IDs
- Project IDs
- User IDs
- Timing metrics
- Failure tracking

---

# 🏁 Production Readiness

## Enterprise Features

- Async architecture
- Retry mechanisms
- Streaming responses
- Multi-agent orchestration
- Safety guardrails
- Scalable infrastructure
- Context-aware retrieval

---

# 🧑‍💻 Local Development

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn src.main:app --reload
```

---

## Run Celery Worker

```bash
celery -A src.worker worker --loglevel=info
```

---

# 📜 License

MIT License

---

# 🙌 Credits

Built using:

- LangGraph
- LangChain
- FastAPI
- OpenAI
- Supabase
- Celery
- Redis
- AWS
- Unstructured

---

# ⭐ Final Notes

RepoWhisperer demonstrates a modern production-grade implementation of:

- Agentic AI
- Retrieval-Augmented Generation
- Multi-agent orchestration
- Hybrid retrieval systems
- Streaming AI UX
- Multi-modal document intelligence

This architecture is highly scalable and suitable for:

- Enterprise knowledge systems
- AI copilots
- Repository intelligence
- Internal documentation search
- Research assistants
- AI developer tools

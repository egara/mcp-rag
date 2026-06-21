# MCP RAG Server

An independent Model Context Protocol (MCP) server that exposes a `search_documents` tool. This server connects to a PostgreSQL database (pgvector) to perform semantic retrieval. It fetches relevant document snippets and returns the raw context directly to the calling Agent/LLM (e.g., OpenWebUI), so the client's LLM can perform the final synthesis.

Built with Python, FastAPI, and the official MCP SDK.

## Project Structure
```
mcp-rag/
├── Dockerfile          # Hardened Alpine-based Docker image
├── README.md
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── src/
    ├── config.py       # Pydantic settings
    ├── rag.py          # Similarity search and retrieval logic
    └── server.py       # FastAPI MCP server definition
```

## Setup & Configuration

1. Copy `.env.example` to `.env` and fill in your PostgreSQL connection details:
   ```bash
   cp .env.example .env
   ```

2. Make sure your `POSTGRES_HOST` is accessible from the container.

## Running with Docker

This project provides a hardened Alpine-based Dockerfile.

1. Build the image:
   ```bash
   docker build -t mcp-rag-server .
   ```

2. Run the container:
   ```bash
   docker run -d \
     --name mcp-rag \
     --env-file .env \
     -p 8000:8000 \
     mcp-rag-server
   ```

The MCP Server will be accessible at `http://localhost:8000/mcp`. You can configure your MCP-compatible clients (like OpenWebUI) to connect via SSE to this endpoint.

## Available MCP Tools

- `search_documents(question: str, top_k: int = 5) -> str`
  Executes a similarity search against the pgvector store and returns the raw text snippets and their citations. Does NOT perform LLM synthesis natively.

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from mcp.server.fastapi import create_mcp_server
from mcp.server.models import InitializationOptions
from mcp.server import Server

from src.rag import query_documents

# Initialize the MCP server
server = Server("mcp-rag")

@server.tool()
async def search_documents(question: str, top_k: int = 5) -> str:
    """
    Search the local PostgreSQL pgvector database for documents relevant to the question.
    Returns raw text snippets that should be used by the calling LLM to answer the user's question.
    
    Args:
        question: The search query to find relevant documents.
        top_k: Number of document chunks to retrieve (default 5).
    """
    sources = query_documents(question, top_k)
    
    if not sources:
        return "No relevant documents found in the database."
        
    result_text = "Retrieved Context:\n\n"
    for i, src in enumerate(sources, 1):
        result_text += f"--- Document {i} (Source: {src['source']}, Page: {src['page']}) ---\n"
        result_text += f"{src['content']}\n\n"
    
    return result_text

# Create FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan, title="MCP RAG Server")

# Bind MCP to FastAPI (SSE transport)
mcp_app = create_mcp_server(server, InitializationOptions(
    server_name="mcp-rag",
    server_version="0.1.0",
    capabilities=server.get_capabilities()
))
app.mount("/mcp", mcp_app)

if __name__ == "__main__":
    uvicorn.run("src.server:app", host="0.0.0.0", port=8000, reload=False)

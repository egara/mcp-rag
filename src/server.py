from fastmcp import FastMCP
from loguru import logger

from src.rag import query_documents

# Initialize the FastMCP server
mcp = FastMCP("mcp-rag")


@mcp.tool()
async def search_documents(question: str, top_k: int = 5) -> str:
    """Searches the local PostgreSQL pgvector database for documents relevant to the question.

    Returns raw text snippets that should be used by the calling LLM to answer the user's question.

    Args:
        question (str): The search query to find relevant documents.
        top_k (int, optional): Number of document chunks to retrieve. Defaults to 5.

    Returns:
        str: A formatted string containing the retrieved context, or a message indicating
            that no documents were found.
    """
    logger.info(f"New query received: '{question}'")

    try:
        sources = query_documents(question, top_k)

        if not sources:
            logger.warning("No relevant documents found in the database.")
            return "No relevant documents found in the database."

        logger.success(
            f"Se han recuperado {len(sources)} documentos de la base de datos."
        )

        result_text = "Retrieved Context:\n\n"
        for i, src in enumerate(sources, 1):
            result_text += (
                f"--- Document {i} (Source: {src['source']}, Page: {src['page']}) ---\n"
            )
            result_text += f"{src['content']}\n\n"

        return result_text
    except Exception:
        logger.exception("Error searching on PostgreSQL")
        return "Error searching on RAG."


if __name__ == "__main__":
    # You can run this server via http for OpenWebUI compatibility
    mcp.run(transport="http", host="0.0.0.0", port=8000)

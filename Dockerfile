# Use a slim Debian base image (Alpine doesn't support PyTorch wheels)
FROM python:3.11-slim

# Set environment variables to avoid python writing .pyc files and running unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user and group
RUN groupadd -r mcpuser && useradd -r -g mcpuser mcpuser

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src/

# Change ownership of the app directory to the non-root user
RUN chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# Expose the FastAPI port
EXPOSE 8000

# Run the FastMCP server directly
CMD ["python", "-m", "src.server"]

# Use a hardened Alpine base image
FROM python:3.11-alpine3.19

# Set environment variables to avoid python writing .pyc files and running unbuffered
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a non-root user and group
RUN addgroup -S mcpuser && adduser -S mcpuser -G mcpuser

# Set working directory
WORKDIR /app

# Install system dependencies needed for compiling python packages like psycopg2
RUN apk add --no-cache gcc musl-dev postgresql-dev

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

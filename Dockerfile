# Multi-stage build for smaller final image
FROM python:3.12-slim as builder

WORKDIR /app

# Install system dependencies needed for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv and dependencies
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache .

# Final stage - minimal runtime image
FROM python:3.12-slim

WORKDIR /app

# Copy only the installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy only necessary application files
COPY server/ ./server/
COPY main.py ./

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
ENV MCP_SERVER_PORT=8000
EXPOSE ${MCP_SERVER_PORT}

# Run the application
CMD ["python", "main.py"] 
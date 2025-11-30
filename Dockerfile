# Use official Python 3.12 slim image
FROM python:3.12-slim

# Install uv using the official installer
RUN pip install --no-cache-dir uv

# Set working directory
WORKDIR /app

# Copy only dependency files first (caching)
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-cache

# Now copy source code
COPY src/ src/

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Default command
CMD ["uv", "run", "src/vending_sim.py"]
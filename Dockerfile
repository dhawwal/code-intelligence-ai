# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYO3_USE_ABI3_FORWARD_COMPATIBILITY 1

# Set work directory
WORKDIR /app

# Install system dependencies (needed for git and tree-sitter builds)
RUN apt-get update && apt-get install -y \
    git \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create storage directory and set permissions
RUN mkdir -p storage && chmod -R 777 storage

# Expose the port Hugging Face Spaces expects
EXPOSE 7860

# Run the application with gunicorn
# Use eventlet worker for SocketIO support if needed, or sync for simplicity
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "--workers", "1", "--threads", "8", "--timeout", "0", "app:app"]

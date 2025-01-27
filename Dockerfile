# Stage 1: Build Stage
FROM python:3.12-slim AS builder

# Set environment variables to prevent Python from writing .pyc files and to enable buffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements.txt file to the working directory
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --user -r requirements.txt

# Stage 2: Production Stage
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy only the necessary system dependencies (if any)
# If your application requires additional system packages, install them here
# RUN apt-get update && apt-get install -y --no-install-recommends <packages> && rm -rf /var/lib/apt/lists/*

# Copy the Python dependencies from the builder stage
COPY --from=builder /root/.local /root/.local

# Update PATH to include the directory with the installed packages
ENV PATH=/root/.local/bin:$PATH

# Copy the application code
COPY backend/ ./backend/

# Expose port 8000 to allow communication to/from the server
EXPOSE 8000

# Define the default command to run the application using Uvicorn
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    pkg-config \
    libopencv-dev \
    libboost-all-dev \
    libgtk-3-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libblas-dev \
    python3-dev \
    libtbb12 \
    libtbb-dev \
    libopenexr-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer1.0-dev \
    ffmpeg \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install wheel
RUN pip install --upgrade pip setuptools wheel

# Copy Docker-optimized requirements first for better caching
COPY requirements-docker.txt .

# Install Python dependencies with better error handling
RUN pip install --no-cache-dir --timeout=1000 -r requirements-docker.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p static_files/uploads static_files/temp models/face_detection models/blink_detection models/audio_deepfake

# Set environment variables for production
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV HOST=0.0.0.0
ENV PORT=5000
ENV USE_LITE_VERSION=true

# Expose port
EXPOSE 5000

# Run the application using the lite version for Docker
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--timeout", "120", "wsgi_lite:app"]
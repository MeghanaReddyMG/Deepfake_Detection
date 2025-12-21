# 🔧 FalsifyX Deployment Troubleshooting Guide

## 🚨 Common Deployment Errors & Solutions

### 1. **Linux: Missing System Dependencies (libatlas-base-dev/libtbb2)**

**Error:**
```
Package libatlas-base-dev is not available
Package libtbb2 is not available
```

**Quick Fix:**
```bash
sudo apt-get update
sudo apt-get install -y libatlas3-base libatlas-base-dev libtbbmalloc2 libtbb-dev
# Then: pip install -r requirements.txt
```

### 2. **Vercel: dlib-bin Compatibility Error**

**Error:**
```
× No solution found when resolving dependencies:
╰─▶ Because dlib-bin==19.24.2 has no wheels with a matching Python version
```

**Solution:**
Use the lightweight Vercel configuration:

```bash
# Deploy with lightweight version
vercel --prod

# Or manually specify requirements
pip install -r requirements-vercel.txt
```

**Files to use for Vercel:**
- `requirements-vercel.txt` (lightweight dependencies)
- `wsgi_lite.py` (serverless entry point)
- `vercel.json` (Vercel configuration)

### 3. **Heroku: Slug Size Too Large**

**Error:**
```
Compiled slug size: 1.2G is too large (max is 500M)
```

**Solution:**
```bash
# Use buildpacks for ML dependencies
heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-apt

# Create .heroku/python-version
echo "python-3.11.7" > .heroku/python-version

# Optimize requirements.txt
pip install --no-deps -r requirements.txt
```

### 4. **Docker: Image Size Too Large (>4GB)**

**Error:**
```
Image of size 4.0 GB exceeded limit of 4.0 GB
Upgrade your plan to increase the image size limit
```

**Solution - Ultra-Minimal Build (Recommended for size limits):**
```bash
# Use minimal Dockerfile (Alpine-based, <1GB final size)
docker build -f Dockerfile.minimal -t falsifyx .

# Or optimized multi-stage build (~1.5GB final size)
docker build -f Dockerfile.multistage -t falsifyx .
```

**Size Optimization Strategies:**

1. **Use Alpine Linux base** (`Dockerfile.minimal`):
   - Alpine packages are 5-10x smaller than Debian
   - Final image: <1GB vs 4GB

2. **Exclude heavy dependencies**:
   - No TensorFlow, OpenCV, or ML libraries
   - No audio processing libraries
   - No development tools

3. **Multi-stage build optimizations**:
   - Separate build and runtime stages
   - Remove build tools from final image
   - Clean up package caches and temp files

4. **Use .dockerignore**:
   - Excludes models, training data, docs
   - Reduces build context from ~2GB to ~50MB

**Package Size Comparison:**
```
Standard build:     4.0GB (all ML libraries)
Docker-optimized:   2.5GB (tensorflow-cpu)
Multi-stage:        1.5GB (optimized runtime)
Minimal Alpine:     <1GB (basic functionality only)
```

**For production deployment with size limits:**
```bash
# Build minimal version
docker build -f Dockerfile.minimal -t falsifyx .

# Verify size
docker images falsifyx

# Should show <1GB instead of 4GB
```

### 5. **Docker: Python Package Installation Failed**

**Error:**
```
RUN pip install --no-cache-dir -r requirements.txt
ERROR: failed to build: process did not complete successfully: exit code: 1
```

**Solution:**
Use Docker-optimized requirements:

```bash
# Use minimal requirements (no ML libraries)
docker build -f Dockerfile.minimal -t falsifyx .

# Or Docker-optimized requirements (with tensorflow-cpu)
docker build -f Dockerfile.multistage -t falsifyx .
```

**Package Installation Strategies:**
- `requirements-minimal.txt` - Basic web app only (~50MB packages)
- `requirements-docker.txt` - Includes tensorflow-cpu (~1.5GB packages)
- `requirements.txt` - Full ML stack (~3GB+ packages)

### 6. **Railway: Memory Limit Exceeded**

**Error:**
```
Process killed due to memory limit (512MB)
Image size exceeded limit
```

**Solution:**
```bash
# Use minimal Docker build for Railway
# railway.toml is configured to use Dockerfile.minimal

# Verify Railway deployment settings:
# - Uses Dockerfile.minimal (<1GB image)
# - Sets MINIMAL_MODE=true
# - Uses wsgi_lite.py entry point
# - Single worker configuration

# Railway deployment commands:
git push origin main  # Auto-deploys
# Or: railway deploy (with Railway CLI)
```

**Railway Optimization:**
- **Image size**: <1GB (well under Railway's 4GB limit)
- **Memory usage**: ~200MB (under Railway's 512MB default)
- **Startup time**: <30 seconds (Railway timeout: 60s)
- **Auto-scaling**: Handles traffic spikes automatically

### 7. **Local: Import Errors**

**Error:**
```
ModuleNotFoundError: No module named 'cv2'
```

**Solution:**
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# If still failing, install individually
pip install opencv-python-headless
pip install dlib
```

## 🎯 Platform-Specific Solutions

### **Vercel Deployment**

1. **Use Lightweight Version:**
```json
// vercel.json
{
  "installCommand": "pip install -r requirements-vercel.txt",
  "builds": [{"src": "wsgi_lite.py", "use": "@vercel/python"}]
}
```

2. **Environment Variables:**
```bash
vercel env add FLASK_ENV production
vercel env add FLASK_DEBUG False
vercel env add USE_LITE_VERSION true
```

### **Heroku Deployment**

1. **Buildpack Configuration:**
```bash
heroku buildpacks:clear
heroku buildpacks:add heroku/python
```

2. **Procfile:**
```
web: gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120
```

3. **Runtime:**
```
python-3.11.7
```

### **Docker Deployment**

1. **Build with System Dependencies:**
```bash
docker build -t falsifyx .
docker run -p 5000:5000 falsifyx
```

2. **Docker Compose:**
```bash
docker-compose up -d
```

### **Railway Deployment**

1. **Environment Variables:**
```
FLASK_ENV=production
PYTHONPATH=/app
PORT=5000
```

2. **Start Command:**
```bash
gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

## 🔍 Debugging Steps

### 1. **Check Python Version**
```bash
python --version  # Should be 3.8+
```

### 2. **Verify Dependencies**
```bash
pip list | grep -E "(flask|opencv|dlib|tensorflow)"
```

### 3. **Test Import**
```python
# Test critical imports
try:
    import flask
    import numpy
    import PIL
    print("✅ Core dependencies OK")
except ImportError as e:
    print(f"❌ Import error: {e}")
```

### 4. **Check Memory Usage**
```bash
# Monitor memory during startup
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')
"
```

### 5. **Test Endpoints**
```bash
# Health check
curl http://localhost:5000/health

# Test upload (with file)
curl -X POST -F "file=@test.jpg" http://localhost:5000/upload
```

## 📊 Performance Optimization

### **Memory Optimization**
```python
# In config.py
import gc
import os

# Enable garbage collection
gc.enable()

# Limit TensorFlow memory growth
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
```

### **Cold Start Optimization**
```python
# Lazy loading for heavy imports
def get_model():
    global _model
    if '_model' not in globals():
        import tensorflow as tf
        _model = tf.keras.models.load_model('model.h5')
    return _model
```

### **Caching Strategy**
```python
# Use functools.lru_cache for expensive operations
from functools import lru_cache

@lru_cache(maxsize=100)
def analyze_file_hash(file_hash):
    # Expensive analysis here
    pass
```

## 🛠️ Environment-Specific Fixes

### **Windows**
```bash
# Install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Use conda for problematic packages
conda install opencv dlib
```

### **macOS**
```bash
# Install Homebrew dependencies
brew install cmake boost opencv

# Install Python packages
pip install dlib --verbose
```

### **Linux (Ubuntu/Debian)**
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    python3-dev \
    libopencv-dev \
    cmake \
    build-essential

# Install Python packages
pip install -r requirements.txt
```

### **Linux: Missing libatlas-base-dev / libtbb2 Error**

**Error:**
```
Package libatlas-base-dev is not available, but is referred to by another package.
Package libtbb2 is not available, but is referred to by another package.
However the following packages replace it: libtbbmalloc2
```

**Solution:**
```bash
# Update package lists
sudo apt-get update

# Install replacement packages
sudo apt-get install -y \
    libatlas3-base \
    libatlas-base-dev \
    libtbbmalloc2 \
    libtbb-dev \
    liblapack-dev \
    libblas-dev \
    gfortran

# Alternative: Install OpenBLAS instead of ATLAS
sudo apt-get install -y \
    libopenblas-dev \
    liblapack-dev

# For newer Ubuntu versions (20.04+), use:
sudo apt-get install -y \
    libtbb2 \
    libtbb-dev

# If packages still not found, enable universe repository
sudo add-apt-repository universe
sudo apt-get update
sudo apt-get install -y libatlas-base-dev libtbb2

# Install OpenCV system dependencies
sudo apt-get install -y \
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
    libdc1394-22-dev

# Then install Python packages
pip install -r requirements.txt
```

## 🔄 Rollback Strategies

### **Quick Rollback**
```bash
# Revert to previous working commit
git log --oneline -5
git reset --hard <previous-commit-hash>
git push --force-with-lease origin main
```

### **Environment Rollback**
```bash
# Use previous requirements
git checkout HEAD~1 -- requirements.txt
pip install -r requirements.txt
```

### **Platform Rollback**
```bash
# Heroku
heroku releases:rollback v123

# Vercel
vercel --prod --force

# Docker
docker run previous-image-tag
```

## 📞 Getting Help

### **Check Logs**
```bash
# Heroku
heroku logs --tail

# Vercel
vercel logs

# Docker
docker logs container-name

# Local
tail -f app.log
```

### **Debug Mode**
```bash
# Enable debug logging
export FLASK_DEBUG=True
export FLASK_ENV=development
python app/main.py
```

### **Test Minimal Setup**
```python
# minimal_test.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "FalsifyX is working!"

if __name__ == '__main__':
    app.run(debug=True)
```

## 🎯 Quick Fix Commands

```bash
# Fix most common issues
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
python -c "import flask, numpy, PIL; print('Dependencies OK')"

# Reset environment
rm -rf .venv
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Test deployment locally
export FLASK_ENV=production
gunicorn wsgi:app --bind 127.0.0.1:5000

# Docker build commands
docker build -t falsifyx .                    # Standard build
docker build -f Dockerfile.multistage -t falsifyx .  # Multi-stage build
docker run -p 5000:5000 falsifyx             # Run container
```

---

**If issues persist, check the [GitHub Issues](https://github.com/sanjanashivshankar07/falsifyx/issues) or create a new issue with:**
- Platform (Vercel, Heroku, Docker, etc.)
- Error message (full traceback)
- Python version
- Operating system
- Steps to reproduce
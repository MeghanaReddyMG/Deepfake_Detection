# 🚀 FalsifyX Deployment Guide

This guide covers various deployment options for the FalsifyX deepfake detection system.

## 📋 Prerequisites

- Python 3.8+ (recommended: 3.11)
- Git
- Docker (optional, for containerized deployment)
- At least 4GB RAM (8GB+ recommended for ML models)
- 10GB+ disk space

## 🔧 Environment Setup

### 1. Clone Repository
```bash
git clone https://github.com/sanjanashivshankar07/falsifyx.git
cd falsifyx
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configuration
nano .env
```

## 🐳 Docker Deployment (Recommended)

### Quick Start with Docker Compose
```bash
# Build and start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### Manual Docker Build
```bash
# Build the image
docker build -t falsifyx .

# Run the container
docker run -d \
  --name falsifyx \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  -v $(pwd)/static_files:/app/static_files \
  -v $(pwd)/models:/app/models \
  falsifyx
```

## 🖥️ Local Development Deployment

### 1. Virtual Environment Setup
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
# Development mode
python app/main.py

# Production mode with Gunicorn
gunicorn wsgi:app --bind 0.0.0.0:5000 --workers 1 --timeout 120
```

## ☁️ Cloud Platform Deployment

### Heroku Deployment

1. **Install Heroku CLI**
```bash
# Install from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Deploy to Heroku**
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-falsifyx-app

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-super-secret-key
heroku config:set FLASK_DEBUG=False

# Deploy
git push heroku main

# Open application
heroku open
```

### Vercel Deployment (Serverless)

1. **Install Vercel CLI**
```bash
npm install -g vercel
```

2. **Deploy to Vercel**
```bash
# Login to Vercel
vercel login

# Deploy (uses vercel.json configuration)
vercel --prod

# Or connect GitHub repository via Vercel dashboard
```

**Note:** Vercel deployment uses lightweight version (`wsgi_lite.py`) with mock ML analysis for demo purposes due to serverless limitations.

### Railway Deployment

1. **Connect GitHub Repository**
   - Go to [Railway.app](https://railway.app)
   - Connect your GitHub account
   - Select the falsifyx repository

2. **Configure Environment Variables**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   FLASK_DEBUG=False
   ```

3. **Deploy automatically via Git push**

### DigitalOcean App Platform

1. **Create App**
   - Go to DigitalOcean App Platform
   - Connect GitHub repository
   - Select falsifyx repository

2. **Configure Build Settings**
   ```yaml
   name: falsifyx
   services:
   - name: web
     source_dir: /
     github:
       repo: sanjanashivshankar07/falsifyx
       branch: main
     run_command: gunicorn wsgi:app
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: FLASK_ENV
       value: production
     - key: SECRET_KEY
       value: your-secret-key
   ```

## 🔒 Production Security Checklist

### Environment Variables
- [ ] Set strong `SECRET_KEY`
- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=False`
- [ ] Configure proper upload directories

### Security Headers
```python
# Add to app/main.py
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

### File Upload Security
- [ ] Validate file types strictly
- [ ] Limit file sizes (current: 100MB)
- [ ] Scan uploaded files for malware
- [ ] Use secure file storage (cloud storage recommended)

## 📊 Performance Optimization

### 1. Model Loading Optimization
```python
# Implement model caching
# Use lazy loading for heavy ML models
# Consider model quantization for faster inference
```

### 2. Database Configuration
```python
# For production, replace in-memory storage with:
# - PostgreSQL for user data
# - Redis for session storage
# - MongoDB for analysis results
```

### 3. Caching Strategy
```python
# Implement Redis caching for:
# - Frequent analysis results
# - User sessions
# - Model predictions
```

## 🔍 Monitoring & Logging

### Application Monitoring
```python
# Add to requirements.txt
sentry-sdk[flask]==1.32.0

# Configure in app/main.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### Health Check Endpoint
```python
# Add to app/routes.py
@main_bp.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': time.time(),
        'version': '1.0.0'
    })
```

## 🚨 Troubleshooting Common Issues

### 1. Memory Issues
```bash
# Increase worker memory limit
gunicorn wsgi:app --max-requests 1000 --max-requests-jitter 100 --preload

# Use swap file on limited memory systems
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 2. Model Loading Errors
```bash
# Ensure model directories exist
mkdir -p models/face_detection models/blink_detection models/audio_deepfake

# Check file permissions
chmod -R 755 models/
```

### 3. File Upload Issues
```bash
# Check upload directory permissions
mkdir -p static_files/uploads static_files/temp
chmod -R 755 static_files/
```

### 4. Port Binding Issues
```bash
# Check if port is available
netstat -tulpn | grep :5000

# Use different port
export PORT=8000
gunicorn wsgi:app --bind 0.0.0.0:$PORT
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Use load balancer (nginx, HAProxy)
- Deploy multiple app instances
- Implement session storage (Redis)
- Use CDN for static assets

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize ML model inference
- Implement GPU acceleration for models

### Database Scaling
- Migrate from in-memory to persistent database
- Implement database connection pooling
- Use read replicas for analytics

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-falsifyx-app"
        heroku_email: "your-email@example.com"
```

## 📞 Support

For deployment issues:
1. Check the [Issues](https://github.com/sanjanashivshankar07/falsifyx/issues) page
2. Review application logs
3. Verify environment configuration
4. Test with minimal configuration first

## 🎯 Quick Deployment Commands

```bash
# Local development
python app/main.py

# Production with Gunicorn
gunicorn wsgi:app --bind 0.0.0.0:5000

# Docker deployment
docker-compose up -d

# Heroku deployment
git push heroku main
```

---

**FalsifyX is now ready for production deployment! 🚀**
#!/usr/bin/env python3
"""
Lightweight WSGI entry point for serverless deployment (Vercel)
Uses simplified routes without heavy ML dependencies
"""
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Try to use lightweight version first
try:
    from app.main_lite import create_app
    print("Using lightweight FalsifyX for serverless deployment")
except ImportError:
    # Fallback to full version
    from app.main import create_app
    print("Using full FalsifyX")

# Create the Flask application
application = create_app()
app = application

if __name__ == "__main__":
    app.run()
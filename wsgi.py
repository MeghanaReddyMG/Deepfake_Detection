#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app.main import create_app

# Create the Flask application
application = create_app()
app = application

if __name__ == "__main__":
    app.run()
#!/usr/bin/env python3
"""
Lightweight WSGI entry point for serverless deployment (Vercel)
Uses simplified routes without heavy ML dependencies
"""
import sys
import os

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

def create_fallback_app():
    """Create a minimal Flask app as fallback"""
    from flask import Flask, jsonify
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fallback-secret-key'
    
    @app.route('/')
    def index():
        return jsonify({
            'status': 'FalsifyX Lite - Fallback Mode',
            'message': 'Minimal deployment active'
        })
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'mode': 'fallback'})
    
    return app

# Try to use lightweight version first
try:
    from app.main_lite import create_app
    print("Using lightweight FalsifyX for serverless deployment")
    application = create_app()
except Exception as e:
    print(f"Error loading main_lite: {e}")
    try:
        # Fallback to full version
        from app.main import create_app
        print("Using full FalsifyX")
        application = create_app()
    except Exception as e2:
        print(f"Error loading main: {e2}")
        # Use minimal fallback
        print("Using fallback Flask app")
        application = create_fallback_app()

app = application

if __name__ == "__main__":
    app.run()
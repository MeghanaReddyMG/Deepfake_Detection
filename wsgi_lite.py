"""
WSGI entry point for production deployment (Railway, Heroku, etc.)
Lightweight version for serverless and containerized deployments
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the lite application
from app.main_lite import create_app

# Create the application instance
app = create_app()

# Configure for production
app.config['ENV'] = 'production'
app.config['DEBUG'] = False

# Railway and other platforms provide PORT via environment variable
# Gunicorn will handle the port binding, but we ensure it's available
port = int(os.environ.get('PORT', 5000))

# This is the WSGI application object that gunicorn will use
application = app

if __name__ == '__main__':
    # This won't be called in production (gunicorn handles it)
    # But useful for local testing
    host = os.environ.get('HOST', '0.0.0.0')
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(debug=debug_mode, host=host, port=port)
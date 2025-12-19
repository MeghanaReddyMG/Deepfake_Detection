"""
Lightweight version of main.py for serverless deployment
Uses simplified routes without heavy ML dependencies
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize config
    Config.init_app(app)
    
    # Use lightweight routes for serverless deployment
    try:
        from routes_lite import main_bp
        print("Using lightweight routes for serverless deployment")
    except ImportError:
        # Fallback to full routes if available
        from routes import main_bp
        print("Using full routes")
    
    # Register blueprints
    app.register_blueprint(main_bp)
    
    # Add health check endpoint
    @app.route('/health')
    def health_check():
        return {'status': 'healthy', 'service': 'FalsifyX', 'mode': 'lite'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    # Use environment variables for production
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '127.0.0.1')
    
    app.run(debug=debug_mode, host=host, port=port)
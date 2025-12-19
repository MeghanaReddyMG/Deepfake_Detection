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
    
    try:
        app.config.from_object(Config)
        # Initialize config safely for serverless
        try:
            Config.init_app(app)
        except Exception as e:
            print(f"Config initialization warning: {e}")
            # Continue without directory creation in serverless
    except Exception as e:
        print(f"Config loading error: {e}")
        # Set minimal config
        app.config['SECRET_KEY'] = 'fallback-secret-key'
    
    # Use lightweight routes for serverless deployment
    try:
        from app.routes_lite import main_bp
        print("Using lightweight routes for serverless deployment")
    except ImportError:
        # Fallback to full routes if available
        try:
            from app.routes import main_bp
            print("Using full routes")
        except ImportError:
            # Create a minimal blueprint if nothing else works
            from flask import Blueprint
            main_bp = Blueprint('main', __name__)
            
            @main_bp.route('/')
            def index():
                return {'status': 'FalsifyX Lite', 'message': 'Minimal deployment active'}
            
            print("Using minimal fallback routes")
    
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
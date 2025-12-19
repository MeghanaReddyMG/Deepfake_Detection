import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-change-in-production')
    
    # File handling
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'static_files', 'uploads'))
    TEMP_FOLDER = os.getenv('TEMP_FOLDER', os.path.join(BASE_DIR, 'static_files', 'temp'))
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'wav', 'mp3', 'webm', 'ogg'}
    MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 100 * 1024 * 1024))  # 100MB default
    
    # Environment
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    ENV = os.getenv('FLASK_ENV', 'development')
    
    # Authentication (remove in production, use proper database)
    USERS = {
        'admin': 'admin123',
        'user': 'demo123'
    }
    
    @staticmethod
    def init_app(app):
        """Initialize application with config"""
        try:
            # Only create directories if not in serverless environment
            if not os.environ.get('VERCEL') and not os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
                # Ensure upload directories exist
                os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
                os.makedirs(Config.TEMP_FOLDER, exist_ok=True)
        except Exception as e:
            print(f"Directory creation skipped in serverless environment: {e}")
    
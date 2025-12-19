import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-change-in-production')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static_files', 'uploads')
    TEMP_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static_files', 'temp')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'avi', 'mov', 'wav', 'mp3', 'webm', 'ogg'}
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB limit
    
    # Authentication
    USERS = {
        'admin': 'admin123',
        'user': 'demo123'
    }
    
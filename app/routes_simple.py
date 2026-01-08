"""
Simple routes for debugging
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os
import time
from config import Config
from functools import wraps

main_bp = Blueprint('main', __name__)

# Simple in-memory user storage
users = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    if not filename or "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in Config.ALLOWED_EXTENSIONS

@main_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    return render_template('index.html', username=session.get('username'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = request.form.get('remember_me')
        
        if hasattr(Config, 'USERS') and username in Config.USERS:
            if Config.USERS[username] == password:
                session['user_id'] = username
                session['username'] = username
                if remember_me:
                    session.permanent = True
                flash('Login successful!', 'success')
                return redirect(url_for('main.index'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username or not password:
            flash('Username and password are required', 'error')
        elif len(username) < 3:
            flash('Username must be at least 3 characters long', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        else:
            errors = []
            if len(password) < 8:
                errors.append("Password must be at least 8 characters long")
            if not any(char.isupper() for char in password):
                errors.append("Password must contain at least one uppercase letter (A-Z)")
            if not any(char.islower() for char in password):
                errors.append("Password must contain at least one lowercase letter (a-z)")
            if not any(char.isdigit() for char in password):
                errors.append("Password must contain at least one number (0-9)")
            special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            if not any(char in special_chars for char in password):
                errors.append("Password must contain at least one special character")
            
            if errors:
                for error in errors:
                    flash(error, 'error')
            elif username in users or (hasattr(Config, 'USERS') and username in Config.USERS):
                flash('Username already exists', 'error')
            else:
                users[username] = {
                    'password': generate_password_hash(password),
                    'created_at': time.time()
                }
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.login'))

@main_bp.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'FalsifyX Simple'})

@main_bp.route('/test')
def test_page():
    """Simple test page for debugging uploads"""
    return render_template('test_upload.html')

@main_bp.route('/simple')
def simple_test():
    """Very simple test page"""
    return render_template('simple_test.html')

@main_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    try:
        print("Upload request received")
        
        if 'file' not in request.files:
            print("Error: No file part in request")
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        print(f"File received: {file.filename}")
        
        if file.filename == '':
            print("Error: Empty filename")
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            print(f"Error: File type not allowed: {file.filename}")
            return jsonify({'error': 'Invalid file type'}), 400
        
        filename = secure_filename(file.filename)
        analysis_id = str(int(time.time() * 1000))
        
        # Simple fake detection - always return FAKE for testing
        results = [{
            'type': 'ai_detection',
            'is_ai_generated': True,
            'ai_generated': True,
            'is_fake': True,
            'confidence': 0.85,
            'generation_method': 'Test Detection',
            'artifacts_found': ['Test artifact'],
        }]
        
        results.append({
            'image_summary': {
                'filename': filename,
                'ai_generated_likelihood': 0.85,
                'detected_generation_method': 'Test Detection',
                'overall_authenticity': 'LIKELY_AI_GENERATED',
                'confidence_level': 'HIGH',
                'recommendation': 'This is a test - always detects as FAKE'
            }
        })
        
        print(f"Returning test results for {filename}")
        return jsonify({'results': results, 'analysis_id': analysis_id})
        
    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@main_bp.route('/test_upload', methods=['GET', 'POST'])
def test_upload():
    """Test endpoint without login requirement"""
    print("Test upload endpoint hit!")
    if request.method == 'POST':
        print(f"POST request received")
        print(f"Files: {request.files}")
        if 'file' in request.files:
            file = request.files['file']
            print(f"File received: {file.filename}")
            return jsonify({'status': 'success', 'filename': file.filename})
        return jsonify({'status': 'no file'})
    return jsonify({'status': 'test endpoint working', 'method': 'GET'})
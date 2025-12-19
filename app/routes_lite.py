"""
Lightweight version of routes for serverless deployment
Removes heavy ML dependencies for platforms like Vercel
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os
import time
import json
import hashlib
from config import Config
from functools import wraps
import random

main_bp = Blueprint('main', __name__)

# Simple in-memory user storage (in production, use a database)
users = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    """Simple file validation without python-magic"""
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
        
        # Check hardcoded users from config first
        if hasattr(Config, 'USERS') and username in Config.USERS:
            if Config.USERS[username] == password:
                session['user_id'] = username
                session['username'] = username
                return redirect(url_for('main.index'))
        
        # Check registered users
        if username in users and check_password_hash(users[username]['password'], password):
            session['user_id'] = username
            session['username'] = username
            return redirect(url_for('main.index'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if not username or not password:
            flash('Username and password are required')
        elif password != confirm_password:
            flash('Passwords do not match')
        elif username in users or (hasattr(Config, 'USERS') and username in Config.USERS):
            flash('Username already exists')
        else:
            users[username] = {
                'password': generate_password_hash(password),
                'created_at': time.time()
            }
            flash('Registration successful! Please login.')
            return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main_bp.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'FalsifyX Lite'})

@main_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Simulate analysis without heavy ML processing
        analysis_id = str(int(time.time() * 1000))
        
        # Mock results based on file type
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            results = mock_image_analysis(filename, analysis_id)
        elif filename.lower().endswith(('.mp4', '.avi', '.mov', '.webm')):
            results = mock_video_analysis(filename, analysis_id)
        elif filename.lower().endswith(('.mp3', '.wav', '.ogg')):
            results = mock_audio_analysis(filename, analysis_id)
        else:
            return jsonify({'error': 'Unsupported file type'}), 400
        
        return jsonify({'results': results, 'analysis_id': analysis_id})
    
    return jsonify({'error': 'Invalid file type'}), 400

def mock_image_analysis(filename, analysis_id):
    """Mock image analysis for demo purposes"""
    time.sleep(1)  # Simulate processing time
    
    num_faces = random.randint(1, 3)
    results = []
    
    for i in range(num_faces):
        is_fake = random.choice([True, False])
        confidence = random.uniform(0.6, 0.95)
        ai_generated = random.choice([True, False])
        
        results.append({
            'is_fake': is_fake,
            'confidence': confidence,
            'face_id': i + 1,
            'learned': False,
            'ai_generated': ai_generated,
            'ai_confidence': random.uniform(0.5, 0.9),
            'generation_method': random.choice(['GAN', 'Diffusion', 'StyleGAN', 'DALL-E', 'Unknown'])
        })
    
    # Add summary
    results.append({
        'image_summary': {
            'faces_detected': num_faces,
            'ai_generated_likelihood': random.uniform(0.2, 0.9),
            'detected_generation_method': random.choice(['GAN', 'Diffusion', 'StyleGAN', 'DALL-E', 'Unknown']),
            'overall_authenticity': random.choice(['SUSPICIOUS', 'LIKELY_AUTHENTIC'])
        }
    })
    
    return results

def mock_video_analysis(filename, analysis_id):
    """Mock video analysis for demo purposes"""
    time.sleep(2)  # Simulate processing time
    
    num_frames = random.randint(8, 15)
    results = []
    
    for frame_num in range(1, num_frames + 1):
        frame_result = {
            'frame': frame_num * 5,
            'face': [],
            'ai_generated': {
                'is_ai_generated': random.choice([True, False]),
                'ai_confidence': random.uniform(0.5, 0.9),
                'generation_method': random.choice(['GAN', 'Diffusion', 'VAE', 'Unknown'])
            },
            'temporal_analysis': {
                'motion_consistency': random.uniform(0.3, 0.9),
                'temporal_smoothness': random.uniform(0.4, 0.9)
            }
        }
        
        # Add face data
        num_faces = random.randint(0, 2)
        for face_id in range(num_faces):
            face_result = {
                'is_fake': random.choice([True, False]),
                'confidence': random.uniform(0.6, 0.9),
                'face_id': face_id + 1,
                'learned': False,
                'ai_generated': random.choice([True, False])
            }
            frame_result['face'].append(face_result)
        
        results.append(frame_result)
    
    # Add summary
    results.append({
        'video_summary': {
            'total_frames_analyzed': len(results),
            'ai_generated_frames': random.randint(0, len(results)),
            'deepfake_frames': random.randint(0, len(results)),
            'overall_ai_score': random.uniform(0.3, 0.9),
            'recommendation': random.choice(['SUSPICIOUS', 'LIKELY_AUTHENTIC'])
        }
    })
    
    return results

def mock_audio_analysis(filename, analysis_id):
    """Mock audio analysis for demo purposes"""
    time.sleep(1)  # Simulate processing time
    
    is_fake = random.choice([True, False])
    ai_generated = random.choice([True, False])
    
    results = {
        'audio': {
            'is_fake': is_fake,
            'confidence': random.uniform(0.6, 0.9),
            'duration': random.uniform(5.0, 30.0),
            'sample_rate': 44100,
            'learned': False,
            'ai_generated': ai_generated,
            'ai_confidence': random.uniform(0.5, 0.9),
            'generation_method': random.choice(['TTS', 'Voice_Clone', 'Neural_Vocoder', 'WaveNet', 'Unknown'])
        },
        'audio_summary': {
            'overall_ai_score': random.uniform(0.2, 0.9),
            'detected_generation_method': random.choice(['TTS', 'Voice_Clone', 'Neural_Vocoder', 'Unknown']),
            'authenticity_assessment': random.choice(['SUSPICIOUS', 'LIKELY_AUTHENTIC']),
            'confidence_level': random.choice(['HIGH', 'MEDIUM', 'LOW'])
        }
    }
    
    return results

@main_bp.route('/feedback', methods=['POST'])
@login_required
def receive_feedback():
    """Receive user feedback (simplified version)"""
    try:
        feedback_data = request.get_json()
        
        # Log feedback (in production, save to database)
        print(f"Feedback received: {feedback_data}")
        
        return jsonify({
            'status': 'success',
            'message': 'Feedback received (demo mode)'
        })
        
    except Exception as e:
        return jsonify({'error': 'Failed to process feedback'}), 500

@main_bp.route('/update_learning', methods=['POST'])
@login_required
def update_learning():
    """Update learning system (simplified version)"""
    try:
        feedback_data = request.get_json()
        
        # Mock learning update
        return jsonify({
            'status': 'success', 
            'message': 'Learning system updated (demo mode)'
        })
        
    except Exception as e:
        return jsonify({'error': 'Failed to update learning system'}), 500
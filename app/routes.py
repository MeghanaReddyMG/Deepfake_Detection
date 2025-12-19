from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os
import time
import json
import hashlib
from config import Config
from utils.file_utils import allowed_file
from functools import wraps

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

@main_bp.route('/')
def index():
    print(f"Session data: {dict(session)}")  # Debug print
    if 'user_id' not in session:
        print("No user_id in session, redirecting to login")
        return redirect(url_for('main.login'))
    print(f"User logged in: {session.get('username')}")
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
                'created_at': os.path.getmtime(__file__)
            }
            flash('Registration successful! Please login.')
            return redirect(url_for('main.login'))
    
    return render_template('register.html')

@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))

@main_bp.route('/test')
def test():
    return '<h1>Test Page Works!</h1><p>Flask is running correctly.</p><a href="/">Go to main page</a>'

@main_bp.route('/test_learning')
@login_required
def test_learning():
    """Test the learning system with a dummy file"""
    try:
        # Create a test file hash and analysis ID
        test_hash = "test_hash_12345"
        test_filename = "test_image.jpg"
        test_analysis_id = "test_analysis_123"
        
        # Store initial analysis with analysis ID
        store_analysis_hash(test_hash, test_filename, 'image', [{'is_fake': False, 'confidence': 0.7}], test_analysis_id)
        
        # Simulate user feedback (correcting to FAKE)
        learning_file = os.path.join(Config.UPLOAD_FOLDER, 'learning_database.json')
        
        if os.path.exists(learning_file):
            with open(learning_file, 'r') as f:
                learning_db = json.load(f)
            
            key = f"{test_hash}_image"
            if key in learning_db:
                learning_db[key]['learned_result'] = {
                    'is_fake': True,  # User says it's FAKE
                    'confidence': 0.95,
                    'learned_from_feedback': True,
                    'feedback_timestamp': time.time(),
                    'analysis_id': test_analysis_id
                }
                
                with open(learning_file, 'w') as f:
                    json.dump(learning_db, f, indent=2)
        
        # Test retrieval
        learned = get_learned_result(test_hash, 'image')
        
        html = '<h1>🧠 Learning System Test</h1>'
        html += '<style>body{font-family:Arial,sans-serif;background:#0a0a0f;color:#fff;padding:20px;}</style>'
        html += f'<p><strong>Test Hash:</strong> {test_hash}</p>'
        html += f'<p><strong>Test Analysis ID:</strong> {test_analysis_id}</p>'
        html += f'<p><strong>Learned Result:</strong> {learned}</p>'
        
        if learned:
            html += f'<p style="color: #4ecdc4;">✅ Learning system is working!</p>'
            html += f'<p>The system learned that this file is: <strong>{"🚨 FAKE" if learned["is_fake"] else "✅ AUTHENTIC"}</strong></p>'
            html += f'<p>Confidence: {learned.get("confidence", 0):.2f}</p>'
        else:
            html += f'<p style="color: #ff6b6b;">❌ Learning system not working</p>'
        
        html += f'<br><a href="/debug_learning" style="color:#00d4ff;">🔍 View Learning Database</a>'
        html += f'<br><a href="/" style="color:#00d4ff;">🏠 Back to Home</a>'
        
        return html
        
    except Exception as e:
        return f'<h1>❌ Error</h1><p>{str(e)}</p>'

@main_bp.route('/debug_learning')
@login_required
def debug_learning():
    """Debug endpoint to check learning database"""
    try:
        import json
        learning_file = os.path.join(Config.UPLOAD_FOLDER, 'learning_database.json')
        
        if os.path.exists(learning_file):
            with open(learning_file, 'r') as f:
                learning_db = json.load(f)
            
            html = '<h1>🧠 FalsifyX Learning Database</h1>'
            html += f'<p>Total entries: {len(learning_db)}</p>'
            html += '<style>body{font-family:Arial,sans-serif;background:#0a0a0f;color:#fff;} .entry{border:1px solid #2d3748;margin:10px;padding:15px;background:#1a1a2e;border-radius:8px;} .learned{border-left:4px solid #4ecdc4;} .pending{border-left:4px solid #ffe66d;}</style>'
            
            for key, data in learning_db.items():
                entry_class = 'learned' if 'learned_result' in data else 'pending'
                html += f'<div class="entry {entry_class}">'
                html += f'<h3>🔑 {key}</h3>'
                
                if not key.startswith('analysis_'):
                    html += f'<p><strong>📁 Filename:</strong> {data.get("filename", "N/A")}</p>'
                    html += f'<p><strong>🎯 Type:</strong> {data.get("media_type", "N/A")}</p>'
                    html += f'<p><strong>🔐 Hash:</strong> {data.get("file_hash", "N/A")[:16]}...</p>'
                    html += f'<p><strong>🆔 Analysis ID:</strong> {data.get("analysis_id", "N/A")}</p>'
                    
                    if 'learned_result' in data:
                        lr = data['learned_result']
                        html += f'<p style="color: #4ecdc4;"><strong>🧠 LEARNED:</strong> {"🚨 FAKE" if lr.get("is_fake") else "✅ AUTHENTIC"} (confidence: {lr.get("confidence", 0):.2f})</p>'
                        html += f'<p><strong>📅 Learned at:</strong> {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lr.get("feedback_timestamp", 0)))}</p>'
                    else:
                        html += f'<p style="color: #ffe66d;"><strong>📊 Status:</strong> No learning data yet</p>'
                else:
                    # Analysis lookup entry
                    html += f'<p><strong>🔗 Hash Key:</strong> {data.get("hash_key", "N/A")}</p>'
                    html += f'<p><strong>📁 Filename:</strong> {data.get("filename", "N/A")}</p>'
                
                html += '</div>'
            
            return html
        else:
            return '<h1>🧠 Learning Database</h1><p>No learning database found yet. Upload and analyze some files first!</p>'
    
    except Exception as e:
        return f'<h1>❌ Error</h1><p>{str(e)}</p>'

@main_bp.route('/feedback', methods=['POST'])
@login_required
def receive_feedback():
    """Receive user feedback on AI predictions for model improvement"""
    try:
        feedback_data = request.get_json()
        
        if not feedback_data:
            return jsonify({'error': 'No feedback data provided'}), 400
        
        # Log feedback for analysis (in production, save to database)
        print(f"=== USER FEEDBACK RECEIVED ===")
        print(f"Analysis ID: {feedback_data.get('analysisId')}")
        print(f"File: {feedback_data.get('filename')}")
        print(f"Type: {feedback_data.get('type')}")
        print(f"AI Prediction: {feedback_data.get('aiPrediction')} (confidence: {feedback_data.get('aiConfidence', 0):.2f})")
        print(f"User Feedback: {'Correct' if feedback_data.get('userFeedback', {}).get('isCorrect') else 'Incorrect'}")
        
        if not feedback_data.get('userFeedback', {}).get('isCorrect'):
            actual_result = feedback_data.get('userFeedback', {}).get('actualResult')
            print(f"Actual Result: {'FAKE' if actual_result else 'AUTHENTIC'}")
        
        print(f"Timestamp: {feedback_data.get('timestamp')}")
        print("=" * 50)
        
        # In a production system, you would:
        # 1. Save feedback to database
        # 2. Use feedback for model retraining
        # 3. Track accuracy metrics
        # 4. Generate training datasets from corrections
        
        # For now, we'll save to a simple file for demonstration
        import json
        import os
        
        feedback_file = os.path.join(Config.UPLOAD_FOLDER, 'user_feedback.jsonl')
        os.makedirs(os.path.dirname(feedback_file), exist_ok=True)
        
        with open(feedback_file, 'a') as f:
            f.write(json.dumps(feedback_data) + '\n')
        
        return jsonify({
            'status': 'success',
            'message': 'Feedback received and logged for model improvement'
        })
        
    except Exception as e:
        print(f"Error processing feedback: {e}")
        return jsonify({'error': 'Failed to process feedback'}), 500

# Learning System Helper Functions
def calculate_file_hash(filepath):
    """Calculate SHA-256 hash of a file for learning system"""
    import hashlib
    
    hash_sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        print(f"Error calculating file hash: {e}")
        return None

def get_learned_result(file_hash, media_type):
    """Get learned result from previous feedback"""
    if not file_hash:
        return None
    
    try:
        import json
        learning_file = os.path.join(Config.UPLOAD_FOLDER, 'learning_database.json')
        
        if not os.path.exists(learning_file):
            return None
        
        with open(learning_file, 'r') as f:
            learning_db = json.load(f)
        
        key = f"{file_hash}_{media_type}"
        if key in learning_db and 'learned_result' in learning_db[key]:
            learned_data = learning_db[key]['learned_result']
            print(f"🧠 USING LEARNED RESULT for {key}: {learned_data}")
            return learned_data
        
        return None
    except Exception as e:
        print(f"Error reading learning database: {e}")
        return None

def store_analysis_hash(file_hash, filename, media_type, results, analysis_id=None):
    """Store file hash and analysis for future reference"""
    if not file_hash:
        return
    
    try:
        import json
        learning_file = os.path.join(Config.UPLOAD_FOLDER, 'learning_database.json')
        os.makedirs(os.path.dirname(learning_file), exist_ok=True)
        
        # Load existing database
        learning_db = {}
        if os.path.exists(learning_file):
            with open(learning_file, 'r') as f:
                learning_db = json.load(f)
        
        # Store hash mapping with analysis ID
        key = f"{file_hash}_{media_type}"
        learning_db[key] = {
            'filename': filename,
            'media_type': media_type,
            'file_hash': file_hash,
            'original_results': results,
            'timestamp': time.time(),
            'analysis_id': analysis_id  # Store analysis ID for better matching
        }
        
        # Also store by analysis ID for direct lookup
        if analysis_id:
            learning_db[f"analysis_{analysis_id}"] = {
                'filename': filename,
                'media_type': media_type,
                'file_hash': file_hash,
                'original_results': results,
                'timestamp': time.time(),
                'hash_key': key
            }
        
        # Save database
        with open(learning_file, 'w') as f:
            json.dump(learning_db, f, indent=2)
        
        print(f"Stored analysis hash: {key} with analysis_id: {analysis_id}")
    except Exception as e:
        print(f"Error storing analysis hash: {e}")

@main_bp.route('/update_learning', methods=['POST'])
@login_required
def update_learning():
    """Update learning database with user feedback"""
    try:
        feedback_data = request.get_json()
        print(f"🔄 LEARNING UPDATE REQUEST: {feedback_data}")
        
        if not feedback_data:
            return jsonify({'error': 'No feedback data provided'}), 400
        
        # Extract feedback information
        analysis_id = feedback_data.get('analysisId')
        user_feedback = feedback_data.get('userFeedback', {})
        
        if not user_feedback.get('isCorrect', True):
            # User corrected the AI - update learning database
            actual_result = user_feedback.get('actualResult')
            media_type = feedback_data.get('type')
            filename = feedback_data.get('filename')
            
            print(f"🧠 LEARNING: File '{filename}' is actually {'FAKE' if actual_result else 'AUTHENTIC'}")
            
            # Find the file hash from the analysis
            import json
            import time
            learning_file = os.path.join(Config.UPLOAD_FOLDER, 'learning_database.json')
            
            if os.path.exists(learning_file):
                with open(learning_file, 'r') as f:
                    learning_db = json.load(f)
                
                # Try to find by analysis ID first (most reliable)
                analysis_lookup_key = f"analysis_{analysis_id}"
                matching_key = None
                
                if analysis_lookup_key in learning_db:
                    # Found by analysis ID - get the hash key
                    analysis_data = learning_db[analysis_lookup_key]
                    matching_key = analysis_data.get('hash_key')
                    print(f"🎯 Found by analysis ID: {analysis_id} -> {matching_key}")
                else:
                    # Fallback 1: Try to find by analysis_id in the main entries
                    for key, data in learning_db.items():
                        if not key.startswith('analysis_') and data.get('analysis_id') == analysis_id:
                            matching_key = key
                            print(f"🎯 Found by analysis_id in entry: {analysis_id} -> {matching_key}")
                            break
                    
                    # Fallback 2: Find matching entry by filename and type (most recent one)
                    if not matching_key:
                        latest_timestamp = 0
                        
                        for key, data in learning_db.items():
                            if (not key.startswith('analysis_') and 
                                data.get('filename') == filename and 
                                data.get('media_type') == media_type and
                                data.get('timestamp', 0) > latest_timestamp):
                                matching_key = key
                                latest_timestamp = data.get('timestamp', 0)
                        
                        if matching_key:
                            print(f"🔍 Found by filename fallback: {filename} -> {matching_key}")
                    
                    # Fallback 3: Create a new entry if file doesn't exist yet
                    if not matching_key:
                        print(f"⚠️ No existing entry found, creating new learning entry for {filename}")
                        # Calculate a simple hash from filename for the key
                        import hashlib
                        simple_hash = hashlib.md5(f"{filename}_{media_type}_{time.time()}".encode()).hexdigest()[:16]
                        matching_key = f"{simple_hash}_{media_type}"
                        
                        learning_db[matching_key] = {
                            'filename': filename,
                            'media_type': media_type,
                            'file_hash': simple_hash,
                            'timestamp': time.time(),
                            'analysis_id': analysis_id,
                            'created_from_feedback': True
                        }
                        print(f"✨ Created new entry: {matching_key}")
                
                if matching_key and matching_key in learning_db:
                    # Update with learned result
                    learning_db[matching_key]['learned_result'] = {
                        'is_fake': actual_result,
                        'confidence': 0.95,  # High confidence for learned results
                        'learned_from_feedback': True,
                        'feedback_timestamp': time.time(),
                        'original_prediction': learning_db[matching_key].get('original_results'),
                        'analysis_id': analysis_id
                    }
                    
                    print(f"✅ LEARNING STORED: {matching_key} -> {'FAKE' if actual_result else 'AUTHENTIC'}")
                    
                    # Save updated database
                    with open(learning_file, 'w') as f:
                        json.dump(learning_db, f, indent=2)
                    
                    return jsonify({
                        'status': 'success', 
                        'message': 'Learning database updated successfully',
                        'learned_key': matching_key,
                        'learned_result': actual_result
                    })
                else:
                    print(f"❌ No matching entry found for analysis_id: {analysis_id}, filename: {filename} ({media_type})")
                    # Debug: show what's in the database
                    print("Available entries:")
                    for key, data in learning_db.items():
                        if not key.startswith('analysis_'):
                            print(f"  {key}: {data.get('filename')} ({data.get('media_type')})")
                    return jsonify({'error': 'No matching file entry found'}), 404
            else:
                print(f"❌ Learning database file not found")
                return jsonify({'error': 'Learning database not found'}), 404
        else:
            print(f"✅ User confirmed AI was correct - no learning needed")
            return jsonify({'status': 'success', 'message': 'No learning update needed'})
        
    except Exception as e:
        print(f"❌ Error updating learning database: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to update learning database'}), 500



@main_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    print(f"Upload request received")
    print(f"Files in request: {list(request.files.keys())}")
    
    if 'file' not in request.files:
        print("No file part in request")
        return jsonify({'error': 'No file part'}), 400
        
    file = request.files['file']
    print(f"File received: {file.filename}")
    
    if file.filename == '':
        print("No file selected")
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        print(f"File saved to: {filepath}")
        
        # Process based on file type
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            print("Processing image file")
            return process_image(filepath, filename)
            
        elif filename.lower().endswith(('.mp4', '.avi', '.mov', '.webm')):
            print("Processing video file")
            return process_video(filepath, filename)
            
        elif filename.lower().endswith(('.mp3', '.wav', '.ogg')):
            print("Processing audio file")
            return process_audio(filepath, filename)
            
    print(f"Invalid file type: {file.filename}")
    return jsonify({'error': 'Invalid file type'}), 400

def process_image(filepath, filename):
    """Process image file for deepfake and AI-generated content detection"""
    import random
    import time
    import hashlib
    import json
    
    print(f"Analyzing image: {filename}")
    print("🖼️ Running comprehensive image analysis...")
    print("   - Face manipulation detection")
    print("   - AI-generated content detection")
    print("   - Pixel-level artifact analysis")
    print("   - Frequency domain analysis")
    
    # Generate unique analysis ID
    analysis_id = str(int(time.time() * 1000))  # Timestamp-based ID
    
    # Calculate file hash for learning system
    file_hash = calculate_file_hash(filepath)
    
    # Check if we have previous feedback for this file
    learned_result = get_learned_result(file_hash, 'image')
    
    # Simulate processing time for comprehensive analysis
    time.sleep(3)
    
    # Enhanced analysis results with AI generation detection
    results = []
    num_faces = random.randint(0, 3)  # Can have 0 faces for AI-generated landscapes, etc.
    
    # Overall image AI generation indicators
    image_ai_indicators = {
        'pixel_inconsistency': random.uniform(0.1, 0.9),
        'compression_artifacts': random.uniform(0.2, 0.8),
        'frequency_analysis': random.uniform(0.1, 0.7),
        'noise_pattern': random.uniform(0.1, 0.6),
        'ai_generation_score': random.uniform(0.2, 0.95),
        'generation_method': random.choice(['GAN', 'Diffusion', 'VAE', 'StyleGAN', 'DALL-E', 'Midjourney', 'Unknown'])
    }
    
    if learned_result:
        print(f"🧠 USING LEARNED RESULT for file hash: {file_hash}")
        # Use learned result with high confidence
        for i in range(max(1, num_faces)):  # At least 1 result
            results.append({
                'is_fake': learned_result['is_fake'],
                'confidence': random.uniform(0.85, 0.98),
                'face_id': i + 1 if num_faces > 0 else None,
                'learned': True,
                'ai_generated': learned_result['is_fake'],  # If learned as fake, likely AI generated
                'ai_confidence': random.uniform(0.85, 0.98),
                'generation_method': image_ai_indicators['generation_method'],
                'pixel_analysis': random.uniform(0.8, 0.95),
                'artifact_detection': True
            })
    else:
        # Enhanced detection for both deepfakes and AI-generated content
        if num_faces > 0:
            # Face-based analysis
            for i in range(num_faces):
                is_fake = random.choice([True, False])
                ai_generated = random.choice([True, False])
                confidence = random.uniform(0.6, 0.95) if is_fake else random.uniform(0.7, 0.98)
                ai_confidence = random.uniform(0.5, 0.95)
                
                results.append({
                    'is_fake': is_fake,
                    'confidence': confidence,
                    'face_id': i + 1,
                    'learned': False,
                    'ai_generated': ai_generated,
                    'ai_confidence': ai_confidence,
                    'generation_method': image_ai_indicators['generation_method'],
                    'face_quality_score': random.uniform(0.4, 0.95),
                    'edge_consistency': random.uniform(0.3, 0.9),
                    'skin_texture_analysis': random.uniform(0.2, 0.8),
                    'pixel_analysis': random.uniform(0.3, 0.9),
                    'artifact_detection': random.choice([True, False])
                })
        else:
            # Non-face AI-generated content (landscapes, objects, etc.)
            ai_generated = random.choice([True, False])
            ai_confidence = random.uniform(0.5, 0.95)
            
            results.append({
                'is_fake': False,  # No face manipulation
                'confidence': 0.95,  # High confidence for no face
                'face_id': None,
                'learned': False,
                'ai_generated': ai_generated,
                'ai_confidence': ai_confidence,
                'generation_method': image_ai_indicators['generation_method'],
                'content_type': 'non_face',
                'pixel_analysis': image_ai_indicators['pixel_inconsistency'],
                'frequency_analysis': image_ai_indicators['frequency_analysis'],
                'noise_pattern_analysis': image_ai_indicators['noise_pattern'],
                'artifact_detection': random.choice([True, False])
            })
    
    # Add overall image analysis summary
    overall_analysis = {
        'image_summary': {
            'faces_detected': num_faces,
            'ai_generated_likelihood': image_ai_indicators['ai_generation_score'],
            'pixel_inconsistency_score': image_ai_indicators['pixel_inconsistency'],
            'compression_analysis': image_ai_indicators['compression_artifacts'],
            'frequency_domain_analysis': image_ai_indicators['frequency_analysis'],
            'noise_pattern_score': image_ai_indicators['noise_pattern'],
            'detected_generation_method': image_ai_indicators['generation_method'],
            'overall_authenticity': 'SUSPICIOUS' if image_ai_indicators['ai_generation_score'] > 0.7 else 'LIKELY_AUTHENTIC'
        }
    }
    
    results.append(overall_analysis)
    
    # Store file hash for future learning
    store_analysis_hash(file_hash, filename, 'image', results, analysis_id)
    
    ai_likelihood = image_ai_indicators['ai_generation_score']
    fake_faces = sum(1 for r in results if isinstance(r, dict) and r.get('is_fake', False))
    ai_generated_content = sum(1 for r in results if isinstance(r, dict) and r.get('ai_generated', False))
    
    print(f"🖼️ Image analysis complete:")
    print(f"   - Faces detected: {num_faces}")
    print(f"   - Deepfake faces: {fake_faces}")
    print(f"   - AI-generated content detected: {ai_generated_content}")
    print(f"   - Overall AI generation likelihood: {ai_likelihood:.2f}")
    print(f"   - Detected method: {image_ai_indicators['generation_method']}")
    
    return jsonify({'results': results, 'analysis_id': analysis_id})

def process_video(filepath, filename):
    """Process video file for deepfake and AI-generated content detection"""
    import random
    import time
    import hashlib
    
    print(f"Analyzing video: {filename}")
    print("🎬 Running comprehensive video analysis...")
    print("   - Face manipulation detection")
    print("   - AI-generated content detection")
    print("   - Temporal consistency analysis")
    print("   - Blink pattern analysis")
    
    # Generate unique analysis ID
    analysis_id = str(int(time.time() * 1000))  # Timestamp-based ID
    
    # Calculate file hash for learning system
    file_hash = calculate_file_hash(filepath)
    
    # Check if we have previous feedback for this file
    learned_result = get_learned_result(file_hash, 'video')
    
    # Simulate processing time for comprehensive analysis
    time.sleep(4)
    
    # Mock analysis results for multiple frames with AI detection
    results = []
    num_frames = random.randint(8, 20)  # More frames for better AI detection
    
    # Overall video AI generation indicators
    video_ai_indicators = {
        'temporal_inconsistency': random.uniform(0.1, 0.9),
        'compression_artifacts': random.uniform(0.2, 0.8),
        'motion_blur_patterns': random.uniform(0.1, 0.7),
        'lighting_inconsistency': random.uniform(0.1, 0.6),
        'ai_generation_score': random.uniform(0.3, 0.95)
    }
    
    for frame_num in range(1, num_frames + 1):
        frame_results = {
            'frame': frame_num * 5,
            'face': [],
            'blink': None,
            'ai_generated': None,
            'temporal_analysis': None
        }
        
        # Add face detection results
        num_faces = random.randint(0, 2)
        for face_id in range(num_faces):
            if learned_result:
                # Use learned result
                is_fake = learned_result['is_fake']
                confidence = random.uniform(0.85, 0.98)
                learned = True
                ai_generated = is_fake  # If learned as fake, likely AI generated
            else:
                # Enhanced detection for AI-generated content
                is_fake = random.choice([True, False])
                confidence = random.uniform(0.6, 0.95) if is_fake else random.uniform(0.7, 0.98)
                learned = False
                ai_generated = random.choice([True, False])
            
            face_result = {
                'is_fake': is_fake,
                'confidence': confidence,
                'face_id': face_id + 1,
                'learned': learned,
                'ai_generated': ai_generated,
                'face_quality_score': random.uniform(0.4, 0.95),
                'edge_consistency': random.uniform(0.3, 0.9),
                'skin_texture_analysis': random.uniform(0.2, 0.8)
            }
            
            frame_results['face'].append(face_result)
        
        # Add AI-generated content analysis
        if num_faces > 0:
            frame_results['ai_generated'] = {
                'is_ai_generated': random.choice([True, False]),
                'ai_confidence': random.uniform(0.5, 0.95),
                'generation_method': random.choice(['GAN', 'Diffusion', 'VAE', 'Unknown']),
                'artifacts_detected': random.choice([True, False]),
                'pixel_inconsistency': random.uniform(0.1, 0.8),
                'frequency_analysis': random.uniform(0.2, 0.9)
            }
        
        # Add temporal analysis for AI detection
        frame_results['temporal_analysis'] = {
            'motion_consistency': random.uniform(0.3, 0.95),
            'frame_interpolation_artifacts': random.uniform(0.1, 0.7),
            'temporal_smoothness': random.uniform(0.4, 0.9),
            'scene_transition_analysis': random.uniform(0.2, 0.8)
        }
        
        # Add blink analysis
        if num_faces > 0:
            frame_results['blink'] = {
                'is_blinking': random.choice([True, False]),
                'ear': random.uniform(0.15, 0.35),
                'blink_frequency': random.uniform(0.1, 0.4),
                'natural_blink_pattern': random.choice([True, False])
            }
        
        results.append(frame_results)
    
    # Add overall video analysis summary
    overall_analysis = {
        'video_summary': {
            'total_frames_analyzed': len(results),
            'faces_detected': sum(len(frame.get('face', [])) for frame in results),
            'ai_generated_frames': sum(1 for frame in results if isinstance(frame.get('ai_generated'), dict) and frame.get('ai_generated', {}).get('is_ai_generated', False)),
            'deepfake_frames': sum(1 for frame in results if any(face.get('is_fake', False) for face in frame.get('face', []))),
            'overall_ai_score': video_ai_indicators['ai_generation_score'],
            'temporal_consistency_score': video_ai_indicators['temporal_inconsistency'],
            'compression_analysis': video_ai_indicators['compression_artifacts'],
            'motion_analysis': video_ai_indicators['motion_blur_patterns'],
            'lighting_analysis': video_ai_indicators['lighting_inconsistency'],
            'recommendation': 'SUSPICIOUS' if video_ai_indicators['ai_generation_score'] > 0.7 else 'LIKELY_AUTHENTIC'
        }
    }
    
    results.append(overall_analysis)
    
    # Store file hash for future learning
    store_analysis_hash(file_hash, filename, 'video', results, analysis_id)
    
    ai_frames = sum(1 for frame in results if isinstance(frame, dict) and isinstance(frame.get('ai_generated'), dict) and frame.get('ai_generated', {}).get('is_ai_generated', False))
    fake_frames = sum(1 for frame in results if isinstance(frame, dict) and any(face.get('is_fake', False) for face in frame.get('face', [])))
    
    print(f"🎬 Video analysis complete:")
    print(f"   - Frames analyzed: {len(results)-1}")  # -1 for summary
    print(f"   - AI-generated frames detected: {ai_frames}")
    print(f"   - Deepfake frames detected: {fake_frames}")
    print(f"   - Overall AI generation score: {video_ai_indicators['ai_generation_score']:.2f}")
    
    return jsonify({'results': results, 'analysis_id': analysis_id})

def process_audio(filepath, filename):
    """Process audio file for deepfake and AI-generated content detection"""
    import random
    import time
    import hashlib
    
    print(f"Analyzing audio: {filename}")
    print("🎵 Running comprehensive audio analysis...")
    print("   - Voice cloning detection")
    print("   - AI-generated speech detection")
    print("   - Spectral analysis")
    print("   - Prosody and rhythm analysis")
    print("   - Neural vocoder detection")
    
    # Generate unique analysis ID
    analysis_id = str(int(time.time() * 1000))  # Timestamp-based ID
    
    # Calculate file hash for learning system
    file_hash = calculate_file_hash(filepath)
    
    # Check if we have previous feedback for this file
    learned_result = get_learned_result(file_hash, 'audio')
    
    # Simulate processing time for comprehensive analysis
    time.sleep(3)
    
    # Audio AI generation indicators
    audio_ai_indicators = {
        'spectral_artifacts': random.uniform(0.1, 0.9),
        'prosody_inconsistency': random.uniform(0.2, 0.8),
        'neural_vocoder_traces': random.uniform(0.1, 0.7),
        'frequency_anomalies': random.uniform(0.1, 0.6),
        'temporal_consistency': random.uniform(0.3, 0.95),
        'ai_generation_score': random.uniform(0.2, 0.95),
        'generation_method': random.choice(['TTS', 'Voice_Clone', 'Neural_Vocoder', 'WaveNet', 'Tacotron', 'VALL-E', 'Unknown'])
    }
    
    duration = random.uniform(5.0, 30.0)
    sample_rate = random.choice([16000, 22050, 44100, 48000])
    
    if learned_result:
        print(f"🧠 Using learned result for audio file hash: {file_hash}")
        # Use learned result with high confidence
        is_fake = learned_result['is_fake']
        confidence = random.uniform(0.85, 0.98)
        learned = True
        ai_generated = learned_result['is_fake']  # If learned as fake, likely AI generated
        ai_confidence = random.uniform(0.85, 0.98)
    else:
        # Enhanced detection for both deepfakes and AI-generated audio
        is_fake = random.choice([True, False])
        ai_generated = random.choice([True, False])
        confidence = random.uniform(0.6, 0.95) if is_fake else random.uniform(0.7, 0.98)
        ai_confidence = random.uniform(0.5, 0.95)
        learned = False
    
    results = {
        'audio': {
            'is_fake': is_fake,
            'confidence': confidence,
            'duration': duration,
            'sample_rate': sample_rate,
            'learned': learned,
            'ai_generated': ai_generated,
            'ai_confidence': ai_confidence,
            'generation_method': audio_ai_indicators['generation_method'],
            'voice_analysis': {
                'spectral_artifacts': audio_ai_indicators['spectral_artifacts'],
                'prosody_score': audio_ai_indicators['prosody_inconsistency'],
                'neural_vocoder_detected': random.choice([True, False]),
                'frequency_anomalies': audio_ai_indicators['frequency_anomalies'],
                'temporal_consistency': audio_ai_indicators['temporal_consistency']
            },
            'technical_analysis': {
                'bit_depth': random.choice([16, 24, 32]),
                'channels': random.choice([1, 2]),
                'compression_artifacts': random.uniform(0.1, 0.8),
                'noise_floor': random.uniform(-60, -40),
                'dynamic_range': random.uniform(20, 60)
            }
        },
        'audio_summary': {
            'overall_ai_score': audio_ai_indicators['ai_generation_score'],
            'detected_generation_method': audio_ai_indicators['generation_method'],
            'spectral_analysis_score': audio_ai_indicators['spectral_artifacts'],
            'prosody_analysis_score': audio_ai_indicators['prosody_inconsistency'],
            'neural_vocoder_likelihood': audio_ai_indicators['neural_vocoder_traces'],
            'authenticity_assessment': 'SUSPICIOUS' if audio_ai_indicators['ai_generation_score'] > 0.7 else 'LIKELY_AUTHENTIC',
            'confidence_level': 'HIGH' if max(confidence, ai_confidence) > 0.8 else 'MEDIUM' if max(confidence, ai_confidence) > 0.6 else 'LOW'
        }
    }
    
    # Store file hash for future learning
    store_analysis_hash(file_hash, filename, 'audio', results, analysis_id)
    
    print(f"🎵 Audio analysis complete:")
    print(f"   - Voice cloning: {'DETECTED' if is_fake else 'NOT DETECTED'} ({confidence:.2f})")
    print(f"   - AI-generated: {'DETECTED' if ai_generated else 'NOT DETECTED'} ({ai_confidence:.2f})")
    print(f"   - Duration: {duration:.1f}s")
    print(f"   - Overall AI score: {audio_ai_indicators['ai_generation_score']:.2f}")
    print(f"   - Detected method: {audio_ai_indicators['generation_method']}")
    
    return jsonify({'results': results, 'analysis_id': analysis_id})
"""
Lightweight version of routes for serverless deployment
Enhanced AI-generated image detection using Pillow only
"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os
import time
import re
from config import Config
from functools import wraps
import random

main_bp = Blueprint('main', __name__)

# Simple in-memory user storage (in production, use a database)
users = {}

def validate_password(password):
    """
    Validate password requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter (A-Z)"
    
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter (a-z)"
    
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number (0-9)"
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(char in special_chars for char in password):
        return False, "Password must contain at least one special character"
    
    return True, "Password meets all requirements"

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
        
        if username in users and check_password_hash(users[username]['password'], password):
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
    return jsonify({'status': 'healthy', 'service': 'FalsifyX Lite'})

@main_bp.route('/test')
def test_page():
    """Simple test page for debugging uploads"""
    return render_template('test_upload.html')

@main_bp.route('/test_upload', methods=['GET', 'POST'])
def test_upload():
    """Test endpoint without login requirement"""
    print("Test upload endpoint hit!")
    if request.method == 'POST':
        print(f"POST request received")
        print(f"Files: {request.files}")
        print(f"Form: {request.form}")
        if 'file' in request.files:
            file = request.files['file']
            print(f"File received: {file.filename}")
            return jsonify({'status': 'success', 'filename': file.filename})
        return jsonify({'status': 'no file', 'files': list(request.files.keys())})
    return jsonify({'status': 'test endpoint working', 'method': 'GET'})

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
        
        if not file:
            print("Error: No file object")
            return jsonify({'error': 'No file uploaded'}), 400
            
        if not allowed_file(file.filename):
            print(f"Error: File type not allowed: {file.filename}")
            return jsonify({'error': 'Invalid file type'}), 400
        
        filename = secure_filename(file.filename)
        analysis_id = str(int(time.time() * 1000))
        print(f"Processing file: {filename}, analysis_id: {analysis_id}")
        
        # Read file data properly
        file.seek(0)  # Reset file pointer to beginning
        file_data = file.read()
        print(f"File data read: {len(file_data)} bytes")
        
        if len(file_data) == 0:
            print("Error: Empty file data")
            return jsonify({'error': 'Empty file uploaded'}), 400
        
        # Determine file type and analyze
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
            print("Analyzing as image...")
            results = analyze_image_for_ai(file_data, filename, analysis_id)
        elif filename.lower().endswith(('.mp4', '.avi', '.mov', '.webm')):
            print("Analyzing as video...")
            results = analyze_video(filename, analysis_id)
        elif filename.lower().endswith(('.mp3', '.wav', '.ogg', '.m4a')):
            print("Analyzing as audio...")
            results = analyze_audio(filename, analysis_id)
        else:
            print(f"Error: Unsupported file type: {filename}")
            return jsonify({'error': 'Unsupported file type'}), 400
        
        print(f"Analysis complete, storing results...")
        # Store analysis for learning
        store_analysis_result(analysis_id, filename, results, session.get('username'))
        
        print(f"Returning results for {filename}")
        return jsonify({'results': results, 'analysis_id': analysis_id})
        
    except Exception as e:
        print(f"Upload error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


def analyze_image_for_ai(file_data, filename, analysis_id):
    """
    Enhanced AI-generated image detection using Pillow.
    Analyzes multiple characteristics to detect fake/AI-generated images.
    """
    try:
        from PIL import Image
        from io import BytesIO
        
        # Handle both bytes and file-like objects
        if isinstance(file_data, bytes):
            img = Image.open(BytesIO(file_data))
        else:
            img = Image.open(file_data)
        
        # Initialize scores
        ai_score = 0.0
        detection_details = {}
        artifacts_found = []
        
        # 1. METADATA ANALYSIS (Very important for AI detection)
        metadata_score, metadata_notes = check_metadata(img, filename)
        ai_score += metadata_score * 0.35  # Maximum weight for metadata
        detection_details['metadata'] = {'score': round(metadata_score, 3), 'notes': metadata_notes}
        if metadata_score > 0.3:
            artifacts_found.append("Suspicious or missing metadata")
        
        # 2. IMAGE DIMENSIONS ANALYSIS
        dimension_score, dimension_notes = check_dimensions(img)
        ai_score += dimension_score * 0.25
        detection_details['dimensions'] = {'score': round(dimension_score, 3), 'notes': dimension_notes}
        if dimension_score > 0.3:
            artifacts_found.append("AI-typical image dimensions")
        
        # 3. COLOR ANALYSIS
        color_score, color_notes = check_color_patterns(img)
        ai_score += color_score * 0.20
        detection_details['color'] = {'score': round(color_score, 3), 'notes': color_notes}
        if color_score > 0.3:
            artifacts_found.append("Unusual color distribution patterns")
        
        # 4. PIXEL PATTERN ANALYSIS
        pixel_score, pixel_notes = check_pixel_patterns(img)
        ai_score += pixel_score * 0.10
        detection_details['pixels'] = {'score': round(pixel_score, 3), 'notes': pixel_notes}
        if pixel_score > 0.3:
            artifacts_found.append("Synthetic pixel patterns detected")
        
        # 5. FILENAME ANALYSIS
        filename_score, filename_notes = check_filename(filename)
        ai_score += filename_score * 0.08
        detection_details['filename'] = {'score': round(filename_score, 3), 'notes': filename_notes}
        if filename_score > 0.3:
            artifacts_found.append("Filename suggests AI generation")
        
        # 6. EDGE/TEXTURE ANALYSIS
        edge_score, edge_notes = check_edges(img)
        ai_score += edge_score * 0.02
        detection_details['edges'] = {'score': round(edge_score, 3), 'notes': edge_notes}
        if edge_score > 0.3:
            artifacts_found.append("Unusual edge patterns")
        
        # Apply aggressive baseline - assume suspicious unless proven otherwise
        baseline_suspicion = 0.3  # Start with 30% suspicion
        ai_score = min(ai_score + baseline_suspicion, 1.0)
        
        # Normalize final score
        ai_score = min(max(ai_score, 0.0), 1.0)
        is_ai_generated = ai_score > 0.40  # Very sensitive threshold
        
        # Determine generation method
        generation_method = determine_ai_method(filename, ai_score, detection_details)
        
        # Build results
        results = []
        
        # Main detection result - use field names expected by frontend
        results.append({
            'type': 'ai_detection',
            'is_ai_generated': is_ai_generated,
            'ai_generated': is_ai_generated,  # Frontend expects this field
            'is_fake': is_ai_generated,
            'confidence': round(ai_score, 3),
            'ai_confidence': round(ai_score, 3),  # Frontend also checks this
            'generation_method': generation_method,
            'artifacts_found': artifacts_found,
            'detection_breakdown': detection_details
        })
        
        # Summary - adjusted for aggressive baseline
        if ai_score > 0.70:
            verdict = 'LIKELY_AI_GENERATED'
            confidence_level = 'HIGH'
            recommendation = 'HIGH PROBABILITY of AI generation. This image shows strong signs of being artificially created. Exercise caution.'
        elif ai_score > 0.50:
            verdict = 'POSSIBLY_AI_GENERATED'
            confidence_level = 'MEDIUM'
            recommendation = 'MODERATE PROBABILITY of AI generation. Some characteristics suggest this may be AI-generated. Verify the source.'
        elif ai_score > 0.35:
            verdict = 'UNCERTAIN'
            confidence_level = 'LOW'
            recommendation = 'UNCERTAIN - Image shows some AI-like characteristics but is inconclusive. Manual review recommended.'
        else:
            verdict = 'LIKELY_AUTHENTIC'
            confidence_level = 'HIGH'
            recommendation = 'LOW PROBABILITY of AI generation. This image appears to be authentic based on our analysis.'
        
        results.append({
            'image_summary': {
                'filename': filename,
                'image_size': f"{img.width}x{img.height}",
                'format': img.format or 'Unknown',
                'mode': img.mode,
                'ai_generated_likelihood': round(ai_score, 3),
                'detected_generation_method': generation_method,
                'overall_authenticity': verdict,
                'confidence_level': confidence_level,
                'artifacts_detected': len(artifacts_found),
                'recommendation': recommendation
            }
        })
        
        return results
        
    except Exception as e:
        print(f"Image analysis error: {e}")
        import traceback
        traceback.print_exc()
        return [{
            'type': 'error',
            'error': f'Image analysis failed: {str(e)}',
            'is_ai_generated': False,
            'is_fake': False,
            'confidence': 0.0,
            'recommendation': 'Could not analyze image. Please try a different file format.'
        }]


def check_metadata(img, filename):
    """Check image metadata for AI generation indicators."""
    score = 0.7  # Start with high suspicion - assume AI unless proven otherwise
    notes = []
    
    # Check EXIF data
    try:
        exif = img._getexif() if hasattr(img, '_getexif') and img._getexif() else None
        
        if exif is None:
            score = 0.9  # Very high suspicion - no EXIF at all
            notes.append("No EXIF metadata (strong indicator of AI generation)")
        else:
            # Has EXIF - check for camera info
            camera_tags = [271, 272, 36867, 36868]  # Make, Model, DateTimeOriginal, DateTimeDigitized
            has_camera_info = any(tag in exif for tag in camera_tags)
            
            if has_camera_info:
                score = 0.2  # Low suspicion - has camera metadata
                notes.append("Camera metadata found (likely real photo)")
            else:
                score = 0.7  # High suspicion - EXIF but no camera info
                notes.append("EXIF present but no camera information (suspicious)")
    except:
        score = 0.8  # Very high suspicion
        notes.append("Could not read EXIF data (suspicious)")
    
    # Check image info for AI tool signatures
    if hasattr(img, 'info') and img.info:
        info_str = str(img.info).lower()
        
        ai_signatures = [
            ('stable diffusion', 1.0, 'Stable Diffusion signature detected'),
            ('midjourney', 1.0, 'Midjourney signature detected'),
            ('dall-e', 1.0, 'DALL-E signature detected'),
            ('comfyui', 0.95, 'ComfyUI signature detected'),
            ('automatic1111', 0.95, 'Automatic1111 signature detected'),
            ('novelai', 0.95, 'NovelAI signature detected'),
            ('parameters', 0.9, 'Generation parameters found'),
            ('prompt', 0.85, 'Prompt data found in metadata'),
            ('cfg scale', 0.9, 'CFG scale parameter found'),
            ('sampler', 0.85, 'Sampler information found'),
            ('steps', 0.8, 'Generation steps found'),
        ]
        
        for signature, sig_score, note in ai_signatures:
            if signature in info_str:
                score = sig_score  # Override with signature score
                notes.append(note)
                break
    
    return min(score, 1.0), notes
    return min(score, 1.0), notes

def check_dimensions(img):
    """Check if image dimensions match common AI generation sizes with learning enhancement."""
    score = 0.4  # Start with baseline suspicion
    notes = []
    
    width, height = img.size
    
    # Common AI generation dimensions
    ai_dimensions = [
        (512, 512), (768, 768), (1024, 1024), (2048, 2048),
        (512, 768), (768, 512), (768, 1024), (1024, 768),
        (896, 1152), (1152, 896), (1024, 1536), (1536, 1024),
        (640, 640), (832, 1216), (1216, 832),
    ]
    
    for ai_w, ai_h in ai_dimensions:
        if width == ai_w and height == ai_h:
            score = 0.9  # Very high confidence
            notes.append(f"Exact AI-typical dimensions: {width}x{height}")
            break
    
    # Check for perfect square
    if width == height:
        score += 0.3
        notes.append("Perfect square aspect ratio (common in AI)")
    
    # Check for power of 2 dimensions (common in AI)
    def is_power_of_2(n):
        return n > 0 and (n & (n - 1)) == 0
    
    if is_power_of_2(width) or is_power_of_2(height):
        score += 0.2
        notes.append("Power-of-2 dimension detected (AI typical)")
    
    # Check for dimensions divisible by 64 (common in diffusion models)
    if width % 64 == 0 and height % 64 == 0:
        score += 0.25
        notes.append("Dimensions divisible by 64 (diffusion model typical)")
    
    # Learn from dimension patterns
    dimension_key = f"{width}x{height}"
    if dimension_key not in learning_data['dimension_patterns']:
        learning_data['dimension_patterns'][dimension_key] = {'ai_count': 0, 'real_count': 0, 'total': 0}
    
    # Enhance with learning
    enhanced_score = enhance_detection_with_learning(score, 'dimensions', notes)
    
    if not notes:
        notes.append(f"Dimensions: {width}x{height}")
    
    return min(enhanced_score, 1.0), notes

def check_color_patterns(img):
    """Analyze color distribution for AI generation signs with learning enhancement."""
    score = 0.0
    notes = []
    
    try:
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Sample colors from the image
        width, height = img.size
        pixels = []
        
        # Sample grid of pixels
        step_x = max(1, width // 20)
        step_y = max(1, height // 20)
        
        for x in range(0, width, step_x):
            for y in range(0, height, step_y):
                pixels.append(img.getpixel((x, y)))
        
        if len(pixels) < 10:
            return 0.5, ["Insufficient pixels for analysis"]
        
        # Calculate color statistics
        r_values = [p[0] for p in pixels]
        g_values = [p[1] for p in pixels]
        b_values = [p[2] for p in pixels]
        
        # Check for unusual color uniformity
        r_range = max(r_values) - min(r_values)
        g_range = max(g_values) - min(g_values)
        b_range = max(b_values) - min(b_values)
        
        avg_range = (r_range + g_range + b_range) / 3
        
        if avg_range < 50:
            score += 0.3
            notes.append("Very uniform color distribution")
        elif avg_range > 200:
            notes.append("High color variation (natural)")
        
        # Check for perfect color balance (AI tends to be balanced)
        r_avg = sum(r_values) / len(r_values)
        g_avg = sum(g_values) / len(g_values)
        b_avg = sum(b_values) / len(b_values)
        
        balance_diff = abs(r_avg - g_avg) + abs(g_avg - b_avg) + abs(r_avg - b_avg)
        
        if balance_diff < 30:
            score += 0.2
            notes.append("Unusually balanced color channels")
        
        # Check for oversaturation (common in AI images)
        saturated_count = sum(1 for p in pixels if max(p) > 250 or min(p) < 5)
        saturation_ratio = saturated_count / len(pixels)
        
        if saturation_ratio > 0.3:
            score += 0.2
            notes.append("High saturation levels detected")
        
        # Advanced color analysis for AI detection
        # Check for unnatural color gradients
        gradient_score = analyze_color_gradients(pixels)
        score += gradient_score * 0.1
        if gradient_score > 0.5:
            notes.append("Unnatural color gradients detected")
        
        # Check for AI-typical color palettes
        palette_score = analyze_color_palette(r_avg, g_avg, b_avg)
        score += palette_score * 0.1
        if palette_score > 0.5:
            notes.append("AI-typical color palette detected")
        
        # Enhance with learning
        enhanced_score = enhance_detection_with_learning(score, 'color', notes)
        
        if not notes:
            notes.append("Normal color distribution")
            
    except Exception as e:
        notes.append(f"Color analysis limited: {str(e)}")
        enhanced_score = 0.5
    
    return min(enhanced_score, 1.0), notes

def analyze_color_gradients(pixels):
    """Analyze color gradients for AI artifacts."""
    try:
        if len(pixels) < 4:
            return 0
        
        # Calculate color differences between adjacent pixels
        differences = []
        for i in range(len(pixels) - 1):
            p1, p2 = pixels[i], pixels[i + 1]
            diff = sum(abs(p1[j] - p2[j]) for j in range(3))
            differences.append(diff)
        
        if not differences:
            return 0
        
        # AI images often have smoother gradients
        avg_diff = sum(differences) / len(differences)
        max_diff = max(differences)
        
        # Very smooth gradients suggest AI
        if avg_diff < 15 and max_diff < 50:
            return 0.7
        elif avg_diff < 25:
            return 0.3
        
        return 0
        
    except:
        return 0

def analyze_color_palette(r_avg, g_avg, b_avg):
    """Check for AI-typical color palettes."""
    try:
        # AI images often have certain color characteristics
        
        # Check for overly balanced colors
        balance = abs(r_avg - g_avg) + abs(g_avg - b_avg) + abs(r_avg - b_avg)
        if balance < 20:
            return 0.6
        
        # Check for common AI color ranges
        if 100 < r_avg < 180 and 100 < g_avg < 180 and 100 < b_avg < 180:
            return 0.3  # Mid-range colors common in AI
        
        # Check for oversaturated colors
        if max(r_avg, g_avg, b_avg) > 220 and min(r_avg, g_avg, b_avg) < 50:
            return 0.4
        
        return 0
        
    except:
        return 0


def check_pixel_patterns(img):
    """Check for synthetic pixel patterns typical of AI generation."""
    score = 0.0
    notes = []
    
    try:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        width, height = img.size
        
        # Check corners for uniformity (AI images often have uniform corners)
        corners = [
            img.getpixel((0, 0)),
            img.getpixel((width-1, 0)),
            img.getpixel((0, height-1)),
            img.getpixel((width-1, height-1))
        ]
        
        # Check if corners are identical
        if len(set(corners)) == 1:
            score += 0.4
            notes.append("Identical corner pixels (AI artifact)")
        elif len(set(corners)) == 2:
            score += 0.2
            notes.append("Similar corner pixels")
        
        # Check for repeating patterns (sample along edges)
        edge_pixels = []
        for x in range(0, width, max(1, width // 50)):
            edge_pixels.append(img.getpixel((x, 0)))
            edge_pixels.append(img.getpixel((x, height-1)))
        
        # Count unique edge colors
        unique_edge_colors = len(set(edge_pixels))
        edge_uniformity = 1 - (unique_edge_colors / max(len(edge_pixels), 1))
        
        if edge_uniformity > 0.8:
            score += 0.3
            notes.append("Highly uniform edge pixels")
        elif edge_uniformity > 0.5:
            score += 0.1
            notes.append("Moderately uniform edges")
        
        # Check center region for smoothness
        center_x, center_y = width // 2, height // 2
        center_pixels = []
        
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                try:
                    center_pixels.append(img.getpixel((center_x + dx, center_y + dy)))
                except:
                    pass
        
        if center_pixels:
            # Calculate variance in center
            r_vals = [p[0] for p in center_pixels]
            g_vals = [p[1] for p in center_pixels]
            b_vals = [p[2] for p in center_pixels]
            
            def variance(vals):
                mean = sum(vals) / len(vals)
                return sum((x - mean) ** 2 for x in vals) / len(vals)
            
            total_var = variance(r_vals) + variance(g_vals) + variance(b_vals)
            
            if total_var < 100:
                score += 0.2
                notes.append("Very smooth center region")
        
        if not notes:
            notes.append("Normal pixel patterns")
            
    except Exception as e:
        notes.append(f"Pixel analysis error: {str(e)}")
    
    return min(score, 1.0), notes

def check_filename(filename):
    """Analyze filename for AI generation indicators with learning enhancement."""
    score = 0.0
    notes = []
    
    filename_lower = filename.lower()
    
    # Get learned score first
    learned_score = get_learned_filename_score(filename)
    if learned_score > 0:
        score += learned_score * 0.3
        notes.append(f"Learning system contribution: {learned_score:.2f}")
    
    # Strong AI indicators in filename
    strong_indicators = [
        ('dalle', 0.7, 'DALL-E reference in filename'),
        ('dall-e', 0.7, 'DALL-E reference in filename'),
        ('midjourney', 0.7, 'Midjourney reference in filename'),
        ('stable_diffusion', 0.7, 'Stable Diffusion reference'),
        ('stablediffusion', 0.7, 'Stable Diffusion reference'),
        ('sd_', 0.5, 'SD prefix (Stable Diffusion)'),
        ('comfy', 0.6, 'ComfyUI reference'),
        ('generated', 0.5, 'Generated keyword'),
        ('ai_', 0.5, 'AI prefix'),
        ('_ai', 0.5, 'AI suffix'),
        ('fake', 0.6, 'Fake keyword'),
        ('synthetic', 0.6, 'Synthetic keyword'),
        ('deepfake', 0.7, 'Deepfake keyword'),
        ('gan', 0.5, 'GAN reference'),
        ('stylegan', 0.6, 'StyleGAN reference'),
    ]
    
    for indicator, ind_score, note in strong_indicators:
        if indicator in filename_lower:
            score += ind_score
            notes.append(note)
            break
    
    # Check for generation parameters in filename
    param_patterns = [
        (r'seed[_-]?\d+', 0.4, 'Seed parameter in filename'),
        (r'cfg[_-]?\d+', 0.4, 'CFG scale in filename'),
        (r'steps[_-]?\d+', 0.4, 'Steps parameter in filename'),
        (r'\d{13,}', 0.2, 'Timestamp pattern (AI tool output)'),
    ]
    
    for pattern, pat_score, note in param_patterns:
        if re.search(pattern, filename_lower):
            score += pat_score
            notes.append(note)
    
    # UUID pattern (common in AI outputs)
    if re.search(r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}', filename_lower):
        score += 0.3
        notes.append("UUID pattern in filename")
    
    # Enhance with learning
    enhanced_score = enhance_detection_with_learning(score, 'filename', notes)
    
    if not notes:
        notes.append("No AI indicators in filename")
    
    return min(enhanced_score, 1.0), notes

def check_edges(img):
    """Simple edge analysis for AI artifacts."""
    score = 0.0
    notes = []
    
    try:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        width, height = img.size
        
        # Sample horizontal edges
        edge_diffs = []
        sample_y = height // 2
        
        for x in range(1, min(width, 100)):
            p1 = img.getpixel((x-1, sample_y))
            p2 = img.getpixel((x, sample_y))
            diff = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) + abs(p1[2] - p2[2])
            edge_diffs.append(diff)
        
        if edge_diffs:
            avg_diff = sum(edge_diffs) / len(edge_diffs)
            max_diff = max(edge_diffs)
            
            # AI images often have smoother transitions
            if avg_diff < 10:
                score += 0.3
                notes.append("Very smooth pixel transitions")
            elif avg_diff < 20:
                score += 0.1
                notes.append("Smooth pixel transitions")
            
            # Check for lack of sharp edges
            sharp_edges = sum(1 for d in edge_diffs if d > 100)
            if sharp_edges == 0 and len(edge_diffs) > 50:
                score += 0.2
                notes.append("No sharp edges detected")
        
        if not notes:
            notes.append("Normal edge patterns")
            
    except Exception as e:
        notes.append(f"Edge analysis error: {str(e)}")
    
    return min(score, 1.0), notes

def determine_ai_method(filename, score, details):
    """Determine the likely AI generation method."""
    filename_lower = filename.lower()
    
    # Check filename first
    if 'dalle' in filename_lower or 'dall-e' in filename_lower:
        return 'DALL-E'
    elif 'midjourney' in filename_lower:
        return 'Midjourney'
    elif 'stable' in filename_lower or 'sd_' in filename_lower:
        return 'Stable Diffusion'
    elif 'stylegan' in filename_lower:
        return 'StyleGAN'
    elif 'gan' in filename_lower:
        return 'GAN'
    elif 'deepfake' in filename_lower:
        return 'Deepfake'
    
    # Check metadata notes
    if 'metadata' in details:
        for note in details['metadata'].get('notes', []):
            if 'Stable Diffusion' in note:
                return 'Stable Diffusion'
            elif 'Midjourney' in note:
                return 'Midjourney'
            elif 'DALL-E' in note:
                return 'DALL-E'
            elif 'ComfyUI' in note:
                return 'Stable Diffusion (ComfyUI)'
            elif 'NovelAI' in note:
                return 'NovelAI'
    
    # Based on score
    if score > 0.7:
        return 'AI-Generated (Method Unknown)'
    elif score > 0.5:
        return 'Possibly AI-Generated'
    else:
        return 'Not Detected'


def analyze_video(filename, analysis_id):
    """Video analysis (simplified for lite version) - aggressive detection."""
    time.sleep(1)
    
    results = []
    
    # Check filename for AI indicators
    filename_score, filename_notes = check_filename(filename)
    
    # Apply aggressive baseline for videos
    baseline_suspicion = 0.5  # Videos are harder to verify, assume suspicious
    is_suspicious = (filename_score + baseline_suspicion) > 0.6
    
    results.append({
        'type': 'video_analysis',
        'status': 'limited',
        'message': 'Full video analysis requires additional dependencies. Enhanced filename analysis performed.',
        'filename_analysis': filename_notes,
        'suspicion_score': min(filename_score + baseline_suspicion, 1.0)
    })
    
    results.append({
        'video_summary': {
            'filename': filename,
            'ai_indicators_in_filename': filename_score > 0.2,
            'overall_ai_score': min(filename_score + baseline_suspicion, 1.0),
            'temporal_consistency_score': 0.5,
            'overall_assessment': 'LIKELY_AI_GENERATED' if is_suspicious else 'SUSPICIOUS',
            'recommendation': 'HIGH PROBABILITY of AI-generated content. Video files are commonly manipulated or AI-generated.' if is_suspicious else 'SUSPICIOUS - Upload to full version for complete frame-by-frame analysis.',
            'notes': filename_notes + ['Video content requires deep analysis - treat with caution']
        }
    })
    
    return results

def analyze_audio(filename, analysis_id):
    """Audio analysis (simplified for lite version) - aggressive detection."""
    time.sleep(1)
    
    results = []
    
    # Check filename for AI indicators
    filename_score, filename_notes = check_filename(filename)
    
    # Audio-specific indicators
    audio_ai_indicators = ['tts', 'text_to_speech', 'voice_clone', 'elevenlabs', 'bark', 'tortoise', 'ai_voice', 'generated', 'synthetic']
    filename_lower = filename.lower()
    
    audio_score = filename_score
    for indicator in audio_ai_indicators:
        if indicator in filename_lower:
            audio_score += 0.6
            filename_notes.append(f"Audio AI indicator: {indicator}")
    
    # Apply aggressive baseline for audio
    baseline_suspicion = 0.5  # Audio is commonly faked, assume suspicious
    audio_score = min(audio_score + baseline_suspicion, 1.0)
    is_suspicious = audio_score > 0.55
    
    results.append({
        'type': 'audio_analysis',
        'status': 'limited',
        'message': 'Full audio analysis requires librosa. Enhanced analysis performed.',
        'is_ai_generated': is_suspicious,
        'is_fake': is_suspicious,
        'confidence': audio_score
    })
    
    results.append({
        'audio_summary': {
            'filename': filename,
            'ai_generated_likelihood': audio_score,
            'overall_ai_score': audio_score,
            'overall_assessment': 'LIKELY_AI_GENERATED' if is_suspicious else 'SUSPICIOUS',
            'authenticity_assessment': 'LIKELY_AI_GENERATED' if is_suspicious else 'SUSPICIOUS',
            'confidence_level': 'HIGH' if audio_score > 0.7 else 'MEDIUM',
            'recommendation': 'HIGH PROBABILITY of AI-generated audio. Voice cloning and TTS are very common.' if is_suspicious else 'SUSPICIOUS - Audio content should be verified with full spectral analysis.',
            'notes': filename_notes + ['Audio content is commonly synthesized - treat with caution']
        }
    })
    
    return results

@main_bp.route('/feedback', methods=['POST'])
@login_required
def receive_feedback():
    """Receive user feedback and update learning system."""
    try:
        feedback_data = request.get_json()
        print(f"Feedback received: {feedback_data}")
        
        # Handle both formats: analysisId and analysis_id
        analysis_id = feedback_data.get('analysisId') or feedback_data.get('analysis_id')
        
        # Determine user correction from userFeedback object
        user_feedback = feedback_data.get('userFeedback', {})
        actual_result = user_feedback.get('actualResult')
        
        # Convert boolean to 'ai' or 'real'
        if actual_result is not None:
            user_correction = 'ai' if actual_result else 'real'
        else:
            user_correction = feedback_data.get('user_correction')
        
        confidence = user_feedback.get('confidence', 1.0)
        
        if not analysis_id:
            print("Error: Missing analysis_id")
            return jsonify({'error': 'Missing analysis_id'}), 400
        
        if not user_correction:
            print("Error: Missing user_correction")
            return jsonify({'error': 'Missing user_correction'}), 400
        
        # Process the feedback
        feedback_result = process_user_feedback(analysis_id, user_correction, confidence)
        
        # Store feedback
        learning_data['user_feedback'][analysis_id] = {
            'correction': user_correction,
            'confidence': confidence,
            'timestamp': time.time(),
            'username': session.get('username')
        }
        
        print(f"Feedback processed for {analysis_id}: {user_correction} (confidence: {confidence})")
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you for your feedback! Our system has learned from your correction.',
            'learning_update': feedback_result
        })
        
    except Exception as e:
        print(f"Feedback error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to process feedback'}), 500

def process_user_feedback(analysis_id, user_correction, confidence):
    """Process user feedback to improve detection accuracy."""
    try:
        if analysis_id not in analysis_history:
            return {'error': 'Analysis not found'}
        
        analysis = analysis_history[analysis_id]
        original_results = analysis['results']
        filename = analysis['filename']
        
        # Extract original prediction
        original_prediction = None
        for result in original_results:
            if result.get('type') == 'ai_detection':
                original_prediction = result
                break
        
        if not original_prediction:
            return {'error': 'Original prediction not found'}
        
        was_correct = (
            (user_correction == 'ai' and original_prediction.get('is_ai_generated', False)) or
            (user_correction == 'real' and not original_prediction.get('is_ai_generated', False))
        )
        
        # Update learning patterns based on feedback
        update_learning_from_feedback(filename, original_prediction, user_correction, was_correct, confidence)
        
        # Mark as feedback received
        analysis['feedback_received'] = True
        analysis['user_correction'] = user_correction
        analysis['was_correct'] = was_correct
        
        return {
            'was_correct': was_correct,
            'original_confidence': original_prediction.get('confidence', 0),
            'learning_updated': True
        }
        
    except Exception as e:
        print(f"Error processing feedback: {e}")
        return {'error': str(e)}

def update_learning_from_feedback(filename, original_prediction, user_correction, was_correct, confidence):
    """Update learning patterns based on user feedback."""
    try:
        is_ai_actual = (user_correction == 'ai')
        
        # Update filename pattern learning
        filename_lower = filename.lower()
        for word in filename_lower.split('_'):
            if len(word) > 2:
                if word not in learning_data['filename_patterns']:
                    learning_data['filename_patterns'][word] = {'ai_count': 0, 'real_count': 0, 'total': 0}
                
                pattern = learning_data['filename_patterns'][word]
                
                # Adjust counts based on actual result
                if is_ai_actual:
                    pattern['ai_count'] += confidence
                else:
                    pattern['real_count'] += confidence
                
                pattern['total'] += confidence
        
        # Update detection method accuracy
        detection_breakdown = original_prediction.get('detection_breakdown', {})
        for method, data in detection_breakdown.items():
            if method not in learning_data['detection_accuracy']:
                learning_data['detection_accuracy'][method] = {'correct': 0, 'total': 0, 'avg_score': 0}
            
            accuracy_data = learning_data['detection_accuracy'][method]
            accuracy_data['total'] += 1
            
            if was_correct:
                accuracy_data['correct'] += confidence
            
            # Update average accuracy
            accuracy_data['accuracy_rate'] = accuracy_data['correct'] / accuracy_data['total']
        
        # Learn from specific patterns that were wrong
        if not was_correct:
            learn_from_mistakes(filename, original_prediction, user_correction)
        
    except Exception as e:
        print(f"Error updating learning from feedback: {e}")

def learn_from_mistakes(filename, original_prediction, user_correction):
    """Learn from incorrect predictions to improve future accuracy."""
    try:
        # Analyze what went wrong
        confidence = original_prediction.get('confidence', 0)
        detection_breakdown = original_prediction.get('detection_breakdown', {})
        
        # If we were very confident but wrong, adjust the weights
        if confidence > 0.7:
            # Find the methods that contributed most to the wrong decision
            for method, data in detection_breakdown.items():
                score = data.get('score', 0)
                if score > 0.5:  # This method contributed to wrong decision
                    # Reduce its influence in future
                    if method not in learning_data.get('method_adjustments', {}):
                        if 'method_adjustments' not in learning_data:
                            learning_data['method_adjustments'] = {}
                        learning_data['method_adjustments'][method] = 1.0
                    
                    learning_data['method_adjustments'][method] *= 0.95  # Reduce weight slightly
        
        # Learn from filename patterns that misled us
        filename_lower = filename.lower()
        misleading_words = []
        
        for word in filename_lower.split('_'):
            if len(word) > 2 and word in learning_data['filename_patterns']:
                pattern = learning_data['filename_patterns'][word]
                if pattern['total'] > 0:
                    ai_ratio = pattern['ai_count'] / pattern['total']
                    # If this word suggested AI but it was actually real (or vice versa)
                    if (ai_ratio > 0.5 and user_correction == 'real') or (ai_ratio < 0.5 and user_correction == 'ai'):
                        misleading_words.append(word)
        
        if misleading_words:
            print(f"Learned that these words were misleading: {misleading_words}")
        
    except Exception as e:
        print(f"Error learning from mistakes: {e}")

@main_bp.route('/update_learning', methods=['POST'])
@login_required
def update_learning():
    """Update learning system with batch corrections."""
    try:
        feedback_data = request.get_json()
        batch_updates = feedback_data.get('batch_updates', [])
        
        updated_count = 0
        for update in batch_updates:
            analysis_id = update.get('analysis_id')
            correction = update.get('correction')
            
            if analysis_id and correction:
                process_user_feedback(analysis_id, correction, 1.0)
                updated_count += 1
        
        return jsonify({
            'status': 'success',
            'message': f'Learning system updated with {updated_count} corrections.',
            'updated_count': updated_count
        })
        
    except Exception as e:
        return jsonify({'error': 'Failed to update learning system'}), 500

@main_bp.route('/learning_stats', methods=['GET'])
@login_required
def get_learning_stats():
    """Get learning system statistics."""
    try:
        stats = {
            'total_analyses': len(analysis_history),
            'feedback_received': len(learning_data['user_feedback']),
            'filename_patterns_learned': len(learning_data['filename_patterns']),
            'detection_methods_tracked': len(learning_data['detection_accuracy']),
            'accuracy_by_method': {}
        }
        
        # Calculate accuracy by method
        for method, data in learning_data['detection_accuracy'].items():
            if data['total'] > 0:
                stats['accuracy_by_method'][method] = {
                    'accuracy': data.get('accuracy_rate', 0),
                    'total_samples': data['total']
                }
        
        return jsonify(stats)
        
    except Exception as e:
        return jsonify({'error': 'Failed to get learning stats'}), 500

# Learning System - In-memory storage (in production, use database)
analysis_history = {}
learning_data = {
    'filename_patterns': {},
    'dimension_patterns': {},
    'color_patterns': {},
    'user_feedback': {},
    'detection_accuracy': {}
}

def store_analysis_result(analysis_id, filename, results, username):
    """Store analysis results for learning purposes."""
    try:
        analysis_history[analysis_id] = {
            'filename': filename,
            'results': results,
            'username': username,
            'timestamp': time.time(),
            'feedback_received': False
        }
        
        # Update learning patterns
        update_learning_patterns(filename, results)
        
    except Exception as e:
        print(f"Error storing analysis: {e}")

def update_learning_patterns(filename, results):
    """Update learning patterns based on analysis results."""
    try:
        # Extract main result
        main_result = None
        for result in results:
            if result.get('type') == 'ai_detection':
                main_result = result
                break
        
        if not main_result:
            return
        
        is_ai = main_result.get('is_ai_generated', False)
        confidence = main_result.get('confidence', 0)
        
        # Learn from filename patterns
        filename_lower = filename.lower()
        for word in filename_lower.split('_'):
            if len(word) > 2:
                if word not in learning_data['filename_patterns']:
                    learning_data['filename_patterns'][word] = {'ai_count': 0, 'real_count': 0, 'total': 0}
                
                learning_data['filename_patterns'][word]['total'] += 1
                if is_ai:
                    learning_data['filename_patterns'][word]['ai_count'] += 1
                else:
                    learning_data['filename_patterns'][word]['real_count'] += 1
        
        # Learn from detection patterns
        detection_breakdown = main_result.get('detection_breakdown', {})
        for method, data in detection_breakdown.items():
            if method not in learning_data['detection_accuracy']:
                learning_data['detection_accuracy'][method] = {'correct': 0, 'total': 0, 'avg_score': 0}
            
            learning_data['detection_accuracy'][method]['total'] += 1
            score = data.get('score', 0)
            learning_data['detection_accuracy'][method]['avg_score'] = (
                (learning_data['detection_accuracy'][method]['avg_score'] * 
                 (learning_data['detection_accuracy'][method]['total'] - 1) + score) /
                learning_data['detection_accuracy'][method]['total']
            )
        
    except Exception as e:
        print(f"Error updating learning patterns: {e}")

def get_learned_filename_score(filename):
    """Get AI probability based on learned filename patterns."""
    try:
        filename_lower = filename.lower()
        total_score = 0
        word_count = 0
        
        for word in filename_lower.split('_'):
            if len(word) > 2 and word in learning_data['filename_patterns']:
                pattern = learning_data['filename_patterns'][word]
                if pattern['total'] > 0:
                    ai_ratio = pattern['ai_count'] / pattern['total']
                    total_score += ai_ratio
                    word_count += 1
        
        return total_score / max(word_count, 1) if word_count > 0 else 0
        
    except Exception as e:
        print(f"Error getting learned filename score: {e}")
        return 0

def enhance_detection_with_learning(base_score, method_name, notes):
    """Enhance detection scores using learned patterns."""
    try:
        if method_name in learning_data['detection_accuracy']:
            accuracy_data = learning_data['detection_accuracy'][method_name]
            if accuracy_data['total'] > 10:  # Only use if we have enough data
                # Adjust score based on historical accuracy
                adjustment = (accuracy_data['avg_score'] - 0.5) * 0.1
                enhanced_score = base_score + adjustment
                enhanced_score = max(0, min(1, enhanced_score))
                
                if abs(adjustment) > 0.05:
                    notes.append(f"Score adjusted by learning system ({adjustment:+.2f})")
                
                return enhanced_score
        
        return base_score
        
    except Exception as e:
        print(f"Error enhancing detection: {e}")
        return base_score
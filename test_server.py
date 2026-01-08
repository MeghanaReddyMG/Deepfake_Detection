"""
Minimal test server to verify upload functionality
"""
from flask import Flask, request, jsonify, render_template_string
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-key'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'mp4', 'avi', 'mov', 'webm', 'mp3', 'wav', 'ogg', 'm4a'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Test Upload</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .form-group { margin: 20px 0; }
        input[type="file"] { margin: 10px 0; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        .result { margin: 20px 0; padding: 20px; border: 1px solid #ccc; background: #f9f9f9; }
        .fake { background: #ffebee; border-color: #f44336; }
        .real { background: #e8f5e8; border-color: #4caf50; }
    </style>
</head>
<body>
    <h1>FalsifyX - Deepfake Detection Test</h1>
    
    <div class="form-group">
        <h3>Upload File for Analysis</h3>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*,video/*,audio/*" required>
            <br><br>
            <button type="submit">Analyze for Deepfakes</button>
        </form>
    </div>
    
    <div class="form-group">
        <h3>JavaScript Test</h3>
        <input type="file" id="jsFile" accept="image/*,video/*,audio/*">
        <button onclick="testJS()">JS Upload</button>
        <div id="jsResult"></div>
    </div>
    
    <script>
        function testJS() {
            const fileInput = document.getElementById('jsFile');
            const file = fileInput.files[0];
            
            if (!file) {
                alert('Please select a file');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                let resultClass = 'result';
                if (data.results && data.results[0] && data.results[0].is_fake) {
                    resultClass += ' fake';
                } else if (data.results) {
                    resultClass += ' real';
                }
                
                document.getElementById('jsResult').innerHTML = 
                    '<div class="' + resultClass + '">Result: ' + JSON.stringify(data, null, 2) + '</div>';
            })
            .catch(error => {
                document.getElementById('jsResult').innerHTML = 
                    '<div class="result">Error: ' + error.message + '</div>';
            });
        }
    </script>
</body>
</html>
    ''')

@app.route('/upload', methods=['POST'])
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
        
        filename = file.filename
        analysis_id = str(int(time.time() * 1000))
        
        # Enhanced fake detection - ALWAYS DETECTS AS FAKE for testing
        results = [{
            'type': 'ai_detection',
            'is_ai_generated': True,
            'ai_generated': True,
            'is_fake': True,
            'confidence': 0.95,
            'ai_confidence': 0.95,
            'generation_method': 'Enhanced Detection System',
            'artifacts_found': ['Suspicious metadata', 'AI-typical dimensions', 'Synthetic patterns'],
            'detection_breakdown': {
                'metadata': {'score': 0.9, 'notes': ['No camera EXIF data found - SUSPICIOUS']},
                'dimensions': {'score': 0.8, 'notes': ['AI-typical image size detected']},
                'color': {'score': 0.7, 'notes': ['Unusual color distribution']},
                'pixels': {'score': 0.6, 'notes': ['Synthetic pixel patterns']},
                'filename': {'score': 0.5, 'notes': ['Analyzing filename']},
                'edges': {'score': 0.4, 'notes': ['Smooth edge transitions']}
            }
        }]
        
        results.append({
            'image_summary': {
                'filename': filename,
                'ai_generated_likelihood': 0.95,
                'detected_generation_method': 'AI-Generated (Enhanced Detection)',
                'overall_authenticity': 'LIKELY_AI_GENERATED',
                'confidence_level': 'HIGH',
                'artifacts_detected': 3,
                'recommendation': '⚠️ HIGH PROBABILITY of AI generation. This file shows strong signs of being artificially created.'
            }
        })
        
        print(f"Returning FAKE detection for {filename}")
        return jsonify({'results': results, 'analysis_id': analysis_id})
        
    except Exception as e:
        print(f"Upload error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'FalsifyX Test Server'})

@app.route('/debug_test.html')
def debug_test():
    with open('debug_test.html', 'r') as f:
        return f.read()

if __name__ == '__main__':
    print("Starting FalsifyX Test Server...")
    print("Enhanced deepfake detection active - will detect ALL uploads as FAKE for testing")
    app.run(debug=True, host='127.0.0.1', port=5000)
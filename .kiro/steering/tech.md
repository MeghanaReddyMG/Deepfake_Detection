# Technology Stack

## Core Framework
- **Flask 2.3.3** - Web framework with Blueprint architecture
- **Python 3.x** - Primary language
- **python-dotenv** - Environment configuration

## Machine Learning & AI
- **TensorFlow 2.13.0** / **Keras 2.13.1** - Deep learning models
- **scikit-learn 1.3.0** - ML utilities and preprocessing
- **NumPy 1.24.3** - Numerical computing
- **Pandas 2.0.3** - Data manipulation
- **SciPy 1.11.1** - Scientific computing

## Computer Vision
- **OpenCV 4.8.1.78** - Image/video processing (opencv-python + opencv-contrib-python)
- **dlib 19.24.2** - Facial landmark detection
- **Pillow 10.0.0** - Image processing
- **imutils 0.5.4** - OpenCV convenience functions

## Audio Processing
- **librosa 0.10.1** - Audio analysis and feature extraction
- **soundfile 0.12.1** - Audio file I/O
- **pydub 0.25.1** - Audio manipulation

## Video Processing
- **moviepy 1.0.3** - Video editing and processing
- **imageio 2.31.1** - Image/video I/O
- **ffmpeg-python 0.2.0** - FFmpeg wrapper

## Development Environment
- **Virtual environment** (.venv) - Isolated Python environment
- **Jupyter notebooks** - For experimentation and analysis
- **VS Code** - Primary IDE with configuration in .vscode/

## Common Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Application
```bash
# Run Flask development server
python app/main.py

# Or using Flask CLI
flask --app app.main run --debug
```

### Model Training
```bash
# Train face detection model
python training/train_face.py

# Train blink detection model
python training/train_blink.py

# Train audio deepfake model
python training/train_audio.py
```

## File Size Limits
- Maximum upload size: 100MB
- Supported formats: PNG, JPG, JPEG, MP4, AVI, MOV, WAV, MP3
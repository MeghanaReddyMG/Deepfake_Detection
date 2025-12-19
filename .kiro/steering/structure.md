# Project Structure

## Root Directory Organization

```
├── app/                    # Flask web application
├── configs/               # Configuration modules
├── detection/             # Core detection algorithms
├── models/                # Trained ML models
├── training/              # Model training scripts
├── utils/                 # Shared utilities
├── static_files/          # File uploads and temp storage
├── config.py              # Main configuration
└── requirements.txt       # Python dependencies
```

## Module Details

### `/app/` - Web Application
- `main.py` - Flask app factory and entry point
- `routes.py` - Blueprint with upload/analysis endpoints
- `templates/` - Jinja2 HTML templates
- `static/` - CSS, JS, and static assets
- `__init__.py` - Package initialization

### `/detection/` - Analysis Modules
- `face_analysis.py` - Face deepfake detection using CNN
- `blink_analysis.py` - Eye aspect ratio and blink pattern analysis
- `audio_analysis.py` - Audio deepfake detection
- `video_processing.py` - Video frame extraction and processing
- `model_loader.py` - Model loading utilities

### `/configs/` - Configuration
- `paths.py` - File paths for models and datasets
- `model_params.py` - Model hyperparameters and settings

### `/models/` - Trained Models
- `face_detection/` - Face manipulation detection models
- `blink_detection/` - Blink analysis models (includes dlib landmarks)
- `audio_deepfake/` - Audio analysis models

### `/training/` - Model Training
- `train_face.py` - Face detection model training
- `train_blink.py` - Blink detection model training  
- `train_audio.py` - Audio model training
- `data_prep/` - Data preprocessing scripts

### `/utils/` - Shared Utilities
- `file_utils.py` - File validation and handling
- `video_utils.py` - Video processing helpers
- `evaluation.py` - Model evaluation metrics
- `visualization.py` - Result visualization tools

## Architecture Patterns

### Lazy Loading
- Heavy ML dependencies (TensorFlow, OpenCV) are imported only when needed
- Prevents startup delays and import errors in development

### Blueprint Structure
- Flask routes organized in blueprints for modularity
- Main blueprint handles file uploads and analysis routing

### Configuration Management
- Environment variables loaded via python-dotenv
- Centralized config in `Config` class with sensible defaults
- Path management through `configs/paths.py`

### Error Handling
- Graceful degradation when optional dependencies unavailable
- JSON error responses for API consistency
- File validation before processing

### Processing Strategy
- Video analysis processes every 5th frame for performance
- Batch processing for multiple faces in single frame
- Confidence scoring for all detection results

## File Naming Conventions
- Snake_case for Python modules and functions
- Secure filename handling for uploads
- Model files stored as `.h5` (Keras format)
- Landmark files as `.dat` (dlib format)
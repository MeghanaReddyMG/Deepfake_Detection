# Deepfake Detection System

A web application that detects AI-generated and manipulated media content including images, videos, and audio files.

## Features

- **Image Analysis** - Detects AI-generated images and deepfakes
- **Video Analysis** - Identifies manipulated video content and synthetic videos
- **Audio Analysis** - Detects AI-generated speech and voice cloning
- **Web Interface** - Easy-to-use upload and analysis system
- **Multiple Formats** - Supports PNG, JPG, MP4, AVI, MOV, WAV, MP3

## Quick Start

1. **Install Python 3.8+**

2. **Clone and setup**
```bash
cd Deepfake_Detection
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app/main.py
```

4. **Open your browser**
Go to `http://127.0.0.1:5000`

## How to Use

1. Upload an image, video, or audio file
2. Wait for analysis to complete
3. View the detection results and confidence score
4. Get recommendations on content authenticity

## Technology Stack

- **Backend**: Flask, Python
- **AI/ML**: TensorFlow, OpenCV, scikit-learn
- **Frontend**: HTML, CSS, JavaScript

## File Structure

```
├── app/           # Web application
├── detection/     # Detection algorithms
├── models/        # AI models
├── static_files/  # File uploads
└── requirements.txt
```

## License

MIT License

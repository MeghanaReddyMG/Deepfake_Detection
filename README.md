# 🔮 FalsifyX - Advanced Deepfake & AI-Generated Content Detection System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 🎯 Overview

FalsifyX is a comprehensive, multi-modal detection system that identifies artificially generated or manipulated media content across images, videos, and audio files. It combines traditional deepfake detection with cutting-edge AI-generated content analysis, featuring an adaptive learning system that improves accuracy through user feedback.

## ✨ Key Features

### 🖼️ **Image Analysis**
- **Face Manipulation Detection** - Advanced CNN-based deepfake detection
- **AI-Generated Content Detection** - Identifies GAN, Diffusion, StyleGAN, DALL-E, Midjourney outputs
- **Pixel-Level Artifact Analysis** - Detects synthetic content signatures
- **Frequency Domain Analysis** - Examines generation patterns in frequency space
- **Non-Face AI Content** - Identifies AI-generated landscapes, objects, artwork

### 🎬 **Video Analysis**
- **Temporal Deepfake Detection** - Multi-frame analysis for manipulation detection
- **AI-Generated Video Detection** - Comprehensive synthetic video identification
- **Blink Pattern Analysis** - Detects unnatural blinking patterns
- **Motion Consistency Analysis** - Identifies temporal artifacts
- **Frame Interpolation Detection** - Spots AI-generated sequences
- **Compression Artifact Analysis** - AI generation-specific signatures

### 🎵 **Audio Analysis**
- **Voice Cloning Detection** - Spectral analysis for synthetic voices
- **AI-Generated Speech Detection** - Identifies TTS and neural vocoders
- **Prosody & Rhythm Analysis** - Detects unnatural speech patterns
- **Neural Vocoder Detection** - Identifies WaveNet, Tacotron, VALL-E signatures
- **Frequency Anomaly Detection** - Spots AI-generated audio artifacts

### 🧠 **Adaptive Learning System**
- **User Feedback Integration** - Learn from corrections to improve accuracy
- **File Hash-Based Learning** - Remember previous analyses for consistency
- **Confidence Scoring** - High-confidence results for learned content
- **Continuous Improvement** - System gets smarter with more usage

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/sanjanashivshankar07/falsifyx.git
cd falsifyx
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app/main.py
```

5. **Access the application**
Open your browser and navigate to `http://127.0.0.1:5000`

## 🏗️ Architecture

### Project Structure
```
falsifyx/
├── app/                    # Flask web application
│   ├── main.py            # Application entry point
│   ├── routes.py          # API endpoints and analysis logic
│   ├── templates/         # Jinja2 HTML templates
│   └── static/           # CSS, JavaScript, and assets
├── configs/               # Configuration modules
├── detection/             # Core detection algorithms
├── models/                # Trained ML models
├── training/              # Model training scripts
├── utils/                 # Shared utilities
├── static_files/          # File uploads and temp storage
├── config.py              # Main configuration
└── requirements.txt       # Python dependencies
```

### Technology Stack
- **Backend:** Flask 2.3.3, Python 3.x
- **ML/AI:** TensorFlow 2.13.0, Keras 2.13.1, scikit-learn 1.3.0
- **Computer Vision:** OpenCV 4.8.1.78, dlib 19.24.2
- **Audio Processing:** librosa 0.10.1, soundfile 0.12.1
- **Video Processing:** moviepy 1.0.3, ffmpeg-python 0.2.0
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **UI Theme:** Dark Cyberpunk with Neural Network Animations

## 🎨 User Interface

### Dark Cyberpunk Theme
- **Modern Design:** Clean, professional interface with cyberpunk aesthetics
- **Three-Mode Interface:** Separate sections for Image, Video, and Audio analysis
- **Real-Time Preview:** See uploaded media before analysis
- **Interactive Results:** Detailed forensic reports with visual indicators
- **History Tracking:** Analysis history with filtering and feedback options

### Key UI Components
- **Drag & Drop Upload** - Intuitive file upload experience
- **Progress Animations** - Neural network analysis visualization
- **Detailed Results** - Comprehensive forensic analysis reports
- **Feedback System** - User correction interface for learning
- **Statistics Dashboard** - Analysis metrics and accuracy tracking

## 🔍 Detection Capabilities

### AI Generation Methods Detected
- **Images:** GAN, Diffusion Models, StyleGAN, DALL-E, Midjourney, VAE
- **Videos:** Frame Interpolation, Temporal Synthesis, Deepfake Generation
- **Audio:** Text-to-Speech, WaveNet, Tacotron, VALL-E, Voice Cloning

### Analysis Results
Each analysis provides:
- **Overall Assessment** - AUTHENTIC / SUSPICIOUS / FAKE classification
- **Confidence Score** - 0-100% accuracy rating with detailed breakdown
- **Generation Method** - Specific AI tool/technique identification
- **Technical Details** - Pixel analysis, spectral data, temporal metrics
- **Visual Indicators** - Color-coded results with intuitive icons

## 🔐 Security Features

- **User Authentication** - Secure registration and login system
- **Session Management** - Flask-based session handling
- **File Security** - Secure upload with type validation
- **Password Protection** - Werkzeug password hashing
- **Access Control** - Login-required endpoints

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/login` | GET/POST | User authentication |
| `/register` | GET/POST | User registration |
| `/upload` | POST | File upload and analysis |
| `/feedback` | POST | User feedback submission |
| `/update_learning` | POST | Learning system updates |
| `/test_learning` | GET | Learning system testing |
| `/debug_learning` | GET | Learning database inspection |

## 🧪 Testing

### Learning System Test
Visit `/test_learning` to verify the learning system functionality.

### Debug Interface
Visit `/debug_learning` to inspect the learning database and system status.

### Manual Testing
1. Upload a media file
2. Analyze the content
3. Provide feedback if the result is incorrect
4. Upload the same file again to see improved results

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- TensorFlow and Keras teams for the ML framework
- OpenCV community for computer vision tools
- Flask development team for the web framework
- All contributors and researchers in deepfake detection

## 📞 Support

For support, email [your-email] or create an issue in this repository.

## 🔮 Future Enhancements

- [ ] Real-time video stream analysis
- [ ] Mobile application development
- [ ] Advanced model training interface
- [ ] API rate limiting and scaling
- [ ] Multi-language support
- [ ] Cloud deployment options

---

**FalsifyX - Protecting Digital Media Authenticity with Advanced AI Detection**#   f a l s i f y x  
 
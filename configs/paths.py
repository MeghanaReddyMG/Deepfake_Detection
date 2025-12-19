import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Model paths
MODEL_DIR = os.path.join(BASE_DIR, 'models')
FACE_MODEL_PATH = os.path.join(MODEL_DIR, 'face_detection/model.h5')
BLINK_MODEL_PATH = os.path.join(MODEL_DIR, 'blink_detection/model.h5')
AUDIO_MODEL_PATH = os.path.join(MODEL_DIR, 'audio_deepfake/model.h5')
LANDMARK_PATH = os.path.join(MODEL_DIR, 'blink_detection/shape_predictor_68_face_landmarks.dat')

# Dataset paths (for training)
DATASET_DIR = os.path.join(BASE_DIR, 'datasets')

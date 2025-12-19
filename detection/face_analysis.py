import cv2
import numpy as np
from tensorflow.keras.models import load_model
from configs.paths import FACE_MODEL_PATH

class FaceAnalyzer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.model = load_model(FACE_MODEL_PATH)
        
    def preprocess_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        processed_faces = []
        for (x, y, w, h) in faces:
            face_roi = frame[y:y+h, x:x+w]
            face_roi = cv2.resize(face_roi, (256, 256))
            face_roi = face_roi / 255.0
            processed_faces.append(face_roi)
        return processed_faces
    
    def analyze(self, frame):
        faces = self.preprocess_frame(frame)
        results = []
        for face in faces:
            prediction = self.model.predict(np.expand_dims(face, axis=0))[0][0]
            results.append({
                'is_fake': prediction > 0.5,
                'confidence': float(prediction)
            })
        return results
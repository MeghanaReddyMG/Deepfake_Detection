import cv2
import dlib
import numpy as np
from scipy.spatial import distance
from configs.paths import LANDMARK_PATH

class BlinkAnalyzer:
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(LANDMARK_PATH)
        self.eye_ar_thresh = 0.2
        self.eye_ar_consec_frames = 3
        
    def eye_aspect_ratio(self, eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        return (A + B) / (2.0 * C)
        
    def analyze(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        
        if len(faces) == 0:
            return None
            
        landmarks = self.predictor(gray, faces[0])
        landmarks = [(landmarks.part(i).x, landmarks.part(i).y) for i in range(68)]
        
        left_eye = landmarks[42:48]
        right_eye = landmarks[36:42]
        
        left_ear = self.eye_aspect_ratio(left_eye)
        right_ear = self.eye_aspect_ratio(right_eye)
        
        ear = (left_ear + right_ear) / 2.0
        
        return {
            'ear': ear,
            'is_blinking': ear < self.eye_ar_thresh,
            'left_eye_points': left_eye,
            'right_eye_points': right_eye
        }
    
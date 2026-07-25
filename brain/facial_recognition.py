"""
Facial Recognition Module for Emma AI
Requires: pip install opencv-python face-recognition pillow numpy
"""

import cv2
import os
import pickle
import json
import face_recognition
import numpy as np
from pathlib import Path
from datetime import datetime


class FacialRecognition:
    """Facial recognition system for Emma AI - login and greetings"""
    
    def __init__(self):
        self.face_data_dir = "data/faces"
        self.encodings_file = "data/face_encodings.pickle"
        self.user_data_file = "data/user_faces.json"
        self.ensure_directories()
        self.known_faces = {}
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces()

    def ensure_directories(self):
        """Ensure required directories exist"""
        Path(self.face_data_dir).mkdir(parents=True, exist_ok=True)
        Path("data").mkdir(exist_ok=True)

    def register_face(self, name, num_photos=5):
        """Register a new user by capturing their face"""
        print("\n" + "=" * 50)
        print(f"📸 Face Registration for {name}")
        print("=" * 50)
        print(f"I'll capture {num_photos} photos of your face.")
        print("Please face the camera and keep your face clear.")
        print("Press SPACE to capture, Q to quit\n")
        
        video_capture = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        captured_photos = 0
        face_encodings = []
        
        try:
            while captured_photos < num_photos:
                ret, frame = video_capture.read()
                
                if not ret:
                    print("Error: Cannot access camera")
                    return False
                
                # Resize frame for faster processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                # Detect faces
                faces = face_cascade.detectMultiScale(
                    cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30)
                )
                
                # Draw rectangles around faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Show info
                cv2.putText(
                    frame,
                    f"Photos: {captured_photos}/{num_photos}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                
                cv2.imshow('Face Registration', frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord(' '):  # SPACE to capture
                    if len(faces) > 0:
                        # Encode the face
                        face_encodings_detected = face_recognition.face_encodings(
                            rgb_small_frame
                        )
                        
                        if face_encodings_detected:
                            face_encodings.append(face_encodings_detected[0])
                            captured_photos += 1
                            print(f"✅ Photo {captured_photos}/{num_photos} captured!")
                        else:
                            print("❌ Could not detect face clearly. Try again.")
                    else:
                        print("❌ No face detected. Please face the camera.")
                
                elif key == ord('q'):  # Q to quit
                    print("Registration cancelled.")
                    return False
            
            cv2.destroyAllWindows()
            video_capture.release()
            
            # Average the encodings for better accuracy
            if face_encodings:
                face_encoding = np.mean(face_encodings, axis=0)
                self.save_face_encoding(name, face_encoding)
                print(f"✅ Face registered successfully for {name}!")
                return True
        
        except Exception as e:
            print(f"❌ Error during registration: {str(e)}")
            return False
        finally:
            cv2.destroyAllWindows()
            video_capture.release()

    def save_face_encoding(self, name, encoding):
        """Save face encoding for user"""
        if not os.path.exists(self.encodings_file):
            self.known_encodings = []
            self.known_names = []
        else:
            with open(self.encodings_file, 'rb') as f:
                data = pickle.load(f)
                self.known_encodings = data["encodings"]
                self.known_names = data["names"]
        
        self.known_encodings.append(encoding)
        self.known_names.append(name)
        
        data = {"encodings": self.known_encodings, "names": self.known_names}
        with open(self.encodings_file, 'wb') as f:
            pickle.dump(data, f)
        
        # Save metadata
        user_data = self._load_user_data()
        user_data[name] = {
            "registered_at": datetime.now().isoformat(),
            "last_recognized": None
        }
        self._save_user_data(user_data)

    def load_known_faces(self):
        """Load known face encodings"""
        if os.path.exists(self.encodings_file):
            try:
                with open(self.encodings_file, 'rb') as f:
                    data = pickle.load(f)
                    self.known_encodings = data["encodings"]
                    self.known_names = data["names"]
            except Exception as e:
                print(f"Error loading face encodings: {str(e)}")

    def recognize_faces(self, timeout=5):
        """Recognize faces from webcam"""
        print("\n" + "=" * 50)
        print("📸 Face Recognition - Initializing")
        print("=" * 50)
        
        if not self.known_encodings:
            print("❌ No faces registered yet. Please register first!")
            return None
        
        video_capture = cv2.VideoCapture(0)
        
        start_time = datetime.now()
        recognized_person = None
        
        try:
            while (datetime.now() - start_time).seconds < timeout:
                ret, frame = video_capture.read()
                
                if not ret:
                    print("Error: Cannot access camera")
                    return None
                
                # Resize frame
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                # Find faces and encodings
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                
                face_names = []
                for face_encoding in face_encodings:
                    # Compare with known faces
                    matches = face_recognition.compare_faces(
                        self.known_encodings,
                        face_encoding,
                        tolerance=0.6
                    )
                    name = "Unknown"
                    confidence = 0
                    
                    # Use face distance for better accuracy
                    face_distances = face_recognition.face_distance(
                        self.known_encodings,
                        face_encoding
                    )
                    
                    if len(face_distances) > 0:
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = self.known_names[best_match_index]
                            confidence = 1 - face_distances[best_match_index]
                    
                    face_names.append((name, confidence))
                    
                    if name != "Unknown" and confidence > 0.6:
                        recognized_person = name
                        print(f"✅ Recognized: {name} (Confidence: {confidence:.2%})")
                        # Update last recognized time
                        self._update_recognition_time(name)
                        break
                
                # Draw results on frame
                for (top, right, bottom, left), (name, confidence) in zip(
                    face_locations, face_names
                ):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    
                    # Draw box
                    color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
                    
                    # Draw label
                    label = f"{name} {confidence:.2%}" if confidence > 0 else name
                    cv2.rectangle(
                        frame,
                        (left, bottom - 35),
                        (right, bottom),
                        color,
                        cv2.FILLED
                    )
                    cv2.putText(
                        frame,
                        label,
                        (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX,
                        0.6,
                        (255, 255, 255),
                        1
                    )
                
                cv2.imshow('Emma - Face Recognition', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                if recognized_person:
                    break
        
        except Exception as e:
            print(f"Error during recognition: {str(e)}")
        
        finally:
            cv2.destroyAllWindows()
            video_capture.release()
        
        return recognized_person

    def _load_user_data(self):
        """Load user metadata"""
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_user_data(self, data):
        """Save user metadata"""
        with open(self.user_data_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _update_recognition_time(self, name):
        """Update last recognition time"""
        user_data = self._load_user_data()
        if name in user_data:
            user_data[name]["last_recognized"] = datetime.now().isoformat()
            self._save_user_data(user_data)

    def get_registered_users(self):
        """Get list of registered users"""
        user_data = self._load_user_data()
        return list(user_data.keys())

    def delete_face_data(self, name):
        """Delete face data for a user"""
        if name in self.known_names:
            idx = self.known_names.index(name)
            self.known_names.pop(idx)
            self.known_encodings.pop(idx)
            
            data = {"encodings": self.known_encodings, "names": self.known_names}
            with open(self.encodings_file, 'wb') as f:
                pickle.dump(data, f)
            
            user_data = self._load_user_data()
            if name in user_data:
                del user_data[name]
                self._save_user_data(user_data)
            
            print(f"✅ Face data deleted for {name}")
            return True
        
        return False

    def show_face_stats(self):
        """Show facial recognition statistics"""
        user_data = self._load_user_data()
        
        print("\n" + "=" * 50)
        print("👤 Face Recognition Statistics")
        print("=" * 50)
        print(f"Registered Users: {len(user_data)}\n")
        
        for name, data in user_data.items():
            registered = data.get("registered_at", "Unknown")
            last_recognized = data.get("last_recognized", "Not yet")
            
            print(f"{name}:")
            print(f"  Registered: {registered[:10]}")
            print(f"  Last recognized: {last_recognized[:10] if last_recognized != 'Not yet' else last_recognized}")
        
        print("=" * 50 + "\n")

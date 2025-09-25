# Create a simplified, error-free version of the face tracking system
# Starting with a basic working version that can be easily extended

# First, let's create a simplified requirements file
simple_requirements = '''# Core Computer Vision Dependencies
opencv-python==4.8.1.78
numpy==1.24.3
pillow==10.0.1

# Deep Learning and YOLO
ultralytics==8.0.196
torch==2.0.1
torchvision==0.15.2

# Face Recognition (Optional - fallback to basic detection if not working)
# insightface==0.7.3
# onnxruntime==1.15.1

# Tracking and Utilities  
scipy==1.10.1
tqdm==4.65.0

# Database
# sqlite3 is built-in with Python

# Utilities
python-dateutil==2.8.2
'''

with open('requirements_simple.txt', 'w') as f:
    f.write(simple_requirements)

print("✅ Created simplified requirements file")

# Create a step-by-step minimal working version
minimal_main = '''#!/usr/bin/env python3
"""
Minimal Face Tracking System - Error-Free Version
This version focuses on getting a working system with basic face detection and tracking.
"""

import cv2
import numpy as np
import time
import os
import sys
import argparse
import sqlite3
import json
from datetime import datetime
from collections import OrderedDict
from scipy.spatial import distance as dist

# Check if YOLO is available
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
    print("✅ YOLOv8 available")
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️  YOLOv8 not available, using OpenCV face detection")

class SimpleLogger:
    """Simple logging system"""
    def __init__(self):
        self.log_dir = "logs"
        self.image_dir = os.path.join(self.log_dir, "images")
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.image_dir, exist_ok=True)
        
        # Setup log file
        self.log_file = os.path.join(self.log_dir, "system.log")
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        # Write to file
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry + "\\n")
        except:
            pass  # Ignore file write errors
    
    def save_image(self, image, name):
        """Save image with timestamp"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.jpg"
            path = os.path.join(self.image_dir, filename)
            cv2.imwrite(path, image)
            return path
        except Exception as e:
            self.log(f"Error saving image: {e}")
            return None

class SimpleFaceDetector:
    """Simple face detector with fallback options"""
    def __init__(self):
        self.logger = SimpleLogger()
        
        # Try YOLOv8 first
        if YOLO_AVAILABLE:
            try:
                # Use a lightweight YOLO model
                self.model = YOLO('yolov8n.pt')  # Will auto-download
                self.detector_type = "yolo"
                self.logger.log("Using YOLOv8 for face detection")
            except Exception as e:
                self.logger.log(f"YOLO failed: {e}, falling back to OpenCV")
                self._init_opencv_detector()
        else:
            self._init_opencv_detector()
    
    def _init_opencv_detector(self):
        """Initialize OpenCV face detector as fallback"""
        try:
            # Download OpenCV face cascade if not exists
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            self.detector_type = "opencv"
            self.logger.log("Using OpenCV Haar Cascade for face detection")
        except Exception as e:
            self.logger.log(f"OpenCV detector failed: {e}")
            self.detector_type = "none"
    
    def detect_faces(self, frame):
        """Detect faces in frame, return list of (x, y, w, h, confidence)"""
        try:
            if self.detector_type == "yolo":
                return self._detect_yolo(frame)
            elif self.detector_type == "opencv":
                return self._detect_opencv(frame)
            else:
                return []
        except Exception as e:
            self.logger.log(f"Face detection error: {e}")
            return []
    
    def _detect_yolo(self, frame):
        """YOLO-based detection"""
        try:
            results = self.model(frame, conf=0.5, verbose=False)
            faces = []
            
            if results and len(results) > 0:
                boxes = results[0].boxes
                if boxes is not None:
                    for box in boxes:
                        # Get coordinates and confidence
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf = box.conf[0].cpu().numpy()
                        
                        # Convert to (x, y, w, h) format
                        x, y, w, h = int(x1), int(y1), int(x2-x1), int(y2-y1)
                        faces.append((x, y, w, h, float(conf)))
            
            return faces
        except Exception as e:
            self.logger.log(f"YOLO detection error: {e}")
            return []
    
    def _detect_opencv(self, frame):
        """OpenCV-based detection"""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces_rect = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
            )
            
            faces = []
            for (x, y, w, h) in faces_rect:
                faces.append((x, y, w, h, 0.8))  # Assign default confidence
            
            return faces
        except Exception as e:
            self.logger.log(f"OpenCV detection error: {e}")
            return []

class SimpleTracker:
    """Simple centroid-based tracker"""
    def __init__(self, max_disappeared=30):
        self.next_id = 0
        self.objects = OrderedDict()
        self.disappeared = OrderedDict()
        self.max_disappeared = max_disappeared
        
    def register(self, centroid):
        """Register a new object"""
        self.objects[self.next_id] = centroid
        self.disappeared[self.next_id] = 0
        self.next_id += 1
        return self.next_id - 1
    
    def deregister(self, object_id):
        """Remove object from tracking"""
        del self.objects[object_id]
        del self.disappeared[object_id]
    
    def update(self, detections):
        """Update tracker with new detections"""
        if len(detections) == 0:
            # Mark all existing objects as disappeared
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return {}
        
        # Calculate centroids from detections
        input_centroids = []
        for (x, y, w, h, _) in detections:
            cx = int(x + w / 2.0)
            cy = int(y + h / 2.0)
            input_centroids.append((cx, cy))
        
        # If no existing objects, register all detections
        if len(self.objects) == 0:
            for centroid in input_centroids:
                self.register(centroid)
        else:
            # Match existing objects to new detections
            object_centroids = list(self.objects.values())
            object_ids = list(self.objects.keys())
            
            # Compute distances
            D = dist.cdist(np.array(object_centroids), input_centroids)
            
            # Find minimum distance assignments
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]
            
            used_rows = set()
            used_cols = set()
            
            # Update matched objects
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                
                if D[row, col] > 100:  # Maximum distance threshold
                    continue
                
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                
                used_rows.add(row)
                used_cols.add(col)
            
            # Handle unmatched detections and objects
            unused_rows = set(range(0, D.shape[0])).difference(used_rows)
            unused_cols = set(range(0, D.shape[1])).difference(used_cols)
            
            # Mark unmatched objects as disappeared
            if D.shape[0] >= D.shape[1]:
                for row in unused_rows:
                    object_id = object_ids[row]
                    self.disappeared[object_id] += 1
                    if self.disappeared[object_id] > self.max_disappeared:
                        self.deregister(object_id)
            
            # Register new objects for unmatched detections
            else:
                for col in unused_cols:
                    self.register(input_centroids[col])
        
        # Return mapping of object_id -> detection
        result = {}
        for i, detection in enumerate(detections):
            if i < len(input_centroids):
                centroid = input_centroids[i]
                for obj_id, obj_centroid in self.objects.items():
                    if obj_centroid == centroid:
                        result[obj_id] = detection
                        break
        
        return result

class SimpleDatabase:
    """Simple SQLite database"""
    def __init__(self, db_path="data/tracker.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create events table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    object_id INTEGER,
                    event_type TEXT,
                    timestamp TEXT,
                    image_path TEXT
                )
            """)
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database init error: {e}")
    
    def log_event(self, object_id, event_type, image_path=None):
        """Log an event"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO events (object_id, event_type, timestamp, image_path)
                VALUES (?, ?, ?, ?)
            """, (object_id, event_type, datetime.now().isoformat(), image_path))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Database log error: {e}")
            return False

class VisitorCounter:
    """Simple visitor counter"""
    def __init__(self, frame_height):
        self.detection_line = frame_height // 2  # Middle of frame
        self.track_states = {}  # track_id -> {last_y, crossed}
        self.entry_count = 0
        self.exit_count = 0
        self.unique_visitors = set()
        
    def update(self, tracked_objects):
        """Update counter with tracked objects"""
        events = []
        
        for track_id, (x, y, w, h, conf) in tracked_objects.items():
            center_y = y + h // 2
            
            # Initialize track state
            if track_id not in self.track_states:
                self.track_states[track_id] = {
                    'last_y': center_y,
                    'crossed': False
                }
            
            state = self.track_states[track_id]
            
            # Check for line crossing
            if not state['crossed']:
                # Entry: from top to bottom
                if state['last_y'] < self.detection_line < center_y:
                    self.entry_count += 1
                    self.unique_visitors.add(track_id)
                    state['crossed'] = True
                    events.append({
                        'track_id': track_id,
                        'event_type': 'entry',
                        'bbox': (x, y, w, h)
                    })
                
                # Exit: from bottom to top  
                elif state['last_y'] > self.detection_line > center_y:
                    self.exit_count += 1
                    state['crossed'] = True
                    events.append({
                        'track_id': track_id,
                        'event_type': 'exit',
                        'bbox': (x, y, w, h)
                    })
            
            state['last_y'] = center_y
        
        return events
    
    def get_stats(self):
        """Get current statistics"""
        return {
            'entries': self.entry_count,
            'exits': self.exit_count,
            'unique_visitors': len(self.unique_visitors),
            'current_occupancy': max(0, self.entry_count - self.exit_count)
        }

class FaceTrackingSystem:
    """Main system class"""
    def __init__(self, video_source=0):
        # Initialize components
        self.logger = SimpleLogger()
        self.face_detector = SimpleFaceDetector()
        self.tracker = SimpleTracker()
        self.database = SimpleDatabase()
        
        # Initialize video capture
        self.cap = cv2.VideoCapture(video_source)
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video source: {video_source}")
        
        # Get frame dimensions
        frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        self.visitor_counter = VisitorCounter(frame_height)
        
        # Runtime variables
        self.frame_count = 0
        self.start_time = time.time()
        
        self.logger.log("Face tracking system initialized successfully")
    
    def process_frame(self, frame):
        """Process a single frame"""
        # Face detection
        faces = self.face_detector.detect_faces(frame)
        
        # Object tracking
        tracked_objects = self.tracker.update(faces)
        
        # Visitor counting
        events = self.visitor_counter.update(tracked_objects)
        
        # Handle events
        for event in events:
            track_id = event['track_id']
            event_type = event['event_type']
            bbox = event['bbox']
            
            # Crop face region
            x, y, w, h = bbox
            face_crop = frame[y:y+h, x:x+w]
            
            # Save face image
            image_path = self.logger.save_image(face_crop, f"face_{track_id}_{event_type}")
            
            # Log to database
            self.database.log_event(track_id, event_type, image_path)
            
            self.logger.log(f"{event_type.upper()}: Track {track_id}")
        
        # Annotate frame
        annotated_frame = self.annotate_frame(frame, faces, tracked_objects)
        
        self.frame_count += 1
        return annotated_frame
    
    def annotate_frame(self, frame, faces, tracked_objects):
        """Add annotations to frame"""
        result = frame.copy()
        
        # Draw detection line
        cv2.line(result, (0, self.visitor_counter.detection_line), 
                (frame.shape[1], self.visitor_counter.detection_line), 
                (0, 255, 255), 2)
        
        # Draw face detections with tracking IDs
        for track_id, (x, y, w, h, conf) in tracked_objects.items():
            # Draw bounding box
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Draw labels
            label = f"ID: {track_id} ({conf:.2f})"
            cv2.putText(result, label, (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Draw statistics
        stats = self.visitor_counter.get_stats()
        info_text = [
            f"Entries: {stats['entries']}",
            f"Exits: {stats['exits']}",
            f"Unique: {stats['unique_visitors']}",
            f"Occupancy: {stats['current_occupancy']}",
            f"Frame: {self.frame_count}"
        ]
        
        # Draw info background
        cv2.rectangle(result, (10, 10), (300, 150), (0, 0, 0), -1)
        
        # Draw info text
        for i, text in enumerate(info_text):
            cv2.putText(result, text, (20, 35 + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return result
    
    def run(self):
        """Main processing loop"""
        self.logger.log("Starting face tracking system...")
        
        try:
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    self.logger.log("No more frames or camera disconnected")
                    break
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Display frame
                cv2.imshow('Face Tracking System', processed_frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.logger.log("Quit requested by user")
                    break
                elif key == ord('r'):
                    # Reset counters
                    self.visitor_counter = VisitorCounter(
                        int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    )
                    self.logger.log("Counters reset")
                elif key == ord('s'):
                    # Save screenshot
                    self.logger.save_image(processed_frame, "screenshot")
                    self.logger.log("Screenshot saved")
        
        except KeyboardInterrupt:
            self.logger.log("System interrupted by user")
        except Exception as e:
            self.logger.log(f"System error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.logger.log("Cleaning up...")
        
        # Get final statistics
        stats = self.visitor_counter.get_stats()
        runtime = time.time() - self.start_time
        
        self.logger.log(f"Session completed:")
        self.logger.log(f"  Runtime: {runtime:.1f} seconds")
        self.logger.log(f"  Frames processed: {self.frame_count}")
        self.logger.log(f"  Final stats: {stats}")
        
        # Release resources
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Simple Face Tracking System")
    parser.add_argument("--video", default=0, 
                       help="Video source (0 for webcam, or path to video file)")
    parser.add_argument("--test", action="store_true",
                       help="Run quick test")
    
    args = parser.parse_args()
    
    if args.test:
        print("Running quick test...")
        # Test basic imports
        try:
            import cv2
            print("✅ OpenCV available")
            import numpy as np
            print("✅ NumPy available")
            import scipy
            print("✅ SciPy available")
            if YOLO_AVAILABLE:
                print("✅ YOLO available")
            else:
                print("⚠️  YOLO not available, will use OpenCV")
            print("✅ All basic dependencies working!")
            return
        except Exception as e:
            print(f"❌ Test failed: {e}")
            return
    
    try:
        # Parse video source
        video_source = args.video
        if video_source != "0" and not video_source.startswith("rtsp"):
            # Try to convert to int for camera index, otherwise treat as file path
            try:
                video_source = int(video_source)
            except ValueError:
                pass  # Keep as string (file path)
        elif video_source == "0":
            video_source = 0
        
        # Initialize and run system
        system = FaceTrackingSystem(video_source=video_source)
        system.run()
        
    except Exception as e:
        print(f"Failed to start system: {e}")
        print("\\nTry running with --test to check dependencies")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''

with open('simple_main.py', 'w') as f:
    f.write(minimal_main)

print("✅ Created simplified main.py with error handling and fallback options")
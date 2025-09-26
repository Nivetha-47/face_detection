# Face Tracking System

A **real-time face tracking and visitor counting system** built in Python.  
Detects faces, tracks individuals, counts entries/exits, saves face images, and logs events to a SQLite database.  

---

## 🚀 Features

- Real-time **face detection** (YOLOv8 with OpenCV fallback)  
- **Multi-object tracking** with unique IDs  
- **Entry/Exit detection** with middle line  
- **Visitor counting** and occupancy monitoring  
- **Face image logging** with timestamps  
- **Event logging** in SQLite database  
- Works with **webcam, video files, or IP cameras**  

---

## ⚙️ Setup Instructions

### Automatic Installer (Recommended)

**Windows:**  
1. Download `install.bat` and run it.  
2. Start the system:  
python simple_main.py
# Linux/Mac:
chmod +x install.sh
./install.sh
python simple_main.py
# Manual Setup:
mkdir face_tracking
cd face_tracking
python -m venv env
# Activate: 
# Windows: env\Scripts\activate
# Mac/Linux: source env/bin/activate
pip install opencv-python numpy ultralytics torch scipy pillow
# Save simple_main.py in your project folder and run:
python simple_main.py
# Sample config.json
{
  "video_source": 0,
  "detection_confidence": 0.5,
  "max_disappeared": 30,
  "detection_line_position": "middle",
  "save_images": true,
  "log_to_db": true
}
# Test dependencies
python simple_main.py --test

# Webcam (default)
python simple_main.py

# Video file
python simple_main.py --video path/to/video.mp4

# IP Camera
python simple_main.py --video "rtsp://camera_url"
# 📁 Generated Files
face_tracking/
├── simple_main.py
├── logs/
│   ├── system.log
│   └── images/
│       └── face_1_entry_TIMESTAMP.jpg
└── data/
    └── tracker.db
# Youtube Video Link : 1)Code Walkthrough---> https://youtu.be/bZfqOGYqDwg 2)Output---> https://youtube.com/shorts/HdnTKdXJplc?feature=share

**This project is a part of a hackathon run by https://katomaran.com**

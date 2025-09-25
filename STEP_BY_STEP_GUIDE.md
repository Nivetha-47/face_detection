# 🎯 COMPLETE STEP-BY-STEP GUIDE - Face Tracking System

## 📋 What This System Does

✅ **Detects faces** in real-time from video/camera  
✅ **Tracks people** across frames with unique IDs  
✅ **Counts visitors** when they cross a detection line  
✅ **Saves face images** with timestamps  
✅ **Logs all events** to database and files  
✅ **Works with webcam, video files, or IP cameras**

---

## 🚀 QUICK START (5 Minutes)

### Option A: Automatic Installation (Recommended)

**Windows Users:**
```cmd
# Download install.bat and double-click it, then:
python simple_main.py
```

**Mac/Linux Users:**  
```bash
# Download install.sh and run:
chmod +x install.sh
./install.sh
python simple_main.py
```

### Option B: Manual Installation

**Step 1: Create Project Folder**
```bash
mkdir face_tracking
cd face_tracking
```

**Step 2: Create Virtual Environment**
```bash
# Create environment
python -m venv face_tracking_env

# Activate it
# Windows: face_tracking_env\Scripts\activate
# Mac/Linux: source face_tracking_env/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install opencv-python numpy ultralytics torch scipy pillow
```

**Step 4: Save the Code**
- Save `simple_main.py` in your project folder

**Step 5: Run the System**
```bash
python simple_main.py
```

---

## 🎮 HOW TO USE

### Basic Usage:

```bash
# Test if everything works
python simple_main.py --test

# Use webcam (default)
python simple_main.py

# Use video file
python simple_main.py --video path/to/video.mp4

# Use IP camera
python simple_main.py --video "rtsp://camera_url"
```

### Controls While Running:
- **Press 'q'**: Quit
- **Press 'r'**: Reset counters
- **Press 's'**: Save screenshot

---

## 📊 WHAT YOU'LL SEE

The system displays a window showing:

1. **Live video** with green boxes around detected faces
2. **Yellow line** in the middle (detection line)
3. **Face IDs** and confidence scores
4. **Statistics panel** showing:
   - Entries: People who crossed line going down
   - Exits: People who crossed line going up  
   - Unique visitors: Total different people detected
   - Current occupancy: People currently in the area
   - Frame counter

---

## 📁 GENERATED FILES

The system automatically creates:

```
face_tracking/
├── simple_main.py           # Your main code
├── logs/                    # All log files
│   ├── system.log          # System events log
│   └── images/             # Saved face images
│       ├── face_1_entry_20240924_103045.jpg
│       ├── face_2_exit_20240924_103102.jpg
│       └── ...
└── data/                   # Database
    └── tracker.db          # SQLite database with all events
```

---

## 🔧 TROUBLESHOOTING

### Common Issues & Solutions:

**1. "No module named 'cv2'"**
```bash
pip install opencv-python
```

**2. "Could not open video source"**  
- For webcam: Try `--video 1` or `--video 2` (different camera)
- For file: Check the file path is correct
- Make sure no other app is using the camera

**3. "YOLO model download failed"**
- Check internet connection
- The first run downloads models automatically
- If still fails, the system falls back to OpenCV detection

**4. Low performance/slow FPS**
- Close other applications using the camera
- Try reducing video resolution
- Use a faster computer or GPU

**5. Windows permission errors**
- Run command prompt as Administrator
- Make sure antivirus isn't blocking

---

## 🎯 TESTING THE SYSTEM

### Quick Test Checklist:

1. **Run test mode**: `python simple_main.py --test`
   - Should show ✅ for all dependencies

2. **Start with webcam**: `python simple_main.py`
   - Green boxes should appear around faces
   - Statistics should show in top-left corner

3. **Test face tracking**:
   - Move around - your face should keep the same ID number
   - Multiple people should get different ID numbers

4. **Test visitor counting**:
   - Cross the yellow line from top to bottom = Entry +1
   - Cross the yellow line from bottom to top = Exit +1
   - Unique visitors should count different people

5. **Check file generation**:
   - Look in `logs/images/` folder for saved face photos
   - Check `logs/system.log` for text logs
   - Verify `data/tracker.db` database file exists

---

## 🏆 FOR HACKATHON EVALUATION

This simplified version provides:

✅ **Real-time face detection** (YOLOv8 + OpenCV fallback)  
✅ **Multi-object tracking** with persistent IDs  
✅ **Entry/exit detection** with line crossing  
✅ **Unique visitor counting** without duplicates  
✅ **Automatic image logging** with timestamps  
✅ **Database storage** of all events  
✅ **Error handling** and graceful fallbacks  
✅ **Works with video files AND live cameras**

### Demo Script:

1. **Start system**: `python simple_main.py`
2. **Show face detection**: Walk in front of camera
3. **Demonstrate tracking**: Same person keeps same ID
4. **Show visitor counting**: Cross the yellow line
5. **Prove persistence**: Exit and re-enter - new ID assigned
6. **Display generated data**: Show saved images and logs

---

## 🔍 WHAT'S DIFFERENT FROM COMPLEX VERSION

This simplified version:

✅ **Fewer dependencies** - easier to install  
✅ **Better error handling** - won't crash easily  
✅ **Automatic fallbacks** - uses OpenCV if YOLO fails  
✅ **Single file** - easier to manage  
✅ **Clear documentation** - step-by-step instructions  
✅ **Same core features** - meets all requirements  

The complex version had more advanced features but was harder to set up. This version focuses on **reliability and ease of use** while still satisfying all hackathon requirements.

---

## 🎉 SUCCESS METRICS

You'll know it's working when you see:

1. ✅ **Faces detected** - green boxes around faces
2. ✅ **Tracking works** - same person keeps same ID  
3. ✅ **Counting works** - crossing line increments counters
4. ✅ **Images saved** - photos appear in logs/images/
5. ✅ **No crashes** - system runs smoothly
6. ✅ **Performance** - reasonable FPS (10+ frames/second)

**Ready for hackathon evaluation!** 🚀

#!/bin/bash
# Face Tracking System Installation Script

echo "🚀 Installing Face Tracking System..."

# Step 1: Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv face_tracking_env

# Step 2: Activate virtual environment
echo "⚡ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source face_tracking_env/Scripts/activate
else
    # macOS/Linux
    source face_tracking_env/bin/activate
fi

# Step 3: Upgrade pip
echo "📈 Upgrading pip..."
python -m pip install --upgrade pip

# Step 4: Install dependencies
echo "📚 Installing dependencies..."
pip install opencv-python==4.8.1.78
pip install numpy==1.24.3
pip install pillow==10.0.1
pip install ultralytics==8.0.196
pip install torch==2.0.1
pip install torchvision==0.15.2
pip install scipy==1.10.1
pip install tqdm==4.65.0
pip install python-dateutil==2.8.2

echo "✅ Installation complete!"
echo "🎯 Run the system with: python simple_main.py"

#!/usr/bin/env python3
"""
BedsideBot Quick Start Script
Automatically installs dependencies and runs the application
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_and_install_dependencies():
    """Check and install required packages"""
    required_packages = [
        "Flask==2.3.3",
        "Flask-CORS==4.0.0", 
        "opencv-python==4.8.1.78",
        "mediapipe==0.10.7",
        "SpeechRecognition==3.10.0",
        "pyttsx3==2.90",
        "python-dotenv==1.0.0",
        "numpy==1.24.3",
        "Pillow==10.0.1"
    ]
    
    print("🔧 Installing dependencies...")
    for package in required_packages:
        try:
            install_package(package)
            print(f"✅ {package}")
        except Exception as e:
            print(f"⚠️  {package} - {e}")
    
    # Optional packages (won't stop execution if they fail)
    optional_packages = ["deepface==0.0.79", "tensorflow==2.13.0", "twilio==8.9.1"]
    for package in optional_packages:
        try:
            install_package(package)
            print(f"✅ {package}")
        except Exception as e:
            print(f"⚠️  {package} - Optional package failed: {e}")

def main():
    print("🤖 BedsideBot - Starting System...")
    print("=" * 50)
    
    # Install dependencies
    check_and_install_dependencies()
    
    print("\n🚀 Starting BedsideBot Application...")
    print("📱 Notifications will be sent to:")
    print("   📧 Email: rahulspharande28@gmail.com")
    print("   📱 SMS: +919604226339")
    print("\n🌐 Open your browser to: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the application")
    print("=" * 50)
    
    # Run the Flask application
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError:
        print("❌ Error: app.py not found. Make sure you're in the correct directory.")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()
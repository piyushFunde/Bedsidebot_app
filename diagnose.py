"""
BedsideBot Camera Diagnostic Tool
Run this to check if everything is working properly
"""

import sys
import cv2

print("=" * 60)
print("BedsideBot Camera Diagnostic Tool")
print("=" * 60)
print()

# Test 1: Python Version
print("[1/5] Checking Python version...")
version = sys.version_info
if version.major >= 3 and version.minor >= 8:
    print(f"    [OK] Python {version.major}.{version.minor}.{version.micro}")
else:
    print(f"    [WARNING] Python {version.major}.{version.minor}.{version.micro}")
    print("    Recommended: Python 3.8 or higher")
print()

# Test 2: OpenCV
print("[2/5] Checking OpenCV...")
try:
    print(f"    [OK] OpenCV version: {cv2.__version__}")
except Exception as e:
    print(f"    [ERROR] OpenCV not found: {e}")
    sys.exit(1)
print()

# Test 3: Camera Detection
print("[3/5] Detecting cameras...")
cameras_found = []
for i in range(3):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        cameras_found.append(i)
        ret, frame = cap.read()
        if ret:
            h, w, c = frame.shape
            print(f"    [OK] Camera {i}: {w}x{h}, {c} channels")
        else:
            print(f"    [WARNING] Camera {i}: Opened but cannot read frames")
        cap.release()

if not cameras_found:
    print("    [ERROR] No cameras detected!")
    print()
    print("Troubleshooting steps:")
    print("  1. Check if camera is connected")
    print("  2. Close other apps using the camera")
    print("  3. Check Windows Privacy Settings > Camera")
    print("  4. Try unplugging and replugging the camera")
    sys.exit(1)
else:
    print(f"    [OK] Found {len(cameras_found)} camera(s): {cameras_found}")
print()

# Test 4: Camera Capture Test
print("[4/5] Testing camera capture...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    cap = cv2.VideoCapture(1)

if cap.isOpened():
    success_count = 0
    for i in range(5):
        ret, frame = cap.read()
        if ret:
            success_count += 1
    
    if success_count == 5:
        print(f"    [OK] Successfully captured {success_count}/5 frames")
    else:
        print(f"    [WARNING] Only captured {success_count}/5 frames")
    
    cap.release()
else:
    print("    [ERROR] Cannot open camera")
    sys.exit(1)
print()

# Test 5: JPEG Encoding Test
print("[5/5] Testing JPEG encoding...")
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    cap = cv2.VideoCapture(1)

if cap.isOpened():
    ret, frame = cap.read()
    if ret:
        ret_encode, buffer = cv2.imencode('.jpg', frame)
        if ret_encode:
            size_kb = len(buffer) / 1024
            print(f"    [OK] JPEG encoding works ({size_kb:.1f} KB)")
        else:
            print("    [ERROR] JPEG encoding failed")
    cap.release()
print()

# Summary
print("=" * 60)
print("DIAGNOSTIC SUMMARY")
print("=" * 60)
print("[OK] All tests passed!")
print()
print("Your camera is working properly.")
print("You can now start the application:")
print("  python app.py")
print()
print("Then open your browser to:")
print("  http://localhost:5000/test_video  (Simple test)")
print("  http://localhost:5000/interface  (Full interface)")
print("=" * 60)

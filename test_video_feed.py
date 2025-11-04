import cv2
import time
import sys

print("Testing video feed generation...")

# Initialize camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Trying camera 1...")
    cap = cv2.VideoCapture(1)

if cap.isOpened():
    print("[OK] Camera opened successfully!")
    
    # Set properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("Testing frame capture and encoding...")
    
    for i in range(10):
        ret, frame = cap.read()
        if ret:
            # Flip frame like in the app
            frame = cv2.flip(frame, 1)
            
            # Try encoding to JPEG
            ret_encode, buffer = cv2.imencode('.jpg', frame)
            if ret_encode:
                print(f"[OK] Frame {i+1}: Captured and encoded ({len(buffer)} bytes)")
            else:
                print(f"[ERROR] Frame {i+1}: Encoding failed")
        else:
            print(f"[ERROR] Frame {i+1}: Capture failed")
        
        time.sleep(0.1)
    
    cap.release()
    print("\n[OK] Video feed test completed successfully!")
else:
    print("[ERROR] No camera found!")

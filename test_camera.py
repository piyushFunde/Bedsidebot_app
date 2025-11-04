import cv2
import time

print("Testing camera...")

# Try to open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera 0 failed, trying camera 1...")
    cap = cv2.VideoCapture(1)

if cap.isOpened():
    print("Camera opened successfully!")
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Test reading frames
    for i in range(5):
        ret, frame = cap.read()
        if ret:
            print(f"Frame {i+1}: {frame.shape}")
        else:
            print(f"Frame {i+1}: Failed to read")
        time.sleep(0.5)
    
    cap.release()
    print("Camera test completed!")
else:
    print("No camera found!")
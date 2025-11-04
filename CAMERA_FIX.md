# Camera Video Feed Fix Guide

## Problem
The camera video feed was not displaying on the interface page when starting the monitoring system.

## What Was Fixed

### 1. Camera Initialization Issues
- **Problem**: Camera was not being initialized when the video feed endpoint was accessed
- **Fix**: Added automatic camera initialization in both `generate_frames()` and `process_frame()` functions
- **Code Changes**: 
  - Camera now initializes automatically when `/video_feed` is accessed
  - Falls back to camera index 1 if camera 0 fails
  - Sets optimal camera properties (640x480, 30 FPS)

### 2. Missing API Endpoint
- **Problem**: Interface was calling `/api/get_patients` which didn't exist
- **Fix**: Added the missing endpoint to return registered patients

### 3. Better Error Handling
- **Problem**: No error messages when camera failed
- **Fix**: Added logging and error handling throughout the video pipeline

## How to Test

### Step 1: Test Camera Hardware
```bash
python test_camera.py
```
Expected output: "Camera opened successfully!" with 5 frames captured

### Step 2: Test Video Feed Encoding
```bash
python test_video_feed.py
```
Expected output: 10 frames captured and encoded successfully

### Step 3: Start the Application
```bash
python app.py
```
Or use the batch file:
```bash
start_app.bat
```

### Step 4: Test Video Feed in Browser

#### Option A: Simple Camera Test Page
1. Open browser: http://localhost:5000/test_video
2. Click "Start Camera" button
3. You should see the live video feed

#### Option B: Full Interface
1. Open browser: http://localhost:5000/interface
2. The video feed should start automatically
3. Look for the live camera feed on the left side

## Troubleshooting

### Issue: "Camera not available" error
**Solutions:**
1. Close any other applications using the camera (Zoom, Teams, Skype, etc.)
2. Check Windows Camera Privacy Settings:
   - Go to Settings > Privacy > Camera
   - Enable "Allow apps to access your camera"
   - Enable "Allow desktop apps to access your camera"
3. Try unplugging and replugging your webcam
4. Restart your computer

### Issue: Video feed shows black screen
**Solutions:**
1. Check if camera LED is on (indicates camera is active)
2. Try covering/uncovering the camera lens
3. Check browser console for errors (F12 > Console tab)
4. Verify the Flask app is running without errors

### Issue: Video feed is very slow
**Solutions:**
1. Close other resource-intensive applications
2. Reduce video quality in app.py:
   ```python
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
   ```
3. Increase sleep time in generate_frames():
   ```python
   time.sleep(0.1)  # Increase from 0.03
   ```

### Issue: Browser shows "Image cannot be displayed"
**Solutions:**
1. Check Flask console for error messages
2. Verify the URL is correct: http://localhost:5000/video_feed
3. Try a different browser (Chrome, Firefox, Edge)
4. Clear browser cache and reload

## Windows Camera Permissions

### Enable Camera Access:
1. Press Windows + I to open Settings
2. Go to Privacy & Security > Camera
3. Turn ON "Camera access"
4. Turn ON "Let apps access your camera"
5. Turn ON "Let desktop apps access your camera"

### Check Camera in Device Manager:
1. Press Windows + X
2. Select Device Manager
3. Expand "Cameras" or "Imaging devices"
4. Right-click your camera > Enable (if disabled)
5. Right-click > Update driver (if needed)

## Code Changes Summary

### app.py Changes:

1. **process_frame()** - Auto-initialize camera if not available
2. **generate_frames()** - Initialize camera at start, better error handling
3. **start_monitoring()** - Set camera properties, return camera status
4. **video_feed()** - Added error logging and exception handling
5. **get_patients()** - New endpoint for patient data

## Testing Checklist

- [ ] Camera test passes (test_camera.py)
- [ ] Video encoding test passes (test_video_feed.py)
- [ ] Flask app starts without errors
- [ ] Test page shows video feed (http://localhost:5000/test_video)
- [ ] Main interface shows video feed (http://localhost:5000/interface)
- [ ] Hand gestures are detected
- [ ] No errors in Flask console
- [ ] No errors in browser console

## Additional Notes

- The camera now initializes automatically when needed
- Frame rate optimized to ~30 FPS for better performance
- Video feed uses MJPEG streaming for real-time display
- Camera is properly released when monitoring stops

## Support

If you still have issues after following this guide:
1. Check the Flask console output for error messages
2. Check browser console (F12) for JavaScript errors
3. Verify all dependencies are installed: `pip install -r requirements.txt`
4. Make sure you're using Python 3.8 or higher
5. Try running as administrator if permission issues persist

# BedsideBot - Quick Start Guide

## Camera Video Feed Fixed! ✓

The camera initialization issue has been resolved. Follow these steps to start using BedsideBot.

## Quick Start (3 Steps)

### Step 1: Run Diagnostics
```bash
python diagnose.py
```
This checks if your camera is working properly.

### Step 2: Start the Application
```bash
python app.py
```
Or double-click: `start_app.bat`

### Step 3: Open in Browser
Choose one of these options:

**Option A - Simple Camera Test:**
```
http://localhost:5000/test_video
```
Use this to verify the camera feed works.

**Option B - Full Patient Interface:**
```
http://localhost:5000/interface
```
Use this for the complete monitoring system.

## What Was Fixed

1. **Automatic Camera Initialization**: Camera now starts automatically when you access the video feed
2. **Better Error Handling**: Clear error messages if camera fails
3. **Fallback Support**: Tries camera 0, then camera 1 if needed
4. **Optimized Settings**: Camera configured for best performance (640x480, 30 FPS)

## If Video Still Doesn't Show

### Quick Fixes:
1. **Close other camera apps** (Zoom, Teams, Skype)
2. **Check Windows Camera Settings**:
   - Settings > Privacy > Camera
   - Enable "Allow apps to access your camera"
   - Enable "Allow desktop apps to access your camera"
3. **Refresh the browser page** (Ctrl + F5)
4. **Try a different browser** (Chrome, Firefox, Edge)

### Check Permissions:
```
Windows Settings > Privacy & Security > Camera
- Turn ON "Camera access"
- Turn ON "Let apps access your camera"  
- Turn ON "Let desktop apps access your camera"
```

## Testing Tools

We've created several tools to help you:

| Tool | Purpose | Command |
|------|---------|---------|
| diagnose.py | Full system check | `python diagnose.py` |
| test_camera.py | Basic camera test | `python test_camera.py` |
| test_video_feed.py | Video encoding test | `python test_video_feed.py` |
| test_video page | Browser camera test | http://localhost:5000/test_video |

## Application Flow

1. **Start App** → `python app.py`
2. **Landing Page** → http://localhost:5000/
3. **Register Hospital** → Fill in hospital details
4. **Register Staff** → Add medical staff
5. **Register Patient** → Add patient information
6. **Register Caregiver** → Add caregiver contacts
7. **Select Modules** → Choose recognition features
8. **Patient Interface** → Start monitoring with live video

## Features Available

- ✓ **Hand Sign Detection** - Use 1-5 fingers to select actions
- ✓ **Voice Recognition** - Say commands like "water", "food", "help"
- ✓ **Emotion Detection** - Automatic facial emotion analysis
- ✓ **Eye Gaze Tracking** - Look left/right/center to select

## Troubleshooting

### Camera LED is ON but no video
- Refresh browser (Ctrl + F5)
- Check browser console for errors (F12)
- Restart the Flask app

### "Camera not available" error
- Run `python diagnose.py` to check camera status
- Close other apps using the camera
- Unplug and replug the webcam

### Video is very slow/laggy
- Close other resource-intensive apps
- Lower video quality in app.py (see CAMERA_FIX.md)
- Check your CPU usage

## Support Files

- `CAMERA_FIX.md` - Detailed fix documentation
- `README.md` - Full project documentation
- `requirements.txt` - Python dependencies

## Need Help?

1. Run diagnostics: `python diagnose.py`
2. Check Flask console for errors
3. Check browser console (F12) for errors
4. Review CAMERA_FIX.md for detailed troubleshooting

## Success Indicators

You'll know everything is working when:
- ✓ Diagnostic tool shows all tests passed
- ✓ Flask app starts without errors
- ✓ Browser shows live video feed
- ✓ Hand gestures are detected and highlighted
- ✓ Action buttons light up when gestures are detected

---

**Ready to start?** Run: `python diagnose.py` then `python app.py`

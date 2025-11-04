@echo off
echo Starting BedsideBot Application...
echo.
echo Testing camera first...
python test_camera.py
echo.
echo.
echo If camera test passed, starting Flask app...
echo.
echo Open your browser and go to:
echo   - Main Interface: http://localhost:5000/interface
echo   - Camera Test: http://localhost:5000/test_video
echo.
python app.py

@echo off
cls
echo ============================================================
echo BedsideBot - Patient Monitoring System
echo ============================================================
echo.
echo [1/2] Running camera diagnostic...
python diagnose.py
echo.
echo ============================================================
echo [2/2] Starting Flask Application...
echo ============================================================
echo.
echo The application will start in a few seconds...
echo.
echo Once started, open your browser and go to:
echo   http://localhost:5000/
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.
python app.py
pause

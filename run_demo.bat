@echo off
echo Starting BedsideBot Demo Setup...
echo.

echo Step 1: Starting the server...
start "BedsideBot Server" cmd /k "python app.py"

echo Waiting for server to start...
timeout /t 5 /nobreak > nul

echo Step 2: Setting up demo data...
python auto_setup.py

echo.
echo ✅ Demo setup complete!
echo 🌐 Open your browser and go to: http://localhost:5000/test_notifications
echo.
pause
@echo off
echo ========================================
echo BedsideBot Installation and Setup
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    echo Please ensure Python is installed and added to PATH
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.

echo Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from template
    echo Please edit .env file with your email and SMS credentials
    echo.
)

echo Starting BedsideBot application...
echo.
echo The application will start on http://localhost:5000
echo Press Ctrl+C to stop the application
echo.

python app.py

pause
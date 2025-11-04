@echo off
title BedsideBot - Multi-Assistant Healthcare System
color 0A

echo.
echo ========================================
echo    BedsideBot Healthcare System
echo ========================================
echo.
echo Starting system...
echo.

cd /d "%~dp0"

echo Installing dependencies and starting application...
python run_bedsidebot.py

echo.
echo System stopped. Press any key to exit...
pause >nul
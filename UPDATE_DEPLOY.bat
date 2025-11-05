@echo off
color 0A
echo.
echo  🔄 UPDATING BEDSIDEBOT DEPLOYMENT 🔄
echo.
echo ================================================================================
echo                        PUSHING LATEST CHANGES TO GITHUB
echo ================================================================================
echo.

echo 📝 Adding all changes...
git add .

echo 💾 Committing changes...
git commit -m "Fix form validation and add patient details/print report features"

echo 📤 Pushing to GitHub...
git push origin main

if %errorlevel% equ 0 (
    echo.
    echo ✅ SUCCESS! Changes pushed to GitHub!
    echo.
    echo 🚀 Your deployed app will update automatically in 1-2 minutes
    echo 🌐 Check your Railway dashboard for deployment status
    echo.
    echo Updated features:
    echo   ✅ Fixed form validation - cannot skip registration steps
    echo   ✅ Patient details modal with comprehensive information
    echo   ✅ Professional print reports in Times New Roman
    echo   ✅ Multi-device patient monitoring
    echo   ✅ Real-time notifications across devices
    echo.
) else (
    echo ❌ Error pushing to GitHub. Please check your connection.
    pause
)

echo.
echo Press any key to close...
pause >nul
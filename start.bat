@echo off
echo ==================================================
echo 🚀 Master Translator Web - Quick Start
echo ==================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)
echo ✅ Python installed

:: Check dependencies
echo.
echo 📦 Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Dependencies not installed, installing...
    pip install -r requirements.txt
) else (
    echo ✅ Dependencies installed
)

:: Create directories
if not exist uploads mkdir uploads
if not exist outputs mkdir outputs
echo ✅ Directories ready

:: Start server
echo.
echo 🌐 Starting server at http://localhost:5001
echo    Press Ctrl+C to stop
echo ==================================================
python app.py
pause

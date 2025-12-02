@echo off
echo ========================================
echo Volatility Insights Pro - Setup for Sharing
echo ========================================
echo.

echo Step 1: Checking if git is installed...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo [OK] Git is installed
echo.

echo Step 2: Initializing git repository...
if exist .git (
    echo [OK] Git repository already initialized
) else (
    git init
    echo [OK] Git repository initialized
)
echo.

echo Step 3: Adding files...
git add .
echo [OK] Files added
echo.

echo Step 4: Creating initial commit...
git commit -m "Volatility Insights Pro - Initial commit" 2>nul
if errorlevel 1 (
    echo [INFO] No changes to commit (or commit already exists)
) else (
    echo [OK] Initial commit created
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Create a repository on GitHub.com
echo 2. Run these commands:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Then deploy to Streamlit Cloud:
echo    - Go to https://share.streamlit.io
echo    - Sign in with GitHub
echo    - Click "New app"
echo    - Select your repository
echo    - Main file: app.py
echo    - Click "Deploy"
echo.
echo For detailed instructions, see: SHARE_VIA_EMAIL.md
echo.
pause


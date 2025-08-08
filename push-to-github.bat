@echo off
echo ========================================
echo Push to GitHub - Enterprise AppData Cleaner
echo ========================================
echo.

echo Your project is ready to be pushed to GitHub!
echo.

echo Step 1: Install Git (if not already installed)
echo Download from: https://git-scm.com/download/win
echo.

echo Step 2: Configure Git (run these commands):
echo   git config --global user.name "Tony Condone"
echo   git config --global user.email "touyboateng339@gmail.com"
echo.

echo Step 3: Initialize Git Repository (run these commands):
echo   git init
echo   git add .
echo   git commit -m "Initial commit: Enterprise AppData Deep Clean Suite v1.2.0"
echo.

echo Step 4: Create GitHub Repository
echo 1. Go to https://github.com/tonycondone
echo 2. Click "New repository"
echo 3. Repository name: enterprise-appdata-cleaner
echo 4. Description: Enterprise-grade AppData cleanup tool with security and compliance features
echo 5. Make it Public or Private
echo 6. DO NOT initialize with README (we already have one)
echo 7. Click "Create repository"
echo.

echo Step 5: Push to GitHub (run these commands):
echo   git remote add origin https://github.com/tonycondone/enterprise-appdata-cleaner.git
echo   git branch -M main
echo   git push -u origin main
echo.

echo ========================================
echo Project Files Ready:
echo ========================================
dir /b
echo.

echo ========================================
echo Features Included:
echo ========================================
echo ✓ Enterprise AppData cleaning (1,480 lines)
echo ✓ Security & compliance frameworks
echo ✓ Batch deployment capabilities
echo ✓ SIEM integration
echo ✓ Performance monitoring
echo ✓ Backup & restore functionality
echo ✓ Configuration management integration
echo ✓ Comprehensive documentation
echo ✓ MIT License
echo.

echo ========================================
echo Next Steps:
echo ========================================
echo 1. Install Git
echo 2. Configure Git with your details
echo 3. Create GitHub repository
echo 4. Run the git commands above
echo 5. Your project will be live on GitHub!
echo.

pause 
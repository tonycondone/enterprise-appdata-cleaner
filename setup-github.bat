@echo off
echo ========================================
echo Enterprise AppData Cleaner - GitHub Setup
echo ========================================
echo.

echo This script will help you set up your GitHub repository.
echo.

echo Step 1: Install Git (if not already installed)
echo Download Git from: https://git-scm.com/download/win
echo After installation, restart this script.
echo.

echo Step 2: Configure Git (if needed)
echo Run these commands after installing Git:
echo   git config --global user.name "Your Name"
echo   git config --global user.email "your.email@example.com"
echo.

echo Step 3: Initialize Git Repository
echo Run these commands in this directory:
echo   git init
echo   git add .
echo   git commit -m "Initial commit: Enterprise AppData Deep Clean Suite v1.2.0"
echo.

echo Step 4: Create GitHub Repository
echo 1. Go to https://github.com
echo 2. Click "New repository"
echo 3. Name it: enterprise-appdata-cleaner
echo 4. Make it public or private as desired
echo 5. DO NOT initialize with README (we already have one)
echo 6. Click "Create repository"
echo.

echo Step 5: Push to GitHub
echo After creating the repository, run:
echo   git remote add origin https://github.com/YOUR_USERNAME/enterprise-appdata-cleaner.git
echo   git branch -M main
echo   git push -u origin main
echo.

echo ========================================
echo Files in this directory:
echo ========================================
dir /b
echo.

echo ========================================
echo Project Structure:
echo ========================================
echo.
echo enterprise-appdata-cleaner/
echo ├── cleaner.py                    (Main script - 1,480 lines)
echo ├── cleaner_config_example.yaml   (Configuration example)
echo ├── requirements.txt              (Python dependencies)
echo ├── README.md                     (Complete documentation)
echo ├── LICENSE                       (MIT License)
echo ├── setup.py                      (Package setup)
echo ├── .gitignore                    (Git ignore rules)
echo ├── CONTRIBUTING.md               (Contribution guidelines)
echo ├── CHANGELOG.md                  (Version history)
echo └── setup-github.bat             (This file)
echo.

echo ========================================
echo Next Steps:
echo ========================================
echo 1. Install Git from https://git-scm.com/download/win
echo 2. Configure Git with your name and email
echo 3. Run the git commands shown above
echo 4. Create a GitHub repository
echo 5. Push your code to GitHub
echo.

echo ========================================
echo Features Included:
echo ========================================
echo ✓ Enterprise-grade AppData cleaning
echo ✓ Security and compliance frameworks
echo ✓ Batch deployment capabilities
echo ✓ Comprehensive reporting
echo ✓ SIEM integration
echo ✓ Performance monitoring
echo ✓ Backup and restore functionality
echo ✓ Configuration management integration
echo ✓ Complete documentation
echo ✓ MIT License
echo.

pause 
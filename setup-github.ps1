# Enterprise AppData Cleaner - GitHub Setup Script
# PowerShell version

Write-Host "========================================" -ForegroundColor Green
Write-Host "Enterprise AppData Cleaner - GitHub Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "This script will help you set up your GitHub repository." -ForegroundColor Yellow
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Host "✓ Git is installed: $gitVersion" -ForegroundColor Green
    } else {
        Write-Host "✗ Git is not installed" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ Git is not installed" -ForegroundColor Red
}

Write-Host ""
Write-Host "Step 1: Install Git (if not already installed)" -ForegroundColor Cyan
Write-Host "Download Git from: https://git-scm.com/download/win" -ForegroundColor White
Write-Host "After installation, restart this script." -ForegroundColor White
Write-Host ""

Write-Host "Step 2: Configure Git (if needed)" -ForegroundColor Cyan
Write-Host "Run these commands after installing Git:" -ForegroundColor White
Write-Host "  git config --global user.name `"Your Name`"" -ForegroundColor Gray
Write-Host "  git config --global user.email `"your.email@example.com`"" -ForegroundColor Gray
Write-Host ""

Write-Host "Step 3: Initialize Git Repository" -ForegroundColor Cyan
Write-Host "Run these commands in this directory:" -ForegroundColor White
Write-Host "  git init" -ForegroundColor Gray
Write-Host "  git add ." -ForegroundColor Gray
Write-Host "  git commit -m `"Initial commit: Enterprise AppData Deep Clean Suite v1.2.0`"" -ForegroundColor Gray
Write-Host ""

Write-Host "Step 4: Create GitHub Repository" -ForegroundColor Cyan
Write-Host "1. Go to https://github.com" -ForegroundColor White
Write-Host "2. Click `"New repository`"" -ForegroundColor White
Write-Host "3. Name it: enterprise-appdata-cleaner" -ForegroundColor White
Write-Host "4. Make it public or private as desired" -ForegroundColor White
Write-Host "5. DO NOT initialize with README (we already have one)" -ForegroundColor White
Write-Host "6. Click `"Create repository`"" -ForegroundColor White
Write-Host ""

Write-Host "Step 5: Push to GitHub" -ForegroundColor Cyan
Write-Host "After creating the repository, run:" -ForegroundColor White
Write-Host "  git remote add origin https://github.com/YOUR_USERNAME/enterprise-appdata-cleaner.git" -ForegroundColor Gray
Write-Host "  git branch -M main" -ForegroundColor Gray
Write-Host "  git push -u origin main" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "Files in this directory:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Get-ChildItem | ForEach-Object {
    $size = if ($_.Length -gt 1MB) { "{0:N1} MB" -f ($_.Length / 1MB) }
           elseif ($_.Length -gt 1KB) { "{0:N1} KB" -f ($_.Length / 1KB) }
           else { "$($_.Length) B" }
    Write-Host "  $($_.Name) ($size)" -ForegroundColor White
}
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "Project Structure:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "enterprise-appdata-cleaner/" -ForegroundColor Yellow
Write-Host "├── cleaner.py                    (Main script - 1,480 lines)" -ForegroundColor Gray
Write-Host "├── cleaner_config_example.yaml   (Configuration example)" -ForegroundColor Gray
Write-Host "├── requirements.txt              (Python dependencies)" -ForegroundColor Gray
Write-Host "├── README.md                     (Complete documentation)" -ForegroundColor Gray
Write-Host "├── LICENSE                       (MIT License)" -ForegroundColor Gray
Write-Host "├── setup.py                      (Package setup)" -ForegroundColor Gray
Write-Host "├── .gitignore                    (Git ignore rules)" -ForegroundColor Gray
Write-Host "├── CONTRIBUTING.md               (Contribution guidelines)" -ForegroundColor Gray
Write-Host "├── CHANGELOG.md                  (Version history)" -ForegroundColor Gray
Write-Host "├── setup-github.bat              (Batch setup script)" -ForegroundColor Gray
Write-Host "└── setup-github.ps1              (PowerShell setup script)" -ForegroundColor Gray
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "Next Steps:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "1. Install Git from https://git-scm.com/download/win" -ForegroundColor White
Write-Host "2. Configure Git with your name and email" -ForegroundColor White
Write-Host "3. Run the git commands shown above" -ForegroundColor White
Write-Host "4. Create a GitHub repository" -ForegroundColor White
Write-Host "5. Push your code to GitHub" -ForegroundColor White
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "Features Included:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Enterprise-grade AppData cleaning" -ForegroundColor Green
Write-Host "✓ Security and compliance frameworks" -ForegroundColor Green
Write-Host "✓ Batch deployment capabilities" -ForegroundColor Green
Write-Host "✓ Comprehensive reporting" -ForegroundColor Green
Write-Host "✓ SIEM integration" -ForegroundColor Green
Write-Host "✓ Performance monitoring" -ForegroundColor Green
Write-Host "✓ Backup and restore functionality" -ForegroundColor Green
Write-Host "✓ Configuration management integration" -ForegroundColor Green
Write-Host "✓ Complete documentation" -ForegroundColor Green
Write-Host "✓ MIT License" -ForegroundColor Green
Write-Host ""

Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 
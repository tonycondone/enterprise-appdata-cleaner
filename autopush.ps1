# === Auto Git Push Script (PowerShell) ===
# Uses folder name as repo name

# Get current folder name as repo name
$REPO_NAME = Split-Path -Leaf (Get-Location)
$BRANCH_NAME = "main"
$GITHUB_USERNAME = "tonycondone"  # << CHANGE THIS

Write-Host "=== Auto Git Push Script ===" -ForegroundColor Green
Write-Host "Repository: $REPO_NAME" -ForegroundColor Yellow
Write-Host "Branch: $BRANCH_NAME" -ForegroundColor Yellow
Write-Host "GitHub User: $GITHUB_USERNAME" -ForegroundColor Yellow
Write-Host ""

# Check if a Git repo exists
if (Test-Path ".git") {
    Write-Host "➤ This is a Git repo, checking status..." -ForegroundColor Green
    
    # Check if remote origin exists
    $remote = & "C:\Program Files\Git\bin\git.exe" remote get-url origin 2>$null
    if ($remote) {
        Write-Host "➤ Remote origin found: $remote" -ForegroundColor Green
        Write-Host "➤ Starting auto-push loop..." -ForegroundColor Green
        Write-Host "➤ Press Ctrl+C to stop" -ForegroundColor Yellow
        Write-Host ""
        
        # === Auto-push loop ===
        while ($true) {
            try {
                & "C:\Program Files\Git\bin\git.exe" add .
                $hasChanges = & "C:\Program Files\Git\bin\git.exe" diff --cached --quiet 2>$null
                if ($LASTEXITCODE -ne 0) {
                    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
                    $commitMessage = "auto: $timestamp"
                    Write-Host "➤ Committing changes: $commitMessage" -ForegroundColor Cyan
                    & "C:\Program Files\Git\bin\git.exe" commit -m $commitMessage
                    Write-Host "➤ Pushing to origin/$BRANCH_NAME" -ForegroundColor Green
                    & "C:\Program Files\Git\bin\git.exe" push origin $BRANCH_NAME
                    Write-Host "➤ Push completed successfully" -ForegroundColor Green
                } else {
                    Write-Host "➤ No changes to commit" -ForegroundColor Gray
                }
                Start-Sleep -Seconds 2
            }
            catch {
                Write-Host "➤ Error in auto-push loop: $_" -ForegroundColor Red
                Start-Sleep -Seconds 5
            }
        }
    } else {
        Write-Host "➤ No remote origin found. Please set up remote first:" -ForegroundColor Yellow
        Write-Host "   git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git" -ForegroundColor White
        Write-Host "   git push -u origin $BRANCH_NAME" -ForegroundColor White
    }
} else {
    Write-Host "➤ Initializing Git for repo: $REPO_NAME" -ForegroundColor Green
    
    # Initial Git setup
    & "C:\Program Files\Git\bin\git.exe" init
    & "C:\Program Files\Git\bin\git.exe" config user.name "tonycondone"
    & "C:\Program Files\Git\bin\git.exe" config user.email "touyboateng339@gmail.com"
    & "C:\Program Files\Git\bin\git.exe" add .
    & "C:\Program Files\Git\bin\git.exe" commit -m "Initial commit"
    & "C:\Program Files\Git\bin\git.exe" branch -M $BRANCH_NAME

    Write-Host "➤ Git initialized successfully!" -ForegroundColor Green
    Write-Host "➤ Now manually connect your GitHub repo:" -ForegroundColor Yellow
    Write-Host "    1. Create a repo on GitHub named: $REPO_NAME" -ForegroundColor White
    Write-Host "    2. Run these commands:" -ForegroundColor White
    Write-Host "       & `"C:\Program Files\Git\bin\git.exe`" remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git" -ForegroundColor Gray
    Write-Host "       & `"C:\Program Files\Git\bin\git.exe`" push -u origin $BRANCH_NAME" -ForegroundColor Gray
    Write-Host "➤ Then run this script again for auto-push functionality" -ForegroundColor Yellow
} 
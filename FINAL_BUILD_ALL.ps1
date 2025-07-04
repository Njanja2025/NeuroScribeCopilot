# NeuroScribe PDF Copilot - Final Build All Packages
# PowerShell Script for Complete Build and Deployment

Write-Host "🧠 NeuroScribe PDF Copilot - Final Build All Packages" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Git installation
Write-Host "Step 1: Checking Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Red
    Write-Host "Make sure to select 'Add Git to PATH' during installation" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Step 2: Create Portable ZIP Package
Write-Host "Step 2: Creating Portable ZIP Package..." -ForegroundColor Yellow
try {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $zipName = "NeuroScribe-Portable-v1.0-FINAL-$timestamp.zip"
    
    $filesToZip = @(
        "app.py",
        "requirements.txt", 
        "README.md",
        "RELEASE_NOTES.md",
        "LAUNCH_ALL_VERSIONS.bat",
        "QUICK_PACKAGE.bat",
        "src"
    )
    
    Compress-Archive -Path $filesToZip -DestinationPath $zipName -Force
    Write-Host "✅ Created: $zipName" -ForegroundColor Green
} catch {
    Write-Host "⚠️  ZIP creation failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""

# Step 3: Create Windows EXE Installer
Write-Host "Step 3: Creating Windows EXE Installer..." -ForegroundColor Yellow
try {
    python create_installer_package.py
    Write-Host "✅ EXE installer created" -ForegroundColor Green
} catch {
    Write-Host "⚠️  EXE creation failed, trying alternative..." -ForegroundColor Yellow
    try {
        python build_exe.py
        Write-Host "✅ Alternative EXE build completed" -ForegroundColor Green
    } catch {
        Write-Host "❌ EXE creation failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# Step 4: Create Professional Package
Write-Host "Step 4: Creating Professional Package..." -ForegroundColor Yellow
try {
    $proZipName = "NeuroScribe-Professional-v1.0-$timestamp.zip"
    $proFiles = @(
        "app.py",
        "requirements.txt",
        "README.md", 
        "RELEASE_NOTES.md",
        "src",
        "LAUNCH_ALL_VERSIONS.bat",
        "QUICK_PACKAGE.bat",
        "FINAL_BUILD_ALL.ps1"
    )
    
    Compress-Archive -Path $proFiles -DestinationPath $proZipName -Force
    Write-Host "✅ Created: $proZipName" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Professional package creation failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""

# Step 5: Create Source Code Archive
Write-Host "Step 5: Creating Source Code Archive..." -ForegroundColor Yellow
try {
    $sourceZipName = "NeuroScribe-Source-v1.0-$timestamp.zip"
    Compress-Archive -Path "." -DestinationPath $sourceZipName -Force
    Write-Host "✅ Created: $sourceZipName" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Source archive creation failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""

# Step 6: Create Release Package Folder
Write-Host "Step 6: Creating Release Package Folder..." -ForegroundColor Yellow
try {
    if (!(Test-Path "release-package")) {
        New-Item -ItemType Directory -Name "release-package"
    }
    
    # Copy all created packages to release folder
    $packages = @(
        "NeuroScribe-Portable-v1.0-FINAL-$timestamp.zip",
        "NeuroScribe-Professional-v1.0-$timestamp.zip", 
        "NeuroScribe-Source-v1.0-$timestamp.zip"
    )
    
    foreach ($package in $packages) {
        if (Test-Path $package) {
            Copy-Item $package "release-package\"
            Write-Host "✅ Copied $package to release-package/" -ForegroundColor Green
        }
    }
    
    # Copy existing installer packages
    $installerPattern = "NeuroScribeCopilot-Quantum-Installer-*.zip"
    Get-ChildItem -Path $installerPattern | ForEach-Object {
        Copy-Item $_.FullName "release-package\"
        Write-Host "✅ Copied $($_.Name) to release-package/" -ForegroundColor Green
    }
    
    # Copy documentation
    Copy-Item "README.md" "release-package\"
    Copy-Item "RELEASE_NOTES.md" "release-package\"
    Write-Host "✅ Copied documentation to release-package/" -ForegroundColor Green
    
} catch {
    Write-Host "⚠️  Release package creation failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""

# Step 7: Setup Git Repository
Write-Host "Step 7: Setting up Git Repository..." -ForegroundColor Yellow
try {
    if (!(Test-Path ".git")) {
        git init
        Write-Host "✅ Git repository initialized" -ForegroundColor Green
    } else {
        Write-Host "✅ Git repository already exists" -ForegroundColor Green
    }
    
    git add .
    git commit -m "Final release v1.0 - NeuroScribe PDF Copilot"
    Write-Host "✅ Files committed to Git" -ForegroundColor Green
    
} catch {
    Write-Host "⚠️  Git setup failed: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""

# Step 8: Connect to GitHub
Write-Host "Step 8: Connecting to GitHub..." -ForegroundColor Yellow
try {
    git remote add origin https://github.com/Njanja2025/NeuroScribeCopilot.git
    Write-Host "✅ GitHub remote added" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Remote might already exist, setting URL..." -ForegroundColor Yellow
    try {
        git remote set-url origin https://github.com/Njanja2025/NeuroScribeCopilot.git
        Write-Host "✅ GitHub remote URL updated" -ForegroundColor Green
    } catch {
        Write-Host "❌ GitHub connection failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""

# Step 9: Push to GitHub
Write-Host "Step 9: Pushing to GitHub..." -ForegroundColor Yellow
try {
    git branch -M main
    git push -u origin main
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Push failed: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "You may need to authenticate with GitHub first" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎉 FINAL BUILD COMPLETE!" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📦 Created Packages:" -ForegroundColor Green
Write-Host "   - NeuroScribe-Portable-v1.0-FINAL-$timestamp.zip" -ForegroundColor White
Write-Host "   - NeuroScribe-Professional-v1.0-$timestamp.zip" -ForegroundColor White
Write-Host "   - NeuroScribe-Source-v1.0-$timestamp.zip" -ForegroundColor White
Write-Host "   - release-package/ (GitHub release folder)" -ForegroundColor White

Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Go to GitHub: https://github.com/Njanja2025/NeuroScribeCopilot" -ForegroundColor White
Write-Host "   2. Create a new release (v1.0)" -ForegroundColor White
Write-Host "   3. Upload all files from release-package/ folder" -ForegroundColor White
Write-Host "   4. Deploy to Streamlit Cloud" -ForegroundColor White

Write-Host ""
Write-Host "🚀 Ready for distribution!" -ForegroundColor Green
Write-Host ""

Read-Host "Press Enter to continue" 
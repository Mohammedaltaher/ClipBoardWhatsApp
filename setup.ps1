# Smart Clipboard WhatsApp Sender - Windows Setup Script
# Run this script to automatically setup and build the application

Write-Host "📱 Smart Clipboard WhatsApp Sender - Windows Setup" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Check if Python is installed
Write-Host "`n🔍 Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.7+ from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is available
Write-Host "`n🔧 Checking pip..." -ForegroundColor Yellow
try {
    $pipVersion = python -m pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ pip is available" -ForegroundColor Green
    } else {
        throw "pip not found"
    }
} catch {
    Write-Host "❌ pip is not available" -ForegroundColor Red
    exit 1
}

# Run the setup script
Write-Host "`n🚀 Running setup and build process..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

try {
    python setup.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n🎉 Setup completed successfully!" -ForegroundColor Green
        Write-Host "`n📁 Check the following folders:" -ForegroundColor Cyan
        Write-Host "   • SmartClipboardWhatsApp_Distribution/ (for sharing)" -ForegroundColor White
        Write-Host "   • dist/ClipboardWhatsAppSender.exe (standalone executable)" -ForegroundColor White
        
        Write-Host "`n🚀 Ready to use!" -ForegroundColor Green
        Write-Host "Double-click ClipboardWhatsAppSender.exe to start the app" -ForegroundColor White
    } else {
        throw "Setup failed"
    }
} catch {
    Write-Host "`n❌ Setup failed. Please check the error messages above." -ForegroundColor Red
    exit 1
}

Write-Host "`n✨ Thank you for using Smart Clipboard WhatsApp Sender!" -ForegroundColor Magenta
Read-Host "Press Enter to exit"

@echo off
title Smart Clipboard WhatsApp Sender
echo.
echo 📱 Smart Clipboard WhatsApp Sender
echo ================================
echo.
echo 🚀 Starting the application...
echo.

REM Check if the executable exists
if exist "ClipboardWhatsAppSender.exe" (
    echo ✅ Found executable, launching...
    start "" "ClipboardWhatsAppSender.exe"
    echo.
    echo 💡 The app is now running in the background
    echo    Copy phone numbers to clipboard to test it!
    echo.
    timeout /t 3 >nul
) else (
    echo ❌ ClipboardWhatsAppSender.exe not found
    echo.
    echo 📋 To build the executable:
    echo    1. Run: python setup.py
    echo    2. Or use: setup.ps1
    echo.
    pause
)

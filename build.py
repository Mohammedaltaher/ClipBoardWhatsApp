import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=ClipboardWhatsAppSender",
        "--icon=icon.ico",  # Optional: add an icon file
        "--add-data=config.json;.",  # Include config file if it exists
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n✅ Build completed successfully!")
        print("📁 Executable created in: dist/ClipboardWhatsAppSender.exe")
        print("\n🚀 You can now distribute the .exe file to run on any Windows machine!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
    except FileNotFoundError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        build_executable()

def main():
    print("🔨 Building Smart Clipboard WhatsApp Sender...")
    print("=" * 50)
    
    # Install requirements first
    install_requirements()
    
    # Build executable
    build_executable()
    
    print("\n📋 Next steps:")
    print("1. Test the executable: dist/ClipboardWhatsAppSender.exe")
    print("2. Copy phone numbers to clipboard while app is running")
    print("3. Enjoy automated WhatsApp messaging! 🎉")

if __name__ == "__main__":
    main()

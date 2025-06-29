#!/usr/bin/env python3
"""
Setup and Build Script for Smart Clipboard WhatsApp Sender
Handles installation, testing, and building executable
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

class SetupBuilder:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    def run_command(self, command, description):
        """Run a command and handle errors"""
        print(f"\n🔧 {description}...")
        try:
            result = subprocess.run(command, shell=True, check=True, 
                                  capture_output=True, text=True)
            print(f"✅ {description} completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed:")
            print(f"Error: {e.stderr}")
            return False
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        self.print_header("CHECKING PYTHON VERSION")
        
        version = sys.version_info
        if version.major >= 3 and version.minor >= 7:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor}.{version.micro} is too old")
            print("Please install Python 3.7 or newer")
            return False
    
    def install_dependencies(self):
        """Install required Python packages"""
        self.print_header("INSTALLING DEPENDENCIES")
        
        # Install basic requirements
        if not self.run_command(
            f"{sys.executable} -m pip install --upgrade pip",
            "Upgrading pip"
        ):
            return False
        
        if not self.run_command(
            f"{sys.executable} -m pip install -r requirements.txt",
            "Installing project requirements"
        ):
            return False
        
        # Install PyInstaller for building executable
        if not self.run_command(
            f"{sys.executable} -m pip install pyinstaller",
            "Installing PyInstaller"
        ):
            return False
        
        return True
    
    def run_tests(self):
        """Run the test suite"""
        self.print_header("RUNNING TESTS")
        
        return self.run_command(
            f"{sys.executable} test.py",
            "Running phone number detection tests"
        )
    
    def clean_build(self):
        """Clean previous build artifacts"""
        self.print_header("CLEANING BUILD ARTIFACTS")
        
        dirs_to_clean = [self.dist_dir, self.build_dir, self.project_dir / "__pycache__"]
        
        for dir_path in dirs_to_clean:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"🗑️ Removed {dir_path}")
        
        # Remove .spec files
        for spec_file in self.project_dir.glob("*.spec"):
            spec_file.unlink()
            print(f"🗑️ Removed {spec_file}")
        
        print("✅ Build artifacts cleaned")
    
    def build_executable(self):
        """Build the executable using PyInstaller"""
        self.print_header("BUILDING EXECUTABLE")
        
        # Prepare PyInstaller command
        cmd_parts = [
            "pyinstaller",
            "--onefile",                    # Single file executable
            "--windowed",                   # No console window
            "--name=ClipboardWhatsAppSender",  # Executable name
            "--add-data=config.json;.",     # Include config file
        ]
        
        # Add icon if available
        icon_path = self.project_dir / "icon.ico"
        if icon_path.exists():
            cmd_parts.append(f"--icon={icon_path}")
        
        cmd_parts.append("main.py")
        
        command = " ".join(cmd_parts)
        
        if self.run_command(command, "Building executable with PyInstaller"):
            exe_path = self.dist_dir / "ClipboardWhatsAppSender.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"🎉 Executable created: {exe_path}")
                print(f"📁 Size: {size_mb:.1f} MB")
                return True
        
        return False
    
    def create_distribution_package(self):
        """Create a distribution package with executable and docs"""
        self.print_header("CREATING DISTRIBUTION PACKAGE")
        
        # Create distribution folder
        package_dir = self.project_dir / "SmartClipboardWhatsApp_Distribution"
        if package_dir.exists():
            shutil.rmtree(package_dir)
        
        package_dir.mkdir()
        
        # Copy executable
        exe_source = self.dist_dir / "ClipboardWhatsAppSender.exe"
        if exe_source.exists():
            shutil.copy2(exe_source, package_dir)
            print("📦 Copied executable")
        
        # Copy documentation
        files_to_copy = ["README.md", "config.json"]
        for file_name in files_to_copy:
            source_file = self.project_dir / file_name
            if source_file.exists():
                shutil.copy2(source_file, package_dir)
                print(f"📄 Copied {file_name}")
        
        # Create quick start guide
        quick_start = package_dir / "QUICK_START.txt"
        with open(quick_start, 'w') as f:
            f.write("""Smart Clipboard WhatsApp Sender - Quick Start Guide
=====================================================

🚀 GETTING STARTED:
1. Double-click ClipboardWhatsAppSender.exe to launch
2. Click "Start Monitoring" button
3. Copy any phone number to your clipboard (Ctrl+C)
4. WhatsApp Web will open automatically!

📱 SUPPORTED PHONE FORMATS:
- International: +1234567890, +971 50 123 4567
- US Format: (234) 567-8900, 234-567-8900
- Simple: 2345678900, 123 456 7890

⚙️ CUSTOMIZATION:
- Edit the default message in the app
- Toggle auto-open browser setting
- Clear duplicate detection as needed

🔧 TROUBLESHOOTING:
- Ensure your default browser is set
- Check internet connection for WhatsApp Web
- Try running as administrator if needed

💡 USE CASES:
- Customer service and support
- Sales and lead follow-up
- Real estate client communication
- Any WhatsApp business messaging

For detailed documentation, see README.md
""")
        
        print(f"✅ Distribution package created: {package_dir}")
        return True
    
    def run_full_setup(self):
        """Run the complete setup and build process"""
        self.print_header("SMART CLIPBOARD WHATSAPP SENDER - SETUP & BUILD")
        
        print("🚀 Starting complete setup and build process...")
        
        # Step 1: Check Python version
        if not self.check_python_version():
            return False
        
        # Step 2: Install dependencies
        if not self.install_dependencies():
            return False
        
        # Step 3: Run tests
        if not self.run_tests():
            print("⚠️ Tests failed, but continuing with build...")
        
        # Step 4: Clean previous builds
        self.clean_build()
        
        # Step 5: Build executable
        if not self.build_executable():
            return False
        
        # Step 6: Create distribution package
        if not self.create_distribution_package():
            return False
        
        # Success!
        self.print_header("BUILD COMPLETED SUCCESSFULLY!")
        print("🎉 Smart Clipboard WhatsApp Sender is ready!")
        print("\n📁 Distribution files:")
        print("   • SmartClipboardWhatsApp_Distribution/")
        print("   • dist/ClipboardWhatsAppSender.exe")
        print("\n🚀 Next steps:")
        print("   1. Test the executable")
        print("   2. Share the Distribution folder")
        print("   3. Enjoy automated WhatsApp messaging!")
        
        return True

def main():
    """Main function"""
    builder = SetupBuilder()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "install":
            builder.install_dependencies()
        elif command == "test":
            builder.run_tests()
        elif command == "clean":
            builder.clean_build()
        elif command == "build":
            builder.build_executable()
        elif command == "package":
            builder.create_distribution_package()
        else:
            print("Usage: python setup.py [install|test|clean|build|package]")
            print("Or run without arguments for full setup")
    else:
        # Run full setup
        success = builder.run_full_setup()
        if not success:
            sys.exit(1)

if __name__ == "__main__":
    main()

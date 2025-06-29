#!/usr/bin/env python3
"""
Test the WhatsApp app functionality
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ClipboardWhatsAppSender

def test_whatsapp_features():
    """Test the WhatsApp opening features"""
    
    print("📱 Testing WhatsApp Features")
    print("=" * 35)
    print()
    
    app = ClipboardWhatsAppSender()
    
    # Test phone number
    test_number = "+1234567890"
    test_message = "Hello! This is a test message."
    
    print(f"📞 Test Number: {test_number}")
    print(f"💬 Test Message: {test_message}")
    print()
    
    # Test URL generation
    print("🔗 Testing URL Generation:")
    url = app.generate_whatsapp_url(test_number, test_message)
    print(f"   URL: {url}")
    print()
    
    # Test WhatsApp app detection
    print("📱 Testing WhatsApp App Availability:")
    try:
        import subprocess
        
        # Try to detect if WhatsApp desktop is installed
        result = subprocess.run(['where', 'whatsapp'], 
                              shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ WhatsApp desktop might be available")
        else:
            print("   ℹ️ WhatsApp desktop not found via 'where' command")
            
        # Try the URL scheme approach
        whatsapp_url = f"whatsapp://send?phone={test_number.replace('+', '')}&text=Test"
        print(f"   🔗 WhatsApp URL scheme: {whatsapp_url}")
        
    except Exception as e:
        print(f"   ⚠️ Error checking WhatsApp app: {e}")
    
    print()
    print("🔧 Configuration Options:")
    print(f"   • use_whatsapp_app: {app.config.get('use_whatsapp_app', False)}")
    print(f"   • auto_open_browser: {app.config.get('auto_open_browser', True)}")
    print(f"   • numbers_only_mode: {app.config.get('numbers_only_mode', False)}")
    print(f"   • avoid_duplicates: {app.config.get('avoid_duplicates', True)}")
    
    print()
    print("✨ Duplicate Prevention Improvements:")
    print("   • Added immediate duplicate tracking")
    print("   • Added 0.5s delay after processing")
    print("   • Better clipboard change detection")
    
    print()
    print("📋 How to Use:")
    print("=" * 15)
    print("1. 🚀 Launch: python main.py")
    print("2. ⚙️ Settings: Check 'Use WhatsApp desktop app'")
    print("3. ▶️ Start: Click 'Start Monitoring'")
    print("4. 📋 Copy: Copy any phone number")
    print("5. 📱 Result: WhatsApp app opens (or web as fallback)")

if __name__ == "__main__":
    test_whatsapp_features()

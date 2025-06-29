#!/usr/bin/env python3
"""
Demonstration of the 'Numbers Only' feature
Shows the difference between normal and numbers-only mode
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ClipboardWhatsAppSender

def demo_numbers_only_feature():
    """Demonstrate the new Numbers Only feature"""
    
    print("🎯 Smart Clipboard WhatsApp Sender - Numbers Only Feature Demo")
    print("=" * 65)
    print()
    
    app = ClipboardWhatsAppSender()
    
    # Test cases to demonstrate the feature
    test_cases = [
        "+1234567890",                           # Just a number
        "  +1234567890  ",                      # Number with spaces
        "(555) 123-4567",                       # Formatted number
        "Call me at +1234567890",               # Number with text before
        "+1234567890 is my number",             # Number with text after
        "My number is +1234567890 please call", # Number in sentence
        "+1234567890\nSecond line",             # Number with extra content
        "Contact: +1234567890",                 # Business card format
    ]
    
    print("📱 Testing different clipboard content:")
    print()
    
    for i, clipboard_content in enumerate(test_cases, 1):
        print(f"{i}. Testing: '{clipboard_content}'")
        
        # Test normal detection (any phone number)
        normal_detection = app.is_valid_phone_number(clipboard_content)
        
        # Test numbers-only detection
        numbers_only_detection = app.is_phone_number_only(clipboard_content)
        
        print(f"   📋 Normal mode (any number):     {'✅ DETECTED' if normal_detection else '❌ NOT DETECTED'}")
        print(f"   🎯 Numbers only mode:           {'✅ DETECTED' if numbers_only_detection else '❌ NOT DETECTED'}")
        
        if normal_detection:
            extracted = app.extract_phone_number(clipboard_content)
            print(f"   📞 Extracted number: {extracted}")
        
        # Show what would happen in each mode
        print(f"   🔄 Result:")
        if normal_detection:
            print(f"      • Normal mode: WhatsApp would open")
        else:
            print(f"      • Normal mode: No action")
            
        if numbers_only_detection:
            print(f"      • Numbers only mode: WhatsApp would open")
        else:
            print(f"      • Numbers only mode: No action (has extra text)")
        
        print()
    
    print("💡 Use Cases for Numbers Only Mode:")
    print("=" * 40)
    print("✅ PERFECT FOR:")
    print("   • Copying numbers from spreadsheets/databases")
    print("   • Clean phone number lists")
    print("   • Avoiding accidental triggers from emails/documents")
    print("   • Professional environments with clean data")
    print()
    print("🔄 NORMAL MODE BETTER FOR:")
    print("   • Copying from business cards or websites")
    print("   • Extracting numbers from mixed content")
    print("   • Social media or informal text sources")
    print("   • When numbers come with context")
    print()
    
    print("⚙️ How to Enable:")
    print("=" * 15)
    print("1. Launch the application")
    print("2. In the Settings section, check '📱 Numbers only (no extra text)'")
    print("3. Click 'Start Monitoring'")
    print("4. Now only standalone phone numbers will trigger WhatsApp!")
    print()
    
    print("🎉 This feature gives you precise control over when WhatsApp opens,")
    print("   preventing unwanted triggers while keeping your workflow smooth!")

if __name__ == "__main__":
    demo_numbers_only_feature()

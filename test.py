#!/usr/bin/env python3
"""
Test script for Smart Clipboard WhatsApp Sender
Tests phone number detection and URL generation
"""

import sys
import os

# Add the main directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ClipboardWhatsAppSender

def test_phone_detection():
    """Test phone number detection functionality"""
    app = ClipboardWhatsAppSender()
    
    # Test cases with various phone number formats
    test_cases = [
        # Format, Input, Expected Result, Numbers Only Result
        ("International with +", "+1234567890", True, True),
        ("International formatted", "+1 234 567 8900", True, True),
        ("US format with parentheses", "(234) 567-8900", True, True),
        ("US format with dashes", "234-567-8900", True, True),
        ("Simple 10 digits", "2345678900", True, True),
        ("International UK", "+44 20 7946 0958", True, True),
        ("International UAE", "+971 50 123 4567", True, True),
        ("Invalid - too short", "12345", False, False),
        ("Invalid - letters", "abc123def", False, False),
        ("Invalid - special chars", "+++---123", False, False),
        ("Valid with spaces", "123 456 7890", True, True),
        ("Valid with dots", "123.456.7890", True, True),
        ("Number with text before", "Call me at +1234567890", True, False),
        ("Number with text after", "+1234567890 is my number", True, False),
        ("Number in sentence", "My number is +1234567890 please call", True, False),
        ("Just number with newlines", "\n+1234567890\n", True, True),
        ("Number with extra spaces", "  +1234567890  ", True, True),
    ]
    
    print("🧪 Testing Phone Number Detection")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for description, test_input, expected_any, expected_only in test_cases:
        result_any = app.is_valid_phone_number(test_input)
        result_only = app.is_phone_number_only(test_input)
        
        status_any = "✅ PASS" if result_any == expected_any else "❌ FAIL"
        status_only = "✅ PASS" if result_only == expected_only else "❌ FAIL"
        
        print(f"{description}")
        print(f"  {status_any} Any detection: '{test_input}' -> {result_any} (expected {expected_any})")
        print(f"  {status_only} Only detection: '{test_input}' -> {result_only} (expected {expected_only})")
        
        if result_any == expected_any and result_only == expected_only:
            passed += 1
        else:
            failed += 1
        
        # Test extraction if it should be valid
        if expected_any and result_any:
            extracted = app.extract_phone_number(test_input)
            print(f"  Extracted: {extracted}")
        
        print()
    
    print(f"📊 Results: {passed} passed, {failed} failed")
    return failed == 0

def test_url_generation():
    """Test WhatsApp URL generation"""
    app = ClipboardWhatsAppSender()
    
    print("🔗 Testing URL Generation")
    print("=" * 30)
    
    test_numbers = [
        "+1234567890",
        "+971501234567",
        "+44207946958"
    ]
    
    test_message = "Hello! This is a test message."
    
    for number in test_numbers:
        url = app.generate_whatsapp_url(number, test_message)
        print(f"📞 {number}")
        print(f"🔗 {url}")
        print()

def test_config_loading():
    """Test configuration loading and saving"""
    app = ClipboardWhatsAppSender()
    
    print("⚙️ Testing Configuration")
    print("=" * 25)
    
    # Test default config
    print("📋 Default configuration:")
    for key, value in app.config.items():
        print(f"   {key}: {value}")
    
    # Test saving config
    print("\n💾 Testing config save...")
    app.config["test_key"] = "test_value"
    app.save_config()
    
    # Test loading config
    print("📥 Testing config load...")
    new_app = ClipboardWhatsAppSender()
    
    if "test_key" in new_app.config and new_app.config["test_key"] == "test_value":
        print("✅ Config save/load working correctly")
    else:
        print("❌ Config save/load failed")
    
    # Clean up test config
    if "test_key" in new_app.config:
        del new_app.config["test_key"]
        new_app.save_config()

def main():
    """Run all tests"""
    print("🚀 Smart Clipboard WhatsApp Sender - Test Suite")
    print("=" * 50)
    print()
    
    # Run tests
    phone_test_passed = test_phone_detection()
    print()
    
    test_url_generation()
    print()
    
    test_config_loading()
    print()
    
    # Summary
    print("📋 Test Summary")
    print("=" * 15)
    
    if phone_test_passed:
        print("✅ All phone detection tests passed!")
        print("🎉 The application should work correctly.")
    else:
        print("❌ Some phone detection tests failed.")
        print("⚠️ Please review the phone number patterns.")
    
    print()
    print("💡 To test the full application:")
    print("   1. Run: python main.py")
    print("   2. Click 'Start Monitoring'")
    print("   3. Copy phone numbers to clipboard")
    print("   4. Watch WhatsApp Web open automatically!")

if __name__ == "__main__":
    main()

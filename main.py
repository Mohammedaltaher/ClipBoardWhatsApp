#!/usr/bin/env python3
"""
Smart Clipboard WhatsApp Sender
A Windows utility that monitors clipboard for phone numbers and opens WhatsApp Web
"""

import pyperclip
import webbrowser
import re
import time
import threading
import json
import os
from urllib.parse import quote
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import logging

class ClipboardWhatsAppSender:
    def __init__(self):
        self.running = False
        self.last_clipboard = ""
        self.processed_numbers = set()
        self.config_file = "config.json"
        self.log_file = "clipboard_whatsapp.log"
        
        # Setup logging
        self.setup_logging()
        
        # Load configuration
        self.config = self.load_config()
        
        # Phone number regex patterns for global formats
        self.phone_patterns = [
            r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,4}',  # International with various separators
            r'\+\d{1,3}\s?\d{6,14}',  # International format with +
            r'\d{10,15}',             # Simple 10-15 digit numbers
            r'\(\d{3}\)\s?\d{3}[-.\s]?\d{4}',  # US format (xxx) xxx-xxxx
            r'\d{3}[-.\s]\d{3}[-.\s]\d{4}',  # US format xxx-xxx-xxxx or xxx.xxx.xxxx
            r'\d{3}\s\d{3}\s\d{4}',   # US format with spaces
        ]
        
        # GUI components
        self.root = None
        self.status_var = None
        self.message_var = None
        self.log_text = None
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self):
        """Load configuration from file or create default"""
        default_config = {
            "default_message": "Hello! I got your number and wanted to reach out.",
            "monitor_enabled": True,
            "check_interval": 1.0,
            "avoid_duplicates": True,
            "auto_open_browser": True,
            "numbers_only_mode": False,
            "use_whatsapp_app": False
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
                
        return default_config
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def is_valid_phone_number(self, text):
        """Check if text contains a valid phone number"""
        # Clean the text
        text = text.strip()
        
        # Check against all patterns
        for pattern in self.phone_patterns:
            if re.search(pattern, text):
                return True
        
        return False
    
    def is_phone_number_only(self, text):
        """Check if text contains ONLY a phone number (no extra text)"""
        text = text.strip()
        
        # If the text is empty after stripping, it's not a valid phone number
        if not text:
            return False
        
        # Extract the phone number from the text
        extracted_number = None
        for pattern in self.phone_patterns:
            match = re.search(pattern, text)
            if match:
                extracted_number = match.group()
                break
        
        if not extracted_number:
            return False
        
        # Clean both the original text and the extracted number for comparison
        # Remove all non-alphanumeric characters except + for comparison
        clean_text = re.sub(r'[^\w+]', '', text)
        clean_number = re.sub(r'[^\w+]', '', extracted_number)
        
        # If the cleaned text equals the cleaned number, then it's only a phone number
        return clean_text == clean_number
    
    def extract_phone_number(self, text):
        """Extract and clean phone number from text"""
        # Try each pattern
        for pattern in self.phone_patterns:
            match = re.search(pattern, text)
            if match:
                number = match.group()
                # Clean the number - remove all non-digit characters except +
                cleaned = re.sub(r'[^\d+]', '', number)
                
                # Handle different number formats
                if cleaned.startswith('+'):
                    # Already has country code
                    return cleaned
                elif len(cleaned) == 10:
                    # Likely US number without country code
                    return '+1' + cleaned
                elif len(cleaned) == 11 and cleaned.startswith('1'):
                    # US number with 1 prefix
                    return '+' + cleaned
                elif len(cleaned) >= 10:
                    # International number without + prefix
                    # For common country codes, try to detect
                    if cleaned.startswith('44'):  # UK
                        return '+' + cleaned
                    elif cleaned.startswith('971'):  # UAE
                        return '+' + cleaned
                    elif cleaned.startswith('91'):  # India
                        return '+' + cleaned
                    else:
                        # Default: add + prefix
                        return '+' + cleaned
                
                return cleaned if cleaned else None
        
        return None
    
    def generate_whatsapp_url(self, phone_number, message=None):
        """Generate WhatsApp Web URL"""
        if message is None:
            message = self.config.get("default_message", "Hello!")
        
        # Encode the message for URL
        encoded_message = quote(message)
        
        # Remove + from phone number for URL
        clean_number = phone_number.replace('+', '')
        
        # Generate WhatsApp URL
        url = f"https://wa.me/{clean_number}?text={encoded_message}"
        
        return url
    
    def open_whatsapp(self, phone_number, message=None):
        """Open WhatsApp (app or web) with the phone number"""
        try:
            if message is None:
                message = self.config.get("default_message", "Hello!")
            
            # Check if we should use WhatsApp desktop app
            use_app = self.config.get("use_whatsapp_app", False)
            
            if use_app:
                # Try to open WhatsApp desktop app
                success = self.open_whatsapp_app(phone_number, message)
                if success:
                    return True
                else:
                    # Fallback to web if app fails
                    self.log_to_gui("⚠️ WhatsApp app not found, using web version...")
            
            # Open WhatsApp Web
            return self.open_whatsapp_web(phone_number, message)
                
        except Exception as e:
            self.logger.error(f"Error opening WhatsApp: {e}")
            self.log_to_gui(f"❌ Error opening WhatsApp: {e}")
            return False
    
    def open_whatsapp_app(self, phone_number, message):
        """Try to open WhatsApp desktop app"""
        import subprocess
        import os
        
        try:
            # Clean phone number (remove + for the URL)
            clean_number = phone_number.replace('+', '')
            
            # Encode the message for URL
            encoded_message = quote(message)
            
            # WhatsApp desktop app URL scheme
            whatsapp_url = f"whatsapp://send?phone={clean_number}&text={encoded_message}"
            
            # Try to open with the URL scheme
            if os.name == 'nt':  # Windows
                subprocess.run(['start', whatsapp_url], shell=True, check=True)
            else:  # macOS/Linux
                subprocess.run(['open', whatsapp_url], check=True)
            
            self.logger.info(f"Opened WhatsApp app for {phone_number}")
            self.log_to_gui(f"📱 Opened WhatsApp app for {phone_number}")
            return True
            
        except subprocess.CalledProcessError:
            self.logger.warning("WhatsApp desktop app not available")
            return False
        except Exception as e:
            self.logger.warning(f"Failed to open WhatsApp app: {e}")
            return False
    
    def open_whatsapp_web(self, phone_number, message):
        """Open WhatsApp Web with the phone number"""
        try:
            url = self.generate_whatsapp_url(phone_number, message)
            
            if self.config.get("auto_open_browser", True):
                webbrowser.open(url)
                self.logger.info(f"Opened WhatsApp Web for {phone_number}")
                self.log_to_gui(f"🌐 Opened WhatsApp Web for {phone_number}")
                return True
            else:
                self.logger.info(f"Generated URL for {phone_number}: {url}")
                self.log_to_gui(f"📋 Generated URL for {phone_number}")
                return url
                
        except Exception as e:
            self.logger.error(f"Error opening WhatsApp Web: {e}")
            return False
    
    def monitor_clipboard(self):
        """Monitor clipboard for phone numbers"""
        self.logger.info("Started clipboard monitoring")
        self.log_to_gui("🔍 Started clipboard monitoring...")
        
        while self.running:
            try:
                # Get current clipboard content
                current_clipboard = pyperclip.paste()
                
                # Check if clipboard content changed
                if current_clipboard != self.last_clipboard and current_clipboard.strip():
                    self.last_clipboard = current_clipboard
                    
                    # Check detection mode
                    numbers_only_mode = self.config.get("numbers_only_mode", False)
                    
                    # Determine if we should process this clipboard content
                    should_process = False
                    
                    if numbers_only_mode:
                        # Only process if clipboard contains ONLY a phone number
                        if self.is_phone_number_only(current_clipboard):
                            should_process = True
                        else:
                            # Log that we're skipping due to extra text
                            if self.is_valid_phone_number(current_clipboard):
                                self.log_to_gui(f"⏭️ Skipping (contains extra text): {current_clipboard[:30]}...")
                    else:
                        # Process if clipboard contains any valid phone number
                        if self.is_valid_phone_number(current_clipboard):
                            should_process = True
                    
                    if should_process:
                        phone_number = self.extract_phone_number(current_clipboard)
                        
                        if phone_number:
                            # Check for duplicates if enabled
                            if self.config.get("avoid_duplicates", True):
                                if phone_number in self.processed_numbers:
                                    self.log_to_gui(f"⚠️ Skipping duplicate: {phone_number}")
                                    time.sleep(self.config.get("check_interval", 1.0))
                                    continue
                            
                            # Add to processed numbers immediately to prevent double processing
                            self.processed_numbers.add(phone_number)
                            
                            # Log the detection
                            self.logger.info(f"Detected phone number: {phone_number}")
                            self.log_to_gui(f"📞 Detected: {phone_number}")
                            
                            # Add a small delay to prevent rapid duplicate processing
                            time.sleep(0.5)
                            
                            # Open WhatsApp
                            message = self.config.get("default_message", "Hello!")
                            if hasattr(self, 'message_var') and self.message_var:
                                custom_message = self.message_var.get()
                                if custom_message.strip():
                                    message = custom_message.strip()
                            
                            self.open_whatsapp(phone_number, message)
                            message = self.config.get("default_message", "Hello!")
                            if hasattr(self, 'message_var') and self.message_var:
                                custom_message = self.message_var.get()
                                if custom_message.strip():
                                    message = custom_message.strip()
                            
                            self.open_whatsapp(phone_number, message)
                
                # Sleep before next check
                time.sleep(self.config.get("check_interval", 1.0))
                
            except Exception as e:
                self.logger.error(f"Error in clipboard monitoring: {e}")
                time.sleep(2.0)  # Wait longer on error
    
    def start_monitoring(self):
        """Start clipboard monitoring in background thread"""
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
            self.monitor_thread.start()
            self.update_status("Running")
    
    def stop_monitoring(self):
        """Stop clipboard monitoring"""
        self.running = False
        self.update_status("Stopped")
        self.log_to_gui("🛑 Clipboard monitoring stopped")
    
    def update_status(self, status):
        """Update status in GUI"""
        if self.status_var:
            self.status_var.set(f"Status: {status}")
    
    def log_to_gui(self, message):
        """Add log message to GUI"""
        if self.log_text:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_text.see(tk.END)
    
    def create_gui(self):
        """Create the GUI interface"""
        self.root = tk.Tk()
        self.root.title("Smart Clipboard WhatsApp Sender")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📱 Smart Clipboard WhatsApp Sender", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Status
        self.status_var = tk.StringVar(value="Status: Stopped")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                font=('Arial', 10))
        status_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        start_btn = ttk.Button(button_frame, text="▶️ Start Monitoring", 
                              command=self.start_monitoring)
        start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        stop_btn = ttk.Button(button_frame, text="⏹️ Stop Monitoring", 
                             command=self.stop_monitoring)
        stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = ttk.Button(button_frame, text="🗑️ Clear Duplicates", 
                              command=self.clear_duplicates)
        clear_btn.pack(side=tk.LEFT)
        
        # Message customization
        message_frame = ttk.LabelFrame(main_frame, text="Default Message", padding="10")
        message_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        message_frame.columnconfigure(0, weight=1)
        
        self.message_var = tk.StringVar(value=self.config.get("default_message", "Hello!"))
        message_entry = ttk.Entry(message_frame, textvariable=self.message_var, width=60)
        message_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        save_msg_btn = ttk.Button(message_frame, text="💾 Save", 
                                 command=self.save_message)
        save_msg_btn.grid(row=0, column=1)
        
        # Settings
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        
        self.auto_open_var = tk.BooleanVar(value=self.config.get("auto_open_browser", True))
        auto_open_cb = ttk.Checkbutton(settings_frame, text="Auto-open browser", 
                                      variable=self.auto_open_var,
                                      command=self.save_settings)
        auto_open_cb.grid(row=0, column=0, sticky=tk.W)
        
        self.avoid_duplicates_var = tk.BooleanVar(value=self.config.get("avoid_duplicates", True))
        avoid_dup_cb = ttk.Checkbutton(settings_frame, text="Avoid duplicates", 
                                      variable=self.avoid_duplicates_var,
                                      command=self.save_settings)
        avoid_dup_cb.grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        self.numbers_only_var = tk.BooleanVar(value=self.config.get("numbers_only_mode", False))
        numbers_only_cb = ttk.Checkbutton(settings_frame, text="Numbers only (no extra text)", 
                                         variable=self.numbers_only_var,
                                         command=self.save_settings)
        numbers_only_cb.grid(row=1, column=0, sticky=tk.W, columnspan=2, pady=(5, 0))
        
        self.use_whatsapp_app_var = tk.BooleanVar(value=self.config.get("use_whatsapp_app", False))
        whatsapp_app_cb = ttk.Checkbutton(settings_frame, text="Use WhatsApp desktop app (instead of web)", 
                                         variable=self.use_whatsapp_app_var,
                                         command=self.save_settings)
        whatsapp_app_cb.grid(row=2, column=0, sticky=tk.W, columnspan=2, pady=(5, 0))
        
        # Log display
        log_frame = ttk.LabelFrame(main_frame, text="Activity Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        # Instructions
        instructions = (
            "📋 Instructions:\n"
            "1. Click 'Start Monitoring' to begin watching clipboard\n"
            "2. Copy any phone number to your clipboard\n"
            "3. WhatsApp will open automatically with your message\n"
            "4. Customize the default message above as needed\n"
            "5. Enable 'Numbers only' to process only standalone numbers\n"
            "6. Enable 'WhatsApp desktop app' to use installed app instead of web\n"
            "   (ignores numbers mixed with other text)"
        )
        self.log_to_gui(instructions)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        return self.root
    
    def save_message(self):
        """Save the default message"""
        if self.message_var:
            self.config["default_message"] = self.message_var.get()
            self.save_config()
            self.log_to_gui("💾 Default message saved")
    
    def save_settings(self):
        """Save settings changes"""
        if hasattr(self, 'auto_open_var'):
            self.config["auto_open_browser"] = self.auto_open_var.get()
        if hasattr(self, 'avoid_duplicates_var'):
            self.config["avoid_duplicates"] = self.avoid_duplicates_var.get()
        if hasattr(self, 'numbers_only_var'):
            self.config["numbers_only_mode"] = self.numbers_only_var.get()
        if hasattr(self, 'use_whatsapp_app_var'):
            self.config["use_whatsapp_app"] = self.use_whatsapp_app_var.get()
        self.save_config()
        self.log_to_gui("⚙️ Settings saved")
    
    def clear_duplicates(self):
        """Clear the processed numbers set"""
        self.processed_numbers.clear()
        self.log_to_gui("🗑️ Duplicate detection cleared")
    
    def on_closing(self):
        """Handle application closing"""
        self.stop_monitoring()
        self.save_config()
        if self.root:
            self.root.destroy()

def main():
    """Main function"""
    app = ClipboardWhatsAppSender()
    
    # Create and run GUI
    root = app.create_gui()
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()

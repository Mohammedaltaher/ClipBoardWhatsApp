# 📱 Smart Clipboard WhatsApp Sender

A lightweight Windows utility that monitors your clipboard for phone numbers and automatically opens WhatsApp Web with a predefined message, perfect for customer service, sales, and lead generation workflows.

## 🌟 Features

- **🔍 Automatic Clipboard Monitoring**: Continuously watches for phone numbers copied to clipboard
- **📞 Global Phone Number Detection**: Supports various international phone number formats
- **💬 Customizable Messages**: Set your own default message template
- **🌐 Auto WhatsApp Launch**: Opens WhatsApp Web instantly with the detected number
- **🛑 Duplicate Prevention**: Avoids opening the same number multiple times
- **🔒 Privacy Focused**: Runs locally, no data stored externally
- **🎨 User-Friendly GUI**: Easy-to-use interface with real-time activity logs
- **📦 Portable**: Single executable file, no installation required

## 🚀 Quick Start

### Option 1: Run from Source (Developer)

1. **Clone/Download** this repository
2. **Install Python 3.7+** if not already installed
3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
4. **Run the application**:
   ```powershell
   python main.py
   ```

### Option 2: Build Executable (Recommended)

1. **Run the build script**:
   ```powershell
   python build.py
   ```
2. **Find your executable** in `dist/ClipboardWhatsAppSender.exe`
3. **Double-click to run** - no installation needed!

## 📋 How to Use

1. **Launch the Application**
   - Run `ClipboardWhatsAppSender.exe` or `python main.py`
   - The GUI will open with monitoring controls

2. **Start Monitoring**
   - Click "▶️ Start Monitoring" button
   - The app will begin watching your clipboard

3. **Copy Phone Numbers**
   - Copy any phone number to your clipboard (Ctrl+C)
   - Supported formats:
     - `+1234567890`
     - `(123) 456-7890`
     - `123-456-7890`
     - `1234567890`
     - International formats with country codes

4. **WhatsApp Opens Automatically**
   - Your default browser opens WhatsApp Web
   - The number is pre-filled with your custom message
   - Ready to send!

## ⚙️ Configuration

### Default Message
- Customize the message sent with each number
- Edit in the GUI and click "💾 Save"
- Supports any text, emojis, and formatting

### Settings
- **Auto-open browser**: Toggle automatic WhatsApp Web opening
- **Avoid duplicates**: Prevent opening the same number twice
- **Numbers only (no extra text)**: Only detect standalone phone numbers
  - ✅ When enabled: Processes `+1234567890` but ignores `Call me at +1234567890`
  - ✅ When disabled: Processes both formats
- **Check interval**: How often to check clipboard (default: 1 second)

### Config File
Settings are automatically saved to `config.json`:

```json
{
  "default_message": "Hello! I got your number and wanted to reach out.",
  "monitor_enabled": true,
  "check_interval": 1.0,
  "avoid_duplicates": true,
  "auto_open_browser": true,
  "numbers_only_mode": false
}
```

## 📞 Supported Phone Number Formats

The app recognizes various phone number formats:

- **International**: `+1 234 567 8900`, `+44 20 7946 0958`
- **US Standard**: `(234) 567-8900`, `234-567-8900`
- **Simple**: `2345678900`, `447946095800`
- **Formatted**: `+1-234-567-8900`, `+44.20.7946.0958`

## 🎯 Use Cases

### Customer Service
- Copy customer phone numbers from CRM
- Instantly reach out via WhatsApp
- Consistent professional messaging

### Sales & Lead Generation
- Quick follow-up on leads
- Copy numbers from spreadsheets/databases
- Streamlined outreach process

### Real Estate
- Contact prospects immediately
- Follow up on property inquiries
- Professional communication

### Call Centers
- Switch from voice to WhatsApp seamlessly
- Handle multiple customer touchpoints
- Improve response times

## 🔧 Technical Details

### Dependencies
- **Python 3.7+**
- **pyperclip**: Clipboard monitoring
- **tkinter**: GUI interface (built into Python)
- **webbrowser**: Opening WhatsApp Web
- **re**: Phone number pattern matching

### System Requirements
- **Windows 7/8/10/11**
- **Internet connection** (for WhatsApp Web)
- **Default web browser** (Chrome, Firefox, Edge, etc.)

### Privacy & Security
- ✅ **No data transmission**: All processing happens locally
- ✅ **No phone number storage**: Numbers aren't saved permanently
- ✅ **No external servers**: Direct browser-to-WhatsApp communication
- ✅ **Open source**: Full code transparency

## 🐛 Troubleshooting

### App Won't Start
- Ensure Python 3.7+ is installed
- Install requirements: `pip install -r requirements.txt`
- Check for antivirus interference

### Phone Numbers Not Detected
- Verify number format (try adding country code)
- Check if clipboard access is blocked
- Restart the monitoring

### WhatsApp Doesn't Open
- Ensure default browser is set
- Check internet connection
- Verify WhatsApp Web is accessible

### Executable Issues
- Try running as administrator
- Check Windows Defender/antivirus settings
- Rebuild executable: `python build.py`

## 📁 Project Structure

```
ClipBoardWhatsApp/
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── build.py            # Build script for executable
├── README.md           # This file
├── config.json         # User settings (auto-generated)
├── clipboard_whatsapp.log  # Activity logs
└── dist/               # Built executable (after build)
    └── ClipboardWhatsAppSender.exe
```

## 🔄 Development

### Adding Features
1. **Fork** the repository
2. **Create** a feature branch
3. **Implement** your changes in `main.py`
4. **Test** thoroughly
5. **Submit** a pull request

### Common Modifications
- **Add new phone formats**: Edit `phone_patterns` in `ClipboardWhatsAppSender` class
- **Custom message templates**: Extend the message customization UI
- **Integration hooks**: Add webhook/API support for CRM systems
- **Hotkeys**: Add keyboard shortcuts for quick actions

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## 📞 Support

If you encounter any issues or need help:

1. Check the troubleshooting section above
2. Review the activity log for error messages
3. Create an issue on the repository

---

**Made with ❤️ for productivity and automation**

*Perfect for customer service teams, sales professionals, real estate agents, and anyone who communicates frequently via WhatsApp!*

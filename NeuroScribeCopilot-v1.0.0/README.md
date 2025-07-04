# 🧠 NeuroScribe PDF Copilot v1.0.0

**AI-powered PDF editing with GPT-4 and OCR support**

## 🚀 Quick Start

### For End Users
1. **Extract** this ZIP file to any folder
2. **Double-click:** `QUICK_START.bat`
3. **Set your OpenAI API key** in the `.env` file
4. **Enjoy!** 🎉

### For Advanced Users
1. **Install Python 3.8+** if not already installed
2. **Run:** `pip install -r requirements.txt`
3. **Set up:** `.env` file with your OpenAI API key
4. **Launch:** `python launcher.py`

## 🔧 Features

- **📄 PDF Processing**: Upload and edit any PDF
- **🧠 GPT-4 Integration**: AI-powered text rewriting
- **🔍 OCR Support**: Extract text from scanned PDFs (requires Tesseract)
- **🔓 PDF Unlock**: Handle encrypted documents (requires qpdf)
- **🛡️ Bulletproof**: Robust error handling and recovery

## 📋 Requirements

- **Windows 10/11**
- **Python 3.8+** (included in package)
- **OpenAI API Key** (for GPT features)
- **Tesseract OCR** (optional, for scanned PDFs)
- **qpdf** (optional, for encrypted PDFs)

## 🎯 Copilot Commands

- **Formal**: "Rewrite formally"
- **Friendly**: "Make it casual"
- **Summarize**: "Summarize this"
- **Translate**: "Translate to Spanish"
- **Custom**: Any natural language instruction

## 🔧 Optional Dependencies

For **full functionality**, install these tools:

### Tesseract OCR (for scanned PDFs)
```cmd
# Using Chocolatey (recommended)
choco install tesseract -y

# Or download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### qpdf (for encrypted PDFs)
```cmd
# Using Chocolatey (recommended)
choco install qpdf -y

# Or download from: https://github.com/qpdf/qpdf/releases
```

## 🧪 Testing

Run the verification script:
```cmd
python verify_setup.py
```

## 🔧 Troubleshooting

### App won't start
- Check if port 8502 is available
- Try running as administrator
- Verify Python installation

### OCR not working
- Install Tesseract OCR
- Add to system PATH
- Restart the application

### PDF unlock failed
- Install qpdf utility
- Add to system PATH
- Try PyMuPDF fallback

## 📞 Support

- **Documentation**: See `MANUAL_INSTALLATION.md`
- **Verification**: Run `python verify_setup.py`
- **Dependencies**: Run `python install_dependencies.py`

## 🔄 Updates

This is version 1.0.0
- Check for updates regularly
- Backup your `.env` file before updating

## 📄 License

This software is provided as-is for educational and personal use.

---

**Made with ❤️ for AI-powered PDF editing**

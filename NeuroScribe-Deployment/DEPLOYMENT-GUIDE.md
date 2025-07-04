# 🚀 NeuroScribe PDF Copilot - Deployment Guide

## 📦 **Quick Start**

### Option 1: Automatic Installation
1. **Double-click `install.bat`**
2. **Edit `.env` file** and add your OpenAI API key
3. **Run `launch.bat`** to start the app
4. **Optional:** Run `create-shortcut.bat` for desktop shortcut

### Option 2: Manual Installation
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set up environment
copy env.template .env
# Edit .env and add your OpenAI API key

# Launch app
streamlit run app.py --server.port 8502
```

## 🔧 **Requirements**

- **Python 3.8+**
- **OpenAI API Key** (get from https://platform.openai.com)
- **Internet connection** for GPT-4 access
- **Optional:** Tesseract OCR for scanned PDFs

## 📁 **File Structure**
```
NeuroScribe-Deployment/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── env.template          # Environment template
├── launch.bat            # Windows launcher
├── install.bat           # Automatic installer
├── create-shortcut.bat   # Desktop shortcut creator
├── src/                  # Source modules
│   ├── __init__.py
│   ├── openai_utils.py   # GPT integration
│   └── pdf_utils.py      # PDF processing
└── README.md             # This file
```

## 🌐 **Access URLs**

After launching, access the app at:
- **Local:** http://localhost:8502
- **Network:** http://[your-ip]:8502

## 🔑 **Environment Setup**

1. **Copy environment template:**
   ```bash
   copy env.template .env
   ```

2. **Edit `.env` file:**
   ```
   OPENAI_API_KEY=sk-your-actual-openai-key-here
   ```

3. **Get OpenAI API Key:**
   - Visit https://platform.openai.com
   - Create account/login
   - Generate API key
   - Add to `.env` file

## 🚀 **Deployment Options**

### Local Development
```bash
launch.bat
```

### Production Server
```bash
# Install as service
pip install streamlit
streamlit run app.py --server.port 8502 --server.address 0.0.0.0
```

### Docker Deployment
```bash
# Build image
docker build -t neuroscribe-copilot .

# Run container
docker run -p 8502:8502 neuroscribe-copilot
```

### Streamlit Cloud
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Deploy automatically

## 🛠 **Troubleshooting**

### Common Issues

**Port already in use:**
```bash
# Kill existing process
netstat -ano | findstr :8502
taskkill /PID [PID] /F
```

**Module not found:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**OpenAI API errors:**
- Check API key in `.env` file
- Verify internet connection
- Check OpenAI account balance

### Logs
- Check terminal output for errors
- Streamlit logs in browser console
- Python error messages in terminal

## 📞 **Support**

For issues or questions:
1. Check this deployment guide
2. Review error messages
3. Verify all requirements are met
4. Check OpenAI API status

## 🎉 **Success Indicators**

✅ App launches without errors  
✅ Can upload PDF files  
✅ GPT processing works  
✅ Can download edited PDFs  
✅ No import errors in terminal  

---

**NeuroScribe PDF Copilot v1.0**  
*Deployed: June 27, 2025* 
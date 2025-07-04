# 🧠 NeuroScribe PDF Copilot Editor

AI-powered PDF editing with GPT-4 and OCR capabilities.

## ✅ Current Status

**App is running successfully!** 🎉

- ✅ All dependencies installed
- ✅ App running on http://localhost:8501
- ✅ OpenAI API integration ready
- ✅ OCR support with Tesseract
- ✅ PDF text extraction and editing

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your OpenAI API key:**
   - Copy `env.template` to `.env`
   - Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`

3. **Run the app:**
   ```bash
   streamlit run app.py --server.port 8501
   ```

4. **Open in browser:**
   - Navigate to: http://localhost:8501

## 🛠️ Features

- **PDF Upload**: Support for text and scanned PDFs
- **AI Copilot**: GPT-powered text editing commands
- **OCR Support**: Automatic text extraction from images
- **Download**: Get your edited PDF back

## 📋 Copilot Commands

- **Formal**: Rewrite text formally
- **Friendly**: Make text casual
- **Summarize**: Summarize content
- **Erase**: Remove text
- **Custom**: Any text editing command

## 🔧 Requirements

- Python 3.7+
- OpenAI API key
- Tesseract OCR (optional, for scanned PDFs)

## 📁 Project Structure

```
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API keys)
├── env.template             # Template for environment setup
├── launch.bat               # Windows launch script
├── launch.sh                # Linux/Mac launch script
└── neuroscribe-pdf-copilot/ # Organized source code
    └── src/
        ├── utils/           # Utility functions
        └── components/      # UI components
```
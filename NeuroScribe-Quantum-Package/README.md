# 🧠 NeuroScribe PDF Copilot Quantum Edition

**AI-powered PDF editing with GPT-4, OCR, and intelligent text removal**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.46.0-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Overview

NeuroScribe PDF Copilot Quantum Edition is an advanced AI-powered PDF editing tool that combines the power of GPT-4, OCR technology, and intelligent image processing to provide seamless PDF manipulation capabilities.

### ✨ Key Features

- **📝 Edit Mode**: AI-powered text editing with GPT-4 integration
- **🧽 Erase Mode**: Intelligent text removal with background restoration
- **🔍 OCR Support**: Automatic text extraction from scanned documents
- **🔓 PDF Unlock**: Handle encrypted and password-protected PDFs
- **📄 Multi-page Preview**: Navigate through complex documents
- **💾 Multiple Export Formats**: PNG, PDF, DOCX export options
- **🔄 Undo/Redo**: Complete history trail for all operations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR (for scanned document support)
- OpenAI API key (for GPT-4 features)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/Njanja2025/NeuroScribe-Copilot-Quantum.git
   cd NeuroScribe-Copilot-Quantum
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**
   - **Windows**: Download from [Tesseract Releases](https://github.com/tesseract-ocr/tesseract/releases)
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr`

4. **Set up OpenAI API key**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

### Launch the Application

#### Option 1: Quick Launch (Windows)
```bash
# Double-click the launcher
launch_quantum.bat
```

#### Option 2: Manual Launch
```bash
streamlit run app_quantum.py --server.port 8501
```

#### Option 3: Restart Clean (if issues)
```bash
restart_app.bat
```

## 🎮 Usage Guide

### 📝 Edit Mode

1. **Upload a PDF** using the file uploader
2. **Enter a command** in the Copilot command field:
   - `"Make this more formal"`
   - `"Summarize this text"`
   - `"Rewrite in a friendly tone"`
   - `"Fix grammar and spelling"`
3. **View the preview** in the Document Preview tab
4. **Download the edited PDF** when satisfied

### 🧽 Erase Mode

1. **Switch to Erase Mode** using the mode selector
2. **Upload a PDF** to process
3. **Use natural language commands**:
   - `"Remove invoice number"`
   - `"Remove date 2023"`
   - `"Remove text 'LTD 2023'"`
4. **Or use manual coordinates** for precise control
5. **Preview the result** and download in your preferred format

### 🔍 OCR Features

- **Automatic detection** of scanned documents
- **Multi-language support** via Tesseract
- **High-accuracy text extraction** with fallback options
- **Unicode character support** for international documents

## 🛠️ Technical Architecture

### Core Components

- **`app_quantum.py`**: Main Streamlit application
- **`src/pdf_utils.py`**: PDF processing and text extraction
- **`src/openai_utils.py`**: GPT-4 integration and text rewriting
- **`src/erase_utils.py`**: AI-powered text removal and restoration

### Dependencies

```txt
streamlit==1.46.0          # Web interface
PyMuPDF==1.26.1           # PDF processing
pytesseract==0.3.10       # OCR interface
opencv-python==4.8.1.78   # Image processing
openai==1.3.7             # GPT-4 API
rembg==2.0.50             # Background removal
pdfplumber==0.11.7        # Text extraction
reportlab==4.4.2          # PDF generation
```

### External Tools

- **Tesseract OCR v5.5.0+**: For scanned document processing
- **OpenAI API**: For GPT-4 text processing

## 📦 Deployment

### Windows Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile app_quantum.py --name "NeuroScribeCopilotQuantum"
```

### Docker Deployment

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy application
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "app_quantum.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🔧 Troubleshooting

### Common Issues

1. **Port 8501 already in use**
   ```bash
   # Kill existing processes
   taskkill /f /im python.exe
   # Restart the app
   restart_app.bat
   ```

2. **Tesseract not found**
   - Ensure Tesseract is installed and in PATH
   - Windows: Install to `C:\Program Files\Tesseract-OCR\`
   - Verify with: `tesseract --version`

3. **OpenAI API errors**
   - Check your API key in `.env` file
   - Ensure sufficient API credits
   - Verify internet connection

4. **PDF processing errors**
   - Try different PDF formats
   - Check file size (recommended < 50MB)
   - Ensure PDF is not corrupted

### Debug Mode

```bash
# Run with debug logging
streamlit run app_quantum.py --server.port 8501 --logger.level debug
```

## 🎯 Advanced Features

### Custom Commands

The Copilot supports natural language commands:

- **Style Commands**: `"Make formal"`, `"Make casual"`, `"Make professional"`
- **Content Commands**: `"Summarize"`, `"Expand"`, `"Simplify"`
- **Format Commands**: `"Fix grammar"`, `"Improve readability"`, `"Add bullet points"`

### Batch Processing

For multiple documents:

1. Process each PDF individually
2. Use consistent commands across documents
3. Download all processed files
4. Combine into a single document if needed

### API Integration

The application can be extended with:

- Custom GPT prompts
- Additional OCR engines
- Cloud storage integration
- Automated workflows

## 📊 Performance

### Recommended Specifications

- **CPU**: Intel i5 or AMD Ryzen 5 (or better)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space
- **GPU**: Optional (CUDA support for faster processing)

### Optimization Tips

- Use smaller PDFs for faster processing
- Close other applications during heavy operations
- Use SSD storage for better I/O performance
- Enable GPU acceleration if available

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone repository
git clone https://github.com/Njanja2025/NeuroScribe-Copilot-Quantum.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_installation.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT-4 API
- **Tesseract** for OCR capabilities
- **Streamlit** for the web framework
- **PyMuPDF** for PDF processing
- **OpenCV** for image processing

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Njanja2025/NeuroScribe-Copilot-Quantum/issues)
- **Documentation**: [Wiki](https://github.com/Njanja2025/NeuroScribe-Copilot-Quantum/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/Njanja2025/NeuroScribe-Copilot-Quantum/discussions)

---

**Made with ❤️ by the NeuroScribe Team**

*Version 1.0.0 - Quantum Edition*
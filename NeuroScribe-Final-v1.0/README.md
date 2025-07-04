# 🧠 NeuroScribe PDF Copilot

**AI-powered PDF editing with GPT-4, OCR, and automated CI/CD deployment.**

[![CI/CD Pipeline](https://github.com/your-username/neuroscribe-pdf-copilot/workflows/NeuroScribe%20Deployment/badge.svg)](https://github.com/your-username/neuroscribe-pdf-copilot/actions)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Features

- **📄 PDF Processing**: Extract text from any PDF (text or scanned)
- **🧠 AI Integration**: GPT-4 powered text editing and summarization
- **📷 OCR Support**: Automatic text recognition for scanned documents
- **🔐 PDF Unlocking**: Handle encrypted and password-protected PDFs
- **🌐 Web Interface**: Beautiful Streamlit-based UI
- **🚀 CI/CD Pipeline**: Automated testing, building, and deployment
- **🐳 Docker Support**: Containerized deployment ready
- **🔒 Security**: Automated security scanning and vulnerability checks

## 📋 Quick Start

### Option 1: Run Locally
```bash
# Clone the repository
git clone https://github.com/your-username/neuroscribe-pdf-copilot.git
cd neuroscribe-pdf-copilot

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py --server.port 8501
```

### Option 2: Docker Deployment
```bash
# Build and run with Docker
docker build -t neuroscribe .
docker run -p 8501:8501 neuroscribe

# Or use Docker Compose
docker-compose up -d
```

### Option 3: Download Executable
1. Go to [Releases](https://github.com/your-username/neuroscribe-pdf-copilot/releases)
2. Download the latest executable
3. Run `NeuroScribeCopilot.exe`

## 🔧 Prerequisites

### System Requirements
- **Python**: 3.8+ (3.10 recommended)
- **Memory**: 4GB RAM minimum
- **Storage**: 1GB free space
- **OS**: Windows 10+, macOS 10.14+, or Linux

### Required Software
- **Tesseract OCR**: For scanned PDF processing
- **QPDF**: For encrypted PDF handling
- **Git**: For version control and CI/CD

### API Keys
- **OpenAI API Key**: For GPT-4 features (optional)
- **GitHub Token**: For CI/CD operations (optional)

## 📦 Installation

### Windows
```bash
# Install Tesseract OCR
winget install -e --id tesseract-ocr.tesseract

# Install QPDF
winget install -e --id QPDF.QPDF

# Install Python dependencies
pip install -r requirements.txt
```

### macOS
```bash
# Install Tesseract OCR
brew install tesseract

# Install QPDF
brew install qpdf

# Install Python dependencies
pip install -r requirements.txt
```

### Linux
```bash
# Install Tesseract OCR
sudo apt-get install tesseract-ocr

# Install QPDF
sudo apt-get install qpdf

# Install Python dependencies
pip install -r requirements.txt
```

## 🚀 Usage

1. **Upload PDF**: Drag and drop or select a PDF file
2. **Process**: The app automatically extracts text and detects if OCR is needed
3. **Edit**: Use AI commands to modify, summarize, or rewrite content
4. **Download**: Get your edited PDF with all changes applied

### AI Commands
- **"Summarize"**: Create a concise summary
- **"Rewrite formally"**: Convert to formal language
- **"Make it casual"**: Convert to casual language
- **"Translate to [language]"**: Translate content
- **"Fix grammar"**: Correct grammar and spelling

## 🔄 CI/CD Pipeline

This project includes a complete CI/CD pipeline that automatically:

### ✅ Testing
- Multi-Python version testing (3.9, 3.10, 3.11)
- Dependency verification
- Unit test execution
- Security scanning

### 🏗️ Building
- Executable creation with PyInstaller
- Docker image building
- Artifact generation

### 🚀 Deployment
- Automated release creation
- Artifact upload to GitHub Releases
- Docker image publishing

### 🔒 Security
- Bandit security analysis
- Safety dependency checking
- Vulnerability scanning

## 📁 Project Structure

```
neuroscribe-pdf-copilot/
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD pipeline
├── src/
│   ├── pdf_utils.py            # PDF processing
│   └── openai_utils.py         # GPT integration
├── app.py                      # Main Streamlit app
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Local deployment
├── requirements.txt            # Python dependencies
├── verify_installations.py     # Dependency checker
├── deploy_to_production.bat    # Deployment script
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Required for GPT features
OPENAI_API_KEY=sk-your_openai_key_here

# Required for CI/CD
GITHUB_TOKEN=ghp_your_github_token_here

# Optional: Custom paths
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
QPDF_PATH=C:\Program Files\qpdf 12.2.0\bin\qpdf.exe
```

### GitHub Secrets
For CI/CD to work, add these secrets to your GitHub repository:

| Secret Name | Description |
|-------------|-------------|
| `GITHUB_TOKEN` | GitHub personal access token |
| `OPENAI_API_KEY` | OpenAI API key for GPT features |

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t neuroscribe-pdf-copilot .
```

### Run Container
```bash
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key \
  neuroscribe-pdf-copilot
```

### Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔒 Security Features

- **Automated Scanning**: Bandit and Safety tools
- **Secret Management**: Environment variables only
- **Dependency Updates**: Automated vulnerability checks
- **Container Security**: Non-root user, minimal base image

## 🛠️ Development

### Local Development
```bash
# Clone repository
git clone https://github.com/your-username/neuroscribe-pdf-copilot.git
cd neuroscribe-pdf-copilot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
streamlit run app.py --server.port 8501
```

### Running Tests
```bash
# Run verification script
python verify_installations.py

# Run unit tests (if available)
python -m pytest tests/

# Run security scans
bandit -r src/
safety check
```

## 📊 Performance

- **PDF Processing**: Up to 100 pages per minute
- **OCR Speed**: ~30 seconds per page (300 DPI)
- **AI Response**: 2-5 seconds per request
- **Memory Usage**: 200-500MB typical

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit**: For the amazing web framework
- **PyMuPDF**: For robust PDF processing
- **Tesseract**: For OCR capabilities
- **OpenAI**: For GPT-4 integration
- **GitHub Actions**: For CI/CD automation

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/neuroscribe-pdf-copilot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/neuroscribe-pdf-copilot/discussions)
- **Documentation**: [Wiki](https://github.com/your-username/neuroscribe-pdf-copilot/wiki)

## 🚀 Deployment Status

[![Deploy to Production](https://github.com/your-username/neuroscribe-pdf-copilot/workflows/Deploy%20to%20Production/badge.svg)](https://github.com/your-username/neuroscribe-pdf-copilot/actions)

---

**Made with ❤️ by the NeuroScribe Team**

*Transform your PDFs with the power of AI! 🧠✨*
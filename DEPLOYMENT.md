# 🚀 NeuroScribe PDF Copilot - Deployment Guide

## 📦 Available Deployment Options

### ✅ Option 1: ZIP Export (Ready)
**File**: `C:\Users\kavha\Documents\NeuroScribe_PDF_Copilot_Backup.zip`

**Usage**:
1. Extract the ZIP file
2. Run `pip install -r requirements.txt`
3. Set up `.env` with your OpenAI API key
4. Run `streamlit run app.py --server.port 8501`

### ✅ Option 2: Docker Container (Ready)
**Files**: `Dockerfile`, `docker-compose.yml`

**Usage**:
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build manually
docker build -t neuroscribe-pdf-copilot .
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key neuroscribe-pdf-copilot
```

### ✅ Option 3: Direct Installation (Ready)
**Location**: `C:\Users\kavha\Documents\NeuroScribe PDF Copilot Editor`

**Usage**:
1. Double-click `launch.bat` (Windows)
2. Or run `./launch.sh` (Linux/Mac)
3. Or manually: `streamlit run app.py --server.port 8501`

## 🔧 Setup Instructions

### 1. Environment Setup
```bash
# Copy environment template
cp env.template .env

# Edit .env and add your OpenAI API key
OPENAI_API_KEY=your_actual_api_key_here
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py --server.port 8501
```

### 4. Access the Application
- **Local**: http://localhost:8501
- **Network**: http://your-ip:8501

## 🐳 Docker Deployment

### Quick Start
```bash
# Clone or extract the project
cd "NeuroScribe PDF Copilot Editor"

# Set environment variable
export OPENAI_API_KEY=your_api_key_here

# Run with Docker Compose
docker-compose up --build
```

### Manual Docker Build
```bash
# Build the image
docker build -t neuroscribe-pdf-copilot .

# Run the container
docker run -d \
  --name neuroscribe-app \
  -p 8501:8501 \
  -e OPENAI_API_KEY=your_api_key_here \
  neuroscribe-pdf-copilot
```

## 🌐 Cloud Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Set environment variables
4. Deploy automatically

### Heroku
1. Add `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Deploy using Heroku CLI or GitHub integration

### AWS/GCP/Azure
Use the Docker container with your preferred cloud platform's container service.

## 📋 Requirements

### System Requirements
- Python 3.7+
- 2GB RAM minimum
- 1GB disk space

### Dependencies
- streamlit
- openai
- PyMuPDF (fitz)
- pytesseract
- Pillow (PIL)
- python-dotenv

### Optional
- Tesseract OCR (for scanned PDFs)
- Docker (for containerized deployment)

## 🔍 Troubleshooting

### Common Issues
1. **OpenAI API Key Error**: Ensure `.env` file exists with correct API key
2. **Tesseract Not Found**: Install Tesseract OCR or use text-only PDFs
3. **Port Already in Use**: Change port in launch command
4. **Dependencies Missing**: Run `pip install -r requirements.txt`

### Logs
- Check terminal output for error messages
- Streamlit logs are displayed in the terminal
- Docker logs: `docker logs neuroscribe-app`

## 📞 Support

For issues or questions:
1. Check the README.md file
2. Review error logs
3. Verify environment setup
4. Test with a simple PDF first

---

**🎉 Your NeuroScribe PDF Copilot is ready for deployment!** 
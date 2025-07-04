#!/usr/bin/env python3
"""
NeuroScribe Copilot Quantum Edition Launcher
Features: Edit Mode + Erase Mode + AI Avatar (coming soon)
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def print_banner():
    """Print the Quantum Edition banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🧠 NEUROSCRIBE COPILOT                    ║
    ║                        QUANTUM EDITION                       ║
    ║                                                              ║
    ║  🎯 MODES:                                                   ║
    ║  📝 Edit Mode: AI-powered text editing with GPT-4           ║
    ║  🧽 Erase Mode: Remove text with background restoration     ║
    ║  🔊 Avatar Mode: Voice commands (coming soon)               ║
    ║                                                              ║
    ║  🚀 POWER FEATURES:                                          ║
    ║  ✅ AI-Inpaint background restoration                        ║
    ║  ✅ Seamless erase with visual match                         ║
    ║  ✅ Precision bounding box targeting                         ║
    ║  ✅ Export to PNG, PDF, or DOCX formats                      ║
    ║  ✅ Undo / Redo history trail                                ║
    ║  ✅ Multi-page processing                                     ║
    ║  ✅ OCR support for scanned documents                        ║
    ║  ✅ PDF unlocking and decryption                             ║
    ║                                                              ║
    ║  🧬 TECH UNDER THE HOOD:                                     ║
    ║  • cv2.inpaint() and rembg for intelligent content filling  ║
    ║  • OpenCV contour tracing for exact word block erase        ║
    ║  • PIL with alpha masking to preserve transparency          ║
    ║  • GPT-4 integration for smart erase suggestions            ║
    ║                                                              ║
    ║  🎮 ERASE COMMAND SYNTAX:                                    ║
    ║  • "Remove invoice number" → highlights and erases          ║
    ║  • "Remove date 2023" → finds and removes date              ║
    ║  • "Remove text 'LTD 2023'" → precise text removal          ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Map package names to their import names
    package_imports = {
        'streamlit': 'streamlit',
        'openai': 'openai', 
        'PyMuPDF': 'fitz',  # PyMuPDF imports as fitz
        'pytesseract': 'pytesseract',
        'opencv-python': 'cv2',  # opencv-python imports as cv2
        'rembg': 'rembg',
        'numpy': 'numpy',
        'scikit-image': 'skimage'  # scikit-image imports as skimage
    }
    
    missing_packages = []
    
    for package, import_name in package_imports.items():
        try:
            __import__(import_name)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_tesseract():
    """Check if Tesseract OCR is available"""
    print("\n🔍 Checking Tesseract OCR...")
    
    # Check common installation paths
    tesseract_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        "tesseract"  # If in PATH
    ]
    
    for path in tesseract_paths:
        try:
            result = subprocess.run([path, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip().split()[1]
                print(f"✅ Tesseract found: {path}")
                print(f"   Version: {version}")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            continue
    
    print("⚠️  Tesseract OCR not found")
    print("💡 Download from: https://github.com/UB-Mannheim/tesseract/wiki")
    print("   OCR features will be limited for scanned PDFs")
    return False

def check_openai_key():
    """Check if OpenAI API key is configured"""
    print("\n🔍 Checking OpenAI API key...")
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            content = f.read()
            if "OPENAI_API_KEY" in content and "sk-" in content:
                print("✅ OpenAI API key found in .env file")
                return True
    
    # Check environment variable
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key found in environment")
        return True
    
    print("⚠️  OpenAI API key not found")
    print("💡 Create .env file with: OPENAI_API_KEY=your_key_here")
    print("   Or set environment variable")
    return False

def check_qpdf():
    print("\n🔍 Checking qpdf...")
    try:
        result = subprocess.run(["qpdf", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.splitlines()[0]
            print(f"✅ qpdf found: {version}")
            return True
    except Exception:
        pass
    print("⚠️  qpdf not found. PDF unlock will use PyMuPDF fallback.")
    print("💡 Download: https://github.com/qpdf/qpdf/releases")
    return False

def start_streamlit():
    """Start the Streamlit app"""
    print("\n🚀 Starting NeuroScribe Copilot Quantum Edition...")
    
    # Find available port
    ports = [8506, 8507, 8508, 8509, 8510]
    selected_port = None
    
    for port in ports:
        try:
            result = subprocess.run(f"netstat -ano | findstr :{port}", 
                                  shell=True, capture_output=True, text=True)
            if not result.stdout.strip():
                selected_port = port
                break
        except:
            continue
    
    if not selected_port:
        print("❌ No available ports found")
        return False
    
    print(f"🌐 Starting on port {selected_port}...")
    
    # Start Streamlit in background
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app_quantum.py",
            "--server.port", str(selected_port),
            "--server.headless", "true"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print(f"✅ Streamlit started successfully!")
            print(f"🌐 Local URL: http://localhost:{selected_port}")
            print(f"🌐 Network URL: http://192.168.0.30:{selected_port}")
            
            # Open browser
            def open_browser():
                time.sleep(2)
                webbrowser.open(f"http://localhost:{selected_port}")
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            print("\n🎮 QUANTUM EDITION FEATURES:")
            print("📝 Edit Mode: Upload PDF → Enter command → Get AI-edited version")
            print("🧽 Erase Mode: Upload PDF → Select 'Erase Mode' → Remove text")
            print("🔄 History: Undo/Redo your erase operations")
            print("📤 Export: Download as PNG, PDF, or DOCX")
            
            print(f"\n⏹️  Press Ctrl+C to stop the server")
            
            # Keep the process running
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping server...")
                process.terminate()
                process.wait()
                print("✅ Server stopped")
            
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Failed to start Streamlit")
            print(f"Error: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        return False

def main():
    """Main launcher function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        return
    
    # Check Tesseract (optional but recommended)
    tesseract_ok = check_tesseract()
    
    # Check OpenAI key (optional but recommended)
    openai_ok = check_openai_key()
    
    # Check qpdf (optional but recommended)
    qpdf_ok = check_qpdf()
    
    print("\n" + "="*60)
    print("🚀 READY TO LAUNCH QUANTUM EDITION!")
    print("="*60)
    
    # Start the app
    if start_streamlit():
        print("\n🎉 NeuroScribe Copilot Quantum Edition launched successfully!")
    else:
        print("\n❌ Failed to launch Quantum Edition")

if __name__ == "__main__":
    main() 
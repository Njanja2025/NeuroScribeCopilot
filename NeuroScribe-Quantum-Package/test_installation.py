#!/usr/bin/env python3
"""
Test script to verify all NeuroScribe PDF Copilot installations and functionality
"""

import sys
import subprocess
import importlib
from pathlib import Path

def print_status(message, status="INFO"):
    """Print formatted status message"""
    colors = {
        "SUCCESS": "✅",
        "ERROR": "❌", 
        "WARNING": "⚠️",
        "INFO": "ℹ️"
    }
    print(f"{colors.get(status, 'ℹ️')} {message}")

def test_python_version():
    """Test Python version"""
    print_status("Testing Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - SUCCESS", "SUCCESS")
        return True
    else:
        print_status(f"Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+", "ERROR")
        return False

def test_package_imports():
    """Test all required package imports"""
    print_status("Testing package imports...")
    
    packages = [
        ("streamlit", "Web interface"),
        ("fitz", "PDF processing (PyMuPDF)"),
        ("pytesseract", "OCR interface"),
        ("cv2", "Image processing (OpenCV)"),
        ("PIL", "Image processing (Pillow)"),
        ("numpy", "Numerical computing"),
        ("pdfplumber", "PDF text extraction"),
        ("reportlab", "PDF generation"),
        ("rembg", "Background removal"),
        ("skimage", "Image processing (scikit-image)")
    ]
    
    all_success = True
    for package, description in packages:
        try:
            importlib.import_module(package)
            print_status(f"{package} ({description}) - SUCCESS", "SUCCESS")
        except ImportError as e:
            print_status(f"{package} ({description}) - FAILED: {e}", "ERROR")
            all_success = False
    
    return all_success

def test_app_modules():
    """Test application-specific modules"""
    print_status("Testing application modules...")
    
    modules = [
        ("src.pdf_utils", "PDF utilities"),
        ("src.openai_utils", "OpenAI integration"),
        ("src.erase_utils", "Text erasure utilities")
    ]
    
    all_success = True
    for module, description in modules:
        try:
            importlib.import_module(module)
            print_status(f"{module} ({description}) - SUCCESS", "SUCCESS")
        except ImportError as e:
            print_status(f"{module} ({description}) - FAILED: {e}", "ERROR")
            all_success = False
    
    return all_success

def test_tesseract():
    """Test Tesseract OCR installation"""
    print_status("Testing Tesseract OCR...")
    
    try:
        result = subprocess.run(["tesseract", "--version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print_status(f"Tesseract OCR - SUCCESS: {version_line}", "SUCCESS")
            return True
        else:
            print_status("Tesseract OCR - FAILED: Command returned error", "ERROR")
            return False
    except FileNotFoundError:
        print_status("Tesseract OCR - FAILED: Not found in PATH", "ERROR")
        return False
    except subprocess.TimeoutExpired:
        print_status("Tesseract OCR - FAILED: Command timed out", "ERROR")
        return False

def test_streamlit():
    """Test Streamlit installation"""
    print_status("Testing Streamlit...")
    
    try:
        import streamlit
        print_status(f"Streamlit {streamlit.__version__} - SUCCESS", "SUCCESS")
        return True
    except ImportError as e:
        print_status(f"Streamlit - FAILED: {e}", "ERROR")
        return False

def test_pdf_processing():
    """Test PDF processing capabilities"""
    print_status("Testing PDF processing...")
    
    try:
        import fitz
        import io
        
        # Create a simple test PDF
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 50), "Test PDF for NeuroScribe")
        
        # Get PDF as bytes
        pdf_bytes = doc.write()
        doc.close()
        
        # Test reading it back
        doc2 = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = doc2.load_page(0).get_text()
        doc2.close()
        
        if "Test PDF" in text:
            print_status("PDF processing - SUCCESS", "SUCCESS")
            return True
        else:
            print_status("PDF processing - FAILED: Text extraction issue", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"PDF processing - FAILED: {e}", "ERROR")
        return False

def main():
    """Run all tests"""
    print("🧪 NeuroScribe PDF Copilot - Installation Test")
    print("=" * 50)
    
    tests = [
        ("Python Version", test_python_version),
        ("Package Imports", test_package_imports),
        ("App Modules", test_app_modules),
        ("Tesseract OCR", test_tesseract),
        ("Streamlit", test_streamlit),
        ("PDF Processing", test_pdf_processing)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"Test failed with exception: {e}", "ERROR")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print_status("🎉 ALL TESTS PASSED! Installation is complete and ready.", "SUCCESS")
        print("\n🚀 Ready to run: streamlit run app_quantum.py --server.port 8501")
    else:
        print_status("⚠️ Some tests failed. Please check the errors above.", "WARNING")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 
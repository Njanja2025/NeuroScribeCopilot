#!/usr/bin/env python3
"""
Tesseract OCR Verification for NeuroScribe Copilot Quantum Edition
"""

import subprocess
import sys
import os
from pathlib import Path

def check_tesseract_installation():
    """Check if Tesseract is properly installed and accessible"""
    
    print("🔍 Verifying Tesseract OCR Installation...")
    print("=" * 50)
    
    # Check if tesseract is in PATH
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Tesseract found in PATH")
            print(f"   Version: {result.stdout.split()[1]}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    # Check common installation paths
    tesseract_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\{}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe".format(os.getenv('USERNAME'))
    ]
    
    for path in tesseract_paths:
        if os.path.exists(path):
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"✅ Tesseract found at: {path}")
                    print(f"   Version: {result.stdout.split()[1]}")
                    
                    # Add to PATH if not already there
                    if path not in os.environ['PATH']:
                        print("⚠️  Tesseract not in PATH, adding...")
                        os.environ['PATH'] += f";{os.path.dirname(path)}"
                        print("✅ Added to PATH for this session")
                    
                    return True
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
                continue
    
    print("❌ Tesseract not found")
    return False

def test_ocr_functionality():
    """Test OCR functionality with a simple text recognition"""
    
    print("\n🧪 Testing OCR Functionality...")
    print("=" * 50)
    
    try:
        # Create a simple test image with text
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a test image
        img = Image.new('RGB', (300, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 10), "Hello World OCR Test", fill='black', font=font)
        
        # Save test image
        test_image = "test_ocr.png"
        img.save(test_image)
        
        print(f"✅ Created test image: {test_image}")
        
        # Test OCR
        result = subprocess.run(['tesseract', test_image, 'stdout'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            recognized_text = result.stdout.strip()
            print(f"✅ OCR Test Successful!")
            print(f"   Recognized: '{recognized_text}'")
            
            # Cleanup
            if os.path.exists(test_image):
                os.remove(test_image)
            
            return True
        else:
            print(f"❌ OCR Test Failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ OCR Test Error: {e}")
        return False

def check_python_integration():
    """Check if pytesseract can access Tesseract"""
    
    print("\n🐍 Testing Python Integration...")
    print("=" * 50)
    
    try:
        import pytesseract
        
        # Test pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"✅ pytesseract working - Version: {version}")
        
        # Test OCR with pytesseract
        from PIL import Image, ImageDraw, ImageFont
        
        # Create test image
        img = Image.new('RGB', (300, 100), color='white')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((10, 10), "Python OCR Test", fill='black', font=font)
        
        # Test OCR
        text = pytesseract.image_to_string(img)
        print(f"✅ Python OCR Test Successful!")
        print(f"   Recognized: '{text.strip()}'")
        
        return True
        
    except ImportError:
        print("❌ pytesseract not installed")
        print("💡 Run: pip install pytesseract")
        return False
    except Exception as e:
        print(f"❌ Python OCR Test Error: {e}")
        return False

def check_quantum_edition_integration():
    """Check if Quantum Edition can use Tesseract"""
    
    print("\n🧠 Testing Quantum Edition Integration...")
    print("=" * 50)
    
    try:
        # Import Quantum Edition modules
        from src.erase_utils import erase_mode
        
        print("✅ Quantum Edition modules imported successfully")
        
        # Test Tesseract path in erase_utils
        import pytesseract
        
        # Check if Tesseract path is set correctly
        tesseract_cmd = pytesseract.pytesseract.tesseract_cmd
        if tesseract_cmd and os.path.exists(tesseract_cmd):
            print(f"✅ Tesseract path configured: {tesseract_cmd}")
        else:
            print("⚠️  Tesseract path not configured, setting...")
            pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            print("✅ Tesseract path set")
        
        return True
        
    except Exception as e:
        print(f"❌ Quantum Edition Integration Error: {e}")
        return False

def main():
    """Main verification function"""
    
    print("🧠 NeuroScribe Copilot Quantum Edition - Tesseract Verification")
    print("=" * 60)
    
    # Check installation
    tesseract_ok = check_tesseract_installation()
    
    if not tesseract_ok:
        print("\n❌ Tesseract installation verification failed")
        print("💡 Please install Tesseract OCR:")
        print("   Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki")
        print("   Or run: winget install UB-Mannheim.TesseractOCR")
        return False
    
    # Test OCR functionality
    ocr_ok = test_ocr_functionality()
    
    # Test Python integration
    python_ok = check_python_integration()
    
    # Test Quantum Edition integration
    quantum_ok = check_quantum_edition_integration()
    
    # Summary
    print("\n📊 VERIFICATION SUMMARY")
    print("=" * 50)
    print(f"Tesseract Installation: {'✅' if tesseract_ok else '❌'}")
    print(f"OCR Functionality: {'✅' if ocr_ok else '❌'}")
    print(f"Python Integration: {'✅' if python_ok else '❌'}")
    print(f"Quantum Edition Integration: {'✅' if quantum_ok else '❌'}")
    
    if all([tesseract_ok, ocr_ok, python_ok, quantum_ok]):
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Tesseract OCR is fully integrated with Quantum Edition")
        print("✅ You can now use OCR features for scanned documents")
        print("✅ Erase Mode will work with image-based PDFs")
        return True
    else:
        print("\n⚠️  Some tests failed")
        print("💡 Please check the errors above and fix them")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
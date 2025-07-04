import os
import sys
import subprocess
from pathlib import Path
from termcolor import colored

def print_status(label, ok, msg=None):
    color = 'green' if ok else 'red'
    status = 'OK' if ok else 'MISSING'
    print(colored(f"[{status}] {label}", color), end='')
    if msg:
        print(f" - {msg}")
    else:
        print()

def check_tesseract():
    paths = [
        r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
        r"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe",
        "tesseract"
    ]
    for path in paths:
        try:
            result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.splitlines()[0]
                print_status("Tesseract OCR", True, version)
                return True
        except Exception:
            continue
    print_status("Tesseract OCR", False, "Not found in PATH or common locations.")
    return False

def check_qpdf():
    try:
        result = subprocess.run(["qpdf", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.splitlines()[0]
            print_status("qpdf", True, version)
            return True
    except Exception:
        pass
    print_status("qpdf", False, "Not found in PATH.")
    return False

def check_python_packages():
    required = {
        'streamlit': 'streamlit',
        'openai': 'openai',
        'PyMuPDF': 'fitz',
        'pytesseract': 'pytesseract',
        'opencv-python': 'cv2',
        'rembg': 'rembg',
        'numpy': 'numpy',
        'scikit-image': 'skimage',
    }
    all_ok = True
    for pkg, imp in required.items():
        try:
            mod = __import__(imp)
            version = getattr(mod, '__version__', 'OK')
            print_status(pkg, True, version)
        except Exception:
            print_status(pkg, False)
            all_ok = False
    return all_ok

def check_openai_key():
    env_file = Path('.env')
    key = os.getenv('OPENAI_API_KEY')
    if not key and env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.strip().startswith('OPENAI_API_KEY='):
                key = line.split('=', 1)[1].strip()
                break
    if key and key.startswith('sk-'):
        print_status('OpenAI API Key', True)
        return True
    print_status('OpenAI API Key', False, 'Not found in env or .env file')
    return False

def main():
    print("\n==== NeuroScribe Quantum Environment Verification ====")
    ok = True
    if not check_tesseract():
        ok = False
    if not check_qpdf():
        ok = False
    if not check_python_packages():
        ok = False
    if not check_openai_key():
        ok = False
    print("\n=====================================================")
    if ok:
        print(colored("All systems GO! Your environment is 100% ready.", 'green'))
        sys.exit(0)
    else:
        print(colored("Some requirements are missing. Please fix the above and re-run.", 'red'))
        sys.exit(1)

if __name__ == "__main__":
    try:
        from termcolor import colored
    except ImportError:
        def colored(text, color):
            return text
    main() 
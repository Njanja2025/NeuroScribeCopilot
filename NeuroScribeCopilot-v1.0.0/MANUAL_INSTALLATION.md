# 🧠 NeuroScribe PDF Copilot - Manual Installation Guide

## ✅ Current Status
Your NeuroScribe PDF Copilot is **already running successfully** on http://localhost:8502!

The app works with basic PDFs, but for **full functionality** (OCR and PDF unlock), you need to install two additional tools.

---

## 🔍 Step 1: Install Tesseract OCR (for scanned PDFs)

### Option A: Download from Official Source
1. **Go to:** https://github.com/UB-Mannheim/tesseract/wiki
2. **Download:** `tesseract-ocr-w64-setup-5.3.3.20231005.exe`
3. **Run as Administrator**
4. **Install to:** `C:\Program Files\Tesseract-OCR\`
5. **✅ IMPORTANT:** Check "Add Tesseract to system PATH"
6. **Restart your terminal/command prompt**

### Option B: Using Chocolatey (if available)
```powershell
# Open PowerShell as Administrator
choco install tesseract -y
```

### Verify Installation
Open a **new** Command Prompt and run:
```cmd
tesseract --version
```
You should see: `tesseract 5.3.3.20231005`

---

## 🔓 Step 2: Install qpdf (for encrypted PDFs)

### Option A: Using Chocolatey (Recommended)
```powershell
# Open PowerShell as Administrator
choco install qpdf -y
```

### Option B: Manual Installation
1. **Go to:** https://github.com/qpdf/qpdf/releases
2. **Download:** `qpdf-11.9.1-bin-msvc.zip`
3. **Extract to:** `C:\Program Files\qpdf\`
4. **Add to PATH:** `C:\Program Files\qpdf\bin\`

### Verify Installation
Open a **new** Command Prompt and run:
```cmd
qpdf --version
```
You should see: `qpdf version 11.9.1`

---

## 🔧 Step 3: Add to System PATH (if manual install)

If you installed manually and didn't add to PATH:

1. **Press:** `Windows + S`
2. **Search:** "Environment Variables"
3. **Click:** "Edit the system environment variables"
4. **Click:** "Environment Variables"
5. **Under "System Variables", find and Edit:** `Path`
6. **Click:** `New`
7. **Add these paths:**
   ```
   C:\Program Files\Tesseract-OCR\
   C:\Program Files\qpdf\bin\
   ```
8. **Click:** `OK` on all dialogs
9. **Restart your terminal**

---

## 🧪 Step 4: Verify Everything Works

Run the verification script:
```cmd
python verify_setup.py
```

All checks should show ✅ for a complete setup.

---

## 🚀 Step 5: Test Your App

1. **Open:** http://localhost:8502
2. **Test with different PDF types:**
   - **Regular PDF:** Should work immediately
   - **Scanned PDF:** Needs Tesseract (OCR)
   - **Encrypted PDF:** Needs qpdf (unlock)

3. **Try Copilot commands:**
   - "Summarize this page"
   - "Rewrite formally"
   - "Make it casual"

---

## 🔧 Troubleshooting

### "Tesseract not found"
- ✅ Check if installed to correct location
- ✅ Verify PATH is set correctly
- ✅ Restart terminal after installation
- ✅ Run as Administrator if needed

### "qpdf not found"
- ✅ Check if extracted to `C:\Program Files\qpdf\`
- ✅ Verify `bin` folder exists
- ✅ Add `C:\Program Files\qpdf\bin\` to PATH
- ✅ Restart terminal

### "App won't start"
- ✅ Check if port 8502 is available
- ✅ Kill existing process: `taskkill /PID 6744 /F`
- ✅ Run: `python launcher.py`

### "PDF processing error"
- ✅ The app has fallback mechanisms
- ✅ Basic PDFs work without external tools
- ✅ Install Tesseract/qpdf for advanced features

---

## 📦 Final Packaging

Once everything works, create your distribution package:

```cmd
# Create ZIP package
python setup_installer.py

# Build executable (optional)
cd NeuroScribeCopilot-Package\exe-build
.\build_exe.bat
```

---

## 🎉 Success!

Your NeuroScribe PDF Copilot now has:
- ✅ **Basic PDF processing** (works immediately)
- ✅ **OCR for scanned PDFs** (with Tesseract)
- ✅ **PDF unlock capability** (with qpdf)
- ✅ **GPT-4 integration** (set your API key)
- ✅ **Bulletproof error handling**

**Ready for distribution!** 🚀 
import os
import streamlit as st
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import fitz
from src.openai_utils import rewrite_with_gpt
from src.pdf_utils import extract_text_blocks, rebuild_pdf
import pytesseract
import shutil

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="NeuroScribe Copilot", layout="wide")
st.title("🧠 NeuroScribe PDF Copilot")

with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/6C63FF/brain.png", width=80)
    st.markdown("""
    # 🧠 NeuroScribe Copilot
    **AI-powered PDF editing with GPT-4 and OCR.**
    - Upload a PDF (text or scanned)
    - Edit or use Copilot commands
    - Download your new PDF
    ---
    **Copilot Commands:**
    • Formal: Rewrite formally
    • Friendly: Make it casual
    • Summarize: Summarize text
    • Erase: Remove text
    ---
    **OCR Support:**
    - Scanned/image PDFs are auto-read with Tesseract OCR
    - [Tesseract Download](https://github.com/tesseract-ocr/tesseract)
    ---
    **🔐 PDF Unlock:**
    - Automatically detects encrypted PDFs
    - Attempts to unlock using qpdf/PyMuPDF
    - Supports password-protected documents
    ---
    **🧠 Bulletproof Processing:**
    - Auto-fallback to OCR for image-based pages
    - Handles encrypted PDFs automatically
    - Robust error handling and recovery
    """)

uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])
command = st.text_input("🧠 Command to Copilot (optional)", placeholder="e.g. Summarize this page")

# Tesseract check and user guidance
if shutil.which("tesseract"):
    try:
        pytesseract.get_tesseract_version()
        st.success("✅ Tesseract OCR detected and ready")
    except Exception as e:
        st.warning("⚠️ Tesseract found but not working properly. OCR features may be limited.")
else:
    st.warning("⚠️ Tesseract OCR is not installed or not found in PATH. OCR for scanned PDFs will not work. See sidebar for install link.")

# Check for qpdf
try:
    import subprocess
    subprocess.run(["qpdf", "--version"], capture_output=True, check=True)
    st.success("✅ qpdf detected - PDF unlock capability available")
except:
    st.info("ℹ️ qpdf not found - PDF unlock will use PyMuPDF fallback")

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()
    
    # Ensure we have valid PDF data
    if not pdf_bytes:
        st.error("❌ Invalid PDF file: No data received")
    else:
        try:
            # Use the bulletproof extract_text_blocks function directly with bytes
            blocks = extract_text_blocks(pdf_bytes)
            
            if blocks:
                st.success(f"✅ Extracted {len(blocks)} text blocks from PDF")
                
                # Display extracted text
                st.subheader("📄 Extracted Text")
                for i, block in enumerate(blocks[:5]):  # Show first 5 blocks
                    block_type = block.get('type', 'unknown')
                    st.text_area(f"Block {i+1} ({block_type})", block.get('text', ''), height=100)
                
                if command:
                    st.subheader("🤖 Processing with GPT...")
                    # Process each block with GPT
                    processed_blocks = []
                    for block in blocks:
                        original_text = block.get('text', '')
                        if original_text.strip() and not original_text.startswith("OCR failed"):
                            processed_text = rewrite_with_gpt(original_text)
                            processed_blocks.append({
                                'text': processed_text,
                                'page': block.get('page', 1),
                                'bbox': block.get('bbox', [0, 0, 100, 100]),
                                'type': 'processed'
                            })
                    
                    if processed_blocks:
                        # Rebuild PDF with processed content
                        pdf_output = rebuild_pdf(processed_blocks)
                        st.download_button("📥 Download Edited PDF", pdf_output, "edited.pdf", mime="application/pdf")
                        st.success("✅ PDF processing complete!")
                    else:
                        st.error("❌ No text was processed")
                else:
                    st.info("💡 Enter a command above to process the PDF with GPT")
            else:
                st.warning("⚠️ No text blocks found in the PDF")
                
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")
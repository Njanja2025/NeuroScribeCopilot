import os
import streamlit as st
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
import fitz
from src.openai_utils import rewrite_with_gpt
from src.pdf_utils import extract_text_blocks, rebuild_pdf, pdf_to_images
from src.erase_utils import erase_mode
import pytesseract
import shutil
import cv2
import numpy as np

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="NeuroScribe Copilot Quantum", layout="wide")
st.title("🧠 NeuroScribe Copilot Quantum Edition")

# Initialize session state
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = 'edit'
if 'processed_images' not in st.session_state:
    st.session_state.processed_images = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0

with st.sidebar:
    st.image("https://img.icons8.com/ios-filled/100/6C63FF/brain.png", width=80)
    st.markdown("""
    # 🧠 NeuroScribe Copilot Quantum
    **AI-powered PDF editing with GPT-4, OCR, and Erase Mode.**
    
    ## 🎯 Modes:
    - **📝 Edit Mode**: Modify text with AI
    - **🧽 Erase Mode**: Remove text with background restoration
    - **🔊 Avatar Mode**: Voice commands (coming soon)
    
    ---
    **Copilot Commands:**
    • Formal: Rewrite formally
    • Friendly: Make it casual
    • Summarize: Summarize text
    • Erase: Remove text "invoice number"
    
    ---
    **🧽 Erase Mode Features:**
    ✅ AI-Inpaint background restoration
    ✅ Seamless erase with visual match
    ✅ Precision bounding box targeting
    ✅ Export to PNG, PDF, or DOCX
    ✅ Undo / Redo history trail
    
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

# Mode selection
mode = st.selectbox(
    "🎯 Select Mode",
    ["📝 Edit Mode", "🧽 Erase Mode"],
    index=0 if st.session_state.current_mode == 'edit' else 1
)

st.session_state.current_mode = 'edit' if mode == "📝 Edit Mode" else 'erase'

uploaded_file = st.file_uploader("📄 Upload PDF", type=["pdf"])

# Tesseract check and user guidance
def check_tesseract_robust():
    """Robust Tesseract detection"""
    import subprocess
    
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
                return True, f"✅ Tesseract OCR detected: {result.stdout.split()[1]}"
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            continue
    
    return False, "⚠️ Tesseract OCR is not installed or not found in PATH. OCR for scanned PDFs will not work. See sidebar for install link."

# Check Tesseract with robust detection
tesseract_available, tesseract_message = check_tesseract_robust()
if tesseract_available:
    st.success(tesseract_message)
else:
    st.warning(tesseract_message)

# qpdf check and user guidance
def check_qpdf_status():
    import subprocess
    try:
        result = subprocess.run(["qpdf", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.splitlines()[0]
            return True, f"✅ qpdf detected: {version}"
    except Exception:
        pass
    return False, "⚠️ qpdf not found. PDF unlock will use PyMuPDF fallback. [Download qpdf](https://github.com/qpdf/qpdf/releases)"

qpdf_available, qpdf_message = check_qpdf_status()
if qpdf_available:
    st.success(qpdf_message)
else:
    st.warning(qpdf_message)

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()
    
    # Ensure we have valid PDF data
    if not pdf_bytes:
        st.error("❌ Invalid PDF file: No data received")
    else:
        if st.session_state.current_mode == 'edit':
            # Edit Mode
            st.subheader("📝 Edit Mode - AI-Powered Text Editing")
            command = st.text_input("🧠 Command to Copilot (optional)", placeholder="e.g. Summarize this page")
            
            # Convert PDF to images for preview
            try:
                preview_images = pdf_to_images(pdf_bytes)
                if preview_images:
                    st.success(f"✅ Loaded {len(preview_images)} pages for preview")
                    
                    # Create tabs for preview and text
                    tab1, tab2 = st.tabs(["📄 Document Preview", "📝 Extracted Text"])
                    
                    with tab1:
                        # Page navigation for preview
                        if len(preview_images) > 1:
                            preview_page = st.selectbox(
                                "📄 Select Page to Preview", 
                                range(len(preview_images)), 
                                index=0,
                                format_func=lambda x: f"Page {x+1}"
                            )
                        else:
                            preview_page = 0
                        
                        # Display preview image
                        st.image(preview_images[preview_page], caption=f"Page {preview_page + 1}", use_column_width=True)
                    
                    with tab2:
                        try:
                            # Use the bulletproof extract_text_blocks function directly with bytes
                            blocks = extract_text_blocks(pdf_bytes)
                            
                            if blocks:
                                st.success(f"✅ Extracted {len(blocks)} text blocks from PDF")
                                
                                # Display extracted text
                                for i, block in enumerate(blocks[:5]):  # Show first 5 blocks
                                    block_type = block.get('type', 'unknown')
                                    st.text_area(f"Block {i+1} ({block_type})", block.get('text', ''), height=100)
                                
                                if command:
                                    st.success(f"✅ Copilot command received: {command}")
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
                                        st.info("🧪 Edit preview applied. Please scroll to see updated content.")
                                    else:
                                        st.error("❌ No text was processed")
                                else:
                                    st.info("💡 Enter a command above to process the PDF with GPT")
                            else:
                                st.warning("⚠️ No text blocks found in the PDF")
                                
                        except Exception as e:
                            st.error(f"❌ Error processing PDF: {str(e)}")
                else:
                    st.error("❌ Could not load PDF for preview")
                    
            except Exception as e:
                st.error(f"❌ Error loading PDF preview: {str(e)}")
        
        else:
            # Erase Mode
            st.subheader("🧽 Erase Mode - AI-Powered Text Removal")
            
            # Erase command input
            erase_command = st.text_input(
                "🧽 Erase Command", 
                placeholder="e.g. Remove invoice number, Remove date 2023, Remove text 'LTD 2023'"
            )
            
            # Manual coordinates input
            st.markdown("**Or manually specify coordinates:**")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                x1 = st.number_input("X1", min_value=0, value=0)
            with col2:
                y1 = st.number_input("Y1", min_value=0, value=0)
            with col3:
                x2 = st.number_input("X2", min_value=0, value=100)
            with col4:
                y2 = st.number_input("Y2", min_value=0, value=100)
            
            # Convert PDF to images
            try:
                images = pdf_to_images(pdf_bytes)
                
                if images:
                    st.success(f"✅ Converted PDF to {len(images)} images")
                    
                    # Page navigation
                    if len(images) > 1:
                        st.session_state.current_page = st.selectbox(
                            "📄 Select Page", 
                            range(len(images)), 
                            index=st.session_state.current_page,
                            format_func=lambda x: f"Page {x+1}"
                        )
                    
                    current_image = images[st.session_state.current_page]
                    
                    # Display current image
                    st.subheader(f"📄 Page {st.session_state.current_page + 1}")
                    
                    # Display image
                    st.image(current_image, caption=f"Page {st.session_state.current_page + 1}", use_column_width=True)
                    
                    # Process erase commands
                    if erase_command or (x1 != 0 or y1 != 0 or x2 != 100 or y2 != 100):
                        st.subheader("🧽 Processing Erase Commands...")
                        
                        # Convert PIL image to OpenCV format
                        processed_image = np.array(current_image)
                        if len(processed_image.shape) == 3 and processed_image.shape[2] == 3:
                            processed_image = cv2.cvtColor(processed_image, cv2.COLOR_RGB2BGR)
                        
                        # Process command-based erasure
                        if erase_command:
                            processed_image, erased_regions = erase_mode.erase_text_by_command(
                                processed_image, erase_command
                            )
                            
                            if erased_regions:
                                st.success(f"✅ Erased {len(erased_regions)} text regions")
                                for region in erased_regions:
                                    st.info(f"Erased: '{region['text']}' at {region['bbox']}")
                            else:
                                st.warning("⚠️ No matching text found for erasure")
                        
                        # Process coordinate-based erasure
                        if x1 != 0 or y1 != 0 or x2 != 100 or y2 != 100:
                            coordinates = [[x1, y1, x2, y2]]
                            processed_image = erase_mode.erase_text_by_coordinates(
                                processed_image, coordinates
                            )
                            st.success("✅ Erased text at specified coordinates")
                        
                        # Add to history
                        erase_mode.add_to_history(processed_image, f"Erase: {erase_command or 'manual coordinates'}")
                        
                        # Display processed image
                        st.subheader("✅ Processed Image")
                        display_processed = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
                        st.image(display_processed, caption="After erasure", use_column_width=True)
                        
                        # Update session state
                        if len(st.session_state.processed_images) <= st.session_state.current_page:
                            st.session_state.processed_images.extend([None] * (st.session_state.current_page + 1 - len(st.session_state.processed_images)))
                        st.session_state.processed_images[st.session_state.current_page] = processed_image
                        
                        # Export options
                        st.subheader("📤 Export Options")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            # Export as PNG
                            png_bytes = cv2.imencode('.png', processed_image)[1].tobytes()
                            st.download_button(
                                "📥 Download as PNG",
                                png_bytes,
                                f"erased_page_{st.session_state.current_page + 1}.png",
                                mime="image/png"
                            )
                        
                        with col2:
                            # Export as PDF
                            if st.button("📥 Download as PDF"):
                                # Create PDF from processed image
                                pdf_output = erase_mode.images_to_pdf([processed_image])
                                if pdf_output:
                                    st.download_button(
                                        "📥 Download PDF",
                                        pdf_output,
                                        f"erased_page_{st.session_state.current_page + 1}.pdf",
                                        mime="application/pdf"
                                    )
                        
                        with col3:
                            # Export all pages as PDF
                            if st.button("📥 Download All Pages"):
                                all_images = []
                                for i, img in enumerate(images):
                                    if i < len(st.session_state.processed_images) and st.session_state.processed_images[i] is not None:
                                        all_images.append(st.session_state.processed_images[i])
                                    else:
                                        all_images.append(img)
                                
                                pdf_output = erase_mode.images_to_pdf(all_images)
                                if pdf_output:
                                    st.download_button(
                                        "📥 Download All Pages PDF",
                                        pdf_output,
                                        "erased_document.pdf",
                                        mime="application/pdf"
                                    )
                    
                    # Undo/Redo controls
                    st.subheader("🔄 History Controls")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("↶ Undo"):
                            undone_image = erase_mode.undo()
                            if undone_image is not None:
                                st.session_state.processed_images[st.session_state.current_page] = undone_image
                                st.success("✅ Undone")
                                st.rerun()
                    
                    with col2:
                        if st.button("↷ Redo"):
                            redone_image = erase_mode.redo()
                            if redone_image is not None:
                                st.session_state.processed_images[st.session_state.current_page] = redone_image
                                st.success("✅ Redone")
                                st.rerun()
                    
                    # History info
                    history_info = erase_mode.get_history_info()
                    st.info(f"History: {history_info['current_step']}/{history_info['total_steps']} steps")
                    
                else:
                    st.error("❌ Failed to convert PDF to images")
                    
            except Exception as e:
                st.error(f"❌ Error in Erase Mode: {str(e)}") 
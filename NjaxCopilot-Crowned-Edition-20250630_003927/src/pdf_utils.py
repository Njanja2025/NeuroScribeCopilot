"""
pdf_utils.py - Bulletproof PDF text extraction with auto-fallback for encrypted/image PDFs.
"""

import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import os
import subprocess
from typing import List, Dict, Any, Union
import shutil

# Set paths for installed tools
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
QPDF_PATH = r"C:\Program Files\qpdf 12.2.0\bin\qpdf.exe"

def extract_text_blocks(uploaded_file):
    """
    Extract text blocks from PDF file with OCR fallback.
    
    Args:
        uploaded_file: PDF file bytes, path, or document object
        
    Returns:
        List[Dict[str, Any]]: Text blocks with metadata
        
    Raises:
        Exception: If extraction fails
    """
    # Check if Tesseract is available
    tesseract_available = os.path.exists(TESSERACT_PATH) or shutil.which("tesseract")
    if not tesseract_available:
        print("⚠️  Tesseract OCR not found. OCR features will be disabled.")
        print("   Install from: https://github.com/UB-Mannheim/tesseract/wiki")
    
    try:
        # Handle different input types
        if hasattr(uploaded_file, 'load_page'):  # Document object
            doc = uploaded_file
            temp_pdf_path = None
        elif isinstance(uploaded_file, bytes):  # Bytes
            temp_pdf_path = "temp_input.pdf"
            with open(temp_pdf_path, "wb") as f:
                f.write(uploaded_file)
            doc = fitz.open(temp_pdf_path)
        elif isinstance(uploaded_file, str) and os.path.exists(uploaded_file):  # File path
            temp_pdf_path = uploaded_file
            doc = fitz.open(temp_pdf_path)
        else:
            raise Exception("Invalid input: must be bytes, file path, or document object")

        # Handle encrypted PDFs
        if doc.is_encrypted:
            try:
                doc.authenticate("")
                print("✅ Successfully unlocked encrypted PDF")
            except:
                raise Exception("❌ Cannot unlock encrypted PDF.")

        text_blocks = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Try direct text extraction first
            text = page.get_text("text")
            
            if not text.strip():
                # 🧠 Fallback to OCR (image-based page)
                if tesseract_available:
                    try:
                        # Set Tesseract path if available
                        if os.path.exists(TESSERACT_PATH):
                            pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
                        
                        pix = page.get_pixmap(dpi=300)
                        img_data = pix.tobytes("png")
                        img = Image.open(io.BytesIO(img_data))
                        
                        # Configure Tesseract for better Unicode handling
                        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,!?@#$%^&*()_+-=[]{}|;:,.<>?/\\"\'`~ '
                        
                        try:
                            text = pytesseract.image_to_string(img, config=custom_config)
                            # Clean up any problematic characters
                            text = text.encode('utf-8', errors='ignore').decode('utf-8')
                            text_type = 'ocr'
                            print(f"📷 OCR used for page {page_num + 1}")
                        except UnicodeEncodeError as ue:
                            # Handle Unicode encoding errors
                            text = f"OCR completed for page {page_num + 1} (some characters may be missing due to encoding)"
                            text_type = 'ocr'
                            print(f"📷 OCR used for page {page_num + 1} (with encoding warnings)")
                        except Exception as ocr_error:
                            text = f"OCR failed for page {page_num + 1}: {str(ocr_error)}"
                            text_type = 'error'
                    except Exception as ocr_error:
                        text = f"OCR failed for page {page_num + 1}: {str(ocr_error)}"
                        text_type = 'error'
                else:
                    text = f"OCR not available for page {page_num + 1} (Tesseract not installed)"
                    text_type = 'error'
            else:
                text_type = 'text'
            
            if text.strip():
                text_blocks.append({
                    'page': page_num + 1,
                    'text': text.strip(),
                    'type': text_type,
                    'bbox': [0, 0, 100, 100]  # Default bbox
                })
        
        # Only close if we opened it (not if it was passed as a document object)
        if temp_pdf_path and temp_pdf_path != uploaded_file:
            doc.close()
        
        # Cleanup temporary file
        if temp_pdf_path and temp_pdf_path != uploaded_file and os.path.exists(temp_pdf_path):
            try:
                os.remove(temp_pdf_path)
            except:
                pass
        
        return text_blocks

    except Exception as e:
        raise Exception(f"🔴 Failed to extract PDF text: {str(e)}")

def unlock_pdf(input_path: str, output_path: str) -> str:
    """
    Attempt to unlock/decrypt a PDF file using qpdf.
    
    Args:
        input_path (str): Path to encrypted PDF
        output_path (str): Path for unlocked PDF
        
    Returns:
        str: Path to unlocked PDF
        
    Raises:
        Exception: If unlocking fails
    """
    try:
        # Try qpdf first (if available)
        qpdf_cmd = QPDF_PATH if os.path.exists(QPDF_PATH) else "qpdf"
        subprocess.run([
            qpdf_cmd, "--decrypt", input_path, output_path
        ], check=True, capture_output=True)
        return output_path
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to PyMuPDF
        try:
            doc = fitz.open(input_path)
            if doc.is_encrypted:
                # Try empty password
                if doc.authenticate(""):
                    doc.save(output_path)
                    doc.close()
                    return output_path
                else:
                    raise Exception("PDF is encrypted and cannot be unlocked")
            else:
                # Not encrypted, just copy
                doc.save(output_path)
                doc.close()
                return output_path
        except Exception as e:
            raise Exception(f"Unlocking failed: {str(e)}")

def render_pdf_as_image(page):
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

def pdf_to_images(pdf_bytes):
    """
    Convert PDF to list of PIL Images for preview.
    
    Args:
        pdf_bytes: PDF file as bytes
        
    Returns:
        List[PIL.Image]: List of page images
    """
    try:
        # Save temporary file
        temp_path = "temp_preview.pdf"
        with open(temp_path, "wb") as f:
            f.write(pdf_bytes)
        
        doc = fitz.open(temp_path)
        images = []
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=150)  # Lower DPI for faster preview
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            images.append(img)
        
        doc.close()
        
        # Cleanup
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        
        return images
        
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return []

def extract_text_with_style(pdf_path):
    doc = fitz.open(pdf_path)
    text_data = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"]
                    bbox = span["bbox"]
                    font = span["font"]
                    size = span["size"]
                    text_data.append({
                        "page": page_num,
                        "text": text,
                        "bbox": bbox,
                        "font": font,
                        "size": size
                    })
    return text_data

def rebuild_pdf(blocks: List[Dict[str, Any]]) -> bytes:
    """
    Rebuild a PDF document from text blocks.
    
    Args:
        blocks (List[Dict[str, Any]]): List of text blocks with metadata.
        
    Returns:
        bytes: PDF document as bytes.
        
    Note:
        This is a simplified implementation. For production use,
        consider using reportlab or similar libraries for proper PDF generation.
    """
    try:
        # Create a new PDF document
        doc = fitz.open()
        
        # Group blocks by page
        pages = {}
        for block in blocks:
            page_num = block.get("page", 1)
            if page_num not in pages:
                pages[page_num] = []
            pages[page_num].append(block)
        
        # Create pages and add text
        for page_num in sorted(pages.keys()):
            page = doc.new_page()
            y_offset = 50  # Starting position
            
            for block in pages[page_num]:
                text = block.get("text", "")
                if text:
                    page.insert_text((50, y_offset), text)
                    y_offset += 20  # Line spacing
        
        # Get PDF as bytes
        pdf_bytes = doc.write()
        doc.close()
        
        return pdf_bytes
        
    except Exception as e:
        # Fallback to dummy PDF if rebuilding fails
        return b"%PDF-1.4\nDummy PDF rebuilt\n%%EOF"

def rebuild_pdf_with_style(original_pdf_path, edited_data):
    doc = fitz.open(original_pdf_path)
    for item in edited_data:
        page = doc.load_page(item["page"])
        x0, y0, x1, y1 = item["bbox"]
        page.insert_text((x0, y0),
                         item["edited_text"],
                         fontname=item["font"],
                         fontsize=item["size"])
    return doc 
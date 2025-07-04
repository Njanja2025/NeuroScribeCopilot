import fitz
from PIL import Image
import pytesseract
import io

def render_pdf_as_image(page):
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

def extract_text_blocks(doc):
    """Extract text blocks from PDF document"""
    text_blocks = []
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Try to extract text directly first
        text = page.get_text()
        
        if text.strip():  # If text was found
            text_blocks.append({
                'page': page_num,
                'text': text,
                'type': 'text'
            })
        else:  # If no text found, try OCR
            try:
                # Convert page to image
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Use OCR to extract text
                ocr_text = pytesseract.image_to_string(img)
                text_blocks.append({
                    'page': page_num,
                    'text': ocr_text,
                    'type': 'ocr'
                })
            except Exception as e:
                text_blocks.append({
                    'page': page_num,
                    'text': f"Error extracting text: {str(e)}",
                    'type': 'error'
                })
    
    return text_blocks

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

def rebuild_pdf(edited_text):
    """Create a simple PDF with the edited text"""
    doc = fitz.open()
    page = doc.new_page()
    
    # Add the edited text to the page
    page.insert_text((50, 50), edited_text, fontsize=12)
    
    # Convert to bytes
    pdf_bytes = doc.write()
    doc.close()
    
    return pdf_bytes

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
"""
erase_utils.py - AI-powered text erasure with background restoration
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import fitz
import io
import os
from typing import List, Dict, Any, Tuple, Optional
import pytesseract
from rembg import remove
import tempfile

def erase_text_from_image(image_path, coordinates, inpaint_radius=3):
    """
    Erases text from the image using OpenCV inpainting.

    Args:
        image_path (str): Path to the image file.
        coordinates (list of tuples): List of (x, y, w, h) tuples where text appears.
        inpaint_radius (int): Radius for inpainting.

    Returns:
        np.array: Image with text erased.
    """
    image = cv2.imread(image_path)
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    for (x, y, w, h) in coordinates:
        mask[y:y+h, x:x+w] = 255

    erased = cv2.inpaint(image, mask, inpaint_radius, cv2.INPAINT_TELEA)
    return erased

class EraseMode:
    """
    AI-powered text erasure with background restoration
    """
    
    def __init__(self):
        self.history = []
        self.current_step = -1
        self.max_history = 10
        
    def detect_text_regions(self, image: np.ndarray) -> List[Dict[str, Any]]:
        """
        Detect text regions in image using OCR and contour detection
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of text regions with bounding boxes and text content
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply threshold to get binary image
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Find contours
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            text_regions = []
            
            for contour in contours:
                # Filter small contours
                if cv2.contourArea(contour) > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Extract region for OCR
                    roi = gray[y:y+h, x:x+w]
                    
                    # OCR the region
                    try:
                        text = pytesseract.image_to_string(roi, config='--psm 8').strip()
                        if text and len(text) > 1:
                            text_regions.append({
                                'bbox': [x, y, x+w, y+h],
                                'text': text,
                                'confidence': 0.8
                            })
                    except:
                        continue
            
            return text_regions
            
        except Exception as e:
            print(f"Error detecting text regions: {e}")
            return []
    
    def create_mask_from_bbox(self, image: np.ndarray, bbox: List[int], 
                            expand: int = 5) -> np.ndarray:
        """
        Create a mask for text removal from bounding box
        
        Args:
            image: Input image
            bbox: Bounding box [x1, y1, x2, y2]
            expand: Pixels to expand the mask
            
        Returns:
            Binary mask for inpainting
        """
        height, width = image.shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)
        
        x1, y1, x2, y2 = bbox
        
        # Expand the bounding box
        x1 = max(0, x1 - expand)
        y1 = max(0, y1 - expand)
        x2 = min(width, x2 + expand)
        y2 = min(height, y2 + expand)
        
        # Create rectangular mask
        mask[y1:y2, x1:x2] = 255
        
        return mask
    
    def inpaint_text_region(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Remove text using OpenCV inpainting
        
        Args:
            image: Input image
            mask: Binary mask of text regions
            
        Returns:
            Image with text removed
        """
        try:
            # Use TELEA algorithm for better results
            result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
            return result
        except Exception as e:
            print(f"Error in inpainting: {e}")
            return image
    
    def ai_enhanced_removal(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Enhanced text removal using AI techniques
        
        Args:
            image: Input image
            mask: Binary mask of text regions
            
        Returns:
            Image with enhanced text removal
        """
        try:
            # Convert to PIL for better processing
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            # Apply mask
            mask_pil = Image.fromarray(mask)
            
            # Use rembg for background removal in masked area
            # This helps with complex backgrounds
            masked_region = np.array(pil_image)
            masked_region[mask == 0] = [255, 255, 255]  # White background
            
            # Convert back to BGR for OpenCV
            masked_region_bgr = cv2.cvtColor(masked_region, cv2.COLOR_RGB2BGR)
            
            # Apply inpainting
            result = self.inpaint_text_region(masked_region_bgr, mask)
            
            # Blend with original image
            alpha = 0.8
            blended = cv2.addWeighted(image, 1-alpha, result, alpha, 0)
            
            return blended
            
        except Exception as e:
            print(f"Error in AI-enhanced removal: {e}")
            return self.inpaint_text_region(image, mask)
    
    def erase_text_by_command(self, image: np.ndarray, command: str) -> Tuple[np.ndarray, List[Dict]]:
        """
        Erase text based on natural language command
        
        Args:
            image: Input image
            command: Natural language command (e.g., "Remove invoice number")
            
        Returns:
            Tuple of (processed_image, erased_regions)
        """
        # Detect text regions
        text_regions = self.detect_text_regions(image)
        
        # Simple keyword matching (can be enhanced with GPT)
        command_lower = command.lower()
        erased_regions = []
        
        for region in text_regions:
            text = region['text'].lower()
            
            # Check if region matches command
            should_erase = False
            
            if 'invoice' in command_lower and any(word in text for word in ['invoice', 'inv', 'bill']):
                should_erase = True
            elif 'date' in command_lower and any(word in text for word in ['date', '2023', '2024']):
                should_erase = True
            elif 'number' in command_lower and any(word in text for word in ['no', 'number', '#']):
                should_erase = True
            elif 'name' in command_lower and len(text.split()) <= 3:
                should_erase = True
            elif 'remove' in command_lower and 'text' in command_lower:
                should_erase = True
            
            if should_erase:
                mask = self.create_mask_from_bbox(image, region['bbox'])
                image = self.ai_enhanced_removal(image, mask)
                erased_regions.append(region)
        
        return image, erased_regions
    
    def erase_text_by_coordinates(self, image: np.ndarray, coordinates: List[List[int]]) -> np.ndarray:
        """
        Erase text at specific coordinates
        
        Args:
            image: Input image
            coordinates: List of bounding boxes [x1, y1, x2, y2]
            
        Returns:
            Processed image
        """
        for bbox in coordinates:
            mask = self.create_mask_from_bbox(image, bbox)
            image = self.ai_enhanced_removal(image, mask)
        
        return image
    
    def pdf_to_images(self, pdf_bytes: bytes) -> List[np.ndarray]:
        """
        Convert PDF to list of images
        
        Args:
            pdf_bytes: PDF file as bytes
            
        Returns:
            List of images as numpy arrays
        """
        try:
            # Save PDF temporarily
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
                tmp_file.write(pdf_bytes)
                tmp_path = tmp_file.name
            
            # Open PDF
            doc = fitz.open(tmp_path)
            images = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Render page as image
                pix = page.get_pixmap(dpi=300)
                img_data = pix.tobytes("png")
                
                # Convert to numpy array
                pil_image = Image.open(io.BytesIO(img_data))
                img_array = np.array(pil_image)
                
                # Convert RGB to BGR for OpenCV
                if len(img_array.shape) == 3:
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                
                images.append(img_array)
            
            doc.close()
            
            # Cleanup
            os.unlink(tmp_path)
            
            return images
            
        except Exception as e:
            print(f"Error converting PDF to images: {e}")
            return []
    
    def images_to_pdf(self, images: List[np.ndarray]) -> bytes:
        """
        Convert list of images back to PDF
        
        Args:
            images: List of images as numpy arrays
            
        Returns:
            PDF as bytes
        """
        try:
            # Create new PDF
            doc = fitz.open()
            
            for img_array in images:
                # Convert BGR to RGB
                if len(img_array.shape) == 3:
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
                
                # Convert to PIL
                pil_image = Image.fromarray(img_array)
                
                # Save to bytes
                img_bytes = io.BytesIO()
                pil_image.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                
                # Create PDF page
                page = doc.new_page()
                
                # Insert image
                page.insert_image(page.rect, stream=img_bytes.getvalue())
            
            # Get PDF as bytes
            pdf_bytes = doc.write()
            doc.close()
            
            return pdf_bytes
            
        except Exception as e:
            print(f"Error converting images to PDF: {e}")
            return b""
    
    def add_to_history(self, image: np.ndarray, action: str):
        """
        Add current state to history for undo/redo
        
        Args:
            image: Current image state
            action: Description of action performed
        """
        # Remove future history if we're not at the end
        if self.current_step < len(self.history) - 1:
            self.history = self.history[:self.current_step + 1]
        
        # Add to history
        self.history.append({
            'image': image.copy(),
            'action': action
        })
        
        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        self.current_step = len(self.history) - 1
    
    def undo(self) -> Optional[np.ndarray]:
        """
        Undo last action
        
        Returns:
            Previous image state or None if no undo available
        """
        if self.current_step > 0:
            self.current_step -= 1
            return self.history[self.current_step]['image'].copy()
        return None
    
    def redo(self) -> Optional[np.ndarray]:
        """
        Redo last undone action
        
        Returns:
            Next image state or None if no redo available
        """
        if self.current_step < len(self.history) - 1:
            self.current_step += 1
            return self.history[self.current_step]['image'].copy()
        return None
    
    def get_history_info(self) -> Dict[str, Any]:
        """
        Get information about undo/redo history
        
        Returns:
            Dictionary with history information
        """
        return {
            'can_undo': self.current_step > 0,
            'can_redo': self.current_step < len(self.history) - 1,
            'total_steps': len(self.history),
            'current_step': self.current_step + 1
        }

# Global instance
erase_mode = EraseMode() 
import streamlit as st
import fitz
import os
from PIL import Image
import io
import base64
from src.pdf_utils import extract_text_blocks, extract_text_with_style
from src.openai_utils import rewrite_with_gpt
from src.erase_utils import erase_text_from_image
import tempfile

# Page configuration
st.set_page_config(
    page_title="NeuroScribe Copilot - Professional Edition",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Professional Header */
    .main-header {
        background: linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 2px solid #ffd700;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    .header-title {
        color: #ffd700;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
    }
    
    .header-subtitle {
        color: #ffffff;
        text-align: center;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2d2d2d 0%, #1a1a1a 100%);
        border-right: 2px solid #ffd700;
    }
    
    /* Mode Selection */
    .mode-selector {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ffd700;
        margin-bottom: 1rem;
    }
    
    /* Document Preview */
    .doc-preview {
        background: #ffffff;
        border: 2px solid #ffd700;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        min-height: 600px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #1a1a1a;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.5);
    }
    
    /* Status Messages */
    .status-success {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffd700;
    }
    
    .status-info {
        background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ffd700;
    }
    
    /* File Upload */
    .uploadedFile {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        border: 2px solid #ffd700;
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Text Areas */
    .stTextArea textarea {
        background: #2d2d2d;
        color: #ffffff;
        border: 1px solid #ffd700;
        border-radius: 8px;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #ffd700 0%, #ffed4e 100%);
    }
</style>
""", unsafe_allow_html=True)

# Professional Header
st.markdown("""
<div class="main-header">
    <h1 class="header-title">🧠 NeuroScribe Copilot</h1>
    <p class="header-subtitle">Professional Edition - AI-Powered Document Processing</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "Edit Mode"
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'document_preview' not in st.session_state:
    st.session_state.document_preview = None
if 'processed_text' not in st.session_state:
    st.session_state.processed_text = ""
if 'edit_history' not in st.session_state:
    st.session_state.edit_history = []
if 'current_page' not in st.session_state:
    st.session_state.current_page = 0

# Sidebar for mode selection and controls
with st.sidebar:
    st.markdown("### 🎯 Mode Selection")
    
    mode = st.selectbox(
        "Choose your mode:",
        ["Edit Mode", "Erase Mode"],
        index=0 if st.session_state.current_mode == "Edit Mode" else 1
    )
    
    st.session_state.current_mode = mode
    
    st.markdown("---")
    
    # File upload
    st.markdown("### 📁 Document Upload")
    uploaded_file = st.file_uploader(
        "Upload your PDF document",
        type=['pdf'],
        help="Upload a PDF file to process"
    )
    
    if uploaded_file:
        st.session_state.uploaded_file = uploaded_file
        
        # Show file info
        file_size = len(uploaded_file.getvalue()) / 1024  # KB
        st.info(f"📄 **File:** {uploaded_file.name}\n📏 **Size:** {file_size:.1f} KB")
        
        # Create document preview
        try:
            pdf_bytes = uploaded_file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            
            # Get first page for preview
            page = doc[st.session_state.current_page]
            pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
            img_data = pix.tobytes("png")
            
            # Convert to PIL Image for display
            img = Image.open(io.BytesIO(img_data))
            
            # Resize for preview
            img.thumbnail((400, 600), Image.Resampling.LANCZOS)
            
            # Convert to base64 for display
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            
            st.session_state.document_preview = img_str
            
            # Page navigation
            if len(doc) > 1:
                st.markdown("### 📄 Page Navigation")
                page_num = st.selectbox(
                    "Select page:",
                    range(len(doc)),
                    index=st.session_state.current_page
                )
                st.session_state.current_page = page_num
                
                # Update preview for selected page
                page = doc[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                img.thumbnail((400, 600), Image.Resampling.LANCZOS)
                buffered = io.BytesIO()
                img.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                st.session_state.document_preview = img_str
            
            doc.close()
            
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
    
    st.markdown("---")
    
    # Status and info
    st.markdown("### ℹ️ Status")
    if st.session_state.uploaded_file:
        st.success("✅ Document loaded")
    else:
        st.info("📁 No document uploaded")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    if st.button("🔄 Refresh Preview"):
        st.rerun()
    
    if st.button("🗑️ Clear All"):
        st.session_state.uploaded_file = None
        st.session_state.document_preview = None
        st.session_state.processed_text = ""
        st.session_state.edit_history = []
        st.rerun()

# Main content area
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📄 Document Preview")
    
    if st.session_state.document_preview:
        st.markdown(f"""
        <div class="doc-preview">
            <img src="data:image/png;base64,{st.session_state.document_preview}" 
                 style="max-width: 100%; height: auto; border-radius: 8px;">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="doc-preview">
            <div style="text-align: center; color: #666;">
                <h3>📄 Document Preview</h3>
                <p>Upload a PDF to see the preview here</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("### 🎮 Processing Panel")
    
    if st.session_state.current_mode == "Edit Mode":
        st.markdown("#### 📝 Edit Mode")
        st.markdown("Use AI to edit and transform your document text.")
        
        if st.session_state.uploaded_file:
            # Extract text
            if st.button("🔍 Extract Text"):
                with st.spinner("Extracting text from document..."):
                    try:
                        pdf_bytes = st.session_state.uploaded_file.getvalue()
                        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                        blocks = extract_text_blocks(doc)
                        st.session_state.processed_text = "\n\n".join(blocks)
                        st.success("✅ Text extracted successfully!")
                        doc.close()
                    except Exception as e:
                        st.error(f"Error extracting text: {str(e)}")
            
            # Show extracted text
            if st.session_state.processed_text:
                st.markdown("#### 📄 Extracted Text")
                st.text_area(
                    "Document Text:",
                    value=st.session_state.processed_text,
                    height=200,
                    key="extracted_text"
                )
                
                # AI editing
                st.markdown("#### 🤖 AI Editing")
                command = st.text_input(
                    "Enter your editing command:",
                    placeholder="e.g., 'Make this more formal', 'Translate to Spanish', 'Summarize this text'"
                )
                
                if command and st.button("✨ Apply AI Edit"):
                    with st.spinner("Processing with AI..."):
                        try:
                            edited_text = rewrite_with_gpt(command, st.session_state.processed_text)
                            st.session_state.edit_history.append({
                                'command': command,
                                'original': st.session_state.processed_text,
                                'edited': edited_text
                            })
                            st.session_state.processed_text = edited_text
                            st.success("✅ AI edit applied successfully!")
                        except Exception as e:
                            st.error(f"Error applying AI edit: {str(e)}")
                
                # Edit history
                if st.session_state.edit_history:
                    st.markdown("#### 📚 Edit History")
                    for i, edit in enumerate(st.session_state.edit_history):
                        with st.expander(f"Edit {i+1}: {edit['command']}"):
                            st.text_area("Original:", edit['original'], height=100, key=f"orig_{i}")
                            st.text_area("Edited:", edit['edited'], height=100, key=f"edit_{i}")
                            if st.button(f"🔄 Restore Edit {i+1}", key=f"restore_{i}"):
                                st.session_state.processed_text = edit['edited']
                                st.rerun()
                
                # Export options
                st.markdown("#### 💾 Export Options")
                col_export1, col_export2 = st.columns(2)
                
                with col_export1:
                    if st.button("📄 Export as PDF"):
                        st.info("PDF export feature coming soon!")
                
                with col_export2:
                    if st.button("📝 Export as Text"):
                        st.download_button(
                            label="📥 Download Text",
                            data=st.session_state.processed_text,
                            file_name="edited_document.txt",
                            mime="text/plain"
                        )
    
    else:  # Erase Mode
        st.markdown("#### 🧽 Erase Mode")
        st.markdown("Remove text from your document with AI-powered inpainting.")
        
        if st.session_state.uploaded_file:
            st.markdown("##### 🎯 Erase Options")
            
            erase_method = st.radio(
                "Choose erase method:",
                ["Natural Language", "Manual Coordinates", "AI Suggestions"]
            )
            
            if erase_method == "Natural Language":
                erase_command = st.text_input(
                    "Describe what to remove:",
                    placeholder="e.g., 'Remove invoice number', 'Remove date 2023'"
                )
                
                if erase_command and st.button("🧽 Erase Text"):
                    with st.spinner("Processing erase command..."):
                        st.info("Erase functionality will be implemented with AI inpainting")
            
            elif erase_method == "Manual Coordinates":
                col_coord1, col_coord2 = st.columns(2)
                with col_coord1:
                    x1 = st.number_input("X1:", min_value=0, value=100)
                    y1 = st.number_input("Y1:", min_value=0, value=100)
                with col_coord2:
                    x2 = st.number_input("X2:", min_value=0, value=200)
                    y2 = st.number_input("Y2:", min_value=0, value=150)
                
                if st.button("🧽 Erase Selected Area"):
                    with st.spinner("Erasing selected area..."):
                        st.info("Manual erase functionality will be implemented")
            
            else:  # AI Suggestions
                st.markdown("AI will analyze your document and suggest text to remove.")
                if st.button("🤖 Get AI Suggestions"):
                    with st.spinner("Analyzing document..."):
                        st.info("AI suggestion feature coming soon!")
            
            # Export options for erase mode
            st.markdown("##### 💾 Export Options")
            col_erase1, col_erase2, col_erase3 = st.columns(3)
            
            with col_erase1:
                if st.button("🖼️ Export as PNG"):
                    st.info("PNG export coming soon!")
            
            with col_erase2:
                if st.button("📄 Export as PDF"):
                    st.info("PDF export coming soon!")
            
            with col_erase3:
                if st.button("📝 Export as DOCX"):
                    st.info("DOCX export coming soon!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>🧠 <strong>NeuroScribe Copilot Professional Edition</strong> | Powered by AI | Made with ❤️</p>
    <p>Version 1.0 | © 2025 NeuroScribe Technologies</p>
</div>
""", unsafe_allow_html=True) 